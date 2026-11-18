## normal — 2026-11-17 16:32 UTC

**PASS** · 301 s · 437 requests · 0 (0.0%) errors · 0 rate-limited · 5,022,151 tokens billed

5 min of Poisson traffic at 1.5 req/s; mix short20 60%, many100 10%, mid1k 10%, mid4k 10%, long8k 5%, long32k 5%. Billed 5,022,151 tokens.

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| all | 437 | 0 (0.0%) | 0 | 0.336 | 1.672 | 3.817 | 4.304 | 1.457 | 16,741 | 0.791 |
| short20 | 241 | 0 (0.0%) | 0 | 0.225 | 1.337 | 3.441 | 3.967 | 0.803 | 6,868 | 0.632 |
| many100 | 48 | 0 (0.0%) | 0 | 0.546 | 1.899 | 3.420 | 3.853 | 0.160 | 5,193 | 0.958 |
| mid1k | 42 | 0 (0.0%) | 0 | 0.040 | 1.306 | 3.161 | 3.805 | 0.140 | 140 | 1.000 |
| mid4k | 43 | 0 (0.0%) | 0 | 0.145 | 0.951 | 1.931 | 2.528 | 0.143 | 545 | 1.000 |
| long8k | 31 | 0 (0.0%) | 0 | 0.465 | 2.424 | 3.533 | 3.824 | 0.103 | 789 | 1.000 |
| long32k | 32 | 0 (0.0%) | 0 | 1.592 | 2.351 | 3.992 | 4.304 | 0.107 | 3,206 | 0.984 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "latency s" 0 --> 4.734
    line [0.2176, 0.2875, 0.2212, 0.3571, 0.4502, 0.2015, 0.2802, 0.5451, 0.3327, 0.4631, 0.5257]
    line [1.744, 1.502, 0.6405, 2.46, 1.463, 0.5549, 3.811, 1.812, 2.233, 1.225, 0.5257]
    line [2.124, 2.201, 1.597, 2.904, 1.621, 1.342, 4.304, 2.365, 3.299, 1.949, 0.5257]
```

*Latency over time: p50, p90, max*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Throughput over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "" 0 --> 22.43
    line [14.17, 18.93, 14.2, 19.98, 20.39, 11.92, 16.05, 17.87, 15.04, 17.76, 1.087]
    line [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

*Throughput over time: API tokens/s ÷ 1000, errors*
