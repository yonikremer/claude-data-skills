---
name: tech-explorer
description: Use when encountering an unfamiliar database, library, or API. Researches, tests, and masters the technology to create a comprehensive SKILL.md guide based on empirical findings.
---

# Tech Explorer

## Overview

Transform "unknowns" into mastery by combining research, real usage artifacts, setup, and hands-on experimentation. Produce a "Gold Standard" skill that maps the technology's full potential, including empirical insights.

## When to Use

- A user asks about a technology you have never used.
- You need to evaluate whether a new library, database, or API fits a use case.
- You are about to create a skill for a technology and need to verify claims before documenting them.

## Workflow

### Step 1: Research & Blueprinting

- **Find the source of truth**: official docs, canonical GitHub repo, package index (PyPI/npm/crates), and recent release notes / changelog. Prefer `https://` endpoints from the project itself.
- **Inspect library source code**: Since you always have access to the target library's installed codebase (e.g., in `site-packages` or local copy), check internal class/function definitions, inline comments, and docstrings directly when official docs are sparse or ambiguous.
- **Harvest domain terminology**: technologies that look simple often hide a vocabulary problem. Create `references/glossary.md` with the columns:
  - **Term**
  - **Definition**
  - **Where you found it** (doc URL, schema field, or query output)
  - **Real example** (a value or snippet observed in an actual response/query result)
  Do not invent definitions from memory; every term must trace to a source.
- **Build a recon plan**: pick the checklist below that matches the technology type.
  - **API / Web service**: locate OpenAPI/Swagger/WSDL/Postman collections; enumerate base URL(s), auth scheme, rate limits, pagination style, error envelope, required vs optional query params; **list every public endpoint in the spec/docs**, not just the most common ones. Group endpoints by functional area if the surface is large.
  - **Database**: identify dialect/version; list every catalog/schema; run introspection queries; **sample every user-facing table**; capture data types, constraints, indexes, and any domain-specific types/enums.
  - **Library / package**: identify the minimal install; list top-level modules/classes; run the version/import smoke test; exercise the "happy path" and one edge case per **every documented public function/class**, not just the showcase examples.
- **Coverage decisions**: If you intentionally skip deprecated, internal, or unsafe endpoints/tables/functions, record the reason in the evidence ledger. The default is full coverage; a subset is only acceptable when the user explicitly asked for one or when probing would mutate production data.
- **Start an evidence ledger**: `references/evidence-ledger.md` records every claim you intend to put in the final skill. Format: `Claim | Source | Verified by (command/URL/output) | Status (verified/unverified)`. If you cannot verify a claim, mark it `UNVERIFIED` and do not present it as fact in `SKILL.md`.

### Step 2: Harvest Existing Usage Artifacts

Existing code, configs, logs, and notebooks encode real usage patterns, edge cases, and domain language that official docs often omit. Ask the user for or search the repository for:

- **Repository source code**: Search the codebase for imports, dependencies, custom wrappers, configurations, or unit tests — reveals existing integrations, helper functions, and local project conventions.
- **API / web service**: client SDK code, Postman collections, API logs/traces, integration tests, frontend callers — reveals idiomatic usage, auth patterns, real headers, and error patterns.
- **Library / package**: example code, test suites, GitHub issues, tutorials, Stack Overflow threads — reveals idiomatic calls, edge cases, common pitfalls, and version quirks.
- **Database**: saved queries, dbt models, stored procedures, BI reports, query logs, notebooks — reveals business logic, join paths, performance gotchas, and domain terminology.

Capture valuable snippets in `references/usage-artifacts.md` with attribution and purpose. Then feed them into the skill:

- **Domain logic** → `references/business-logic.md` (workflows, state machines, validation rules).
- **Domain terms** → `references/glossary.md` (acronyms, status values, field names, real examples).
- **Patterns / idioms** → `SKILL.md` (canonical usage, common call sequences).
- **Smoke tests** → `scripts/smoke_test.py` (verified working examples).
- **Wall of Shame** → `SKILL.md` (fragile patterns, common errors, deprecated paths).

### Step 3: Setup & Installation

A solid foundation is required before exploration.

