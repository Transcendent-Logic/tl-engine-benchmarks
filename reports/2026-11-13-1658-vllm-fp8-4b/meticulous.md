## meticulous — 2026-11-13 18:01 UTC

**PASS** · 1075 s · 888 requests · 0 (0.0%) errors · 0 rate-limited · 9,944,407 tokens billed

Sequential requests (one in flight) unless stated; every query carries a nonce so nothing is served from the API's prefix cache.


### Single document: latency vs length

| rung | Qwen tokens | billed | errors | p50 s | p90 s | max s | API tok/s |
|---|---|---|---|---|---|---|---|
| 256 | 229 | 323 | 0 (0.0%) | 0.052 | 0.054 | 0.084 | 6,055 |
| 512 | 457 | 551 | 0 (0.0%) | 0.067 | 0.069 | 0.071 | 8,181 |
| 1,024 | 911 | 1,005 | 0 (0.0%) | 0.120 | 0.122 | 0.123 | 8,362 |
| 2,048 | 1,872 | 1,966 | 0 (0.0%) | 0.246 | 0.248 | 0.253 | 7,967 |
| 4,096 | 3,707 | 3,801 | 0 (0.0%) | 0.520 | 0.523 | 0.527 | 7,327 |
| 8,192 | 7,545 | 7,640 | 0 (0.0%) | 1.195 | 1.201 | 1.207 | 6,388 |
| 16,384 | 15,274 | 15,368 | 0 (0.0%) | 3.097 | 3.101 | 3.105 | 4,963 |
| 32,768 | 25,438 | 25,536 | 0 (0.0%) | 6.668 | 6.678 | 6.730 | 3,831 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Single document: latency vs length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 7.345
    line [0.05184, 0.06709, 0.1198, 0.2464, 0.5196, 1.195, 3.097, 6.668]
    line [0.05376, 0.06928, 0.1218, 0.2476, 0.5226, 1.201, 3.101, 6.678]
```

*Single document: latency vs length: p50, p90*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Single document: throughput vs length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "" 0 --> 9.198
    line [6.055, 8.181, 8.362, 7.967, 7.327, 6.388, 4.963, 3.831]
```

*Single document: throughput vs length: API tokens/s ÷ 1000*


### ~30K tokens per request: latency vs document length (fewer, longer documents)

| rung | docs/request | billed | errors | p50 s | p90 s | max s | API tok/s |
|---|---|---|---|---|---|---|---|
| 256 | 100 | 32,379 | 0 (0.0%) | 1.886 | 1.895 | 1.902 | 17,174 |
| 512 | 55 | 30,278 | 0 (0.0%) | 1.754 | 1.867 | 1.977 | 17,085 |
| 1,024 | 28 | 28,174 | 0 (0.0%) | 1.842 | 2.043 | 2.108 | 15,200 |
| 2,048 | 13 | 25,572 | 0 (0.0%) | 1.902 | 2.110 | 2.263 | 13,815 |
| 4,096 | 6 | 22,807 | 0 (0.0%) | 2.131 | 2.354 | 2.514 | 10,931 |
| 8,192 | 3 | 22,923 | 0 (0.0%) | 2.628 | 3.045 | 3.346 | 8,995 |
| 16,384 | 1 | 15,367 | 0 (0.0%) | 3.095 | 3.100 | 3.104 | 4,965 |
| 32,768 | 1 | 25,541 | 0 (0.0%) | 6.663 | 6.680 | 6.728 | 3,830 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "~30K tokens: latency vs document length"
    x-axis "document length" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 7.348
    line [1.886, 1.754, 1.842, 1.902, 2.131, 2.628, 3.095, 6.663]
    line [1.895, 1.867, 2.043, 2.11, 2.354, 3.045, 3.1, 6.68]
```

*~30K tokens: latency vs document length: p50, p90*


### Latency vs number of documents

| documents | billed | errors | p50 s | p90 s | max s | MRR |
|---|---|---|---|---|---|---|
| 1 tiny | 91.5 | 0 (0.0%) | 0.029 | 0.030 | 0.033 | 1.000 |
| 10 tiny | 921 | 0 (0.0%) | 0.072 | 0.077 | 0.077 | 1.000 |
| 100 tiny | 9,299 | 0 (0.0%) | 0.400 | 0.402 | 0.405 | 1.000 |
| 1000 tiny | 93,489 | 0 (0.0%) | 2.902 | 3.789 | 3.810 | 1.000 |
| 1×256 | 323 | 0 (0.0%) | 0.052 | 0.054 | 0.055 | 1.000 |
| 10×256 | 3,232 | 0 (0.0%) | 0.233 | 0.263 | 0.284 | 1.000 |
| 50×256 | 16,155 | 0 (0.0%) | 0.960 | 1.027 | 1.057 | 1.000 |
| 100×256 | 32,339 | 0 (0.0%) | 1.875 | 1.886 | 1.886 | 0.950 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency vs number of documents"
    x-axis "documents per request" ["1 tiny", "10 tiny", "100 tiny", "1000 tiny", "1×256", "10×256", "50×256", "100×256"]
    y-axis "s" 0 --> 4.168
    line [0.02851, 0.07161, 0.3999, 2.902, 0.05194, 0.2333, 0.9601, 1.875]
    line [0.02989, 0.07687, 0.4023, 3.789, 0.05363, 0.2629, 1.027, 1.886]
```

