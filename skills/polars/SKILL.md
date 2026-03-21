---
name: polars
description: High-performance DataFrame library with a parallel Apache Arrow backend. Use for 1GB-100GB datasets where pandas is too slow. CRITICAL: Use `lazy` mode and `streaming` for datasets approaching RAM limits.
---
# Polars

## ⚠️ Mandatory Pre-flight: Resource Check

Polars is extremely fast but can easily consume all available CPU and RAM if not configured correctly.

1. **Run Detection**: Execute `python skills/get-available-resources/scripts/detect_resources.py`.
2. **Strategy Selection**:
   - **Data < 50% RAM**: Use **Eager mode** (`pl.read_csv`) for convenience.
   - **Data 50-90% RAM**: Use **Lazy mode** (`pl.scan_csv`) and `.collect()`.
   - **Data > RAM**: Use **Streaming mode** (`.collect(streaming=True)`).
3. **CPU Cores**: Polars uses all available cores by default. If the system is shared, limit threads via `POLARS_MAX_THREADS` environment variable.

## Strict Idioms & Performance Gold

- **Prefer `scan_*` over `read_*`**: Always start with a `LazyFrame` to allow the query optimizer to prune columns (projection pushdown) and rows (predicate pushdown).
- **Expressions, not Lambdas**: NEVER use `.map_elements(lambda x: ...)` if a native expression exists. It breaks parallelization and optimization.
- **Select Early**: Use `.select()` as the first step in a lazy chain to reduce the memory footprint of the intermediate buffers.

## Common Pitfalls (The "Wall of Shame")

1. **`to_pandas()` too early**: Converting a large Polars DataFrame to Pandas will often trigger an OOM as it duplicates the memory and loses Arrow optimization.
2. **Missing `collect()`**: In lazy mode, operations return a `LazyFrame` (a query plan), not data. You must call `.collect()` to get the results.
3. **Using `&` instead of `,` in filters**: While `df.filter((pl.col("a") > 1) & (pl.col("b") < 2))` works, `df.filter(pl.col("a") > 1, pl.col("b") < 2)` is more idiomatic and allows for better optimization.

## References (Load on demand)
- `references/core_concepts.md` — Expressions, contexts, and the query optimizer.
- `references/pandas_migration.md` — Direct syntax mapping for Pandas users.
- `references/io_guide.md` — Optimized reading for Parquet, CSV, and SQL.

## Quick Start

### Installation and Basic Usage

Install Polars:
```python
uv pip install polars
```

Basic DataFrame creation and operations:
```python
import polars as pl

# Create DataFrame
df = pl.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["NY", "LA", "SF"]
})

# Select columns
df.select("name", "age")

# Filter rows
df.filter(pl.col("age") > 25)

# Add computed columns
df.with_columns(
    age_plus_10=pl.col("age") + 10
)
```

## Core Concepts

### Expressions

Expressions are the fundamental building blocks of Polars operations. They describe transformations on data and can be composed, reused, and optimized.

**Key principles:**
- Use `pl.col("column_name")` to reference columns
- Chain methods to build complex transformations
- Expressions are lazy and only execute within contexts (select, with_columns, filter, group_by)

**Example:**
```python
# Expression-based computation
df.select(
    pl.col("name"),
    (pl.col("age") * 12).alias("age_in_months")
)
```

### Lazy vs Eager Evaluation

**Eager (DataFrame):** Operations execute immediately
```python
df = pl.read_csv("file.csv")  # Reads immediately
result = df.filter(pl.col("age") > 25)  # Executes immediately
```

**Lazy (LazyFrame):** Operations build a query plan, optimized before execution
```python
lf = pl.scan_csv("file.csv")  # Doesn't read yet
result = lf.filter(pl.col("age") > 25).select("name", "age")
df = result.collect()  # Now executes optimized query
```

**When to use lazy:**
- Working with large datasets
- Complex query pipelines
- When only some columns/rows are needed
- Performance is critical

**Benefits of lazy evaluation:**
- Automatic query optimization
- Predicate pushdown
- Projection pushdown
- Parallel execution

For detailed concepts, load `references/core_concepts.md`.

## Common Operations

### Select
Select and manipulate columns:
```python
# Select specific columns
df.select("name", "age")

# Select with expressions
df.select(
    pl.col("name"),
    (pl.col("age") * 2).alias("double_age")
)

# Select all columns matching a pattern
df.select(pl.col("^.*_id$"))
```

### Filter
Filter rows by conditions:
```python
# Single condition
df.filter(pl.col("age") > 25)

# Multiple conditions (cleaner than using &)
df.filter(
    pl.col("age") > 25,
    pl.col("city") == "NY"
)

# Complex conditions
df.filter(
    (pl.col("age") > 25) | (pl.col("city") == "LA")
)
```

### With Columns
Add or modify columns while preserving existing ones:
```python
# Add new columns
df.with_columns(
    age_plus_10=pl.col("age") + 10,
    name_upper=pl.col("name").str.to_uppercase()
)

# Parallel computation (all columns computed in parallel)
df.with_columns(
    pl.col("value") * 10,
    pl.col("value") * 100,
)
```

### Group By and Aggregations
Group data and compute aggregations:
```python
# Basic grouping
df.group_by("city").agg(
    pl.col("age").mean().alias("avg_age"),
    pl.len().alias("count")
)

# Multiple group keys
df.group_by("city", "department").agg(
    pl.col("salary").sum()
)

# Conditional aggregations
df.group_by("city").agg(
    (pl.col("age") > 30).sum().alias("over_30")
)
```

For detailed operation patterns, load `references/operations.md`.

