"""
Search tools for FastMCP server.
Handles multi-engine search and Google Search scraping.
"""

from typing import Optional
from fastmcp import FastMCP

from src.core.fetch import rival_retrieve
from src.core import GoogleSearchScraper
from src.logger import logger


def register_search_tools(mcp: FastMCP):
    """Register all search-related tools."""
    
    @mcp.tool
    async def google_search(
        query: str,
        num_results: int = 10,
        lang: str = "en",
        proxy: Optional[str] = None,
        advanced: bool = True,
        sleep_interval: float = 0,
        timeout: int = 5,
        safe: str = "active",
        ssl_verify: Optional[bool] = None,
        region: Optional[str] = None,
        start_num: int = 0,
        unique: bool = False,
        use_multi_engine: bool = False
    ) -> dict:
        """
        Comprehensive Google Search with multi-engine fallback and advanced features.
        
        Args:
            query: Search query
            num_results: Number of results to return
            lang: Language for search (default: "en")
            proxy: Proxy to use for requests
            advanced: Enable advanced features like rich snippets detection
            sleep_interval: Delay between requests
            timeout: Request timeout in seconds
            safe: Safe search setting ("active", "off")
            ssl_verify: SSL verification setting
            region: Geographic region for search
            start_num: Starting position for results
            unique: Return only unique results
            use_multi_engine: Use multi-engine search as fallback if direct scraping fails
        """
        try:
            logger.info(f"🔍 Performing Google Search for: {query}")
            logger.info(f"📊 Target results: {num_results}")
            
            # First try direct Google Search scraping
            try:
                scraper = GoogleSearchScraper()
                results = scraper.search_google(
                    term=query,
                    num_results=num_results,
                    lang=lang,
                    proxy=proxy,
                    advanced=advanced,
                    sleep_interval=sleep_interval,
                    timeout=timeout,
                    safe=safe,
                    ssl_verify=ssl_verify,
                    region=region,
                    start_num=start_num,
                    unique=unique
                )
                
                if results:
                    # Convert results to dict format for serialization
                    result_dicts = []
                    for result in results:
                        result_dicts.append({
                            'title': result.title,
                            'url': result.url,
                            'description': result.description,
                            'position': result.position,
                            'domain': result.domain,
                            'search_features': result.search_features,
                            'estimated_traffic': result.estimated_traffic,
                            'has_rich_snippet': result.has_rich_snippet,
                            'rich_snippet_type': result.rich_snippet_type
                        })
                    
                    # Extract metadata
                    search_metadata = {
                        "total_results": len(results),
                        "unique_domains": len(set(r.domain for r in results)),
                        "rich_snippets": len([r for r in results if r.has_rich_snippet]),
                        "high_traffic_results": len([r for r in results if r.estimated_traffic == "high"]),
                        "search_features": list(set(feature for r in results for feature in (r.search_features or []))),
                        "method": "direct_scraping"
                    }
                    
                    return {
                        "success": True,
                        "results": result_dicts,
                        "query": query,
                        "count": len(results),
                        "total_results": len(results),
                        "search_metadata": search_metadata
                    }
                
            except Exception as e:
                logger.warning(f"Direct Google scraping failed: {e}")
                if not use_multi_engine:
                    raise e
            
            # Fallback to multi-engine search if direct scraping failed or no results
            if use_multi_engine or not results:
                logger.info(f"🔄 Falling back to multi-engine search for: {query}")
                search_resource = f"search:{query}"
                content = await rival_retrieve(search_resource, num_results)
                
                if not content or "No search results found" in content:
                    return {
                        "success": False,
                        "results": [],
                        "query": query,
                        "count": 0,
                        "total_results": 0,
                        "search_metadata": {"method": "multi_engine_fallback"},
                        "error": "No results found or search blocked"
                    }
                
                # Parse the formatted results back into structured data
                if isinstance(content, str):
                    lines = content.split('\n')
                else:
                    lines = str(content).split('\n')
                
                search_results = []
                current_result = {}
                
                for line in lines:
                    line = line.strip()
                    if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')):
                        if current_result:
                            search_results.append(current_result)
                        current_result = {'title': line[3:].strip()}
                    elif line.startswith('   URL: ') and current_result:
                        current_result['link'] = line[7:].strip()
                    elif line.startswith('   Snippet: ') and current_result:
                        current_result['snippet'] = line[11:].strip()
                
                # Add the last result
                if current_result:
                    search_results.append(current_result)
                
                return {
                    "success": True,
                    "results": search_results,
                    "query": query,
                    "count": len(search_results),
                    "total_results": len(search_results),
                    "search_metadata": {
                        "method": "multi_engine_fallback",
                        "total_results": len(search_results)
                    }
                }
            
            # If we get here, no results were found
            return {
                "success": False,
                "results": [],
                "query": query,
                "count": 0,
                "total_results": 0,
                "search_metadata": {"method": "direct_scraping"},
                "error": "No results found or search blocked"
            }
            
        except Exception as e:
            logger.error(f"Google Search failed for {query}: {e}")
            return {
                "success": False,
                "results": [],
                "query": query,
                "count": 0,
                "total_results": 0,
                "search_metadata": {"method": "error"},
                "error": str(e)
            }
