---
name: skill-engineering
description: Analyzes local libraries/codebases and generates new Claude Code skills. Use when encountering a proprietary or undocumented internal library to create persistent "Gold Standard" documentation and scripts.
---
# Skill Engineering (Library-to-Skill)

This meta-skill allows the agent to ingest a local library or codebase and transform it into a structured, high-quality Claude Code skill.

## Workflow: Creating a New Skill

### Phase 1: Library Discovery & Analysis

1. **Locate Source**: Identify the root directory of the library.
2. **Inspect Structure**: List files to understand modules, tests, and examples.
3. **Analyze Exports**: Use Python's `inspect` module or read `__init__.py` to find primary classes and functions.
4. **Read Docstrings/Tests**: Extract "Gold Standard" usage patterns from existing docstrings and unit tests.

### Phase 2: Knowledge Extraction

For the target library, identify:
- **Core Intent**: What is the primary problem this library solves?
- **Primary API**: The top 5-10 functions/classes users need daily.
- **Resource Constraints**: Does it use significant RAM? Does it need GPU? (Informs the `get-available-resources` integration).
- **Common Pitfalls**: What are the frequent errors or non-idiomatic ways to use it?

### Phase 3: Skill Generation

Create a new directory in `skills/` following the project's standard architecture:

```
skills/[library-name]/
├── SKILL.md              # Entry point with Gold Standard sections
├── references/           # In-depth API docs, common patterns
└── scripts/              # Helper scripts (e.g., check_system.py, templates)
```

**MANDATORY Sections for `SKILL.md`**:
- **Resource Check**: Pre-flight checks for hardware limits.
- **Strict Idioms**: Force the most modern/performant way to use the library.
- **Wall of Shame**: Explicitly list common model hallucinations for this library.

### Phase 4: Registration & Validation

1. **Update Marketplace**: Add the new skill path to `.claude-plugin/marketplace.json`.
2. **Update Skills Index**: Add the skill name and description to the root-level `SKILLS.md` file.
3. **Commit**: Use `git` to track the new skill and the updated index.
4. **Verify**: Test the skill by asking a question that requires its usage.

## Workflow: Database to Skill Creation

Use this workflow when you want to create a skill for interacting with a specific database or schema.

1. **Schema Discovery**: Connect to the database and extract schema information (tables, columns, types, relationships).
2. **Entity Mapping**: Identify core entities and how they map to business logic.
3. **Common Query Patterns**: Document the 5-10 most frequent or complex query patterns.
4. **Validation Logic**: Create `Pydantic` models or `SQLAlchemy` schemas for data validation.
5. **Skill Generation**:
   - `scripts/query_generator.py`: A helper script for generating or validating queries.
   - `references/schema.md`: Detailed documentation of the database structure.
   - `SKILL.md`: Entry point with core query examples and "Gold Standard" safety rules (e.g., "Always use parameterized queries").

## Workflow: API to Skill Creation

Use this workflow when you want to create a skill for interacting with a specific REST or GraphQL API.

1. **Endpoint Analysis**: Read OpenAPI/Swagger specs or inspect live endpoints to map available resources.
2. **Authentication Flow**: Document how to obtain and use API keys or tokens.
3. **Data Contract Extraction**: Identify request/response structures for primary endpoints.
4. **Error Handling**: Document specific API error codes and their meanings.
5. **Skill Generation**:
   - `scripts/api_client.py`: A lightweight, robust client template for interacting with the API.
   - `references/endpoints.md`: Documentation of all major endpoints and parameters.
   - `SKILL.md`: Entry point with common request examples and "Gold Standard" efficiency rules (e.g., "Use batch endpoints when possible").

## Best Practices for OS Models

- **Dense Documentation**: Keep the primary `SKILL.md` dense with keywords to save tokens.
- **Script-First**: If the library is complex, prefer writing a `scripts/template.py` that the model can copy rather than explaining the syntax in text.
- **Version Locking**: Explicitly state which version of the library the skill is designed for.
