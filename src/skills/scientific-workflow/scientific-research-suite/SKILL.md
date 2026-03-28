---
name: scientific-research-suite
description: Use for the entire scientific lifecycle: brainstorming, research design, critical thinking, writing, and peer review. Unified guide for high-impact research, literature synthesis, and publication-quality manuscripts. CRITICAL: For deep research, use `research-lookup` first.
---
# Scientific Research Suite (Consolidated)

Unified expert guide for the complete scientific research lifecycle, from initial ideation to final publication and peer review.

## ⚠️ Mandatory Pre-flight: Deep Research

High-quality scientific output requires current, verified data.

1. **Research First**: Use the `research-lookup` skill to find recent (last 5-10 years) high-impact papers.
2. **Verify Citations**: Never hallucinate citations. Cross-reference all claims against original sources.
3. **Visuals are Mandatory**: Every scientific output MUST include a graphical abstract and technical schematics.

---

## 1. Ideation & Brainstorming

Use for creative research design and interdisciplinary exploration.

### Core Idioms
- **Divergent Thinking**: Explore adjacent fields for novel methodology.
- **Feasibility Check**: Always assess data availability and computational cost early.
- **Hypothesis Generation**: Formulate testable, falsifiable research questions.

```markdown
# Brainstorming Workflow
1. Identify knowledge gaps via research-lookup.
2. Draft 3 alternative research designs (Conservative, Bold, Hybrid).
3. Evaluate each for impact vs. feasibility.
```

---

## 2. Critical Thinking & Evaluation

Use for assessing claims, methodology, and scholar impact.

### Core Tools
- **Methodology Check**: Evaluate sample size, controls, and potential biases.
- **Evidence Hierarchy**: Prioritize meta-analyses and RCTs over case reports.
- **Scholar Impact**: Look beyond h-index; assess contribution to the field's "red thread."

---

## 3. Scientific Writing (IMRAD)

Use for drafting manuscripts, reports, and white papers.

### Core Idioms
- **Two-Stage Process**: **Outline (Bullet points) → Prose (Full paragraphs)**.
- **Full Prose Only**: NEVER leave bullet points in a final manuscript.
- **Visual-First**: Plan your figures and tables as the backbone of the story.

```latex
% Professional Report Formatting (XeLaTeX)
\usepackage{scientific_report}
\begin{keyfindings}[Discovery]
AI-driven drug discovery reduced lead time by 40% (p < 0.001).
\end{keyfindings}
```

---

## 4. Peer Review & Revision

Use for structured evaluation of manuscripts and grant proposals.

### Core Workflow
1. **The "Big Picture"**: Does the study address a significant problem?
2. **The "Technical Core"**: Is the methodology sound and reproducible?
3. **The "Formatting"**: Are figures clear? Is the language precise?

---

## 🛠️ Common Pitfalls (The "Wall of Shame")

1. **Bullet Pointing**: Submitting a manuscript with bulleted lists in the Discussion section.
2. **Visual Absence**: Scientific papers without a graphical abstract or flowcharts.
3. **Citation Hallucination**: Inventing papers or authors to support a claim.
4. **Subscript Error**: Using Unicode subscripts (₀₁) in LaTeX/ReportLab; use `_{1}` or `<sub>1</sub>`.

## References
- `skills/scientific-workflow/scientific-research-suite/references/writing/` — IMRAD and Citation styles.
- `skills/scientific-workflow/scientific-research-suite/references/visualization/` — Multi-panel figures.
- `skills/scientific-workflow/scientific-research-suite/references/peer-review/` — Reviewer checklists.
