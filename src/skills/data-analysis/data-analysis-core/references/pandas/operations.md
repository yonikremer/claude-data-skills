# pandas Operations — Complete Reference

## GroupBy Patterns

### Aggregation functions

```python
# Single function
df.groupby('cat')['val'].sum()
df.groupby('cat')['val'].agg('sum')

# Multiple functions on one column
df.groupby('cat')['val'].agg(['mean', 'std', 'count'])

# Different functions per column
df.groupby('cat').agg({'val': 'mean', 'qty': 'sum'})

# Named aggregations — cleanest output
df.groupby('cat').agg(
    avg_val=('val',  'mean'),
    total   =('qty',  'sum'),
    n       =('val',  'count'),
    p95     =('val',  lambda x: x.quantile(0.95)),
)
```

### transform — broadcast result back to original shape

```python
# Add group statistics as new columns (keeps all rows)
df['group_mean']    = df.groupby('cat')['val'].transform('mean')
df['group_z_score'] = df.groupby('cat')['val'].transform(
    lambda x: (x - x.mean()) / x.std()
)
df['pct_of_group']  = df['val'] / df.groupby('cat')['val'].transform('sum')
```

### filter — drop entire groups

```python
# Keep groups where condition holds for the group
df.groupby('cat').filter(lambda g: g['val'].mean() > 10)
df.groupby('cat').filter(lambda g: len(g) >= 5)
```

### apply — arbitrary function per group

```python
# Returns a DataFrame per group, concat'd
def top_n(group, n=3):
    return group.nlargest(n, 'val')

df.groupby('cat').apply(top_n, n=2)

# Avoid apply when vectorized alternatives exist (it's slow)
# Instead of: df.groupby('cat').apply(lambda g: g['val'].sum())
# Use:        df.groupby('cat')['val'].sum()
```

### cumulative operations within groups

```python
df['cumsum']  = df.groupby('cat')['val'].cumsum()
df['cummax']  = df.groupby('cat')['val'].cummax()
df['rank']    = df.groupby('cat')['val'].rank(method='dense', ascending=False)
df['shifted'] = df.groupby('cat')['val'].shift(1)    # previous value in group
```

## Merge / Join

### Basic merges

```python
# Inner join (default)
pd.merge(left, right, on='key')

# Outer joins
pd.merge(left, right, on='key', how='left')    # keep all left rows
pd.merge(left, right, on='key', how='right')
pd.merge(left, right, on='key', how='outer')   # keep all rows

# Different key names
pd.merge(left, right, left_on='user_id', right_on='id')

# Multiple keys
pd.merge(left, right, on=['date', 'category'])

# Keep track of merge source
pd.merge(left, right, on='key', how='outer', indicator=True)
# adds '_merge' column: 'left_only', 'right_only', 'both'
```

### Suffix handling for duplicate column names

```python
pd.merge(left, right, on='id', suffixes=('_left', '_right'))
```

### Index-based joins

```python
df1.join(df2, how='left')                      # join on index
df1.join(df2, on='key')                        # df1 col → df2 index
pd.merge(df1, df2, left_index=True, right_index=True)
```

### Merge diagnostics

```python
# Check for unexpected many-to-many
pd.merge(left, right, on='key', validate='1:1')    # raises if not unique
pd.merge(left, right, on='key', validate='1:m')
pd.merge(left, right, on='key', validate='m:1')

# Find unmatched rows after left join
merged = pd.merge(left, right, on='key', how='left', indicator=True)
unmatched = merged[merged['_merge'] == 'left_only']
```

### concat

```python
pd.concat([df1, df2])                          # stack rows
pd.concat([df1, df2], ignore_index=True)       # reset index
pd.concat([df1, df2], axis=1)                  # add columns side-by-side
pd.concat([df1, df2], keys=['a', 'b'])         # creates MultiIndex
pd.concat([df1, df2], join='inner')            # only shared columns
```

## Window Functions

