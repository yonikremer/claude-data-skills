import os
from mcp.server.fastmcp import FastMCP
from .tools import lookup_term

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

if __name__ == "__main__":
    # When running as a standalone script for testing
    mcp.run()
