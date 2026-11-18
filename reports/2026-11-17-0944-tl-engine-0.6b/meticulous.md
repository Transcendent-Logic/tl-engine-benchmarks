## meticulous — 2026-11-17 09:55 UTC

**PASS** · 345 s · 2392 requests · 0 (0.0%) errors · 0 rate-limited · 22,924,382 tokens billed

Sequential requests (one in flight) unless stated; every query carries a nonce so nothing is served from the API's prefix cache.


### Single document: latency vs length

| rung | Qwen tokens | billed | errors | p50 s | p90 s | max s | API tok/s |
|---|---|---|---|---|---|---|---|
| 256 | 229 | 324 | 0 (0.0%) | 0.023 | 0.024 | 0.063 | 13,054 |
| 512 | 457 | 550 | 0 (0.0%) | 0.023 | 0.026 | 0.026 | 23,175 |
| 1,024 | 911 | 1,005 | 0 (0.0%) | 0.027 | 0.029 | 0.032 | 36,956 |
| 2,048 | 1,872 | 1,966 | 0 (0.0%) | 0.045 | 0.046 | 0.048 | 43,264 |
| 4,096 | 3,707 | 3,800 | 0 (0.0%) | 0.093 | 0.094 | 0.095 | 40,718 |
| 8,192 | 7,545 | 7,640 | 0 (0.0%) | 0.212 | 0.214 | 0.216 | 35,938 |
| 16,384 | 15,274 | 15,368 | 0 (0.0%) | 0.600 | 0.603 | 0.606 | 25,600 |
| 32,768 | 25,438 | 25,536 | 0 (0.0%) | 1.380 | 1.384 | 1.386 | 18,493 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Single document: latency vs length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 1.522
    line [0.02311, 0.02315, 0.02663, 0.04513, 0.09311, 0.2121, 0.5998, 1.38]
    line [0.02425, 0.0256, 0.02862, 0.04645, 0.09405, 0.214, 0.6025, 1.384]
```

*Single document: latency vs length: p50, p90*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Single document: throughput vs length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "" 0 --> 47.59
    line [13.05, 23.17, 36.96, 43.26, 40.72, 35.94, 25.6, 18.49]
```

*Single document: throughput vs length: API tokens/s ÷ 1000*


### ~30K tokens per request: latency vs document length (fewer, longer documents)

| rung | docs/request | billed | errors | p50 s | p90 s | max s | API tok/s |
|---|---|---|---|---|---|---|---|
| 256 | 100 | 32,406 | 0 (0.0%) | 0.333 | 0.336 | 0.337 | 97,305 |
| 512 | 55 | 30,278 | 0 (0.0%) | 0.303 | 0.317 | 0.329 | 99,524 |
| 1,024 | 28 | 28,185 | 0 (0.0%) | 0.309 | 0.328 | 0.334 | 91,784 |
| 2,048 | 13 | 25,567 | 0 (0.0%) | 0.328 | 0.354 | 0.372 | 80,070 |
| 4,096 | 6 | 22,805 | 0 (0.0%) | 0.395 | 0.432 | 0.449 | 59,039 |
| 8,192 | 3 | 22,922 | 0 (0.0%) | 0.496 | 0.571 | 0.626 | 47,074 |
| 16,384 | 1 | 15,367 | 0 (0.0%) | 0.601 | 0.602 | 0.603 | 25,584 |
| 32,768 | 1 | 25,541 | 0 (0.0%) | 1.381 | 1.385 | 1.388 | 18,480 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "~30K tokens: latency vs document length"
    x-axis "document length" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 1.524
    line [0.3325, 0.3029, 0.309, 0.3275, 0.3948, 0.4963, 0.601, 1.381]
    line [0.3356, 0.3167, 0.3285, 0.3545, 0.4319, 0.5713, 0.6018, 1.385]
