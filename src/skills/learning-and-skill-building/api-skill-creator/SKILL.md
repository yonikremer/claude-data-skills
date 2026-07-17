---
name: api-skill-creator
description: Use when the user wants to create a new skill to interact with an internal API, web service, or system using API documentation (URL, Wiki, Confluence, Swagger, etc.)
---

# API Skill Creator

## Overview

This skill guides you through transforming API documentation (whether from an internal wiki, Confluence, auto-generated
Swagger/OpenAPI docs, or raw text) into a dedicated, reusable Claude/Gemini skill. This allows the AI agent to fluently
interact with the specified internal or external API in future sessions.

## When to Use

- A user says "I have an internal API I want to make a skill for."
- A user provides a link to an API spec or documentation and asks you to "make a skill" for it.
- You need to build a specialized skill to encapsulate complex API authentication, base URLs, and endpoint definitions.

## Workflow

### Step 1: Discover and Master the API

1. **Locate Documentation**: Fetch via URL, wiki, or raw text.
2. **Mastery Phase**: If the API is unknown, complex, or poorly documented, **you MUST use `tech-explorer` first** to
   verify the endpoints and authentication work as described. Do not document an API you haven't successfully called.

### Step 2: Initialize the New Skill

1. Use the standards from `writing-skills` (TDD-based process).
2. Create the skill directory and `SKILL.md`:
   ```bash
   mkdir -p <destination-folder>/<skill-name>/scripts
   touch <destination-folder>/<skill-name>/SKILL.md
   ```

### Step 3: Extract and Synthesize

1. **API Reference**: Save request/response schemas and endpoints into `references/api-docs.md`.
2. **Authentication**: Instruct the agent to use environment variables (e.g., `$env:MY_API_KEY`).

### Step 4: Write the New SKILL.md

Follow the "Gold Standard" in `writing-skills`:

- **Frontmatter**: Concise "Use when..." description.
- **Mandatory Pre-flight**: Check for authentication and required environment variables.
- **Mastery Idioms**: Provide the most efficient, idiomatic examples (e.g., `curl` or Python `requests`).
- **Reference Pointers**: Point to `references/api-docs.md` for endpoint details.

### Step 5: Package and Install

1. Run `setup-data-skills` from this package to copy the new skill into `~/.claude/skills` and `.gemini/commands`.
2. In Claude Code, restart or run `/skills reload` if supported by your client.

## Interoperability

- **Tech Explorer**: Use to master and verify the API before documentation.
- **Writing Skills**: Use for the "Gold Standard" skill structure and TDD-based process.

## Anti-Patterns

- **Do NOT** hardcode API keys or credentials.
- **Do NOT** dump raw Swagger JSON into `SKILL.md`.
- **Do NOT** forget to specify the Base URL.