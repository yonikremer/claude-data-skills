from typing import Dict, Any, Optional
import difflib
from .llm_client import get_llm_client

VALIDATOR_SYSTEM_PROMPT = """
You are a Cynical Peer Reviewer. Your goal is to find reasons why the proposed extraction (term, overview, deep dive, or relationship) is WRONG or UNSUPPORTED by the raw context.

### THE ZERO-TRUST PROTOCOL:
1. LOGICAL ENTAILMENT: Does the Raw Context logically imply the Proposed Overview, Deep Dive, or Relationship? 
2. NO EXTERNAL KNOWLEDGE: If the extraction includes facts NOT found in the Raw Context (even if true in the real world), it is a "Contextual Hallucination."
3. ANCHOR CHECK: Verify the provided anchor quote actually exists in the raw text and supports the specific claim.
4. RELATIONSHIP CHECK: For triplets [Subject] --[Relationship]--> [Object], ensure the context explicitly defines this link.

### EVALUATION CRITERIA:
- GOLD: The extraction is 100% supported by the context and has a perfect verbatim anchor.
- SILVER: The extraction is logically implied by the context, but uses some summarization or the anchor is slightly fuzzy.
- BRONZE: The extraction is mentioned in passing, but the definition/overview is speculative.
- CONFLICT/HALLUCINATION: The extraction contradicts the context or adds non-existent details.

### OUTPUT FORMAT (JSON ONLY):
{
  "is_valid": boolean,
  "confidence_level": "GOLD" | "SILVER" | "BRONZE" | "PENDING",
  "status": "PASS" | "CONFLICT" | "HALLUCINATION",
  "reasoning": "Explanation of why it passed or failed.",
  "suggested_fix": "A revised version that is strictly supported, or null."
}
"""

def verify_anchor_exists(raw_text: str, anchor: str, threshold: float = 0.85) -> bool:
    """
    Deterministic hard-check to ensure the anchor exists in the raw text.
    Pitfall 1 Second-Order Fix: Sliding Window Check for long documents.
    """
    if not anchor:
        return False
    
    clean_anchor = anchor.strip()
    if clean_anchor in raw_text:
        return True
    
    # Fuzzy fallback with sliding window
    # We split raw_text into overlapping chunks to avoid difflib complexity on giant strings
    window_size = len(clean_anchor) * 3
    step = len(clean_anchor)
    
    for i in range(0, len(raw_text), step):
        window = raw_text[i : i + window_size]
        if len(window) < len(clean_anchor):
            break
            
        match = difflib.get_close_matches(clean_anchor, [window], n=1, cutoff=threshold)
        if match:
            return True
            
    return False

def validate_with_llm(raw_text: str, extraction: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates an extraction using a local LLM with an initial hard-anchor check.
    """
    anchor = extraction.get("anchor", "")
    
    # 1. Hard-Anchor Verification (Pitfall 1 Fix)
    if not verify_anchor_exists(raw_text, anchor):
        return {
            "is_valid": False,
            "confidence_level": "PENDING",
            "status": "HALLUCINATION",
            "reasoning": "Hard-Anchor Verification Failed: The provided quote does not exist in the source text.",
            "suggested_fix": None
        }

    # 2. LLM Logical Validation
    client = get_llm_client()
    messages = [
        {"role": "system", "content": VALIDATOR_SYSTEM_PROMPT},
        {"role": "user", "content": f"Raw Context:\n{raw_text}\n\nProposed Extraction:\n{extraction}"}
    ]
    
    return client.chat(messages, json_mode=True)
