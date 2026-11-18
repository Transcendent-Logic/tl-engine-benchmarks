## speed — 2026-11-17 09:43 UTC

**PASS** · 442 s · 1875 requests · 0 (0.0%) errors · 0 rate-limited · 29,617,031 tokens billed

Closed loop, 25 s per cell, 5 request classes × concurrency [1, 4, 16]. 1875 requests, 29,617,031 tokens billed.

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| short20 ×1 | 209 | 0 (0.0%) | 0 | 0.118 | 0.154 | 0.194 | 0.199 | 8.306 | 71,875 | 0.665 |
| short20 ×4 | 306 | 0 (0.0%) | 0 | 0.308 | 0.411 | 0.480 | 0.483 | 12.1 | 105,324 | 0.639 |
| short20 ×16 | 318 | 0 (0.0%) | 0 | 1.303 | 1.428 | 1.538 | 1.551 | 12.2 | 105,007 | 0.635 |
| many100 ×1 | 75 | 0 (0.0%) | 0 | 0.334 | 0.338 | 0.349 | 0.369 | 2.982 | 96,534 | 0.987 |
| many100 ×4 | 112 | 0 (0.0%) | 0 | 0.922 | 0.926 | 0.930 | 1.048 | 4.343 | 140,641 | 0.982 |
| many100 ×16 | 124 | 0 (0.0%) | 0 | 3.636 | 3.693 | 3.699 | 3.898 | 4.331 | 140,259 | 0.984 |
| long8k ×1 | 117 | 0 (0.0%) | 0 | 0.214 | 0.216 | 0.221 | 0.222 | 4.661 | 35,613 | 1.000 |
| long8k ×4 | 127 | 0 (0.0%) | 0 | 0.782 | 0.866 | 0.873 | 0.873 | 4.928 | 37,652 | 1.000 |
| long8k ×16 | 138 | 0 (0.0%) | 0 | 3.269 | 3.285 | 3.290 | 3.291 | 4.921 | 37,599 | 1.000 |
| pack32k ×1 | 70 | 0 (0.0%) | 0 | 0.328 | 0.510 | 0.589 | 0.620 | 2.772 | 72,575 | 1.000 |
| pack32k ×4 | 86 | 0 (0.0%) | 0 | 1.224 | 1.415 | 1.529 | 1.544 | 3.274 | 85,184 | 1.000 |
| pack32k ×16 | 97 | 0 (0.0%) | 0 | 4.923 | 5.297 | 5.422 | 5.430 | 3.207 | 82,994 | 1.000 |
| long32k ×1 | 26 | 0 (0.0%) | 0 | 0.937 | 1.385 | 1.389 | 1.389 | 0.992 | 29,182 | 1.000 |
| long32k ×4 | 29 | 0 (0.0%) | 0 | 3.788 | 4.400 | 4.555 | 4.582 | 1.026 | 30,369 | 1.000 |
| long32k ×16 | 41 | 0 (0.0%) | 0 | 14.9 | 16.8 | 17.0 | 17.0 | 1.009 | 29,931 | 0.988 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Throughput vs concurrency"
    x-axis "concurrency" ["×1", "×4", "×16"]
    y-axis "API tokens/s ÷ 1000" 0 --> 154.7
    line [71.87, 105.3, 105]
    line [96.53, 140.6, 140.3]
    line [35.61, 37.65, 37.6]
    line [72.58, 85.18, 82.99]
    line [29.18, 30.37, 29.93]
```

*Throughput vs concurrency: short20, many100, long8k, pack32k, long32k*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Requests/s vs concurrency"
    x-axis "concurrency" ["×1", "×4", "×16"]
    y-axis "req/s" 0 --> 13.39
    line [8.306, 12.14, 12.17]
    line [2.982, 4.343, 4.331]
    line [4.661, 4.928, 4.921]
    line [2.772, 3.274, 3.207]
    line [0.9919, 1.026, 1.009]
```

*Requests/s vs concurrency: short20, many100, long8k, pack32k, long32k*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "p50 latency vs concurrency"
    x-axis "concurrency" ["×1", "×4", "×16"]
    y-axis "s" 0 --> 16.4
    line [0.118, 0.3084, 1.303]
    line [0.3342, 0.9217, 3.636]
    line [0.2139, 0.7824, 3.269]
    line [0.3282, 1.224, 4.923]
    line [0.9371, 3.788, 14.91]
```

*p50 latency vs concurrency: short20, many100, long8k, pack32k, long32k*
