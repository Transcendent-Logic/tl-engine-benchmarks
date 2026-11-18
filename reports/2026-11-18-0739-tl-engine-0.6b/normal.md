## normal — 2026-11-18 07:39 UTC

**PASS** · 301 s · 436 requests · 0 (0.0%) errors · 0 rate-limited · 4,988,419 tokens billed

5 min of Poisson traffic at 1.5 req/s; mix short20 60%, many100 10%, mid1k 10%, mid4k 10%, long8k 5%, long32k 5%. Billed 4,988,419 tokens.

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| all | 436 | 0 (0.0%) | 0 | 0.147 | 0.897 | 1.739 | 2.408 | 1.453 | 16,628 | 0.793 |
| short20 | 241 | 0 (0.0%) | 0 | 0.127 | 0.478 | 1.647 | 1.977 | 0.803 | 6,868 | 0.634 |
| many100 | 47 | 0 (0.0%) | 0 | 0.333 | 0.706 | 1.506 | 1.633 | 0.157 | 5,080 | 0.968 |
| mid1k | 42 | 0 (0.0%) | 0 | 0.030 | 0.376 | 1.430 | 1.913 | 0.140 | 140 | 1.000 |
| mid4k | 43 | 0 (0.0%) | 0 | 0.091 | 0.315 | 0.588 | 0.728 | 0.143 | 545 | 1.000 |
| long8k | 31 | 0 (0.0%) | 0 | 0.210 | 1.058 | 1.663 | 1.741 | 0.103 | 789 | 1.000 |
| long32k | 32 | 0 (0.0%) | 0 | 0.998 | 1.411 | 2.279 | 2.408 | 0.107 | 3,206 | 0.984 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "latency s" 0 --> 2.649
    line [0.1246, 0.136, 0.1289, 0.2083, 0.161, 0.1137, 0.139, 0.1678, 0.1625, 0.1445, 0.3253]
    line [0.8777, 0.8102, 0.3741, 0.8641, 0.8943, 0.342, 1.543, 0.9678, 0.96, 0.6408, 0.3253]
    line [1.122, 1.376, 1.002, 1.741, 1.021, 0.8479, 2.408, 1.091, 1.991, 1.114, 0.3253]
```

*Latency over time: p50, p90, max*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Throughput over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "" 0 --> 22.43
    line [14.17, 18.94, 14.19, 19.99, 20.39, 11.92, 16.04, 17.87, 15.03, 16.67, 1.087]
    line [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

*Throughput over time: API tokens/s ÷ 1000, errors*
