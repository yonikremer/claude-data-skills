---
name: elasticsearch
description: Queries and indexes data in Elasticsearch for search and log analysis. Use when performing full-text search or complex aggregations on large logs. Do NOT use for relational data modeling (use postgresql) or for simple tabular storage (use s3).
---
# Elasticsearch

## Quick Start

```bash
pip install elasticsearch
```

```python
from elasticsearch import Elasticsearch
import pandas as pd

# Connect
es = Elasticsearch('http://localhost:9200')
# or with auth:
es = Elasticsearch(
    'https://my-cluster.es.io:9243',
    api_key='my_api_key',
)
es = Elasticsearch('http://localhost:9200',
                   basic_auth=('user', 'password'))

# Verify connection
es.info()

# Simple search
resp = es.search(index='my-index', query={'match_all': {}}, size=10)
hits = resp['hits']['hits']
df = pd.DataFrame([h['_source'] for h in hits])
```

## Query DSL

### match — full-text search

```python
es.search(index='logs', query={
    'match': {'message': 'error connection timeout'}
})

# Match phrase (exact phrase order)
es.search(index='logs', query={
    'match_phrase': {'message': 'connection timed out'}
})
```

### term / terms — exact value (keyword fields)

```python
# Single value (use for keyword, numeric, boolean — NOT analyzed text)
es.search(index='logs', query={
    'term': {'status': 'ERROR'}
})

# Multiple values (like SQL IN)
es.search(index='logs', query={
    'terms': {'status': ['ERROR', 'WARN']}
})
```

### range

```python
es.search(index='logs', query={
    'range': {
        'timestamp': {
            'gte': '2024-01-01T00:00:00',
            'lt':  '2024-02-01T00:00:00',
        }
    }
})

# Numeric range
es.search(index='metrics', query={
    'range': {'value': {'gte': 0, 'lte': 100}}
})
```

### bool — combine queries

```python
es.search(index='logs', query={
    'bool': {
        'must':     [{'match': {'message': 'error'}}],      # AND, affects score
        'filter':   [{'term': {'level': 'ERROR'}},           # AND, no score
                     {'range': {'timestamp': {'gte': 'now-1d/d'}}}],
        'should':   [{'match': {'message': 'timeout'}}],    # OR (boosts score)
        'must_not': [{'term': {'environment': 'dev'}}],     # NOT
    }
})
```

### Selecting fields and sorting

```python
es.search(
    index='logs',
    query={'match': {'message': 'error'}},
    source=['timestamp', 'level', 'message', 'host'],  # select fields
    sort=[{'timestamp': {'order': 'desc'}}],
    size=100,
)
```

## Aggregations

```python
resp = es.search(
    index='logs',
    query={'range': {'timestamp': {'gte': 'now-7d/d'}}},
    size=0,   # don't return hits, only aggs
    aggs={
        # Terms (group by)
        'by_level': {
            'terms': {'field': 'level', 'size': 10}
        },
        # Date histogram
        'per_hour': {
            'date_histogram': {
                'field': 'timestamp',
                'calendar_interval': 'hour',
            },
            'aggs': {
                'avg_duration': {'avg': {'field': 'duration_ms'}}
            }
        },
        # Stats
        'duration_stats': {
            'extended_stats': {'field': 'duration_ms'}
        },
        # Percentiles
        'p95_duration': {
            'percentiles': {'field': 'duration_ms', 'percents': [50, 95, 99]}
        },
    }
)

# Extract aggregation results into pandas
buckets = resp['aggregations']['by_level']['buckets']
df_levels = pd.DataFrame(buckets)[['key', 'doc_count']].rename(
    columns={'key': 'level', 'doc_count': 'count'}
)
```

## Extracting Large Result Sets

### scroll API (for older ES / full index dumps)

