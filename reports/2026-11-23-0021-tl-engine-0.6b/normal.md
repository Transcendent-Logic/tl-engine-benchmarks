## normal — 2026-11-23 00:21 UTC

**PASS** · 301 s · 436 requests · 0 (0.0%) errors · 0 rate-limited · 4,988,441 tokens billed

5 min of Poisson traffic at 1.5 req/s; mix short20 60%, many100 10%, mid1k 10%, mid4k 10%, long8k 5%, long32k 5%. Billed 4,988,441 tokens.

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| all | 436 | 0 (0.0%) | 0 | 0.102 | 0.806 | 1.594 | 2.148 | 1.453 | 16,628 | 0.795 |
| short20 | 241 | 0 (0.0%) | 0 | 0.092 | 0.378 | 1.444 | 1.661 | 0.803 | 6,868 | 0.637 |
| many100 | 47 | 0 (0.0%) | 0 | 0.246 | 0.560 | 1.311 | 1.409 | 0.157 | 5,080 | 0.968 |
| mid1k | 42 | 0 (0.0%) | 0 | 0.025 | 0.276 | 1.254 | 1.648 | 0.140 | 140 | 1.000 |
| mid4k | 43 | 0 (0.0%) | 0 | 0.084 | 0.218 | 0.449 | 0.560 | 0.143 | 545 | 1.000 |
| long8k | 31 | 0 (0.0%) | 0 | 0.194 | 0.967 | 1.459 | 1.586 | 0.103 | 789 | 1.000 |
| long32k | 32 | 0 (0.0%) | 0 | 0.880 | 1.279 | 2.060 | 2.148 | 0.107 | 3,206 | 0.984 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "latency s" 0 --> 2.363
    line [0.09319, 0.09425, 0.09568, 0.1385, 0.1029, 0.08478, 0.1029, 0.1445, 0.1068, 0.105, 0.2429]
    line [0.8062, 0.6882, 0.2957, 0.7603, 0.7667, 0.2502, 1.253, 0.885, 0.8291, 0.5413, 0.2429]
    line [1.037, 1.273, 0.9239, 1.598, 0.9598, 0.7777, 2.148, 1.011, 1.864, 1.002, 0.2429]
```

*Latency over time: p50, p90, max*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Throughput over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "" 0 --> 22.44
    line [14.17, 18.93, 14.21, 19.99, 20.4, 11.91, 16.04, 17.87, 15.04, 16.66, 1.083]
    line [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

*Throughput over time: API tokens/s ÷ 1000, errors*
