from typing import List, Dict, Any
import os
from datetime import datetime
from .extractor import extract_all
from .filters import is_domain_specific
from .discovery import extract_with_llm
from .validator import validate_with_llm
from .models import Dictionary, DictionaryEntry, UsageExample, GraphTriplet
from .graph_engine import GraphKnowledgeEngine
from .hashing import HashStore

class SelectiveKnowledgePipeline:
    def __init__(self, dictionary: Dictionary = None, whitelist: List[str] = None, hash_store: HashStore = None):
        self.dictionary = dictionary or Dictionary()
        self.whitelist = whitelist or []
        self.graph_engine = GraphKnowledgeEngine(self.dictionary)
        self.hash_store = hash_store or HashStore()

    def process_directory(self, dir_path: str) -> List[str]:
        """
        Processes all documents in a directory in reverse-chronological order.
        """
        all_added = []
        files = []
        for root, _, filenames in os.walk(dir_path):
            for f in filenames:
                path = os.path.join(root, f)
                files.append((path, os.path.getmtime(path)))
        
        # Sort by mtime descending (newest first)
        files.sort(key=lambda x: x[1], reverse=True)
        
        for file_path, _ in files:
            if not self.hash_store.has_changed(file_path):
                print(f"Skipping unchanged file: {file_path}")
                continue
            
            added = self.process_document(file_path)
            all_added.extend(added)
            
        self.hash_store.save()
        return all_added

    def process_document(self, file_path: str) -> List[str]:
        """
        Runs the full 4-gate pipeline on a document.
        """
        text = extract_all(file_path)
        if text.startswith("[Error"):
            return []

        added_terms = []
        discovered = extract_with_llm(text)
        
        for item in discovered:
            term = item.get("term")
            definition = item.get("definition")
            anchor = item.get("anchor")
            entity_type = item.get("entity_type")
            relationships = item.get("relationships", [])
            
            if not term: continue

            if not is_domain_specific(term, self.whitelist): continue
                
            validation = validate_with_llm(text, item)
            if not validation.get("is_valid", False): continue
                
            # Temporal Reconciliation: If term exists, check for conflict
            if term in self.dictionary.entries:
                existing = self.dictionary.entries[term]
                # If existing is OLDER than current doc (we process newest first, so existing is NEWER)
                # But if we are doing a re-index or manual run, we trust the newest document.
                # Here, we append usage. If the definition is DIFFERENT, we can flag the old one.
                existing.usage_examples.append(UsageExample(context=anchor, source=file_path))
                existing.last_seen = datetime.now().isoformat()
            else:
                self.dictionary.entries[term] = DictionaryEntry(
                    term=term,
                    definition=definition,
                    source_file=file_path,
                    entity_type=entity_type,
                    usage_examples=[UsageExample(context=anchor, source=file_path)],
                    last_seen=datetime.now().isoformat()
                )
                added_terms.append(term)

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
