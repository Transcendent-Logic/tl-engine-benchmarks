## meticulous — 2026-11-13 14:24 UTC

**PASS** · 432 s · 1777 requests · 0 (0.0%) errors · 0 rate-limited · 17,636,233 tokens billed

Sequential requests (one in flight) unless stated; every query carries a nonce so nothing is served from the API's prefix cache.


### Single document: latency vs length

| rung | Qwen tokens | billed | errors | p50 s | p90 s | max s | API tok/s |
|---|---|---|---|---|---|---|---|
| 256 | 229 | 324 | 0 (0.0%) | 0.018 | 0.019 | 0.057 | 16,817 |
| 512 | 457 | 551 | 0 (0.0%) | 0.021 | 0.022 | 0.023 | 26,346 |
| 1,024 | 911 | 1,005 | 0 (0.0%) | 0.033 | 0.035 | 0.035 | 29,912 |
| 2,048 | 1,872 | 1,966 | 0 (0.0%) | 0.060 | 0.061 | 0.062 | 32,549 |
| 4,096 | 3,707 | 3,801 | 0 (0.0%) | 0.128 | 0.129 | 0.130 | 29,671 |
| 8,192 | 7,545 | 7,639 | 0 (0.0%) | 0.325 | 0.328 | 0.334 | 23,454 |
| 16,384 | 15,274 | 15,368 | 0 (0.0%) | 0.931 | 0.936 | 0.938 | 16,486 |
| 32,768 | 25,438 | 25,536 | 0 (0.0%) | 2.167 | 2.173 | 2.182 | 11,808 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Single document: latency vs length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 2.391
    line [0.01778, 0.02055, 0.03343, 0.06034, 0.1281, 0.325, 0.9312, 2.167]
    line [0.01895, 0.02197, 0.0348, 0.06112, 0.1293, 0.3284, 0.9358, 2.173]
```

*Single document: latency vs length: p50, p90*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Single document: throughput vs length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "" 0 --> 35.8
    line [16.82, 26.35, 29.91, 32.55, 29.67, 23.45, 16.49, 11.81]
```

*Single document: throughput vs length: API tokens/s ÷ 1000*


### ~30K tokens per request: latency vs document length (fewer, longer documents)

| rung | docs/request | billed | errors | p50 s | p90 s | max s | API tok/s |
|---|---|---|---|---|---|---|---|
| 256 | 100 | 32,406 | 0 (0.0%) | 0.464 | 0.469 | 0.469 | 69,713 |
| 512 | 55 | 30,271 | 0 (0.0%) | 0.424 | 0.445 | 0.467 | 70,740 |
| 1,024 | 28 | 28,179 | 0 (0.0%) | 0.441 | 0.478 | 0.494 | 63,526 |
| 2,048 | 13 | 25,573 | 0 (0.0%) | 0.468 | 0.510 | 0.538 | 56,089 |
| 4,096 | 6 | 22,806 | 0 (0.0%) | 0.553 | 0.600 | 0.631 | 42,328 |
| 8,192 | 3 | 22,922 | 0 (0.0%) | 0.747 | 0.846 | 0.912 | 31,813 |
| 16,384 | 1 | 15,367 | 0 (0.0%) | 0.932 | 0.934 | 0.935 | 16,483 |
| 32,768 | 1 | 25,540 | 0 (0.0%) | 2.161 | 2.171 | 2.178 | 11,823 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "~30K tokens: latency vs document length"
    x-axis "document length" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 2.388
    line [0.4639, 0.4238, 0.4415, 0.468, 0.5531, 0.7466, 0.9319, 2.161]
    line [0.4689, 0.4446, 0.4777, 0.5101, 0.5997, 0.8455, 0.9341, 2.171]
