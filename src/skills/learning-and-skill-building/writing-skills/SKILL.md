---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment. Extends Gemini CLI's capabilities with specialized knowledge, workflows, or tool integrations.
---

# Writing Skills

## Overview

**Writing skills IS Test-Driven Development applied to process documentation.**

Skills are modular, self-contained packages that transform Gemini CLI from a general-purpose agent into a specialized
agent equipped with procedural knowledge.

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right
thing.

**REQUIRED BACKGROUND:** You MUST understand `superpowers:test-driven-development` before using this skill.

## About Skills

### What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains.
2. **Tool integrations** - Instructions for working with specific file formats or APIs.
3. **Domain expertise** - Company-specific knowledge, schemas, business logic.
4. **Bundled resources** - Scripts, references, and assets for complex tasks.

### Core Principles

- **Concise is Key**: Only add context Gemini CLI doesn't already have. Challenge each piece of information.
- **Appropriate Degrees of Freedom**:
    - *High freedom*: Text-based instructions for heuristical tasks.
    - *Medium freedom*: Pseudocode or scripts with parameters.
    - *Low freedom*: Specific scripts for fragile, error-prone operations.

## Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (name, description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code (Node.js/Python/Bash/etc.)
    ├── references/ - Documentation loaded as needed
    └── assets/     - Files used in output (templates, icons, etc.)
```

### Progressive Disclosure

Manage context efficiently by splitting content:

1. **Metadata**: Always in context.
2. **SKILL.md body**: Loaded when skill triggers.
3. **Bundled resources**: Loaded only as needed by the agent.

## Skill Creation Process (TDD Adapted)

Follow these steps in order:

### 1. Understanding & RED Phase (Write Failing Test)

- **Understand**: Clearly understand concrete examples of how the skill will be used. Ask 1-2 clarifying questions if
  needed.
- **Baseline Test**: Run a pressure scenario with a subagent WITHOUT the skill.
- **Watch it fail**: Document exact rationalizations and failures. This is your "failing test."
- **Mastery Phase (Optional)**: If the subject is an unfamiliar technology (library, API, database), you MUST use
  `tech-explorer` to achieve empirical mastery before proceeding to documentation.

### 2. Planning & GREEN Phase (Write Minimal Skill)

- **Plan**: Identify what scripts, references, and assets would be helpful.
- **Specialized Creators**: For specific domains, use specialized workflows:
    - **APIs**: Use `api-skill-creator`.
    - **Databases**: Use `database-skill-creator`.
- **Initialize**: Use the `init_skill.cjs` script:
  `node <path-to-skill-creator>/scripts/init_skill.cjs <skill-name> --path <output-directory>`
- **Write Minimal Skill**: Write the `SKILL.md` and resources addressing specific baseline failures.
- **Watch it pass**: Run scenario WITH skill. Agent should now comply.

### 3. Refactor Phase (Close Loopholes)

- **Plug Holes**: Find new rationalizations → plug them in `SKILL.md` → re-verify until bulletproof.

### 4. Packaging & Deployment

- **Package**: `node <path-to-skill-creator>/scripts/package_skill.cjs <path/to/skill-folder>`
- **Install**: Offer to install locally (`--scope workspace`) or at user level (`--scope user`).
- **Reload**: Notify user they MUST manually execute `/skills reload`.

## Interoperability

- **Tech Explorer**: Used for discovering and mastering unfamiliar technologies before they are documented.
- **API Skill Creator**: Specialized workflow for mapping API documentation to skills.
- **Database Skill Creator**: Specialized workflow for mapping database structures to skills.

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

This applies to NEW skills AND EDITS to existing skills. Delete untested changes.

## Quick Reference: SKILL.md Structure

- **Frontmatter**: `name` (hyphen-case) and `description` (Use when..., single-line).
- **Description**: Describes ONLY when to use (triggering conditions), NOT what it does. **NEVER summarize the workflow
  in the description.**

## Common Mistakes

- **Narrative Examples**: Don't tell stories; provide reusable patterns.
- **Multi-Language Dilution**: One excellent example (e.g., Python for data) is better than 5 mediocre ones.
- **Workflow in Description**: If you summarize the workflow in the metadata, the agent may skip reading the full skill.

## Deployment Checklist

- [ ] Create pressure scenarios.
- [ ] Run WITHOUT skill - document behavior.
- [ ] Initialize with `init_skill.cjs`.
- [ ] YAML frontmatter correct (single-line description).
- [ ] Description starts with "Use when...".
- [ ] Run WITH skill - verify compliance.
- [ ] Package with `package_skill.cjs`.
- [ ] Commit to git.
