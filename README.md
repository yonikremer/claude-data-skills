# Claude Data Skills 🐍📊

A professional-grade collection of data science, analysis, and engineering skills and scripts for AI-assisted development.

[![PyPI Version](https://img.shields.io/pypi/v/claude-data-skills.svg)](https://pypi.org/project/claude-data-skills/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## Overview

`claude-data-skills` is a comprehensive library designed to enhance AI-assisted data workflows. It provides a structured collection of "skills"—reusable, idiomatic patterns and scripts for everything from advanced standard library usage to complex machine learning pipelines.

## Key Features

- **🚀 Professional Stdlib Usage**: High-performance patterns for `pathlib`, `itertools`, `collections`, and `contextlib`.
- **🛡️ Data Safety First**: Built-in guardrails to prevent accidental data loss or corruption during autonomous execution.
- **📊 Modern Visualization**: First-class support for Plotly and Dash, ensuring interactive and high-quality data stories.
- **🧠 ML-Ready**: Pre-configured patterns for PyTorch, Scikit-Learn, and Transformers.
- **📁 Unstructured Data Support**: Advanced parsing for PDF, DOCX, XLSX, and binary formats.

## Installation

Install the package directly from PyPI:

```bash
pip install claude-data-skills
```

## Quick Start

### Using the CLI
The package includes several built-in commands. For example, to run the standard library demonstration:

```bash
stdlib-demo
```

### Importing Skills
You can import advanced utility patterns directly into your own scripts:

```python
from skills.python_dev.python_stdlib_pro.scripts.stdlib_demo import test_pathlib

# Run a verified pathlib pattern
test_pathlib()
```

## Core Principles

- **Resource Aware**: Every intensive task starts with hardware resource validation.
- **LLM Optimized**: Scripts are dense, idiomatic, and contain strict guardrails for local/open-source LLMs.
- **Atomic Operations**: Prevents file corruption by using temp-and-replace patterns for all writes.

## Project Structure

```text
skills/
├── data-analysis/          # Dask, Polars, Pandas, Geopandas
├── machine-learning/       # PyMC, PyTorch-Lightning, Scikit-Learn
├── python-dev/             # Stdlib Pro, Debugging, Refactoring
├── scientific-workflow/    # Scholar Evaluation, Visualization
└── unstructured-data/      # PDF, DOCX, XLSX, Binary
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Created and maintained by **Yoni Kremer**.
