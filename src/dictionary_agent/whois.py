import sys
import os
from .storage import load_dictionary
from .graph_engine import GraphKnowledgeEngine

def get_expert_info(term: str, dictionary_path: str = "GOLDEN_TERMS.json") -> str:
    # Use environment variable if set, otherwise default
    env_path = os.getenv("DICTIONARY_PATH")
    path = env_path or dictionary_path
    
    if not os.path.exists(path):
        return f"Error: Dictionary file '{path}' not found."

    dictionary = load_dictionary(path)
    engine = GraphKnowledgeEngine(dictionary)
    
    # Get all neighbors (including flipped/inverse relationships)
    neighbors = engine.get_neighbors(term)
    
    experts = []
    managers = []
    orgs = []
    
    for r in neighbors:
        if r.relationship == "HAS_EXPERT":
            experts.append(r.object)
        elif r.relationship == "IS_EXPERT_OF": # Term perspective: Person IS_EXPERT_OF Term
            experts.append(r.subject)
            
        elif r.relationship == "MANAGES":
            managers.append(r.object)
        elif r.relationship == "IS_MANAGER_OF":
            managers.append(r.subject)
            
        elif r.relationship == "IS_SUB_ORGANIZATION_OF":
            orgs.append(r.object)
        elif r.relationship == "HAS_SUB_ORGANIZATION":
            orgs.append(r.subject)
            
    res = f"Who is responsible for: {term}\n"
    res += "=" * (len(term) + 25) + "\n"
    
    if experts:
        res += f"Technical Experts: {', '.join(set(experts))}\n"
    else:
        res += "Technical Experts: No specific experts identified in graph.\n"
        
    if managers:
        res += f"Managers/Owners:   {', '.join(set(managers))}\n"
    else:
        res += "Managers/Owners:   No specific managers identified in graph.\n"
        
    if orgs:
        res += f"Organization:      {', '.join(set(orgs))}\n"
        
    # Check for reports
    reports = [r.object for r in neighbors if r.relationship == "HAS_DIRECT_REPORT"]
    if reports:
        res += f"Direct Reports:    {', '.join(set(reports))}\n"
        
    return res

def main():
    if len(sys.argv) < 2:
        print("Usage: dictionary-whois <term>")
        sys.exit(1)

    term = " ".join(sys.argv[1:])
    print(get_expert_info(term))

if __name__ == "__main__":
    main()
