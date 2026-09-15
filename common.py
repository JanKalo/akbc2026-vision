"""Shared pieces of the vision-paper pilot v2 (split-source comparison).

Loads `passages.yaml`, renders passages, and enumerates the
request cells. Imported by the audit, run and report scripts and by
`run.py`. Nothing here touches the network.

Design:

* A passage = base paragraph (country x register) with the country name,
  the value and ONE slot sentence filled in. The slot carries the expression
  level (label / definition / term / none); nothing else in the passage may.
* Retrieval sets: M (two passages, mismatched frameworks; the test),
  C (two passages, same framework; over-hedging control), F (all four
  passages; reference).
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent
DATA_PATH = REPO / "passages.yaml"

FRAMEWORKS = ("territorial", "consumption")
LEVELS = ("label", "definition", "term", "none")
REGISTERS = ("A", "B")
SETS = ("M", "C", "F")

DEFAULT_LEVELS = ("label", "definition", "none")
DEFAULT_C_LEVELS = ("definition",)
DEFAULT_F_LEVELS = ("label", "definition")

DEFAULT_MODELS = (
    "openrouter/google/gemma-4-31b-it",
    "openrouter/qwen/qwen3.8-max-0902",
    "openrouter/anthropic/claude-opus-5",
)
MODEL_SHORT = {
    "openrouter/google/gemma-4-31b-it": "gemma",
    "openrouter/qwen/qwen3.8-max-0902": "qwen",
    "openrouter/anthropic/claude-opus-5": "opus",
}
# Reasoning on, medium effort, for Qwen and Opus; Gemma runs plain.
# Sent as OpenRouter's native `reasoning` object via extra_body: litellm's
# `reasoning_effort` is only forwarded for models its own registry flags as
# reasoning-capable, and this build flags qwen3.8-max as not capable.
REASONING_MODELS = {
    "openrouter/qwen/qwen3.8-max-0902",
    "openrouter/anthropic/claude-opus-5",
}
REASONING_KWARGS = {"extra_body": {"reasoning": {"effort": "medium"}}}

TEMPERATURE = 0.0
MAX_TOKENS = 4096
CACHE_SALT = "vision-pilot-v2"

SYSTEM_PROMPT = ("You are a research assistant. Answer the user's question "
                 "using the retrieved excerpts.")
QUESTION = ("Did {COUNTRY_1} or {COUNTRY_2} have higher total annual CO2 "
            "emissions in 2022?")

VALUE_SENTENCE = ("According to the Global Carbon Budget figures published by "
                  "Our World in Data, {COUNTRY}'s carbon dioxide emissions in "
                  "2022 totalled {VALUE} million tonnes.")


def load_spec(path: Path = DATA_PATH) -> dict:
    spec = yaml.safe_load(Path(path).read_text())
    for key in ("values", "pairs", "slots", "bases"):
        if key not in spec:
            raise ValueError(f"{path}: missing top-level key {key!r}")
    spec.setdefault("shared_sentences", {r: [] for r in REGISTERS})
    spec.setdefault("display_names", {})
    return spec


def format_value(value: float) -> str:
    return f"{value:.1f}"


def model_short(model: str) -> str:
    if model in MODEL_SHORT:
        return MODEL_SHORT[model]
    return re.sub(r"[^A-Za-z0-9]+", "_", model.split("/")[-1]).strip("_")


def display_name(spec: dict, country: str) -> str:
    """The name as it appears in prose: "the United Kingdom", "France"."""
    return spec.get("display_names", {}).get(country, country)


def base_text(spec: dict, country: str, register: str) -> str:
    """The base paragraph as one line (the YAML folds it)."""
    return " ".join(spec["bases"][country][register].split())


def render_passage(spec: dict, country: str, register: str,
                   framework: str, level: str) -> str:
    base = base_text(spec, country, register)
    slot = spec["slots"][framework][level]
    value = format_value(spec["values"][country][framework])
    return (base.replace("{SLOT}", slot)
                .replace("{COUNTRY}", display_name(spec, country))
                .replace("{VALUE}", value))


def pair_by_id(spec: dict, pair_id: str) -> dict:
    for p in spec["pairs"]:
        if p["id"] == pair_id:
            return p
    raise KeyError(pair_id)


def expected_consistent_rankings(spec: dict, countries: list[str]) -> dict:
    """framework -> the country that is higher under that framework."""
    out = {}
    for fw in FRAMEWORKS:
        out[fw] = max(countries, key=lambda c: spec["values"][c][fw])
    return out


def _passage(spec, country, register, framework, level) -> dict:
    return {
        "country": country, "register": register, "framework": framework,
        "level": level, "value": spec["values"][country][framework],
        "text": render_passage(spec, country, register, framework, level),
    }


def _cell(spec, set_, pair, assignment, level, model, passages) -> dict:
    c1, c2 = pair["countries"]
    cell = {
        "cell_id": f"{set_}-{pair['id']}-{assignment}-{level}-{model_short(model)}",
        "set": set_, "pair": pair["id"], "pair_kind": pair["kind"],
        "assignment": assignment, "level": level,
        "model": model, "model_short": model_short(model),
        "countries": [c1, c2],
        "display_names": [display_name(spec, c1), display_name(spec, c2)],
        "passages": passages,
        "passage_order": [f"{p['country']}:{p['framework']}:{p['register']}"
                          for p in passages],
        "expected_consistent_rankings":
            expected_consistent_rankings(spec, [c1, c2]),
        "mismatch_ranking": None,
    }
    if set_ == "M":
        # The country the raw cross-framework comparison favours.
        cell["mismatch_ranking"] = max(passages, key=lambda p: p["value"])["country"]
    return cell


def build_cells(spec: dict, *, levels=DEFAULT_LEVELS, sets=SETS,
                models=DEFAULT_MODELS, c_levels=DEFAULT_C_LEVELS,
                f_levels=DEFAULT_F_LEVELS) -> list[dict]:
    """Every request cell, in a deterministic order (set, pair, assignment,
    level, model)."""
    for lv in (*levels, *c_levels, *f_levels):
        if lv not in LEVELS:
            raise ValueError(f"unknown level {lv!r}; choose from {LEVELS}")
    for s in sets:
        if s not in SETS:
            raise ValueError(f"unknown set {s!r}; choose from {SETS}")
    cells: list[dict] = []
    for set_ in sets:
        for pair in spec["pairs"]:
            c1, c2 = pair["countries"]
            if set_ == "M":
                for level in levels:
                    # A: first-listed country territorial, shown first;
                    # second country consumption-based.
                    # B: frameworks reversed, first-listed country shown
                    # second. Registers stay with the country (first-listed
                    # A, second B) so each register carries each framework
                    # equally often (brief section 11, fix 3).
                    variants = {
                        "A": [_passage(spec, c1, "A", "territorial", level),
                              _passage(spec, c2, "B", "consumption", level)],
                        "B": [_passage(spec, c2, "B", "territorial", level),
                              _passage(spec, c1, "A", "consumption", level)],
                    }
                    for assignment, passages in variants.items():
                        for model in models:
                            cells.append(_cell(spec, set_, pair, assignment,
                                               level, model, passages))
            elif set_ == "C":
                for level in c_levels:
                    for fw in FRAMEWORKS:
                        passages = [_passage(spec, c1, "A", fw, level),
                                    _passage(spec, c2, "B", fw, level)]
                        for model in models:
                            cells.append(_cell(spec, set_, pair, fw, level,
                                               model, passages))
            elif set_ == "F":
                for level in f_levels:
                    # Register A carries one framework per country and
                    # register B the other (brief section 11, fix 3).
                    passages = [
                        _passage(spec, c1, "A", "territorial", level),
                        _passage(spec, c2, "A", "consumption", level),
                        _passage(spec, c1, "B", "consumption", level),
                        _passage(spec, c2, "B", "territorial", level),
                    ]
                    for model in models:
                        cells.append(_cell(spec, set_, pair, "all", level,
                                           model, passages))
    ids = [c["cell_id"] for c in cells]
    assert len(ids) == len(set(ids)), "duplicate cell ids"
    return cells


def build_messages(cell: dict) -> list[dict]:
    c1, c2 = cell["display_names"]
    excerpts = "\n\n".join(f"[{i}] {p['text']}"
                           for i, p in enumerate(cell["passages"], 1))
    user = (QUESTION.format(COUNTRY_1=c1, COUNTRY_2=c2)
            + "\n\nRetrieved excerpts:\n\n" + excerpts)
    return [{"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user}]


def request_kwargs(model: str) -> dict:
    """Decoding kwargs for `llm.call_with_meta`, mirroring how
    the decoding dict is passed through as kwargs."""
    kw = {"temperature": TEMPERATURE, "max_tokens": MAX_TOKENS,
          "cache_salt": CACHE_SALT, "empty_response_retries": 0,
          "max_retries": 3}
    if model in REASONING_MODELS:
        kw.update(REASONING_KWARGS)
    return kw


def format_cell_for_snapshot(cell: dict) -> str:
    msgs = build_messages(cell)
    return ("=== CELL ===\n" + cell["cell_id"] + "\n"
            + "=== SYSTEM ===\n" + msgs[0]["content"] + "\n\n"
            + "=== USER ===\n" + msgs[1]["content"] + "\n")
