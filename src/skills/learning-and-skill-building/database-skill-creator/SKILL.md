---
name: database-skill-creator
description: Use when the user wants to create a new skill to interact with Oracle, Elasticsearch, or PostgreSQL databases by extracting schemas and documenting business logic.
---

# Database Skill Creator

## Overview

Build reusable skills for Oracle, Elasticsearch, or PostgreSQL.

## When to Use

- A user says "I have a new database I want to analyze."
- You need a specialized skill for a company-specific Oracle, Elasticsearch, or PostgreSQL data store.
- The user provides connection details and asks for a skill that "knows my data."

## Workflow

### Step 1: Discover the Environment

1. **Identify the dialect and version**:
   - PostgreSQL: `SELECT version();`
   - Oracle: `SELECT * FROM v$version;`
   - Elasticsearch: `GET /`
2. **Handle credentials safely**: ask for connection details; store in `.env` if needed and gitignore it. Prefer `os.environ[...]`.
3. **Verify connectivity** with `scripts/connect.py`:
   - PostgreSQL: `psycopg` / `psycopg2`
   - Oracle: `oracledb` (preferred) or `cx_Oracle`
   - Elasticsearch: `elasticsearch` Python client

### Step 2: Initialize the New Skill

1. Use the `writing-skills` standards.
2. Create the skill directory and `SKILL.md`:
   ```bash
   mkdir -p <destination-folder>/<skill-name>/scripts
   touch <destination-folder>/<skill-name>/SKILL.md
   ```

### Step 3: Extract Schemas, Context, and Domain Terms

1. **Introspect the catalog** (read-only):
   - **PostgreSQL**: `information_schema.tables`, `information_schema.columns`, `pg_catalog`.
   - **Oracle**: `ALL_TABLES`, `ALL_TAB_COLUMNS`, `ALL_CONSTRAINTS`, `ALL_INDEXES`.
   - **Elasticsearch**: `GET /_cat/indices`, `GET /<index>/_mapping`, `GET /<index>/_settings`.
   Save results in `references/schemas.md`.
2. **Sample real rows**:
   - PostgreSQL: `SELECT * FROM <table> LIMIT 5`
   - Oracle 12c+: `SELECT * FROM <table> FETCH FIRST 5 ROWS ONLY`; legacy: `WHERE ROWNUM <= 5`
   - Elasticsearch: `GET /<index>/_search { "size": 5 }`
   Capture output in `references/schemas.md`.
3. **Document domain terms and business logic** in `references/glossary.md` and `references/business-logic.md`. Mark inferred items as inferred.

### Step 4: Harvest Existing Queries and Reports

Existing queries encode business logic, relationships, and domain language that schemas alone do not reveal. Ask the user for saved reports, BI queries, dbt models, stored procedures, notebooks, or query logs.

For each source, extract:

- **Saved reports / BI queries**: common filters, date ranges, status logic, KPI calculations.
- **dbt models / stored procedures**: reusable transformations, derived tables, business definitions.
- **Query logs / slow-query log**: hot paths, expensive joins, performance gotchas.
- **Notebooks / ad-hoc SQL**: domain acronyms, aliases, recurring metrics.

Capture valuable queries in `references/queries.md` with attribution and purpose. Then feed them into the skill:

- **Business logic** → `references/business-logic.md` (rules, standard filters, calculations).
- **Domain terms** → `references/glossary.md` (acronyms, aliases, status codes, real examples).
- **Query idioms** → `SKILL.md` (canonical joins, standard filters, common aggregations).
- **Smoke tests** → `scripts/connect_and_sample.py` (verified working queries).
- **Anti-patterns** → `SKILL.md` (slow, fragile, or deprecated patterns to avoid).

### Step 5: Write the New SKILL.md

Follow the `writing-skills` Gold Standard:

- **Frontmatter**: clear "Use when..." description.
- **Mandatory Pre-flight**: check connection and required environment variables.
- **Dialect Notes**:
  - **PostgreSQL**: `||` concatenation, `LIMIT`.
  - **Oracle**: uppercase identifiers unless quoted; `FETCH FIRST` (12c+) or `ROWNUM`; `NVL`/`COALESCE`; no `LIMIT`.
  - **Elasticsearch**: no joins; query DSL (`bool`, `match`, `term`); aggregations replace `GROUP BY`; mappings set analyzers and types.
- **Query Idioms**: dialect-specific, optimized examples.
- **Domain Fundamentals**: briefly explain the modeled domain and jargon.
- **Reference Pointers**: point to `references/schemas.md`, `references/business-logic.md`, `references/glossary.md`, and `references/queries.md`.

### Step 6: Smoke Test the Skill

Create `scripts/connect_and_sample.py` that:

1. Connects using the same pattern as `SKILL.md`.
2. Runs introspection and sample queries for each user-facing table/index.
3. Prints counts and a few sample values.
4. Runs without errors in the current environment.

The skill is **not finished** until `python scripts/connect_and_sample.py` passes.

### Step 7: Package and Install

1. Run `setup-data-skills` to copy the new skill into `~/.claude/skills` and `.gemini/commands`.
2. Restart Claude Code or run `/skills reload`.

## Interoperability

- **Tech Explorer**: Use `tech-explorer` to master the database structure before writing the skill.
- **Writing Skills**: Use for the TDD-based documentation process.

## Anti-Patterns

- Do NOT include sensitive data or credentials.
- Do NOT skip user-facing tables/indexes. Document the full surface unless the user asks for a subset.
- Do NOT assume Elasticsearch behaves like SQL (no joins, no ad-hoc schema changes).
- Do NOT quote PostgreSQL identifiers incorrectly: unquoted names are lowercased, so `MyTable` and `mytable` are different objects.
- Do NOT assume Oracle `ALL_*` views are scoped to the current user; use `USER_*` views when you only want the current schema.
- Do NOT ignore existing queries; they often contain the real business logic and domain language.
- Do NOT rely on memory for dialect syntax; run the query and confirm it works.
- Do NOT mutate data during exploration unless explicitly requested.
