---
name: elasticsearch-query-optimization
description: Use when analyzing, profiling, or optimizing slow Elasticsearch queries, using Search Profiler, or configuring search caches.
---

# Elasticsearch Query Optimization

## Overview
This skill provides strategies for detecting, diagnosing, and solving performance issues in Elasticsearch (ES) search queries. It details mapping optimizations, query patterns, and cluster/shard sizing considerations.

## Pre-flight Checks
Before analyzing slow Elasticsearch queries:
1. **Locate Shard Allocation**: Determine how many shards the query hits. High shard counts can cause latency due to network coordination.
2. **JVM Heap Health Check**: Ensure JVM heap usage is within safe limits (typically < 75% utilization) to avoid GC pause interference.
3. **Slow Logs Check**: Check the cluster slow log parameters to see if queries exceed established latency thresholds.

## Core Workflow: Diagnosing Performance Bottlenecks

### 1. The Profile API
Use the `profile` parameter to break down search phase durations.
```json
GET /my-index/_search
{
  "profile": true,
  "query": {
    "match": {
      "message": "error occurred"
    }
  }
}
```
*Look for:*
- **query_time**: Total query execution time.
- **collector**: Time spent gathering matching documents. High collector time indicates too many matching documents or expensive sorting.
- **create_weight**: Time spent parsing query and computing weights.

### 2. Search Slow Logs
Identify long-running queries in production. Set thresholds dynamically:
```json
PUT /my-index/_settings
{
  "index.search.slowlog.threshold.query.warn": "10s",
  "index.search.slowlog.threshold.query.info": "2s",
  "index.search.slowlog.level": "info"
}
```

## Optimization Techniques

### 1. Filter Context vs Query Context
Use `filter` inside `bool` queries when relevance score (`_score`) calculation is not needed (e.g., status matching, range queries, ID lookups).
- **Query Context**: Computes scores. Slow, not cached.
- **Filter Context**: Skips scoring. Fast, automatically cached.

*Bad Query:*
```json
{
  "query": {
    "match": { "status": "active" }
  }
}
```
*Good Query:*
```json
{
  "query": {
    "bool": {
      "filter": [
        { "term": { "status": "active" } }
      ]
    }
  }
}
```

### 2. Avoid Deep Pagination
Do **NOT** use `from` and `size` to page deep into results (e.g. `from: 10000`). Each shard must build priority queues for all preceding hits.
- **Alternative**: Use the **Search After** API for sequential paging.
- **Alternative**: Use **Scroll** API for background data exporting.

### 3. Precise Document Retrieval
- Use `_source` filtering to fetch only the required fields instead of whole documents:
  ```json
  GET /my-index/_search
  {
    "_source": ["id", "timestamp", "status"],
    "query": { "term": { "user_id": 42 } }
  }
  ```
- Use `docvalue_fields` or `stored_fields` for targeted extraction of values without parsing `_source` JSON.

### 4. Schema and Mappings Tuning
- Use `keyword` fields for exact matches, filtering, and aggregations (instead of `text`).
- Disable `doc_values` and indexing on fields that are never searched or aggregated to save memory/disk.
- Use index sorting (`index.sort.field`) to pre-sort data on disk for fast retrievals aligned with your sort criteria.

---

## Wall of Shame (Pitfalls to Avoid)

| Anti-Pattern | Bad Example | Good Example | Why |
|---|---|---|---|
| Leading Wildcards | `{"wildcard": {"url": "*domain.com"}}` | Use `reversed_wildcard` analyzer, `ngram`, or `edge_ngram` | Forces ES to scan every term in the index dictionary |
| Dynamic Mapping | Relying on auto-created fields in production | Define static mappings and set `dynamic: strict` | Dynamic mappings choose suboptimal data types (e.g., `text` + `keyword` multi-fields on everything) |
| High-cardinality terms aggregation | Aggregating on unique user IDs or UUIDs without restrictions | Filter before aggregating, or use composite aggregations | Demands high JVM heap for global ordinals, risk of OutOfMemory (OOM) |
| Excessive Shard Counts | 100 small shards of 50MB each | Consolidate to 10GB-50GB shards | Coordination overhead across small shards slows queries down |
