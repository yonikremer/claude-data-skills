# Elasticsearch API Reference (Python Client)

This document provides a reference for core functions and classes used for interacting with Elasticsearch via the Python
client.

## Core Client

### `elasticsearch.Elasticsearch(hosts=None, **kwargs)`

Initialize the Elasticsearch client.

- **hosts**: List of hosts to connect to. Can be a string or a list of dictionaries.
- **api_key**: Optional API key for authentication (e.g., `(id, api_key)` or just `api_key`).
- **basic_auth**: Optional tuple of `(username, password)`.
- **verify_certs**: Whether to verify SSL certificates (default: True).

---

## Helpers

### `elasticsearch.helpers.bulk(client, actions, stats_only=False, **kwargs)`

Helper for the `bulk` API that provides a more user-friendly interface for indexing, updating, or deleting multiple
documents.

- **client**: The `Elasticsearch` client instance.
- **actions**: An iterable of action dictionaries. Each action must contain `_index` and can contain `_id`, `_source`,
  `_op_type` (default is `index`), etc.
- **stats_only**: If `True`, only return counts of successful and failed actions.

---

### `elasticsearch.helpers.scan(client, query=None, index=None, **kwargs)`

Simple abstraction on top of the scroll API - a generator that yields all hits matching the query. This is the preferred
way to retrieve large numbers of documents.

- **client**: The `Elasticsearch` client instance.
- **query**: The query to execute (DSL).
- **index**: The index to scan.
