#!/usr/bin/env python3
"""
RivalSearchMCP Server - Root entry point for FastMCP Cloud deployment
"""

# Import the mcp object from src.server
from src.server import mcp

if __name__ == "__main__":
    # For CLI compatibility, run directly with STDIO transport
    mcp.run()
