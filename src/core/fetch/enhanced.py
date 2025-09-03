#!/usr/bin/env python3
"""
Enhanced retrieval functionality for RivalSearchMCP.
Handles URLs, search queries, and Google search integration.
"""

from typing import Any, Dict, List, Union

from src.logging.logger import logger
from src.utils import clean_html_to_markdown

# Import the new multi-search system
from ..search.core.multi_engines import MultiSearchResult
from ..search.engines.bing.bing_engine import BingSearchEngine
from .base import base_fetch_url


async def rival_retrieve(
    resource: Union[str, List[str]], limit: int = 5, max_length: int = 2000
) -> Union[str, List[Dict[str, Any]]]:
    """
    Enhanced retrieval function that handles both URLs and search queries.

    Args:
        resource: URL, list of URLs, or search query
        limit: Maximum number of results
        max_length: Maximum content length per result

    Returns:
        Formatted string or list of results
    """
    if isinstance(resource, list):
        # Handle list of URLs
        from .batch import batch_rival_retrieve

        results = await batch_rival_retrieve(resource[:limit])
        return results
    elif resource.startswith(("http://", "https://")):
        # Handle single URL
        html_content = await base_fetch_url(resource)
        if html_content:
            # Process HTML to clean markdown
            clean_content = clean_html_to_markdown(html_content, resource)
            return clean_content
        return f"Failed to retrieve content from {resource}"
    else:
        # Handle search query using new multi-search system
        try:
            bing_engine = BingSearchEngine()
            search_results = await bing_engine.search(
                query=resource,
                num_results=limit,
                extract_content=False  # Don't extract content for this function
            )
            
            if search_results:
                formatted_results = []
                for result in search_results:
                    formatted_results.append(
                        {
                            "title": result.title,
                            "url": result.url,
                            "snippet": result.description,
                            "engine": result.engine,
                        }
                    )
                # Format results as string
                formatted_string = ""
                for i, result in enumerate(formatted_results, 1):
                    formatted_string += f"{i}. {result['title']}\n"
                    formatted_string += f"   URL: {result['url']}\n"
                    formatted_string += f"   Description: {result['snippet']}\n"
                    formatted_string += f"   Engine: {result['engine']}\n\n"
                return formatted_string
            else:
                return f"No search results found for: {resource}"
        except Exception as e:
            logger.error(f"Search failed for '{resource}': {e}")
            return f"Search failed for '{resource}': {str(e)}"


async def google_search_fetch(query: str, num_results: int = 5) -> str:
    """
    Simplified multi-engine search that returns formatted string.

    Args:
        query: Search query
        num_results: Number of results

    Returns:
        Formatted string with search results
    """
    try:
        bing_engine = BingSearchEngine()
        results = await bing_engine.search(
            query=query,
            num_results=num_results,
            extract_content=False  # Don't extract content for this function
        )
        
        if not results:
            return f"No results found for: {query}"

        formatted = f"Search results for '{query}':\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"{i}. {result.title}\n"
            formatted += f"   URL: {result.url}\n"
            formatted += f"   Description: {result.description}\n"
            formatted += f"   Engine: {result.engine}\n\n"

        return formatted

    except Exception as e:
        logger.error(f"Multi-engine search failed: {e}")
        return f"Search failed: {str(e)}"
