## normal — 2026-11-17 17:49 UTC

**PASS** · 301 s · 436 requests · 0 (0.0%) errors · 0 rate-limited · 4,989,654 tokens billed

5 min of Poisson traffic at 1.5 req/s; mix short20 60%, many100 10%, mid1k 10%, mid4k 10%, long8k 5%, long32k 5%. Billed 4,989,654 tokens.

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| all | 436 | 0 (0.0%) | 0 | 0.141 | 0.872 | 1.683 | 2.300 | 1.453 | 16,632 | 0.789 |
| short20 | 241 | 0 (0.0%) | 0 | 0.126 | 0.445 | 1.557 | 1.867 | 0.803 | 6,868 | 0.626 |
| many100 | 47 | 0 (0.0%) | 0 | 0.328 | 0.649 | 1.451 | 1.577 | 0.157 | 5,084 | 0.968 |
| mid1k | 42 | 0 (0.0%) | 0 | 0.030 | 0.370 | 1.366 | 1.802 | 0.140 | 140 | 1.000 |
| mid4k | 43 | 0 (0.0%) | 0 | 0.092 | 0.297 | 0.526 | 0.649 | 0.143 | 545 | 1.000 |
| long8k | 31 | 0 (0.0%) | 0 | 0.206 | 1.023 | 1.574 | 1.680 | 0.103 | 789 | 1.000 |
| long32k | 32 | 0 (0.0%) | 0 | 0.975 | 1.384 | 2.189 | 2.300 | 0.107 | 3,206 | 0.984 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "latency s" 0 --> 2.53
    line [0.1283, 0.1348, 0.1315, 0.2028, 0.1607, 0.1128, 0.1324, 0.1623, 0.1568, 0.1494, 0.3163]
    line [0.8823, 0.7957, 0.3627, 0.8311, 0.8581, 0.3414, 1.42, 0.9415, 0.9284, 0.6264, 0.3163]
    line [1.101, 1.338, 0.9776, 1.684, 0.9921, 0.8261, 2.3, 1.06, 1.942, 1.078, 0.3163]
```

*Latency over time: p50, p90, max*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Throughput over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "" 0 --> 22.43
    line [14.17, 18.93, 14.21, 19.97, 20.4, 11.91, 16.06, 17.87, 15.04, 16.68, 1.087]
    line [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

*Throughput over time: API tokens/s ÷ 1000, errors*
