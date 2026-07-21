---
name: api-skill-creator
description: Use when the user wants to create a new skill to interact with an internal API, web service, or system using API documentation (URL, Wiki, Confluence, Swagger, etc.)
---

# API Skill Creator

## Overview

Transform API documentation and real usage artifacts into a dedicated, reusable skill so agents can interact with the API fluently.

## When to Use

- A user says "I have an internal API I want to make a skill for."
- A user provides a link to an API spec or documentation and asks you to "make a skill" for it.
- You need to build a specialized skill to encapsulate complex API authentication, base URLs, and endpoint definitions.

## Workflow

### Step 1: Discover and Verify the API

1. **Locate canonical documentation**: Use web search/fetch to find the official docs, OpenAPI/Swagger JSON, or Postman collection. Treat anything older than the latest release notes with suspicion.
2. **Mastery Phase**: If the API is unknown, complex, or poorly documented, **you MUST use `tech-explorer` first** to verify the endpoints and authentication work as described. Do not document an API you haven't successfully called.
3. **Build an Endpoint Verification Matrix** in `references/api-docs.md`:

   | Method | Path | Purpose | Required params | Verified? | HTTP status of probe | Notes |
   |---|---|---|---|---|---|---|
   | GET | `/v1/foo` | ... | ... | ✅ | 200 | ... |

   **List every public endpoint from the spec/docs in the matrix**, grouped by functional area if needed. Probe every endpoint you can safely exercise; for endpoints that cannot be probed (e.g., they mutate state or require privileged credentials), mark them `UNVERIFIED` but still document them. Capture a *small* sample response in `references/` for each verified endpoint.
4. **Harvest domain terms**: APIs often hide a private language in query params and response fields. Build `references/glossary.md` listing term, definition, source URL, and a real example value from a probe response.

### Step 2: Initialize the New Skill

1. Use the standards from `writing-skills` (TDD-based process).
2. Create the skill directory and `SKILL.md`:
   ```bash
   mkdir -p <destination-folder>/<skill-name>/scripts
   touch <destination-folder>/<skill-name>/SKILL.md
   ```

### Step 3: Extract and Synthesize

1. **API Reference**: Save request/response schemas and endpoints into `references/api-docs.md`. Include:
   - Base URL(s) and environment differences.
   - Authentication method and required environment variables.
   - Rate limits, pagination style, and error envelope.
   - Endpoint table (from Step 1) and sample responses.
2. **Glossary**: Promote the most important terms into `SKILL.md` itself; keep the full glossary in `references/glossary.md`.
3. **Authentication**: Instruct the agent to use environment variables (e.g., `$env:MY_API_KEY` on Windows, `${MY_API_KEY}` on Unix). Never hardcode keys.

### Step 4: Harvest Existing API Usage

Existing client code, integration tests, API logs, and frontend callers encode real usage patterns, auth edge cases, and domain language that specs alone do not reveal. Ask the user for SDK examples, Postman collections, API logs/traces, incident reports, or code that calls the API.

For each source, extract:

- **SDK / client code**: idiomatic usage, auth patterns, retry logic, required headers.
- **Integration tests**: expected request/response shapes, edge cases, required fields.
- **API logs / traces**: real headers, common errors, latency gotchas, rate-limit hits.
- **Frontend / mobile code**: domain terminology, user-facing names for fields, valid value ranges.
- **Incident reports / runbooks**: fragile endpoints, known workarounds, deprecated paths.

Capture valuable examples in `references/usage-artifacts.md` with attribution and purpose. Then feed them into the skill:

- **Domain logic** → `references/business-logic.md` (workflows, state machines, validation rules).
- **Domain terms** → `references/glossary.md` (acronyms, header names, status values, real examples).
- **Mastery idioms** → `SKILL.md` (canonical request patterns, auth flows, pagination loops).
- **Smoke tests** → `scripts/smoke_test.py` (verified working calls).
- **Wall of Shame** → `SKILL.md` (rate-limit surprises, required headers, fields that look optional but aren't).

### Step 5: Write the New SKILL.md

Follow the "Gold Standard" in `writing-skills`:

- **Frontmatter**: Concise "Use when..." description.
- **Mandatory Pre-flight**: Check for authentication and required environment variables.
- **Base URL + Auth**: State them before any endpoint examples.
- **Mastery Idioms**: Provide the most efficient, idiomatic examples (e.g., `curl` or Python `requests`). Include at least one minimal example and one realistic multi-step example.
- **Domain Fundamentals**: Briefly explain what problem the API solves and define the jargon an outsider would not know.
- **Wall of Shame**: Document pitfalls you discovered empirically (rate-limit surprises, required headers, pagination quirks, fields that look optional but aren't).
- **Reference Pointers**: Point to `references/api-docs.md`, `references/glossary.md`, `references/business-logic.md`, and `references/usage-artifacts.md` for deep details.

### Step 6: Smoke Test the Skill

Create `scripts/smoke_test.py` that:

1. Imports or implements the minimal examples from `SKILL.md`.
2. Exercises at least one endpoint per functional group; aim to touch every public endpoint that can be safely probed.
3. Asserts that the response contains expected keys/status codes.
4. Runs without errors in the current environment.

The skill is **not finished** until `python scripts/smoke_test.py` passes.

### Step 7: Package and Install

1. Run `setup-data-skills` from this package to copy the new skill into `~/.claude/skills` and `.gemini/commands`.
2. In Claude Code, restart or run `/skills reload` if supported by your client.

## Interoperability

- **Tech Explorer**: Use to master and verify the API before documentation.
- **Writing Skills**: Use for the "Gold Standard" skill structure and TDD-based process.
- **Testing Knowledge Skills**: Use `writing-skills/testing-knowledge-skills.md` for the fact-check harness and rubric.

## Anti-Patterns

- **Do NOT** hardcode API keys or credentials.
- **Do NOT** dump raw Swagger JSON into `SKILL.md`.
- **Do NOT** forget to specify the Base URL.
- **Do NOT** silently drop endpoints because they look obscure or uncommon. If you cannot probe an endpoint, mark it `UNVERIFIED` in `references/api-docs.md` and omit it from `SKILL.md`.
- **Do NOT** truncate the API surface to the "most important" endpoints unless the user explicitly asked for a subset.
- **Do NOT** ignore existing client code, tests, or API logs; they often reveal the real usage patterns and pitfalls.
- **Do NOT** rely on training-data memory for current endpoint behavior; fetch the live docs or probe the endpoint.
