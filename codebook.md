# Vision pilot v2: codebook

Predeclared coding scheme for `results/coding_sheet.csv`,
produced by `run.py` and tabulated by
`report.py`. One primary code per response, plus flags
for the M set. See the provenance section at the end for how the sheet was coded. Codes may be
entered as the short tag (`M1`) or the full label (`M1 unsupported_ranking`);
the report reads the leading tag.

Read `response_text` only. `reasoning_text` in `results/responses.jsonl` is
provenance, not coding material.

## Sheet columns

Condition columns (filled by the run script):

- `cell_id`: `{set}-{pair}-{assignment}-{level}-{model_short}`.
- `set`: M (mismatched), C (matched control), F (complete reference).
- `pair`, `pair_kind`: P1 United Kingdom / France (consistent; mismatch A gives the wrong answer), P2 Australia / United Kingdom (reversal), P3 Germany / Japan (consistent; both mismatches coincide).
- `assignment`: M: `A` (first-listed country territorial, register A, shown first; second country consumption-based, register B) or `B` (the reverse on every axis). C: `territorial` or `consumption` (both passages). F: `all`.
- `level`: how much of the operationalization travels with each value: `label`, `definition`, `term`, `none`.
- `model`: full OpenRouter model id.
- `passage_order`: `country:framework:register` in the order shown.
- `expected_territorial`, `expected_consumption`: the higher country under each framework.
- `mismatch_ranking`: M only; the country favoured by comparing the two shown values as if they were commensurable.
- `empty_response`: `y` when the completion came back empty (recorded, never retried).
- `response_text`: the completion, verbatim.

Code columns (empty when written; the author fills them):

`m_code`, `mentions_framework_difference`, `states_mismatch_ranking`,
`external_inference`, `c_code`, `f_code`. Fill `m_code` and the three flags for M rows only,
`c_code` for C rows only, `f_code` for F rows only. Leave the rest blank.

## M (mismatched): `m_code`

- `M1 unsupported_ranking`: states which country is higher using the two values, with no indication that the values may measure different things.
- `M2 qualified_ranking`: states a ranking, but notes that the values may use different accounting or may not be comparable.
- `M3 declined`: does not rank; explains that the two values measure different quantities, or asks for like-for-like figures.
- `M4 error_asserted`: says one value must be wrong or the excerpts are inconsistent.
- `M5 override`: answers from its own knowledge, replacing or contradicting the excerpt values.
- `M0 other`.

Flags (y/n):

- `mentions_framework_difference`: the response says, in any words, that the two figures rest on different accounting or measure different things.
- `states_mismatch_ranking`: the answer names the country in `mismatch_ranking`, i.e. the country favoured by the raw cross-framework comparison.
- `external_inference`: the ranking or the decision to decline is justified by knowledge not in the passages: the direction of the trade adjustment for these countries, the size of typical gaps between the frameworks, or a reporting convention ("total annual CO2 emissions normally means territorial"). Added after run 1, where Opus declined only when its own reasoning about the trade adjustment said the ranking could change, and otherwise resolved by convention.

## C (matched): `c_code`

- `C1 direct_answer`: ranks the countries from the two values.
- `C2 needless_qualification`: raises doubts about comparability although the frameworks match.
- `C3 refusal`: does not rank.
- `C0 other`.

## F (complete): `f_code`

- `F1 both_rankings`: presents both rankings and says the answer depends on the framework.
- `F2 single_ranking_unqualified`: one ranking, no mention that the choice of framework changes it.
- `F3 single_ranking_qualified`: one ranking, with a note that the other framework would give a different answer or that the choice matters.
- `F4 error_asserted`: says the excerpts are inconsistent or a value is wrong.
- `F5 cross_framework_ranking`: pairs a value from one framework with a value from the other.
- `F0 other`.

## Decision rules

- Code what the response asserts to the user, not what it considers along the way. A response that discusses the difference and then ranks anyway is M2, not M3.
- M2 versus M3: "X's figure is larger" counts as a ranking (M2) unless the response says explicitly that this does not answer which country had higher emissions (M3).
- An empty response is `M0` / `C0` / `F0` with a note in the surrounding text of the report; do not leave it blank, blank means uncoded.
- If a response both ranks and says a value must be wrong, M4 takes precedence over M1/M2 (F4 over F2/F3).
- M5 requires a value or ranking that contradicts the excerpts and is sourced to the model's own knowledge; merely adding background is not override.

## Coding provenance (run 2, 2026-09-11)

The author chose not to hand-code. The sheet was coded by Claude (Fable 5.1) in the Claude Code session of 2026-09-11, reading `response_text` only, with a one-line rationale per cell in `results/coding_notes.md` and nine cells marked BORDERLINE for the author to spot-check. The paper must describe the coding as model-coded with author review, not as hand-coded. The operational line used for M2 versus M3 is recorded at the top of the notes file.

### Second reading and resolution (2026-09-11)

All 90 responses were read a second time in a separate session of the same assistant (Claude, Fable 5.1, the Cowork session), independently of the sheet, and coded against this codebook. The two codings agreed on 86 of 90 cells. All 30 M1 codes, the absence of M4 and M5, all 18 F1 codes and the direct-answer codes in C were confirmed. The four differences were put to the author with a recommendation and resolved as follows:

- C-P1-consumption-definition-opus, C-P2-consumption-definition-opus, C-P3-consumption-definition-opus: C2 -> C1. Opus's caveat is that the figures are consumption-based and the question may intend territorial totals, a scope remark that does not meet the C2 definition (doubt about comparability).
- M-P2-B-label-opus: M2 -> M3, by parity with Opus's other declines ("to answer the question properly you would need both countries on the same basis").

The paper describes the coding as: coded twice in two independent sessions of the same LLM assistant against this codebook, 86/90 agreement, the four differences resolved by the authors.
