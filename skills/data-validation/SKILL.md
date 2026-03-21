---
name: data-validation
description: Enforces data quality, schemas, and analytical methodology. Use for technical schema enforcement (Pandera/Pydantic) and QAing analyses for bias and accuracy.
---
# Data Validation

## 1. Technical Validation (Schemas)

Pick the right tool for the job:
- **pandera**: DataFrame schema validation (pandas/polars).
- **pydantic**: JSON, API responses, and structured objects.
- **built-in assertions**: Quick checks in scripts.

### pandera Example
```python
import pandera as pa
schema = pa.DataFrameSchema({
    "id": pa.Column(int, unique=True, nullable=False),
    "value": pa.Column(float, pa.Check.ge(0)),
    "status": pa.Column(str, pa.Check.isin(['ok', 'error']))
})
validated_df = schema.validate(df)
```

## 2. Analytical Methodology (QA)

Before sharing results, run this checklist:

### Data Quality Checks
- [ ] **Freshness**: Is the data current enough?
- [ ] **Completeness**: No unexpected gaps in time series.
- [ ] **Deduplication**: No double-counting from bad joins.
- [ ] **Null handling**: Are nulls handled (excluded vs imputed)?

### Common Pitfalls
- **Join Explosion**: Check row counts before and after joins.
- **Survivorship Bias**: Are you only analyzing "survivors"?
- **Average of Averages**: Always aggregate from raw data.
- **Simpson's Paradox**: Check if trends reverse when segmented.

## 3. Statistical Sanity
- **Magnitude**: Are the numbers plausible? (e.g., conversion between 0-100%).
- **Cross-Validation**: Calculate the same metric two different ways to see if they match.
- **Red Flags**: Any metric that changed >50% WoW without an obvious cause.
