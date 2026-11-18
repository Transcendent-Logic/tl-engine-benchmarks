## normal — 2026-11-18 07:45 UTC

**PASS** · 301 s · 436 requests · 0 (0.0%) errors · 0 rate-limited · 4,990,225 tokens billed

5 min of Poisson traffic at 1.5 req/s; mix short20 60%, many100 10%, mid1k 10%, mid4k 10%, long8k 5%, long32k 5%. Billed 4,990,225 tokens.

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| all | 436 | 0 (0.0%) | 0 | 0.148 | 0.878 | 1.720 | 2.331 | 1.453 | 16,634 | 0.791 |
| short20 | 241 | 0 (0.0%) | 0 | 0.131 | 0.453 | 1.585 | 1.894 | 0.803 | 6,868 | 0.630 |
| many100 | 47 | 0 (0.0%) | 0 | 0.334 | 0.654 | 1.495 | 1.622 | 0.157 | 5,086 | 0.968 |
| mid1k | 42 | 0 (0.0%) | 0 | 0.032 | 0.373 | 1.389 | 1.833 | 0.140 | 140 | 1.000 |
| mid4k | 43 | 0 (0.0%) | 0 | 0.094 | 0.300 | 0.538 | 0.660 | 0.143 | 545 | 1.000 |
| long8k | 31 | 0 (0.0%) | 0 | 0.210 | 1.039 | 1.595 | 1.693 | 0.103 | 789 | 1.000 |
| long32k | 32 | 0 (0.0%) | 0 | 0.986 | 1.398 | 2.219 | 2.331 | 0.107 | 3,206 | 0.984 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "latency s" 0 --> 2.565
    line [0.1253, 0.1374, 0.1383, 0.205, 0.167, 0.1182, 0.1396, 0.1646, 0.1615, 0.1506, 0.3358]
    line [0.8581, 0.8002, 0.3621, 0.8379, 0.8706, 0.3459, 1.457, 0.9528, 0.9419, 0.6367, 0.3358]
    line [1.102, 1.34, 0.9865, 1.735, 1.001, 0.8372, 2.331, 1.073, 1.968, 1.104, 0.3358]
```

*Latency over time: p50, p90, max*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Throughput over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "" 0 --> 22.43
    line [14.17, 18.94, 14.21, 20, 20.39, 11.91, 16.05, 17.87, 15.03, 16.67, 1.09]
    line [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

*Throughput over time: API tokens/s ÷ 1000, errors*
