"""
Core fetching and retrieval functionality for RivalSearchMCP.
Componentized fetch functionality with base fetching, batch retrieval, and enhanced retrieval.
"""

from .base_fetch import base_fetch_url, stream_fetch
from .batch_retrieval import batch_rival_retrieve
from .enhanced_retrieval import rival_retrieve, google_search_fetch
from .resource_management import cleanup_resources

__all__ = [
    # Base Fetching
    'base_fetch_url',
    'stream_fetch',
    
    # Batch Retrieval
    'batch_rival_retrieve',
    
    # Enhanced Retrieval
    'rival_retrieve',
    'google_search_fetch',
    
    # Resource Management
    'cleanup_resources'
]
