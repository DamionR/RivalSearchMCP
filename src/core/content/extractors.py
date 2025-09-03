#!/usr/bin/env python3
"""
Unified content extractors for RivalSearchMCP.
Consolidates the best extraction methods from all modules.
"""

import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

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


class BaseContentExtractor(ABC):
    """Base class for content extractors."""
    
    def __init__(self):
        """Initialize the extractor."""
        pass
    
    @abstractmethod
    def extract(self, content: str, **kwargs) -> Any:
        """Extract content using the extractor's method."""
        pass


class UnifiedContentExtractor(BaseContentExtractor):
    """Unified content extractor with multiple fallback methods."""
    
    def extract(self, html_content: str, **kwargs) -> str:
        """Extract main content from HTML using multiple optimized methods as fallbacks."""
        if not html_content:
            return ""
        
        try:
            # Method 1: Use selectolax for ultra-fast parsing (if available)
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
                                    logger.debug(f"Method 1 (selectolax {selector}) succeeded")
                                    return content
                        except Exception:
                            continue
                    
                    # Try body extraction with selectolax
                    try:
                        body = parser.css_first("body")
                        if body:
                            content = body.text(separator=" ", strip=True)
                            if len(content) > 100:
                                logger.debug("Method 1 (selectolax body) succeeded")
                                return content
                    except Exception:
                        pass
                        
                except Exception as e:
                    logger.debug(f"selectolax method failed: {e}")
            
            # Method 2: Use BeautifulSoup with lxml parser (faster than html.parser)
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
                            logger.debug(f"Method 2 (BeautifulSoup {selector}) succeeded")
                            return content
                except Exception:
                    continue
            
            # Method 3: Extract from body with cleanup
            try:
                # Remove unwanted elements
                for tag in soup(["script", "style", "nav", "footer", "header", "aside", "menu"]):
                    if isinstance(tag, Tag) and hasattr(tag, 'decompose'):
                        tag.decompose()
                
                body = soup.find("body")
                if isinstance(body, Tag) and hasattr(body, 'get_text'):
                    content = body.get_text(separator=" ", strip=True)
                    if len(content) > 100:
                        logger.debug("Method 3 (body cleanup) succeeded")
                        return content
            except Exception:
                pass
            
            # Method 4: Fallback to regex-based extraction
            try:
                # Remove HTML tags and clean up
                text_content = re.sub(r'<[^>]+>', '', html_content)
                text_content = re.sub(r'\s+', ' ', text_content)
                text_content = text_content.strip()
                
                if len(text_content) > 100:
                    logger.debug("Method 4 (regex) succeeded")
                    return text_content
            except Exception:
                pass
            
            # Method 5: Last resort - extract from title and any text
            try:
                title = soup.find("title")
                if isinstance(title, Tag) and hasattr(title, 'get_text'):
                    title_text = title.get_text()
                    if len(title_text) > 10:
                        logger.debug("Method 5 (title) succeeded")
                        return title_text
            except Exception:
                pass
            
            logger.warning("All content extraction methods failed")
            return ""
            
        except Exception as e:
            logger.error(f"Content extraction failed: {e}")
            return ""


