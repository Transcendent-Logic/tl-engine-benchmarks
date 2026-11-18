## meticulous — 2026-11-16 08:14 UTC

**PASS** · 1436 s · 803 requests · 1 (0.1%) errors · 0 rate-limited · 9,208,211 tokens billed

Sequential requests (one in flight) unless stated; every query carries a nonce so nothing is served from the API's prefix cache.


### Single document: latency vs length

| rung | Qwen tokens | billed | errors | p50 s | p90 s | max s | API tok/s |
|---|---|---|---|---|---|---|---|
| 256 | 229 | 324 | 0 (0.0%) | 0.087 | 0.089 | 0.121 | 3,668 |
| 512 | 457 | 551 | 0 (0.0%) | 0.107 | 0.110 | 0.113 | 5,109 |
| 1,024 | 911 | 1,005 | 1 (3.3%) | 0.196 | 0.199 | 0.201 | 5,104 |
| 2,048 | 1,872 | 1,966 | 0 (0.0%) | 0.390 | 0.395 | 0.395 | 5,022 |
| 4,096 | 3,707 | 3,800 | 0 (0.0%) | 0.797 | 0.801 | 0.808 | 4,769 |
| 8,192 | 7,545 | 7,640 | 0 (0.0%) | 1.747 | 1.751 | 1.758 | 4,374 |
| 16,384 | 15,274 | 15,368 | 0 (0.0%) | 4.248 | 4.252 | 4.255 | 3,617 |
| 32,768 | 25,438 | 25,536 | 0 (0.0%) | 8.618 | 8.631 | 8.687 | 2,963 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Single document: latency vs length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 9.494
    line [0.08695, 0.1073, 0.1961, 0.3904, 0.7966, 1.747, 4.248, 8.618]
    line [0.08893, 0.1096, 0.1987, 0.395, 0.8013, 1.751, 4.252, 8.631]
```

*Single document: latency vs length: p50, p90*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Single document: throughput vs length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "" 0 --> 5.62
    line [3.668, 5.109, 5.104, 5.022, 4.769, 4.374, 3.617, 2.963]
```

*Single document: throughput vs length: API tokens/s ÷ 1000*


### ~30K tokens per request: latency vs document length (fewer, longer documents)

| rung | docs/request | billed | errors | p50 s | p90 s | max s | API tok/s |
|---|---|---|---|---|---|---|---|
| 256 | 100 | 32,346 | 0 (0.0%) | 2.976 | 2.999 | 3.016 | 10,846 |
| 512 | 55 | 30,293 | 0 (0.0%) | 2.777 | 2.965 | 3.131 | 10,797 |
| 1,024 | 28 | 28,178 | 0 (0.0%) | 2.917 | 3.200 | 3.302 | 9,674 |
| 2,048 | 13 | 25,573 | 0 (0.0%) | 2.932 | 3.262 | 3.488 | 8,942 |
| 4,096 | 6 | 22,804 | 0 (0.0%) | 3.190 | 3.538 | 3.767 | 7,288 |
| 8,192 | 3 | 22,922 | 0 (0.0%) | 3.761 | 4.400 | 4.845 | 6,258 |
| 16,384 | 1 | 15,367 | 0 (0.0%) | 4.238 | 4.240 | 4.241 | 3,626 |
| 32,768 | 1 | 25,541 | 0 (0.0%) | 8.609 | 8.625 | 8.683 | 2,967 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "~30K tokens: latency vs document length"
    x-axis "document length" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 9.487
    line [2.976, 2.777, 2.917, 2.932, 3.19, 3.761, 4.238, 8.609]
    line [2.999, 2.965, 3.2, 3.262, 3.538, 4.4, 4.24, 8.625]
```

*~30K tokens: latency vs document length: p50, p90*


### Latency vs number of documents

| documents | billed | errors | p50 s | p90 s | max s | MRR |
|---|---|---|---|---|---|---|
| 1 tiny | 91.0 | 0 (0.0%) | 0.046 | 0.046 | 0.049 | 1.000 |
| 10 tiny | 923 | 0 (0.0%) | 0.106 | 0.127 | 0.132 | 1.000 |
| 100 tiny | 9,319 | 0 (0.0%) | 0.490 | 0.631 | 0.632 | 1.000 |
| 1000 tiny | 94,289 | 0 (0.0%) | 3.334 | 3.636 | 5.789 | 1.000 |
| 1×256 | 323 | 0 (0.0%) | 0.087 | 0.088 | 0.090 | 1.000 |
| 10×256 | 3,232 | 0 (0.0%) | 0.386 | 0.411 | 0.449 | 1.000 |
| 50×256 | 16,160 | 0 (0.0%) | 1.578 | 1.653 | 1.685 | 1.000 |
| 100×256 | 32,299 | 0 (0.0%) | 3.014 | 3.053 | 3.054 | 1.000 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency vs number of documents"
    x-axis "documents per request" ["1 tiny", "10 tiny", "100 tiny", "1000 tiny", "1×256", "10×256", "50×256", "100×256"]
    y-axis "s" 0 --> 3.999
    line [0.04554, 0.1061, 0.4901, 3.334, 0.0866, 0.3855, 1.578, 3.014]
    line [0.04649, 0.1273, 0.6305, 3.636, 0.0883, 0.4107, 1.653, 3.053]
```

