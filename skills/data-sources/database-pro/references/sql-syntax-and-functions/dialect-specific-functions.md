# Dialect-Specific SQL Functions and Syntax Reference

This guide helps translate common SQL functions and operations between different database systems.

## 1. Null Handling
| Logic | PostgreSQL | MySQL | SQLite | Oracle | SQL Server |
|---|---|---|---|---|---|
| First non-null | `COALESCE(a, b)` | `COALESCE(a, b)` | `COALESCE(a, b)` | `NVL(a, b)` / `COALESCE` | `ISNULL(a, b)` / `COALESCE` |
| Null if equal | `NULLIF(a, b)` | `NULLIF(a, b)` | `NULLIF(a, b)` | `NULLIF(a, b)` | `NULLIF(a, b)` |

## 2. String Concatenation
- **Standard (Postgres/Oracle/SQLite)**: `'Hello ' || 'World'`
- **MySQL**: `CONCAT('Hello ', 'World')`
- **SQL Server**: `'Hello ' + 'World'`

## 3. Date and Time Functions
| Action | PostgreSQL | MySQL | SQLite | Oracle |
|---|---|---|---|---|
| Current Date | `CURRENT_DATE` | `CURDATE()` | `DATE('now')` | `SYSDATE` |
| Add 1 Day | `col + INTERVAL '1 day'` | `DATE_ADD(col, INTERVAL 1 DAY)` | `DATE(col, '+1 day')` | `col + 1` |
| Date Format | `TO_CHAR(col, 'YYYY-MM-DD')` | `DATE_FORMAT(col, '%Y-%m-%d')` | `STRFTIME('%Y-%m-%d', col)` | `TO_CHAR(col, 'YYYY-MM-DD')` |

## 4. Limit and Offset (Pagination)
- **Postgres/MySQL/SQLite**: `SELECT * FROM tbl LIMIT 10 OFFSET 20`
- **Oracle (12c+)/SQL Server (2012+)**: `SELECT * FROM tbl OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY`
- **Oracle (Old)**: `SELECT * FROM (SELECT a.*, ROWNUM r FROM tbl a) WHERE r > 20 AND r <= 30`

## 5. Metadata and Information Schema
- **List Tables**:
  - Postgres: `\dt` or `SELECT * FROM information_schema.tables`
  - MySQL: `SHOW TABLES`
  - SQLite: `SELECT name FROM sqlite_master WHERE type='table'`
  - Oracle: `SELECT table_name FROM user_tables`
