---
name: research-summaries
description: Generates professional research summaries in two formats: Detailed Technical (for Confluence) and High-Level Executive (for Department Emails). Use to communicate findings, methodologies, and insights.
---
# Research Summaries

This skill provides standardized formats for communicating research findings to different audiences.

## Summary Types

### 1. Detailed Technical Report (Confluence)
**Audience**: Peer engineers, data scientists, and project managers.
**Goal**: Absolute transparency and reproducibility.
**Components**:
- **Metadata**: Author, Date, Dataset Versions.
- **Problem Statement**: Specific objectives and hypotheses.
- **Methodology & Definitions**: Exact formulas, data filters, and technical definitions.
- **Challenges & Solutions**: Documentation of edge cases, "dirty" data encountered, and the logic used to fix it.
- **Results**: Complete statistical tables and deep-dive charts.
- **Appendix**: SQL queries, Python snippets, and raw logs.

### 2. High-Level Executive Insight (Email)
**Audience**: Department-scale, stakeholders, and non-technical leadership.
**Goal**: Communication of value and "The Lead."
**Components**:
- **The Hook**: A clear, 1-sentence summary of the biggest finding.
- **Visual Evidence**: 1-2 primary Plotly charts with descriptive labeling.
- **Impact Examples**: "What this means for the business/user."
- **Key Takeaways**: Bullet points focused on insights, not metrics.
- **Call to Action**: Next steps for the department.

## Workflow

1. **Select Type**: Choose based on the target platform (Confluence vs Email).
2. **Consult Data Dictionary**: Reference `.claude_data_dictionary.json` for exact column meanings.
3. **Generate Content**: Use the templates provided in `assets/`.
4. **Validation**: Ensure all Plotly charts follow the "Gold Standard" labeling (descriptive titles, units).

## References (Load on demand)
- `assets/confluence_template.md` — Detailed markdown structure.
- `assets/executive_email_template.md` — Scannable email structure.