*Latency vs number of documents: p50, p90*


### Cold vs cached: the same single-document request sent twice in a row

The API caches prompt prefixes, so a repeated (query, document) pair skips most of the compute. Cold = fresh nonce in the query; cached = the identical request again immediately after.

| rung | pairs | cold p50 s | cached p50 s | speed-up × | cold max s | cached max s | errors |
|---|---|---|---|---|---|---|---|
| 256 | 10 | 0.079 | 0.044 | 1.779 | 0.085 | 0.046 |  |
| 512 | 10 | 0.100 | 0.046 | 2.173 | 0.104 | 0.048 |  |
| 1,024 | 10 | 0.190 | 0.047 | 4.061 | 0.193 | 0.047 |  |
| 2,048 | 10 | 0.379 | 0.051 | 7.481 | 0.381 | 0.052 |  |
| 4,096 | 10 | 0.775 | 0.057 | 13.5 | 0.779 | 0.059 |  |
| 8,192 | 10 | 1.729 | 0.071 | 24.3 | 1.738 | 0.074 |  |
| 16,384 | 10 | 4.217 | 0.098 | 42.9 | 4.222 | 0.100 |  |
| 32,768 | 10 | 8.577 | 0.132 | 65.1 | 8.631 | 0.134 |  |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Cold vs cached latency vs document length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 9.435
    line [0.07893, 0.1001, 0.1899, 0.3793, 0.7748, 1.729, 4.217, 8.577]
    line [0.04437, 0.04605, 0.04675, 0.0507, 0.05729, 0.07109, 0.09822, 0.1318]
```

*Cold vs cached latency vs document length: cold p50, cached p50*


### short20: latency and throughput vs concurrency

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| ×1 | 23 | 0 (0.0%) | 0 | 0.997 | 1.401 | 1.918 | 1.957 | 0.907 | 8,006 | 0.709 |
| ×2 | 26 | 0 (0.0%) | 0 | 2.276 | 2.314 | 3.058 | 3.060 | 0.981 | 8,602 | 0.704 |
| ×4 | 27 | 0 (0.0%) | 0 | 3.912 | 5.415 | 5.438 | 5.442 | 0.947 | 8,348 | 0.735 |
| ×8 | 32 | 0 (0.0%) | 0 | 8.002 | 9.803 | 9.896 | 9.898 | 0.987 | 8,878 | 0.706 |
| ×16 | 40 | 0 (0.0%) | 0 | 15.9 | 16.7 | 17.3 | 17.4 | 0.978 | 8,524 | 0.768 |
| ×32 | 55 | 0 (0.0%) | 0 | 29.2 | 33.0 | 33.4 | 33.4 | 0.965 | 8,466 | 0.750 |

No 429s up to concurrency ×32.

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "short20: latency vs concurrency"
    x-axis "concurrency" ["×1", "×2", "×4", "×8", "×16", "×32"]
    y-axis "s" 0 --> 36.31
    line [0.9967, 2.276, 3.912, 8.002, 15.88, 29.23]
    line [1.401, 2.314, 5.415, 9.803, 16.73, 33.01]
```

*short20: latency vs concurrency: p50, p90*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "short20: throughput vs concurrency"
    x-axis "concurrency" ["×1", "×2", "×4", "×8", "×16", "×32"]
    y-axis "" 0 --> 9.765
    line [0.9069, 0.9811, 0.9465, 0.9875, 0.9778, 0.9655]
    line [8.006, 8.602, 8.348, 8.878, 8.524, 8.466]
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

| error | count | example | response |
|---|---|---|---|
| http 424 ModelError container 0 | 1 | ladder1-1024 ladder1-1024/ctx1024_query35 | {"ErrorCode":"INTERNAL_FAILURE_FROM_MODEL","LogStreamArn":"arn:aws:logs:eu-west-3:<account-id>:log-group:/aws/sagemaker/Endpoints/reranker-aws031-8b-int8-3","Message":"Received server error (0) from primary with message \"Connection reset by peer for the reranker-aws031-8b-int8-3 endpoint. Please re |

803 requests, 9,208,211 tokens billed.
