# Plotly Scientific Visualization Examples

This reference provides complete, copy-pasteable examples of publication-quality figures created with Plotly.

## Example 1: Publication-Ready Line Plot

A standard single-column line plot with error bands, suitable for Nature or Science.

```python
import plotly.express as px
import pandas as pd
import numpy as np

# Generate synthetic data
x = np.linspace(0, 10, 50)
y = np.sin(x) + np.random.normal(0, 0.1, 50)
y_upper = y + 0.2
y_lower = y - 0.2

df = pd.DataFrame({'x': x, 'y': y, 'y_upper': y_upper, 'y_lower': y_lower})

# Create figure
fig = px.line(df, x='x', y='y', labels={'x': 'Time (s)', 'y': 'Amplitude (mV)'})

# Add error bands (using go.Scatter for shading)
import plotly.graph_objects as go
fig.add_trace(go.Scatter(
    x=np.concatenate([df['x'], df['x'][::-1]]),
    y=np.concatenate([df['y_upper'], df['y_lower'][::-1]]),
    fill='toself',
    fillcolor='rgba(0,176,246,0.2)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo="skip",
    showlegend=False
))

# Apply publication styling
fig.update_layout(
    template="simple_white",
    width=350,  # ~89mm
    height=250,
    font=dict(family="Arial, sans-serif", size=10),
    margin=dict(l=40, r=10, t=10, b=40),
    xaxis=dict(showgrid=False, ticks="outside", tickwidth=1, ticklen=5),
    yaxis=dict(showgrid=False, ticks="outside", tickwidth=1, ticklen=5)
)

# Export (requires kaleido)
fig.write_image("line_plot.pdf")
```

## Example 2: Statistical Comparison (Box + Strip)

```python
import plotly.express as px

df = px.data.tips()

fig = px.box(df, x="day", y="total_bill", color="smoker", 
             points="all", # Show individual points
             notched=True, 
             labels={"total_bill": "Total Bill ($)", "day": "Day of Week"},
             category_orders={"day": ["Thur", "Fri", "Sat", "Sun"]})

fig.update_layout(
    template="simple_white",
    width=350,
    height=300,
    boxmode='group',
    font=dict(family="Arial, sans-serif", size=10),
    legend=dict(title=None, yanchor="top", y=0.99, xanchor="left", x=0.01)
)

fig.write_image("statistical_comparison.pdf")
```

## Example 3: Multi-Panel Figure

Using Plotly subplots for complex layouts.

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(rows=1, cols=2, 
                    subplot_titles=("<b>A</b>", "<b>B</b>"),
                    horizontal_spacing=0.15)

# Panel A
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6], name="Group 1"), row=1, col=1)

# Panel B
fig.add_trace(go.Bar(x=['X', 'Y', 'Z'], y=[2, 5, 3], name="Group 2"), row=1, col=2)

fig.update_layout(
    template="simple_white",
    width=700, # ~183mm (double column)
    height=300,
    font=dict(family="Arial, sans-serif", size=10),
    showlegend=True
)

# Individual axes styling
fig.update_xaxes(title_text="Time", row=1, col=1)
fig.update_yaxes(title_text="Value", row=1, col=1)
fig.update_xaxes(title_text="Category", row=1, col=2)
fig.update_yaxes(title_text="Count", row=1, col=2)

fig.write_image("multipanel_figure.pdf")
```

## Example 4: Heatmap with Perceptually Uniform Colormap

```python
import plotly.express as px
import numpy as np

z = np.random.rand(10, 10)
fig = px.imshow(z, 
                color_continuous_scale='Viridis', # Perceptually uniform
                labels=dict(color="Z-score"))

fig.update_layout(
    template="simple_white",
    width=400,
    height=350,
    font=dict(family="Arial, sans-serif", size=10)
)

fig.write_image("heatmap.pdf")
```

## Tips for Publication Quality

1. **Fonts**: Always use `Arial` or `Helvetica` as requested by most journals.
2. **Size**: Set `width` and `height` in pixels (96 px = 1 inch). Nature single column is ~350px.
3. **Background**: Use `template="simple_white"` to remove gray backgrounds and gridlines.
4. **Lines**: Ensure `tickwidth` and axis `linewidth` are consistent (usually 1).
5. **Resolution**: Use `scale=3.125` when calling `write_image` for PNGs to get 300 DPI.
