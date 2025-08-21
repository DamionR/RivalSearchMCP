#!/usr/bin/env python3
"""
RivalSearchMCP Server - Advanced Web Research and Content Discovery
"""

import argparse
import sys

from fastmcp import FastMCP

# Import modular tool registration functions
from src.tools.retrieval_tools import register_retrieval_tools
from src.tools.search_tools import register_search_tools
from src.tools.traversal_tools import register_traversal_tools
from src.tools.analysis_tools import register_analysis_tools

# Import prompts and resources
from src.prompts import register_prompts
from src.resources import register_resources

# Import logger
from src.logger import logger

# Create FastMCP server instance
mcp = FastMCP("rival-search-mcp")

# Register all tools using modular approach
register_retrieval_tools(mcp)
register_search_tools(mcp)
register_traversal_tools(mcp)
register_analysis_tools(mcp)

# Register prompts and resources
register_prompts(mcp)
register_resources(mcp)

if __name__ == "__main__":
    # For CLI compatibility, run directly with STDIO transport
    mcp.run()