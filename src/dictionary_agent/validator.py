from typing import Dict, Any
from .llm_client import get_llm_client

VALIDATOR_SYSTEM_PROMPT = """
You are a Cynical Peer Reviewer. Your goal is to find reasons why the proposed extraction (term, definition, or relationship) is WRONG or UNSUPPORTED by the raw context.

### THE ZERO-TRUST PROTOCOL:
1. LOGICAL ENTAILMENT: Does the Raw Context logically imply the Proposed Definition or Relationship? 
2. NO EXTERNAL KNOWLEDGE: If the extraction includes facts NOT found in the Raw Context (even if true in the real world), it is a "Contextual Hallucination."
3. ANCHOR CHECK: Verify the provided anchor quote actually exists in the raw text and supports the specific claim.
4. RELATIONSHIP CHECK: For triplets [Subject] --[Relationship]--> [Object], ensure the context explicitly defines this link.

### EVALUATION CRITERIA:
- PASS: The extraction is 100% supported by the context.
- CONFLICT: The extraction contradicts the context.
- HALLUCINATION: The extraction adds details not found in the context.

### OUTPUT FORMAT (JSON ONLY):
{
  "is_valid": boolean,
  "status": "PASS" | "CONFLICT" | "HALLUCINATION",
  "reasoning": "Explanation of why it passed or failed.",
  "suggested_fix": "A revised version that is strictly supported, or null."
}
"""

def validate_with_llm(raw_text: str, extraction: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates an extraction using a local LLM.
    """
    client = get_llm_client()
    messages = [
        {"role": "system", "content": VALIDATOR_SYSTEM_PROMPT},
        {"role": "user", "content": f"Raw Context:\n{raw_text}\n\nProposed Extraction:\n{extraction}"}
    ]
    
    return client.chat(messages, json_mode=True)

# Backward compatibility wrapper
def validate_definition(raw_text: str, definition: str) -> bool:
    # Legacy interface only returned bool
    result = validate_with_llm(raw_text, {"definition": definition})
    return result.get("is_valid", False)
