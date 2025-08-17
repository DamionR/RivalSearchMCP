"""
Web retrieval and research tools for FastMCP server.
Modular FastMCP approach - tools defined here, registered in server.py
"""

from mcp.server import FastMCP

from src.core.fetch import base_fetch_url, batch_rival_retrieve, stream_fetch, google_search_fetch
from src.core.traversal import research_topic, explore_documentation, map_website_structure
from src.core.multi_modal import process_images_ocr
from src.schemas.schemas import RetrieveResult, GoogleSearchResult, WebsiteTraversalResult, SearchResult
from src.logger import logger


def register_web_tools(mcp: FastMCP):
    """Register all web retrieval and research tools."""
    
    @mcp.tool()
    async def rival_retrieve(resource: str, limit: int = 5, store_data: bool = False, max_length: int = 2000) -> RetrieveResult:
        """Enhanced web content retrieval with advanced bypass techniques."""
        try:
            logger.info(f"Retrieving content from: {resource}")
            content = await base_fetch_url(resource)
            
            # Truncate if needed
            if len(content) > max_length:
                content = content[:max_length] + "..."
            
            return RetrieveResult(
                success=True,
                data={"content": content},
                original_url=resource,
                is_search=False
            )
        except Exception as e:
            logger.error(f"Retrieval failed for {resource}: {e}")
            return RetrieveResult(
                success=False,
                data={"error": str(e)},
                original_url=resource,
                is_search=False,
                error_message=str(e)
            )
    
    @mcp.tool()
    async def google_search(query: str, max_results: int = 10) -> GoogleSearchResult:
        """Enhanced multi-engine search with DuckDuckGo and fallbacks."""
        try:
            logger.info(f"Performing multi-engine search for: {query}")
            results = await google_search_fetch(query, max_results)
            
            if not results:
                return GoogleSearchResult(
                    success=False,
                    results=[],
                    query=query,
                    count=0,
                    error="No results found or search blocked"
                )
            
            # Convert dict results to SearchResult objects
            search_results = [
                SearchResult(
                    title=r.get('title', ''),
                    link=r.get('url', ''),  # Updated to match new format
                    snippet=r.get('snippet', '')
                ) for r in results
            ]
            
            return GoogleSearchResult(
                success=True,
                results=search_results,
                query=query,
                count=len(search_results)
            )
        except Exception as e:
            logger.error(f"Multi-engine search failed for {query}: {e}")
            return GoogleSearchResult(
                success=False,
                results=[],
                query=query,
                count=0,
                error=str(e)
            )
    
    @mcp.tool()
    async def research_website(url: str, max_pages: int = 5) -> WebsiteTraversalResult:
        """Research a website by traversing its pages."""
        try:
            logger.info(f"Researching website: {url}")
            result = await research_topic(url, max_pages=max_pages)
            
            return WebsiteTraversalResult(
                success=True,
                pages=result.get('pages', []),
                summary=result.get('summary', ''),
                total_pages=len(result.get('pages', [])),
                source=url
            )
        except Exception as e:
            logger.error(f"Website research failed for {url}: {e}")
            return WebsiteTraversalResult(
                success=False,
                pages=[],
                summary=f"Error: {str(e)}",
                total_pages=0,
                source=url
            )
    
    @mcp.tool()
    async def explore_docs(url: str, max_pages: int = 5) -> WebsiteTraversalResult:
        """Explore documentation by traversing its pages."""
        try:
            logger.info(f"Exploring documentation: {url}")
            result = await explore_documentation(url, max_pages=max_pages)
            
            return WebsiteTraversalResult(
                success=True,
                pages=result.get('pages', []),
                summary=result.get('summary', ''),
                total_pages=len(result.get('pages', [])),
                source=url
            )
        except Exception as e:
            logger.error(f"Documentation exploration failed for {url}: {e}")
            return WebsiteTraversalResult(
                success=False,
                pages=[],
                summary=f"Error: {str(e)}",
                total_pages=0,
                source=url
            )
    
    @mcp.tool()
    async def map_website(url: str, max_depth: int = 2, max_pages: int = 10) -> WebsiteTraversalResult:
        """Map website structure by traversing its pages."""
        try:
            logger.info(f"Mapping website: {url}")
            result = await map_website_structure(url, max_pages=max_pages)
            
            return WebsiteTraversalResult(
                success=True,
                pages=result.get('pages', []),
                summary=result.get('summary', ''),
                total_pages=len(result.get('pages', [])),
                source=url
            )
        except Exception as e:
            logger.error(f"Website mapping failed for {url}: {e}")
            return WebsiteTraversalResult(
                success=False,
                pages=[],
                summary=f"Error: {str(e)}",
                total_pages=0,
                source=url
            )
    
    @mcp.tool()
    async def stream_retrieve(url: str) -> RetrieveResult:
        """Retrieve streaming content from WebSocket URLs."""
        try:
            logger.info(f"Retrieving stream from: {url}")
            content = await stream_fetch(url)
            
            return RetrieveResult(
                success=True,
                data={"content": content},
                original_url=url,
                is_search=False
            )
        except Exception as e:
            logger.error(f"Stream retrieval failed for {url}: {e}")
            return RetrieveResult(
                success=False,
                data={"error": str(e)},
                original_url=url,
                is_search=False,
                error_message=str(e)
            )
    
    @mcp.tool()
    async def extract_images(url: str) -> RetrieveResult:
        """Extract and process images from a webpage using OCR."""
        try:
            logger.info(f"Extracting images from: {url}")
            content = await base_fetch_url(url)
            
            # Process images with OCR
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            ocr_results = await process_images_ocr(soup, url)
            
            if ocr_results:
                image_text = "\n".join(ocr_results)
                return RetrieveResult(
                    success=True,
                    data={"content": f"Image texts extracted:\n{image_text}"},
                    original_url=url,
                    is_search=False
                )
            else:
                return RetrieveResult(
                    success=True,
                    data={"content": "No images found or OCR processing failed"},
                    original_url=url,
                    is_search=False
                )
        except Exception as e:
            logger.error(f"Image extraction failed for {url}: {e}")
            return RetrieveResult(
                success=False,
                data={"error": str(e)},
                original_url=url,
                is_search=False,
                error_message=str(e)
            )
    
    @mcp.tool()
    async def batch_retrieve(resources: list, limit: int = 5) -> RetrieveResult:
        """Retrieve content from multiple resources in parallel."""
        try:
            logger.info(f"Batch retrieving from {len(resources)} resources")
            results = await batch_rival_retrieve(resources, {'limit': limit})
            
            combined_content = "\n\n---\n\n".join(results)
            
            return RetrieveResult(
                success=True,
                data={"content": combined_content},
                original_url=", ".join(resources),
                is_search=False
            )
        except Exception as e:
            logger.error(f"Batch retrieval failed: {e}")
            return RetrieveResult(
                success=False,
                data={"error": str(e)},
                original_url=", ".join(resources),
                is_search=False,
                error_message=str(e)
            )