```

*~30K tokens: latency vs document length: p50, p90*


### Latency vs number of documents

| documents | billed | errors | p50 s | p90 s | max s | MRR |
|---|---|---|---|---|---|---|
| 1 tiny | 90.8 | 0 (0.0%) | 0.017 | 0.019 | 0.021 | 1.000 |
| 10 tiny | 922 | 0 (0.0%) | 0.030 | 0.032 | 0.032 | 1.000 |
| 100 tiny | 9,289 | 0 (0.0%) | 0.130 | 0.133 | 0.135 | 1.000 |
| 1000 tiny | 93,889 | 0 (0.0%) | 0.906 | 1.159 | 1.182 | 0.950 |
| 1×256 | 324 | 0 (0.0%) | 0.017 | 0.018 | 0.019 | 1.000 |
| 10×256 | 3,224 | 0 (0.0%) | 0.060 | 0.063 | 0.066 | 1.000 |
| 50×256 | 16,170 | 0 (0.0%) | 0.237 | 0.245 | 0.249 | 1.000 |
| 100×256 | 32,339 | 0 (0.0%) | 0.461 | 0.467 | 0.467 | 1.000 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency vs number of documents"
    x-axis "documents per request" ["1 tiny", "10 tiny", "100 tiny", "1000 tiny", "1×256", "10×256", "50×256", "100×256"]
    y-axis "s" 0 --> 1.275
    line [0.017, 0.03048, 0.1296, 0.906, 0.0169, 0.0596, 0.237, 0.4613]
    line [0.01921, 0.03158, 0.1331, 1.159, 0.01757, 0.06252, 0.2453, 0.4665]
```

*Latency vs number of documents: p50, p90*


### Cold vs cached: the same single-document request sent twice in a row

The API caches prompt prefixes, so a repeated (query, document) pair skips most of the compute. Cold = fresh nonce in the query; cached = the identical request again immediately after.

| rung | pairs | cold p50 s | cached p50 s | speed-up × | cold max s | cached max s | errors |
|---|---|---|---|---|---|---|---|
| 256 | 10 | 0.017 | 0.017 | 1.005 | 0.044 | 0.020 |  |
| 512 | 10 | 0.020 | 0.018 | 1.144 | 0.021 | 0.019 |  |
| 1,024 | 10 | 0.033 | 0.019 | 1.719 | 0.034 | 0.020 |  |
| 2,048 | 10 | 0.057 | 0.022 | 2.647 | 0.058 | 0.024 |  |
| 4,096 | 10 | 0.124 | 0.028 | 4.477 | 0.126 | 0.033 |  |
| 8,192 | 10 | 0.319 | 0.041 | 7.767 | 0.324 | 0.047 |  |
| 16,384 | 10 | 0.925 | 0.068 | 13.6 | 0.927 | 0.069 |  |
| 32,768 | 10 | 2.171 | 0.101 | 21.6 | 2.177 | 0.101 |  |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Cold vs cached latency vs document length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 2.388
    line [0.01746, 0.02037, 0.03297, 0.05729, 0.1239, 0.3194, 0.9247, 2.171]
    line [0.01738, 0.0178, 0.01918, 0.02164, 0.02768, 0.04112, 0.06783, 0.1005]
```

*Cold vs cached latency vs document length: cold p50, cached p50*


### short20: latency and throughput vs concurrency

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| ×1 | 155 | 0 (0.0%) | 0 | 0.156 | 0.213 | 0.272 | 0.280 | 6.187 | 54,057 | 0.663 |
| ×2 | 194 | 0 (0.0%) | 0 | 0.247 | 0.338 | 0.385 | 0.399 | 7.702 | 66,968 | 0.656 |
| ×4 | 196 | 0 (0.0%) | 0 | 0.499 | 0.620 | 0.733 | 0.736 | 7.711 | 67,085 | 0.662 |
| ×8 | 200 | 0 (0.0%) | 0 | 1.025 | 1.162 | 1.264 | 1.319 | 7.673 | 66,640 | 0.657 |
| ×16 | 208 | 0 (0.0%) | 0 | 2.053 | 2.227 | 2.375 | 2.426 | 7.660 | 66,218 | 0.660 |
| ×32 | 224 | 0 (0.0%) | 0 | 4.130 | 4.406 | 4.580 | 4.631 | 7.686 | 66,449 | 0.655 |

No 429s up to concurrency ×32.

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "short20: latency vs concurrency"
    x-axis "concurrency" ["×1", "×2", "×4", "×8", "×16", "×32"]
    y-axis "s" 0 --> 4.846
    line [0.156, 0.2474, 0.4986, 1.025, 2.053, 4.13]
    line [0.213, 0.3375, 0.6195, 1.162, 2.227, 4.406]
```

*short20: latency vs concurrency: p50, p90*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "short20: throughput vs concurrency"
    x-axis "concurrency" ["×1", "×2", "×4", "×8", "×16", "×32"]
    y-axis "" 0 --> 73.79
    line [6.187, 7.702, 7.711, 7.673, 7.66, 7.686]
    line [54.06, 66.97, 67.09, 66.64, 66.22, 66.45]
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

1777 requests, 17,636,233 tokens billed.
