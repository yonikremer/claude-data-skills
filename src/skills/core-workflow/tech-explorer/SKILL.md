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
- **Scope Definition**: Identify the full extent of the technology (e.g., all major modules, API endpoints, or database features) to ensure comprehensive exploration.

### 2. Setup & Installation
A solid foundation is required before exploration.
- **Environment Preparation**: Identify and install required system dependencies (e.g., CUDA, specific runtimes, CLI tools).
- **Dependency Verification**: Rigorously check for version mismatches or missing components.
- **Automated Fixes**: Attempt to resolve installation issues using available tools (e.g., `pip`, `winget`, `npm`).
- **Sub-Agent Debugging**: If installation fails or becomes complex, **you MUST use a specialized debugging sub-agent** (e.g., `systematic-debugging`) to identify and resolve root causes.
- **Verification**: Run a minimal "version check" or "smoke test" to confirm the environment is ready.

### 3. Empirical Testing (The Mastery Phase)
You MUST NOT document a technology until you have successfully used it and explored its full potential.
- **Comprehensive API/Database Mapping**: Do not stop at "Hello World". You must systematically test all major functional areas (e.g., Linalg, FFT, Sparse, Random, Interoperability for a numerical library).
- **Scaffolding**: Create temporary test scripts (e.g., `test_api_explorer.py`) to exercise the breadth of the technology.
- **Stress Testing**: Try edge cases (e.g., large payloads, invalid inputs, network timeouts, resource limits).
- **Pitfall Discovery**: Document exactly what failed, why it was confusing, and how you fixed it. These become your "Wall of Shame" entries.

### 4. Documentation (The Gold Standard)
Create the final `SKILL.md` and optional `references/` in a new skill folder. 
Every skill must include:
- **Discovery Frontmatter**: A high-quality "Use when..." description.
- **Mandatory Pre-flight**: Explicit checks for environment variables, dependencies, or system resources.
- **Comprehensive API Guide**: Detailed sections for all major functional areas, not just the basics.
- **Mastery Idioms**: The most efficient, idiomatic, and performance-conscious ways to use the technology based on your testing.
- **The Wall of Shame**: A categorized list of common errors, misleading messages, and anti-patterns discovered during Step 2 and 3.
- **Ready-to-Run Examples**: Verified code snippets for all major use cases.

## Skill Standards
- **Exhaustive Coverage**: Document the technology's full potential, not just what was needed for the immediate task.
- **Conciseness**: Avoid fluff; focus on high-density procedural knowledge.
- **Security**: Never hardcode credentials; always use environment variables.
- **Resource Awareness**: Include checks for memory/CPU/GPU if the technology handles large data.

## Iteration
If a user reports a bug or a missing feature in a skill you created, re-enter the **Mastery Phase** to expand the documentation and update the "Wall of Shame".
