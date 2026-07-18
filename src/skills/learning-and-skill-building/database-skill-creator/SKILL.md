---
name: database-skill-creator
description: Use when the user wants to create a new skill to interact with a specific database (PostgreSQL, BigQuery, Snowflake, etc.) by extracting schemas and documenting business logic.
---

# Database Skill Creator

## Overview

This skill guides you through transforming a database's structure (schemas, tables, relationships) into a dedicated,
reusable Claude/Gemini skill. This allows the AI agent to fluently query and analyze data in that specific database in
future sessions.

## When to Use

- A user says "I have a new database I want to analyze."
- You need to build a specialized skill for a company-specific data warehouse.
- The user provides connection details and asks for a skill that "knows my data."

## Workflow

### Step 1: Discover the Environment

1. **Identify the Dialect and Version**: Determine if it's PostgreSQL, BigQuery, Snowflake, SQLite, DuckDB, an embedded
   graph DB, etc. Record the exact version string.
2. **Handle Credentials Safely**:
   - Ask the user for connection details and credentials.
   - If you must store them locally, use a `.env` file and ensure `.gitignore` excludes it.
   - Prefer environment variables in scripts: `os.environ["DB_PASSWORD"]`.
3. **Verify Connectivity**: Create a Python script called `scripts/connect.py` to connect to this database and verify it works.
   For embedded databases (e.g., DuckDB, Kùzu), this script should also confirm the package is installed/importable.

### Step 2: Initialize the New Skill

1. Use the `writing-skills` standards for the overall process.
2. Create the skill directory and `SKILL.md`:
   ```bash
   mkdir -p <destination-folder>/<skill-name>/scripts
   touch <destination-folder>/<skill-name>/SKILL.md
   ```

### Step 3: Extract Schemas, Context, and Domain Terms

1. **Introspect the catalog**: Run read-only queries appropriate to the dialect:
   - PostgreSQL / most SQL databases: `information_schema.tables`, `information_schema.columns`, `pg_catalog`.
   - SQLite: `PRAGMA table_info(...)`, `sqlite_master`.
   - BigQuery: `INFORMATION_SCHEMA.TABLES`, `INFORMATION_SCHEMA.COLUMNS`.
   - Embedded graph / NoSQL DBs: use the native catalog API.
   Save the results in `references/schemas.md`.
2. **Sample real rows**: For each user-facing table, run a `SELECT * LIMIT 5` (or dialect equivalent) and capture output in
   `references/schemas.md`. Real values reveal domain terminology and data-quality surprises. If the database has many
   tables, sample at least the ones that are not clearly system catalogs; document any groups you intentionally skip.
3. **Harvest domain terminology**: Create `references/glossary.md` with columns:
   - **Term** (column name, type, metric, acronym)
   - **Definition**
   - **Source** (schema query, doc URL, or sampled value)
   - **Real example** from the sample rows.
4. **Business Logic**: Ask the user about key terms and metrics (e.g., ARR calculation) and data hygiene (standard filters).
   Save this to `references/business-logic.md`. If no user is available, derive candidates from constraints, defaults,
   and column names, marking them as inferred.

### Step 4: Write the New SKILL.md

Follow the "Gold Standard" from `writing-skills`:

- **Frontmatter**: Clear "Use when..." description.
- **Mandatory Pre-flight**: Check for database connection and required environment variables.
- **Dialect Notes**: Document version-specific quirks (string concatenation, booleans, date functions, limits).
- **Query Idioms**: Provide optimized, dialect-specific query examples.
- **Domain Fundamentals**: Briefly explain the domain the database models and define the jargon.
- **Reference Pointers**: Point to `references/schemas.md`, `references/business-logic.md`, and `references/glossary.md`.

### Step 5: Smoke Test the Skill

Create `scripts/connect_and_sample.py` that:

1. Connects using the same pattern as `SKILL.md`.
2. Runs at least one introspection query and one sample query per user-facing table.
3. Prints row counts and a few sample values.
4. Runs without errors in the current environment.

The skill is **not finished** until `python scripts/connect_and_sample.py` passes.

### Step 6: Package and Install

1. Run `setup-data-skills` from this package to copy the new skill into `~/.claude/skills` and `.gemini/commands`.
2. In Claude Code, restart or run `/skills reload` if supported by your client.

## Interoperability

- **Tech Explorer**: Use `tech-explorer` to master the database structure before writing the skill.
- **Writing Skills**: Use for the TDD-based documentation process.
- **Testing Knowledge Skills**: Use `writing-skills/testing-knowledge-skills.md` for the fact-check harness and rubric.

## Anti-Patterns

- **Do NOT** include sensitive data or credentials.
- **Do NOT** skip tables just because they look obscure or low-value. Document the full user-facing surface unless the user
  explicitly asked for a subset.
- **Do NOT** forget to specify the SQL dialect and version.
- **Do NOT** rely on memory for dialect syntax; run the query and confirm it works.
- **Do NOT** mutate data during exploration. All exploration queries should be read-only unless the user explicitly
  requests a change.
