---
name: query-optimization
description: Use when writing SQL queries for large datasets, troubleshooting slow execution times, or designing high-performance database schemas. Ideal for indexing strategies, join optimization, and execution plan analysis. CRITICAL: Always use `EXPLAIN` or `EXPLAIN ANALYZE` to identify bottlenecks before making changes.
---

# SQL Query Optimization (Best Practices)

## ⚠️ Mandatory Pre-flight: Resource Check

Large queries can lock tables or consume all available database memory/CPU.

1. **Production Safety**: Never run `EXPLAIN ANALYZE` on a potentially massive query in a production environment without a `LIMIT`. `EXPLAIN ANALYZE` actually executes the query.
2. **Locking**: Be aware that some optimization operations (like creating an index) can lock the table for writes.

## Common Pitfalls (The "Wall of Shame")

1. **Index Suppression**: Using a function on a column in the `WHERE` clause (e.g., `WHERE DATE(created_at) = '2023-01-01'`) prevents the database from using an index on `created_at`.
2. **N+1 Problem**: Executing many small queries instead of one large join or bulk fetch.
3. **Implicit Type Conversion**: Comparing a string column to a number (`WHERE string_col = 123`) can cause the database to ignore the index.

## Overview

This skill provides essential techniques for writing efficient, high-performance SQL queries.

## 1. Indexing Strategies
Indices are the most powerful tool for query optimization. Use them wisely:
- **Single-Column Index**: Create on frequently filtered columns (`WHERE`) and columns used for `JOIN`s.
- **Composite Index**: Create on multiple columns used together in `WHERE` clauses (e.g., `(user_id, status)`). The order of columns matters!
- **Covering Index**: An index that includes all columns needed for a query, allowing the database to satisfy the query from the index alone.

## 2. Join Optimization
JOINs can be expensive. Follow these rules to keep them fast:
- **JOIN on Indexed Columns**: Always JOIN on columns with an index (usually primary and foreign keys).
- **Start with the Smallest Table**: In most databases, the query optimizer handles this, but it's good practice to filter the smaller table first in complex queries.
- **Avoid Cross Joins**: Unless explicitly needed, `CROSS JOIN` (or `FROM table1, table2`) can lead to Cartesian products and massive result sets.

## 3. Query Writing Best Practices
- **SELECT only what's needed**: Avoid `SELECT *`. Explicitly list columns to reduce data transfer and allow for covering indices.
- **Use CTEs for Clarity**: While they may not always improve performance (some DBs materialize them), CTEs make complex logic much easier to optimize and maintain.
- **Limit Result Sets**: Use `LIMIT` or `FETCH FIRST` to restrict the number of rows returned, especially during testing.
- **Avoid Functions on Filtered Columns**: `WHERE YEAR(order_date) = 2023` prevents the use of an index on `order_date`. Instead, use `WHERE order_date >= '2023-01-01' AND order_date < '2024-01-01'`.

## 4. Analytical Optimization
- **Window Functions vs. Subqueries**: Window functions are often faster than correlated subqueries for tasks like ranking and running totals.
- **Pre-Aggregating Data**: For very large datasets, consider pre-aggregating data into summary tables or materialized views.

## 5. Execution Plan Analysis
Always use `EXPLAIN` or `EXPLAIN ANALYZE` (depending on the DB) to understand how a query is being executed:
- **Scan Types**: Look for `Sequential Scan` (slow for large tables) vs. `Index Scan` (fast).
- **Cost Estimates**: Pay attention to the relative costs of different parts of the query plan.
- **Bottlenecks**: Identify which `JOIN`s or `GROUP BY` operations are taking the most time.
