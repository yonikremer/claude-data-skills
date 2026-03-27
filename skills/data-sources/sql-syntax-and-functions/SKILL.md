---
name: sql-syntax-and-functions
description: Use when writing complex SQL queries across PostgreSQL, MySQL, SQLite, and Oracle. Ideal for complex data transformations, DDL/DML operations, and advanced analytical queries.
---

# SQL Syntax and Functions (Core Guide)

This skill provides a detailed reference for writing clean, high-performance SQL. It focuses on modern standards (SQL:2016) while addressing common dialect variations.

## 1. Common Data Manipulation (DML)
- **Insert with Return**: `INSERT INTO users (name) VALUES ('Alice') RETURNING id;` (Postgres)
- **Upsert (Insert or Update)**:
  - Postgres: `INSERT INTO tbl (k, v) VALUES (1, 'a') ON CONFLICT (k) DO UPDATE SET v = 'a';`
  - MySQL: `INSERT INTO tbl (k, v) VALUES (1, 'a') ON DUPLICATE KEY UPDATE v = 'a';`
  - SQLite: `INSERT OR REPLACE INTO tbl (k, v) VALUES (1, 'a');`

## 2. Advanced Analytical Features
### CTEs (Common Table Expressions)
Always use CTEs for complex, multi-step logic instead of nested subqueries.
```sql
WITH regional_sales AS (
    SELECT region, SUM(amount) AS total_sales
    FROM sales
    GROUP BY region
)
SELECT region, total_sales
FROM regional_sales
WHERE total_sales > (SELECT AVG(total_sales) FROM regional_sales);
```

### Window Functions
Essential for ranking, running totals, and comparing values against a group.
```sql
SELECT
    user_id,
    order_date,
    amount,
    SUM(amount) OVER (PARTITION BY user_id ORDER BY order_date) AS running_total,
    RANK() OVER (PARTITION BY category_id ORDER BY amount DESC) AS rank_in_category
FROM orders;
```

## 3. String & Numeric Functions
- **Coalesce**: Use `COALESCE(col, default_val)` to handle NULLs consistently.
- **Substring**: `SUBSTRING('Data Science' FROM 1 FOR 4)` (Standard)
- **Case Logic**:
```sql
SELECT name,
       CASE WHEN age < 18 THEN 'Minor'
            WHEN age >= 65 THEN 'Senior'
            ELSE 'Adult' END AS category
FROM users;
```

## 4. Dialect Variations Reference
See [dialect-specific-functions.md](references/dialect-specific-functions.md) for a comprehensive list of how common tasks (date addition, pagination, null handling) differ between PostgreSQL, MySQL, SQLite, and Oracle.

## 5. Strict Idioms
- **Schema Qualification**: Always use schema names (e.g., `public.users`) if working in multi-schema environments.
- **Alias Clarity**: Always use `AS` for column aliases and meaningful table aliases (e.g., `s` for `sales`).
- **Data Types**: Be explicit about casting when comparing different types: `col::INTEGER` (Postgres) or `CAST(col AS INT)`.
