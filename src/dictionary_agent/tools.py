from .storage import load_dictionary
import difflib

def lookup_term(term: str, dictionary_path: str = "dictionary.json") -> str:
    dictionary = load_dictionary(dictionary_path)
    
    # Exact match
    if term in dictionary.entries:
        entry = dictionary.entries[term]
        return format_entry(entry)
    
    # Fuzzy match
    matches = difflib.get_close_matches(term, dictionary.entries.keys(), n=1, cutoff=0.6)
    if matches:
        closest_term = matches[0]
        entry = dictionary.entries[closest_term]
        return f"Exact term '{term}' not found. Closest match: '{closest_term}'\n\n{format_entry(entry)}"
    
    return f"Term '{term}' not found in dictionary."

def format_entry(entry) -> str:
    res = f"Term: {entry.term}\nDefinition: {entry.definition}\nSource: {entry.source_file}"
    if entry.usage_examples:
        res += "\n\nUsage Examples:"
        for ex in entry.usage_examples:
            res += f"\n- {ex.context} (Source: {ex.source})"
    if entry.related_terms:
        res += f"\n\nRelated Terms: {', '.join(entry.related_terms)}"
    return res

def main():
    import sys
    if len(sys.argv) < 3 or sys.argv[1] != "lookup":
        print("Usage: dictionary-lookup lookup <term>")
        sys.exit(1)
    
    term = " ".join(sys.argv[2:])
    print(lookup_term(term))

if __name__ == "__main__":
    main()
