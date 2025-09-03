"""
Extract module for RivalSearchMCP.
Handles content extraction and triple extraction.
"""

from .extract import extract_search_results
from .triple import extract_triples

__all__ = [
    "extract_search_results",
    "extract_triples",
]
