#!/usr/bin/env python3
"""
Unified content extraction utility for RivalSearchMCP.
Consolidates HTML parsing and content extraction logic.
"""

import re
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup, Tag

from src.logging.logger import logger

# Performance optimization imports
try:
    from selectolax.parser import HTMLParser
    SELECTOLAX_AVAILABLE = True
except ImportError:
    SELECTOLAX_AVAILABLE = False

try:
    import lxml
    LXML_AVAILABLE = True
except ImportError:
    LXML_AVAILABLE = False

# Import content extraction utilities from the MCP server
try:
    from src.utils.content import clean_html_to_markdown, extract_structured_content
    from src.utils.parsing import create_soup, extract_text_safe, clean_text
    from src.utils.llms import clean_html_content, extract_text_from_html
    CONTENT_UTILS_AVAILABLE = True
except ImportError:
    CONTENT_UTILS_AVAILABLE = False


class ContentExtractor:
    """Unified content extraction utility with multiple fallback methods."""
    
    @staticmethod
    def extract_main_content(html_content: str) -> str:
        """Extract main content from HTML using multiple optimized methods as fallbacks."""
        if not html_content:
            return ""
        
        try:
            # Method 1: Use MCP server utilities if available
            if CONTENT_UTILS_AVAILABLE:
                try:
                    # Try structured content extraction first
                    structured = extract_structured_content(html_content)
                    if structured.get("content"):
                        logger.debug("Method 1 (structured) succeeded")
                        return structured["content"]
                    
                    # Fallback to clean HTML to markdown
                    markdown = clean_html_to_markdown(html_content)
                    if markdown:
                        logger.debug("Method 1 (markdown) succeeded")
                        return markdown
                except Exception as e:
                    logger.debug(f"Method 1 failed: {e}")
            
            # Method 2: Use selectolax for ultra-fast parsing (if available)
            if SELECTOLAX_AVAILABLE:
                try:
                    parser = HTMLParser(html_content)
                    
                    # Try multiple content selectors with selectolax
                    content_selectors = [
                        "main",
                        '[role="main"]',
                        ".main-content",
                        ".content",
                        ".post-content",
                        ".article-content",
                        "#content",
                        "#main",
                        ".entry-content",
                        ".post-body",
                        ".article-body"
                    ]
                    
                    for selector in content_selectors:
                        try:
                            element = parser.css_first(selector)
                            if element:
                                content = element.text(separator=" ", strip=True)
                                if len(content) > 100:
                                    logger.debug(f"Method 2 (selectolax {selector}) succeeded")
                                    return content
                        except Exception:
                            continue
                    
                    # Try body extraction with selectolax
                    try:
                        body = parser.css_first("body")
                        if body:
                            content = body.text(separator=" ", strip=True)
                            if len(content) > 100:
                                logger.debug("Method 2 (selectolax body) succeeded")
                                return content
                    except Exception:
                        pass
                        
                except Exception as e:
                    logger.debug(f"selectolax method failed: {e}")
            
            # Method 3: Use BeautifulSoup with lxml parser (faster than html.parser)
            parser_name = 'lxml' if LXML_AVAILABLE else 'html.parser'
            soup = BeautifulSoup(html_content, parser_name)
            
            # Try multiple content selectors
            content_selectors = [
                "main",
                '[role="main"]',
                ".main-content",
                ".content",
                ".post-content",
                ".article-content",
                "#content",
                "#main",
                ".entry-content",
                ".post-body",
                ".article-body"
            ]
            
            for selector in content_selectors:
                try:
                    element = soup.select_one(selector)
                    if element and hasattr(element, 'get_text'):
                        content = element.get_text(separator=" ", strip=True)
                        if len(content) > 100:
                            logger.debug(f"Method 3 (BeautifulSoup {selector}) succeeded")
                            return content
                except Exception:
                    continue
            
            # Method 4: Extract from body with cleanup
            try:
                # Remove unwanted elements
                for tag in soup(["script", "style", "nav", "footer", "header", "aside", "menu"]):
                    if isinstance(tag, Tag) and hasattr(tag, 'decompose'):
                        tag.decompose()
                
                body = soup.find("body")
                if isinstance(body, Tag) and hasattr(body, 'get_text'):
                    content = body.get_text(separator=" ", strip=True)
                    if len(content) > 100:
                        logger.debug("Method 4 (body cleanup) succeeded")
                        return content
            except Exception:
                pass
            
            # Method 5: Fallback to regex-based extraction
            try:
                # Remove HTML tags and clean up
                text_content = re.sub(r'<[^>]+>', '', html_content)
                text_content = re.sub(r'\s+', ' ', text_content)
                text_content = text_content.strip()
                
                if len(text_content) > 100:
                    logger.debug("Method 5 (regex) succeeded")
                    return text_content
            except Exception:
                pass
            
            # Method 6: Last resort - extract from title and any text
            try:
                title = soup.find("title")
                if isinstance(title, Tag) and hasattr(title, 'get_text'):
                    title_text = title.get_text()
                    if len(title_text) > 10:
                        logger.debug("Method 6 (title) succeeded")
                        return title_text
            except Exception:
                pass
            
            logger.warning("All content extraction methods failed")
            return ""
            
        except Exception as e:
            logger.error(f"Content extraction failed: {e}")
            return ""
    
    @staticmethod
    def extract_html_structure(html_content: str) -> Dict[str, Any]:
        """Extract HTML structure information."""
        if not html_content:
            return {}
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            structure = {
                "title": "",
                "meta_description": "",
                "headings": [],
                "links": [],
                "images": [],
                "forms": [],
                "tables": []
            }
            
            # Extract title
            title_tag = soup.find("title")
            if isinstance(title_tag, Tag) and hasattr(title_tag, 'get_text'):
                structure["title"] = title_tag.get_text().strip()
            
            # Extract meta description
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if isinstance(meta_desc, Tag) and hasattr(meta_desc, 'get'):
                structure["meta_description"] = meta_desc.get("content", "")
            
            # Extract headings
            for i in range(1, 7):
                headings = soup.find_all(f"h{i}")
                for heading in headings:
                    if isinstance(heading, Tag) and hasattr(heading, 'get_text'):
                        structure["headings"].append({
                            "level": i,
                            "text": heading.get_text().strip()
                        })
            
            # Extract links
            links = soup.find_all("a", href=True)
            for link in links:
                if isinstance(link, Tag) and hasattr(link, 'get'):
                    structure["links"].append({
                        "text": link.get_text().strip(),
                        "href": link.get("href", "")
                    })
            
            # Extract images
            images = soup.find_all("img")
            for img in images:
                if isinstance(img, Tag) and hasattr(img, 'get'):
                    structure["images"].append({
                        "alt": img.get("alt", ""),
                        "src": img.get("src", "")
                    })
            
            # Extract forms
            forms = soup.find_all("form")
            for form in forms:
                if isinstance(form, Tag) and hasattr(form, 'get'):
                    inputs = form.find_all("input")
                    structure["forms"].append({
                        "action": form.get("action", ""),
                        "method": form.get("method", ""),
                        "inputs": len(inputs) if inputs else 0
                    })
            
            # Extract tables
            tables = soup.find_all("table")
            for table in tables:
                if isinstance(table, Tag):
                    rows = table.find_all("tr")
                    cell_count = 0
                    for row in rows:
                        if isinstance(row, Tag):
                            cells = row.find_all(["td", "th"])
                            cell_count += len(cells) if cells else 0
                    structure["tables"].append({
                        "rows": len(rows),
                        "cells": cell_count
                    })
            
            return structure
            
        except Exception as e:
            logger.error(f"HTML structure extraction failed: {e}")
            return {}
    
    @staticmethod
    def extract_internal_links(html_content: str, base_url: str) -> list:
        """Extract internal links from HTML content."""
        if not html_content:
            return []
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            internal_links = []
            
            links = soup.find_all("a", href=True)
            for link in links:
                if isinstance(link, Tag) and hasattr(link, 'get'):
                    href = link.get("href", "")
                    if href and isinstance(href, str) and href.startswith(("http", "/", "#")):
                        internal_links.append(href)
            
            return internal_links[:50]  # Limit to 50 links
            
        except Exception as e:
            logger.error(f"Internal link extraction failed: {e}")
            return []
    
    @staticmethod
    def clean_html_to_markdown(html_content: str, base_url: str = "") -> str:
        """Convert HTML to clean markdown."""
        if not html_content:
            return ""
        
        try:
            # Use MCP server utility if available
            if CONTENT_UTILS_AVAILABLE:
                try:
                    return clean_html_to_markdown(html_content, base_url)
                except Exception as e:
                    logger.debug(f"MCP server markdown conversion failed: {e}")
            
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
