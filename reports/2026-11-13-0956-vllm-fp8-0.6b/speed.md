## speed — 2026-11-13 10:20 UTC

**PASS** · 457 s · 1318 requests · 0 (0.0%) errors · 0 rate-limited · 20,935,800 tokens billed

Closed loop, 25 s per cell, 5 request classes × concurrency [1, 4, 16]. 1318 requests, 20,935,800 tokens billed.

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| short20 ×1 | 160 | 0 (0.0%) | 0 | 0.150 | 0.203 | 0.262 | 0.268 | 6.399 | 55,761 | 0.651 |
| short20 ×4 | 205 | 0 (0.0%) | 0 | 0.498 | 0.595 | 0.651 | 0.707 | 8.056 | 69,755 | 0.654 |
| short20 ×16 | 216 | 0 (0.0%) | 0 | 1.972 | 2.135 | 2.272 | 2.326 | 8.024 | 69,520 | 0.654 |
| many100 ×1 | 56 | 0 (0.0%) | 0 | 0.450 | 0.455 | 0.460 | 0.460 | 2.221 | 71,942 | 0.982 |
| many100 ×4 | 75 | 0 (0.0%) | 0 | 1.391 | 1.431 | 1.474 | 1.580 | 2.847 | 92,157 | 0.987 |
| many100 ×16 | 86 | 0 (0.0%) | 0 | 5.612 | 5.659 | 5.710 | 5.902 | 2.823 | 91,398 | 0.988 |
| long8k ×1 | 80 | 0 (0.0%) | 0 | 0.314 | 0.317 | 0.319 | 0.321 | 3.176 | 24,268 | 1.000 |
| long8k ×4 | 88 | 0 (0.0%) | 0 | 1.190 | 1.196 | 1.202 | 1.226 | 3.381 | 25,833 | 1.000 |
| long8k ×16 | 100 | 0 (0.0%) | 0 | 4.711 | 4.766 | 4.774 | 4.789 | 3.383 | 25,850 | 1.000 |
| pack32k ×1 | 49 | 0 (0.0%) | 0 | 0.453 | 0.748 | 0.862 | 0.876 | 1.948 | 50,522 | 1.000 |
| pack32k ×4 | 60 | 0 (0.0%) | 0 | 1.738 | 2.074 | 2.243 | 2.251 | 2.276 | 59,755 | 1.000 |
| pack32k ×16 | 72 | 0 (0.0%) | 0 | 6.733 | 7.370 | 7.675 | 7.723 | 2.282 | 59,623 | 1.000 |
| long32k ×1 | 17 | 0 (0.0%) | 0 | 1.377 | 2.084 | 2.101 | 2.102 | 0.674 | 19,832 | 1.000 |
| long32k ×4 | 21 | 0 (0.0%) | 0 | 5.180 | 6.604 | 6.739 | 6.749 | 0.719 | 21,317 | 1.000 |
| long32k ×16 | 33 | 0 (0.0%) | 0 | 21.7 | 23.1 | 24.0 | 24.3 | 0.680 | 19,984 | 0.985 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Throughput vs concurrency"
    x-axis "concurrency" ["×1", "×4", "×16"]
    y-axis "API tokens/s ÷ 1000" 0 --> 101.4
    line [55.76, 69.76, 69.52]
    line [71.94, 92.16, 91.4]
    line [24.27, 25.83, 25.85]
    line [50.52, 59.75, 59.62]
    line [19.83, 21.32, 19.98]
```

*Throughput vs concurrency: short20, many100, long8k, pack32k, long32k*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Requests/s vs concurrency"
    x-axis "concurrency" ["×1", "×4", "×16"]
    y-axis "req/s" 0 --> 8.862
    line [6.399, 8.056, 8.024]
    line [2.221, 2.847, 2.823]
    line [3.176, 3.381, 3.383]
    line [1.948, 2.276, 2.282]
    line [0.6736, 0.7188, 0.6798]
```

*Requests/s vs concurrency: short20, many100, long8k, pack32k, long32k*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "p50 latency vs concurrency"
    x-axis "concurrency" ["×1", "×4", "×16"]
    y-axis "s" 0 --> 23.89
    line [0.1504, 0.4982, 1.972]
    line [0.4496, 1.391, 5.612]
    line [0.3145, 1.19, 4.711]
    line [0.4526, 1.738, 6.733]
    line [1.377, 5.18, 21.72]
```

*p50 latency vs concurrency: short20, many100, long8k, pack32k, long32k*
