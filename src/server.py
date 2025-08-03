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

from mcp.server.fastmcp import FastMCP

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
                        help="Transport protocol to use")
    parser.add_argument("--host", default="localhost", help="Host for HTTP/SSE transport")
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP transport")
    parser.add_argument("--sse-port", type=int, default=8001, help="Port for SSE transport")
    
    args = parser.parse_args()
    
    if args.transport == "stdio":
        # STDIO transport (default for Claude Desktop)
        mcp.run()
    elif args.transport == "http":
        # HTTP transport 
        import uvicorn
        from mcp.server.fastmcp.server import create_fastmcp_httpx_server
        
        app = create_fastmcp_httpx_server(mcp)
        uvicorn.run(app, host=args.host, port=args.port)
    elif args.transport == "sse":
        # SSE transport
        import uvicorn
        from mcp.server.fastmcp.server import create_fastmcp_sse_server
        
        app = create_fastmcp_sse_server(mcp)
        uvicorn.run(app, host=args.host, port=args.sse_port)


if __name__ == "__main__":
    main()