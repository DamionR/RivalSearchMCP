"""
HTML parsing utilities for RivalSearchMCP.
Handles BeautifulSoup operations and text extraction.
"""

import re
from bs4 import BeautifulSoup


def create_soup(html_content: str) -> BeautifulSoup:
    """Create a BeautifulSoup object with consistent parser."""
    return BeautifulSoup(html_content, 'html.parser')


def extract_text_safe(element) -> str:
    """Safely extract text from BeautifulSoup element."""
    if element is None:
        return ""
    return element.get_text(strip=True) if hasattr(element, 'get_text') else str(element).strip()


def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    if not text:
        return ""
    cleaned_text = re.sub(r'\s+', ' ', text)
    return cleaned_text.strip()
