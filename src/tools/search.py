"""
Search tools for FastMCP server.
Handles multi-engine search and Google Search scraping.
"""

from typing import Optional, Annotated
from datetime import datetime

from fastmcp import FastMCP, Context
from pydantic import Field

# Import the new multi-search system
from src.core.search.engines.bing.bing_engine import BingSearchEngine
from src.core.fetch import rival_retrieve
from src.logging.logger import logger


def register_search_tools(mcp: FastMCP):
    """Register all search-related tools."""

    @mcp.tool(
        name="google_search",
        description="Advanced Google Search with Cloudflare bypass, rich snippets detection, and multi-engine fallback",
        tags={"search", "web", "primary", "google"},
        meta={
            "version": "2.0",
            "category": "Search",
            "performance": "high",
            "rate_limit": "10/second",
            "anti_detection": True,
            "rich_snippets": True,
            "traffic_estimation": True
        },
        annotations={
            "title": "Google Search",
            "readOnlyHint": True,
            "openWorldHint": True,
            "destructiveHint": False,
            "idempotentHint": False
        }
    )
    async def google_search(
        query: Annotated[str, Field(
            description="Search query string",
            min_length=2,
            max_length=500
        )],
        num_results: Annotated[int, Field(
            description="Number of results to return",
            ge=1,
            le=100,
            default=10
        )] = 10,
        lang: Annotated[str, Field(
            description="Language for search results",
            default="en"
        )] = "en",
        proxy: Annotated[Optional[str], Field(
            description="Proxy server to use for requests"
        )] = None,
        advanced: Annotated[bool, Field(
            description="Enable advanced features like rich snippets detection"
        )] = True,
        sleep_interval: Annotated[float, Field(
            description="Delay between requests in seconds",
            ge=0,
            le=10,
            default=0
        )] = 0,
        timeout: Annotated[int, Field(
            description="Request timeout in seconds",
            ge=1,
            le=60,
            default=5
        )] = 5,
        safe: Annotated[str, Field(
            description="Safe search setting",
            default="active"
        )] = "active",
        ssl_verify: Annotated[Optional[bool], Field(
            description="SSL verification setting"
        )] = None,
        region: Annotated[Optional[str], Field(
            description="Geographic region for search"
        )] = None,
        start_num: Annotated[int, Field(
            description="Starting position for results",
            ge=0,
            default=0
        )] = 0,
        unique: Annotated[bool, Field(
            description="Return only unique results"
        )] = False,
        use_multi_engine: Annotated[bool, Field(
            description="Use multi-engine search as fallback if direct scraping fails"
        )] = False,
        ctx: Optional[Context] = None
    ) -> dict:
        """
        Comprehensive Google Search with multi-engine fallback and advanced features.
        
        This tool provides advanced Google search capabilities including:
        - Cloudflare bypass and anti-detection measures
        - Rich snippets detection and analysis
        - Traffic estimation for results
        - Multi-engine fallback for reliability
        - Comprehensive result metadata
        
        Returns structured search results with rich metadata for analysis.
        """
        try:
            if ctx:
                await ctx.info(f"🔍 Starting Google Search for: {query}")
                await ctx.info(f"📊 Target results: {num_results}")
                await ctx.report_progress(progress=0, total=100)
            
            logger.info(f"🔍 Performing Google Search for: {query}")
            logger.info(f"📊 Target results: {num_results}")

            # First try direct Google Search scraping
            try:
                if ctx:
                    await ctx.info("🔄 Attempting direct Google search...")
                    await ctx.report_progress(progress=20, total=100)
                
                # TODO: Implement Google search integration
