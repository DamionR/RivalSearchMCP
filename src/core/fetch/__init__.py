"""
Fetch module for RivalSearchMCP.
Handles URL fetching and batch retrieval.
"""

from .base import (
    base_fetch_url, 
    stream_fetch,
    BaseFetcher,
    URLFetcher,
    BatchFetcher,
    EnhancedFetcher,
    UnifiedFetcher
)
from .batch import batch_rival_retrieve
from .enhanced import rival_retrieve, google_search_fetch

__all__ = [
    "base_fetch_url",
    "stream_fetch",
    "batch_rival_retrieve", 
    "rival_retrieve",
    "google_search_fetch",
    "BaseFetcher",
    "URLFetcher",
    "BatchFetcher",
    "EnhancedFetcher",
    "UnifiedFetcher"
]
