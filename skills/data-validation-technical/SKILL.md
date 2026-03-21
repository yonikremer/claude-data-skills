---
name: data-validation-technical
description: Enforces data quality and schemas using pandera or pydantic. Use when ingesting external data or ensuring ETL pipeline integrity. Do NOT use for high-level QA methodology (use data-validation-methodology) or for format identification (use data-format-detection).
---
# Data Validation

## Overview

Pick the right tool for the job:

| Tool | Best For |
|------|----------|
| **pandera** | DataFrame schema validation (pandas/polars) |
| **pydantic** | JSON, API responses, config files, dataclasses |
| **great_expectations** | Pipeline-level data quality checks with reporting |
| **built-in assertions** | Quick one-off checks in scripts |

## Quick Checks (no library)

For simple scripts, assertions are fast and sufficient:

```python
import pandas as pd

df = pd.read_csv('data.csv')

# Shape
assert df.shape[0] > 0, "Empty DataFrame"
assert set(['id', 'timestamp', 'value']).issubset(df.columns), "Missing columns"

# Nulls
assert df['id'].notna().all(), "Null IDs found"
null_pct = df['value'].isna().mean()
assert null_pct < 0.05, f"Too many nulls in 'value': {null_pct:.1%}"

# Ranges
assert df['value'].between(0, 1000).all(), "Values out of expected range"
assert (df['timestamp'] >= '2020-01-01').all(), "Old timestamps found"

# Uniqueness
assert df['id'].nunique() == len(df), "Duplicate IDs"

# Referential
valid_statuses = {'active', 'inactive', 'pending'}
assert df['status'].isin(valid_statuses).all(), \
    f"Unknown statuses: {set(df['status']) - valid_statuses}"
```

## pandera — DataFrame Schema Validation

```bash
pip install pandera
```

### Schema-based validation

```python
import pandera as pa
import pandas as pd

schema = pa.DataFrameSchema({
    'id':        pa.Column(int,   nullable=False, unique=True),
    'timestamp': pa.Column('datetime64[ns]', nullable=False),
    'channel':   pa.Column(int,   pa.Check.isin([1, 2, 3, 4])),
    'value':     pa.Column(float, [
                     pa.Check.ge(0),          # >= 0
                     pa.Check.le(1000),        # <= 1000
                     pa.Check(lambda s: s.notna().mean() > 0.95,
                              error="Too many nulls in value"),
                 ]),
    'status':    pa.Column(str,   pa.Check.isin(['ok', 'error', 'pending'])),
    'optional':  pa.Column(str,   nullable=True, required=False),
},
    index=pa.Index(int),
    strict=False,   # allow extra columns
    coerce=True,    # try to cast columns to declared types
)

# Validate — raises SchemaError if invalid
validated_df = schema.validate(df)

# Validate with lazy=True — collect ALL errors instead of raising on first
try:
    schema.validate(df, lazy=True)
except pa.errors.SchemaErrors as e:
    print(e.failure_cases)   # DataFrame of all failures
```

### DataFrameModel (class-based, cleaner for complex schemas)

```python
from pandera.typing import Series, DateTime
import pandera as pa

class MeasurementSchema(pa.DataFrameModel):
    id:        Series[int]   = pa.Field(nullable=False, unique=True)
    timestamp: Series[DateTime]
    channel:   Series[int]   = pa.Field(isin=[1, 2, 3, 4])
    value:     Series[float] = pa.Field(ge=0, le=1000)
    status:    Series[str]   = pa.Field(isin=['ok', 'error'])

    class Config:
        strict = False
        coerce = True

    @pa.check('value')
    def value_not_mostly_null(cls, series: Series) -> bool:
        return series.notna().mean() > 0.95

# Use as type annotation with @pa.check_types
from pandera.typing import DataFrame

@pa.check_types
def process(df: DataFrame[MeasurementSchema]) -> DataFrame[MeasurementSchema]:
    df['value'] = df['value'].clip(0, 1000)
    return df
```

### Check types

