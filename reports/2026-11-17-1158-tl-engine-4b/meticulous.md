## meticulous — 2026-11-17 12:49 UTC

**PASS** · 911 s · 915 requests · 0 (0.0%) errors · 0 rate-limited · 10,180,207 tokens billed

Sequential requests (one in flight) unless stated; every query carries a nonce so nothing is served from the API's prefix cache.


### Single document: latency vs length

| rung | Qwen tokens | billed | errors | p50 s | p90 s | max s | API tok/s |
|---|---|---|---|---|---|---|---|
| 256 | 229 | 324 | 0 (0.0%) | 0.050 | 0.051 | 0.082 | 6,359 |
| 512 | 457 | 551 | 0 (0.0%) | 0.062 | 0.069 | 0.070 | 8,645 |
| 1,024 | 911 | 1,005 | 0 (0.0%) | 0.107 | 0.109 | 0.113 | 9,318 |
| 2,048 | 1,872 | 1,966 | 0 (0.0%) | 0.213 | 0.216 | 0.222 | 9,197 |
| 4,096 | 3,707 | 3,801 | 0 (0.0%) | 0.459 | 0.469 | 0.478 | 8,247 |
| 8,192 | 7,545 | 7,640 | 0 (0.0%) | 0.986 | 0.991 | 0.993 | 7,739 |
| 16,384 | 15,274 | 15,368 | 0 (0.0%) | 2.420 | 2.435 | 2.443 | 6,342 |
| 32,768 | 25,438 | 25,536 | 0 (0.0%) | 4.978 | 4.989 | 5.044 | 5,127 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Single document: latency vs length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 5.487
    line [0.04966, 0.06246, 0.1074, 0.2128, 0.4593, 0.9863, 2.42, 4.978]
    line [0.05101, 0.0685, 0.1092, 0.2162, 0.4692, 0.9907, 2.435, 4.989]
```

*Single document: latency vs length: p50, p90*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Single document: throughput vs length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "" 0 --> 10.25
    line [6.359, 8.645, 9.318, 9.197, 8.247, 7.739, 6.342, 5.127]
```

*Single document: throughput vs length: API tokens/s ÷ 1000*


### ~30K tokens per request: latency vs document length (fewer, longer documents)

| rung | docs/request | billed | errors | p50 s | p90 s | max s | API tok/s |
|---|---|---|---|---|---|---|---|
| 256 | 100 | 32,426 | 0 (0.0%) | 1.734 | 1.743 | 1.755 | 18,703 |
| 512 | 55 | 30,278 | 0 (0.0%) | 1.607 | 1.684 | 1.784 | 18,786 |
| 1,024 | 28 | 28,191 | 0 (0.0%) | 1.649 | 1.809 | 1.866 | 17,083 |
| 2,048 | 13 | 25,572 | 0 (0.0%) | 1.671 | 1.842 | 1.985 | 15,680 |
| 4,096 | 6 | 22,809 | 0 (0.0%) | 1.869 | 2.084 | 2.224 | 12,383 |
| 8,192 | 3 | 22,922 | 0 (0.0%) | 2.157 | 2.509 | 2.753 | 10,975 |
| 16,384 | 1 | 15,367 | 0 (0.0%) | 2.420 | 2.422 | 2.425 | 6,351 |
| 32,768 | 1 | 25,540 | 0 (0.0%) | 4.947 | 4.960 | 5.024 | 5,159 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "~30K tokens: latency vs document length"
    x-axis "document length" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 5.456
    line [1.734, 1.607, 1.649, 1.671, 1.869, 2.157, 2.42, 4.947]
    line [1.743, 1.684, 1.809, 1.842, 2.084, 2.509, 2.422, 4.96]
