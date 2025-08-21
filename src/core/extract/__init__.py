"""
Content extraction utilities for RivalSearchMCP.
Componentized extraction functionality for triples and search results.
"""

from .triple_extraction import extract_triples
from .search_extraction import extract_search_results

__all__ = [
    # Triple Extraction
    'extract_triples',
    
    # Search Result Extraction
    'extract_search_results'
]
