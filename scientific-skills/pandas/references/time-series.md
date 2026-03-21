# pandas Time Series — Complete Reference

## Parsing and Creating Datetimes

```python
import pandas as pd

# Parse from strings
pd.to_datetime('2024-01-15')
pd.to_datetime(['2024-01-01', '2024-02-01'])
pd.to_datetime(df['col'])
pd.to_datetime(df['col'], format='%Y-%m-%d %H:%M:%S')  # explicit format (faster)
pd.to_datetime(df['col'], errors='coerce')              # invalid → NaT

# From Unix timestamps
pd.to_datetime(df['epoch'], unit='s')    # seconds
pd.to_datetime(df['epoch'], unit='ms')   # milliseconds
pd.to_datetime(df['epoch'], unit='us')   # microseconds

# Generate date ranges
pd.date_range('2024-01-01', periods=30, freq='D')
pd.date_range('2024-01-01', '2024-12-31', freq='ME')   # month end
pd.date_range('2024-01-01', periods=100, freq='h')     # hourly
pd.bdate_range('2024-01-01', periods=20)               # business days

# Timedelta
pd.to_timedelta('1 day')
pd.to_timedelta(df['duration_secs'], unit='s')
pd.Timedelta(hours=2, minutes=30)
```

## DatetimeIndex

```python
# Set datetime index
df = df.set_index('timestamp').sort_index()

# Index properties
df.index.year
df.index.month
df.index.day
df.index.hour
df.index.minute
df.index.dayofweek          # 0=Monday
df.index.day_name()
df.index.is_month_start
df.index.is_month_end
df.index.quarter
df.index.date               # numpy array of date objects
df.index.time               # numpy array of time objects
```

## Slicing Time Series

```python
# Partial string indexing — pandas infers the granularity
df['2024']                          # full year 2024
df['2024-03']                       # March 2024
df['2024-03-01':'2024-03-31']       # date range (inclusive)
df['2024-01-01 09:00':'2024-01-01 17:00']   # time range

# .truncate
df.truncate(before='2024-01-01', after='2024-06-30')

# Time-of-day filter
df.between_time('09:00', '17:00')
df.between_time('22:00', '06:00')   # overnight range (wraps midnight)

# First / last N periods
df.first('7D')     # first 7 days
df.last('1ME')     # last calendar month
```

## Resampling (Time-Based Aggregation)

```python
# Downsample: higher frequency → lower frequency
df.resample('D').mean()            # daily mean
df.resample('W').sum()             # weekly sum
df.resample('ME').last()           # month-end last value
df.resample('QE').agg({'open': 'first', 'close': 'last', 'volume': 'sum'})

# Upsample: lower → higher frequency (creates NaNs)
df.resample('h').asfreq()          # hourly, NaN for missing
df.resample('h').ffill()           # forward-fill
df.resample('h').interpolate()     # linear interpolation

# Common frequency aliases
# 'min' or 'T'  — minute
# 'h' or 'H'   — hour
# 'D'          — calendar day
# 'B'          — business day
# 'W'          — week (Sunday)
# 'ME'         — month end
# 'MS'         — month start
# 'QE'         — quarter end
# 'YE'         — year end
# '15min'      — 15 minutes
# '2h'         — 2 hours

# Resample with groupby
df.groupby('category').resample('D').mean()
# or
df.set_index('timestamp').groupby([pd.Grouper(freq='D'), 'category']).mean()
```

## Rolling and Expanding Windows

```python
# Rolling — fixed window
df['val'].rolling(window=7).mean()
df['val'].rolling(window=7, min_periods=1).mean()  # allow partial windows
df['val'].rolling(window=7, center=True).mean()    # center the window
df['val'].rolling(window='7D').mean()              # time-based window (requires DatetimeIndex)

# Rolling with custom function
df['val'].rolling(5).apply(lambda x: x[-1] / x[0] - 1, raw=True)  # 5-period return

# Expanding — cumulative from start
df['val'].expanding().mean()
df['val'].expanding(min_periods=10).std()

# Exponential weighted
df['val'].ewm(span=10).mean()
df['val'].ewm(halflife=5).mean()
df['val'].ewm(alpha=0.3).mean()     # smoothing factor directly
df['val'].ewm(com=9.5).std()        # center of mass

# Rolling correlation / covariance
df['a'].rolling(30).corr(df['b'])
df['a'].rolling(30).cov(df['b'])
```

## Shift, Lag, and Diff

```python
df['prev']       = df['val'].shift(1)        # previous row
df['next']       = df['val'].shift(-1)       # next row
df['lag_7']      = df['val'].shift(7)        # 7-period lag
df['diff_1']     = df['val'].diff()          # first difference
df['diff_7']     = df['val'].diff(7)         # 7-period difference
df['pct_chg']    = df['val'].pct_change()
df['pct_chg_7']  = df['val'].pct_change(7)

# Within-group shift
df['grp_prev'] = df.groupby('cat')['val'].shift(1)
```

## Time Zones

```python
# Localize naive datetime (attach tz without converting)
df.index = df.index.tz_localize('UTC')
df.index = df.index.tz_localize('America/New_York')

# Convert between time zones
df.index = df.index.tz_convert('Europe/London')
df.index = df.index.tz_convert('UTC')

# Remove time zone (convert to naive)
df.index = df.index.tz_localize(None)

# Parse strings with time zone
pd.to_datetime('2024-01-01T12:00:00+05:30')
pd.to_datetime(df['col'], utc=True)    # parse and normalize to UTC
```

## Date Offsets and Arithmetic

```python
from pandas.tseries.offsets import BDay, MonthEnd, MonthBegin, Hour

# Add offsets
df.index + pd.DateOffset(months=1)
df.index + BDay(5)       # 5 business days forward
df.index + MonthEnd(0)   # snap to end of current month

# Arithmetic between Timestamps / DatetimeIndex
(df.index[-1] - df.index[0]).days     # total days span
df.index.to_series().diff().dt.total_seconds()  # seconds between rows

# dt accessor on a Series
df['ts'].dt.year
df['ts'].dt.floor('h')       # truncate to hour
df['ts'].dt.ceil('D')        # ceil to day
df['ts'].dt.round('15min')   # round to 15-minute boundary
df['ts'].dt.normalize()      # set time to midnight
df['ts'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
```

## Handling Gaps and Irregular Series

```python
# Detect gaps
gaps = df.index.to_series().diff()
large_gaps = gaps[gaps > pd.Timedelta('1h')]

# Fill gaps by reindexing to a regular grid
full_idx = pd.date_range(df.index.min(), df.index.max(), freq='1min')
df = df.reindex(full_idx)
df = df.fillna(method='ffill')     # or bfill, or interpolate

# Interpolate over time
df['val'].interpolate(method='time')    # linear, time-aware
df['val'].interpolate(method='linear')
df['val'].interpolate(method='cubic', limit=5)  # max 5 consecutive NaNs filled
```