- **Environment Preparation**: Identify and install required system dependencies (e.g., CUDA, specific runtimes, CLI tools).
- **Dependency Verification**: Rigorously check for version mismatches or missing components.
- **Automated Fixes**: Attempt to resolve installation issues using available tools (e.g., `pip`, `winget`, `npm`).
- **Sub-Agent Debugging**: If installation fails or becomes complex, spawn a focused sub-agent to isolate the root cause (environment, dependency version, missing system library) before proceeding.
- **Verification**: Run a minimal "version check" or "smoke test" to confirm the environment is ready.

### Step 4: Empirical Testing (The Mastery Phase)

You MUST NOT document a technology until you have successfully used it and explored its full potential.

- **Comprehensive Mapping**: Do not stop at "Hello World". Systematically test all public endpoints/functional areas for an API/library and all user-facing tables for a database.
- **Understanding**: What problems does the technology solve? What are the key domain use cases? What are its limitations?
- **Code Inspection**: Read implementation code of library modules to trace private helpers, default arguments, exception triggers, and undocumented options.
- **Domain Fundamentals**: For each major module or functional area, document the "Why" and "What" of the underlying domain concepts (e.g., "What is a Butterworth filter?", "What is the physical meaning of a Spectrogram?").
- **Scaffolding**: Create temporary test scripts (e.g., `test_api_explorer.py`) to exercise the breadth of the technology. Keep raw responses/query results in `references/`, not in `SKILL.md`.
- **Stress Testing**: Try edge cases (e.g., large payloads, invalid inputs, network timeouts, resource limits).
- **Pitfall Discovery**: Document exactly what failed, why it was confusing, and how you fixed it. These become your "Wall of Shame" entries.

### Step 5: Documentation (The Gold Standard)

Once mastery is achieved, translate the knowledge into a permanent skill.

- **Core Guidelines**: Strictly follow the standards in `writing-skills` for the TDD-based documentation process.
- **Section: Domain Fundamentals**: Every "Gold Standard" skill MUST include a section explaining the basics of the domain (e.g., "What is a filter?", "What is FFT?") and how they relate to the tool's usage.
- **Section: Glossary**: Surface the most important terms from `references/glossary.md` in `SKILL.md` so an agent reading only the skill can understand the jargon.
- **Specialized Creators**: Delegate to these if appropriate:
    - Use `api-skill-creator` for web/system APIs.
    - Use `database-skill-creator` for SQL/NoSQL databases.
- **General Skills**: Use the base `writing-skills` process for libraries and general tools.

## Required Deliverables

Before declaring mastery, ensure these artifacts exist:

1. `SKILL.md` with correct frontmatter and a domain-fundamentals section.
2. `references/tech-specs.md` — base URL/version, auth, core concepts, and a complete list of endpoints/classes/tables with coverage notes.
3. `references/glossary.md` — terminology with definitions, sources, and real examples.
4. `references/business-logic.md` — workflows, rules, and domain logic inferred from usage artifacts.
5. `references/usage-artifacts.md` — existing code, configs, logs, or queries with attribution.
6. `references/evidence-ledger.md` — claim-to-source mapping; ideally no `UNVERIFIED` items.
7. `scripts/smoke_test.py` (or equivalent) that runs against the real technology and asserts expected behavior.

## Interoperability

- **Writing Skills**: Provides the "Gold Standard" for skill structure and the Red/Green/Refactor writing process.
- **Testing Knowledge Skills**: Use `writing-skills/testing-knowledge-skills.md` for the fact-check harness and rubric.
- **API Skill Creator**: Specialized path for mapping API documentation to skills.
- **Database Skill Creator**: Specialized path for mapping database structures to skills.
- **Debugging**: Use a focused sub-agent or your standard debugging workflow for installation and setup failures.

## Iteration

If a user reports a bug or a missing feature in a skill you created, re-enter the **Mastery Phase** to expand the documentation and update the "Wall of Shame".

## Anti-Patterns

- **Do NOT** ignore existing usage artifacts; they often reveal the real patterns and pitfalls official docs omit.
- **Do NOT** ignore the repository's own source code; it often contains wrapper classes, database models, or utility functions that show how the technology is already used.
- **Do NOT** treat the library as a black box; inspect its source code, internal docstrings, and module structures directly.
- **Do NOT** document a technology you haven't successfully exercised.
- **Do NOT** present unverified claims as fact in `SKILL.md`.
- **Do NOT** dump raw artifacts or full response bodies into `SKILL.md`; keep them in `references/`.
- **Do NOT** skip the evidence ledger for claims you intend to document.
- **Do NOT** mutate production data during exploration unless the user explicitly approved it.
