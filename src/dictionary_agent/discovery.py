from typing import List, Dict, Any
from datetime import datetime
from .llm_client import get_llm_client
from .models import Dictionary, DictionaryEntry, UsageExample, GraphTriplet

EXTRACTOR_SYSTEM_PROMPT = """
You are a Senior Technical Librarian. Your task is to extract "Golden Terms" and "Semantic Triplets" from internal documentation. 

### THE RULES:
1. IDENTIFY: Unique project names (e.g., "Prism"), internal acronyms (e.g., "N-RT-RIC"), and specialized technical terms.
2. RELATIONSHIPS: Also identify triplets in format [Subject] --[Relationship]--> [Object].
   - Allowed Relationships: SUB_PROJECT_OF, DEPENDS_ON, USES, MANAGED_BY, REPLACES, ALIAS_OF.
3. CONTEXTUAL ALIASING: If you deduce that terms refer to the same project or concept (e.g., Hebrew and English terms), create an 'ALIAS_OF' relationship.
4. REJECT: Common industry terms (e.g., "SQL", "Docker", "API").
5. COLD START: If context is missing for a definition, set to "[PENDING]".
6. ANCHOR: Provide a verbatim, 100% accurate quote from the text for every term/triplet.

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

def process_discovered_terms(discovered_terms: List[Dict], dictionary: Dictionary, 
                             source_file: str, is_seed: bool = False, graph_engine: Any = None) -> List[str]:
    """
    Consolidated logic for updating the dictionary with discovered terms.
    Returns the list of terms that were newly added.
    """
    terms_seen_in_current_doc = set()
    added_terms = []
    
    for item in discovered_terms:
        term = item.get("term")
        definition = item.get("definition")
        anchor = item.get("anchor") or item.get("usage_context", "")
        entity_type = item.get("entity_type")
        relationships = item.get("relationships", [])
        
        if not term: continue

        status = "ACTIVE"
        if definition == "[PENDING]":
            status = "PENDING_DEFINITION"

        if term in dictionary.entries:
            existing = dictionary.entries[term]
            
            # Upgrade Logic: If existing is PENDING and new is ACTIVE, upgrade it
            if existing.status == "PENDING_DEFINITION" and status == "ACTIVE":
                existing.definition = definition
                existing.status = "ACTIVE"
            
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
                definition=definition,
                source_file=source_file,
                entity_type=entity_type,
                usage_examples=[UsageExample(context=anchor, source=source_file)],
                last_seen=datetime.now().isoformat(),
                document_count=1,
                status=status,
                authority_level="SEED" if is_seed else "DISCOVERED",
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
