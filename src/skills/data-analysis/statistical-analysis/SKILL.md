---
name: statistical-analysis
description: Use when performing statistical testing, trend analysis, and business metric investigation. Ideal for hypothesis testing (t-test, ANOVA), A/B test analysis, and answering complex data questions with rigorous methodology.
---

# Statistical Analysis

## 1. Business Metrics & Trends

Investigate performance and patterns in business data.

- **Central Tendency**: Always report **Mean and Median** together. If they diverge, the data is skewed.
- **Trend Smoothing**: Use 7-day or 28-day rolling averages to remove weekly/monthly noise.
- **Growth**: Calculate WoW, MoM, and YoY (Gold Standard) to account for seasonality.
- **Forecasting**: Use simple naive or linear trend models for quick estimates; communicate uncertainty as a range.

## 2. Hypothesis Testing (Academic Rigor)

Determine if differences are real or due to chance.

| Scenario              | Recommended Test                          |
|-----------------------|-------------------------------------------|
| Compare 2 means       | Independent t-test                        |
| Compare 2 proportions | Z-test for proportions (Conversion rates) |
| Compare 3+ means      | ANOVA                                     |
| Non-normal data       | Mann-Whitney U or Kruskal-Wallis          |
| Category association  | Chi-squared test                          |

**Workflow**:

1. **Check Assumptions**: Verify normality (Shapiro-Wilk) and homogeneity of variance (Levene's).
2. **Run Test**: Use `pingouin` or `scipy.stats`.
3. **Effect Size**: Always report **Cohen's d** or **Partial Eta-squared** alongside p-values.

## 3. Answering Analysis Questions

When asked to "analyze" a problem:

1. **Gather Data**: Extract from SQL or local files using appropriate joins.
2. **Validate**: Run row-count sanity checks and magnitude checks.
3. **Segment**: Look for Simpson's Paradox (trends reversing when sliced).
4. **Report**: Lead with the key insight, support with data, and list actionable recommendations.

## Common Pitfalls

- **P-hacking**: Don't test until you find something significant.
- **Correlation != Causation**: Be explicit about confounding variables.
- **Multiple Comparisons**: Use Bonferroni correction if testing many hypotheses at once.