class GoogleSpecificExtractor(BaseContentExtractor):
    """Google-specific content extractor with specialized selectors."""
    
    def extract(self, html_content: str, **kwargs) -> List[Dict[str, str]]:
        """Extract Google search results using specialized selectors."""
        max_results = kwargs.get('max_results', 10)
        
        soup = BeautifulSoup(html_content, "html.parser")
        results = []
        seen_urls = set()

        # Google-specific selector sets (from extract.py)
        selector_sets = [
            {"container": "#search div[data-hveid]", "title": "h3", "snippet": ".VwiC3b"},
            {"container": "#rso div[data-hveid]", "title": "h3", "snippet": '[data-sncf="1"]'},
            {"container": ".g", "title": "h3", "snippet": 'div[style*="webkit-line-clamp"]'},
            {"container": "div[jscontroller][data-hveid]", "title": "h3", "snippet": 'div[role="text"]'},
        ]
        
        alt_snippet_selectors = [
            ".VwiC3b",
            '[data-sncf="1"]',
            'div[style*="webkit-line-clamp"]',
            'div[role="text"]',
        ]

        for selectors in selector_sets:
            if len(results) >= max_results:
                break
            containers = soup.select(selectors["container"])
            for container in containers:
                if len(results) >= max_results:
                    break

                # Extract title
                title_elem = container.select_one(selectors["title"])
                if not title_elem:
                    continue
                title = title_elem.text.strip()
                link = ""

                # Extract link with multiple fallback strategies
                link_in_title = title_elem.find_parent("a")
                if link_in_title and isinstance(link_in_title, Tag) and hasattr(link_in_title, "get"):
                    link = link_in_title.get("href", "")
                else:
                    parent = title_elem.parent
                    while parent and parent.name != "a":
                        parent = parent.parent
                    if parent and parent.name == "a" and isinstance(parent, Tag) and hasattr(parent, "get"):
                        link = parent.get("href", "")
                    else:
                        container_link = container.find("a")
                        if container_link and isinstance(container_link, Tag) and hasattr(container_link, "get"):
                            link = container_link.get("href", "")

                if (
                    not link
                    or not isinstance(link, str)
                    or not link.startswith("http")
                    or link in seen_urls
                ):
                    continue

                # Extract snippet
                snippet = ""
                snippet_elem = container.select_one(selectors["snippet"])
                if snippet_elem:
                    snippet = snippet_elem.text.strip()
                else:
                    for alt in alt_snippet_selectors:
                        elem = container.select_one(alt)
                        if elem:
                            snippet = elem.text.strip()
                            break
                    if not snippet:
                        text_divs = []
                        for div in container.find_all("div"):
                            if isinstance(div, Tag) and not div.find("h3") and len(div.text.strip()) > 20:
                                text_divs.append(div)
                        if text_divs:
                            snippet = text_divs[0].text.strip()

                if title and link:
                    results.append({"title": title, "link": link, "snippet": snippet})
                    seen_urls.add(link)

        # Fallback: extract from any HTTP links
        if len(results) < max_results:
            anchors = soup.select("a[href^='http']")
            for a in anchors:
                if len(results) >= max_results:
                    break

                link = a.get("href", "")
                if (
                    not link
                    or not isinstance(link, str)
                    or not link.startswith("http")
                    or "google.com" in link
                    or link in seen_urls
                ):
                    continue
                title = a.text.strip()
                if not title:
                    continue
                snippet = ""
                parent = a.parent
                for _ in range(3):
                    if parent:
                        text = parent.text.strip()
                        if len(text) > 20 and text != title:
                            snippet = text
                            break
                        parent = parent.parent
                results.append({"title": title, "link": link, "snippet": snippet})
                seen_urls.add(link)

        return results[:max_results]


class GenericContentExtractor(BaseContentExtractor):
    """Generic content extractor for documentation and general websites."""
    
    def extract(self, html_content: str, **kwargs) -> str:
        """Extract main content using generic selectors and element removal."""
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Try to find main content areas (from llms generator)
        main_selectors = [
            "main",
            '[role="main"]',
            ".main-content",
            ".content",
            ".post-content",
            ".article-content",
            "#content",
            "#main",
        ]

        for selector in main_selectors:
            main_element = soup.select_one(selector)
            if main_element:
                return str(main_element)

        # Fallback: remove unwanted elements and get body content
        self._remove_unwanted_elements(soup)
        body = soup.find("body")
        if body:
            return str(body)

        return str(soup)
    
    def _remove_unwanted_elements(self, soup):
        """Remove unwanted HTML elements."""
        # Remove script and style elements
        for element in soup(["script", "style", "noscript", "iframe", "embed", "object"]):
            element.decompose()

        # Remove navigation, footer, header elements
        for element in soup(["nav", "footer", "header", "aside", "menu"]):
            element.decompose()

        # Remove common ad and tracking elements
        for element in soup.find_all(
            class_=re.compile(
                r"(ad|ads|advertisement|banner|tracking|analytics|cookie|popup|modal|overlay)",
                re.I,
            )
        ):
            element.decompose()