```

*~30K tokens: latency vs document length: p50, p90*


### Latency vs number of documents

| documents | billed | errors | p50 s | p90 s | max s | MRR |
|---|---|---|---|---|---|---|
| 1 tiny | 91.1 | 0 (0.0%) | 0.014 | 0.015 | 0.018 | 1.000 |
| 10 tiny | 919 | 0 (0.0%) | 0.035 | 0.036 | 0.037 | 1.000 |
| 100 tiny | 9,299 | 0 (0.0%) | 0.106 | 0.107 | 0.107 | 1.000 |
| 1000 tiny | 93,789 | 0 (0.0%) | 0.931 | 0.965 | 0.991 | 1.000 |
| 1×256 | 324 | 0 (0.0%) | 0.022 | 0.024 | 0.025 | 1.000 |
| 10×256 | 3,237 | 0 (0.0%) | 0.053 | 0.057 | 0.059 | 1.000 |
| 50×256 | 16,155 | 0 (0.0%) | 0.174 | 0.187 | 0.188 | 1.000 |
| 100×256 | 32,319 | 0 (0.0%) | 0.330 | 0.334 | 0.337 | 1.000 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency vs number of documents"
    x-axis "documents per request" ["1 tiny", "10 tiny", "100 tiny", "1000 tiny", "1×256", "10×256", "50×256", "100×256"]
    y-axis "s" 0 --> 1.061
    line [0.01384, 0.03496, 0.1055, 0.9311, 0.02246, 0.05327, 0.1741, 0.3298]
    line [0.01458, 0.03634, 0.1073, 0.9649, 0.02443, 0.05689, 0.1871, 0.3344]
```

*Latency vs number of documents: p50, p90*


### Cold vs cached: the same single-document request sent twice in a row

The API caches prompt prefixes, so a repeated (query, document) pair skips most of the compute. Cold = fresh nonce in the query; cached = the identical request again immediately after.

| rung | pairs | cold p50 s | cached p50 s | speed-up × | cold max s | cached max s | errors |
|---|---|---|---|---|---|---|---|
| 256 | 10 | 0.023 | 0.015 | 1.495 | 0.049 | 0.017 |  |
| 512 | 10 | 0.023 | 0.016 | 1.452 | 0.025 | 0.018 |  |
| 1,024 | 10 | 0.026 | 0.018 | 1.464 | 0.027 | 0.019 |  |
| 2,048 | 10 | 0.042 | 0.020 | 2.110 | 0.044 | 0.022 |  |
| 4,096 | 10 | 0.089 | 0.027 | 3.285 | 0.090 | 0.029 |  |
| 8,192 | 10 | 0.208 | 0.045 | 4.616 | 0.211 | 0.047 |  |
| 16,384 | 10 | 0.591 | 0.071 | 8.313 | 0.593 | 0.074 |  |
| 32,768 | 10 | 1.380 | 0.105 | 13.2 | 1.385 | 0.107 |  |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Cold vs cached latency vs document length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 1.518
    line [0.02284, 0.02303, 0.02594, 0.04185, 0.08851, 0.2082, 0.5912, 1.38]
    line [0.01528, 0.01586, 0.01772, 0.01984, 0.02694, 0.04511, 0.07112, 0.105]
```

*Cold vs cached latency vs document length: cold p50, cached p50*


### short20: latency and throughput vs concurrency

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| ×1 | 208 | 0 (0.0%) | 0 | 0.118 | 0.156 | 0.191 | 0.196 | 8.278 | 71,571 | 0.667 |
| ×2 | 295 | 0 (0.0%) | 0 | 0.165 | 0.227 | 0.280 | 0.291 | 11.7 | 102,489 | 0.636 |
| ×4 | 314 | 0 (0.0%) | 0 | 0.298 | 0.404 | 0.471 | 0.527 | 12.4 | 107,645 | 0.634 |
| ×8 | 318 | 0 (0.0%) | 0 | 0.638 | 0.724 | 0.823 | 0.829 | 12.4 | 107,398 | 0.639 |
| ×16 | 323 | 0 (0.0%) | 0 | 1.286 | 1.409 | 1.489 | 1.518 | 12.3 | 106,600 | 0.638 |
| ×32 | 334 | 0 (0.0%) | 0 | 2.577 | 2.772 | 2.885 | 2.949 | 12.2 | 105,518 | 0.639 |

No 429s up to concurrency ×32.

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "short20: latency vs concurrency"
    x-axis "concurrency" ["×1", "×2", "×4", "×8", "×16", "×32"]
    y-axis "s" 0 --> 3.049
    line [0.1177, 0.1651, 0.2983, 0.6379, 1.286, 2.577]
    line [0.1557, 0.2267, 0.4038, 0.7241, 1.409, 2.772]
```

*short20: latency vs concurrency: p50, p90*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "short20: throughput vs concurrency"
    x-axis "concurrency" ["×1", "×2", "×4", "×8", "×16", "×32"]
    y-axis "" 0 --> 118.4
    line [8.278, 11.74, 12.45, 12.45, 12.34, 12.22]
    line [71.57, 102.5, 107.6, 107.4, 106.6, 105.5]
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

2392 requests, 22,924,382 tokens billed.
