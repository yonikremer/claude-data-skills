# Skill-Creation A/B Test Harness

This directory holds a reproducible experiment to test whether the improved
`api-skill-creator`, `database-skill-creator`, and `tech-explorer` skills actually
produce better agent skills for obscure, jargon-heavy APIs and databases.

## Targets

| Slug | Technology | Why it is hard |
|---|---|---|
| `clinicaltrials` | ClinicalTrials.gov API v2 | Deep nested modules (`protocolSection`, `designModule`, `armsInterventionsModule`) and clinical jargon (`allocation`, `masking`, `phases`). |
| `kuzu` | Kùzu embedded graph DB | Obscure property-graph DB with Cypher-like DDL; easy to confuse with Neo4j or RDF stores. |

A third target, **WoRMS** (World Register of Marine Species), was planned but not
run because the subagent provider quota was exhausted before the RED phase could
complete.

## Manual Validation

Because the provider quota blocked subagent runs, I manually applied the
*improved* workflow to `clinicaltrials` and `kuzu`. Both produced skills whose
smoke tests pass against the real technology:

```bash
python skill-trials/clinicaltrials/improved/scripts/smoke_test.py
python skill-trials/kuzu/improved/scripts/connect_and_sample.py
```

See the rubric scores at the bottom of this file.

## Subagent A/B Instructions (run when quota is available)

### 1. RED — baseline without skill guidance

Create the three control output directories, then run the swarm below.

```bash
mkdir -p skill-trials/worms/control
mkdir -p skill-trials/clinicaltrials/control
mkdir -p skill-trials/kuzu/control
```

Use the prompt in `prompts/control-prompt.txt`. The key instruction is:

> Research the target and create a reusable agent skill. No existing skill-creation
> files should be read. Work fully autonomously.

### 2. Improve the skills (already done in this branch)

The improved skills live in:

- `src/skills/learning-and-skill-building/tech-explorer/SKILL.md`
- `src/skills/learning-and-skill-building/api-skill-creator/SKILL.md`
- `src/skills/learning-and-skill-building/database-skill-creator/SKILL.md`
- `src/skills/learning-and-skill-building/writing-skills/testing-knowledge-skills.md`

### 3. GREEN — treatment with skill guidance

Create the treatment output directories, then run the swarm below with the
prompt in `prompts/treatment-prompt.txt`. The key difference:

> Before writing anything, read these skill files and follow their workflow
> exactly: `tech-explorer/SKILL.md`, `api-skill-creator/SKILL.md` or
> `database-skill-creator/SKILL.md`, and `testing-knowledge-skills.md`.

### 4. Score both sets of outputs

Use the rubric in `src/skills/learning-and-skill-building/writing-skills/testing-knowledge-skills.md`
(or copy the short version below). Verify at least:

- Frontmatter and directory structure.
- Glossary with sources + real examples.
- Endpoint/table verification matrix.
- Smoke test exists and passes (`python scripts/smoke_test.py`).
- Hallucination audit of 5 claims.

## Scoring Rubric (short version)

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Structure | Missing frontmatter or no scripts | Has frontmatter + SKILL.md body | Also has references/ and scripts/ with required files |
| Coverage | Only a few endpoints/tables/modules covered | Main surface covered | Full public surface covered (or exclusions explicitly noted) |
| Glossary | No glossary or <3 terms | Glossary present but missing sources/examples | Glossary present, every term has source + real example |
| Live verification | No probes executed | Some endpoints/tables probed | Every documented endpoint/table probed + smoke test passes |
| Hallucination rate | >2 unverified claims | 1-2 unverified claims | 0 unverified claims or all marked UNVERIFIED |
| Operational utility | Agent could not follow it | Agent could follow but would hit avoidable errors | Agent can follow and avoid documented pitfalls |

Maximum score: **12**. Passing knowledge skill: **≥ 10**.

## Manual Validation Scores

| Target | Structure | Coverage | Glossary | Live verification | Hallucination | Utility | Total |
|---|---|---|---|---|---|---|---|
| ClinicalTrials.gov v2 | 2 | 2 | 2 | 2 | 2 | 2 | **12/12** |
| Kùzu graph DB | 2 | 1 | 2 | 2 | 2 | 2 | **11/12** |

Notes:

- ClinicalTrials.gov v2: the known public surface (`/studies`, `/studies/{nctId}`, `/studies/download`, `/version`) is enumerated.
- Kùzu: the core DDL/DML surface used by the skill is covered, but advanced features (COPY TO, EXPLAIN, transactions,
  full data-type matrix) are listed in `references/tech-specs.md` as not yet probed.

Both improved manual outputs include:

- Correct frontmatter.
- `references/api-docs.md` or `references/tech-specs.md` with a verification matrix.
- `references/glossary.md` where every term has a source and a real example.
- A runnable smoke test that exercises the real technology and passes.
- A "Wall of Shame" section documenting empirically discovered pitfalls.
