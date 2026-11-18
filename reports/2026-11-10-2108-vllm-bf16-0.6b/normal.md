## normal — 2026-11-10 21:26 UTC

**PASS** · 301 s · 437 requests · 0 (0.0%) errors · 0 rate-limited · 5,021,049 tokens billed

5 min of Poisson traffic at 1.5 req/s; mix short20 60%, many100 10%, mid1k 10%, mid4k 10%, long8k 5%, long32k 5%. Billed 5,021,049 tokens.

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| all | 437 | 0 (0.0%) | 0 | 0.329 | 1.715 | 3.753 | 4.241 | 1.457 | 16,737 | 0.793 |
| short20 | 241 | 0 (0.0%) | 0 | 0.214 | 1.340 | 3.375 | 3.911 | 0.803 | 6,867 | 0.636 |
| many100 | 48 | 0 (0.0%) | 0 | 0.545 | 1.837 | 3.350 | 3.793 | 0.160 | 5,190 | 0.958 |
| mid1k | 42 | 0 (0.0%) | 0 | 0.037 | 1.252 | 3.094 | 3.744 | 0.140 | 140 | 1.000 |
| mid4k | 43 | 0 (0.0%) | 0 | 0.143 | 0.946 | 1.948 | 2.557 | 0.143 | 545 | 1.000 |
| long8k | 31 | 0 (0.0%) | 0 | 0.455 | 2.342 | 3.487 | 3.758 | 0.103 | 789 | 1.000 |
| long32k | 32 | 0 (0.0%) | 0 | 1.603 | 2.265 | 3.928 | 4.241 | 0.107 | 3,206 | 0.984 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "latency s" 0 --> 4.665
    line [0.2929, 0.2841, 0.2414, 0.3509, 0.4389, 0.1867, 0.2704, 0.4946, 0.2947, 0.4381, 0.5049]
    line [1.848, 1.587, 0.6688, 2.477, 1.456, 0.5366, 3.748, 1.874, 2.163, 1.179, 0.5049]
    line [2.27, 2.223, 1.602, 2.911, 1.616, 1.326, 4.241, 2.312, 3.231, 1.891, 0.5049]
```

*Latency over time: p50, p90, max*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Throughput over time"
    x-axis "minute" ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    y-axis "" 0 --> 22.41
    line [14.16, 18.94, 14.2, 19.98, 20.37, 11.92, 16.05, 17.86, 15.04, 17.75, 1.083]
    line [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

*Throughput over time: API tokens/s ÷ 1000, errors*
