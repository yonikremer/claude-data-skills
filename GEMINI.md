# GEMINI.md - Dictionary Agent Integration

## 🧠 Domain Knowledge: Golden Terms
Before starting any technical task, always consult the **Golden Terms Dictionary** for domain-specific definitions:
- [GOLDEN_TERMS.md](./GOLDEN_TERMS.md)

## 🛠️ Automated Lookup Strategy (MANDATORY)
1. **Detection**: If you encounter an unfamiliar term (e.g., an acronym like "N-RT-RIC" or a project name), **DO NOT GUESS**.
2. **Action**: Immediately run `/define <term>`.
3. **Synthesis**: Incorporate the returned definition and usage examples into your response.
4. **Tool**: If `/define` is unavailable, use `python -m src.dictionary_agent.tools lookup "<term>"`.
