## meticulous — 2026-11-17 09:32 UTC

**PASS** · 445 s · 1628 requests · 0 (0.0%) errors · 0 rate-limited · 16,388,119 tokens billed

Sequential requests (one in flight) unless stated; every query carries a nonce so nothing is served from the API's prefix cache.


### Single document: latency vs length

| rung | Qwen tokens | billed | errors | p50 s | p90 s | max s | API tok/s |
|---|---|---|---|---|---|---|---|
| 256 | 229 | 324 | 0 (0.0%) | 0.018 | 0.019 | 0.060 | 16,690 |
| 512 | 457 | 551 | 0 (0.0%) | 0.023 | 0.024 | 0.029 | 24,222 |
| 1,024 | 911 | 1,005 | 0 (0.0%) | 0.035 | 0.036 | 0.038 | 28,550 |
| 2,048 | 1,872 | 1,966 | 0 (0.0%) | 0.065 | 0.066 | 0.067 | 29,995 |
| 4,096 | 3,707 | 3,800 | 0 (0.0%) | 0.137 | 0.139 | 0.141 | 27,650 |
| 8,192 | 7,545 | 7,640 | 0 (0.0%) | 0.344 | 0.349 | 0.351 | 22,179 |
| 16,384 | 15,274 | 15,368 | 0 (0.0%) | 0.968 | 0.974 | 0.977 | 15,864 |
| 32,768 | 25,438 | 25,536 | 0 (0.0%) | 2.212 | 2.221 | 2.227 | 11,558 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Single document: latency vs length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 2.443
    line [0.01788, 0.02258, 0.03513, 0.06542, 0.1373, 0.3436, 0.968, 2.212]
    line [0.01889, 0.02356, 0.03646, 0.06635, 0.1394, 0.349, 0.9742, 2.221]
```

*Single document: latency vs length: p50, p90*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Single document: throughput vs length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "" 0 --> 32.99
    line [16.69, 24.22, 28.55, 29.99, 27.65, 22.18, 15.86, 11.56]
```

*Single document: throughput vs length: API tokens/s ÷ 1000*


### ~30K tokens per request: latency vs document length (fewer, longer documents)

| rung | docs/request | billed | errors | p50 s | p90 s | max s | API tok/s |
|---|---|---|---|---|---|---|---|
| 256 | 100 | 32,399 | 0 (0.0%) | 0.519 | 0.524 | 0.526 | 62,343 |
| 512 | 55 | 30,293 | 0 (0.0%) | 0.471 | 0.505 | 0.529 | 63,078 |
| 1,024 | 28 | 28,181 | 0 (0.0%) | 0.494 | 0.544 | 0.552 | 56,776 |
| 2,048 | 13 | 25,578 | 0 (0.0%) | 0.513 | 0.564 | 0.601 | 51,009 |
| 4,096 | 6 | 22,809 | 0 (0.0%) | 0.598 | 0.648 | 0.688 | 39,269 |
| 8,192 | 3 | 22,923 | 0 (0.0%) | 0.788 | 0.901 | 0.972 | 30,055 |
| 16,384 | 1 | 15,367 | 0 (0.0%) | 0.971 | 0.973 | 0.978 | 15,834 |
| 32,768 | 1 | 25,541 | 0 (0.0%) | 2.210 | 2.215 | 2.226 | 11,565 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "~30K tokens: latency vs document length"
    x-axis "document length" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 2.437
    line [0.5189, 0.4711, 0.4936, 0.5125, 0.5984, 0.7879, 0.9713, 2.21]
    line [0.5238, 0.505, 0.5435, 0.5641, 0.6479, 0.9013, 0.9734, 2.215]
