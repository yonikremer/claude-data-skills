---
name: plotly-dash
description: Use when building interactive web dashboards and data applications. Ideal for creating complex reactive UIs with charts and sliders. Do NOT use for simple static plots (use plotly) or for basic notebook interactivity (use jupyter).
---
# Plotly Dash

## Overview

Dash turns Plotly charts into interactive web apps using only Python. The core concepts:
- **Layout** — define the UI using HTML/component tree
- **Callbacks** — Python functions that react to user input and update outputs
- **Components** — `dash_core_components` (graphs, dropdowns, sliders) and `dash_html_components` (divs, headings)

```bash
pip install dash pandas plotly
```

## Quick Start

```python
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('data.csv')

app = Dash(__name__)

app.layout = html.Div([
    html.H1("My Dashboard"),
    dcc.Dropdown(
        id='category-filter',
        options=[{'label': c, 'value': c} for c in df['category'].unique()],
        value=df['category'].iloc[0],
        clearable=False,
    ),
    dcc.Graph(id='main-chart'),
])

@app.callback(
    Output('main-chart', 'figure'),
    Input('category-filter', 'value'),
)
def update_chart(selected_category):
    filtered = df[df['category'] == selected_category]
    return px.line(filtered, x='date', y='value', title=f'{selected_category} over time')

if __name__ == '__main__':
    app.run(debug=True)   # opens at http://127.0.0.1:8050
```

## Layout Components

### Core Components (`dcc`)

```python
from dash import dcc

# Dropdown
dcc.Dropdown(id='dd', options=['A', 'B', 'C'], value='A', multi=False)
dcc.Dropdown(id='dd', options=[{'label': 'Option A', 'value': 'a'}], multi=True)

# Slider
dcc.Slider(id='sl', min=0, max=100, step=5, value=50,
           marks={0: '0', 50: '50', 100: '100'})

# Range slider
dcc.RangeSlider(id='rs', min=0, max=100, value=[20, 80])

# Date picker
dcc.DatePickerSingle(id='dp', date='2024-01-01')
dcc.DatePickerRange(id='dpr',
    start_date='2024-01-01', end_date='2024-12-31',
    display_format='YYYY-MM-DD')

# Text input
dcc.Input(id='inp', type='text', placeholder='Search...', debounce=True)

# Radio buttons
dcc.RadioItems(id='radio',
    options=[{'label': 'A', 'value': 'a'}, {'label': 'B', 'value': 'b'}],
    value='a', inline=True)

# Checklist
dcc.Checklist(id='cl',
    options=['Option 1', 'Option 2', 'Option 3'],
    value=['Option 1'])

# Graph (Plotly figure container)
dcc.Graph(id='chart', figure={})

# Store (client-side data storage, invisible)
dcc.Store(id='store', data={})

# Interval (trigger callbacks on a timer)
dcc.Interval(id='interval', interval=5000, n_intervals=0)  # every 5 seconds

# Tabs
dcc.Tabs([
    dcc.Tab(label='Tab 1', children=[...]),
    dcc.Tab(label='Tab 2', children=[...]),
])
```

### HTML Components

```python
from dash import html

html.Div(children=[...], id='container', className='my-class', style={'padding': '20px'})
html.H1('Title')
html.P('Some text')
html.Button('Click me', id='btn', n_clicks=0)
html.Hr()   # horizontal rule
html.Br()   # line break
html.A('Link', href='https://example.com')
html.Img(src='/assets/logo.png', style={'width': '100px'})
```

## Callbacks

### Basic Input → Output

```python
from dash import callback, Input, Output, State

@callback(
    Output('output-div', 'children'),
    Input('my-input', 'value'),
)
def update_output(input_value):
    return f'You entered: {input_value}'
```

### Multiple Inputs and Outputs

```python
@callback(
    Output('chart', 'figure'),
    Output('summary', 'children'),
    Input('category-dd', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
)
def update(category, start_date, end_date):
    filtered = df[
        (df['category'] == category) &
        (df['date'] >= start_date) &
        (df['date'] <= end_date)
    ]
    fig = px.bar(filtered, x='date', y='value')
    summary = f"{len(filtered)} records"
    return fig, summary
```

