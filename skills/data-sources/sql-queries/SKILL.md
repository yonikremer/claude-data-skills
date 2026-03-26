---
name: sql-queries
description: Generates and optimizes SQL across major dialects (Postgres, Snowflake, BigQuery, DuckDB). Use for writing complex joins, CTEs, and translating natural language to performant SQL.
---
# SQL Queries & Generation

This skill provides essential techniques for generating and executing high-quality SQL queries.

## 1. Parameterized Queries (Critical Safety)
Always use parameterized queries to prevent SQL injection and ensure data safety. Never use string formatting or f-strings to build queries.

### General Pattern
- **Placeholder**: A special character or name (e.g., `?`, `%s`, `:name`) that acts as a placeholder for a parameter.
- **Parameters**: A separate tuple or dictionary of values that will be safely substituted into the placeholders by the database driver.

### Quick Examples
- **SQLite (`sqlite3`)**: `cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))`
- **Postgres (`psycopg2`)**: `cur.execute("SELECT * FROM users WHERE email = %s", ("user@example.com",))`
- **SQLAlchemy**: `conn.execute(text("SELECT * FROM users WHERE email = :email"), {"email": "user@example.com"})`

See [python-db-drivers.md](references/python-db-drivers.md) for a comprehensive list of how to execute parameterized queries across various Python database drivers.

## 2. SQL Best Practices
- **Use CTEs for Clarity**: Always use Common Table Expressions (CTEs) for multi-step logic to ensure the code is readable and debuggable.
- **Filter Early**: Place `WHERE` clauses as close to the base table as possible to reduce the amount of data processed.
- **Avoid SELECT ***: Explicitly list the columns needed to reduce data transfer and allow for covering indices.
- **Alias Tables**: Always use table aliases (e.g., `SELECT u.id FROM users as u`) to avoid ambiguity.

## 3. Dialect-Specific Features
- **Postgres / DuckDB**: `DATE_TRUNC('month', created_at)`, `data->>'key'` (JSON).
- **BigQuery**: `DATE_TRUNC(created_at, MONTH)`, `SAFE_DIVIDE(a, b)` (avoid division by zero).
- **Snowflake**: `DATEADD(day, 7, col)`, `col:path.to.key::string` (JSON).

## 4. Query Optimization Reference
See the [query-optimization](../query-optimization/SKILL.md) skill for a comprehensive guide on indexing, join optimization, and execution plan analysis.
