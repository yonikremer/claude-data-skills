---
name: visualization-pro
description: Use for creating ALL data visualizations, from static statistical plots to interactive web dashboards. Unified guide for Plotly (Primary Recommendation), Dash (Dashboards), and Seaborn (Static Stats). CRITICAL: Use Plotly for interactive web-based outputs.
---

# Visualization Pro (Consolidated)

Unified expert guide for high-impact data visualization and interactive dashboard development.

## ⚠️ Mandatory Pre-flight: Design & interactivity

1. **Plotly First**: Always prefer Plotly for interactive, web-ready visualizations.
2. **Accessibility**: Use colorblind-friendly palettes (e.g., `viridis`, `colorblind`).
3. **Resource Awareness**: For datasets > 100k points, use `go.Scattergl` (WebGL) in Plotly to prevent browser lag.

---

## 1. Plotly (The Interactive Standard)

Use for interactive, publication-quality visualizations.

### Core Idioms

- **Express vs Graph Objects**: Use `plotly.express` for fast exploration; use `graph_objects` for fine-grained control.
- **Figure Layout**: Always include clear axis labels, titles, and legends.

```python
import plotly.express as px
df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
fig.show()
```

---

## 2. Plotly Dash (Interactive Dashboards)

Use for building complex, multi-component data applications.

### Core Idioms

- **Callbacks**: Use `Input` and `Output` to create reactive components.
- **Layout**: Use `dash_bootstrap_components` (dbc) for responsive, professional designs.

---

## 3. Seaborn (Static Statistical Plots)

Use for publication-ready static figures and quick statistical exploration.

### Core Idiom

- **Context**: Use `sns.set_context("paper")` for publication-ready font sizes.

```python
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")
sns.boxplot(data=df, x="species", y="sepal_length")
plt.show()
```

---

## 🛠️ Common Pitfalls (The "Wall of Shame")

1. **Over-Plotting**: Trying to show 1M points in a standard SVG scatter plot; use WebGL or downsampling.
2. **Misleading Scales**: Not starting the Y-axis at zero for bar charts unless explicitly justified.
3. **Legend Bloat**: Including a legend with 20+ items; use interactive filtering or faceted plots instead.

## References

- `skills/visualization/visualization-pro/references/plotly/` — Advanced graph objects and layouts.
- `skills/visualization/visualization-pro/references/plotly-dash/` — Callback patterns and state management.
- `skills/visualization/visualization-pro/references/seaborn/` — Statistical plot types and color palettes.
