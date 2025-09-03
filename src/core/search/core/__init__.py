"""
Core search functionality package.
"""

from .multi_engines import BaseSearchEngine, MultiSearchResult
from .engine import MultiEngineSearch

__all__ = [
    'BaseSearchEngine',
    'MultiSearchResult',
    'MultiEngineSearch'
]
