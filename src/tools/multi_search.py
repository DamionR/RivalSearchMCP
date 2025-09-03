"""
Multi-search engine tool for RivalSearchMCP.
Provides comprehensive search across multiple engines with fallback support.
"""

import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime

from fastmcp import Context
from src.core.search.core.multi_engines import MultiSearchResult
from src.core.search.engines.bing.bing_engine import BingSearchEngine
from src.core.search.engines.duckduckgo.duckduckgo_engine import DuckDuckGoSearchEngine
from src.core.search.engines.yahoo.yahoo_engine import YahooSearchEngine
from src.logging.logger import logger


class MultiSearchOrchestrator:
    """Orchestrates searches across multiple engines with fallback support."""
    
    def __init__(self):
        self.engines = {
            "bing": BingSearchEngine(),
            "duckduckgo": DuckDuckGoSearchEngine(),
            "yahoo": YahooSearchEngine()
        }
        self.engine_order = ["bing", "duckduckgo", "yahoo"]  # Priority order
    
    async def search_all_engines(
        self,
        query: str,
        num_results: int = 10,
        extract_content: bool = True,
        follow_links: bool = True,
        max_depth: int = 2,
        fallback_on_failure: bool = True
    ) -> Dict[str, Any]:
        """
        Search across all engines with fallback support.
        
        Args:
            query: Search query
            num_results: Number of results per engine
            extract_content: Whether to extract full page content
            follow_links: Whether to follow internal links
            max_depth: Maximum depth for link following
            fallback_on_failure: Whether to try other engines if one fails
        
        Returns:
            Dictionary with results from all engines
        """
        results = {}
        successful_engines = 0
        total_results = 0
        
        for engine_name in self.engine_order:
            try:
                logger.info(f"Searching {engine_name} for: {query}")
                engine = self.engines[engine_name]
                
                engine_results = await engine.search(
                    query=query,
                    num_results=num_results,
                    extract_content=extract_content,
                    follow_links=follow_links,
                    max_depth=max_depth
                )
                
                if engine_results:
                    results[engine_name] = {
                        "status": "success",
                        "count": len(engine_results),
                        "results": [result.to_dict() for result in engine_results],
                        "timestamp": datetime.now().isoformat()
                    }
                    successful_engines += 1
                    total_results += len(engine_results)
                    logger.info(f"{engine_name} search successful: {len(engine_results)} results")
                else:
                    results[engine_name] = {
                        "status": "no_results",
                        "count": 0,
                        "results": [],
                        "timestamp": datetime.now().isoformat()
                    }
                    logger.warning(f"{engine_name} returned no results")
                    
            except Exception as e:
                logger.error(f"{engine_name} search failed: {e}")
                results[engine_name] = {
                    "status": "failed",
                    "error": str(e),
                    "count": 0,
                    "results": [],
                    "timestamp": datetime.now().isoformat()
                }
                
                if not fallback_on_failure:
                    break
        
        # Generate summary
        summary = {
            "query": query,
            "engines_tested": len(self.engine_order),
            "successful_engines": successful_engines,
            "failed_engines": len(self.engine_order) - successful_engines,
            "total_results": total_results,
            "extract_content": extract_content,
            "follow_links": follow_links,
            "max_depth": max_depth,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "summary": summary,
            "results": results
        }
    
    async def search_with_fallback(
        self,
        query: str,
        num_results: int = 10,
        extract_content: bool = True,
        follow_links: bool = True,
        max_depth: int = 2
    ) -> Dict[str, Any]:
        """
        Search with intelligent fallback - if primary engine fails, try others.
        
        Args:
            query: Search query
            num_results: Number of results per engine
            extract_content: Whether to extract full page content
            follow_links: Whether to follow internal links
            max_depth: Maximum depth for link following
        
        Returns:
            Dictionary with results from working engines
        """
        # Try Bing first (most reliable)
        try:
            logger.info(f"Trying primary engine (Bing) for: {query}")
            bing_engine = self.engines["bing"]
            bing_results = await bing_engine.search(
                query=query,
                num_results=num_results,
                extract_content=extract_content,
                follow_links=follow_links,
                max_depth=max_depth
            )
            
            if bing_results:
                logger.info(f"Primary engine (Bing) successful: {len(bing_results)} results")
                return {
                    "primary_engine": "bing",
                    "status": "primary_success",
                    "results": {
                        "bing": {
                            "status": "success",
                            "count": len(bing_results),
                            "results": [result.to_dict() for result in bing_results],
                            "timestamp": datetime.now().isoformat()
                        }
                    },
                    "summary": {
                        "query": query,
                        "primary_engine": "bing",
                        "total_results": len(bing_results),
                        "extract_content": extract_content,
                        "follow_links": follow_links,
                        "max_depth": max_depth,
                        "timestamp": datetime.now().isoformat()
                    }
                }
        except Exception as e:
            logger.warning(f"Primary engine (Bing) failed: {e}")
        
        # Fallback to other engines
        logger.info("Primary engine failed, trying fallback engines...")
        return await self.search_all_engines(
            query=query,
            num_results=num_results,
            extract_content=extract_content,
            follow_links=follow_links,
            max_depth=max_depth,
            fallback_on_failure=True
        )
    
    async def close_all_engines(self):
        """Close all engine sessions."""
        for engine in self.engines.values():
            try:
                await engine.close()
            except Exception as e:
                logger.debug(f"Error closing engine: {e}")


