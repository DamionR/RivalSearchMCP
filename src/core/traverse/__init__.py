"""
Website traversal and crawling capabilities for RivalSearchMCP.
Componentized traversal functionality with core traverser and specialized traversal types.
"""

from .core_traverser import WebsiteTraverser
from .specialized_traversal import (
    research_topic, explore_documentation, map_website_structure
)

__all__ = [
    # Core Traverser
    'WebsiteTraverser',
    
    # Specialized Traversal
    'research_topic',
    'explore_documentation',
    'map_website_structure'
]
