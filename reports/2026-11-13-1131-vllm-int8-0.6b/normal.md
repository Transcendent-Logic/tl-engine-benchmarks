## normal — 2026-11-13 11:48 UTC

**PASS** · 301 s · 437 requests · 0 (0.0%) errors · 0 rate-limited · 5,022,011 tokens billed

5 min of Poisson traffic at 1.5 req/s; mix short20 60%, many100 10%, mid1k 10%, mid4k 10%, long8k 5%, long32k 5%. Billed 5,022,011 tokens.

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| all | 437 | 0 (0.0%) | 0 | 0.244 | 1.535 | 3.389 | 3.971 | 1.457 | 16,740 | 0.793 |
| short20 | 241 | 0 (0.0%) | 0 | 0.184 | 1.177 | 3.117 | 3.604 | 0.803 | 6,867 | 0.635 |
| many100 | 48 | 0 (0.0%) | 0 | 0.480 | 1.615 | 3.036 | 3.402 | 0.160 | 5,193 | 0.958 |
| mid1k | 42 | 0 (0.0%) | 0 | 0.035 | 1.139 | 2.838 | 3.474 | 0.140 | 140 | 1.000 |
| mid4k | 43 | 0 (0.0%) | 0 | 0.125 | 0.809 | 1.606 | 2.113 | 0.143 | 545 | 1.000 |
| long8k | 31 | 0 (0.0%) | 0 | 0.333 | 2.080 | 3.151 | 3.364 | 0.103 | 789 | 1.000 |
| long32k | 32 | 0 (0.0%) | 0 | 1.492 | 2.170 | 3.702 | 3.971 | 0.107 | 3,206 | 0.984 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "latency s" 0 --> 4.368
    line [0.1701, 0.2546, 0.1737, 0.3143, 0.314, 0.1721, 0.2223, 0.3056, 0.2546, 0.3221, 0.4442]
    line [1.614, 1.398, 0.5737, 2.088, 1.315, 0.4589, 3.376, 1.507, 2.064, 1.005, 0.4442]
    line [1.934, 2.174, 1.539, 2.675, 1.532, 1.23, 3.971, 2.014, 3.102, 1.72, 0.4442]
```

*Latency over time: p50, p90, max*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Throughput over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "" 0 --> 22.43
    line [14.17, 18.93, 14.21, 19.99, 20.39, 11.91, 16.06, 17.87, 15.04, 17.76, 1.083]
    line [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

*Throughput over time: API tokens/s ÷ 1000, errors*
