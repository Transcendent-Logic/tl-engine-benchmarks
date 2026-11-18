## normal — 2026-11-13 10:12 UTC

**PASS** · 301 s · 437 requests · 0 (0.0%) errors · 0 rate-limited · 5,020,470 tokens billed

5 min of Poisson traffic at 1.5 req/s; mix short20 60%, many100 10%, mid1k 10%, mid4k 10%, long8k 5%, long32k 5%. Billed 5,020,470 tokens.

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| all | 437 | 0 (0.0%) | 0 | 0.247 | 1.513 | 3.345 | 3.929 | 1.457 | 16,735 | 0.789 |
| short20 | 241 | 0 (0.0%) | 0 | 0.181 | 1.163 | 3.087 | 3.564 | 0.803 | 6,867 | 0.627 |
| many100 | 48 | 0 (0.0%) | 0 | 0.473 | 1.556 | 3.006 | 3.363 | 0.160 | 5,188 | 0.958 |
| mid1k | 42 | 0 (0.0%) | 0 | 0.034 | 1.120 | 2.806 | 3.433 | 0.140 | 140 | 1.000 |
| mid4k | 43 | 0 (0.0%) | 0 | 0.122 | 0.800 | 1.571 | 2.056 | 0.143 | 545 | 1.000 |
| long8k | 31 | 0 (0.0%) | 0 | 0.330 | 2.063 | 3.093 | 3.305 | 0.103 | 789 | 1.000 |
| long32k | 32 | 0 (0.0%) | 0 | 1.476 | 2.108 | 3.665 | 3.929 | 0.107 | 3,206 | 0.984 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "latency s" 0 --> 4.322
    line [0.1705, 0.2515, 0.169, 0.3073, 0.3048, 0.1693, 0.2222, 0.2993, 0.2486, 0.3196, 0.4446]
    line [1.616, 1.36, 0.5671, 2.032, 1.307, 0.4656, 3.329, 1.54, 2.047, 1.005, 0.4446]
    line [1.903, 2.11, 1.498, 2.619, 1.508, 1.237, 3.929, 2.007, 3.077, 1.708, 0.4446]
```

*Latency over time: p50, p90, max*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Throughput over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "" 0 --> 22.43
    line [14.16, 18.94, 14.2, 19.98, 20.39, 11.91, 16.04, 17.85, 15.04, 17.75, 1.087]
    line [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

*Throughput over time: API tokens/s ÷ 1000, errors*
