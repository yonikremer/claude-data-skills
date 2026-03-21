---
name: data-visualization
description: Generates high-quality visualizations and provides design guidance. Use for creating charts from DataFrames/Queries and applying accessibility principles. Plotly is the primary recommendation.
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

- **No Chart Junk**: Remove unnecessary gridlines and borders.
- **Hierarchy**: Use color to highlight the most important series; use grey for others.
- **Accessibility**: Use line styles (dashed/dotted) in addition to color to distinguish series.
- **Honesty**: Avoid 3D charts or dual-axes that imply false correlation.

## References (Load on demand)
- `skills/scientific-visualization/references/plotly_examples.md` — Complex subplots and error bands.
- `skills/scientific-visualization/references/color_palettes.md` — Colorblind-safe hex codes.