## Aggregations and Window Functions

### Aggregation Functions
Common aggregations within `group_by` context:
- `pl.len()` - count rows
- `pl.col("x").sum()` - sum values
- `pl.col("x").mean()` - average
- `pl.col("x").min()` / `pl.col("x").max()` - extremes
- `pl.first()` / `pl.last()` - first/last values

### Window Functions with `over()`
Apply aggregations while preserving row count:
```python
# Add group statistics to each row
df.with_columns(
    avg_age_by_city=pl.col("age").mean().over("city"),
    rank_in_city=pl.col("salary").rank().over("city")
)

# Multiple grouping columns
df.with_columns(
    group_avg=pl.col("value").mean().over("category", "region")
)
```

**Mapping strategies:**
- `group_to_rows` (default): Preserves original row order
- `explode`: Faster but groups rows together
- `join`: Creates list columns

## Data I/O

### Supported Formats
Polars supports reading and writing:
- CSV, Parquet, JSON, Excel
- Databases (via connectors)
- Cloud storage (S3, Azure, GCS)
- Google BigQuery
- Multiple/partitioned files

### Common I/O Operations

**CSV:**
```python
# Eager
df = pl.read_csv("file.csv")
df.write_csv("output.csv")

# Lazy (preferred for large files)
lf = pl.scan_csv("file.csv")
result = lf.filter(...).select(...).collect()
```

**Parquet (recommended for performance):**
```python
df = pl.read_parquet("file.parquet")
df.write_parquet("output.parquet")
```

**JSON:**
```python
df = pl.read_json("file.json")
df.write_json("output.json")
```

For comprehensive I/O documentation, load `references/io_guide.md`.

## Transformations

### Joins
Combine DataFrames:
```python
# Inner join
df1.join(df2, on="id", how="inner")

# Left join
df1.join(df2, on="id", how="left")

# Join on different column names
df1.join(df2, left_on="user_id", right_on="id")
```

### Concatenation
Stack DataFrames:
```python
# Vertical (stack rows)
pl.concat([df1, df2], how="vertical")

# Horizontal (add columns)
pl.concat([df1, df2], how="horizontal")

# Diagonal (union with different schemas)
pl.concat([df1, df2], how="diagonal")
```

### Pivot and Unpivot
Reshape data:
```python
# Pivot (wide format)
df.pivot(values="sales", index="date", columns="product")

# Unpivot (long format)
df.unpivot(index="id", on=["col1", "col2"])
```

For detailed transformation examples, load `references/transformations.md`.

## Pandas Migration

Polars offers significant performance improvements over pandas with a cleaner API. Key differences:

### Conceptual Differences
- **No index**: Polars uses integer positions only
- **Strict typing**: No silent type conversions
- **Lazy evaluation**: Available via LazyFrame
- **Parallel by default**: Operations parallelized automatically

### Common Operation Mappings

| Operation | Pandas | Polars |
|-----------|--------|--------|
| Select column | `df["col"]` | `df.select("col")` |
| Filter | `df[df["col"] > 10]` | `df.filter(pl.col("col") > 10)` |
| Add column | `df.assign(x=...)` | `df.with_columns(x=...)` |
| Group by | `df.groupby("col").agg(...)` | `df.group_by("col").agg(...)` |
| Window | `df.groupby("col").transform(...)` | `df.with_columns(...).over("col")` |

### Key Syntax Patterns

**Pandas sequential (slow):**
```python
df.assign(
    col_a=lambda df_: df_.value * 10,
    col_b=lambda df_: df_.value * 100
)
```

**Polars parallel (fast):**
```python
df.with_columns(
    col_a=pl.col("value") * 10,
    col_b=pl.col("value") * 100,
)
```

For comprehensive migration guide, load `references/pandas_migration.md`.

## Best Practices

### Performance Optimization

1. **Use lazy evaluation for large datasets:**
   ```python
   lf = pl.scan_csv("large.csv")  # Don't use read_csv
   result = lf.filter(...).select(...).collect()
   ```

2. **Avoid Python functions in hot paths:**
   - Stay within expression API for parallelization
   - Use `.map_elements()` only when necessary
   - Prefer native Polars operations

3. **Use streaming for very large data:**
   ```python
   lf.collect(streaming=True)
   ```

4. **Select only needed columns early:**
   ```python
   # Good: Select columns early
   lf.select("col1", "col2").filter(...)

   # Bad: Filter on all columns first
   lf.filter(...).select("col1", "col2")
   ```

5. **Use appropriate data types:**
   - Categorical for low-cardinality strings
   - Appropriate integer sizes (i32 vs i64)
   - Date types for temporal data

### Expression Patterns

**Conditional operations:**
```python
pl.when(condition).then(value).otherwise(other_value)
```

**Column operations across multiple columns:**
```python
df.select(pl.col("^.*_value$") * 2)  # Regex pattern
```

**Null handling:**
```python
pl.col("x").fill_null(0)
pl.col("x").is_null()
pl.col("x").drop_nulls()
```

For additional best practices and patterns, load `references/best_practices.md`.

## Resources

This skill includes comprehensive reference documentation:

### references/
- `core_concepts.md` - Detailed explanations of expressions, lazy evaluation, and type system
- `operations.md` - Comprehensive guide to all common operations with examples
- `pandas_migration.md` - Complete migration guide from pandas to Polars
- `io_guide.md` - Data I/O operations for all supported formats
- `transformations.md` - Joins, concatenation, pivots, and reshaping operations
- `best_practices.md` - Performance optimization tips and common patterns

Load these references as needed when users require detailed information about specific topics.

