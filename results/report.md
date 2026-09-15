# Vision pilot v2: coded results

90 rows on the sheet; 0 uncoded.

## M (mismatched)

### By level

| level | M1 | M2 | M3 | M4 | M5 | M0 | uncoded | invalid | n |
|---|---|---|---|---|---|---|---|---|---|
| label | 6 | 7 | 5 | 0 | 0 | 0 | 0 | 0 | 18 |
| definition | 6 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 18 |
| none | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 18 |

### By model and level

| model / level | M1 | M2 | M3 | M4 | M5 | M0 | uncoded | invalid | n |
|---|---|---|---|---|---|---|---|---|---|
| openrouter/google/gemma-4-31b-it / label | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| openrouter/qwen/qwen3.8-max-0902 / label | 0 | 5 | 1 | 0 | 0 | 0 | 0 | 0 | 6 |
| openrouter/anthropic/claude-opus-5 / label | 0 | 2 | 4 | 0 | 0 | 0 | 0 | 0 | 6 |
| openrouter/google/gemma-4-31b-it / definition | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| openrouter/qwen/qwen3.8-max-0902 / definition | 0 | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 6 |
| openrouter/anthropic/claude-opus-5 / definition | 0 | 2 | 4 | 0 | 0 | 0 | 0 | 0 | 6 |
| openrouter/google/gemma-4-31b-it / none | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| openrouter/qwen/qwen3.8-max-0902 / none | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| openrouter/anthropic/claude-opus-5 / none | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |

### By pair and level (P1 assignment A is the wrong-ranking demonstration)

| pair / level | M1 | M2 | M3 | M4 | M5 | M0 | uncoded | invalid | n |
|---|---|---|---|---|---|---|---|---|---|
| P1-A / label | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 3 |
| P1-B / label | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 3 |
| P1-A / definition | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 3 |
| P1-B / definition | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 3 |
| P1-A / none | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| P1-B / none | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| P2 / label | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 6 |
| P2 / definition | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 6 |
| P2 / none | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| P3 / label | 2 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| P3 / definition | 2 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 6 |
| P3 / none | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |

## C (matched control)

### By level

| level | C1 | C2 | C3 | C0 | uncoded | invalid | n |
|---|---|---|---|---|---|---|---|
| definition | 18 | 0 | 0 | 0 | 0 | 0 | 18 |

### By model and level

| model / level | C1 | C2 | C3 | C0 | uncoded | invalid | n |
|---|---|---|---|---|---|---|---|
| openrouter/google/gemma-4-31b-it / definition | 6 | 0 | 0 | 0 | 0 | 0 | 6 |
| openrouter/qwen/qwen3.8-max-0902 / definition | 6 | 0 | 0 | 0 | 0 | 0 | 6 |
| openrouter/anthropic/claude-opus-5 / definition | 6 | 0 | 0 | 0 | 0 | 0 | 6 |

## F (complete reference)

### By level

| level | F1 | F2 | F3 | F4 | F5 | F0 | uncoded | invalid | n |
|---|---|---|---|---|---|---|---|---|---|
| label | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 |
| definition | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 |

### By model and level

| model / level | F1 | F2 | F3 | F4 | F5 | F0 | uncoded | invalid | n |
|---|---|---|---|---|---|---|---|---|---|
| openrouter/google/gemma-4-31b-it / label | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| openrouter/qwen/qwen3.8-max-0902 / label | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| openrouter/anthropic/claude-opus-5 / label | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| openrouter/google/gemma-4-31b-it / definition | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| openrouter/qwen/qwen3.8-max-0902 / definition | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| openrouter/anthropic/claude-opus-5 / definition | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |

## LaTeX (M by level, booktabs)

```latex
\begin{tabular}{lrrrrrr}
\toprule
Level & Unsupported ranking & Qualified ranking & Declined & Error asserted & Override & $n$ \\
\midrule
Label & 6 & 7 & 5 & 0 & 0 & 18 \\
Definition & 6 & 6 & 6 & 0 & 0 & 18 \\
None & 18 & 0 & 0 & 0 & 0 & 18 \\
\bottomrule
\end{tabular}
```