```python
# Range checks
pa.Check.ge(0)               # >= 0
pa.Check.gt(0)               # > 0
pa.Check.le(100)             # <= 100
pa.Check.lt(100)             # < 100
pa.Check.between(0, 100)     # inclusive

# Set membership
pa.Check.isin(['a', 'b', 'c'])
pa.Check.notin(['x', 'y'])

# String checks
pa.Check.str_matches(r'^\d{4}-\d{2}$')
pa.Check.str_startswith('prefix_')
pa.Check.str_length(min_value=1, max_value=50)

# Custom
pa.Check(lambda s: (s % 2 == 0).all(), error="Must be even")
pa.Check(lambda s: s.is_monotonic_increasing, error="Must be sorted")

# Element-wise (check each value, not the whole series)
pa.Check(lambda x: x > 0, element_wise=True)
```

## pydantic — Structured Data Validation

```bash
pip install pydantic
```

### Basic model

```python
from pydantic import BaseModel, Field, validator, field_validator
from datetime import datetime
from typing import Optional, List
import json

class Measurement(BaseModel):
    id:        int
    timestamp: datetime
    channel:   int = Field(ge=1, le=4)
    value:     float = Field(ge=0, le=1000)
    status:    str = Field(pattern=r'^(ok|error|pending)$')
    tags:      List[str] = []
    metadata:  Optional[dict] = None

    @field_validator('value')
    @classmethod
    def round_value(cls, v):
        return round(v, 4)

# Parse and validate
m = Measurement(id=1, timestamp='2024-01-01T10:00:00', channel=2, value=3.14, status='ok')
m.timestamp   # datetime object (auto-parsed from string)

# From dict
m = Measurement.model_validate({'id': 1, 'timestamp': '...', ...})

# From JSON string
m = Measurement.model_validate_json('{"id": 1, ...}')

# Validation error
from pydantic import ValidationError
try:
    m = Measurement(id=1, channel=99, ...)  # channel > 4
except ValidationError as e:
    print(e.errors())   # list of dicts with loc, msg, type
    # [{'loc': ('channel',), 'msg': 'Input should be less than or equal to 4', ...}]
```

### Validate many records

```python
def validate_records(raw: list[dict]) -> tuple[list[Measurement], list[dict]]:
    valid, errors = [], []
    for i, record in enumerate(raw):
        try:
            valid.append(Measurement.model_validate(record))
        except ValidationError as e:
            errors.append({'index': i, 'record': record, 'errors': e.errors()})
    return valid, errors

valid, errors = validate_records(raw_records)
print(f"{len(valid)} valid, {len(errors)} invalid")

# Convert validated records to DataFrame
import pandas as pd
df = pd.DataFrame([m.model_dump() for m in valid])
```

### Config files / environment variables

```python
from pydantic_settings import BaseSettings  # pip install pydantic-settings

class Settings(BaseSettings):
    db_url:      str
    s3_bucket:   str
    batch_size:  int = 1000
    debug:       bool = False

    class Config:
        env_file = '.env'    # reads from .env file
        env_prefix = 'APP_'  # APP_DB_URL, APP_S3_BUCKET, etc.

settings = Settings()   # raises if required fields missing
```

## Reporting Validation Results

```python
import pandas as pd
from datetime import datetime

def validation_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return a row-per-check summary of validation results."""
    checks = []

    def check(name, condition_series, threshold=1.0):
        pass_rate = condition_series.mean()
        checks.append({
            'check':      name,
            'pass_rate':  pass_rate,
            'passed':     int(condition_series.sum()),
            'failed':     int((~condition_series).sum()),
            'ok':         pass_rate >= threshold,
        })

    check('no_null_id',         df['id'].notna())
    check('no_null_value',      df['value'].notna(), threshold=0.95)
    check('value_in_range',     df['value'].between(0, 1000))
    check('valid_status',       df['status'].isin(['ok', 'error', 'pending']))
    check('unique_id',          ~df['id'].duplicated())
    check('timestamp_recent',   df['timestamp'] >= '2020-01-01')

    report = pd.DataFrame(checks)
    print(report.to_string(index=False))
    return report

report = validation_report(df)
if not report['ok'].all():
    failed = report[~report['ok']]['check'].tolist()
    raise ValueError(f"Validation failed: {failed}")
```
