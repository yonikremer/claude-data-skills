# Testing Knowledge Skills

**Load this reference when:** creating or editing a skill that teaches an agent how to use a real API, database, library,
or dataset. Use it to verify the skill is factually correct and operationally useful.

## Overview

Discipline-enforcing skills (TDD, security) are tested with *pressure scenarios* (see `testing-skills-with-subagents.md`).
Knowledge skills are tested with a *fact-check harness*: the skill is only as good as the claims it makes about a real
piece of technology.

## Test Checklist

Run through this checklist before claiming a knowledge skill is finished.

### 1. Structure and Format

- [ ] `SKILL.md` exists at `<skill-name>/SKILL.md`.
- [ ] YAML frontmatter has `name` (hyphen-case) and a single-line `description` starting with "Use when...".
- [ ] Body has a "Mandatory Pre-flight" section.
- [ ] Body has a "Domain Fundamentals" or "Overview" that explains what the technology is for.
- [ ] Body has a "Wall of Shame" / pitfalls section.
- [ ] `references/` directory exists with at least `api-docs.md`, `schemas.md`, or `tech-specs.md`.
- [ ] `scripts/` directory exists with a runnable smoke test.

### 2. Glossary Quality

- [ ] `references/glossary.md` exists with at least 5 domain terms.
- [ ] Each term has a definition, a source (doc URL / schema field / query output), and a real example from live data.
- [ ] No term is invented from memory without a source.

### 3. Empirical Verification

For **APIs**:

- [ ] Endpoint Verification Matrix includes **all public endpoints** discovered in the spec/docs (grouped if the surface is large).
- [ ] Each endpoint in `SKILL.md` was probed and returned 2xx or an expected documented error, or is explicitly marked `UNVERIFIED`.
- [ ] `scripts/smoke_test.py` calls real endpoints and asserts expected keys/status codes.
- [ ] `python scripts/smoke_test.py` passes in the current environment.

For **Databases**:

- [ ] Schema reference comes from an executed introspection query and includes **all user-facing tables**.
- [ ] Sample rows are captured from actual `SELECT` output for every user-facing table.
- [ ] `scripts/connect_and_sample.py` connects and returns row counts / samples.
- [ ] `python scripts/connect_and_sample.py` passes in the current environment.

For **Libraries / Packages**:

- [ ] Install/import smoke test passes.
- [ ] Example code from `SKILL.md` was executed and produced the claimed output.
- [ ] Edge cases noted in "Wall of Shame" were reproduced.

### 4. Hallucination Audit

Pick 5 concrete claims from `SKILL.md` (endpoint paths, parameter names, column names, function signatures, version
constraints). For each:

- [ ] Find the source in live docs, a probed response, or a query result.
- [ ] If a claim cannot be sourced, mark it `UNVERIFIED` or remove it.

### 5. Operational Utility

Ask: could an agent that has never used this technology follow the skill and succeed on its first try?

- [ ] The first example is the absolute minimal working call/query.
- [ ] Required environment variables are named explicitly.
- [ ] Common errors have copy-pasteable fixes.
- [ ] Pitfalls are described as failures you actually observed, not generic warnings.

## Scoring Rubric

Use this rubric to compare two versions of a knowledge skill (control vs. improved).

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| **Structure** | Missing frontmatter or no scripts | Has frontmatter and SKILL.md body | Also has references/ and scripts/ with required files |
| **Coverage** | Only a few endpoints/tables/modules covered | Main surface covered | Full public surface covered (or exclusions explicitly noted) |
| **Glossary** | No glossary or <3 terms | Glossary present but missing sources/examples | Glossary present, every term has source + real example |
| **Live verification** | No probes executed | Some endpoints/tables probed | Every documented endpoint/table probed + smoke test passes |
| **Hallucination rate** | >2 unverified claims | 1-2 unverified claims | 0 unverified claims or all marked UNVERIFIED |
| **Operational utility** | Agent could not follow it | Agent could follow but would hit avoidable errors | Agent can follow and avoid documented pitfalls |

Maximum score: **12**. A passing knowledge skill should score at least **10/12**.

## How to Run an A/B Test With Subagents

1. Choose a target (obscure API/DB/library with domain jargon).
2. **RED (control)**: ask a subagent to research the target and create a skill with *no* guidance beyond the deliverables.
3. Capture failures against this checklist.
4. Improve the skill-creation skills based on the failures.
5. **GREEN (treatment)**: ask a subagent to research the same target, but first read the improved skill-creation skills.
6. Score both outputs with the rubric above and compare.

See `testing-skills-with-subagents.md` for the general RED/GREEN/REFACTOR discipline.
