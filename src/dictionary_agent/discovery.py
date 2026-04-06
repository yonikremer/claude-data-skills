from typing import List, Dict, Any, Optional
from datetime import datetime
from .llm_client import get_llm_client
from .models import Dictionary, DictionaryEntry, UsageExample, GraphTriplet

EXTRACTOR_SYSTEM_PROMPT = """
You are a Senior Technical Librarian. Your task is to extract "Golden Terms" and "Semantic Triplets" from internal documentation. 

### THE RULES:
1. IDENTIFY: Unique project names, internal acronyms, and specialized technical terms.
2. RELATIONSHIPS: Also identify triplets in format [Subject] --[Relationship]--> [Object].
   - Allowed Relationships: SUB_PROJECT_OF, DEPENDS_ON, USES, MANAGED_BY, REPLACES, ALIAS_OF.
3. STRUCTURE: For each term, provide:
   - OVERVIEW: A concise, one-sentence "executive summary" for non-technical readers.
   - DEEP DIVE: All technical details, formulas ($Base * Rate$), threshold limits, and implementation specifics.
4. CONTRASTIVE FILTERING (Pitfall 5 Fix): 
   - REJECT common industry terms (e.g., "SQL", "Docker", "API") IF they refer to the generic tool.
   - ACCEPT common terms ONLY if they have a specific internal project meaning (e.g., "The API" referring to a specific internal service).
5. CONTEXTUAL ALIASING: If you deduce that terms refer to the same project or concept, create an 'ALIAS_OF' relationship.
6. COLD START: If context is missing for an overview, set to "[PENDING]".
7. ANCHOR: Provide a verbatim, 100% accurate quote from the text for every term/triplet.

### OUTPUT FORMAT (JSON LIST ONLY):
[
  {
    "term": "Term Name",
    "overview": "One-sentence executive summary.",
    "deep_dive": "Detailed technical explanation.",
    "anchor": "Verbatim quote.",
    "entity_type": "PROJECT|COMPONENT|TECH_STACK",
    "relationships": [
       {"target": "Other Term", "type": "SUB_PROJECT_OF"}
    ]
  }
]
"""

def extract_with_llm(text: str, context_hints: Optional[str] = None) -> List[Dict]:
    """
    Extracts terms and relationships using a local LLM.
    Pitfall 4 Fix: Recursive Context Injection via context_hints.
    """
    client = get_llm_client()
    
    system_prompt = EXTRACTOR_SYSTEM_PROMPT
    if context_hints:
        system_prompt += f"\n\n### CONTEXT HINTS (Priority Extraction):\n{context_hints}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Extract terms and relationships from the following text:\n\n{text}"}
    ]
    
    response = client.chat(messages, json_mode=True)
    return response

# Keeping legacy name for backward compatibility in tests
def extract_with_anchors(text: str) -> List[Dict]:
    return extract_with_llm(text)

def process_discovered_terms(discovered_terms: List[Dict], dictionary: Dictionary, 
                             source_file: str, is_seed: bool = False, graph_engine: Any = None,
                             confidence_levels: Dict[str, str] = None) -> List[str]:
    """
    Consolidated logic for updating the dictionary with discovered terms.
    Pitfall 6 Fix: Multi-Tiered Confidence Scoring.
    """
    terms_seen_in_current_doc = set()
    added_terms = []
    confidence_levels = confidence_levels or {}
    
    for item in discovered_terms:
        term = item.get("term")
        overview = item.get("overview")
        deep_dive = item.get("deep_dive")
        anchor = item.get("anchor") or item.get("usage_context", "")
        entity_type = item.get("entity_type")
        relationships = item.get("relationships", [])
        confidence = confidence_levels.get(term, "BRONZE")
        
        if not term: continue

        status = "ACTIVE"
        if overview == "[PENDING]" or not overview:
            status = "PENDING_DEFINITION"
            overview = "[PENDING]"
            confidence = "PENDING"

        if term in dictionary.entries:
            existing = dictionary.entries[term]
            
            # Upgrade Logic: If existing is PENDING and new is ACTIVE, upgrade it
            if existing.status == "PENDING_DEFINITION" and status == "ACTIVE":
                existing.overview = overview
                existing.deep_dive = deep_dive
                existing.status = "ACTIVE"
                existing.confidence_level = confidence
            
            # Confidence Upgrade
            confidence_order = {"PENDING": 0, "BRONZE": 1, "SILVER": 2, "GOLD": 3}
            if confidence_order.get(confidence, 0) > confidence_order.get(existing.confidence_level, 0):
                existing.confidence_level = confidence
            
            # Update deep_dive if it was empty but now we have info
            if not existing.deep_dive and deep_dive:
                existing.deep_dive = deep_dive
            
            existing.usage_examples.append(UsageExample(context=anchor, source=source_file))
            existing.last_seen = datetime.now().isoformat()
            
            if is_seed:
                existing.authority_level = "SEED"
                existing.is_golden = True

            if term not in terms_seen_in_current_doc:
                existing.document_count += 1
        else:
            dictionary.entries[term] = DictionaryEntry(
                term=term,
                overview=overview,
                deep_dive=deep_dive,
                source_file=source_file,
                entity_type=entity_type,
                usage_examples=[UsageExample(context=anchor, source=source_file)],
                last_seen=datetime.now().isoformat(),
                document_count=1,
                status=status,
                authority_level="SEED" if is_seed else "DISCOVERED",
                confidence_level=confidence,
                is_golden=is_seed
            )
            added_terms.append(term)

        terms_seen_in_current_doc.add(term)

        # Process Relationships if graph engine is provided
        if graph_engine:
            for rel in relationships:
                target = rel.get("target")
                rel_type = rel.get("type")
                if target and rel_type:
                    triplet = GraphTriplet(
                        subject=term,
                        relationship=rel_type,
                        object=target,
                        anchor=anchor,
                        source_file=source_file
                    )
                    graph_engine.add_triplet(triplet)
                    
    return added_terms