*Latency vs number of documents: p50, p90*


### Cold vs cached: the same single-document request sent twice in a row

The API caches prompt prefixes, so a repeated (query, document) pair skips most of the compute. Cold = fresh nonce in the query; cached = the identical request again immediately after.

| rung | pairs | cold p50 s | cached p50 s | speed-up × | cold max s | cached max s | errors |
|---|---|---|---|---|---|---|---|
| 256 | 10 | 0.048 | 0.030 | 1.622 | 0.066 | 0.031 |  |
| 512 | 10 | 0.061 | 0.031 | 1.953 | 0.063 | 0.032 |  |
| 1,024 | 10 | 0.114 | 0.033 | 3.444 | 0.116 | 0.033 |  |
| 2,048 | 10 | 0.239 | 0.037 | 6.470 | 0.244 | 0.038 |  |
| 4,096 | 10 | 0.506 | 0.044 | 11.5 | 0.513 | 0.045 |  |
| 8,192 | 10 | 1.186 | 0.057 | 20.9 | 1.196 | 0.058 |  |
| 16,384 | 10 | 3.080 | 0.083 | 37.3 | 3.089 | 0.084 |  |
| 32,768 | 10 | 6.657 | 0.115 | 58.0 | 6.710 | 0.118 |  |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Cold vs cached latency vs document length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 7.323
    line [0.04849, 0.06127, 0.1138, 0.2392, 0.5056, 1.186, 3.08, 6.657]
    line [0.02989, 0.03137, 0.03305, 0.03696, 0.04394, 0.05675, 0.0826, 0.1148]
```

*Cold vs cached latency vs document length: cold p50, cached p50*


### short20: latency and throughput vs concurrency

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| ×1 | 37 | 0 (0.0%) | 0 | 0.626 | 0.978 | 1.196 | 1.233 | 1.457 | 12,879 | 0.680 |
| ×2 | 40 | 0 (0.0%) | 0 | 1.423 | 1.673 | 1.927 | 1.928 | 1.543 | 13,448 | 0.723 |
| ×4 | 41 | 0 (0.0%) | 0 | 2.528 | 3.207 | 3.452 | 3.457 | 1.509 | 13,124 | 0.732 |
| ×8 | 46 | 0 (0.0%) | 0 | 5.057 | 5.911 | 6.245 | 6.245 | 1.564 | 13,590 | 0.728 |
| ×16 | 54 | 0 (0.0%) | 0 | 10.1 | 10.8 | 11.1 | 11.3 | 1.546 | 13,624 | 0.715 |
| ×32 | 70 | 0 (0.0%) | 0 | 20.2 | 21.1 | 21.6 | 21.6 | 1.531 | 13,619 | 0.687 |

No 429s up to concurrency ×32.

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "short20: latency vs concurrency"
    x-axis "concurrency" ["×1", "×2", "×4", "×8", "×16", "×32"]
    y-axis "s" 0 --> 23.24
    line [0.6258, 1.423, 2.528, 5.057, 10.09, 20.19]
    line [0.9776, 1.673, 3.207, 5.911, 10.78, 21.13]
```

*short20: latency vs concurrency: p50, p90*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "short20: throughput vs concurrency"
    x-axis "concurrency" ["×1", "×2", "×4", "×8", "×16", "×32"]
    y-axis "" 0 --> 14.99
    line [1.457, 1.543, 1.509, 1.564, 1.546, 1.531]
    line [12.88, 13.45, 13.12, 13.59, 13.62, 13.62]
```

*short20: throughput vs concurrency: req/s, API tokens/s ÷ 1000*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "short20: 429s per second vs concurrency"
    x-axis "concurrency" ["×1", "×2", "×4", "×8", "×16", "×32"]
    y-axis "429 responses/s" 0 --> 1.1
    line [0, 0, 0, 0, 0, 0]
```

*short20: 429s per second vs concurrency: 429/s*

888 requests, 9,944,407 tokens billed.
