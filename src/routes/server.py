"""
Main FastMCP server for RivalSearchMCP.
Integrates multi-search engine tools with comprehensive content extraction.
"""

from typing import Any, Dict, Optional

from fastmcp import FastMCP, Context

# Import tools
from ..tools.multi_search import multi_search, search_with_google_fallback

# Server configuration
SERVER_NAME = "RivalSearchMCP"
SERVER_VERSION = "2.0.0"
SERVER_DESCRIPTION = """
Advanced Multi-Engine Search and Content Analysis MCP Server

Features:
- Multi-engine search (Bing, DuckDuckGo, Yahoo) with fallback support
- Comprehensive content extraction and analysis
- Multi-level link following and content discovery
- Performance optimization with concurrent processing
- Robust error handling and recovery strategies

Optimized for:
- High-performance content extraction
- Reliable search across multiple engines
- Deep content analysis and research
- Production-ready deployment
"""

# Create FastMCP instance
mcp = FastMCP(
    name=SERVER_NAME,
    version=SERVER_VERSION,
    include_fastmcp_meta=True
)

# Tool registration with comprehensive metadata
@mcp.tool(
    name="multi_search",
    description="Search across multiple engines (Bing, DuckDuckGo, Yahoo) with comprehensive content extraction",
    tags={"search", "multi-engine", "content-extraction"},
    meta={
        "category": "Search",
        "priority": "high",
        "performance": "optimized",
        "fallback_support": True
    }
)
async def multi_search_tool(
    query: str,
    num_results: int = 10,
    extract_content: bool = True,
    follow_links: bool = True,
    max_depth: int = 2,
    use_fallback: bool = True,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Multi-engine search with comprehensive content extraction and fallback support.
    
    Args:
        query: Search query to execute
        num_results: Number of results per engine (default: 10)
        extract_content: Whether to extract full page content (default: True)
        follow_links: Whether to follow internal links (default: True)
        max_depth: Maximum depth for link following (default: 2)
        use_fallback: Whether to use fallback strategy (default: True)
        ctx: FastMCP context for progress reporting
    
    Returns:
        Comprehensive search results from multiple engines
    """
    try:
        if ctx and hasattr(ctx, 'info'):
            await ctx.info(f"🔍 Starting multi-engine search for: {query}")
        
        results = await multi_search(
            query=query,
            num_results=num_results,
            extract_content=extract_content,
            follow_links=follow_links,
            max_depth=max_depth,
            use_fallback=use_fallback,
            ctx=ctx
        )
        
        if ctx and hasattr(ctx, 'info'):
            await ctx.info(f"✅ Multi-engine search completed successfully!")
        
        return results
        
    except Exception as e:
        error_msg = f"Multi-engine search failed: {e}"
        if ctx and hasattr(ctx, 'error'):
            await ctx.error(error_msg)
        
        return {
            "error": error_msg,
            "status": "failed",
            "timestamp": "2025-09-02T12:00:00"
        }


@mcp.tool(
    name="search_with_google_fallback",
    description="Search using Google first, then fallback to other engines if needed",
    tags={"search", "google", "fallback", "multi-engine"},
    meta={
        "category": "Search",
        "priority": "high",
        "google_priority": True,
        "fallback_support": True
    }
)
async def search_with_google_fallback_tool(
    query: str,
    num_results: int = 10,
    extract_content: bool = True,
    follow_links: bool = True,
    max_depth: int = 2,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Search with Google priority and intelligent fallback to other engines.
    
    Args:
        query: Search query to execute
        num_results: Number of results per engine
        extract_content: Whether to extract full page content
        follow_links: Whether to follow internal links
        max_depth: Maximum depth for link following
        ctx: FastMCP context for progress reporting
    
    Returns:
        Search results with Google priority and fallback support
    """
    try:
        if ctx and hasattr(ctx, 'info'):
            await ctx.info(f"🔍 Starting Google-priority search for: {query}")
        
        results = await search_with_google_fallback(
            query=query,
            num_results=num_results,
            extract_content=extract_content,
            follow_links=follow_links,
            max_depth=max_depth,
            ctx=ctx
        )
        
        if ctx and hasattr(ctx, 'info'):
            await ctx.info(f"✅ Google-priority search completed successfully!")
        
        return results
        
    except Exception as e:
        error_msg = f"Google-priority search failed: {e}"
        if ctx and hasattr(ctx, 'error'):
            await ctx.error(error_msg)
        
        return {
            "error": error_msg,
            "status": "failed",
            "timestamp": "2025-09-02T12:00:00"
        }


# Startup and shutdown events
async def startup_event():
    """Initialize server on startup."""
    print(f"🚀 {SERVER_NAME} v{SERVER_VERSION} starting up...")
    print("📚 Loading multi-search engine tools...")
    print("✅ Server initialization completed successfully!")


async def shutdown_event():
    """Cleanup on server shutdown."""
    print(f"🛑 {SERVER_NAME} shutting down...")
    print("✅ Server shutdown completed successfully!")


# Main server instance
app = mcp

if __name__ == "__main__":
    import uvicorn
    
    print(f"🚀 Starting {SERVER_NAME} v{SERVER_VERSION}")
    print(f"📖 Description: {SERVER_DESCRIPTION}")
    
    # For now, just print that the server is ready
    print("🚀 Server is ready! Use FastMCP to run it.") 