### State (read input without triggering callback)

```python
@callback(
    Output('result', 'children'),
    Input('submit-btn', 'n_clicks'),    # triggers the callback
    State('text-input', 'value'),       # read but doesn't trigger
)
def on_submit(n_clicks, text_value):
    if not n_clicks:
        return ''
    return f'Submitted: {text_value}'
```

### Prevent Update

```python
from dash.exceptions import PreventUpdate

@callback(Output('out', 'children'), Input('inp', 'value'))
def update(value):
    if not value:
        raise PreventUpdate   # don't update anything
    return value.upper()
```

### Pattern-Matching Callbacks (dynamic components)

```python
from dash import ALL, MATCH

# Output/Input referencing all components with {'type': 'filter', 'index': ALL}
@callback(
    Output({'type': 'chart', 'index': MATCH}, 'figure'),
    Input({'type': 'filter', 'index': MATCH}, 'value'),
)
def update_chart(selected):
    ...
```

## DataTable

```python
from dash import dash_table

dash_table.DataTable(
    id='table',
    data=df.to_dict('records'),
    columns=[{'name': c, 'id': c} for c in df.columns],

    # Filtering and sorting
    filter_action='native',
    sort_action='native',
    sort_mode='multi',

    # Pagination
    page_action='native',
    page_size=20,

    # Row selection
    row_selectable='multi',
    selected_rows=[],

    # Styling
    style_table={'overflowX': 'auto'},
    style_cell={'textAlign': 'left', 'padding': '8px'},
    style_header={'backgroundColor': '#f0f0f0', 'fontWeight': 'bold'},
    style_data_conditional=[
        {'if': {'filter_query': '{value} > 100'}, 'backgroundColor': '#ffe0e0'},
    ],
)

# Read selected rows in a callback
@callback(
    Output('detail', 'children'),
    Input('table', 'selected_rows'),
    State('table', 'data'),
)
def show_selected(selected_rows, data):
    if not selected_rows:
        raise PreventUpdate
    selected = [data[i] for i in selected_rows]
    return str(selected)
```

## Common Dashboard Patterns

### Live-updating chart (polling)

```python
app.layout = html.Div([
    dcc.Graph(id='live-chart'),
    dcc.Interval(id='interval', interval=10_000, n_intervals=0),  # 10s
])

@callback(Output('live-chart', 'figure'), Input('interval', 'n_intervals'))
def refresh(_):
    df = fetch_latest_data()   # query DB / API
    return px.line(df, x='ts', y='value')
```

### Store data between callbacks (avoid querying DB twice)

```python
app.layout = html.Div([
    dcc.Dropdown(id='filter'),
    dcc.Store(id='filtered-data'),   # intermediate storage
    dcc.Graph(id='chart'),
    html.Div(id='summary'),
])

@callback(Output('filtered-data', 'data'), Input('filter', 'value'))
def load_data(filter_val):
    df = query_db(filter_val)
    return df.to_dict('records')   # Store holds JSON-serializable data

@callback(Output('chart', 'figure'), Input('filtered-data', 'data'))
def draw_chart(data):
    return px.line(pd.DataFrame(data), x='date', y='value')

@callback(Output('summary', 'children'), Input('filtered-data', 'data'))
def show_summary(data):
    return f"{len(data)} records"
```

## Styling and Layout

```python
# Inline style
html.Div(style={'display': 'flex', 'gap': '20px', 'padding': '10px'})

# CSS classes — put CSS files in assets/ directory, they load automatically
html.Div(className='dashboard-container')

# Bootstrap (no custom CSS needed)
# pip install dash-bootstrap-components
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(dcc.Graph(id='chart1'), width=8),
        dbc.Col(dcc.Graph(id='chart2'), width=4),
    ]),
    dbc.Row([
        dbc.Col(dash_table.DataTable(...), width=12),
    ]),
])
```

## Running and Deploying

```python
# Development
app.run(debug=True, port=8050)

# Production (use a WSGI server)
server = app.server   # exposes the underlying Flask server
# Then: gunicorn app:server -b 0.0.0.0:8050 -w 4
```
