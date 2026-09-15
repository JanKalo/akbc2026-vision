# Coding notes

One line of rationale per cell, coded against `codebook.md` from `response_text` only. Cells marked BORDERLINE were the closest calls. Operational line for M2 vs M3: M3 only when the response explicitly says which country had higher emissions cannot be determined or answered from the excerpts, or that answering it would require both values on the same basis; M2 when it states a ranking and only calls the figures not directly comparable / not like-for-like. `external_inference` = y when the response asserts the direction or size of the trade adjustment for these countries, a typical gap for net importers/exporters, or a reporting convention about what "total annual CO2 emissions" means.

| cell | codes | note |
|---|---|---|
| M-P1-A-label-gemma | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P1-A-label-qwen | M2 fw=y mm=y ext=y | Ranks France, then caveat. external_inference=y on 'consumption-based totals are typically higher for net-importing economies'. |
| M-P1-A-label-opus | M3 fw=y mm=n ext=y | Declines: 'the excerpts don't allow a valid comparison'; justified by the direction of the trade adjustment for these countries. |
| M-P1-B-label-gemma | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P1-B-label-qwen | M3 fw=y mm=n ext=y | BORDERLINE M2/M3. Opens 'the UK had the higher figure', closes 'a strictly apples-to-apples answer cannot be given from these sources alone'. Coded M3 under the explicit-refusal rule. |
| M-P1-B-label-opus | M3 fw=y mm=n ext=y | Declines: 'the excerpts don't allow a valid comparison'; justified by the direction of the trade adjustment for these countries. |
| M-P1-A-definition-gemma | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P1-A-definition-qwen | M2 fw=y mm=y ext=y | BORDERLINE M2/M3. States France's figure is higher; says the two 'cannot be directly compared as like-for-like totals' but never says the question cannot be answered. Coded M2. external_inference=y on 'tends to yield a larger number for net-importing economies'. |
| M-P1-A-definition-opus | M3 fw=y mm=n ext=y | Declines: 'the excerpts don't allow a valid comparison'; justified by the direction of the trade adjustment for these countries. |
| M-P1-B-definition-gemma | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P1-B-definition-qwen | M3 fw=y mm=n ext=y | Explicit: 'one cannot definitively say which country had higher emissions from these excerpts alone'. external_inference=y: asserts a UK territorial figure would be lower and a French consumption figure higher. |
| M-P1-B-definition-opus | M3 fw=y mm=n ext=y | Declines: 'the excerpts don't allow a valid comparison'; justified by the direction of the trade adjustment for these countries. |
| M-P1-A-none-gemma | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P1-A-none-qwen | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P1-A-none-opus | M1 fw=n mm=y ext=n | Ranks from the two values without qualification. Adds scope/revision/per-capita caveats but does not say the bases differ. Mentions 'different again if consumption-based accounting were used' as a hypothetical, not as a property of these two figures; mentions_framework_difference=n. |
| M-P1-B-none-gemma | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P1-B-none-qwen | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P1-B-none-opus | M1 fw=n mm=y ext=n | Ranks from the two values without qualification. Adds scope/revision/per-capita caveats but does not say the bases differ. |
| M-P2-A-label-gemma | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P2-A-label-qwen | M2 fw=y mm=y ext=n | Names the mismatch-favoured country, then a caveat that the bases differ; still ranks ('nonetheless, on the numbers as reported'). |
| M-P2-A-label-opus | M3 fw=y mm=n ext=y | Declines: 'the excerpts don't allow a valid comparison'; justified by the direction of the trade adjustment for these countries. |
| M-P2-B-label-gemma | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P2-B-label-qwen | M2 fw=y mm=y ext=n | Names the mismatch-favoured country, then a caveat that the bases differ; still ranks ('nonetheless, on the numbers as reported'). |
| M-P2-B-label-opus | M2 fw=y mm=y ext=y | BORDERLINE M2/M3. 'On the face of the numbers Australia's figure is the higher ... shouldn't be treated as settled'; 'Australia's 365.1 exceeds the UK's 311.1 as reported'. Coded M2. external_inference=y: UK net importer, Australia net exporter. |
| M-P2-A-definition-gemma | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P2-A-definition-qwen | M2 fw=y mm=y ext=n | Names the mismatch-favoured country, then a caveat that the bases differ; still ranks ('nonetheless, on the numbers as reported'). |
| M-P2-A-definition-opus | M3 fw=y mm=n ext=y | Declines ('can't complete the comparison from these sources'); UK net importer, Australia exporter; 'most commonly territorial'. |
| M-P2-B-definition-gemma | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P2-B-definition-qwen | M2 fw=y mm=y ext=n | BORDERLINE M2/M3. States Australia's reported figure is higher; 'cannot be directly compared as like-for-like measures'; no explicit refusal to answer. Coded M2 for consistency with M-P1-A-definition-qwen. |
| M-P2-B-definition-opus | M3 fw=y mm=n ext=y | Declines ('a like-for-like comparison isn't possible'); 'that ordering may not hold on a consistent basis'; Australia coal/gas exporter. |
| M-P2-A-none-gemma | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P2-A-none-qwen | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P2-A-none-opus | M1 fw=n mm=y ext=n | Ranks from the two values without qualification. Adds scope/revision/per-capita caveats but does not say the bases differ. |
| M-P2-B-none-gemma | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P2-B-none-qwen | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P2-B-none-opus | M1 fw=n mm=y ext=n | Ranks from the two values without qualification. Adds scope/revision/per-capita caveats but does not say the bases differ. |
| M-P3-A-label-gemma | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P3-A-label-qwen | M2 fw=y mm=y ext=n | Names the mismatch-favoured country, then a caveat that the bases differ; still ranks ('nonetheless, on the numbers as reported'). |
| M-P3-A-label-opus | M2 fw=y mm=y ext=y | Ranks Japan 'by a wide margin' with caveat; justifies robustness from Japan being a net importer and the wedge being 'nowhere near large enough'. |
| M-P3-B-label-gemma | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P3-B-label-qwen | M2 fw=y mm=y ext=n | Names the mismatch-favoured country, then a caveat that the bases differ; still ranks ('nonetheless, on the numbers as reported'). |
| M-P3-B-label-opus | M2 fw=y mm=y ext=y | Ranks Japan with caveat; 'Japan's economy and population are both substantially bigger ... almost certainly ranked higher on either basis'. |
| M-P3-A-definition-gemma | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P3-A-definition-qwen | M3 fw=y mm=n ext=n | BORDERLINE M2/M3. 'Japan's figure is numerically higher' then 'cannot be directly ranked against each other as total annual CO2 emissions'. Coded M3: explicit that the ranking is not available. |
| M-P3-A-definition-opus | M2 fw=y mm=y ext=y | Ranks Japan with caveat; 'both are net importers ... gap very unlikely to be closed by the accounting difference'; population and nuclear idling cited. |
| M-P3-B-definition-gemma | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P3-B-definition-qwen | M2 fw=y mm=y ext=n | Names the mismatch-favoured country, then a caveat that the bases differ; still ranks ('nonetheless, on the numbers as reported'). |
| M-P3-B-definition-opus | M2 fw=y mm=y ext=y | BORDERLINE M2/M3. 'Japan's figure is higher, but not apples-to-apples'; then 'Japan almost certainly had higher territorial emissions as well ... direction reliable'. Coded M2. external_inference=y: 'total annual CO2 emissions normally means territorial'; Germany net exporter. |
| M-P3-A-none-gemma | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P3-A-none-qwen | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P3-A-none-opus | M1 fw=n mm=y ext=n | Ranks from the two values without qualification. Adds scope/revision/per-capita caveats but does not say the bases differ. |
| M-P3-B-none-gemma | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P3-B-none-qwen | M1 fw=n mm=y ext=n | Ranks from the two values; no mention that they rest on different accounting. |
| M-P3-B-none-opus | M1 fw=n mm=y ext=n | Ranks from the two values without qualification. Adds scope/revision/per-capita caveats but does not say the bases differ. |
| C-P1-territorial-definition-gemma | C1 | Direct answer from the two values. |
| C-P1-territorial-definition-qwen | C1 | Direct answer from the two values. |
| C-P1-territorial-definition-opus | C1 | Direct answer. Notes both figures are territorial and that consumption-based rankings 'could differ' / 'could shift the comparison'; treated as a scope note, not a doubt about this comparison. BORDERLINE C1/C2 for P1 and P2. |
| C-P1-consumption-definition-gemma | C1 | Direct answer from the two values. |
| C-P1-consumption-definition-qwen | C1 | Direct answer from the two values. |
| C-P1-consumption-definition-opus | C2 | Ranks, then hedges: the figures are consumption-based, 'not what total annual CO2 emissions usually means in national reporting'; a territorial comparison 'could give a different ranking' / 'these figures are not the right ones'. Coded C2 (needless qualification); the doubt rests on a reporting convention, not on any mismatch in the excerpts. This is the external-inference pattern in a matched pair. |
| C-P2-territorial-definition-gemma | C1 | Direct answer from the two values. |
| C-P2-territorial-definition-qwen | C1 | Direct answer from the two values. |
| C-P2-territorial-definition-opus | C1 | Direct answer. Notes both figures are territorial and that consumption-based rankings 'could differ' / 'could shift the comparison'; treated as a scope note, not a doubt about this comparison. BORDERLINE C1/C2 for P1 and P2. |
| C-P2-consumption-definition-gemma | C1 | Direct answer from the two values. |
| C-P2-consumption-definition-qwen | C1 | Direct answer from the two values. |
| C-P2-consumption-definition-opus | C2 | Ranks, then hedges: the figures are consumption-based, 'not what total annual CO2 emissions usually means in national reporting'; a territorial comparison 'could give a different ranking' / 'these figures are not the right ones'. Coded C2 (needless qualification); the doubt rests on a reporting convention, not on any mismatch in the excerpts. This is the external-inference pattern in a matched pair. |
| C-P3-territorial-definition-gemma | C1 | Direct answer from the two values. |
| C-P3-territorial-definition-qwen | C1 | Direct answer from the two values. |
| C-P3-territorial-definition-opus | C1 | Direct answer; notes both are territorial; no doubt raised. |
| C-P3-consumption-definition-gemma | C1 | Direct answer from the two values. |
| C-P3-consumption-definition-qwen | C1 | Direct answer from the two values. |
| C-P3-consumption-definition-opus | C2 | Ranks, then hedges: the figures are consumption-based, 'not what total annual CO2 emissions usually means in national reporting'; a territorial comparison 'could give a different ranking' / 'these figures are not the right ones'. Coded C2 (needless qualification); the doubt rests on a reporting convention, not on any mismatch in the excerpts. This is the external-inference pattern in a matched pair. |
| F-P1-all-label-gemma | F1 | BORDERLINE F1/F5. First line pairs France's consumption value (437.4) against the UK's territorial value (311.1) and calls France higher, then corrects itself in the same bullet to UK higher on both bases. Final assertion is F1; the cross-framework pairing is visible in the response. |
| F-P1-all-label-qwen | F1 | Presents both rankings, each from its own framework. |
| F-P1-all-label-opus | F1 | Presents both; says territorial is 'the one usually meant by total annual CO2 emissions'; warns explicitly against mixing the measures. F1. |
| F-P1-all-definition-gemma | F1 | Presents both rankings, each from its own framework. |
| F-P1-all-definition-qwen | F1 | Presents both rankings, each from its own framework. |
| F-P1-all-definition-opus | F1 | Presents both; says territorial is 'the one usually meant by total annual CO2 emissions'; warns explicitly against mixing the measures. F1. |
| F-P2-all-label-gemma | F1 | F1 with a visible self-correction: first states the UK higher territorially with 311.1 vs 384.1 (wrong reading of correct numbers, not a cross-framework pairing), then corrects to Australia. |
| F-P2-all-label-qwen | F1 | Presents both rankings and says the answer depends on the basis; then resolves by convention ('the standard territorial measure' / 'as conventionally reported under the UNFCCC') in favour of Australia. F1; the convention step is external inference in a complete-retrieval cell. |
| F-P2-all-label-opus | F1 | Presents both rankings and says the answer depends on the basis; then resolves by convention ('the standard territorial measure' / 'as conventionally reported under the UNFCCC') in favour of Australia. F1; the convention step is external inference in a complete-retrieval cell. |
| F-P2-all-definition-gemma | F1 | F1 with the same self-correction as the label cell. |
| F-P2-all-definition-qwen | F1 | Presents both rankings and says the answer depends on the basis; then resolves by convention ('the standard territorial measure' / 'as conventionally reported under the UNFCCC') in favour of Australia. F1; the convention step is external inference in a complete-retrieval cell. |
| F-P2-all-definition-opus | F1 | Presents both rankings and says the answer depends on the basis; then resolves by convention ('the standard territorial measure' / 'as conventionally reported under the UNFCCC') in favour of Australia. F1; the convention step is external inference in a complete-retrieval cell. |
| F-P3-all-label-gemma | F1 | Presents both rankings, each from its own framework. |
| F-P3-all-label-qwen | F1 | Presents both rankings, each from its own framework. |
| F-P3-all-label-opus | F1 | Presents both; warns explicitly against mixing the measures. F1. |
| F-P3-all-definition-gemma | F1 | Presents both rankings, each from its own framework. |
| F-P3-all-definition-qwen | F1 | Presents both rankings, each from its own framework. |
| F-P3-all-definition-opus | F1 | Presents both rankings, each from its own framework. |

**Borderline cells (9):** M-P1-B-label-qwen, M-P1-A-definition-qwen, M-P2-B-label-opus, M-P2-B-definition-qwen, M-P3-A-definition-qwen, M-P3-B-definition-opus, C-P1-territorial-definition-opus, C-P2-territorial-definition-opus, F-P1-all-label-gemma

## Resolution (2026-09-11, author with second independent reading)

A second reading of all 90 responses, in a separate session of the same assistant, agreed with the codes above on 86 cells. The four differences were resolved by the author as follows:

- C-P1-consumption-definition-opus, C-P2-consumption-definition-opus, C-P3-consumption-definition-opus: C2 -> C1. Opus's caveat is that the figures are consumption-based and the question may intend territorial totals; that is a scope remark, not a doubt about comparability, so it does not meet the C2 definition.
- M-P2-B-label-opus: M2 -> M3. "Shouldn't be treated as settled ... to answer the question properly you would need both countries on the same basis" withholds the ranking in the same terms as Opus's other declines.

All 30 M1 codes, the absence of M4 and M5, all 18 F1 codes and the direct-answer codes in C were confirmed by the second reading.
