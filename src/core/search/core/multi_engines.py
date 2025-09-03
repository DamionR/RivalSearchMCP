"""
Multi-search engine core module for RivalSearchMCP.
Provides optimized search across multiple engines with concurrent processing.
"""

import asyncio

import re
from typing import Any, Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse, parse_qs


import httpx
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from fake_useragent import UserAgent
import cloudscraper

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

from src.logging.logger import logger


class MultiSearchResult:
    """Represents a search result from any engine."""
    
    def __init__(
        self,
        title: str,
        url: str,
        description: str,
        engine: str,
        position: int,
        timestamp: str,
        real_url: Optional[str] = None,
        full_content: Optional[str] = None,
        internal_links: Optional[List[str]] = None,
        second_level_content: Optional[Dict[str, Any]] = None,
        html_structure: Optional[Dict[str, Any]] = None,
        raw_html: Optional[str] = None
    ):
        self.title = title
        self.url = url
        self.description = description
        self.engine = engine
        self.position = position
        self.timestamp = timestamp
        self.real_url = real_url
        self.full_content = full_content
        self.internal_links = internal_links
        self.second_level_content = second_level_content
        self.html_structure = html_structure
        self.raw_html = raw_html
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "title": self.title,
            "url": self.url,
            "description": self.description,
            "engine": self.engine,
            "position": self.position,
            "timestamp": self.timestamp,
            "real_url": self.real_url,
            "full_content": self.full_content,
            "internal_links": self.internal_links,
            "second_level_content": self.second_level_content,
            "html_structure": self.html_structure,
            "raw_html": self.raw_html
        }


