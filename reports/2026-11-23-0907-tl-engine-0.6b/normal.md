## normal — 2026-11-23 09:07 UTC

**PASS** · 301 s · 437 requests · 0 (0.0%) errors · 0 rate-limited · 5,021,503 tokens billed

5 min of Poisson traffic at 1.5 req/s; mix short20 60%, many100 10%, mid1k 10%, mid4k 10%, long8k 5%, long32k 5%. Billed 5,021,503 tokens.

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| all | 437 | 0 (0.0%) | 0 | 0.104 | 0.831 | 1.590 | 2.151 | 1.457 | 16,738 | 0.794 |
| short20 | 241 | 0 (0.0%) | 0 | 0.093 | 0.399 | 1.455 | 1.666 | 0.803 | 6,867 | 0.637 |
| many100 | 48 | 0 (0.0%) | 0 | 0.246 | 0.554 | 1.276 | 1.336 | 0.160 | 5,191 | 0.958 |
| mid1k | 42 | 0 (0.0%) | 0 | 0.025 | 0.277 | 1.257 | 1.652 | 0.140 | 140 | 1.000 |
| mid4k | 43 | 0 (0.0%) | 0 | 0.084 | 0.223 | 0.450 | 0.554 | 0.143 | 545 | 1.000 |
| long8k | 31 | 0 (0.0%) | 0 | 0.196 | 0.962 | 1.460 | 1.582 | 0.103 | 789 | 1.000 |
| long32k | 32 | 0 (0.0%) | 0 | 0.894 | 1.289 | 2.068 | 2.151 | 0.107 | 3,206 | 0.984 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "latency s" 0 --> 2.366
    line [0.09387, 0.0924, 0.09596, 0.1461, 0.1034, 0.08555, 0.1019, 0.1465, 0.1114, 0.1074, 0.2462]
    line [0.8281, 0.6957, 0.3049, 0.7529, 0.7807, 0.2495, 1.237, 0.8856, 0.8442, 0.4997, 0.2462]
    line [1.037, 1.275, 0.9283, 1.594, 0.9528, 0.776, 2.151, 0.9846, 1.883, 1.003, 0.2462]
```

*Latency over time: p50, p90, max*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Throughput over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "" 0 --> 22.42
    line [14.16, 18.94, 14.2, 19.98, 20.39, 11.92, 16.05, 17.87, 15.04, 17.76, 1.087]
    line [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

*Throughput over time: API tokens/s ÷ 1000, errors*