```python
from elasticsearch.helpers import scan

# scan() handles scroll internally — yields one hit at a time
hits = scan(
    es,
    index='my-index',
    query={'query': {'range': {'timestamp': {'gte': '2024-01-01'}}}},
    source=['timestamp', 'value', 'host'],
    size=1000,     # page size
)

records = [h['_source'] for h in hits]
df = pd.DataFrame(records)
```

### search_after (preferred for recent ES)

```python
def search_after_all(es, index, query, sort_field='timestamp', page_size=1000):
    records = []
    search_after = None

    while True:
        body = {
            'query': query,
            'sort': [{sort_field: 'asc'}, {'_id': 'asc'}],  # tiebreaker
            'size': page_size,
        }
        if search_after:
            body['search_after'] = search_after

        resp = es.search(index=index, **body)
        hits = resp['hits']['hits']
        if not hits:
            break

        records.extend(h['_source'] for h in hits)
        search_after = hits[-1]['sort']

    return pd.DataFrame(records)
```

## Bulk Indexing

```python
from elasticsearch.helpers import bulk, parallel_bulk

# bulk() — index list of documents
docs = [
    {'_index': 'my-index', '_id': str(i), '_source': {'val': i, 'ts': '2024-01-01'}}
    for i in range(10_000)
]
success, errors = bulk(es, docs, chunk_size=500, raise_on_error=False)
print(f'Indexed {success}, errors: {len(errors)}')

# From DataFrame
def df_to_es(df: pd.DataFrame, index: str, id_col: str = None):
    for _, row in df.iterrows():
        doc = {'_index': index, '_source': row.to_dict()}
        if id_col:
            doc['_id'] = str(row[id_col])
        yield doc

bulk(es, df_to_es(df, 'my-index', id_col='id'))

# parallel_bulk for high throughput
for ok, info in parallel_bulk(es, docs, thread_count=4, chunk_size=500):
    if not ok:
        print(info)
```

## Index Management

```python
# Create index with mappings
es.indices.create(index='my-index', body={
    'settings': {'number_of_shards': 1, 'number_of_replicas': 0},
    'mappings': {
        'properties': {
            'timestamp': {'type': 'date'},
            'level':     {'type': 'keyword'},
            'message':   {'type': 'text'},
            'duration_ms': {'type': 'float'},
            'host':      {'type': 'keyword'},
        }
    }
})

# Check if index exists
es.indices.exists(index='my-index')

# Delete
es.indices.delete(index='my-index', ignore_unavailable=True)

# Refresh (make recently indexed docs searchable immediately)
es.indices.refresh(index='my-index')

# Get mapping
es.indices.get_mapping(index='my-index')

# Get index stats
es.indices.stats(index='my-index')
```

## Log Analysis Patterns

```python
# Count errors per host in last 24h
resp = es.search(index='logs-*', size=0, query={
    'bool': {
        'filter': [
            {'term': {'level': 'ERROR'}},
            {'range': {'@timestamp': {'gte': 'now-24h'}}},
        ]
    }
}, aggs={
    'errors_by_host': {
        'terms': {'field': 'host.keyword', 'size': 20}
    }
})

df = pd.DataFrame(
    resp['aggregations']['errors_by_host']['buckets']
)[['key', 'doc_count']].rename(columns={'key': 'host', 'doc_count': 'error_count'})

# Time series of error rate
resp = es.search(index='logs-*', size=0, aggs={
    'per_minute': {
        'date_histogram': {'field': '@timestamp', 'fixed_interval': '1m'},
        'aggs': {
            'errors': {'filter': {'term': {'level': 'ERROR'}}},
        }
    }
})

rows = []
for b in resp['aggregations']['per_minute']['buckets']:
    rows.append({
        'time':   pd.to_datetime(b['key_as_string']),
        'total':  b['doc_count'],
        'errors': b['errors']['doc_count'],
    })
df = pd.DataFrame(rows)
df['error_rate'] = df['errors'] / df['total'].replace(0, float('nan'))
```
