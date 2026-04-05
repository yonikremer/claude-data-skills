---
name: model
description: Use when suggesting an ML baseline for a target variable in a file. Usage: /model <target> <file>
---

# Model Command

When this skill is invoked (e.g., via `/model <target> <file>`), use the `ml-classical` skill to:

1. Analyze the data and suggest a baseline model to predict the target variable.
2. Include preprocessing steps (handling skew, encoding, scaling).
3. Provide a sample Scikit-Learn implementation.
