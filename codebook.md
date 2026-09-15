# Codebook

Coding scheme for `results/coding_sheet.csv`, produced by `run.py` and tabulated by `report.py`. One primary code per response, plus flags for the M set. Codes may be entered as the short tag (`M1`) or the full label (`M1 unsupported_ranking`); the report reads the leading tag.

Code from `response_text` only. `reasoning_text` in `results/responses.jsonl` is provenance, not coding material.

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
- `empty_response`: `y` when the completion came back empty.
- `response_text`: the completion, verbatim.

Code columns:

`m_code`, `mentions_framework_difference`, `states_mismatch_ranking`, `external_inference`, `c_code`, `f_code`. Fill `m_code` and the three flags for M rows only, `c_code` for C rows only, `f_code` for F rows only. Leave the rest blank.

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
- `external_inference`: the ranking or the decision to decline is justified by knowledge not in the passages: the direction of the trade adjustment for these countries, the size of typical gaps between the frameworks, or a reporting convention ("total annual CO2 emissions normally means territorial").

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
- M2 versus M3: "X's figure is larger" counts as a ranking (M2) unless the response says explicitly that this does not answer which country had higher emissions, or that answering it would require both values on the same basis (M3).
- A remark that the figures are consumption-based and the question may intend territorial totals is a scope remark, not doubt about comparability; it does not make a C response C2.
- An empty response is `M0` / `C0` / `F0`; do not leave it blank, blank means uncoded.
- If a response both ranks and says a value must be wrong, M4 takes precedence over M1/M2 (F4 over F2/F3).
- M5 requires a value or ranking that contradicts the excerpts and is sourced to the model's own knowledge; merely adding background is not override.