```python
# Rolling
df['roll_mean'] = df['val'].rolling(window=7).mean()
df['roll_std']  = df['val'].rolling(window=7).std()
df['roll_sum']  = df['val'].rolling(window=7, min_periods=1).sum()

# Expanding (cumulative from start)
df['exp_mean'] = df['val'].expanding().mean()

# Exponential weighted
df['ewm'] = df['val'].ewm(span=10).mean()
df['ewm'] = df['val'].ewm(halflife=5).mean()

# Rolling with groupby
df['group_roll'] = (
    df.groupby('cat')['val']
    .transform(lambda x: x.rolling(3).mean())
)
```

## apply, map, applymap

```python
# Series.map — element-wise, best for substitution
df['status'].map({'active': 1, 'inactive': 0})
df['val'].map(lambda x: x ** 2)

# Series.apply — element-wise function (same as map for callables)
df['val'].apply(np.sqrt)

# DataFrame.apply — applies along axis
df.apply(lambda col: col.max() - col.min())        # column-wise (axis=0)
df.apply(lambda row: row['a'] + row['b'], axis=1)  # row-wise (axis=1, slow)

# DataFrame.map (pandas 2.1+) / applymap (older) — element-wise on all cells
df.map(lambda x: round(x, 2))

# Prefer vectorized over apply:
# Instead of: df.apply(lambda r: r['a'] * r['b'], axis=1)
# Use:        df['a'] * df['b']
```

## Sorting

```python
df.sort_values('val')
df.sort_values('val', ascending=False)
df.sort_values(['cat', 'val'], ascending=[True, False])
df.sort_values('val', na_position='first')    # NaNs first or last

df.nlargest(5, 'val')    # faster than sort + head
df.nsmallest(5, 'val')
```

## Vectorized Operations (avoid loops)

```python
# Conditional: np.where
df['label'] = np.where(df['val'] > 0, 'positive', 'negative')

# Multi-condition: np.select
conditions = [df['val'] > 100, df['val'] > 0, df['val'] <= 0]
choices    = ['high', 'low', 'negative']
df['label'] = np.select(conditions, choices, default='unknown')

# Pandas equivalent: pd.cut / pd.qcut for binning
df['bin']   = pd.cut(df['val'], bins=[0, 10, 50, 100], labels=['low', 'mid', 'high'])
df['qbin']  = pd.qcut(df['val'], q=4, labels=['Q1','Q2','Q3','Q4'])

# clip values
df['val'].clip(lower=0, upper=100)

# Arithmetic between DataFrames aligns on index and columns
result = df1[['a','b']] + df2[['a','b']]   # NaN where index/cols don't match
result = df1[['a','b']].add(df2[['a','b']], fill_value=0)  # treat missing as 0
```

## String Operations

```python
s = df['text']

s.str.lower() / s.str.upper() / s.str.title()
s.str.strip() / s.str.lstrip() / s.str.rstrip()
s.str.replace('old', 'new', regex=False)
s.str.replace(r'\s+', ' ', regex=True)

s.str.split(',')                     # Series of lists
s.str.split(',', expand=True)        # DataFrame of columns
s.str.split(',').str[0]              # first element

s.str.extract(r'(\d{4})-(\d{2})')   # regex groups → DataFrame columns
s.str.extractall(r'(\d+)')          # all matches, MultiIndex result
s.str.findall(r'\d+')               # list of all matches per row

s.str.len()
s.str.count(r'\d')
s.str.startswith('foo')
s.str.endswith('bar')
s.str.contains('baz', case=False, na=False)
s.str.cat(sep=', ')                  # join all values into one string
```

## Value Counts and Frequencies

```python
df['cat'].value_counts()
df['cat'].value_counts(normalize=True)   # as proportions
df['cat'].value_counts(dropna=False)     # include NaN

# Cross-tabulation
pd.crosstab(df['cat'], df['status'])
pd.crosstab(df['cat'], df['status'], normalize='index')  # row percentages

# Frequency table with cut
pd.cut(df['val'], bins=10).value_counts().sort_index()
```
