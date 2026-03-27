# Python Database Drivers and Parameterized Queries

This guide provides high-quality examples of how to execute parameterized queries across various Python database drivers to prevent SQL injection and ensure data safety.

## 1. PostgreSQL (`psycopg2`)
Uses `%s` as the placeholder for parameters.
```python
import psycopg2

conn = psycopg2.connect("dbname=test user=postgres")
cur = conn.cursor()

# Parameterized Query
query = "SELECT * FROM users WHERE email = %s AND status = %s"
params = ("user@example.com", "active")
cur.execute(query, params)

results = cur.fetchall()
cur.close()
conn.close()
```

## 2. SQLite (`sqlite3`)
Uses `?` as the placeholder for parameters.
```python
import sqlite3

conn = sqlite3.connect("example.db")
cur = conn.cursor()

# Parameterized Query
query = "SELECT * FROM tasks WHERE category = ? AND priority >= ?"
params = ("work", 3)
cur.execute(query, params)

results = cur.fetchall()
conn.close()
```

## 3. Oracle (`cx_Oracle`)
Uses `:name` or `:1` as the placeholder for parameters.
```python
import cx_Oracle

conn = cx_Oracle.connect("user/pass@host:port/service_name")
cur = conn.cursor()

# Parameterized Query (Named Parameters)
query = "SELECT * FROM employees WHERE department_id = :dept_id AND salary > :min_salary"
params = {"dept_id": 101, "min_salary": 50000}
cur.execute(query, params)

results = cur.fetchall()
cur.close()
conn.close()
```

## 4. Microsoft SQL Server (`pyodbc`)
Uses `?` as the placeholder for parameters.
```python
import pyodbc

conn = pyodbc.connect("DRIVER={SQL Server};SERVER=server_name;DATABASE=db_name;UID=user;PWD=pass")
cur = conn.cursor()

# Parameterized Query
query = "SELECT * FROM sales WHERE region = ? AND order_date >= ?"
params = ("North", "2023-01-01")
cur.execute(query, params)

results = cur.fetchall()
cur.close()
conn.close()
```

## 5. MySQL (`mysql-connector-python`)
Uses `%s` as the placeholder for parameters.
```python
import mysql.connector

conn = mysql.connector.connect(user='scott', password='password', host='127.0.0.1', database='employees')
cur = conn.cursor()

# Parameterized Query
query = "SELECT * FROM employees WHERE hire_date BETWEEN %s AND %s"
params = ("2023-01-01", "2023-12-31")
cur.execute(query, params)

results = cur.fetchall()
cur.close()
conn.close()
```

## 6. SQLAlchemy (SQL Expression Language)
SQLAlchemy uses `:name` internally and handles translation for the underlying driver.
```python
from sqlalchemy import create_engine, text

engine = create_engine("postgresql://user:pass@host/dbname")

with engine.connect() as conn:
    # Use text() with named parameters
    query = text("SELECT * FROM users WHERE email = :email")
    params = {"email": "user@example.com"}
    result = conn.execute(query, params)
    
    for row in result:
        print(row)
```

## Summary of Placeholders
| Driver | Placeholder |
|---|---|
| `psycopg2` (Postgres) | `%s` |
| `sqlite3` (SQLite) | `?` |
| `cx_Oracle` (Oracle) | `:name` |
| `pyodbc` (SQL Server) | `?` |
| `mysql-connector` (MySQL) | `%s` |
| `sqlalchemy` | `:name` (with `text()`) |
