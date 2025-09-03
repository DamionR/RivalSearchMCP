"""
Website traversal and crawling capabilities for RivalSearchMCP.
Componentized traversal functionality with core traverser and specialized traversal types.
"""

from .core import WebsiteTraverser
from .specialized import (
    explore_documentation,
    map_website_structure,
    research_topic,
)

# Create convenience functions that use the WebsiteTraverser
async def traverse_website(url: str, max_depth: int = 3, max_pages: int = 50):
    """Convenience function to traverse a website."""
    traverser = WebsiteTraverser()
    return await traverser.traverse_website(url, max_depth, max_pages)

async def get_sitemap(url: str, max_pages: int = 100):
    """Get a sitemap-like structure of a website."""
    return await map_website_structure(url, max_pages, 3)

async def extract_links(url: str, max_pages: int = 20):
    """Extract links from a website."""
    pages = await traverse_website(url, 1, max_pages)
    links = []
    for page in pages:
        if 'links' in page:
            links.extend(page['links'])
    return list(set(links))

async def analyze_structure(url: str, max_pages: int = 50):
    """Analyze the structure of a website."""
    return await map_website_structure(url, max_pages, 3)

__all__ = [
    # Core Traverser
    "WebsiteTraverser",
    # Specialized Traversal
    "research_topic",
    "explore_documentation",
    "map_website_structure",
    # Convenience functions
    "traverse_website",
    "get_sitemap",
    "extract_links",
    "analyze_structure",
]
