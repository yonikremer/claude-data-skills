from typing import List, Dict
from .llm_client import get_llm_client

EXTRACTOR_SYSTEM_PROMPT = """
You are a Senior Technical Librarian. Your task is to extract "Golden Terms" and "Semantic Triplets" from internal documentation. 

### THE RULES:
1. IDENTIFY: Unique project names (e.g., "Prism"), internal acronyms (e.g., "N-RT-RIC"), and specialized technical terms.
2. RELATIONSHIPS: Also identify triplets in format [Subject] --[Relationship]--> [Object].
   - Allowed Relationships: SUB_PROJECT_OF, DEPENDS_ON, USES, MANAGED_BY, REPLACES.
3. REJECT: Common industry terms (e.g., "SQL", "Docker", "API"). If a student of CS would know it, DROP IT.
4. ANCHOR: For every term/triplet, you MUST provide a "Source Anchor"—a verbatim, 100% accurate quote from the text.
5. NOISE: Ignore meeting headers and copyright boilerplate.

### OUTPUT FORMAT (JSON LIST ONLY):
[
  {
    "term": "Term Name",
    "definition": "Concise definition.",
    "anchor": "Verbatim quote.",
    "entity_type": "PROJECT|COMPONENT|TECH_STACK",
    "relationships": [
       {"target": "Other Term", "type": "SUB_PROJECT_OF"}
    ]
  }
]
"""

def extract_with_llm(text: str) -> List[Dict]:
    """
    Extracts terms and relationships using a local LLM.
    """
    client = get_llm_client()
    messages = [
        {"role": "system", "content": EXTRACTOR_SYSTEM_PROMPT},
        {"role": "user", "content": f"Extract terms and relationships from the following text:\n\n{text}"}
    ]
    
    response = client.chat(messages, json_mode=True)
    return response

# Keeping legacy name for backward compatibility in tests
def extract_with_anchors(text: str) -> List[Dict]:
    return extract_with_llm(text)
