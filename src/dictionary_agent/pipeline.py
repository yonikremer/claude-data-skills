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
from .strategic_filter import StrategicSieve

class SelectiveKnowledgePipeline:
    def __init__(self, dictionary: Dictionary = None, whitelist: List[str] = None, 
                 hash_store: HashStore = None, strategic_sieve: StrategicSieve = None,
                 seed_paths: List[str] = None, chunk_size: int = 2000):
        self.dictionary = dictionary or Dictionary()
        self.whitelist = whitelist or []
        self.graph_engine = GraphKnowledgeEngine(self.dictionary)
        self.hash_store = hash_store or HashStore()
        self.strategic_sieve = strategic_sieve or StrategicSieve()
        self.seed_paths = seed_paths or []
        self.chunk_size = chunk_size

    def process_directory(self, dir_path: str) -> List[str]:
        """
        Processes documents, starting with seed documents if provided.
        """
        all_added = []
        
        # 1. Process Seeds First
        for seed in self.seed_paths:
            if os.path.isfile(seed):
                all_added.extend(self.process_document(seed, is_seed=True))
            elif os.path.isdir(seed):
                # Process directory as seeds
                for root, _, filenames in os.walk(seed):
                    for f in filenames:
                        path = os.path.join(root, f)
                        all_added.extend(self.process_document(path, is_seed=True))

        # 2. Process Remaining Docs in reverse-chronological order
        files = []
        for root, _, filenames in os.walk(dir_path):
            for f in filenames:
                path = os.path.join(root, f)
                # Skip if already processed as seed
                if any(os.path.samefile(path, s) for s in self.seed_paths if os.path.exists(s) and os.path.isfile(path)):
                    continue
                files.append((path, os.path.getmtime(path)))
        
        # Sort by mtime descending (newest first)
        files.sort(key=lambda x: x[1], reverse=True)
        
        for file_path, _ in files:
            # Gate 1: Strategic Sieve (Prune decommissioned projects)
            if not self.strategic_sieve.is_relevant(file_path):
                reason = self.strategic_sieve.get_reason_skipped(file_path)
                print(f"Skipping Gate 1 (Strategic): {file_path} - {reason}")
                continue

            if not self.hash_store.has_changed(file_path):
                print(f"Skipping cached file: {file_path}")
                continue
            
            added = self.process_document(file_path)
            all_added.extend(added)
            
        self.hash_store.save()
        return all_added

    def process_document(self, file_path: str, is_seed: bool = False) -> List[str]:
        """
        Runs the 5-gate pipeline on a single document.
        """
        # Gate 2: Extraction (Expanded formats)
        text = extract_all(file_path)
        if text.startswith("[Error"):
            return []

        added_terms = []
        discovered = extract_with_llm(text)
        terms_seen_in_current_doc = set()
        
        for item in discovered:
            term = item.get("term")
            definition = item.get("definition")
            anchor = item.get("anchor")
            entity_type = item.get("entity_type")
            relationships = item.get("relationships", [])
            
            if not term: continue

            # Gate 3: Base-Knowledge Filter
            if not is_domain_specific(term, self.whitelist): continue
                
            # Gate 5: Zero-Trust Validation
            validation = validate_with_llm(text, item)
            if not validation.get("is_valid", False):
                print(f"Discarding Gate 5 (Hallucination): {term}")
                continue
                
            # Temporal Reconciliation & Document Counting
            status = "ACTIVE"
            if definition == "[PENDING]":
                status = "PENDING_DEFINITION"

            if term in self.dictionary.entries:
                existing = self.dictionary.entries[term]
                
                # Upgrade Logic: If existing is PENDING and new is ACTIVE, upgrade it
                if existing.status == "PENDING_DEFINITION" and status == "ACTIVE":
                    existing.definition = definition
                    existing.status = "ACTIVE"
                
                existing.usage_examples.append(UsageExample(context=anchor, source=file_path))
                existing.last_seen = datetime.now().isoformat()
                
                if is_seed:
                    existing.authority_level = "SEED"
                    existing.is_golden = True

                if term not in terms_seen_in_current_doc:
                    existing.document_count += 1
            else:
                self.dictionary.entries[term] = DictionaryEntry(
                    term=term,
                    definition=definition,
                    source_file=file_path,
                    entity_type=entity_type,
                    usage_examples=[UsageExample(context=anchor, source=file_path)],
                    last_seen=datetime.now().isoformat(),
                    document_count=1,
                    status=status,
                    authority_level="SEED" if is_seed else "DISCOVERED",
                    is_golden=is_seed
                )
                added_terms.append(term)

            terms_seen_in_current_doc.add(term)

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
