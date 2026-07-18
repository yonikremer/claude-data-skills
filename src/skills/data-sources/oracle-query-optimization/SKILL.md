---
name: oracle-query-optimization
description: Use when analyzing, tuning, or optimizing slow Oracle SQL queries, reading EXPLAIN PLAN, or gathering statistics.
---

# Oracle SQL Query Optimization

## Overview
This skill outlines standard guidelines for evaluating and tuning query performance inside Oracle Database environments. It focuses on the Cost-Based Optimizer (CBO), plan evaluation, and structural indexing strategies.

## Pre-flight Checks
Before diagnostic runs:
1. **Verify Optimizer Stats**: Make sure statistics are fresh. Oracle's CBO relies entirely on table statistics.
   ```sql
   -- Check stats age
   SELECT table_name, last_analyzed, num_rows FROM user_tables;
   ```
2. **Re-gather Stats if Stale**:
   ```sql
   EXEC DBMS_STATS.GATHER_TABLE_STATS('SCHEMA_NAME', 'TABLE_NAME');
   ```

## Core Workflow: The `EXPLAIN PLAN` Protocol

Generate and view execution plans to pinpoint bottlenecks without actually executing long-running queries:

```sql
-- 1. Generate execution plan
EXPLAIN PLAN FOR
SELECT * FROM employees WHERE department_id = 10;

-- 2. Fetch formatted output
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY());
```

### Analyzing Plan Output
- **Operation / Options**: Look for `TABLE ACCESS FULL`. Ensure full scans are intended and not due to missing indexes.
- **Cost**: Relative estimator. Compare the cost between query variants (lower cost is usually preferred, but must be verified against actual time).
- **Cardinality (Rows)**: Estimated row outputs. Stale statistics cause discrepancies between estimated and actual row counts, resulting in incorrect join algorithms (e.g. Hash Join vs Nested Loops).
- **Cartesian Join**: If `MERGE JOIN CARTESIAN` appears, check for missing join predicates immediately.

## Optimization Techniques

### 1. Indexing Strategies
* **B-Tree Indexes**: Standard for high-cardinality columns.
* **Bitmap Indexes**: Ideal for low-cardinality columns (e.g., `status`, `gender`) in read-heavy/data-warehouse tables. *Never use on high-concurrency OLTP tables due to row-locking behavior.*
* **Function-Based Indexes**: Use if querying with expressions:
  ```sql
  CREATE INDEX idx_emp_upper_name ON employees(UPPER(last_name));
  ```
* **Composite Indexes**: Oracle can execute an `INDEX SKIP SCAN` if the leading column of a composite index is omitted in the query, but it is always faster to place the most selective filter columns first.

### 2. Best Coding Practices
* **Use Bind Variables**: Prevents hard parsing in the Shared Pool.
  - *Bad*: `SELECT * FROM sales WHERE id = 1052;` (forces compilation every time the ID changes)
  - *Good*: `SELECT * FROM sales WHERE id = :bind_id;`
* **Minimize Cartesian Joins**: Double check table join predicates.
* **Avoid Implicit Type Conversions**: If `char_col` is a `VARCHAR2`, querying `char_col = 123` forces Oracle to apply `TO_NUMBER(char_col) = 123`, disabling any index on `char_col`.

### 3. Oracle SQL Tuning Tools
For advanced assistance, request permissions to run built-in helpers:
- **SQL Tuning Advisor**: Analyzes SQL profile, indices, and stats:
  ```sql
  DECLARE
    l_sql_tune_task_id VARCHAR2(100);
  BEGIN
    l_sql_tune_task_id := DBMS_SQLTUNE.CREATE_TUNING_TASK(
                            sql_text => 'SELECT * FROM employees WHERE department_id = 10',
                            task_name => 'tune_employees_query');
    DBMS_SQLTUNE.EXECUTE_TUNING_TASK('tune_employees_query');
  END;
  /
  -- Get recommendations
  SELECT DBMS_SQLTUNE.REPORT_TUNING_TASK('tune_employees_query') FROM DUAL;
  ```

---

## Wall of Shame (Pitfalls to Avoid)

| Anti-Pattern | Bad Example | Good Example | Why |
|---|---|---|---|
| Blind Hinting | `SELECT /*+ INDEX(e idx_emp) */ * FROM employees e;` | Let CBO decide unless stats are perfect and choice is proven | Hints force paths and can break when statistics or data structures change |
| Implicit Conversion | `WHERE string_zip = 90210` | `WHERE string_zip = '90210'` | Disables indexes by wrapping column in `TO_NUMBER()` |
| OLTP Bitmap Index | Bitmap index on `status` in OLTP tables | B-Tree index or no index | Bitmap indexes lock entire index blocks on write, serializing transactions |
| NOT IN with NULL | `WHERE dept_id NOT IN (SELECT parent_id FROM dept)` | `WHERE NOT EXISTS (SELECT 1 FROM dept WHERE parent_id = e.dept_id)` | If a single `parent_id` is `NULL`, `NOT IN` returns zero rows |
