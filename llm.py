"""Thin LiteLLM wrapper with on-disk response cache."""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
import urllib.request
from pathlib import Path
from typing import Any, Iterable

import litellm
from dotenv import load_dotenv

import transcript

load_dotenv()

# Overridable so a cold end-to-end run can exercise the live API path
# without discarding or polluting the warm cache.
CACHE_DIR = Path(os.environ.get("CM_LLM_CACHE", ".cache/llm"))

# Server-side/transport errors worth retrying (in addition to rate limits).
_TRANSIENT_ERRORS = tuple(
    exc for exc in (
        getattr(litellm, name, None)
        for name in ("InternalServerError", "ServiceUnavailableError",
                     "APIConnectionError", "Timeout")
    ) if isinstance(exc, type) and issubclass(exc, BaseException)
)

_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)
_JSON_OBJ_RE = re.compile(r"\{.*\}", re.DOTALL)


def _key(model: str, messages: list[dict], extra: dict) -> str:
    payload = json.dumps(
        {"model": model, "messages": messages, "extra": extra},
        sort_keys=True,
        ensure_ascii=False,
        default=str,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def call_with_meta(
    model: str,
    messages: list[dict],
    *,
    temperature: float | None = 0.0,
    max_tokens: int = 2000,
    response_format: dict | None = None,
    use_cache: bool = True,
    cache_salt: str | None = None,
    empty_response_retries: int = 0,
    max_retries: int = 3,
    **kw: Any,
) -> tuple[dict, dict]:
    """Like call(), but also returns request metadata for row provenance:
    request_ts / response_ts (ISO, UTC), retry_count, cache_hit, and the
    request params as sent. temperature=None omits the parameter (provider
    default) — used for resampling. cache_salt enters the cache key but is
    never sent to the API."""
    extra = {"temperature": temperature, "max_tokens": max_tokens,
             "response_format": response_format, **kw}
    # Only key the salt when set — existing cache entries must keep their keys.
    if cache_salt is not None:
        extra["cache_salt"] = cache_salt
    cache_path = CACHE_DIR / f"{_key(model, messages, extra)}.json"
    request_params = {"temperature": temperature, "max_tokens": max_tokens,
                      "response_format": response_format,
                      "cache_salt": cache_salt, **kw}

    # A cached EMPTY completion must not satisfy a request that asked for
    # empty-response retries: the blanks this policy exists for were
    # produced and cached by the very runs that motivated it, so rerunning
    # the affected cells replayed them and changed nothing.
    if (use_cache and cache_path.exists() and empty_response_retries > 0
            and not get_text(json.loads(cache_path.read_text()))):
        use_cache = False
    if use_cache and cache_path.exists():
        now = _utc_now()
        meta = {"request_ts": now, "response_ts": now, "retry_count": 0,
                "cache_hit": True, "request_params": request_params}
        data = json.loads(cache_path.read_text())
        # Cache hits are logged too: the transcript records what an
        # experiment consumed, not only what it paid for.
        transcript.log(model, messages, data, meta)
        return data, meta

    kwargs: dict[str, Any] = {"max_tokens": max_tokens, **kw}
    if temperature is not None:
        kwargs["temperature"] = temperature
    if response_format is not None:
        kwargs["response_format"] = response_format

    request_ts = _utc_now()
    last_exc: Exception | None = None
    retry_count = 0
    empty_left = empty_response_retries
    # 1 attempt + max_retries. The count was the literal 4 while both
    # frozen configs declared retry.max_retries and both runners recorded
    # it in the run manifest — provenance asserting a policy the code
    # could not honour.
    for attempt in range(max_retries + 1):
        try:
            resp = litellm.completion(model=model, messages=messages, **kwargs)
            # A reasoning model can burn its whole budget and return an
            # empty completion. The frozen config carries an
            # empty_response_retries policy; without this it was recorded
            # and never applied, and the row became invalid on the first
            # blank.
            if empty_left > 0 and not get_text(
                    resp.model_dump() if hasattr(resp, "model_dump") else dict(resp)):
                empty_left -= 1
                retry_count += 1
                continue
            break
        except litellm.RateLimitError as e:
            last_exc = e
            retry_count = attempt + 1
            time.sleep(2 ** attempt * 5)
        except _TRANSIENT_ERRORS as e:
            last_exc = e
            retry_count = attempt + 1
            time.sleep(2 ** attempt * 2)
    else:
        raise last_exc  # type: ignore[misc]
    data = resp.model_dump() if hasattr(resp, "model_dump") else dict(resp)

    if use_cache:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(data, indent=2, default=str))

    meta = {"request_ts": request_ts, "response_ts": _utc_now(),
            "retry_count": retry_count, "cache_hit": False,
            "request_params": request_params}
    transcript.log(model, messages, data, meta)
    return data, meta


def call(
    model: str,
    messages: list[dict],
    **kwargs: Any,
) -> dict:
    """Backward-compatible wrapper around call_with_meta (drops metadata)."""
    data, _meta = call_with_meta(model, messages, **kwargs)
    return data


def _utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def prompt_sha256(messages: list[dict]) -> str:
    """Stable digest of the exact rendered prompt (P0.4 provenance)."""
    payload = json.dumps(messages, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def get_text(resp: dict) -> str:
    try:
        return resp["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError):
        return ""


def parse_loose_json(text: str) -> dict | None:
    """Parse JSON tolerating Markdown code fences and surrounding prose."""
    cleaned = _FENCE_RE.sub("", text).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    m = _JSON_OBJ_RE.search(cleaned)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"


def unknown_openrouter_models(models: Iterable[str]) -> list[str]:
    """Which of these `openrouter/...` IDs does OpenRouter not serve?

    A model ID is only ever validated by using it, and a wrong one fails
    per row with a 400 rather than up front: the frozen slate carried
    `openrouter/google/gemini-3-pro` — an ID that never existed — through
    every dry run, test and gate, and it was found only by spending money
    on 63 rows that all came back "not a valid model ID".

    Returns [] when the catalogue cannot be reached. A launch must not be
    blocked by this endpoint being down; the point is to catch a typo or a
    withdrawn model, not to add a dependency to the launch path.
    """
    wanted = {m for m in models if m.startswith("openrouter/")}
    if not wanted:
        return []
    try:
        with urllib.request.urlopen(OPENROUTER_MODELS_URL, timeout=15) as r:
            served = {m["id"] for m in json.load(r).get("data", [])}
    except Exception:                       # offline, rate-limited, changed
        return []
    if not served:
        return []
    # Suffixes like ":free" / ":batch" pin routing and are listed separately;
    # compare on the bare ID so a paid-routing slate is not falsely flagged.
    return sorted(m for m in wanted
                  if m[len("openrouter/"):].split(":")[0] not in
                  {s.split(":")[0] for s in served})


def assert_key_present(model: str) -> None:
    if model.startswith(("gpt-", "openai/", "o1", "o3")):
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY not set")
    elif model.startswith(("claude-", "anthropic/")):
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise RuntimeError("ANTHROPIC_API_KEY not set")
    elif model.startswith(("gemini", "google/")):
        if not os.getenv("GEMINI_API_KEY"):
            raise RuntimeError("GEMINI_API_KEY not set")
    elif model.startswith("openrouter/"):
        if not os.getenv("OPENROUTER_API_KEY"):
            raise RuntimeError("OPENROUTER_API_KEY not set")
