## speed — 2026-11-22 18:34 UTC

**PASS** · 441 s · 2032 requests · 0 (0.0%) errors · 0 rate-limited · 32,138,057 tokens billed

Closed loop, 25 s per cell, 5 request classes × concurrency [1, 4, 16]. 2032 requests, 32,138,057 tokens billed.

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| short20 ×1 | 273 | 0 (0.0%) | 0 | 0.088 | 0.128 | 0.161 | 0.170 | 10.9 | 96,199 | 0.651 |
| short20 ×4 | 316 | 0 (0.0%) | 0 | 0.319 | 0.388 | 0.453 | 0.515 | 12.5 | 108,108 | 0.642 |
| short20 ×16 | 329 | 0 (0.0%) | 0 | 1.266 | 1.383 | 1.462 | 1.473 | 12.6 | 108,654 | 0.640 |
| many100 ×1 | 101 | 0 (0.0%) | 0 | 0.245 | 0.252 | 0.266 | 0.272 | 4.036 | 130,730 | 0.980 |
| many100 ×4 | 116 | 0 (0.0%) | 0 | 0.888 | 0.894 | 0.947 | 0.970 | 4.488 | 145,350 | 0.983 |
| many100 ×16 | 127 | 0 (0.0%) | 0 | 3.551 | 3.561 | 3.673 | 3.919 | 4.483 | 145,156 | 0.984 |
| long8k ×1 | 125 | 0 (0.0%) | 0 | 0.200 | 0.201 | 0.203 | 0.232 | 4.997 | 38,181 | 1.000 |
| long8k ×4 | 132 | 0 (0.0%) | 0 | 0.781 | 0.790 | 0.791 | 0.792 | 5.144 | 39,299 | 1.000 |
| long8k ×16 | 144 | 0 (0.0%) | 0 | 3.128 | 3.139 | 3.145 | 3.147 | 5.125 | 39,159 | 1.000 |
| pack32k ×1 | 80 | 0 (0.0%) | 0 | 0.283 | 0.467 | 0.541 | 0.575 | 3.196 | 83,466 | 1.000 |
| pack32k ×4 | 88 | 0 (0.0%) | 0 | 1.195 | 1.367 | 1.474 | 1.477 | 3.370 | 87,435 | 1.000 |
| pack32k ×16 | 100 | 0 (0.0%) | 0 | 4.703 | 4.991 | 5.229 | 5.245 | 3.375 | 87,696 | 1.000 |
| long32k ×1 | 27 | 0 (0.0%) | 0 | 0.883 | 1.303 | 1.307 | 1.307 | 1.061 | 31,231 | 1.000 |
| long32k ×4 | 31 | 0 (0.0%) | 0 | 3.640 | 4.241 | 4.340 | 4.342 | 1.065 | 31,416 | 1.000 |
| long32k ×16 | 43 | 0 (0.0%) | 0 | 14.9 | 16.0 | 16.2 | 16.2 | 1.060 | 31,453 | 0.988 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Throughput vs concurrency"
    x-axis "concurrency" ["×1", "×4", "×16"]
    y-axis "API tokens/s ÷ 1000" 0 --> 159.9
    line [96.2, 108.1, 108.7]
    line [130.7, 145.4, 145.2]
    line [38.18, 39.3, 39.16]
    line [83.47, 87.43, 87.7]
    line [31.23, 31.42, 31.45]
```

*Throughput vs concurrency: short20, many100, long8k, pack32k, long32k*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Requests/s vs concurrency"
    x-axis "concurrency" ["×1", "×4", "×16"]
    y-axis "req/s" 0 --> 13.85
    line [10.91, 12.52, 12.59]
    line [4.036, 4.488, 4.483]
    line [4.997, 5.144, 5.125]
    line [3.196, 3.37, 3.375]
    line [1.061, 1.065, 1.06]
```

*Requests/s vs concurrency: short20, many100, long8k, pack32k, long32k*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "p50 latency vs concurrency"
    x-axis "concurrency" ["×1", "×4", "×16"]
    y-axis "s" 0 --> 16.39
    line [0.08802, 0.3192, 1.266]
    line [0.2451, 0.888, 3.551]
    line [0.1996, 0.7814, 3.128]
    line [0.2832, 1.195, 4.703]
    line [0.8826, 3.64, 14.9]
```

*p50 latency vs concurrency: short20, many100, long8k, pack32k, long32k*
