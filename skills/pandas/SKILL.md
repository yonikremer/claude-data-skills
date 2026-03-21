---
name: pandas
description: Analyzes and transforms tabular data using DataFrames. Use for data cleaning, merging, and time-series analysis of datasets that fit in memory. Do NOT use for larger-than-memory datasets (use dask) or for extreme performance (use polars).
---
# pandas

## Overview

pandas is the standard Python library for working with structured (tabular) data. It provides two core data structures — `DataFrame` (2D table) and `Series` (1D column) — with rich support for data cleaning, transformation, grouping, joining, time series, and I/O across many formats.

**When to use pandas vs alternatives:**
- `pandas` — default choice for datasets that fit in RAM (up to a few GB)
- `polars` — drop-in faster alternative when pandas is too slow
- `dask` — when data exceeds available RAM

## Quick Start

```python
import pandas as pd
import numpy as np

# Create DataFrame
df = pd.DataFrame({
    'timestamp': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
    'value':     [1.1, 2.2, 3.3],
    'category':  ['a', 'b', 'a'],
})

# Basic inspection
df.shape          # (3, 3)
df.dtypes
df.describe()
df.head()

# Select columns
df['value']                  # Series
df[['timestamp', 'value']]   # DataFrame

# Filter rows
df[df['value'] > 2]
df.query('value > 2 and category == "a"')

# Add column
df['value_x2'] = df['value'] * 2
df = df.assign(value_x2=df['value'] * 2)   # non-mutating form
```

## Selection and Indexing

```python
# Label-based: .loc[row_label, col_label]
df.loc[0, 'value']
df.loc[0:2, ['value', 'category']]
df.loc[df['value'] > 2, 'category']

# Position-based: .iloc[row_int, col_int]
df.iloc[0]           # first row as Series
df.iloc[0, 1]        # row 0, col 1
df.iloc[:3, 1:]      # first 3 rows, cols from index 1 onward

# Boolean indexing
mask = (df['value'] > 1) & (df['category'] == 'a')
df[mask]

# .at / .iat — fast scalar access
df.at[0, 'value']
df.iat[0, 1]
```

## Data Cleaning

```python
# Missing values
df.isnull().sum()
df.dropna()
df.dropna(subset=['value'])
df.fillna(0)
df.fillna({'value': 0, 'category': 'unknown'})
df['value'].fillna(df['value'].median())

# Duplicates
df.duplicated()
df.drop_duplicates()
df.drop_duplicates(subset=['category'], keep='first')

# Type casting
df['value'] = df['value'].astype('float32')
df['category'] = df['category'].astype('category')   # memory-efficient
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Rename / drop columns
df.rename(columns={'value': 'val', 'category': 'cat'})
df.drop(columns=['value_x2'])

# String operations
df['category'].str.upper()
df['category'].str.startswith('a')
df['category'].str.contains(r'^[ab]', regex=True)
df['category'].str.replace('a', 'A')
```

## GroupBy and Aggregations

```python
# Basic groupby
df.groupby('category')['value'].mean()
df.groupby('category').agg({'value': ['mean', 'std', 'count']})

# Multiple group keys
df.groupby(['category', 'flag'])['value'].sum()

# Named aggregations (clean output column names)
df.groupby('category').agg(
    avg_val=('value', 'mean'),
    max_val=('value', 'max'),
    n=('value', 'count'),
)

# Transform — broadcast aggregation back to original index
df['group_mean'] = df.groupby('category')['value'].transform('mean')
df['rank_in_group'] = df.groupby('category')['value'].rank()

# Filter groups
df.groupby('category').filter(lambda g: g['value'].mean() > 2)

# Apply custom function
df.groupby('category').apply(lambda g: g.nlargest(2, 'value'))
```

## Merge and Join

```python
# Inner / left / right / outer join
pd.merge(df1, df2, on='id')
pd.merge(df1, df2, on='id', how='left')
pd.merge(df1, df2, left_on='user_id', right_on='id', how='left')

# Merge on index
pd.merge(df1, df2, left_index=True, right_index=True)
df1.join(df2, how='left')    # alias for index-based merge

# Stack rows
pd.concat([df1, df2], ignore_index=True)
pd.concat([df1, df2], axis=1)   # side by side

# Update values from another DataFrame
df1.update(df2)              # in-place, NaN in df2 = keep df1 value
df1.combine_first(df2)       # fill NaN in df1 with df2 values
```

