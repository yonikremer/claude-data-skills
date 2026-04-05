---
name: forecast
description: Use when performing zero-shot forecasting on a time-series column. Usage: /forecast <column> <file>
---

# Forecast Command

When this skill is invoked (e.g., via `/forecast <column> <file>`), use the `timesfm-forecasting` skill to:

1. Perform a zero-shot forecast on the specified column.
2. Handle frequency detection automatically.
3. Provide a plot of the historical vs forecasted values.
