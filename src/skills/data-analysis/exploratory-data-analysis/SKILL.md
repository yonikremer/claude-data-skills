---
name: exploratory-data-analysis
description: Use when performing comprehensive exploratory analysis on scientific and business data. Ideal for deep structural analysis, data quality checks, profiling, and categorical hierarchies. CRITICAL: Run `get-available-resources` first for datasets > 500MB.
---

# Exploratory Data Analysis

## ⚠️ Mandatory Pre-flight: Resource Check

EDA on large datasets (SQL tables, HDF5, CSV) can crash the session if memory is not managed.

1. **Run Detection**: Execute `python skills/get-available-resources/scripts/detect_resources.py`.
2. **Strategy**:
    - **Data < 50% RAM**: Perform full in-memory analysis using `pandas`, `polars`, or `numpy`.
    - **Data 50-90% RAM**: Use `polars` lazy mode.
    - **Data > RAM**: Perform **Streaming Analysis** or sample the first/random 10% of the dataset.

## Professional Workflow & Logical Checks

Beyond basic statistics, you MUST answer these "Deep EDA" questions for every dataset:

### 1. Structure & Grain

- How many rows and columns? What is the primary key?
- What is the grain (one row per what)?
- **Categorical Hierarchies**: Identify if columns have a parent-child relationship (e.g., `City` → `Country`).
    - *Check*: For every unique value in A, is there only one unique value in B?

### 2. Missingness (Nullity) Patterns

- **Missingness Correlation**: Do certain columns always fail together? Calculate `df.isnull().corr()`.
- **Conditional Nullity**: Is a column null only for certain categories? (e.g., `pregnancy_status` is only non-null for
  `Gender='Female'`).

### 3. Redundancy & Constants

- **Constant Columns**: Identify and ignore columns with `nunique() <= 1`.
- **High Collinearity**: Identify numeric columns with `corr() > 0.99`.
- **Redundant Categories**: Use Normalized Mutual Information (NMI) to find overlapping dimensions.

### 4. Distribution & Skew

- **Concentration Risk**: What % of the total sum is held by the top 1% of values? (Gini-coefficient style).
- **Zero-Inflation**: Flag columns with >50% zeros.

## Common Pitfalls (The "Wall of Shame")

1. **Assuming Random Missingness**: Missing data is often a "signal" (e.g., failed sensor at low temps). Check
   `nullity_correlation`.
2. **Over-Analysis of IDs**: Don't calculate mean/std for ID columns. Flag them as `identifiers` immediately.
3. **Ignoring Unit Scales**: Mixing meters and millimeters in the same column. Check for multi-modal distributions.

## Workflow

### Step 1: Data Access & Type Detection

Identify if you are querying a **SQL Warehouse** or a **Local File**.

- For SQL, explore schema metadata first.

### Step 2: Perform Data Profiling

Use `scripts/eda_analyzer.py` for automated file analysis or run custom profiling:

- Dimensions, dtypes, null rates.
- Summary statistics (Mean, Median, Std, Percentiles p1-p99).
- Value counts for dimensions.

### Step 3: Deep Logic Checks

Apply the hierarchical and nullity checks defined above to uncover hidden data rules.

### Step 4: Generate Report & Memory

Create a `{filename}_eda_report.md` with Findings, Data Quality Issues, and Downstream Recommendations.

- **MANDATORY**: Update `.claude_data_dictionary.json` in the project root. This file acts as the agent's long-term
  memory for dataset schemas, column meanings, and discovered hierarchies.

## References (Load on demand)

- `references/advanced_eda_questions.md` — Detailed logic for hierarchy and nullity checks.
- `references/general_scientific_formats.md` — How to read CSV, HDF5, Parquet, etc.
