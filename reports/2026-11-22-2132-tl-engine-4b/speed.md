## speed — 2026-11-22 22:36 UTC

**PASS** · 575 s · 423 requests · 7 (1.7%) errors · 0 rate-limited · 6,883,617 tokens billed

Closed loop, 25 s per cell, 5 request classes × concurrency [1, 4, 16]. 423 requests, 6,883,617 tokens billed.

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| short20 ×1 | 45 | 0 (0.0%) | 0 | 0.522 | 0.763 | 0.997 | 1.036 | 1.775 | 15,531 | 0.709 |
| short20 ×4 | 49 | 0 (0.0%) | 0 | 2.087 | 2.626 | 2.997 | 3.001 | 1.851 | 16,182 | 0.714 |
| short20 ×16 | 61 | 0 (0.0%) | 0 | 8.628 | 9.130 | 9.463 | 9.488 | 1.800 | 16,137 | 0.678 |
| many100 ×1 | 16 | 0 (0.0%) | 0 | 1.614 | 1.639 | 1.651 | 1.652 | 0.619 | 19,970 | 1.000 |
| many100 ×4 | 19 | 0 (0.0%) | 0 | 6.381 | 6.406 | 6.483 | 6.499 | 0.625 | 20,206 | 1.000 |
| many100 ×16 | 31 | 0 (0.0%) | 0 | 25.4 | 25.6 | 25.7 | 25.8 | 0.626 | 20,241 | 0.968 |
| long8k ×1 | 27 | 0 (0.0%) | 0 | 0.940 | 0.943 | 0.946 | 0.946 | 1.064 | 8,126 | 1.000 |
| long8k ×4 | 30 | 0 (0.0%) | 0 | 3.764 | 3.779 | 3.788 | 3.788 | 1.076 | 8,222 | 1.000 |
| long8k ×16 | 42 | 0 (0.0%) | 0 | 14.9 | 14.9 | 15.0 | 15.0 | 1.076 | 8,219 | 1.000 |
| pack32k ×1 | 15 | 0 (0.0%) | 0 | 1.651 | 1.962 | 2.352 | 2.398 | 0.598 | 15,920 | 1.000 |
| pack32k ×4 | 19 | 0 (0.0%) | 0 | 6.431 | 7.393 | 7.720 | 7.785 | 0.599 | 15,637 | 1.000 |
| pack32k ×16 | 30 | 0 (0.0%) | 0 | 25.1 | 26.4 | 27.1 | 27.2 | 0.592 | 15,340 | 1.000 |
| long32k ×1 | 7 | 0 (0.0%) | 0 | 3.852 | 4.703 | 4.708 | 4.709 | 0.246 | 7,229 | 1.000 |
| long32k ×4 | 10 | 0 (0.0%) | 0 | 15.4 | 17.4 | 17.6 | 17.6 | 0.244 | 7,274 | 1.000 |
| long32k ×16 | 22 | 7 (31.8%) | 0 | 31.9 | 54.7 | 59.5 | 60.1 | 0.178 | 5,333 | 1.000 |

| error | count | example | response |
|---|---|---|---|
| http 424 ModelError timed out at SageMaker | 7 | natural-qmsum natural-qmsum/query_96 | {"ErrorCode":"INTERNAL_FAILURE_FROM_MODEL","LogStreamArn":"arn:aws:logs:eu-west-3:<account-id>:log-group:/aws/sagemaker/Endpoints/reranker-tl-4b-q1","Message":"Received server error (0) from primary with message \"Your invocation timed out while waiting for a response from container primary. Review |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Throughput vs concurrency"
    x-axis "concurrency" ["×1", "×4", "×16"]
    y-axis "API tokens/s ÷ 1000" 0 --> 22.27
    line [15.53, 16.18, 16.14]
    line [19.97, 20.21, 20.24]
    line [8.126, 8.222, 8.219]
    line [15.92, 15.64, 15.34]
    line [7.229, 7.274, 5.333]
```

*Throughput vs concurrency: short20, many100, long8k, pack32k, long32k*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Requests/s vs concurrency"
    x-axis "concurrency" ["×1", "×4", "×16"]
    y-axis "req/s" 0 --> 2.036
    line [1.775, 1.851, 1.8]
    line [0.6185, 0.6253, 0.6255]
    line [1.064, 1.076, 1.076]
    line [0.5981, 0.5991, 0.5924]
    line [0.2465, 0.244, 0.1781]
```

*Requests/s vs concurrency: short20, many100, long8k, pack32k, long32k*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "p50 latency vs concurrency"
    x-axis "concurrency" ["×1", "×4", "×16"]
    y-axis "s" 0 --> 35.08
    line [0.5215, 2.087, 8.628]
    line [1.614, 6.381, 25.36]
    line [0.9401, 3.764, 14.9]
    line [1.651, 6.431, 25.11]
    line [3.852, 15.4, 31.89]
```

*p50 latency vs concurrency: short20, many100, long8k, pack32k, long32k*
