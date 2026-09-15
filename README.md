# Operationalization pilot

Small prototype for the pilot study in *Operationalization Is Part of the Claim* (Kalo, AKBC 2026).

Retrieval returns one 2022 CO2 value per country, but the two values use different accounting frameworks (territorial vs. consumption-based). The model is asked which country emitted more. We vary how the passage expresses the framework (a label, a plain-language definition, or nothing) and record whether the model ranks anyway, ranks with a caveat, or declines.

Three models (Gemma 4 31B, Qwen3.8 Max, Claude Opus 5), three country pairs, 90 requests. Mismatched responses by level (18 each):

| Level | Ranked | Ranked with caveat | Declined |
|---|---|---|---|
| label | 6 | 7 | 5 |
| definition | 6 | 6 | 6 |
| none | 18 | 0 | 0 |

Gemma ranked without a caveat in every case. Qwen and Opus caught the mismatch when the framework was stated and never when it was not.

## Files

- `passages.yaml`: values, pairs, framework sentences, base paragraphs.
- `run.py`, `common.py`: build the 90 requests and call the models (`llm.py`, `transcript.py` are the API wrapper).
- `report.py`: tabulate the coded sheet.
- `codebook.md`: coding scheme.
- `results/`: model responses, coded sheet with per-cell notes, and the tables.

## Run

```bash
pip install -r requirements.txt
python run.py --dry-run --out /tmp/vp     # render the prompts, no API calls
python report.py                          # rebuild results/report.md
OPENROUTER_API_KEY=... python run.py --out results_new   # live run
```
