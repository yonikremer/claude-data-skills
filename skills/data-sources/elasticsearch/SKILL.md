---
name: elasticsearch
description: Queries and indexes data in Elasticsearch 8.x. Use for full-text search, high-performance aggregations, and large-scale log analysis.
---
# Elasticsearch (8.x)

## 1. Connection (Modern Client)
```python
from elasticsearch import Elasticsearch

# 8.x client uses basic_auth or api_key
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "password"),
    verify_certs=False # Only for local dev
)
```

## 2. High-Performance Extraction (Search After)
The `scroll` API is deprecated for deep pagination. Use `search_after` with a PIT (Point in Time) or a unique sort key.

```python
def fetch_all(index, query):
    records = []
    resp = es.search(
        index=index,
        query=query,
        sort=[{"timestamp": "asc"}, {"_id": "asc"}],
        size=1000
    )
    
    while len(resp['hits']['hits']) > 0:
        hits = resp['hits']['hits']
        records.extend([h['_source'] for h in hits])
        
        # Use the sort values of the last hit to get the next page
        last_sort = hits[-1]['sort']
        resp = es.search(
            index=index,
            query=query,
            sort=[{"timestamp": "asc"}, {"_id": "asc"}],
            size=1000,
            search_after=last_sort
        )
    return records
```

## 3. Bulk Indexing (Gold Standard)
Always use the `helpers` module for bulk operations to minimize network roundtrips.
```python
from elasticsearch.helpers import bulk

actions = [
    {
        "_index": "my-index",
        "_source": doc
    }
    for doc in my_docs
]
bulk(es, actions)
```

## 4. Common Pitfalls
- **Keyword vs Text**: Use `.keyword` fields for exact matches and aggregations. Use `text` fields only for full-text search.
- **Refresh Interval**: For large bulk imports, set `index.refresh_interval: -1` to speed up ingestion, then reset to `1s` when done.
- **Mapping Explosion**: Avoid dynamic mapping for large objects; explicitly define schemas to prevent index bloating.
