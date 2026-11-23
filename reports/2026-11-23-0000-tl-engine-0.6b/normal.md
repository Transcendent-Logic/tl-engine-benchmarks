## normal — 2026-11-23 00:00 UTC

**PASS** · 301 s · 436 requests · 0 (0.0%) errors · 0 rate-limited · 4,988,682 tokens billed

5 min of Poisson traffic at 1.5 req/s; mix short20 60%, many100 10%, mid1k 10%, mid4k 10%, long8k 5%, long32k 5%. Billed 4,988,682 tokens.

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| all | 436 | 0 (0.0%) | 0 | 0.103 | 0.793 | 1.604 | 2.156 | 1.453 | 16,629 | 0.795 |
| short20 | 241 | 0 (0.0%) | 0 | 0.091 | 0.389 | 1.457 | 1.674 | 0.803 | 6,868 | 0.637 |
| many100 | 47 | 0 (0.0%) | 0 | 0.246 | 0.569 | 1.321 | 1.418 | 0.157 | 5,081 | 0.968 |
| mid1k | 42 | 0 (0.0%) | 0 | 0.025 | 0.274 | 1.263 | 1.660 | 0.140 | 140 | 1.000 |
| mid4k | 43 | 0 (0.0%) | 0 | 0.084 | 0.222 | 0.456 | 0.569 | 0.143 | 545 | 1.000 |
| long8k | 31 | 0 (0.0%) | 0 | 0.195 | 0.965 | 1.468 | 1.593 | 0.103 | 789 | 1.000 |
| long32k | 32 | 0 (0.0%) | 0 | 0.895 | 1.286 | 2.070 | 2.156 | 0.107 | 3,206 | 0.984 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "latency s" 0 --> 2.372
    line [0.09355, 0.09565, 0.09743, 0.1487, 0.1049, 0.08415, 0.1033, 0.1371, 0.1071, 0.1035, 0.2487]
    line [0.8125, 0.6942, 0.2998, 0.7701, 0.7821, 0.25, 1.266, 0.8706, 0.8302, 0.5396, 0.2487]
    line [1.037, 1.286, 0.9238, 1.609, 0.9555, 0.778, 2.156, 0.9754, 1.878, 1, 0.2487]
```

*Latency over time: p50, p90, max*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Throughput over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "" 0 --> 22.43
    line [14.17, 18.93, 14.2, 19.99, 20.39, 11.92, 16.05, 17.86, 15.02, 16.67, 1.087]
    line [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

*Throughput over time: API tokens/s ÷ 1000, errors*
