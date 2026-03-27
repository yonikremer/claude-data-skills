---
name: elasticsearch
description: Interact with Elasticsearch using both Python client and ES|QL (curl-based) for querying, indexing, data management, and cluster health checks.
---
# Elasticsearch (8.x) - Merged Capabilities

This skill combines the power of the Elasticsearch Python client for robust data operations with the flexibility of ES|QL via cURL for advanced querying and direct API interaction.

## Authentication and Setup

To connect to Elasticsearch, a URL and an API key are generally required. These are typically managed via environment variables:
`ELASTIC_URL` and `ELASTIC_API_KEY`.

## IMPORTANT

Always follow these rules:
- When using the Python client, ensure proper client initialization.
- When using cURL, never display the `ELASTIC_URL` and `ELASTIC_API_KEY` in your response.

## 1. Python Client API Usage (for Data Operations)

Use the Python client for high-performance indexing, efficient data extraction, and general data manipulation tasks.

### 1.1 Connection (Modern Client)
```python
from elasticsearch import Elasticsearch

# 8.x client uses basic_auth or api_key
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "password"),
    verify_certs=False # Only for local dev, ensure proper certificate verification in production
)
```

### 1.2 High-Performance Extraction (Search After)
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

### 1.3 Bulk Indexing (Gold Standard)
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

## 2. ES|QL (cURL-based) Usage (for Advanced Querying & Management)

Use direct cURL commands with ES|QL for powerful, piped queries, index management, and cluster health checks.

### 2.1 Available cURL APIs

The available APIs to interact with Elasticsearch via cURL are:

#### Health Check (not available if Elasticsearch is running on serverless)

```bash
curl -s "${ELASTIC_URL%/}/_cluster/health" -H "Authorization: ApiKey $(printenv ELASTIC_API_KEY)"
```

#### List indices

```bash
curl -s "${ELASTIC_URL%/}/_cat/indices/*,-.internal.*?format=json" -H "Authorization: ApiKey $(printenv ELASTIC_API_KEY)"
```

#### Get mapping of an index

```bash
curl -s "${ELASTIC_URL%/}/my-index/_mapping" -H "Authorization: ApiKey $(printenv ELASTIC_API_KEY)"
```

### 2.2 Search (using Elasticsearch Query Language, ES|QL)

When a user requests to search for data in Elasticsearch using ES|QL, follow this procedure:

1. **Determine the target index**
- Identify the appropriate Elasticsearch index based on the user’s request.
- If the index is not explicitly specified, use the List Indices API to retrieve available indices.
- Select the index that best matches the user’s query.

2. **Retrieve Index Mapping**
- Check whether the index mapping is already available.
- If not, use the Get Mappings API to retrieve the index mapping.
- Store the mapping information for use in query construction.

3. **Read the ES|QL reference** for syntax details:
   - [ES|QL Complete Reference](references/esql-reference.md)

4. **Generate the query** following ES|QL syntax:
   - Start with `FROM index-pattern`
   - Add `WHERE` for filtering
   - Use `EVAL` for computed fields
   - Use `STATS ... BY` for aggregations
   - Add `SORT` and `LIMIT` as needed

5. **Translate the user's request into ES|QL**
- Translate the user's request in an ES|QL query using the index mapping to translate the user’s request.
- Ensure the query aligns with the field types and structure defined in the mapping.

6. Execute the Query
- Execute the generated ES|QL query using the following API command (replace `insert-here-the-query` with the translated ES|QL query):
```bash
curl -s -X POST "${ELASTIC_URL%/}/_query" 
  -H "Authorization: ApiKey $(printenv ELASTIC_API_KEY)" 
  -H "Content-Type: application/json" 
  -d "$(jq -n --arg q "insert-here-the-query" '{query: $q}')"
```

## ES|QL Quick Reference

### Basic Structure

```
FROM index-pattern
| WHERE condition
| EVAL new_field = expression
| STATS aggregation BY grouping
| SORT field DESC
| LIMIT n
```

### Common Patterns

**Filter and limit:**

```esql
FROM logs-*
| WHERE @timestamp > NOW() - 24 hours AND level == "error"
| SORT @timestamp DESC
| LIMIT 100
```

**Aggregate by time:**

```esql
FROM metrics-*
| WHERE @timestamp > NOW() - 7 days
| STATS avg_cpu = AVG(cpu.percent) BY bucket = DATE_TRUNC(1 hour, @timestamp)
| SORT bucket DESC
```

**Top N with count:**

```esql
FROM web-logs
| STATS count = COUNT(*) BY response.status_code
| SORT count DESC
| LIMIT 10
```

**Text search (8.17+):**

```esql
FROM documents METADATA _score
| WHERE MATCH(content, "search terms")
| SORT _score DESC
| LIMIT 20
```

## 3. Common Pitfalls (Applies to both methods)
- **Keyword vs Text**: Use `.keyword` fields for exact matches and aggregations. Use `text` fields only for full-text search.
- **Refresh Interval**: For large bulk imports, set `index.refresh_interval: -1` to speed up ingestion, then reset to `1s` when done.
- **Mapping Explosion**: Avoid dynamic mapping for large objects; explicitly define schemas to prevent index bloating.

## Full Reference

For complete ES|QL syntax including all commands, functions, and operators, read:

- [ES|QL Complete Reference](references/esql-reference.md)
- [Query Patterns](references/query-patterns.md) - Natural language to ES|QL translation
- [Generation Tips](references/generation-tips.md) - Best practices for query generation

<h2>Error Handling</h2>

When query execution fails, the script returns:

- The generated ES|QL query
- The error message from Elasticsearch
- Suggestions for common issues

**Common issues:**

- Field doesn't exist → Check schema with the Get Mapping API
- Type mismatch → Use type conversion functions (TO_STRING, TO_INTEGER, etc.)
- Syntax error → Review ES|QL reference for correct syntax
- No results → Check time range and filter conditions
