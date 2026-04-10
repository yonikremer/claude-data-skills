from typing import List, Dict, Any, Optional
import os
from datetime import datetime
from .extractor import extract_all
from .filters import is_domain_specific
from .discovery import extract_with_llm, process_discovered_terms
from .validator import validate_with_llm
from .models import Dictionary, DictionaryEntry, UsageExample
from .graph_engine import GraphKnowledgeEngine
from .hashing import HashStore
from .strategic_filter import StrategicSieve
from .storage import load_dictionary, save_dictionary
from .llm_client import get_llm_client

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

    def get_bounty_hints(self) -> Optional[str]:
        """
        Pitfall 3 Fix: Bounty System. Identifies high-velocity pending terms.
        Bounty Capping (Second-Order Fix): Limit to top 10 to protect context window.
        """
        pending_entries = [
            e for e in self.dictionary.entries.values() 
            if e.status == "PENDING_DEFINITION" and e.document_count >= 3
        ]
        # Sort by ubiquity to find most important missing terms
        pending_entries.sort(key=lambda x: x.document_count, reverse=True)
        bounty_terms = [e.term for e in pending_entries[:10]] # Capped at 10
        
        if not bounty_terms:
            return None
        return "The following terms have been seen multiple times but lack a definition. Please prioritize finding their meanings: " + ", ".join(bounty_terms)

    def merge_conflicting_definitions(self, existing: DictionaryEntry, new_item: Dict[str, Any]) -> bool:
        """
        Synthesis Gate: Merges conflicting high-confidence definitions using an LLM.
        """
        # If both are high confidence (GOLD or SILVER) and overviews differ significantly
        confidence_order = {"PENDING": 0, "BRONZE": 1, "SILVER": 2, "GOLD": 3}
        new_conf = new_item.get("confidence_level", "BRONZE")
        
        if (confidence_order.get(existing.confidence_level, 0) >= 2 and 
            confidence_order.get(new_conf, 0) >= 2 and
            existing.overview.strip().lower() != new_item.get("overview", "").strip().lower()):
            
            print(f"Triggering Synthesis Gate for term: {existing.term}")
            client = get_llm_client()
            prompt = f"""You are a Master Lexicographer. Two authoritative sources have defined the same term differently. 
Your task is to SYNTHESIZE them into a single, unified definition that captures the nuances of both.

Term: {existing.term}
Definition A: {existing.overview}
Definition B: {new_item.get("overview")}

Deep Dive A: {existing.deep_dive or "None"}
Deep Dive B: {new_item.get("deep_dive") or "None"}

Provide a single JSON response with:
- overview: The synthesized 1-sentence summary.
- deep_dive: The combined technical details.
"""
            messages = [
                {"role": "system", "content": "Return JSON with 'overview' and 'deep_dive'."},
                {"role": "user", "content": prompt}
            ]
            
            try:
                synthesized = client.chat(messages, json_mode=True)
                existing.overview = synthesized.get("overview", existing.overview)
                existing.deep_dive = synthesized.get("deep_dive", existing.deep_dive)
                # Upgrade to highest confidence if merged
                existing.confidence_level = "GOLD" if "GOLD" in [existing.confidence_level, new_conf] else "SILVER"
                return True
            except:
                return False
        return False

    def reconcile_supersedes(self, subject: str, target: str):
        """
        Gate 4 Extension: If a new term SUPERSEDES an old one, update statuses.
        """
        if target in self.dictionary.entries:
            old_entry = self.dictionary.entries[target]
            if old_entry.status != "LEGACY":
                print(f"Temporal Reconciliation: {subject} SUPERSEDES {target}. Marking {target} as LEGACY.")
                old_entry.status = "LEGACY"
                
        # Also mark related relationships as legacy
        for rel in self.dictionary.relationships:
            if rel.subject == target or rel.object == target:
                if rel.status != "LEGACY":
                    rel.status = "LEGACY"

    def process_document(self, file_path: str, is_seed: bool = False) -> List[str]:
        """
        Runs the 5-gate pipeline on a document by processing it in metadata-aware chunks.
        """
        from .extractor import chunk_text
        from .discovery import process_discovered_terms
        
        # Gate 2: Extraction
        full_text = extract_all(file_path)
        if full_text.startswith("[Error"):
            return []

        # Pitfall: Large documents need chunking
        chunks = chunk_text(full_text, file_path)
        all_added_terms = []
        
        for chunk in chunks:
            # Pitfall 4 Fix: Recursive Context Injection
            context_hints = self.get_bounty_hints()
            discovered = extract_with_llm(chunk, context_hints=context_hints)
            
            valid_items = []
            confidence_map = {}
            
            for item in discovered:
                term = item.get("term")
                if not term: continue

                # Gate 3: Base-Knowledge Filter
                if not is_domain_specific(term, self.whitelist): continue
                    
                # Gate 5: Zero-Trust Validation (Pitfall 1 & 6 Fix)
                # Note: We validate against the chunk to ensure the anchor is present
                validation = validate_with_llm(chunk, item)
                if not validation.get("is_valid", False):
                    # Don't print for every common word failure to avoid noise
                    if validation.get("status") == "HALLUCINATION" and "Hard-Anchor" in validation.get("reasoning", ""):
                        print(f"Discarding Hallucination (No Anchor): {term}")
                    continue
                
                valid_items.append(item)
                confidence_map[term] = validation.get("confidence_level", "BRONZE")
                    
                # Temporal Reconciliation: Check for SUPERSEDES
                for rel in item.get("relationships", []):
                    if rel.get("type") == "SUPERSEDES":
                        self.reconcile_supersedes(term, rel.get("target"))

            # Gate 4: Temporal Reconciliation
            # Check for conflicts before processing
            for item in valid_items:
                term = item.get("term")
                if term in self.dictionary.entries:
                    item["confidence_level"] = confidence_map.get(term, "BRONZE")
                    self.merge_conflicting_definitions(self.dictionary.entries[term], item)

            added_terms = process_discovered_terms(
                valid_items, 
                self.dictionary, 
                file_path, 
                is_seed=is_seed, 
                graph_engine=self.graph_engine,
                confidence_levels=confidence_map
            )
            all_added_terms.extend(added_terms)
            
        return list(set(all_added_terms)) # Deduplicate added terms

    def generate_summary(self) -> str:
        """
        Generates a comprehensive summary of the agent's learning journey.
        """
        entries = list(self.dictionary.entries.values())
        total_terms = len(entries)
        active_entries = [e for e in entries if e.status == "ACTIVE"]
        pending_entries = [e for e in entries if e.status == "PENDING_DEFINITION"]
        
        # Sort by document_count to find most common terms
        common_terms = sorted(active_entries, key=lambda x: x.document_count, reverse=True)[:5]
        
        lines = [
            "\n" + "="*50,
            "📊 DICTIONARY AGENT LEARNING SUMMARY",
            "="*50,
            f"Total Concepts Tracked:  {total_terms}",
            f"Fully Defined Terms:     {len(active_entries)}",
            f"Pending Definitions:     {len(pending_entries)}",
            f"Knowledge Graph Links:   {len(self.dictionary.relationships)}",
            f"Identified Communities:  {len(self.dictionary.community_reports)}",
            "\n⭐ MOST COMMON TERMS:",
        ]
        
        for entry in common_terms:
            lines.append(f"• {entry.term} (seen in {entry.document_count} files)")
            lines.append(f"  Confidence: {entry.confidence_level}")
            lines.append(f"  Overview: {entry.overview}")
            if entry.deep_dive:
                # Show first 100 chars of deep dive
                dd_snippet = (entry.deep_dive[:100] + "...") if len(entry.deep_dive) > 100 else entry.deep_dive
                lines.append(f"  Deep Dive: {dd_snippet}")
            lines.append("")

        bounty_candidates = [e for e in pending_entries if e.document_count >= 3]
        if bounty_candidates:
            lines.append("🎯 BOUNTY LIST (Critical missing definitions):")
            for entry in sorted(bounty_candidates, key=lambda x: x.document_count, reverse=True)[:10]:
                lines.append(f"• {entry.term} (seen {entry.document_count} times)")
        elif pending_entries:
            lines.append("⏳ TOP PENDING CONCEPTS (Need more context):")
            for entry in sorted(pending_entries, key=lambda x: x.document_count, reverse=True)[:3]:
                lines.append(f"• {entry.term} (seen {entry.document_count} times)")
        
        lines.append("\n" + "="*50 + "\n")
        return "\n".join(lines)
