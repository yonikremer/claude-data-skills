from typing import List, Dict, Any
import networkx as nx
from .models import Dictionary, GraphTriplet, DictionaryEntry, UsageExample, CommunityReport
from .llm_client import get_llm_client

class GraphKnowledgeEngine:
    """
    Manages the Knowledge Graph state, clustering, and global reasoning.
    """
    def __init__(self, dictionary: Dictionary = None):
        self.dictionary = dictionary or Dictionary()

    def add_triplet(self, triplet: GraphTriplet):
        for existing in self.dictionary.relationships:
            if (existing.subject == triplet.subject and 
                existing.relationship == triplet.relationship and 
                existing.object == triplet.object):
                return
        self.dictionary.relationships.append(triplet)

    def get_neighbors(self, term: str) -> List[GraphTriplet]:
        return [r for r in self.dictionary.relationships 
                if r.subject == term or r.object == term]

    def build_nx_graph(self) -> nx.Graph:
        G = nx.Graph()
        for rel in self.dictionary.relationships:
            G.add_edge(rel.subject, rel.object, type=rel.relationship)
        return G

    def cluster_communities(self) -> List[List[str]]:
        """
        Groups nodes into communities using connected components (simple) 
        or Louvain (advanced).
        """
        G = self.build_nx_graph()
        if G.number_of_nodes() == 0:
            return []
        
        # Using connected components for a robust local implementation
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
                    context.append(f"Term: {node}, Def: {entry.definition}")
            
            rels = []
            for rel in self.dictionary.relationships:
                if rel.subject in nodes and rel.object in nodes:
                    rels.append(f"{rel.subject} --{rel.relationship}--> {rel.object}")

            prompt = f"Write a high-level summary report for this project community:\n\nNodes:\n" + "\n".join(context) + "\n\nRelationships:\n" + "\n".join(rels)
            
            messages = [
                {"role": "system", "content": "You are a Strategic Architect. Summarize the following project cluster into a coherent executive report."},
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
            
        for r in neighbors:
            lines.append(f"- {r.subject} --[{r.relationship}]--> {r.object}")
        
        # Add Community Summary if available
        for report in self.dictionary.community_reports:
            if term in report.nodes:
                lines.append(f"\nExecutive Summary (Community Context):\n{report.summary}")
                break
                
        return "\n".join(lines)
