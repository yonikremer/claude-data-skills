import difflib
import os
from .storage import load_dictionary
from .graph_engine import GraphKnowledgeEngine

def lookup_term(term: str, dictionary_path: str = "GOLDEN_TERMS.json") -> str:
    # Use environment variable if set, otherwise default
    env_path = os.getenv("DICTIONARY_PATH")
    path = env_path or dictionary_path
    
    if not os.path.exists(path):
        return f"Error: Dictionary file '{path}' not found."

    dictionary = load_dictionary(path)
    graph_engine = GraphKnowledgeEngine(dictionary)

    # Exact match
    if term in dictionary.entries:
        return format_entry(term, dictionary, graph_engine)

    # Fuzzy match
    matches = difflib.get_close_matches(term, dictionary.entries.keys(), n=1, cutoff=0.6)
    if matches:
        closest_term = matches[0]
        return f"Exact term '{term}' not found. Closest match: '{closest_term}'\n\n{format_entry(closest_term, dictionary, graph_engine)}"

    return f"Term '{term}' not found in dictionary."

def format_entry(term: str, dictionary, graph_engine) -> str:
    entry = dictionary.entries[term]
    res = f"Term: {entry.term}\n"
    res += f"Overview: {entry.overview}\n"
    if entry.deep_dive:
        res += f"Deep Dive: {entry.deep_dive}\n"
    res += f"Status: {entry.status}\n"
    res += f"Authority: {entry.authority_level}\n"
    res += f"Ubiquity: Found in {entry.document_count} unique documents.\n"
    
    if entry.usage_examples:
        res += "\nUsage Examples:"
        # Only show last 3 examples to keep it concise
        for ex in entry.usage_examples[-3:]:
            res += f"\n- \"{ex.context}\" (Source: {os.path.basename(ex.source)})"
            
    # Add Knowledge Graph Context
    res += f"\n\n--- Knowledge Graph Context ---"
    neighbors = graph_engine.get_neighbors(term)
    if neighbors:
        for r in neighbors:
            res += f"\n- {r.subject} --[{r.relationship}]--> {r.object}"
    else:
        res += "\nNo relationships found."
        
    # Add Community Summary if available
    for report in dictionary.community_reports:
        if term in report.nodes:
            res += f"\n\n--- Community Executive Summary ---\n{report.summary}"
            break
            
    return res

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m graph_sieve.tools lookup <term>")
        sys.exit(1)

    # Allow 'lookup' subcommand or just the term
    args = sys.argv[1:]
    if args[0] == "lookup":
        term = " ".join(args[1:])
    else:
        term = " ".join(args)
        
    print(lookup_term(term))

if __name__ == "__main__":
    main()
