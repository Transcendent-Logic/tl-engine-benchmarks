## quality — 2026-11-22 21:32 UTC

**PASS** · 2950 s · 2000 requests · 0 (0.0%) errors · 0 rate-limited · 29,476,787 tokens billed

Up to 300 requests per set (100 for natural-*) at 2 in flight (429s retried); 2000 requests, 29,476,787 tokens billed. nDCG@10 / MRR are against the ground-truth labels; every reference column is computed over the same requests. Local reference variants of Qwen3-Reranker-0.6B (scripts/reference.py): **none available here** — run scripts/reference.py on a GPU. |Δ| is the mean absolute score difference per document; top-1 is the share of requests where the API and the reference pick the same best document.

| set | requests | errors | 429s | nDCG@10 API | MRR API | p50 s |
|---|---|---|---|---|---|---|
| beir-arguana | 300 | 0 (0.0%) | 0 | 0.600 | 0.463 | 0.912 |
| beir-fiqa | 300 | 0 (0.0%) | 0 | 0.767 | 0.786 | 0.889 |
| beir-scifact | 300 | 0 (0.0%) | 0 | 0.847 | 0.811 | 1.409 |
| ladder-1024 | 50 | 0 (0.0%) | 0 | 1.000 | 1.000 | 3.032 |
| ladder-16384 | 50 | 0 (0.0%) | 0 | 1.000 | 1.000 | 4.576 |
| ladder-2048 | 50 | 0 (0.0%) | 0 | 1.000 | 1.000 | 3.202 |
| ladder-256 | 50 | 0 (0.0%) | 0 | 0.978 | 0.970 | 3.244 |
| ladder-32768 | 50 | 0 (0.0%) | 0 | 1.000 | 1.000 | 9.339 |
| ladder-4096 | 50 | 0 (0.0%) | 0 | 1.000 | 1.000 | 3.369 |
| ladder-512 | 50 | 0 (0.0%) | 0 | 1.000 | 1.000 | 2.956 |
| ladder-8192 | 50 | 0 (0.0%) | 0 | 1.000 | 1.000 | 4.012 |
| ladder1-1024 | 50 | 0 (0.0%) | 0 | 1.000 | 1.000 | 0.200 |
| ladder1-16384 | 50 | 0 (0.0%) | 0 | 1.000 | 1.000 | 4.577 |
| ladder1-2048 | 50 | 0 (0.0%) | 0 | 1.000 | 1.000 | 0.399 |
| ladder1-256 | 50 | 0 (0.0%) | 0 | 1.000 | 1.000 | 0.065 |
| ladder1-32768 | 50 | 0 (0.0%) | 0 | 1.000 | 1.000 | 9.341 |
| ladder1-4096 | 50 | 0 (0.0%) | 0 | 1.000 | 1.000 | 0.851 |
| ladder1-512 | 50 | 0 (0.0%) | 0 | 1.000 | 1.000 | 0.106 |
| ladder1-8192 | 50 | 0 (0.0%) | 0 | 1.000 | 1.000 | 1.836 |
| natural-2wikimqa | 100 | 0 (0.0%) | 0 | 1.000 | 1.000 | 7.624 |
| natural-qmsum | 100 | 0 (0.0%) | 0 | 0.990 | 0.987 | 7.992 |
| natural-summ_screen_fd | 100 | 0 (0.0%) | 0 | 1.000 | 1.000 | 7.996 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "nDCG@10 per set (bars: API; lines: local reference variants)"
    x-axis ["beir-arguana", "beir-fiqa", "beir-scifact", "ladder-1024", "ladder-16384", "ladder-2048", "ladder-256", "ladder-32768", "ladder-4096", "ladder-512", "ladder-8192", "ladder1-1024", "ladder1-16384", "ladder1-2048", "ladder1-256", "ladder1-32768", "ladder1-4096", "ladder1-512", "ladder1-8192", "natural-2wikimqa", "natural-qmsum", "natural-summ_screen_fd"]
    y-axis "nDCG@10" 0 --> 1.1
    bar [0.5996, 0.7668, 0.8474, 1, 1, 1, 0.9779, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.99, 1]
```

*nDCG@10 per set (bars: API; lines: local reference variants): API*