```

*~30K tokens: latency vs document length: p50, p90*


### Latency vs number of documents

| documents | billed | errors | p50 s | p90 s | max s | MRR |
|---|---|---|---|---|---|---|
| 1 tiny | 90.9 | 0 (0.0%) | 0.031 | 0.033 | 0.036 | 1.000 |
| 10 tiny | 919 | 0 (0.0%) | 0.064 | 0.072 | 0.072 | 1.000 |
| 100 tiny | 9,259 | 0 (0.0%) | 0.359 | 0.363 | 0.380 | 1.000 |
| 1000 tiny | 93,789 | 0 (0.0%) | 3.560 | 3.714 | 3.715 | 1.000 |
| 1×256 | 324 | 0 (0.0%) | 0.049 | 0.050 | 0.051 | 1.000 |
| 10×256 | 3,232 | 0 (0.0%) | 0.216 | 0.237 | 0.265 | 1.000 |
| 50×256 | 16,180 | 0 (0.0%) | 0.891 | 0.945 | 0.981 | 1.000 |
| 100×256 | 32,309 | 0 (0.0%) | 1.747 | 1.761 | 1.774 | 0.950 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency vs number of documents"
    x-axis "documents per request" ["1 tiny", "10 tiny", "100 tiny", "1000 tiny", "1×256", "10×256", "50×256", "100×256"]
    y-axis "s" 0 --> 4.086
    line [0.03072, 0.06426, 0.3586, 3.56, 0.04868, 0.2165, 0.8908, 1.747]
    line [0.03312, 0.07208, 0.3631, 3.714, 0.04976, 0.2366, 0.9448, 1.761]
```

*Latency vs number of documents: p50, p90*


### Cold vs cached: the same single-document request sent twice in a row

The API caches prompt prefixes, so a repeated (query, document) pair skips most of the compute. Cold = fresh nonce in the query; cached = the identical request again immediately after.

| rung | pairs | cold p50 s | cached p50 s | speed-up × | cold max s | cached max s | errors |
|---|---|---|---|---|---|---|---|
| 256 | 10 | 0.046 | 0.034 | 1.365 | 0.048 | 0.035 |  |
| 512 | 10 | 0.058 | 0.035 | 1.634 | 0.064 | 0.036 |  |
| 1,024 | 10 | 0.103 | 0.037 | 2.788 | 0.105 | 0.038 |  |
| 2,048 | 10 | 0.209 | 0.040 | 5.264 | 0.221 | 0.041 |  |
| 4,096 | 10 | 0.452 | 0.046 | 9.748 | 0.457 | 0.047 |  |
| 8,192 | 10 | 0.969 | 0.067 | 14.5 | 0.986 | 0.069 |  |
| 16,384 | 10 | 2.404 | 0.094 | 25.6 | 2.418 | 0.096 |  |
| 32,768 | 10 | 4.946 | 0.132 | 37.4 | 5.012 | 0.133 |  |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Cold vs cached latency vs document length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 5.44
    line [0.04595, 0.05794, 0.1032, 0.2091, 0.4519, 0.9685, 2.404, 4.946]
    line [0.03366, 0.03545, 0.03701, 0.03972, 0.04636, 0.06688, 0.09402, 0.1322]
```

*Cold vs cached latency vs document length: cold p50, cached p50*


### short20: latency and throughput vs concurrency

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| ×1 | 41 | 0 (0.0%) | 0 | 0.574 | 0.824 | 1.066 | 1.108 | 1.616 | 14,054 | 0.730 |
| ×2 | 44 | 0 (0.0%) | 0 | 1.111 | 1.559 | 1.912 | 2.041 | 1.704 | 14,691 | 0.717 |
| ×4 | 46 | 0 (0.0%) | 0 | 2.127 | 2.920 | 2.961 | 2.983 | 1.733 | 15,055 | 0.716 |
| ×8 | 51 | 0 (0.0%) | 0 | 4.390 | 5.065 | 5.641 | 5.844 | 1.744 | 15,342 | 0.716 |
| ×16 | 58 | 0 (0.0%) | 0 | 9.212 | 10.0 | 10.4 | 10.4 | 1.708 | 15,197 | 0.687 |
| ×32 | 75 | 0 (0.0%) | 0 | 18.9 | 20.0 | 20.6 | 20.6 | 1.698 | 14,997 | 0.684 |

No 429s up to concurrency ×32.

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "short20: latency vs concurrency"
    x-axis "concurrency" ["×1", "×2", "×4", "×8", "×16", "×32"]
    y-axis "s" 0 --> 21.95
    line [0.5744, 1.111, 2.127, 4.39, 9.212, 18.86]
    line [0.8236, 1.559, 2.92, 5.065, 10.01, 19.95]
```

*short20: latency vs concurrency: p50, p90*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "short20: throughput vs concurrency"
    x-axis "concurrency" ["×1", "×2", "×4", "×8", "×16", "×32"]
    y-axis "" 0 --> 16.88
    line [1.616, 1.704, 1.733, 1.744, 1.708, 1.698]
    line [14.05, 14.69, 15.05, 15.34, 15.2, 15]
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

915 requests, 10,180,207 tokens billed.
