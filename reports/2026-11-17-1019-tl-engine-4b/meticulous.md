## meticulous — 2026-11-17 11:09 UTC

**PASS** · 887 s · 925 requests · 0 (0.0%) errors · 0 rate-limited · 10,280,214 tokens billed

Sequential requests (one in flight) unless stated; every query carries a nonce so nothing is served from the API's prefix cache.


### Single document: latency vs length

| rung | Qwen tokens | billed | errors | p50 s | p90 s | max s | API tok/s |
|---|---|---|---|---|---|---|---|
| 256 | 229 | 323 | 0 (0.0%) | 0.050 | 0.051 | 0.098 | 6,233 |
| 512 | 457 | 551 | 0 (0.0%) | 0.064 | 0.068 | 0.069 | 8,568 |
| 1,024 | 911 | 1,005 | 0 (0.0%) | 0.107 | 0.108 | 0.111 | 9,372 |
| 2,048 | 1,872 | 1,966 | 0 (0.0%) | 0.208 | 0.210 | 0.216 | 9,440 |
| 4,096 | 3,707 | 3,801 | 0 (0.0%) | 0.439 | 0.442 | 0.445 | 8,645 |
| 8,192 | 7,545 | 7,640 | 0 (0.0%) | 0.953 | 0.957 | 0.964 | 8,017 |
| 16,384 | 15,274 | 15,368 | 0 (0.0%) | 2.343 | 2.352 | 2.355 | 6,555 |
| 32,768 | 25,438 | 25,536 | 0 (0.0%) | 4.837 | 4.843 | 4.908 | 5,277 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Single document: latency vs length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 5.327
    line [0.05009, 0.06359, 0.1071, 0.2075, 0.4394, 0.9532, 2.343, 4.837]
    line [0.05092, 0.06823, 0.1082, 0.2104, 0.4423, 0.9575, 2.352, 4.843]
```

*Single document: latency vs length: p50, p90*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Single document: throughput vs length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "" 0 --> 10.38
    line [6.233, 8.568, 9.372, 9.44, 8.645, 8.017, 6.555, 5.277]
```

*Single document: throughput vs length: API tokens/s ÷ 1000*


### ~30K tokens per request: latency vs document length (fewer, longer documents)

| rung | docs/request | billed | errors | p50 s | p90 s | max s | API tok/s |
|---|---|---|---|---|---|---|---|
| 256 | 100 | 32,406 | 0 (0.0%) | 1.661 | 1.671 | 1.682 | 19,496 |
| 512 | 55 | 30,286 | 0 (0.0%) | 1.538 | 1.627 | 1.722 | 19,549 |
| 1,024 | 28 | 28,161 | 0 (0.0%) | 1.583 | 1.730 | 1.769 | 17,859 |
| 2,048 | 13 | 25,574 | 0 (0.0%) | 1.602 | 1.771 | 1.894 | 16,375 |
| 4,096 | 6 | 22,803 | 0 (0.0%) | 1.799 | 2.000 | 2.131 | 12,848 |
| 8,192 | 3 | 22,922 | 0 (0.0%) | 2.076 | 2.416 | 2.653 | 11,377 |
| 16,384 | 1 | 15,366 | 0 (0.0%) | 2.338 | 2.342 | 2.343 | 6,571 |
| 32,768 | 1 | 25,541 | 0 (0.0%) | 4.821 | 4.837 | 4.884 | 5,290 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "~30K tokens: latency vs document length"
    x-axis "document length" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 5.32
    line [1.661, 1.538, 1.583, 1.602, 1.799, 2.076, 2.338, 4.821]
    line [1.671, 1.627, 1.73, 1.771, 2, 2.416, 2.342, 4.837]
