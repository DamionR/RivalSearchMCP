"""
Core module for RivalSearchMCP.
Main functionality for search, fetch, bypass, and content processing.
"""

from .bypass import (
    detect_paywall,
    get_archive_url,
    get_proxies,
    refresh_proxies,
    select_proxy,
    test_proxy,
)

from .extract import extract_search_results, extract_triples

from .fetch import (
    base_fetch_url,
    stream_fetch,
    batch_rival_retrieve,
    rival_retrieve,
    google_search_fetch,
)

from .content import (
    extract_main_content,
    extract_search_results as unified_extract_search_results,
    clean_html_content,
    parse_html_structure,
    html_to_markdown
)



from .search import BaseSearchEngine, MultiSearchResult, BingSearchEngine, DuckDuckGoSearchEngine, YahooSearchEngine

from .traverse import (
    traverse_website,
    get_sitemap,
    extract_links,
    analyze_structure,
)

from .trends import GoogleTrendsAPI

from .llms import ContentProcessor, LLMsTxtGenerator

__all__ = [
    # Bypass
    "detect_paywall",
    "get_archive_url", 
    "get_proxies",
    "refresh_proxies",
    "select_proxy",
    "test_proxy",
    
    # Extract
    "extract_search_results",
    "extract_triples",
    
    # Fetch
    "base_fetch_url",
    "stream_fetch",
    "batch_rival_retrieve",
    "rival_retrieve",
    "google_search_fetch",
    
    # Search
    "BaseSearchEngine",
    "MultiSearchResult",
    "BingSearchEngine",
    "DuckDuckGoSearchEngine",
    "YahooSearchEngine",
    
    # Traverse
    "traverse_website",
    "get_sitemap",
    "extract_links",
    "analyze_structure",
    
    # Trends
    "GoogleTrendsAPI",
    
    # LLMs
    "ContentProcessor",
    "LLMsTxtGenerator",
]
