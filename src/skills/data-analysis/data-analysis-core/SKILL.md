---
name: data-analysis-pro
description: Use for ANY tabular data analysis, numerical computing, or large-scale data processing. Combines NumPy (arrays), Pandas (tabular), and Polars (high-performance/large-scale). CRITICAL: Run `get-available-resources` first to choose between Pandas (<100MB), Polars (100MB-1GB), or Polars-Lazy/Streaming (>1GB).
---
# Data Analysis Pro (Consolidated)

This skill provides a unified workflow for efficient data analysis using the Python ecosystem's "Big Three": NumPy, Pandas, and Polars.

## ⚠️ Mandatory Pre-flight: Resource Check

Always assess system memory before loading data to prevent OOM errors or system freezes.

1. **Run Detection**: Execute `python skills/get-available-resources/scripts/detect_resources.py`.
2. **Strategy Selection**:
   - **Small (< 100MB)**: Use **Pandas** for its rich API and ecosystem compatibility.
   - **Medium (100MB - 1GB)**: Use **Polars Eager** (`pl.read_csv`) for speed.
   - **Large (> 1GB or > 50% RAM)**: Use **Polars Lazy** (`pl.scan_csv`) with `.collect(streaming=True)`.
   - **Pure Numerical/Matrix**: Use **NumPy** directly for maximum performance.

---

## 1. NumPy: High-Performance Arrays

Use for vectorized math, linear algebra, and low-level buffer manipulation.

### Core Idioms
- **No Python Loops**: Always use vectorized ufuncs (`np.sin(arr)`) instead of loops.
- **Reproducibility**: Use `rng = np.random.default_rng(seed=42)` instead of legacy `np.random`.
- **Memory**: Use `float32` instead of `float64` to halve memory usage for large arrays.

```python
import numpy as np
rng = np.random.default_rng(42)

# Vectorized operations (FAST)
arr = rng.standard_normal((1000, 1000), dtype=np.float32)
result = np.exp(arr) * np.sin(arr)

# Broadcasting (aligning different shapes)
row_means = arr.mean(axis=1, keepdims=True)
normalized = arr - row_means
```

---

## 2. Pandas: The Tabular Standard

Use for cleaning, merging, and time-series analysis on datasets that fit comfortably in RAM.

### Core Idioms (v2.0+)
- **No `append`**: Use `pd.concat([df1, df2])`.
- **Copy-on-Write**: Use `.loc` for assignment to avoid `SettingWithCopyWarning`.
- **PyArrow Backend**: Use `pd.read_csv(..., engine='pyarrow')` for faster I/O.

```python
import pandas as pd

# Load and clean
df = pd.read_csv('data.csv', engine='pyarrow')
df.loc[df['value'].isna(), 'value'] = df['value'].median()

# GroupBy and Named Aggregation
summary = df.groupby('category').agg(
    avg_val=('value', 'mean'),
    count=('id', 'count')
)

# Time Series
df['ts'] = pd.to_datetime(df['ts'])
hourly = df.set_index('ts').resample('1h').mean()
```

---

## 3. Polars: The Performance Powerhouse

Use for large datasets, parallel processing, and performance-critical pipelines.

### Core Idioms
- **Lazy First**: Always prefer `pl.scan_csv()` over `pl.read_csv()`.
- **Expressions over Lambdas**: Use `pl.col("x").mean()` instead of `.map_elements(lambda x: ...)`.
- **Streaming**: Use `.collect(streaming=True)` for datasets larger than available RAM.

```python
import polars as pl

# Lazy query pipeline (Optimized automatically)
lf = pl.scan_csv("large_data.csv")
result = (
    lf.filter(pl.col("age") > 25)
    .with_columns(
        age_in_months=pl.col("age") * 12,
        avg_age_by_city=pl.col("age").mean().over("city")
    )
    .group_by("city")
    .agg(pl.all().mean())
    .collect(streaming=True)
)
```

---

## 🛠️ Common Pitfalls (The "Wall of Shame")

1. **Pandas Chained Indexing**: `df[df.a > 1]['b'] = 2` (Will fail/warn). Use `.loc`.
2. **Polars Missing `.collect()`**: Forgetting to call `.collect()` on a `LazyFrame` returns a query plan, not data.
3. **NumPy Array Appending**: `np.append` in a loop is $O(N^2)$. Pre-allocate with `np.zeros` and fill.
4. **Silent Import Errors**: NEVER catch `ImportError` silently. Let the agent see the missing dependency.

## References
- `skills/data-analysis/data-analysis-core/references/pandas/` — Deep dive into indexing, time-series, and I/O.
- `skills/data-analysis/data-analysis-core/references/polars/` — Lazy evaluation, expressions, and streaming guide.
- `skills/data-analysis/data-analysis-core/references/numpy/` — Linear algebra and structured arrays.
