"""
Schemas package for RivalSearchMCP.
Componentized schema modules for different functionality areas.
"""

# Import all schemas from componentized modules
from .retrieval_schemas import (
    SearchResult, WebContent, TraversalPage, TraversalResult, 
    RetrieveResult, StreamResult
)
from .web_tools_schemas import (
    GoogleSearchResult, GoogleSearchScrapeResult, WebsiteTraversalResult
)
from .common_schemas import SuccessResponse

__all__ = [
    # Retrieval schemas
    'SearchResult',
    'WebContent', 
    'TraversalPage',
    'TraversalResult',
    'RetrieveResult',
    'StreamResult',
    # Web tools schemas
    'GoogleSearchResult',
    'GoogleSearchScrapeResult',
    'WebsiteTraversalResult',
    # Common schemas
    'SuccessResponse'
]