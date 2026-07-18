---
name: postgres-query-optimization
description: Use when analyzing or optimizing slow PostgreSQL queries, reading EXPLAIN plans, or configuring indexes.
---

# PostgreSQL Query Optimization

## Overview
This skill provides a structured workflow for diagnosing and resolving performance bottlenecks in PostgreSQL queries. It covers execution plan analysis, indexing strategies, and database-specific configuration optimizations.

## Pre-flight Checks
Before optimizing any query:
1. **Check Table Stats Availability**: Verify if statistics are up-to-date. If not, run:
   ```sql
   ANALYZE table_name;
   ```
2. **Estimate Data Volume**: Know the row count. Techniques that work on 10,000 rows may fail or degrade performance on 10,000,000 rows.
3. **Identify Environment**: Ensure test environment has a similar volume of data and schema representation to production.

## Core Workflow: The `EXPLAIN` Protocol

Always run execution plans using the recommended parameters to fetch memory and cache hits:
```sql
EXPLAIN (ANALYZE, BUFFERS, VERBOSE) <YOUR_QUERY>;
```
> [!WARNING]
> Running `EXPLAIN ANALYZE` executes the query. For mutating queries (`INSERT`, `UPDATE`, `DELETE`), wrap in a transaction and rollback:
> ```sql
> BEGIN;
> EXPLAIN (ANALYZE, BUFFERS, VERBOSE) UPDATE ...;
> ROLLBACK;
> ```

### Analyzing the Plan Output (Innermost Outward)
1. **Look for `Seq Scan`**: Check for sequential scans on tables with >10,000 rows. This indicates a missing index or that Postgres determined an index is slower due to high selectivity.
2. **Look for `Rows Removed by Filter`**: Indicates that many rows were read and discarded. An index on the filtered column(s) will bypass this overhead.
3. **Compare `Rows` vs `Actual Rows`**: If there is an order-of-magnitude difference, the query planner is using stale statistics. Run `ANALYZE`.
4. **Inspect `Shared Hit/Read` Buffers**:
   - `shared hit`: Read from OS/PostgreSQL cache.
   - `shared read`: Read from disk (slow). High reads indicate index misses or cold cache.

## Optimization Techniques

### 1. Indexing Strategies
* **B-Tree Indexes**: Default. Use for equality, range searches, and sorting.
* **Partial Indexes**: If querying a subset (e.g. `WHERE active = true`), index only that subset:
  ```sql
  CREATE INDEX idx_active_users ON users(id) WHERE active = true;
  ```
* **Covering Indexes (Index-Only Scan)**: Include frequently selected columns in the index to avoid table lookup:
  ```sql
  CREATE INDEX idx_users_email_include_name ON users(email) INCLUDE (display_name);
  ```
* **Composite Indexes**: Match leftmost prefix order. If querying `WHERE a = 1 AND b = 2`, create index on `(a, b)`.

### 2. Query Rewriting
* **Avoid Mismatched Data Types**: Mismatched types (e.g., comparing `varchar` column to `int` value) prevent the planner from using indexes.
* **Replace `IN` with `EXISTS`**: For subqueries, `EXISTS` is often faster than `IN` because it stops scanning once a match is found.
* **Avoid Functions in WHERE Clauses**: `WHERE LOWER(email) = 'abc@test.com'` bypasses a standard index on `email`. Use a functional index instead:
  ```sql
  CREATE INDEX idx_users_lower_email ON users(LOWER(email));
  ```

### 3. Session Configurations
For complex sorting or hash joins, temporarily increase work memory:
```sql
SET work_mem = '64MB';
-- Run query
RESET work_mem;
```

---

## Wall of Shame (Pitfalls to Avoid)

| Anti-Pattern | Bad Example | Good Example | Why |
|---|---|---|---|
| Mismatched Types | `WHERE user_id_str = 123` | `WHERE user_id_str = '123'` | Prevents index scan |
| Functions on Index | `WHERE DATE(created_at) = '2026-01-01'` | `WHERE created_at >= '2026-01-01 00:00:00' AND created_at < '2026-01-02 00:00:00'` | Keeps index usable |
| Over-indexing | Creating 20 indexes on a highly write-intensive table | Keep only high-read filters indexed | Drastically slows down `INSERT`/`UPDATE` |
| Deep Offset Pagination | `SELECT * FROM logs LIMIT 50 OFFSET 1000000;` | Use cursor/seek method: `WHERE id > last_seen_id LIMIT 50;` | Postgres must scan all offset rows first |
