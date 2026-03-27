---
name: legacy-migration-suite
description: Use for migrating legacy codebases (C#, MATLAB, Python 2) to modern Python (3.9+). Unified guide for automated refactoring, type conversion, and logic verification. CRITICAL: Always use `python-core-pro` for the final modern code standards.
---
# Legacy Migration Suite (Consolidated)

Unified expert guide for high-fidelity code migration and modernization.

## ⚠️ Mandatory Pre-flight: Validation & Verification

1. **Verify Logic First**: Ensure you have a working baseline (or tests) for the legacy code before starting.
2. **Automated Conversion**: Use specialized tools (e.g., `2to3`, `f2py`, custom regex) for the initial pass.
3. **Type Parity**: Verify that data types (especially floating point precision) match between the legacy and modern implementations.

---

## 1. Migration from Python 2 to 3

Use for updating legacy Python codebases to modern standards.

### Core Idioms
- **Prints & Divisions**: Update `print` statements to functions and ensure integer division (`//`) is used correctly.
- **Unicode**: Convert all strings to Unicode (default in Python 3).

---

## 2. Migration from C# / MATLAB

Use for porting specialized logic and matrix computations to Python.

### Core Tools
- **NumPy/SciPy**: Use for MATLAB-to-Python matrix operations.
- **Python Standard Library**: Use for C#-to-Python logic (Pathlib, Datetime, JSON).

---

## 🛠️ Common Pitfalls (The "Wall of Shame")

1. **One-to-One Translation**: Blindly copying logic without adapting to Pythonic idioms.
2. **Ignoring Library Differences**: Assuming `numpy.sin` and `matlab.sin` behave exactly the same in edge cases.
3. **Incomplete Coverage**: Migrating code without a testing strategy to confirm logic parity.

## References
- `skills/python-dev/legacy-migration-suite/references/legacy-migration/` — C# and MATLAB porting patterns.
- `skills/python-dev/legacy-migration-suite/references/python2-migration/` — Python 2to3 checklists.
