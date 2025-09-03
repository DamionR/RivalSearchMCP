#!/usr/bin/env python3
"""
Unified text cleaners for RivalSearchMCP.
Consolidates the best text cleaning methods from all modules.
"""

import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup, Tag

from src.logging.logger import logger


class BaseTextCleaner(ABC):
    """Base class for text cleaners."""
    
    def __init__(self):
        """Initialize the cleaner."""
        pass
    
    @abstractmethod
    def clean(self, content: str, **kwargs) -> str:
        """Clean content using the cleaner's method."""
        pass


class UnifiedTextCleaner(BaseTextCleaner):
    """Unified text cleaner with multiple cleaning strategies."""
    
    def clean(self, content: str, **kwargs) -> str:
        """Clean and normalize text content."""
        if not content:
            return ""
        
        try:
            # Remove extra whitespace
            content = re.sub(r'\s+', ' ', content)
            
            # Remove special characters that might interfere with markdown
            content = re.sub(r'[^\w\s\-.,!?;:()[\]{}"\']', "", content)
            
            # Normalize quotes
            content = content.replace('"', '"').replace('"', '"')
            content = content.replace(""", "'").replace(""", "'")
            
            return content.strip()
            
        except Exception as e:
            logger.error(f"Text cleaning failed: {e}")
            return content.strip() if content else ""


class HTMLToMarkdownConverter(BaseTextCleaner):
    """Convert HTML to clean markdown."""
    
    def clean(self, html_content: str, **kwargs) -> str:
        """Convert HTML to clean markdown."""
        if not html_content:
            return ""
        
        try:
            # Use MCP server utility if available
            try:
                from src.utils.content import clean_html_to_markdown
                return clean_html_to_markdown(html_content, kwargs.get('base_url', ''))
            except ImportError:
                pass
            
            # Fallback to basic HTML to text conversion
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove unwanted elements
            for tag in soup(["script", "style", "nav", "footer", "header", "aside", "menu"]):
                if isinstance(tag, Tag) and hasattr(tag, 'decompose'):
                    tag.decompose()
            
            # Convert to text with basic formatting
            text = soup.get_text(separator="\n", strip=True)
            
            # Clean up whitespace
            text = re.sub(r'\n\s*\n', '\n\n', text)
            text = re.sub(r' +', ' ', text)
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"HTML to markdown conversion failed: {e}")
            return ""


class SearchResultCleaner(BaseTextCleaner):
    """Clean search result text specifically."""
    
    def clean(self, content: str, **kwargs) -> str:
        """Clean search result text."""
        if not content:
            return ""
        
        try:
            # Remove extra whitespace
            content = re.sub(r'\s+', ' ', content)
            
            # Remove common search result artifacts
            content = re.sub(r'\[.*?\]', '', content)  # Remove brackets
            content = re.sub(r'\(.*?\)', '', content)  # Remove parentheses
            
            # Clean up text
            content = content.strip()
            
            return content
            
        except Exception as e:
            logger.error(f"Search result cleaning failed: {e}")
            return content.strip() if content else ""


class DocumentationCleaner(BaseTextCleaner):
    """Clean documentation text specifically."""
    
    def clean(self, content: str, **kwargs) -> str:
        """Clean documentation text."""
        if not content:
            return ""
        
        try:
            # Remove HTML tags
            content = re.sub(r'<[^>]+>', '', content)
            
            # Remove extra whitespace
            content = re.sub(r'\s+', ' ', content)
            
            # Clean up text
            content = content.strip()
            
            return content
            
        except Exception as e:
            logger.error(f"Documentation cleaning failed: {e}")
            return content.strip() if content else ""
