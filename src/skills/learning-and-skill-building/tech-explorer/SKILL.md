---
name: tech-explorer
description: Use when encountering an unfamiliar database, library, or API. Researches, tests, and masters the technology to create a comprehensive SKILL.md guide based on empirical findings.
---

# Tech Explorer

## Overview
The Tech Explorer guide transforms "unknowns" into "mastery" by combining deep research, systematic setup, and exhaustive hands-on experimentation. The goal is to produce a "Gold Standard" skill that maps the *entire* potential of the new technology, including hard-won empirical insights.

## Workflow

### 1. Research & Blueprinting
- **Search**: Use `google_web_search` and `web_fetch` to find official documentation, GitHub repos, and recent tutorials.
- **Synthesize**: Create a `references/tech-specs.md` with the base URL, authentication methods, core concepts, and key API endpoints/classes.
- **Scope Definition**: Identify the full extent of the technology (e.g., all major modules, API endpoints, or database tables) to ensure comprehensive exploration.

### 2. Setup & Installation
A solid foundation is required before exploration.
- **Environment Preparation**: Identify and install required system dependencies (e.g., CUDA, specific runtimes, CLI tools).
- **Dependency Verification**: Rigorously check for version mismatches or missing components.
- **Automated Fixes**: Attempt to resolve installation issues using available tools (e.g., `pip`, `winget`, `npm`).
- **Sub-Agent Debugging**: If installation fails or becomes complex, **you MUST use a specialized debugging sub-agent** (e.g., `systematic-debugging`) to identify and resolve root causes.
- **Verification**: Run a minimal "version check" or "smoke test" to confirm the environment is ready.

### 3. Empirical Testing (The Mastery Phase)
You MUST NOT document a technology until you have successfully used it and explored its full potential.
- **Comprehensive Mapping**: Do not stop at "Hello World". You must systematically test all major functional areas for an API/library and all tables for a database.
- **Understanding**: What problems does the technology solve? What are the key use cases? What are its limitations?
- **Scaffolding**: Create temporary test scripts (e.g., `test_api_explorer.py`) to exercise the breadth of the technology.
- **Stress Testing**: Try edge cases (e.g., large payloads, invalid inputs, network timeouts, resource limits).
- **Pitfall Discovery**: Document exactly what failed, why it was confusing, and how you fixed it. These become your "Wall of Shame" entries.

### 4. Documentation (The Gold Standard)
Once mastery is achieved, translate the knowledge into a permanent skill.
- **Core Guidelines**: Strictly follow the standards in `writing-skills` for the TDD-based documentation process.
- **Specialized Creators**: Delegate to these if appropriate:
    - Use `api-skill-creator` for web/system APIs.
    - Use `database-skill-creator` for SQL/NoSQL databases.
- **General Skills**: Use the base `writing-skills` process for libraries and general tools.

## Interoperability
- **Writing Skills**: Provides the "Gold Standard" for skill structure and the Red/Green/Refactor writing process.
- **API Skill Creator**: Specialized path for mapping API documentation to skills.
- **Database Skill Creator**: Specialized path for mapping database structures to skills.
- **Systematic Debugging**: Use for troubleshooting installation and setup failures.

## Iteration
If a user reports a bug or a missing feature in a skill you created, re-enter the **Mastery Phase** to expand the documentation and update the "Wall of Shame".
