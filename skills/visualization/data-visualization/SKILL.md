---
name: data-visualization
description: Use when generating high-quality visualizations or applying design guidance to charts. Ideal for matching data relationships to chart types and ensuring accessibility. CRITICAL: Always provide specific, insight-driven titles and labeled axes with units.
---
# Data Visualization

## Workflow: Create a Visualization

1. **Select Chart Type**: Match the data relationship (Trend → Line, Comparison → Bar, Correlation → Scatter).
2. **Generate Code**: Use **Plotly** (preferred for interactivity) or **Seaborn** (static).
3. **Apply Design Standards**:
   - Title must state the *insight* (e.g., "Revenue Grew 20%").
   - Use colorblind-friendly palettes (`px.colors.qualitative.Safe`).
   - Axes must be labeled with units. Bar charts MUST start at zero.
4. **Save & Export**: Save as PNG/PDF for reports or HTML for interactivity.

## Chart Selection Guide

| Goal | Best Chart | Alternative |
|---|---|---|
| **Trend** | Line Chart | Area Chart |
| **Comparison** | Horizontal Bar | Lollipop |
| **Distribution** | Histogram | Box / Violin Plot |
| **Correlation** | Scatter Plot | Heatmap |
| **Part-to-Whole** | Treemap | Donut (max 5 slices) |

## Implementation Patterns (Plotly)

### Standard Line Plot
```python
import plotly.express as px
fig = px.line(df, x='date', y='value', color='category', 
              template='simple_white', title='Insight Summary')
fig.update_layout(hovermode='x unified')
fig.show()
```

### Publication-Quality Export
```python
# Requires kaleido: pip install kaleido
fig.write_image("output.pdf", width=800, height=500, scale=2)
```

## Design Principles

- **Descriptive & Specific Titles (MANDATORY)**: Never use generic titles like "Job Distribution" or "Revenue Over Time". Titles must describe the **subset, filters, and core insight**.
  - *Bad*: "Job Distribution"
  - *Good*: "Top 10 Job Categories for American Adults (2023 Survey)"
  - *Bad*: "Monthly Revenue"
  - *Good*: "Monthly Revenue ($) for Enterprise Customers in North America"
- **Technically Correct Axis Labels**: Always include units in parentheses (e.g., "Revenue ($)", "Temperature (°C)", "Time (ms)").
- **Contextual Annotations**: If the data is filtered (e.g., `df[df['age'] > 18]`), the title or a subtitle MUST reflect this (e.g., "Adult Population only").
- **No Chart Junk**: Remove unnecessary gridlines and borders.
- **Hierarchy**: Use color to highlight the most important series; use grey for others.

## References (Load on demand)
- `skills/visualization/plotly/references/api-reference.md` — Plotly API signatures.
- `skills/visualization/seaborn/references/api-reference.md` — Seaborn API signatures.
- `skills/scientific-visualization/references/plotly_examples.md` — Complex subplots and error bands.
- `skills/scientific-visualization/references/color_palettes.md` — Colorblind-safe hex codes.
