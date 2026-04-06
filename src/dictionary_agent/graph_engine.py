from typing import List, Dict, Any
import networkx as nx
from .models import Dictionary, GraphTriplet, DictionaryEntry, UsageExample, CommunityReport, RELATION_WEIGHTS
from .llm_client import get_llm_client

class GraphKnowledgeEngine:
    """
    Manages the Knowledge Graph state, clustering, and global reasoning.
    """
    def __init__(self, dictionary: Dictionary = None):
        self.dictionary = dictionary or Dictionary()

    def add_triplet(self, triplet: GraphTriplet):
        # 1. Assign weight based on relationship type
        triplet.weight = RELATION_WEIGHTS.get(triplet.relationship, 0.5)

        for existing in self.dictionary.relationships:
            if (existing.subject == triplet.subject and 
                existing.relationship == triplet.relationship and 
                existing.object == triplet.object):
                # Update existing triplet if it has a lower weight (e.g. was BRONZE before)
                existing.weight = max(existing.weight, triplet.weight)
                return
        self.dictionary.relationships.append(triplet)

    def get_neighbors(self, term: str) -> List[GraphTriplet]:
        return [r for r in self.dictionary.relationships 
                if r.subject == term or r.object == term]

    def build_nx_graph(self, prune_threshold: float = 0.0) -> nx.Graph:
        """
        Builds a NetworkX graph using weighted edges.
        """
        G = nx.Graph()
        for rel in self.dictionary.relationships:
            # Pitfall 2 Fix: Pruning weak edges before clustering
            if rel.weight < prune_threshold:
                continue
            G.add_edge(rel.subject, rel.object, type=rel.relationship, weight=rel.weight)
        return G

    def cluster_communities(self, prune_threshold: float = 0.4) -> List[List[str]]:
        """
        Groups nodes into communities using connected components.
        Prunes weak edges (e.g. USES, REPLACES) to avoid semantic drift.
        """
        G = self.build_nx_graph(prune_threshold=prune_threshold)
        if G.number_of_nodes() == 0:
            return []
        
        return [list(c) for f in [nx.connected_components(G)] for c in f]

    def generate_community_reports(self):
        """
        Uses an LLM to summarize each community for global reasoning.
        """
        communities = self.cluster_communities()
        client = get_llm_client()
        self.dictionary.community_reports = []

        for i, nodes in enumerate(communities):
            if len(nodes) < 2: continue # Skip singletons
            
            # Gather all info for this community
            context = []
            for node in nodes:
                entry = self.dictionary.entries.get(node)
                if entry:
                    info = f"Term: {node}, Overview: {entry.overview}"
                    if entry.deep_dive:
                        info += f", Deep Dive: {entry.deep_dive}"
                    context.append(info)
            
            rels = []
            for rel in self.dictionary.relationships:
                if rel.subject in nodes and rel.object in nodes:
                    rels.append(f"{rel.subject} --{rel.relationship} ({rel.weight})--> {rel.object}")

            prompt = f"Write a high-level summary report for this project community:\n\nNodes:\n" + "\n".join(context) + "\n\nRelationships:\n" + "\n".join(rels)
            
            messages = [
                {"role": "system", "content": """You are a Strategic Architect specializing in Complex Knowledge Mapping. 
Your goal is to summarize a "Project Community" (a cluster of related technical terms and relationships) into a high-level executive report.

Identify:
1. THE CORE MISSION: What is the primary purpose of this project cluster?
2. CRITICAL DEPENDENCIES: Key technical or structural links.
3. SEMANTIC HUB: The most central term(s) in the community.
4. GAPS: Any logical inconsistencies or missing definitions.

TONE: Objective, concise, and architectural."""},
                {"role": "user", "content": prompt}
            ]
            
            report_data = client.chat(messages, json_mode=False) # Get text summary
            
            self.dictionary.community_reports.append(CommunityReport(
                community_id=f"comm_{i}",
                title=f"Community {i}: " + ", ".join(nodes[:3]),
                summary=report_data,
                nodes=nodes
            ))

    def get_context_map(self, term: str) -> str:
        neighbors = self.get_neighbors(term)
        entry = self.dictionary.entries.get(term)
        
        lines = [f"Knowledge Graph Context for '{term}':"]
        if entry:
            lines.append(f"Ubiquity: Found in {entry.document_count} unique documents.")
            lines.append(f"Confidence Level: {entry.confidence_level}")
            
        for r in neighbors:
            lines.append(f"- {r.subject} --[{r.relationship} (w:{r.weight})]--> {r.object}")
        
        # Add Community Summary if available
        for report in self.dictionary.community_reports:
            if term in report.nodes:
                lines.append(f"\nExecutive Summary (Community Context):\n{report.summary}")
                break
                
        return "\n".join(lines)
