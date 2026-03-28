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
| **Clean/Transform data**  | `data-analysis-pro`, `python-core-pro`                   |
| **Visualize data**        | `visualization-pro`, `scientific-visualization`           |
| **Train/Evaluate ML**     | `ml-classical`, `ml-deep-learning`, `timesfm-forecasting` |
| **Write/Optimize SQL**    | `database-pro`                                             |
| **Build a UI/Dashboard**  | `visualization-pro`                                        |
| **Parallel Processing**   | `python-core-pro`                                          |
| **Verify code quality**   | `python-core-pro`                                          |
| **Manage version control** | `git`                                                      |
| **Process audio/video**   | `ffmpeg`                                                   |
| **Repair corrupted data** | `bit-error-correction`                                     |
| **Create new skills**     | `skill-engineering`                                        |
| **Summarize research**    | `scientific-research-suite`                                |
| **Manage dictionary**     | `dictionary-agent`                                         |
| **Handle specific files** | `document-processing-pro`, `binary-data-parsing`           |


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

## Slash Commands (Out-of-the-Box)

The following commands are available as high-level shortcuts for common data tasks. When a user invokes these, skip the planning phase and immediately trigger the corresponding skill:

- **`/analyze <file>`**: Immediately trigger the `exploratory-data-analysis` skill on the specified file. Perform grain detection, structure analysis, and nullity checks.
- **`/plot <type> <file>`**: Immediately trigger the `visualization-pro` skill to create the requested plot type for the dataset. Prefer Plotly for interactivity.
- **`/query <task>`**: Immediately trigger the `database-pro` skill to write, optimize, or explain a SQL query or database operation.
- **`/model <target> <file>`**: Immediately trigger the `ml-classical` skill to suggest a preprocessing pipeline and baseline model for the target variable.
- **`/forecast <col> <file>`**: Immediately trigger the `timesfm-forecasting` skill to perform a zero-shot forecast on the specified time-series column.
- **`/explore <technology>`**: Immediately trigger the `tech-explorer` skill to research, test, and master an unfamiliar database, library, or API.
- **`/define <term>`**: Immediately trigger the `dictionary-agent` skill to lookup a technical term or acronym in the domain dictionary.
