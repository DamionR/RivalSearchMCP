#!/usr/bin/env python3
"""
Enhanced retrieval functionality for RivalSearchMCP.
Handles URLs, search queries, and Google search integration.
"""

from typing import Union, List, Dict, Any

from src.logger import logger
from src.utils import clean_html_to_markdown, extract_structured_content, format_search_results
from .base_fetch import base_fetch_url
from ..search import GoogleSearchScraper


async def rival_retrieve(
    resource: Union[str, List[str]],
    limit: int = 5,
    max_length: int = 2000
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
        from .batch_retrieval import batch_rival_retrieve
        results = await batch_rival_retrieve(resource[:limit])
        return results
    elif resource.startswith(('http://', 'https://')):
        # Handle single URL
        html_content = await base_fetch_url(resource)
        if html_content:
            # Process HTML to clean markdown
            clean_content = clean_html_to_markdown(html_content, resource)
            return clean_content[:max_length] + "..." if len(clean_content) > max_length else clean_content
        return f"Failed to retrieve content from {resource}"
    else:
        # Handle search query
        try:
            scraper = GoogleSearchScraper()
            search_results = scraper.search_google(term=resource, num_results=limit)
            if search_results:
                formatted_results = []
                for result in search_results:
                    formatted_results.append({
                        'title': result.title,
                        'url': result.url,
                        'snippet': result.description[:max_length] + "..." if len(result.description) > max_length else result.description,
                        'domain': result.domain
                    })
                # Use the new formatting function
                return format_search_results(formatted_results)
            else:
                return f"No search results found for: {resource}"
        except Exception as e:
            logger.error(f"Search failed for '{resource}': {e}")
            return f"Search failed for '{resource}': {str(e)}"


async def google_search_fetch(query: str, num_results: int = 5) -> str:
    """
    Simplified Google search that returns formatted string.
    
    Args:
        query: Search query
        num_results: Number of results
        
    Returns:
        Formatted string with search results
    """
    try:
        scraper = GoogleSearchScraper()
        results = scraper.search_google(term=query, num_results=num_results)
        if not results:
            return f"No results found for: {query}"
        
        formatted = f"Search results for '{query}':\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"{i}. {result.title}\n"
            formatted += f"   URL: {result.url}\n"
            formatted += f"   Description: {result.description[:200]}...\n\n"
        
        return formatted
        
    except Exception as e:
        logger.error(f"Google search failed: {e}")
        return f"Search failed: {str(e)}"
