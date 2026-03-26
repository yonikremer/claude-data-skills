# Python PDB Debugger Guide

Use the Python debugger (`pdb`) to step through code and inspect variables.

## How to Start the Debugger

### 1. Insert a Breakpoint
Add this line right before the error or the line you want to inspect:
```python
import pdb; pdb.set_trace()
```

### 2. Run your Script
When the code hits that line, the program will pause and show a `(Pdb)` prompt.

## Essential PDB Commands
Type these commands at the `(Pdb)` prompt:

- **`n` (next)**: Go to the next line in the current function.
- **`s` (step)**: Step into a function call.
- **`c` (continue)**: Continue running until the next breakpoint.
- **`p <variable>` (print)**: Print the value of a variable.
- **`ll` (long list)**: Show the source code for the current function.
- **`q` (quit)**: Stop the debugger and the program.

## Step-by-Step Workflow
1. Find where the code is acting weird.
2. Put `import pdb; pdb.set_trace()` right before that spot.
3. Run the code.
4. When it stops, use `p <variable_name>` to check your data.
5. Use `n` to step through the logic one line at a time.
6. Figure out where the data changes unexpectedly.
7. Quit with `q` when you're done.
