# SKILL: dictionary-agent

Use this skill when you encounter unfamiliar technical terms, project-specific acronyms, or domain names. **DO NOT GUESS.**

## 🛠️ THE RULE OF ZERO TOLERANCE FOR GUESSING
If you see a word you don't know (e.g., "N-RT-RIC", "A1-P", "O-DU"), you MUST immediately perform a lookup.

### Step 1: Check the Golden Dictionary
Look at the root of the project for `GOLDEN_TERMS.md`. If the term is there, use that definition.

### Step 2: Use the Lookup Tool
If the term is NOT in the Golden Dictionary, run the following command immediately:
```bash
dictionary-lookup lookup "TERM_NAME"
```
Or, if your environment supports slash commands:
```bash
/define TERM_NAME
```

### Step 3: Synthesis
When the tool returns a result:
1. **Explain the definition** clearly to the user.
2. **Provide the usage context** (if the tool returned usage examples).
3. **Connect to current task**: Explain how this specific definition changes or informs the code/analysis you are currently writing.

---

## 🏗️ HOW TO EXTRACT NEW TERMS (For the Agent)
If you are asked to "learn from files" or "build the dictionary":

1. **Scan**: Run `dictionary-scan "PATH_TO_FILES"`.
2. **Analyze**: Read the text returned by the scanner.
3. **Extract**: Identify all technical keywords. 
4. **Compare**: Check `dictionary.json` (via the lookup tool) to see if the term exists.
5. **Update**: 
   - If **New**: Add a concise, AI-ready definition.
   - If **Existing**: Add the new sentence as a `Usage Example`.

---

## ⚠️ "Wall of Shame" (Common AI Errors to Avoid)
- **hallucinating definitions**: Never provide a definition for an acronym unless you have verified it via the tool or `GOLDEN_TERMS.md`.
- **Ignoring Context**: If the dictionary lists two different meanings for a term, ask the user which project context applies.
- **Duplicate Entries**: Do not add a new entry if a fuzzy match exists (e.g., "Term-A" and "Term A" are the same).
