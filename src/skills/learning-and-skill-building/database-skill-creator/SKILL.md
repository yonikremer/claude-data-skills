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

1. **Identify the Dialect**: Determine if it's PostgreSQL, BigQuery, Snowflake, etc.
2. **Ask for credentials**: and save them in a .env file
3. **Verify Connectivity**: Make a Python script called connect.py to connect tot this db. make sure iot works.

### Step 2: Initialize the New Skill

1. Use the `writing-skills` standards for the overall process.
2. Run the skill initialization script:
   ```bash
   node <path-to-skill-creator>/scripts/init_skill.cjs <skill-name> --path <destination-folder>
   ```

### Step 3: Extract Schemas and Context

1. **Schemas**: Go over each human-generated schema and describe it. Ignore auto-generated tables and schemas that exists in every oracle DB.
2. **Table Documentation**: Save schema details (columns, types, foreign keys) into `references/schemas.md`.
3. **Business Logic**: Ask the user about key terms and metrics (e.g., ARR calculation) and data hygiene (standard filters). Save this to `references/business-logic.md`.

### Step 4: Write the New SKILL.md

Follow the "Gold Standard" from `writing-skills`:

- **Frontmatter**: Clear "Use when..." description.
- **Mandatory Pre-flight**: Check for database connection and required environment variables.
- **Query Idioms**: Provide optimized, dialect-specific query examples.
- **Reference Pointers**: Point to `references/schemas.md` and `references/business-logic.md`.

### Step 5: Package and Install

1. Package the skill: `node <path-to-skill-creator>/scripts/package_skill.cjs <path/to/skill-folder>`
2. Install: `gemini skills install <path/to/skill-name.skill> --scope workspace`
3. Inform the user to run `/skills reload`.

## Interoperability

- **Tech Explorer**: Use `tech-explorer` to master the database structure before writing the skill.
- **Writing Skills**: Use `writing-skills` for the TDD-based documentation process.

## Anti-Patterns

- **Do NOT** include sensitive data or credentials.
- **Do NOT** document every single table; focus on the most valuable domains first.
- **Do NOT** forget to specify the SQL dialect.
