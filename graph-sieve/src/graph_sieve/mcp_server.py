import os
from mcp.server.fastmcp import FastMCP
from .tools import lookup_term
from .whois import get_expert_info

# Create an MCP server
mcp = FastMCP("DictionaryAgent")

@mcp.tool()
def lookup(term: str) -> str:
    """
    Lookup a technical term, project name, or acronym in the internal knowledge graph.
    Returns the definition, status, and relationship context.
    """
    # Ensure the path is relative to the project root or uses the environment variable
    return lookup_term(term)

@mcp.tool()
def whois(term: str) -> str:
    """
    Find technical experts, managers, and organizational context for a given term.
    """
    return get_expert_info(term)

if __name__ == "__main__":
    # When running as a standalone script for testing
    mcp.run()