## Reshape

```python
# Pivot table
df.pivot_table(values='value', index='date', columns='category', aggfunc='mean')

# Pivot (no aggregation — must be unique)
df.pivot(index='date', columns='category', values='value')

# Melt (wide → long)
pd.melt(df, id_vars=['date'], value_vars=['cat_a', 'cat_b'],
        var_name='category', value_name='value')

# Stack / unstack (MultiIndex ↔ columns)
df.stack()      # columns → inner index level
df.unstack()    # inner index level → columns

# Explode list column
df['tags'].explode()
```

## Time Series

```python
# Parse and set datetime index
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.set_index('timestamp').sort_index()

# Resample (aggregate by time bucket)
df.resample('1h').mean()
df.resample('D').agg({'value': 'sum', 'count': 'last'})

# Rolling window
df['rolling_mean'] = df['value'].rolling(window=10).mean()
df['rolling_std']  = df['value'].rolling(window=10).std()
df['ewm']          = df['value'].ewm(span=10).mean()

# Shift / lag / lead
df['prev_value'] = df['value'].shift(1)
df['next_value'] = df['value'].shift(-1)
df['diff']       = df['value'].diff()
df['pct_change'] = df['value'].pct_change()

# Date component extraction
df['hour']    = df.index.hour
df['weekday'] = df.index.day_name()
df['month']   = df.index.month

# Select time ranges
df['2024-01']                          # January 2024
df['2024-01-01':'2024-03-31']          # date slice
df.between_time('09:00', '17:00')      # time-of-day filter
df.first('7D')                         # first 7 days
```

## I/O

```python
# CSV
df = pd.read_csv('data.csv')
df = pd.read_csv('data.csv', parse_dates=['timestamp'], index_col='timestamp')
df.to_csv('out.csv', index=False)

# JSON
df = pd.read_json('data.json')
df = pd.read_json('data.json', lines=True)   # newline-delimited JSON (logs)
df.to_json('out.json', orient='records', lines=True)

# Parquet (recommended for persistent storage)
df = pd.read_parquet('data.parquet')
df.to_parquet('out.parquet', index=False)

# SQL
import sqlalchemy
engine = sqlalchemy.create_engine('postgresql://user:pass@host/db')
df = pd.read_sql('SELECT * FROM table WHERE id > 100', engine)
df = pd.read_sql_table('my_table', engine)
df.to_sql('my_table', engine, if_exists='append', index=False)

# Excel
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
df.to_excel('out.xlsx', sheet_name='Results', index=False)

# S3 (requires s3fs: pip install s3fs)
df = pd.read_csv('s3://bucket/path/data.csv')
df = pd.read_parquet('s3://bucket/path/data.parquet')
df.to_parquet('s3://bucket/path/out.parquet')
```

## Performance Tips

```python
# Use categorical for low-cardinality string columns (10-100× less memory)
df['status'] = df['status'].astype('category')

# Downcast numeric types
df['int_col']   = pd.to_numeric(df['int_col'],   downcast='integer')
df['float_col'] = pd.to_numeric(df['float_col'], downcast='float')

# Check memory usage
df.memory_usage(deep=True).sum() / 1e6   # MB

# Avoid chained assignment (causes SettingWithCopyWarning)
# BAD:  df[df['x'] > 0]['y'] = 1
# GOOD: df.loc[df['x'] > 0, 'y'] = 1

# Use query() for readable boolean filtering (also slightly faster)
df.query('a > 1 and b == "foo"')

# Vectorize — avoid row-wise apply() when possible
df['result'] = np.where(df['value'] > 0, df['a'], df['b'])   # fast
df['result'] = df.apply(lambda r: r['a'] if r['value'] > 0 else r['b'], axis=1)  # slow

# Read only needed columns
df = pd.read_csv('big.csv', usecols=['id', 'timestamp', 'value'])
# Read in chunks
for chunk in pd.read_csv('big.csv', chunksize=100_000):
    process(chunk)
```

## References

- `references/indexing-selection.md` — loc/iloc, MultiIndex, advanced boolean indexing, index operations
- `references/operations.md` — groupby patterns, merge/join edge cases, window functions, apply vs vectorization
- `references/time-series.md` — datetime parsing, resampling, rolling, time zones, date offsets
- `references/io-guide.md` — CSV/JSON/Parquet/SQL/Excel/S3 options, chunked reading, type inference