```

*~30K tokens: latency vs document length: p50, p90*


### Latency vs number of documents

| documents | billed | errors | p50 s | p90 s | max s | MRR |
|---|---|---|---|---|---|---|
| 1 tiny | 90.5 | 0 (0.0%) | 0.015 | 0.017 | 0.018 | 1.000 |
| 10 tiny | 924 | 0 (0.0%) | 0.030 | 0.031 | 0.032 | 1.000 |
| 100 tiny | 9,299 | 0 (0.0%) | 0.134 | 0.135 | 0.137 | 1.000 |
| 1000 tiny | 94,289 | 0 (0.0%) | 0.924 | 1.244 | 1.272 | 1.000 |
| 1×256 | 323 | 0 (0.0%) | 0.018 | 0.019 | 0.019 | 1.000 |
| 10×256 | 3,229 | 0 (0.0%) | 0.062 | 0.065 | 0.072 | 1.000 |
| 50×256 | 16,170 | 0 (0.0%) | 0.264 | 0.280 | 0.282 | 1.000 |
| 100×256 | 32,309 | 0 (0.0%) | 0.517 | 0.521 | 0.529 | 1.000 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency vs number of documents"
    x-axis "documents per request" ["1 tiny", "10 tiny", "100 tiny", "1000 tiny", "1×256", "10×256", "50×256", "100×256"]
    y-axis "s" 0 --> 1.368
    line [0.01512, 0.02968, 0.1336, 0.9235, 0.01769, 0.06169, 0.2643, 0.5173]
    line [0.01669, 0.03071, 0.1354, 1.244, 0.01926, 0.06488, 0.2796, 0.5209]
```

*Latency vs number of documents: p50, p90*


### Cold vs cached: the same single-document request sent twice in a row

The API caches prompt prefixes, so a repeated (query, document) pair skips most of the compute. Cold = fresh nonce in the query; cached = the identical request again immediately after.

| rung | pairs | cold p50 s | cached p50 s | speed-up × | cold max s | cached max s | errors |
|---|---|---|---|---|---|---|---|
| 256 | 10 | 0.019 | 0.017 | 1.119 | 0.040 | 0.018 |  |
| 512 | 10 | 0.023 | 0.018 | 1.304 | 0.024 | 0.021 |  |
| 1,024 | 10 | 0.033 | 0.019 | 1.754 | 0.036 | 0.023 |  |
| 2,048 | 10 | 0.061 | 0.023 | 2.675 | 0.062 | 0.025 |  |
| 4,096 | 10 | 0.133 | 0.030 | 4.521 | 0.136 | 0.031 |  |
| 8,192 | 10 | 0.340 | 0.044 | 7.806 | 0.345 | 0.051 |  |
| 16,384 | 10 | 0.968 | 0.070 | 13.8 | 0.978 | 0.072 |  |
| 32,768 | 10 | 2.216 | 0.101 | 21.8 | 2.222 | 0.108 |  |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Cold vs cached latency vs document length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 2.438
    line [0.01881, 0.02325, 0.03331, 0.06135, 0.1334, 0.3404, 0.968, 2.216]
    line [0.01681, 0.01784, 0.01899, 0.02294, 0.0295, 0.04361, 0.07013, 0.1015]
```

*Cold vs cached latency vs document length: cold p50, cached p50*


### short20: latency and throughput vs concurrency

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| ×1 | 141 | 0 (0.0%) | 0 | 0.172 | 0.240 | 0.306 | 0.314 | 5.622 | 49,203 | 0.676 |
| ×2 | 167 | 0 (0.0%) | 0 | 0.285 | 0.391 | 0.452 | 0.508 | 6.635 | 57,828 | 0.669 |
| ×4 | 169 | 0 (0.0%) | 0 | 0.583 | 0.725 | 0.845 | 0.858 | 6.627 | 57,722 | 0.668 |
| ×8 | 173 | 0 (0.0%) | 0 | 1.190 | 1.355 | 1.486 | 1.535 | 6.634 | 57,953 | 0.661 |
| ×16 | 181 | 0 (0.0%) | 0 | 2.375 | 2.610 | 2.764 | 2.821 | 6.635 | 57,995 | 0.667 |
| ×32 | 197 | 0 (0.0%) | 0 | 4.721 | 5.130 | 5.315 | 5.368 | 6.633 | 57,591 | 0.667 |

No 429s up to concurrency ×32.

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "short20: latency vs concurrency"
    x-axis "concurrency" ["×1", "×2", "×4", "×8", "×16", "×32"]
    y-axis "s" 0 --> 5.643
    line [0.1725, 0.2845, 0.5835, 1.19, 2.375, 4.721]
    line [0.2396, 0.3911, 0.7252, 1.355, 2.61, 5.13]
```

*short20: latency vs concurrency: p50, p90*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "short20: throughput vs concurrency"
    x-axis "concurrency" ["×1", "×2", "×4", "×8", "×16", "×32"]
    y-axis "" 0 --> 63.79
    line [5.622, 6.635, 6.627, 6.634, 6.635, 6.633]
    line [49.2, 57.83, 57.72, 57.95, 58, 57.59]
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

1628 requests, 16,388,119 tokens billed.
