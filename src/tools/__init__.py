"""
Tools module for RivalSearchMCP.
Provides various tools for search, analysis, and content processing.
"""

from .multi_search import multi_search, search_with_google_fallback

__all__ = [
    "multi_search",
    "search_with_google_fallback"
]
