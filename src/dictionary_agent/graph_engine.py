from typing import List, Dict, Any
from .models import Dictionary, GraphTriplet, DictionaryEntry, UsageExample
from .storage import save_dictionary, load_dictionary

class GraphKnowledgeEngine:
    """
    Manages the Knowledge Graph state within the Dictionary object.
    """
    def __init__(self, dictionary: Dictionary = None):
        self.dictionary = dictionary or Dictionary()

    def add_triplet(self, triplet: GraphTriplet):
        """
        Adds a validated triplet to the graph if it doesn't already exist.
        """
        # Check for duplicates
        for existing in self.dictionary.relationships:
            if (existing.subject == triplet.subject and 
                existing.relationship == triplet.relationship and 
                existing.object == triplet.object):
                return
        
        self.dictionary.relationships.append(triplet)

    def get_neighbors(self, term: str) -> List[GraphTriplet]:
        """
        Returns all relationships involving the given term.
        """
        return [r for r in self.dictionary.relationships 
                if r.subject == term or r.object == term]

    def get_context_map(self, term: str) -> str:
        """
        Returns a string representation of the term's neighborhood for AI context.
        """
        neighbors = self.get_neighbors(term)
        if not neighbors:
            return f"No known relationships for {term}."
            
        lines = [f"Knowledge Graph Context for '{term}':"]
        for r in neighbors:
            lines.append(f"- {r.subject} --[{r.relationship}]--> {r.object}")
        return "\n".join(lines)
