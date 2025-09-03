#!/usr/bin/env python3
"""
Utility functions for unified content processing.
Provides easy access to the best content processing methods.
"""

from typing import Any, Dict, List, Optional, Union

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
    HTMLToMarkdownConverter,
    SearchResultCleaner,
    DocumentationCleaner
)


def extract_main_content(html_content: str, **kwargs) -> str:
    """Extract main content from HTML using unified extractor."""
    extractor = UnifiedContentExtractor()
    return extractor.extract(html_content, **kwargs)


def extract_search_results(html_content: str, **kwargs) -> List[Dict[str, str]]:
    """Extract search results from HTML using Google-specific extractor."""
    extractor = GoogleSpecificExtractor()
    return extractor.extract(html_content, **kwargs)


def clean_html_content(html_content: str, **kwargs) -> str:
    """Clean HTML content using unified cleaner."""
    cleaner = UnifiedTextCleaner()
    return cleaner.clean(html_content, **kwargs)


def parse_html_structure(html_content: str, **kwargs) -> Dict[str, Any]:
    """Parse HTML structure using unified parser."""
    parser = UnifiedHTMLParser()
    return parser.parse(html_content, **kwargs)


def html_to_markdown(html_content: str, **kwargs) -> str:
    """Convert HTML to markdown using unified converter."""
    converter = HTMLToMarkdownConverter()
    return converter.clean(html_content, **kwargs)


def clean_search_results(content: str, **kwargs) -> str:
    """Clean search result text specifically."""
    cleaner = SearchResultCleaner()
    return cleaner.clean(content, **kwargs)


def clean_documentation(content: str, **kwargs) -> str:
    """Clean documentation text specifically."""
    cleaner = DocumentationCleaner()
    return cleaner.clean(content, **kwargs)


def parse_documentation(html_content: str, **kwargs) -> Dict[str, Any]:
    """Parse documentation HTML for LLMs.txt generation."""
    parser = DocumentationParser()
    return parser.parse(html_content, **kwargs)


def extract_triples(text: str) -> List[tuple]:
    """Extract subject-predicate-object triples from text."""
    import re
    
    triples = []
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)
    for sentence in sentences:
        words = sentence.split()
        if len(words) > 2:
            subject = words[0]
            predicate = words[1]
            obj = " ".join(words[2:])
            triples.append((subject, predicate, obj))
    return triples
