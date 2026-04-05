from typing import List, Dict, Any
import os
from .extractor import extract_all
from .filters import is_domain_specific
from .discovery import extract_with_llm
from .validator import validate_with_llm
from .models import Dictionary, DictionaryEntry, UsageExample, GraphTriplet
from .graph_engine import GraphKnowledgeEngine

class SelectiveKnowledgePipeline:
    def __init__(self, dictionary: Dictionary = None, whitelist: List[str] = None):
        self.dictionary = dictionary or Dictionary()
        self.whitelist = whitelist or []
        self.graph_engine = GraphKnowledgeEngine(self.dictionary)

    def process_document(self, file_path: str) -> List[str]:
        """
        Runs the full 4-gate pipeline on a document.
        Returns a list of successfully added terms.
        """
        # Gate 0: Extraction (Expanded formats)
        text = extract_all(file_path)
        if text.startswith("[Error"):
            print(f"Skipping {file_path}: {text}")
            return []

        added_terms = []
        
        # Gate 2: Extraction with LLM (Triplets + Anchors)
        discovered = extract_with_llm(text)
        
        for item in discovered:
            term = item.get("term")
            definition = item.get("definition")
            anchor = item.get("anchor")
            entity_type = item.get("entity_type")
            relationships = item.get("relationships", [])
            
            if not term:
                continue

            # Gate 1: Filter
            if not is_domain_specific(term, self.whitelist):
                continue
                
            # Gate 3: Validation
            validation = validate_with_llm(text, item)
            if not validation.get("is_valid", False):
                print(f"Discarding hallucination: {term} - {validation.get('reasoning')}")
                continue
                
            # Add to dictionary
            if term not in self.dictionary.entries:
                self.dictionary.entries[term] = DictionaryEntry(
                    term=term,
                    definition=definition,
                    source_file=file_path,
                    entity_type=entity_type,
                    usage_examples=[UsageExample(context=anchor, source=file_path)]
                )
                added_terms.append(term)
            else:
                entry = self.dictionary.entries[term]
                entry.usage_examples.append(UsageExample(context=anchor, source=file_path))
                if not entry.entity_type:
                    entry.entity_type = entity_type

            # Process Relationships (Graph Engine)
            for rel in relationships:
                target = rel.get("target")
                rel_type = rel.get("type")
                if target and rel_type:
                    triplet = GraphTriplet(
                        subject=term,
                        relationship=rel_type,
                        object=target,
                        anchor=anchor,
                        source_file=file_path
                    )
                    self.graph_engine.add_triplet(triplet)
                
        return added_terms