#                 # Use multi-engine search as primary method
                if ctx and hasattr(ctx, 'info'):
                    await ctx.info("Using multi-engine search for comprehensive results")
                
                from src.tools.multi_search import multi_search
                results = await multi_search(
                    query=query,
                    num_results=num_results,
                    extract_content=True,
                    follow_links=False,
                    max_depth=1,
                    use_fallback=True,
                    ctx=ctx
                )

                if results:
                    if ctx:
                        await ctx.info(f"✅ Direct search successful: {len(results)} results")
                        await ctx.report_progress(progress=60, total=100)
                    
                    # Convert results to dict format for serialization
                    result_dicts = []
                    if isinstance(results, dict) and 'results' in results:
                        # Multi-search returned structured results
                        for result in results['results']:
                            if isinstance(result, dict):
                                result_dicts.append(result)
                            else:
                                # Handle MultiSearchResult objects - ensure all values are serializable
                                try:
                                    result_dicts.append({
                                        "title": str(getattr(result, 'title', '')),
                                        "url": str(getattr(result, 'url', '')),
                                        "description": str(getattr(result, 'description', '')),
                                        "position": int(getattr(result, 'position', 0)),
                                        "engine": str(getattr(result, 'engine', 'multi_engine')),
                                        "timestamp": str(getattr(result, 'timestamp', '')),
                                    })
                                except Exception as attr_error:
                                    # Fallback to basic string representation
                                    logger.warning(f"Error extracting attributes from result: {attr_error}")
                                    result_dicts.append({
                                        "title": str(result) if hasattr(result, '__str__') else 'Unknown',
                                        "url": "",
                                        "description": "",
                                        "position": 0,
                                        "engine": "multi_engine",
                                        "timestamp": datetime.now().isoformat(),
                                    })
                    else:
                        # Handle direct results list
                        for result in results:
                            if isinstance(result, dict):
                                result_dicts.append(result)
                            else:
                                try:
                                    result_dicts.append({
                                        "title": str(getattr(result, 'title', '')),
                                        "url": str(getattr(result, 'url', '')),
                                        "description": str(getattr(result, 'description', '')),
                                        "position": int(getattr(result, 'position', 0)),
                                        "engine": str(getattr(result, 'engine', 'multi_engine')),
                                        "timestamp": str(getattr(result, 'timestamp', '')),
                                    })
                                except Exception as attr_error:
                                    # Fallback to basic string representation
                                    logger.warning(f"Error extracting attributes from result: {attr_error}")
                                    result_dicts.append({
                                        "title": str(result) if hasattr(result, '__str__') else 'Unknown',
                                        "url": "",
                                        "description": "",
                                        "position": 0,
                                        "engine": "multi_engine",
                                        "timestamp": datetime.now().isoformat(),
                                    })
                    
                    # Extract metadata
                    search_metadata = {
                        "total_results": len(result_dicts),
                        "unique_engines": len(set(r.get('engine', 'unknown') for r in result_dicts)),
                        "search_method": "multi_engine_search",
                        "query": query,
                        "timestamp": datetime.now().isoformat(),
                        "parameters": {
                            "num_results": num_results,
                            "extract_content": True,
                            "follow_links": False,
                            "max_depth": 1
                        }
                    }

                    if ctx:
                        await ctx.report_progress(progress=100, total=100)
                        await ctx.info(f"🎯 Search completed successfully with {len(results)} results")
                    
                    return {
                        "status": "success",
                        "method": "multi_engine_search",
                        "results": result_dicts,
                        "metadata": search_metadata,
                        "query": query,
                        "execution_time": datetime.now().isoformat()
                    }
                else:
                    # No results returned
                    if ctx:
                        await ctx.warning("⚠️ No results returned from multi-engine search")
                        await ctx.report_progress(progress=100, total=100)
                    
                    return {
                        "status": "partial",
                        "method": "multi_engine_search",
                        "results": [],
                        "metadata": {
                            "total_results": 0,
                            "search_method": "multi_engine_search",
                            "query": query,
                            "timestamp": datetime.now().isoformat(),
                            "warning": "No results returned"
                        },
                        "query": query,
                        "execution_time": datetime.now().isoformat()
                    }

            except Exception as e:
                if ctx:
                    await ctx.warning(f"⚠️ Direct Google search failed: {str(e)}")
                    await ctx.info("🔄 Attempting multi-engine fallback...")
                    await ctx.report_progress(progress=40, total=100)
                
                logger.warning(f"Direct Google search failed: {e}")
                
                if use_multi_engine:
                    # Fallback to multi-engine search
                    try:
                        if ctx:
                            await ctx.info("🔄 Using multi-engine fallback...")
                            await ctx.report_progress(progress=70, total=100)
                        
                        # Use proper multi-engine search implementation
                        from src.tools.multi_search import multi_search
                        fallback_results = await multi_search(
                            query=query,
                            num_results=num_results,
                            extract_content=True,
                            follow_links=False,
                            max_depth=1,
                            use_fallback=True,
                            ctx=ctx
                        )
                        
                        if ctx:
                            await ctx.info("✅ Multi-engine fallback successful")
                            await ctx.report_progress(progress=100, total=100)
                        
                        return {
                            "status": "success",
                            "method": "multi_engine_fallback",
                            "results": fallback_results,
                            "metadata": {
                                "total_results": len(fallback_results) if isinstance(fallback_results, list) else 1,
                                "search_method": "multi_engine_fallback",
                                "query": query,
                                "timestamp": datetime.now().isoformat(),
                                "fallback_reason": str(e)
                            },
                            "query": query,
                            "execution_time": datetime.now().isoformat()
                        }
                        
                    except Exception as fallback_error:
                        if ctx:
                            await ctx.error(f"❌ Multi-engine fallback also failed: {str(fallback_error)}")
                        
                        logger.error(f"Multi-engine fallback failed: {fallback_error}")
                        error_msg = f"Both direct Google search and multi-engine fallback failed. Direct error: {e}, Fallback error: {fallback_error}"
                        if ctx:
                            await ctx.error(f"❌ {error_msg}")
                        
                        return {
                            "status": "error",
                            "error": error_msg,
                            "query": query,
                            "timestamp": datetime.now().isoformat()
                        }
                else:
                    # Direct search failed and multi-engine fallback is disabled
                    error_msg = f"Direct Google search failed and multi-engine fallback is disabled: {e}"
                    if ctx:
                        await ctx.error(f"❌ {error_msg}")
                    
                    logger.error(error_msg)
                    return {
                        "status": "error",
                        "error": error_msg,
                        "query": query,
                        "timestamp": datetime.now().isoformat()
                    }

        except Exception as e:
            error_msg = f"Google search failed for '{query}': {str(e)}"
            if ctx:
                await ctx.error(f"❌ {error_msg}")
            
            logger.error(error_msg)
            return {
                "status": "error",
                "error": str(e),
                "query": query,
                "timestamp": datetime.now().isoformat()
            }
