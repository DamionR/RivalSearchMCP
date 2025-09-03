"""
Unified content processing module for RivalSearchMCP.
Consolidates the best content extraction, parsing, and cleaning methods.
"""

from .extractors import (
    UnifiedContentExtractor,
    GoogleSpecificExtractor,
    GenericContentExtractor
)
from .parsers import (
    UnifiedHTMLParser,
    GoogleSearchParser,
    DocumentationParser
)
from .cleaners import (
    UnifiedTextCleaner,
    HTMLToMarkdownConverter
)
from .utils import (
    extract_main_content,
    extract_search_results,
    clean_html_content,
    parse_html_structure,
    html_to_markdown
)

__all__ = [
    # Extractors
    'UnifiedContentExtractor',
    'GoogleSpecificExtractor', 
    'GenericContentExtractor',
    
    # Parsers
    'UnifiedHTMLParser',
    'GoogleSearchParser',
    'DocumentationParser',
    
    # Cleaners
    'UnifiedTextCleaner',
    'HTMLToMarkdownConverter',
    
    # Utility functions
    'extract_main_content',
    'extract_search_results',
    'clean_html_content',
    'parse_html_structure',
    'html_to_markdown'
]
