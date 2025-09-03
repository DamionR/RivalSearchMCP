"""
Models package for search functionality.
"""

# Base models
from .base import BaseSearchResult, BaseSearchMetadata, BaseSearchRequest

# Google models
from .models import (
    GoogleSearchResult, GoogleSearchMetadata,
    GoogleNewsResult, GoogleVideoResult, GoogleImageResult
)

# Bing models
from .bing import (
    BingSearchResult, BingSearchMetadata,
    BingNewsResult, BingVideoResult, BingImageResult
)

# DuckDuckGo models
from .duckduckgo import (
    DuckDuckGoSearchResult, DuckDuckGoSearchMetadata,
    DuckDuckGoInstantAnswer, DuckDuckGoRelatedTopic
)

# Yahoo models
from .yahoo import (
    YahooSearchResult, YahooSearchMetadata,
    YahooNewsResult, YahooVideoResult, YahooImageResult
)

__all__ = [
    # Base models
    'BaseSearchResult', 'BaseSearchMetadata', 'BaseSearchRequest',
    
    # Google models
    'GoogleSearchResult', 'GoogleSearchMetadata',
    'GoogleNewsResult', 'GoogleVideoResult', 'GoogleImageResult',
    
    # Bing models
    'BingSearchResult', 'BingSearchMetadata',
    'BingNewsResult', 'BingVideoResult', 'BingImageResult',
    
    # DuckDuckGo models
    'DuckDuckGoSearchResult', 'DuckDuckGoSearchMetadata',
    'DuckDuckGoInstantAnswer', 'DuckDuckGoRelatedTopic',
    
    # Yahoo models
    'YahooSearchResult', 'YahooSearchMetadata',
    'YahooNewsResult', 'YahooVideoResult', 'YahooImageResult',
]
