---
name: sql-queries
description: Generates and optimizes SQL across major dialects (Postgres, Snowflake, BigQuery, DuckDB). Use for writing complex joins, CTEs, and translating natural language to performant SQL.
---
# SQL Queries & Generation

## Workflow: Natural Language to SQL

1. **Understand Requirements**: Identify output columns, filters, aggregations, and joins.
2. **Determine Dialect**: Confirm if Postgres, Snowflake, BigQuery, Redshift, Databricks, or DuckDB.
3. **Discover Schema**: If a warehouse is connected, inspect tables and column relationships.
4. **Write Optimized SQL**: Use CTEs for readability, filter early, and avoid `SELECT *`.

## Dialect-Specific Quick Reference

### PostgreSQL / DuckDB
- **Date**: `DATE_TRUNC('month', created_at)`, `NOW() - INTERVAL '7 days'`
- **JSON**: `data->>'key'` (text), `data->'nested'` (json)
- **Regex**: `column ~ '^prefix'`

### BigQuery
- **Date**: `DATE_TRUNC(created_at, MONTH)`, `DATE_DIFF(d1, d2, DAY)`
- **Safety**: Use `SAFE_DIVIDE(a, b)` to avoid division by zero.
- **Arrays**: `UNNEST(array_column)` to flatten.

### Snowflake
- **Date**: `DATEADD(day, 7, col)`, `DATEDIFF(day, c1, c2)`
- **JSON**: `col:path.to.key::string`
- **Flatten**: `LATERAL FLATTEN(input => col)`

## Core SQL Patterns

### 1. Window Functions (The "Gold Standard")
```sql
-- Most recent record per user
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) as rn
  FROM events
) WHERE rn = 1;

-- 7-day Moving Average
AVG(revenue) OVER (ORDER BY date_col ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
```

### 2. Common Table Expressions (CTEs)
Always use CTEs for multi-step logic to ensure the code is debuggable.
```sql
WITH base AS (...),
     agg AS (SELECT id, SUM(val) FROM base GROUP BY 1)
SELECT * FROM agg;
```

## Performance & Optimization

- **Filter Pushdown**: Place `WHERE` clauses inside CTEs or as close to the base table as possible.
- **Join Logic**: Prefer `EXISTS` over `IN` for large subqueries. Ensure join keys have matching types.
- **Partitioning**: Always filter by the partition column (usually a date) in BigQuery/Snowflake.

## Error Handling
- **Ambiguity**: Always alias tables (`SELECT t1.id FROM table as t1`).
- **Nulls**: Use `COALESCE(col, 0)` or `NULLIF(col, 0)`.
