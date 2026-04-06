from typing import List, Dict, Any
import os
from .extractor import extract_all
from .filters import is_domain_specific
from .discovery import extract_with_llm, process_discovered_terms
from .validator import validate_with_llm
from .models import Dictionary
from .graph_engine import GraphKnowledgeEngine
from .hashing import HashStore
from .strategic_filter import StrategicSieve
from .storage import load_dictionary, save_dictionary

class DictionaryAgent:
    """
    The main entry point for the Dictionary Agent.
    Consolidates the 5-gate pipeline logic and the high-level agent interface.
    """
    def __init__(self, dictionary_path: str = None, whitelist: List[str] = None, 
                 hash_store: HashStore = None, strategic_sieve: StrategicSieve = None,
                 seed_paths: List[str] = None):
        self.dictionary_path = dictionary_path
        self.dictionary = load_dictionary(dictionary_path) if dictionary_path else Dictionary()
        self.whitelist = whitelist or []
        self.graph_engine = GraphKnowledgeEngine(self.dictionary)
        self.hash_store = hash_store or HashStore()
        self.strategic_sieve = strategic_sieve or StrategicSieve()
        self.seed_paths = seed_paths or []

    def scan_file(self, file_path: str):
        """Simple interface for scanning a single file."""
        return self.process_document(file_path)

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
                is_already_seed = any(os.path.samefile(path, s) for s in self.seed_paths if os.path.exists(s) and os.path.isfile(s))
                if is_already_seed:
                    continue
                files.append((path, os.path.getmtime(path)))
        
        files.sort(key=lambda x: x[1], reverse=True)
        
        for file_path, _ in files:
            # Gate 1: Strategic Sieve
            if not self.strategic_sieve.is_relevant(file_path):
                continue

            if not self.hash_store.has_changed(file_path):
                continue
            
            added = self.process_document(file_path)
            all_added.extend(added)
            
        self.hash_store.save()
        if self.dictionary_path:
            save_dictionary(self.dictionary, self.dictionary_path)
        return all_added

    def process_document(self, file_path: str, is_seed: bool = False) -> List[str]:
        """
        Runs the 5-gate pipeline on a single document.
        """
        # Gate 2: Extraction
        text = extract_all(file_path)
        if text.startswith("[Error"):
            return []

        # LLM Discovery
        discovered = extract_with_llm(text)
        valid_items = []
        
        for item in discovered:
            term = item.get("term")
            if not term: continue

            # Gate 3: Base-Knowledge Filter
            if not is_domain_specific(term, self.whitelist): continue
                
            # Gate 5: Zero-Trust Validation
            validation = validate_with_llm(text, item)
            if not validation.get("is_valid", False):
                print(f"Discarding Hallucination: {term}")
                continue
            
            valid_items.append(item)
                
        # Gate 4: Temporal Reconciliation
        added_terms = process_discovered_terms(
            valid_items, 
            self.dictionary, 
            file_path, 
            is_seed=is_seed, 
            graph_engine=self.graph_engine
        )
            
        return added_terms or []
