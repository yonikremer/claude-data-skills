# Autonomous Logic Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a systematic migration skill that instruments legacy code (C#, MATLAB, Python), observes behavior via trace logs, and replicates logic in modern Python using TDD.

**Architecture:** A multi-stage pipeline:
1. **Instrumentor:** Injects non-destructive logging into legacy source.
2. **Tracer:** Executes code with generated inputs to capture I/O and decision paths.
3. **Synthesis:** Generates Python code and TDD tests from trace logs.
4. **Validator:** Differentially tests legacy vs. modern output.

**Tech Stack:** Python 3.9+, pytest, regex-based code manipulation.

---

### Task 1: Skill Structure & Metadata

**Files:**
- Create: `skills/python-dev/autonomous-logic-recovery/SKILL.md`
- Create: `skills/python-dev/autonomous-logic-recovery/__init__.py`

- [ ] **Step 1: Create SKILL.md**

```markdown
---
name: autonomous-logic-recovery
description: Systematically migrates complex legacy logic by instrumenting, observing behavior, and replicating via TDD.
---

# Autonomous Logic Recovery

## Workflow
1. **Instrumentation**: Inject probes into legacy code.
2. **Observation**: Run legacy code and capture trace logs.
3. **Synthesis**: Generate modern Python and TDD tests.
4. **Verification**: Differentially test legacy vs. new.
```

- [ ] **Step 2: Initialize package**
Create `skills/python-dev/autonomous-logic-recovery/__init__.py` (empty file).

- [ ] **Step 3: Commit Task 1**
`git add skills/python-dev/autonomous-logic-recovery/ && git commit -m "feat: init autonomous-logic-recovery skill structure"`

---

### Task 2: C# Instrumentor (Probe Injection)

**Files:**
- Create: `skills/python-dev/autonomous-logic-recovery/scripts/csharp_prober.py`
- Create: `skills/python-dev/autonomous-logic-recovery/tests/test_csharp_prober.py`

- [ ] **Step 1: Write failing test for C# instrumentation**

```python
def test_inject_if_probe():
    code = "if (x > 0) { doWork(); }"
    prober = CSharpProber()
    result = prober.inject(code)
    assert 'Console.WriteLine("DEBUG: if (x > 0) entered");' in result
```

- [ ] **Step 2: Implement CSharpProber**
Use regex to find `if`, `else`, and `foreach` blocks and inject `Console.WriteLine` statements.

- [ ] **Step 3: Verify and Commit**
Run `pytest` and commit.

---

### Task 3: MATLAB Instrumentor

**Files:**
- Create: `skills/python-dev/autonomous-logic-recovery/scripts/matlab_prober.py`
- Create: `skills/python-dev/autonomous-logic-recovery/tests/test_matlab_prober.py`

- [ ] **Step 1: Write failing test for MATLAB instrumentation**

```python
def test_inject_matlab_probe():
    code = "if x > 0\n    disp('hello')\nend"
    prober = MatlabProber()
    result = prober.inject(code)
    assert "fprintf('DEBUG: if x > 0 entered\\n');" in result
```

- [ ] **Step 2: Implement MatlabProber**
Regex to find `if`, `elseif`, `for`, `while` and inject `fprintf` calls.

- [ ] **Step 3: Verify and Commit**
Run `pytest` and commit.

---

### Task 4: Trace Log Parser & Synthesis

**Files:**
- Create: `skills/python-dev/autonomous-logic-recovery/scripts/logic_synthesizer.py`

- [ ] **Step 1: Define Trace Log Format**
Create a parser for logs like `DEBUG: if (x > 0) entered`.

- [ ] **Step 2: Generate TDD Template**
Implement `generate_test(trace_json)` which returns a `pytest` file matching captured inputs to captured outputs.

- [ ] **Step 3: Commit Task 4**

---

### Task 5: Differential Validator

**Files:**
- Create: `skills/python-dev/autonomous-logic-recovery/scripts/validator.py`

- [ ] **Step 1: Implement Output Comparator**
Function to compare JSON outputs from legacy and Python, allowing for epsilon float differences.

- [ ] **Step 2: Verification Gate**
Integrate `verification-before-completion` as a final check.

- [ ] **Step 3: Final Commit**