class BaseSearchEngine:
    """Base class for search engines with optimized content extraction."""
    
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.ua = UserAgent()
        self.scraper = cloudscraper.create_scraper()
        
        # Optimized HTTP client with connection pooling and rate limiting
        limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
        self.session = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0, connect=10.0, read=20.0),
            follow_redirects=True,
            limits=limits,
            headers={
                'User-Agent': self.ua.random,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        )
        self.visited_urls: Set[str] = set()
    
    async def search(
        self, 
        query: str, 
        num_results: int = 10,
        extract_content: bool = True,
        follow_links: bool = True,
        max_depth: int = 2
    ) -> List[MultiSearchResult]:
        """Search using the engine's implementation."""
        raise NotImplementedError
    
    async def _fetch_page_content(self, url: str) -> Optional[str]:
        """Fetch page content with optimized error handling."""
        if url in self.visited_urls:
            return None
        
        self.visited_urls.add(url)
        
        try:
            async with self.session as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.text
        except Exception as e:
            logger.warning(f"Failed to fetch content from {url}: {e}")
            return None
    
    def _extract_real_url(self, url: str) -> Optional[str]:
        """Extract real URL from redirect links."""
        try:
            # Handle DuckDuckGo redirects
            if 'duckduckgo.com' in url and 'uddg=' in url:
                parsed = urlparse(url)
                query_params = parse_qs(parsed.query)
                if 'uddg' in query_params:
                    return query_params['uddg'][0]
            
            # Handle other redirect patterns
            if 'redirect' in url.lower() or 'go' in url.lower():
                # Extract from query parameters
                parsed = urlparse(url)
                query_params = parse_qs(parsed.query)
                
                # Common redirect parameter names
                for param in ['url', 'target', 'link', 'dest', 'to']:
                    if param in query_params:
                        return query_params[param][0]
            
            return url
        except Exception as e:
            logger.debug(f"Failed to extract real URL from redirect: {e}")
            return url
    
    def _extract_main_content(self, html_content: str) -> str:
        """Extract main content from HTML using unified content extractor."""
        from ..utils.content_extractor import ContentExtractor
        return ContentExtractor.extract_main_content(html_content)
    
    def _extract_internal_links(self, html_content: str, base_url: str) -> List[str]:
        """Extract internal links from HTML content using optimized methods."""
        try:
            links = []
            
            # Method 1: Use selectolax for ultra-fast link extraction (if available)
            if SELECTOLAX_AVAILABLE:
                try:
                    parser = HTMLParser(html_content)
                    link_elements = parser.css('a[href]')
                    
                    for link in link_elements:
                        if hasattr(link, 'attributes') and link.attributes and 'href' in link.attributes:
                            href = link.attributes['href']
                            absolute_url = urljoin(base_url, str(href))
                            
                            # Only include internal links (same domain)
                            if self._extract_domain(absolute_url) == self._extract_domain(base_url):
                                links.append(absolute_url)
                    
                    if links:
                        logger.debug("Method 1 (selectolax) succeeded for link extraction")
                        # Remove duplicates and limit
                        unique_links = list(set(links))[:10]
                        logger.info(f"Extracted {len(unique_links)} internal links from {base_url}")
                        return unique_links
                        
                except Exception as e:
                    logger.debug(f"selectolax link extraction failed: {e}")
            
            # Method 2: Fallback to BeautifulSoup with lxml parser
            parser_name = 'lxml' if LXML_AVAILABLE else 'html.parser'
            soup = BeautifulSoup(html_content, parser_name)
            
            for link in soup.find_all('a', href=True):
                try:
                    if isinstance(link, Tag) and hasattr(link, 'attrs') and link.attrs and 'href' in link.attrs:
                        href = link.attrs['href']
                        absolute_url = urljoin(base_url, str(href))
                        
                        # Only include internal links (same domain)
                        if self._extract_domain(absolute_url) == self._extract_domain(base_url):
                            links.append(absolute_url)
                except Exception:
                    continue
            
            # Remove duplicates and limit
            unique_links = list(set(links))[:10]  # Limit to 10 internal links
            logger.info(f"Extracted {len(unique_links)} internal links from {base_url}")
            return unique_links
            
        except Exception as e:
            logger.warning(f"Failed to extract internal links: {e}")
            return []
    
    async def _extract_second_level_content(self, url: str, internal_links: List[str], 
                                          max_links: int = 3) -> Dict[str, Any]:
        """Extract content from internal links (second level) using concurrent processing."""
        second_level = {}
        
        # Process second level links concurrently for better performance
        async def process_second_level_link(link: str) -> Tuple[str, Dict[str, Any]]:
            try:
                logger.info(f"Extracting second level content from: {link}")
                content = await self._fetch_page_content(link)
                
                if not content:
                    return link, {}
                
                # Extract main content using optimized methods
                main_content = self._extract_main_content(content)
                internal_links = self._extract_internal_links(content, link)
                
                result = {
                    "title": self._extract_title(content),
                    "content_preview": main_content[:500] + "..." if len(main_content) > 500 else main_content,
                    "content_length": len(main_content),
                    "internal_links": internal_links
                }
                
                # Extract third level content concurrently (limited to 2 links)
                if internal_links:
                    third_level = await self._extract_third_level_content_concurrent(internal_links[:2])
                    result["third_level"] = third_level
                
                return link, result
                
            except Exception as e:
                logger.warning(f"Failed to extract second level from {link}: {e}")
                return link, {}
        
        # Process all second level links concurrently
        tasks = [process_second_level_link(link) for link in internal_links[:max_links]]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Build the result dictionary
        for result in results:
            if isinstance(result, tuple) and len(result) == 2:
                link, result_data = result
                if isinstance(result_data, dict) and result_data:
                    second_level[link] = result_data
        
        return second_level
    
    async def _extract_third_level_content_concurrent(self, third_links: List[str]) -> Dict[str, Any]:
        """Extract third level content concurrently for better performance."""
        third_level = {}
        
        async def process_third_level_link(link: str) -> Tuple[str, Dict[str, Any]]:
            try:
                third_content = await self._fetch_page_content(link)
                if not third_content:
                    return link, {}
                
                third_main = self._extract_main_content(third_content)
                return link, {
                    "title": self._extract_title(third_content),
                    "content_preview": third_main[:300] + "..." if len(third_main) > 300 else third_main,
                    "content_length": len(third_main)
                }
            except Exception as e:
                logger.debug(f"Failed to extract third level from {link}: {e}")
                return link, {}
        
        # Process all third level links concurrently
        tasks = [process_third_level_link(link) for link in third_links]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Build the result dictionary
        for result in results:
            if isinstance(result, tuple) and len(result) == 2:
                link, result_data = result
                if isinstance(result_data, dict) and result_data:
                    third_level[link] = result_data
        
        return third_level
    
    def _extract_title(self, html_content: str) -> str:
        """Extract page title from HTML."""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            title_tag = soup.find('title')
            if isinstance(title_tag, Tag) and hasattr(title_tag, 'get_text'):
                return title_tag.get_text(strip=True)
            return ""
        except Exception:
            return ""
    
    def _extract_html_structure(self, html_content: str) -> Dict[str, Any]:
        """Extract HTML structure information for debugging."""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Get basic structure info
            structure = {
                "tag_name": soup.name or "document",
                "classes": [],
                "id": "",
                "data_attributes": {},
                "child_elements": [],
                "text_length": len(soup.get_text()) if hasattr(soup, 'get_text') and callable(getattr(soup, 'get_text')) else 0
            }
            
            # Get body or main element
            main_element = soup.find('body') or soup.find('main') or soup
            
            if isinstance(main_element, Tag) and hasattr(main_element, 'attrs') and main_element.attrs:
                # Extract classes and ID safely
                attrs = main_element.attrs
                if 'class' in attrs:
                    classes = attrs['class']
                    if isinstance(classes, list):
                        structure["classes"] = classes
                    elif isinstance(classes, str):
                        structure["classes"] = [classes]
                
                if 'id' in attrs:
                    structure["id"] = str(attrs['id'])
                
                # Extract data attributes
                data_attrs = {}
                for attr, value in attrs.items():
                    if attr.startswith('data-'):
                        data_attrs[attr] = str(value)
                structure["data_attributes"] = data_attrs
                
                # Extract child elements info safely
                children = []
                try:
                    if isinstance(main_element, Tag) and hasattr(main_element, 'find_all') and callable(getattr(main_element, 'find_all')):
                        for child in main_element.find_all(recursive=False)[:5]:  # Limit to first 5
                            if isinstance(child, Tag) and hasattr(child, 'name') and child.name:
                                child_info = {
                                    "tag": child.name,
                                    "classes": [],
                                    "text_preview": ""
                                }
                                
                                # Safely extract classes
                                if isinstance(child, Tag) and hasattr(child, 'attrs') and child.attrs and 'class' in child.attrs:
                                    child_classes = child.attrs['class']
                                    if isinstance(child_classes, list):
                                        child_info["classes"] = child_classes
                                    elif isinstance(child_classes, str):
                                        child_info["classes"] = [child_classes]
                                
                                # Safely extract text preview
                                if isinstance(child, Tag) and hasattr(child, 'get_text') and callable(getattr(child, 'get_text')):
                                    try:
                                        child_info["text_preview"] = child.get_text(strip=True)[:100]
                                    except:
                                        child_info["text_preview"] = ""
                                
                                children.append(child_info)
                except Exception as e:
                    logger.debug(f"Error extracting child elements: {e}")
                
                structure["child_elements"] = children
            
            return structure
            
        except Exception as e:
            logger.warning(f"Failed to extract HTML structure: {e}")
            return {"error": str(e)}
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            return urlparse(url).netloc
        except Exception:
            return ""
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""
        return re.sub(r'\s+', ' ', text).strip()
    
    async def close(self):
        """Close the HTTP session."""
        await self.session.aclose()
