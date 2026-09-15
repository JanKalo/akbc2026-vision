"""Vision-paper pilot v2: render every cell; optionally send them.

    python run.py --dry-run          # review artifact
    python run.py                    # live (author only)

Flags: --levels (M levels, default label,definition,none), --sets (default
M,C,F), --models (default the three in common.py), --c-levels
(default definition), --f-levels (default label,definition), --dry-run,
--out (default results/).

--dry-run writes prompts_preview.md (one section per cell) and cells.jsonl
and makes no API call. A live run additionally writes responses.jsonl (one
row per cell, appended as it goes; cells already present are skipped) and
coding_sheet.csv with EMPTY code columns for the author to fill.

Decoding: a kwargs dict spread into
`llm.call_with_meta`, recorded per row in request_params. Temperature 0,
max_tokens 4096, cache_salt "vision-pilot-v2", no content retries: an empty
completion is recorded as empty. Reasoning (medium) for Qwen and Opus is
sent as OpenRouter's `reasoning` object via extra_body; see
common.REASONING_KWARGS for why not litellm's reasoning_effort.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    DEFAULT_C_LEVELS, DEFAULT_F_LEVELS, DEFAULT_LEVELS, DEFAULT_MODELS, SETS,
    build_cells, build_messages, load_spec, request_kwargs,
)

# Section 7 code columns (plus external_inference from section 11), in this
# order, always empty when written here.
CODE_COLUMNS = ["m_code", "mentions_framework_difference",
                "states_mismatch_ranking", "external_inference", "c_code",
                "f_code"]
CONDITION_COLUMNS = ["cell_id", "set", "pair", "pair_kind", "assignment",
                     "level", "model", "passage_order", "expected_territorial",
                     "expected_consumption", "mismatch_ranking",
                     "empty_response", "response_text"]


def _csv_list(s: str) -> tuple[str, ...]:
    return tuple(x.strip() for x in s.split(",") if x.strip())


def parse_args(argv=None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--levels", type=_csv_list, default=DEFAULT_LEVELS,
                    help="M levels (label,definition,term,none)")
    ap.add_argument("--sets", type=_csv_list, default=SETS)
    ap.add_argument("--models", type=_csv_list, default=DEFAULT_MODELS)
    ap.add_argument("--c-levels", type=_csv_list, default=DEFAULT_C_LEVELS)
    ap.add_argument("--f-levels", type=_csv_list, default=DEFAULT_F_LEVELS)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", type=Path, default=Path("results"))
    return ap.parse_args(argv)


def cells_for(args: argparse.Namespace) -> list[dict]:
    spec = load_spec()
    return build_cells(spec, levels=args.levels, sets=args.sets,
                       models=args.models, c_levels=args.c_levels,
                       f_levels=args.f_levels)


def preview_markdown(cells: list[dict]) -> str:
    out = ["# Vision pilot v2: prompt preview", "",
           f"{len(cells)} cells. Each section is one request, rendered "
           "exactly as sent (system message, then user message).", ""]
    for cell in cells:
        msgs = build_messages(cell)
        out += [f"## {cell['cell_id']}", "",
                f"- set: {cell['set']}  pair: {cell['pair']} "
                f"({cell['pair_kind']})  assignment: {cell['assignment']}  "
                f"level: {cell['level']}  model: `{cell['model']}`",
                f"- passages: {' | '.join(cell['passage_order'])}",
                f"- expected consistent rankings: "
                f"{json.dumps(cell['expected_consistent_rankings'])}",
                f"- mismatch ranking: {cell['mismatch_ranking']}", "",
                "**SYSTEM**", "", "```", msgs[0]["content"], "```", "",
                "**USER**", "", "```", msgs[1]["content"], "```", ""]
    return "\n".join(out)


def write_dry_run(cells: list[dict], out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / "prompts_preview.md").write_text(preview_markdown(cells))
    with (out / "cells.jsonl").open("w") as fh:
        for cell in cells:
            row = {**cell, "messages": build_messages(cell),
                   "request_kwargs": request_kwargs(cell["model"])}
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def reasoning_text(resp: dict) -> str:
    """Whatever reasoning the provider returned, if any."""
    try:
        msg = resp["choices"][0]["message"] or {}
    except (KeyError, IndexError, TypeError):
        return ""
    for key in ("reasoning_content", "reasoning"):
        if msg.get(key):
            return str(msg[key])
    psf = msg.get("provider_specific_fields") or {}
    for key in ("reasoning_content", "reasoning"):
        if psf.get(key):
            return str(psf[key])
    return ""


def response_row(cell: dict, messages: list[dict], resp: dict | None,
                 meta: dict | None, error: str | None = None) -> dict:
    from llm import get_text, prompt_sha256
    text = get_text(resp) if resp else ""
    choice = (resp or {}).get("choices") or [{}]
    return {
        **{k: cell[k] for k in ("cell_id", "set", "pair", "pair_kind",
                                 "assignment", "level", "model",
                                 "passage_order",
                                 "expected_consistent_rankings",
                                 "mismatch_ranking")},
        "messages": messages,
        "prompt_sha256": prompt_sha256(messages),
        "response_text": text,
        "reasoning_text": reasoning_text(resp) if resp else "",
        "empty_response": not text.strip(),
        "finish_reason": choice[0].get("finish_reason") if choice else None,
        "resolved_model": (resp or {}).get("model"),
        "usage": (resp or {}).get("usage"),
        "error": error,
        **(meta or {}),
    }


def coding_sheet_rows(rows: list[dict]) -> list[dict]:
    out = []
    for r in rows:
        exp = r["expected_consistent_rankings"]
        out.append({
            "cell_id": r["cell_id"], "set": r["set"], "pair": r["pair"],
            "pair_kind": r["pair_kind"], "assignment": r["assignment"],
            "level": r["level"], "model": r["model"],
            "passage_order": " | ".join(r["passage_order"]),
            "expected_territorial": exp["territorial"],
            "expected_consumption": exp["consumption"],
            "mismatch_ranking": r["mismatch_ranking"] or "",
            "empty_response": "y" if r.get("empty_response") else "n",
            "response_text": r.get("response_text", ""),
            **{c: "" for c in CODE_COLUMNS},
        })
    return out


def write_coding_sheet(rows: list[dict], path: Path) -> None:
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CONDITION_COLUMNS + CODE_COLUMNS)
        w.writeheader()
        for r in coding_sheet_rows(rows):
            w.writerow(r)


def run_live(cells: list[dict], out: Path) -> list[dict]:
    import transcript
    from llm import assert_key_present, call_with_meta

    tpath = transcript.default_to(out)
    print(f"[vision_pilot] transcript -> {tpath}")
    for model in sorted({c["model"] for c in cells}):
        assert_key_present(model)

    responses = out / "responses.jsonl"
    done: dict[str, dict] = {}
    if responses.exists():
        for line in responses.read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                done[row["cell_id"]] = row
    if done:
        print(f"[vision_pilot] {len(done)} cells already in {responses}; "
              "skipping those")

    with responses.open("a") as fh:
        for i, cell in enumerate(cells, 1):
            if cell["cell_id"] in done:
                continue
            messages = build_messages(cell)
            kw = request_kwargs(cell["model"])
            try:
                with transcript.context(cell_id=cell["cell_id"],
                                        pilot="vision-pilot-v2"):
                    resp, meta = call_with_meta(cell["model"], messages, **kw)
                row = response_row(cell, messages, resp, meta)
            except Exception as e:  # transport retries are exhausted inside
                row = response_row(cell, messages, None, None,
                                   error=f"{type(e).__name__}: {e}")
            done[cell["cell_id"]] = row
            fh.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
            fh.flush()
            status = ("ERROR" if row["error"] else
                      "empty" if row["empty_response"] else "ok")
            print(f"[{i}/{len(cells)}] {cell['cell_id']}: {status}")
    ordered = [done[c["cell_id"]] for c in cells]
    write_coding_sheet(ordered, out / "coding_sheet.csv")
    return ordered


def main(argv=None) -> int:
    args = parse_args(argv)
    cells = cells_for(args)
    by_set = {s: sum(c["set"] == s for c in cells) for s in args.sets}
    print(f"[vision_pilot] {len(cells)} cells: "
          + ", ".join(f"{s}={n}" for s, n in by_set.items()))
    write_dry_run(cells, args.out)
    print(f"[vision_pilot] wrote {args.out / 'prompts_preview.md'} and "
          f"{args.out / 'cells.jsonl'}")
    if args.dry_run:
        print("[vision_pilot] dry run: no API calls made")
        return 0
    rows = run_live(cells, args.out)
    n_err = sum(bool(r["error"]) for r in rows)
    n_empty = sum(bool(r["empty_response"]) and not r["error"] for r in rows)
    print(f"[vision_pilot] {len(rows)} rows; {n_empty} empty, {n_err} errors; "
          f"coding sheet -> {args.out / 'coding_sheet.csv'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
