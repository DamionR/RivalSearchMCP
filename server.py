#!/usr/bin/env python3
"""
RivalSearchMCP Server - Advanced Web Research and Content Discovery
"""

from fastmcp import FastMCP

# Import modular tool registration functions
from src.tools.retrieval_tools import register_retrieval_tools
from src.tools.search_tools import register_search_tools
from src.tools.traversal_tools import register_traversal_tools
from src.tools.analysis_tools import register_analysis_tools

# Import prompts
from src.prompts import register_prompts

# Import logger
from src.logger import logger

# Create FastMCP server instance
app = FastMCP("rival-search-mcp")

# Register all tools using modular approach
register_retrieval_tools(app)
register_search_tools(app)
register_traversal_tools(app)
register_analysis_tools(app)

# Register prompts
register_prompts(app)

if __name__ == "__main__":
    # For CLI compatibility, run directly with STDIO transport
    app.run()