## normal — 2026-11-17 16:48 UTC

**PASS** · 301 s · 437 requests · 0 (0.0%) errors · 0 rate-limited · 5,020,414 tokens billed

5 min of Poisson traffic at 1.5 req/s; mix short20 60%, many100 10%, mid1k 10%, mid4k 10%, long8k 5%, long32k 5%. Billed 5,020,414 tokens.

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| all | 437 | 0 (0.0%) | 0 | 0.339 | 1.689 | 3.888 | 4.367 | 1.457 | 16,735 | 0.793 |
| short20 | 241 | 0 (0.0%) | 0 | 0.226 | 1.371 | 3.491 | 4.034 | 0.803 | 6,866 | 0.634 |
| many100 | 48 | 0 (0.0%) | 0 | 0.557 | 1.922 | 3.474 | 3.929 | 0.160 | 5,189 | 0.958 |
| mid1k | 42 | 0 (0.0%) | 0 | 0.041 | 1.327 | 3.210 | 3.865 | 0.140 | 140 | 1.000 |
| mid4k | 43 | 0 (0.0%) | 0 | 0.144 | 0.973 | 1.979 | 2.584 | 0.143 | 545 | 1.000 |
| long8k | 31 | 0 (0.0%) | 0 | 0.464 | 2.453 | 3.596 | 3.901 | 0.103 | 789 | 1.000 |
| long32k | 32 | 0 (0.0%) | 0 | 1.627 | 2.389 | 4.044 | 4.367 | 0.107 | 3,206 | 0.984 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "latency s" 0 --> 4.804
    line [0.228, 0.2902, 0.2538, 0.3542, 0.5033, 0.2029, 0.2833, 0.5666, 0.3145, 0.4635, 0.528]
    line [1.755, 1.511, 0.675, 2.504, 1.494, 0.5722, 3.876, 1.866, 2.262, 1.249, 0.528]
    line [2.136, 2.188, 1.615, 2.937, 1.65, 1.357, 4.367, 2.403, 3.325, 1.966, 0.528]
```

*Latency over time: p50, p90, max*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Throughput over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "" 0 --> 22.43
    line [14.16, 18.93, 14.2, 19.98, 20.39, 11.92, 16.04, 17.87, 15.04, 17.75, 1.083]
    line [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

*Throughput over time: API tokens/s ÷ 1000, errors*