```

*~30K tokens: latency vs document length: p50, p90*


### Latency vs number of documents

| documents | billed | errors | p50 s | p90 s | max s | MRR |
|---|---|---|---|---|---|---|
| 1 tiny | 91.4 | 0 (0.0%) | 0.032 | 0.033 | 0.036 | 1.000 |
| 10 tiny | 927 | 0 (0.0%) | 0.073 | 0.074 | 0.074 | 1.000 |
| 100 tiny | 9,339 | 0 (0.0%) | 0.359 | 0.373 | 0.374 | 1.000 |
| 1000 tiny | 93,989 | 0 (0.0%) | 3.490 | 3.578 | 3.589 | 1.000 |
| 1×256 | 324 | 0 (0.0%) | 0.050 | 0.050 | 0.050 | 1.000 |
| 10×256 | 3,233 | 0 (0.0%) | 0.209 | 0.228 | 0.267 | 1.000 |
| 50×256 | 16,140 | 0 (0.0%) | 0.847 | 0.909 | 0.941 | 1.000 |
| 100×256 | 32,389 | 0 (0.0%) | 1.652 | 1.670 | 1.672 | 0.950 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency vs number of documents"
    x-axis "documents per request" ["1 tiny", "10 tiny", "100 tiny", "1000 tiny", "1×256", "10×256", "50×256", "100×256"]
    y-axis "s" 0 --> 3.936
    line [0.03249, 0.07253, 0.3594, 3.49, 0.04969, 0.2088, 0.8472, 1.652]
    line [0.03327, 0.07364, 0.3725, 3.578, 0.05008, 0.2284, 0.9094, 1.67]
```

*Latency vs number of documents: p50, p90*


### Cold vs cached: the same single-document request sent twice in a row

The API caches prompt prefixes, so a repeated (query, document) pair skips most of the compute. Cold = fresh nonce in the query; cached = the identical request again immediately after.

| rung | pairs | cold p50 s | cached p50 s | speed-up × | cold max s | cached max s | errors |
|---|---|---|---|---|---|---|---|
| 256 | 10 | 0.047 | 0.035 | 1.338 | 0.064 | 0.036 |  |
| 512 | 10 | 0.059 | 0.038 | 1.561 | 0.065 | 0.040 |  |
| 1,024 | 10 | 0.100 | 0.039 | 2.545 | 0.102 | 0.040 |  |
| 2,048 | 10 | 0.201 | 0.042 | 4.765 | 0.208 | 0.043 |  |
| 4,096 | 10 | 0.429 | 0.049 | 8.807 | 0.433 | 0.051 |  |
| 8,192 | 10 | 0.932 | 0.068 | 13.7 | 0.944 | 0.069 |  |
| 16,384 | 10 | 2.327 | 0.094 | 24.8 | 2.335 | 0.099 |  |
| 32,768 | 10 | 4.811 | 0.133 | 36.2 | 4.875 | 0.135 |  |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Cold vs cached latency vs document length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 5.292
    line [0.04712, 0.0586, 0.1001, 0.2008, 0.429, 0.9318, 2.327, 4.811]
    line [0.03521, 0.03755, 0.03935, 0.04214, 0.04871, 0.06816, 0.094, 0.1327]
```

*Cold vs cached latency vs document length: cold p50, cached p50*


### short20: latency and throughput vs concurrency

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| ×1 | 43 | 0 (0.0%) | 0 | 0.539 | 0.793 | 1.023 | 1.058 | 1.701 | 14,686 | 0.707 |
| ×2 | 46 | 0 (0.0%) | 0 | 1.068 | 1.476 | 1.830 | 1.958 | 1.797 | 15,614 | 0.717 |
| ×4 | 48 | 0 (0.0%) | 0 | 2.012 | 2.794 | 2.831 | 2.845 | 1.816 | 15,854 | 0.729 |
| ×8 | 52 | 0 (0.0%) | 0 | 4.379 | 4.841 | 5.189 | 5.190 | 1.794 | 15,888 | 0.720 |
| ×16 | 60 | 0 (0.0%) | 0 | 8.794 | 9.187 | 9.392 | 9.573 | 1.787 | 15,978 | 0.687 |
| ×32 | 76 | 0 (0.0%) | 0 | 17.6 | 18.4 | 18.5 | 18.5 | 1.773 | 15,711 | 0.682 |

No 429s up to concurrency ×32.

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "short20: latency vs concurrency"
    x-axis "concurrency" ["×1", "×2", "×4", "×8", "×16", "×32"]
    y-axis "s" 0 --> 20.25
    line [0.539, 1.068, 2.012, 4.379, 8.794, 17.65]
    line [0.7926, 1.476, 2.794, 4.841, 9.187, 18.41]
```

*short20: latency vs concurrency: p50, p90*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "short20: throughput vs concurrency"
    x-axis "concurrency" ["×1", "×2", "×4", "×8", "×16", "×32"]
    y-axis "" 0 --> 17.58
    line [1.701, 1.797, 1.816, 1.794, 1.787, 1.773]
    line [14.69, 15.61, 15.85, 15.89, 15.98, 15.71]
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

925 requests, 10,280,214 tokens billed.
