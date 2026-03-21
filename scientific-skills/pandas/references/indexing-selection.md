# pandas Indexing and Selection — Complete Reference

## The Index

The Index is a label array attached to rows (and columns). It enables fast label-based lookup and alignment during merge/concat.

```python
df.index           # row index
df.columns         # column index (also an Index)

df.set_index('id')              # promote column to index
df.reset_index()                # demote index to column
df.reset_index(drop=True)       # discard index, reset to 0..n

# Sort index (important for slicing and time series)
df.sort_index()
df.sort_index(ascending=False)
```

## .loc — Label-Based

```python
# Single row by label
df.loc[42]                         # row where index == 42

# Slice of labels (inclusive on both ends — unlike iloc)
df.loc[10:20]
df.loc['2024-01-01':'2024-03-31']  # works on datetime index

# Row + column
df.loc[42, 'value']
df.loc[10:20, ['value', 'status']]
df.loc[10:20, 'value':'status']    # column slice by name

# Boolean index
mask = df['value'] > 100
df.loc[mask]
df.loc[mask, 'status']

# Callable (avoids temp variable)
df.loc[lambda d: d['value'] > d['value'].median()]

# Assignment
df.loc[mask, 'status'] = 'high'
df.loc[df['id'] == 42, ['a', 'b']] = [1, 2]
```

## .iloc — Position-Based

```python
# Single row/cell
df.iloc[0]           # first row
df.iloc[-1]          # last row
df.iloc[0, 2]        # row 0, col 2

# Slices (exclusive end — like Python lists)
df.iloc[0:5]         # rows 0-4
df.iloc[:, 1:4]      # all rows, cols 1-3
df.iloc[0:5, 1:4]

# List of positions
df.iloc[[0, 2, 4]]
df.iloc[[0, 2], [1, 3]]

# Negative indexing
df.iloc[-5:]         # last 5 rows
df.iloc[:, -1]       # last column
```

## .at / .iat — Fast Scalar Access

```python
# Use when you need exactly one value
df.at[row_label, 'col_name']    # label-based, fast
df.iat[0, 2]                    # position-based, fast

# Assignment
df.at[row_label, 'col_name'] = 99
```

## Boolean Indexing

```python
# Combining conditions — use & | ~ with parentheses
df[(df['a'] > 1) & (df['b'] == 'foo')]
df[(df['a'] > 1) | (df['b'] == 'foo')]
df[~(df['a'] > 1)]

# isin — membership test
df[df['status'].isin(['active', 'pending'])]
df[~df['status'].isin(['deleted'])]

# between
df[df['value'].between(10, 20)]           # inclusive by default
df[df['value'].between(10, 20, inclusive='left')]

# String matching
df[df['name'].str.startswith('A')]
df[df['name'].str.contains('foo', case=False, na=False)]
df[df['name'].str.match(r'^\d{4}-')]

# Null checks
df[df['value'].notna()]
df[df['value'].isna()]
```

## query() Syntax

Cleaner for complex conditions. Uses column names as variables.

```python
df.query('value > 100')
df.query('value > 100 and status == "active"')
df.query('status in ["active", "pending"]')
df.query('a > b')                   # compare columns to each other
df.query('value > @threshold')      # reference Python variable with @
df.query('index > 100')             # filter on index
df.query('`col name with spaces` > 0')   # backtick-quote column names
```

## MultiIndex

```python
# Create
df = df.set_index(['date', 'category'])

# Access
df.loc[('2024-01-01', 'a')]
df.loc['2024-01-01']               # all rows for that date (cross-section)
df.loc[pd.IndexSlice['2024-01':'2024-03', 'a']]  # slice + filter

# xs — cross-section shorthand
df.xs('a', level='category')
df.xs(('2024-01-01', 'a'))

# Reset
df.reset_index()                   # both levels → columns
df.reset_index(level='category')   # only one level

# Stack / unstack
df.unstack('category')             # level → columns
df.stack()                         # innermost column level → row level

# Sort MultiIndex (required for slicing)
df.sort_index()
```

## Selecting Columns by Type or Pattern

```python
# By dtype
df.select_dtypes(include='number')
df.select_dtypes(include=['float64', 'int64'])
df.select_dtypes(exclude='object')

# By name pattern
df.filter(like='_id')              # columns containing '_id'
df.filter(regex=r'^val_\d+$')     # regex match
df.filter(items=['a', 'b', 'c'])   # exact list (silently skips missing)
```

## Index Alignment

pandas automatically aligns on index during arithmetic — a key difference from numpy:

```python
s1 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s2 = pd.Series([10, 20, 30], index=['b', 'c', 'd'])

s1 + s2
# a     NaN
# b    12.0
# c    23.0
# d     NaN

# Disable alignment (operate by position)
s1.values + s2.values   # numpy array, no alignment
```

## Common Index Operations

```python
df.index.unique()
df.index.nunique()
df.index.duplicated()
df.index.isin(['a', 'b'])

# Rename index
df.index.name = 'row_id'
df.rename_axis('row_id')
df.rename_axis(columns='metric')   # rename column axis

# Reindex — conform to a new index, filling missing with NaN
new_idx = pd.date_range('2024-01-01', periods=30, freq='D')
df.reindex(new_idx)
df.reindex(new_idx, method='ffill')   # forward-fill gaps
```