# Global orchestrator instance
_orchestrator = None


def get_orchestrator() -> MultiSearchOrchestrator:
    """Get or create the global orchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = MultiSearchOrchestrator()
    return _orchestrator


async def multi_search(
    query: str,
    num_results: int = 10,
    extract_content: bool = True,
    follow_links: bool = True,
    max_depth: int = 2,
    use_fallback: bool = True,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Multi-engine search with comprehensive content extraction.
    
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
        if ctx and hasattr(ctx, 'report_progress'):
            await ctx.report_progress(0.1)
        
        orchestrator = get_orchestrator()
        
        if ctx and hasattr(ctx, 'report_progress'):
            await ctx.report_progress(0.2)
        
        if use_fallback:
            results = await orchestrator.search_with_fallback(
                query=query,
                num_results=num_results,
                extract_content=extract_content,
                follow_links=follow_links,
                max_depth=max_depth
            )
        else:
            results = await orchestrator.search_all_engines(
                query=query,
                num_results=num_results,
                extract_content=extract_content,
                follow_links=follow_links,
                max_depth=max_depth
            )
        
        if ctx and hasattr(ctx, 'report_progress'):
            await ctx.report_progress(1.0)
        if ctx and hasattr(ctx, 'info'):
            await ctx.info(f"✅ Search completed: {results['summary']['total_results']} total results from {results['summary']['successful_engines']} engines")
        
        return results
        
    except Exception as e:
        error_msg = f"Multi-engine search failed: {e}"
        logger.error(error_msg)
        if ctx and hasattr(ctx, 'error'):
            await ctx.error(error_msg)
        
        return {
            "error": error_msg,
            "status": "failed",
            "timestamp": datetime.now().isoformat()
        }


async def search_with_google_fallback(
    query: str,
    num_results: int = 10,
    extract_content: bool = True,
    follow_links: bool = True,
    max_depth: int = 2,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Search using Google first, then fallback to other engines if needed.
    
    Args:
        query: Search query to execute
        num_results: Number of results per engine
        extract_content: Whether to extract full page content
        follow_links: Whether to follow internal links
        max_depth: Maximum depth for link following
        ctx: FastMCP context for progress reporting
    
    Returns:
        Search results with Google priority
    """
    try:
        if ctx and hasattr(ctx, 'info'):
            await ctx.info(f"🔍 Starting Google-priority search for: {query}")
        if ctx and hasattr(ctx, 'report_progress'):
            await ctx.report_progress(0.1)
        
        # TODO: Implement Google search integration
        # For now, use multi-engine search as fallback
        if ctx and hasattr(ctx, 'warning'):
            await ctx.warning("Google search not yet implemented, using multi-engine fallback")
        if ctx and hasattr(ctx, 'report_progress'):
            await ctx.report_progress(0.5)
        
        return await multi_search(
            query=query,
            num_results=num_results,
            extract_content=extract_content,
            follow_links=follow_links,
            max_depth=max_depth,
            use_fallback=True,
            ctx=ctx
        )
        
    except Exception as e:
        error_msg = f"Google-priority search failed: {e}"
        logger.error(error_msg)
        if ctx and hasattr(ctx, 'error'):
            await ctx.error(error_msg)
        
        return {
            "error": error_msg,
            "status": "failed",
            "timestamp": datetime.now().isoformat()
        }
