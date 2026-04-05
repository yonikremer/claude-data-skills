# Advanced EDA Questions & Logical Checks

This reference provides specific logical patterns for deep exploratory data analysis, focusing on relationships between
variables, data quality, and structural anomalies.

## 1. Categorical Relationships & Hierarchies

Detecting if one categorical column is a "sub-category" of another.

**Question:** Is Column A a sub-category of Column B?
**Logic:** For every unique value in A, is there only one unique value in B?

```python
def is_sub_category(df, col_a, col_b):
    """Checks if col_a is a sub-category of col_b."""
    # Group by A and count unique B values
    counts = df.groupby(col_a)[col_b].nunique()
    return (counts <= 1).all()

# Example: 'City' is a sub-category of 'Country'
# If every 'City' belongs to exactly one 'Country', it's a hierarchy.
```

**Question:** What is the overlap between two categorical columns?
**Logic:** Use a contingency table (Crosstab) and Chi-squared test for independence.

```python
import pandas as pd
from scipy.stats import chi2_contingency

contingency = pd.crosstab(df['Category_A'], df['Category_B'])
chi2, p, dof, ex = chi2_contingency(contingency)
# Small p-value (< 0.05) indicates a significant relationship.
```

## 2. Nullity & Missingness Patterns

Understanding *why* data is missing is often more important than knowing *how much* is missing.

**Question:** Is there a relationship between the nullity of two columns?
**Logic:** Create binary "is_null" indicators and calculate correlation.

```python
def nullity_correlation(df):
    """Calculates correlation between missingness of columns."""
    null_df = df.isnull().astype(int)
    # Filter out columns with no nulls
    null_df = null_df.loc[:, null_df.any()]
    return null_df.corr()

# High positive correlation means when A is missing, B is also missing.
# High negative correlation means when A is present, B is missing (mutually exclusive).
```

**Question:** Is a column null for one category and not for others? (Conditional Nullity)
**Logic:** Group by the categorical column and calculate the null rate of the target column.

```python
def conditional_nullity(df, cat_col, target_col):
    """Calculates null rate of target_col per category in cat_col."""
    return df.groupby(cat_col)[target_col].apply(lambda x: x.isnull().mean())

# If null rate is 1.0 for 'Category A' and 0.0 for 'Category B', 
# the data might only be collected/applicable for certain groups.
```

## 3. Redundancy & Feature Overlap

**Question:** Are two columns providing the same information?
**Logic:** Check for identical values or extremely high correlation.

```python
# For numeric:
correlation_matrix = df.corr().abs()
# Flag pairs with r > 0.99

# For categorical:
# Calculate Normalized Mutual Information (NMI)
from sklearn.metrics import normalized_mutual_info_score
nmi = normalized_mutual_info_score(df['col_a'], df['col_b'])
# nmi close to 1.0 indicates redundancy.
```

## 4. Value Concentration & Imbalance

**Question:** Is the data dominated by a few values?
**Logic:** Calculate the "Concentration Ratio" (top N values share of total).

```python
def concentration_ratio(df, col, n=1):
    """Calculates the share of the top N values."""
    counts = df[col].value_counts(normalize=True)
    return counts.head(n).sum()

# If top 1% of users account for 80% of revenue, you have a skewed population.
```

## 5. Unit & Scale Detection

**Question:** Are the values in a specific unit or scale?
**Logic:**

- Check if all values are between 0 and 1 (Probabilities/Normalized).
- Check if all values are integers (Counts).
- Check column names for keywords: `_kg`, `_ms`, `_usd`, `_pct`.

## 6. Constant & Near-Constant Columns

**Question:** Does this column provide any information?
**Logic:** Calculate variance or unique value count.

```python
# Remove columns with only 1 unique value
constant_cols = [col for col in df.columns if df[col].nunique() <= 1]

# Remove columns with very low variance (near-constant)
from sklearn.feature_selection import VarianceThreshold
# (Requires numeric data)
```

## 7. Temporal Drift & Stationarity

**Question:** Does the data distribution change over time?
**Logic:** Split the data into two halves (early vs late) and compare distributions (KS-test).

```python
from scipy.stats import ks_2samp
# Compare distribution of 'Value' in first 50% vs last 50% of time
statistic, p_value = ks_2samp(early_data, late_data)
# Small p-value indicates "Data Drift".
```
