---
name: jupyter
description: Manages interactive development and visualization within Jupyter notebooks. Use when prototyping analyses or creating interactive widgets. Do NOT use for production-grade automation (use cli-scripts) or for complex web apps (use plotly-dash).
---
# Jupyter

## Essential Magic Commands

```python
# --- Timing ---
%time  some_function()          # time a single call
%timeit some_function()         # average over many runs (auto-selects repeat count)
%%time                          # time entire cell
%%timeit                        # benchmark entire cell

# --- Display ---
%matplotlib inline              # render matplotlib in notebook
%matplotlib widget              # interactive matplotlib (requires ipympl)

# --- File system ---
%pwd                            # print working directory
%ls                             # list files
%cd path/to/dir                 # change directory
%run script.py                  # run a .py file in notebook context
%run script.py arg1 arg2        # with arguments

# --- Code ---
%who                            # list variables in namespace
%whos                           # variables with type and value
%reset                          # clear namespace
%history                        # show input history
%history -n 1-10                # lines 1-10
%recall 5                       # put line 5 in next input
%store x                        # persist variable across notebooks
%store -r x                     # restore persisted variable

# --- Shell ---
!ls -la                         # run any shell command
!pip install pandas
files = !ls *.csv               # capture shell output as list
result = !python script.py      # capture stdout

# --- Profiling ---
%prun some_function()           # cProfile
%lprun -f func some_function()  # line profiler (pip install line_profiler)
%memit some_function()          # memory usage (pip install memory_profiler)

# --- Other ---
%env VAR=value                  # set environment variable
%load script.py                 # load file contents into cell
%save output.py 1-5             # save cells 1-5 to .py file
%notebook output.ipynb          # export history to notebook
%debug                          # post-mortem debugger on last exception
%pdb on                         # auto-invoke debugger on exception
```

## Rich Output and Display

```python
from IPython.display import display, HTML, Markdown, Image, JSON, Audio, Video

# Render HTML
display(HTML("<h2 style='color:red'>Hello</h2>"))

# Render Markdown
display(Markdown("## Section\n- item 1\n- item 2"))

# Show image from file or URL
display(Image('plot.png'))
display(Image(url='https://example.com/img.png', width=400))

# Show JSON interactively (collapsible tree)
display(JSON({'key': [1, 2, {'nested': True}]}))

# Multiple outputs from one cell
display(df.head(), df.describe())

# Suppress output with semicolon
df.plot();    # the ; suppresses the matplotlib output line

# Progress bars
from tqdm.notebook import tqdm   # pip install tqdm
for item in tqdm(items, desc='Processing'):
    process(item)

# Pandas display options
import pandas as pd
pd.set_option('display.max_columns', 50)
pd.set_option('display.max_rows', 100)
pd.set_option('display.float_format', '{:.4f}'.format)
pd.set_option('display.max_colwidth', 200)
pd.reset_option('all')   # reset to defaults
```

## ipywidgets — Interactive Controls

```bash
pip install ipywidgets
```

```python
import ipywidgets as widgets
from IPython.display import display

# Slider
slider = widgets.IntSlider(value=50, min=0, max=100, step=5, description='N:')
display(slider)
slider.value   # read current value

# Dropdown
dd = widgets.Dropdown(options=['A', 'B', 'C'], value='A', description='Cat:')

# Text input
txt = widgets.Text(value='', placeholder='Search...', description='Query:')

# Checkbox
cb = widgets.Checkbox(value=False, description='Include nulls')

# Date picker
dp = widgets.DatePicker(description='Date:')

# interact — auto-create widgets from function signature
from ipywidgets import interact, interactive

@interact(n=(10, 100, 10), category=['A', 'B', 'C'])
def show_top(n=20, category='A'):
    display(df[df['cat'] == category].head(n))

# interact_manual — only update on button click (for slow operations)
from ipywidgets import interact_manual

@interact_manual(query='', threshold=(0.0, 1.0, 0.05))
def search(query='', threshold=0.5):
    results = run_query(query, threshold)
    display(results)

# Output widget — capture output in a specific cell
out = widgets.Output()
display(out)

with out:
    display(df.plot())   # output goes into the widget, not the cell

out.clear_output()

# Full interactive dashboard with observe
dd = widgets.Dropdown(options=df['category'].unique(), description='Category:')
fig_output = widgets.Output()
display(dd, fig_output)

def on_change(change):
    fig_output.clear_output(wait=True)
    with fig_output:
        filtered = df[df['category'] == change['new']]
        display(filtered.plot(x='date', y='value'))

dd.observe(on_change, names='value')
```

## nbconvert — Export Notebooks

```bash
# HTML (default, shareable)
jupyter nbconvert --to html notebook.ipynb
jupyter nbconvert --to html --no-input notebook.ipynb   # hide code cells

# PDF (requires LaTeX)
jupyter nbconvert --to pdf notebook.ipynb

# Python script
jupyter nbconvert --to script notebook.ipynb

# Execute and export in one step
jupyter nbconvert --to html --execute notebook.ipynb
jupyter nbconvert --to html --execute --ExecutePreprocessor.timeout=300 notebook.ipynb

# Execute only (update outputs in-place)
jupyter nbconvert --to notebook --execute notebook.ipynb --output notebook_executed.ipynb

# Multiple notebooks
jupyter nbconvert --to html *.ipynb
```

## Programmatic Notebook Execution

```python
# pip install nbformat nbconvert
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

with open('analysis.ipynb') as f:
    nb = nbformat.read(f, as_version=4)

ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
ep.preprocess(nb, {'metadata': {'path': '.'}})

with open('analysis_executed.ipynb', 'w') as f:
    nbformat.write(nb, f)
```

## Useful Keyboard Shortcuts

**Command mode (Esc):**
- `A` / `B` — insert cell above / below
- `D D` — delete cell
- `M` — convert to Markdown
- `Y` — convert to code
- `Shift+Up/Down` — select multiple cells
- `Shift+M` — merge selected cells
- `C` / `V` — copy / paste cell

**Edit mode (Enter):**
- `Ctrl+Enter` — run cell
- `Shift+Enter` — run cell, move to next
- `Alt+Enter` — run cell, insert below
- `Tab` — autocomplete
- `Shift+Tab` — tooltip / docstring
- `Ctrl+/` — toggle comment
- `Ctrl+Z` — undo

## Productivity Tips

```python
# See function signature and docs inline
?pd.read_csv          # short docstring
??pd.read_csv         # full source

# Autoreload — automatically reload changed .py files without restarting kernel
%load_ext autoreload
%autoreload 2

# Watermark — record environment info in notebooks
# pip install watermark
%load_ext watermark
%watermark -v -p pandas,numpy,plotly

# Suppress all warnings in notebook
import warnings
warnings.filterwarnings('ignore')

# Show all outputs from a cell (not just the last expression)
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'
```
