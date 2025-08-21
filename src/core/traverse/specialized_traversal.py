#!/usr/bin/env python3
"""
Specialized traversal functionality for RivalSearchMCP.
Different types of traversal for research, documentation, and website mapping.
"""

from typing import List, Dict, Any

from .core_traverser import WebsiteTraverser


async def research_topic(
    topic: str,
    max_pages: int = 20,
    max_depth: int = 2
) -> List[Dict[str, Any]]:
    """
    Research a topic by traversing relevant websites.
    
    Args:
        topic: Topic to research
        max_pages: Maximum pages to visit
        max_depth: Maximum traversal depth
        
    Returns:
        List of page data
    """
    # This would typically start with a search to find relevant URLs
    # For now, we'll use a placeholder
    start_url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
    
    traverser = WebsiteTraverser()
    return await traverser.traverse_website(start_url, max_depth, max_pages)


async def explore_documentation(
    docs_url: str,
    max_pages: int = 30,
    max_depth: int = 3
) -> List[Dict[str, Any]]:
    """
    Explore documentation websites.
    
    Args:
        docs_url: Documentation base URL
        max_pages: Maximum pages to visit
        max_depth: Maximum traversal depth
        
    Returns:
        List of page data
    """
    traverser = WebsiteTraverser()
    return await traverser.traverse_website(docs_url, max_depth, max_pages)


async def map_website_structure(
    website_url: str,
    max_pages: int = 50,
    max_depth: int = 3
) -> List[Dict[str, Any]]:
    """
    Map the structure of a website.
    
    Args:
        website_url: Website URL to map
        max_pages: Maximum pages to visit
        max_depth: Maximum traversal depth
        
    Returns:
        List of page data with structure information
    """
    traverser = WebsiteTraverser()
    pages = await traverser.traverse_website(website_url, max_depth, max_pages)
    
    # Add structure information
    for page in pages:
        page['structure_info'] = {
            'depth': page['url'].count('/') - 2,  # Rough depth calculation
            'is_homepage': page['url'].rstrip('/') == website_url.rstrip('/'),
            'has_navigation': 'nav' in page['html'].lower() or 'menu' in page['html'].lower()
        }
    
    return pages
