# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository is **claude-data-analytics-skills**, a personalized Claude Code plugin containing high-quality skills
for data science, machine learning, research, and engineering. It is specifically optimized for use with **Open-Source
LLMs**, emphasizing resource-aware execution, idiomatic Python best practices, and robust visualization via Plotly.

## Releasing

To release a new version:

1. Bump the `version` field in `.claude-plugin/marketplace.json`
2. Commit and push to `main`

## Global Agent Guardrails

### 1. Foundation Skills (MANDATORY)

The following skills are **Foundation Skills**. They must be consulted and applied to **EVERY** relevant task,
regardless of whether the user explicitly asks for them:

- **`python-best-practices`**: Must be applied to all Python code generation, formatting, and refactoring.
- **`get-available-resources`**: Must be run before any task involving data loading (>100MB) or model training.
- **`data-validation`**: Must be applied to all data processing and analytical reporting.
- **`git`**: Must be used for tracking all code and skill modifications.

### 2. Skill Routing Table

When a user provides a prompt, route to these specialized skills based on intent:

| If user wants to...       | Use these Primary Skills                                   |
|:--------------------------|:-----------------------------------------------------------|
| **Explore a new dataset** | `exploratory-data-analysis`                                |
| **Clean/Transform data**  | `pandas`, `polars`, `numpy`, `python-stdlib-pro`           |
| **Visualize data**        | `data-visualization`, `scientific-visualization`           |
| **Train/Evaluate ML**     | `scikit-learn`, `anomaly-detection`, `timesfm-forecasting` |
| **Write/Optimize SQL**    | `sql-queries`                                              |
| **Build a UI/Dashboard**  | `build-dashboard`, `plotly-dash`                           |
| **Parallel Processing**   | `parallel-processing-pro`                                  |
| **Verify code quality**   | `pytest`, `pydantic`, `python-best-practices`              |
| **Manage version control** | `git`                                                      |
| **Process audio/video**   | `ffmpeg`                                                   |
| **Repair corrupted data** | `bit-error-correction`                                     |
| **Create new skills**     | `skill-engineering`                                        |
| **Summarize research**    | `research-summaries`                                       |
| **Handle specific files** | `pdf`, `docx`, `pptx`, `xlsx`, `binary-data-parsing`       |


## Gold Standard Requirements

Every skill in this repository should adhere to the "Gold Standard":

1. **Data Integrity & Safety**: **NEVER** delete, overwrite, or drop data (files, columns, or rows) without explicit
   user permission. Prefer creating new columns or files (e.g., `_processed.csv`) to preserve original data.
2. **No Silent Import Failures (CRITICAL)**: **NEVER** catch `ImportError` silently. Scripts must fail loudly if a 
   dependency is missing so the agent can see the error and install the required library.
3. **Resource Awareness**: Call `get-available-resources` for data-intensive tasks.
4. **Strict Idioms**: Enforce PEP-8 and modern library syntax (e.g., Pandas 2.0+, Pydantic V2).
5. **Reference Tiering**: Keep `SKILL.md` focused; move deep documentation to `references/`.
6. **Pitfalls Section**: Explicitly list common hallucinations or errors for OS models.

### Special Skills

- **`get-available-resources`**: Detects CPU/GPU/memory/disk info.
- **`python-best-practices`**: Enforces coding standards and tiered testing strategy.
- **`exploratory-data-analysis`**: Entry point for scientific file analysis.
