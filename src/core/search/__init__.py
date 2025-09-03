#!/usr/bin/env python3
"""
Search functionality package for RivalSearchMCP.
Provides multi-engine search capabilities with content extraction.
"""

# Core search functionality
from .core import BaseSearchEngine, MultiSearchResult, MultiEngineSearch

# Search engines
from .engines import BingSearchEngine, DuckDuckGoSearchEngine, YahooSearchEngine

# Parsers and scrapers
from .parsers import GoogleSearchHTMLParser

# Models
from .models import GoogleSearchResult

# Utilities
from .utils import process_images_ocr

__all__ = [
    # Core
    'BaseSearchEngine',
    'MultiSearchResult', 
    'MultiEngineSearch',
    
    # Engines
    'BingSearchEngine',
    'DuckDuckGoSearchEngine',
    'YahooSearchEngine',
    
    # Parsers
    'GoogleSearchHTMLParser',
    
    # Models
    'GoogleSearchResult',
    
    # Utilities
    'process_images_ocr'
]
