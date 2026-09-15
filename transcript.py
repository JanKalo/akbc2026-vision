"""Append-only log of every LLM interaction, for post-hoc audit.

Subject prompts and answers are recoverable from result rows; judge calls
are not — the judge builds its messages internally and persists only a
label and a sha. This is the only record of what a judge was shown.

Every call through `llm.call_with_meta` lands here, including cache hits,
so the log reflects what a run consumed rather than what it paid for.
Destination `$CM_TRANSCRIPT`, else `logs/llm_transcript.jsonl`; set to
"off" to disable (the test suite does). Prompts only, never credentials.
"""
from __future__ import annotations

import contextvars
import json
import os
import threading
import time
from contextlib import contextmanager
from pathlib import Path

_DEFAULT = Path("logs/llm_transcript.jsonl")
_lock = threading.Lock()
_handle: list = []          # [dest, fh] — one slot; the
                            # destination changes at most once per run
_context: contextvars.ContextVar[dict] = contextvars.ContextVar(
    "transcript_context", default={})


def path() -> Path | None:
    """Destination, or None when logging is disabled."""
    raw = os.environ.get("CM_TRANSCRIPT", "")
    if raw.strip().lower() in ("off", "0", "false", "none"):
        return None
    return Path(raw) if raw.strip() else _DEFAULT


def default_to(run_dir: Path) -> Path | None:
    """Point the transcript at this run unless the operator overrode it.

    Generation and offline judging are separate invocations, so without a
    per-run default each phase lands wherever CM_TRANSCRIPT happened to
    point — leaving no single file that holds everything about one run,
    which is the only thing the transcript is for.
    """
    if not os.environ.get("CM_TRANSCRIPT"):
        os.environ["CM_TRANSCRIPT"] = str(Path(run_dir) / "transcript.jsonl")
    return path()


@contextmanager
def context(**fields):
    """Tag calls made inside the block. Per-task (contextvars), so the
    generation and judging thread pools do not race on the tags."""
    token = _context.set({**_context.get(), **fields})
    try:
        yield
    finally:
        _context.reset(token)


def log(model: str, messages: list[dict], response: dict, meta: dict) -> None:
    """Append one interaction. Never raises — an audit log must not be
    able to take down a run that is otherwise succeeding."""
    dest = path()
    if dest is None:
        return
    try:
        from .llm import get_text, prompt_sha256
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            **_context.get(),
            "model": model,
            "resolved_model": response.get("model"),
            "prompt_sha256": prompt_sha256(messages),
            "messages": messages,
            "response_text": get_text(response),
            "usage": response.get("usage"),
            "cache_hit": meta.get("cache_hit"),
            "retry_count": meta.get("retry_count"),
            "request_params": meta.get("request_params"),
            "request_ts": meta.get("request_ts"),
            "response_ts": meta.get("response_ts"),
        }
        line = json.dumps(entry, ensure_ascii=False, default=str)
        with _lock:
            # One handle per destination, opened once: reopening per call
            # costs ~17x the write itself, and this runs under a global
            # lock on every LLM call including cache replays.
            if not _handle or _handle[0] != dest:
                if _handle:
                    _handle[1].close()
                dest.parent.mkdir(parents=True, exist_ok=True)
                _handle[:] = [dest, dest.open("a", buffering=1)]
            _handle[1].write(line + "\n")
    except Exception:  # noqa: BLE001
        pass


def read(dest: Path | None = None) -> list[dict]:
    """Load the transcript."""
    dest = dest or path()
    if dest is None or not dest.exists():
        return []
    return [json.loads(l) for l in dest.read_text().splitlines() if l.strip()]
