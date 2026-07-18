---
name: tech-explorer
description: Use when encountering an unfamiliar database, library, or API. Researches, tests, and masters the technology to create a comprehensive SKILL.md guide based on empirical findings.
---

# Tech Explorer

## Overview

The Tech Explorer guide transforms "unknowns" into "mastery" by combining deep research, systematic setup, and
exhaustive hands-on experimentation. The goal is to produce a "Gold Standard" skill that maps the *entire* potential of
the new technology, including hard-won empirical insights.

## When to Use

- A user asks about a technology you have never used.
- You need to evaluate whether a new library, database, or API fits a use case.
- You are about to create a skill for a technology and need to verify claims before documenting them.

## Workflow

### 1. Research & Blueprinting

- **Find the source of truth**: official docs, canonical GitHub repo, package index (PyPI/npm/crates), and a recent release notes / changelog. Prefer `https://` endpoints from the project itself.
- **Harvest domain terminology**: technologies that look simple often hide a vocabulary problem. Create
  `references/glossary.md` with the columns:
  - **Term**
  - **Definition**
  - **Where you found it** (doc URL, schema field, or query output)
  - **Real example** (a value or snippet observed in an actual response/query result)
  Do not invent definitions from memory; every term must trace to a source.
- **Build a recon plan**: pick the checklist below that matches the technology type.
  - **API / Web service**: locate OpenAPI/Swagger/WSDL/Postman collections; enumerate base URL(s), auth scheme, rate limits,
    pagination style, error envelope, required vs optional query params; **list every public endpoint in the spec/docs**,
    not just the most common ones. Group endpoints by functional area if the surface is large.
  - **Database**: identify dialect/version; list every catalog/schema; run introspection queries; **sample every user-facing
    table**; capture data types, constraints, indexes, and any domain-specific types/enums.
  - **Library / package**: identify the minimal install; list top-level modules/classes; run the version/import smoke test;
    exercise the "happy path" and one edge case per **every documented public function/class**, not just the showcase examples.
- **Coverage decisions**: If you intentionally skip deprecated, internal, or unsafe endpoints/tables/functions, record the
  reason in the evidence ledger. The default is full coverage; a subset is only acceptable when the user explicitly asked
  for one or when probing would mutate production data.
- **Start an evidence ledger**: `references/evidence-ledger.md` records every claim you intend to put in the final skill.
  Format: `Claim | Source | Verified by (command/URL/output) | Status (verified/unverified)`. If you cannot verify a claim,
  mark it `UNVERIFIED` and do not present it as fact in `SKILL.md`.

### 2. Setup & Installation

A solid foundation is required before exploration.

- **Environment Preparation**: Identify and install required system dependencies (e.g., CUDA, specific runtimes, CLI tools).
- **Dependency Verification**: Rigorously check for version mismatches or missing components.
- **Automated Fixes**: Attempt to resolve installation issues using available tools (e.g., `pip`, `winget`, `npm`).
- **Sub-Agent Debugging**: If installation fails or becomes complex, spawn a focused sub-agent to isolate the root cause
  (environment, dependency version, missing system library) before proceeding.
- **Verification**: Run a minimal "version check" or "smoke test" to confirm the environment is ready.

### 3. Empirical Testing (The Mastery Phase)

You MUST NOT document a technology until you have successfully used it and explored its full potential.

- **Comprehensive Mapping**: Do not stop at "Hello World". Systematically test all public endpoints/functional areas for an
  API/library and all user-facing tables for a database.
- **Understanding**: What problems does the technology solve? What are the key domain use cases? What are its limitations?
- **Domain Fundamentals**: For each major module or functional area, document the "Why" and "What" of the underlying domain
  concepts (e.g., "What is a Butterworth filter?", "What is the physical meaning of a Spectrogram?").
- **Scaffolding**: Create temporary test scripts (e.g., `test_api_explorer.py`) to exercise the breadth of the technology.
  Keep raw responses/query results in `references/`, not in `SKILL.md`.
- **Stress Testing**: Try edge cases (e.g., large payloads, invalid inputs, network timeouts, resource limits).
- **Pitfall Discovery**: Document exactly what failed, why it was confusing, and how you fixed it. These become your
  "Wall of Shame" entries.

### 4. Documentation (The Gold Standard)

Once mastery is achieved, translate the knowledge into a permanent skill.

- **Core Guidelines**: Strictly follow the standards in `writing-skills` for the TDD-based documentation process.
- **Section: Domain Fundamentals**: Every "Gold Standard" skill MUST include a section explaining the basics of the domain
  (e.g., "What is a filter?", "What is FFT?") and how they relate to the tool's usage.
- **Section: Glossary**: Surface the most important terms from `references/glossary.md` in `SKILL.md` so an agent reading
  only the skill can understand the jargon.
- **Specialized Creators**: Delegate to these if appropriate:
    - Use `api-skill-creator` for web/system APIs.
    - Use `database-skill-creator` for SQL/NoSQL databases.
- **General Skills**: Use the base `writing-skills` process for libraries and general tools.

## Required Deliverables

Before declaring mastery, ensure these artifacts exist:

1. `SKILL.md` with correct frontmatter and a domain-fundamentals section.
2. `references/tech-specs.md` — base URL/version, auth, core concepts, and a complete list of endpoints/classes/tables with coverage notes.
3. `references/glossary.md` — terminology with definitions, sources, and real examples.
4. `references/evidence-ledger.md` — claim-to-source mapping; ideally no `UNVERIFIED` items.
5. `scripts/smoke_test.py` (or equivalent) that runs against the real technology and asserts expected behavior.

## Interoperability

- **Writing Skills**: Provides the "Gold Standard" for skill structure and the Red/Green/Refactor writing process.
- **API Skill Creator**: Specialized path for mapping API documentation to skills.
- **Database Skill Creator**: Specialized path for mapping database structures to skills.
- **Debugging**: Use a focused sub-agent or your standard debugging workflow for installation and setup failures.

## Iteration

If a user reports a bug or a missing feature in a skill you created, re-enter the **Mastery Phase** to expand the
documentation and update the "Wall of Shame".
