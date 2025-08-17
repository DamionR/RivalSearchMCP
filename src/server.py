"""
Modular FastMCP server for rival_search_mcp.
Uses modular tool registration while maintaining all functionality.
"""

import argparse
import sys
import os

# Add project root to path for imports
if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)

from mcp.server import FastMCP

# Import modular tool registration functions
from src.tools.web_tools import register_web_tools
from src.tools.reasoning_tools import register_reasoning_tools
from src.tools.data_tools import register_data_tools

# Import prompts and resources
from src.prompts import register_prompts
from src.resources import register_resources

# Create FastMCP server
mcp = FastMCP("rival-search")

# Register all tools using modular approach
register_web_tools(mcp)
register_reasoning_tools(mcp)
register_data_tools(mcp)

# Register prompts and resources
register_prompts(mcp)
register_resources(mcp)


def main():
    """Main entry point with transport selection."""
    parser = argparse.ArgumentParser(description="RivalSearchMCP Server")
    parser.add_argument("--transport", choices=["stdio", "http", "sse"], default="stdio",
                        help="Transport protocol to use (sse maps to streamable HTTP)")
    parser.add_argument("--host", default="localhost", help="Host for HTTP transport")
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP transport")
    
    args = parser.parse_args()
    
    if args.transport == "stdio":
        # STDIO transport (default for Claude Desktop)
        from src.logger import logger
        logger.info("Server started in STDIO mode, waiting for MCP input...")
        try:
            # Use the standard run() method for STDIO
            mcp.run()
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}")
            sys.exit(1)
    elif args.transport == "http":
        # HTTP transport using streamable-http
        from src.logger import logger
        logger.info(f"Server started in HTTP mode on {args.host}:{args.port}")
        mcp.run(transport="streamable-http")
    elif args.transport == "sse":
        # SSE transport
        from src.logger import logger
        logger.info(f"Server started in SSE mode on {args.host}:{args.port}")
        mcp.run(transport="sse")


if __name__ == "__main__":
    main()