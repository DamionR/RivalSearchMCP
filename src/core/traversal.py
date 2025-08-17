"""
Link traversal functionality for deep content discovery.
Intelligently follows links to extract comprehensive information across websites.
"""

import asyncio
import re
from typing import List, Set, Dict, Any, Optional, Tuple
from urllib.parse import urljoin, urlparse, urlunparse
from bs4 import BeautifulSoup
from dataclasses import dataclass

from .fetch import base_fetch_url
from .bypass import refresh_proxies
from ..logger import logger


@dataclass
class TraversalResult:
    """Result from link traversal operation."""
    url: str
    content: str
    title: str
    links_found: List[str]
    depth: int
    success: bool
    error: Optional[str] = None


@dataclass
class TraversalConfig:
    """Configuration for link traversal."""
    max_depth: int = 2
    max_pages: int = 10
    max_content_per_page: int = 3000
    follow_external_links: bool = False
    link_patterns: Optional[List[str]] = None  # Regex patterns for links to follow
    exclude_patterns: Optional[List[str]] = None  # Patterns to exclude
    same_domain_only: bool = True
    respect_robots_txt: bool = True
    delay_between_requests: float = 1.0


class LinkTraverser:
    """Advanced link traversal system for comprehensive content discovery."""
    
    def __init__(self, config: Optional[TraversalConfig] = None):
        self.config = config or TraversalConfig()
        self.visited_urls: Set[str] = set()
        self.results: List[TraversalResult] = []
        
    def normalize_url(self, url: str, base_url: Optional[str] = None) -> str:
        """Normalize URL for consistent comparison."""
        if base_url:
            url = urljoin(base_url, url)
        
        # Parse and rebuild URL to normalize
        parsed = urlparse(url)
        # Remove fragment and normalize
        normalized = urlunparse((
            parsed.scheme,
            parsed.netloc.lower(),
            parsed.path.rstrip('/') if parsed.path != '/' else '/',
            parsed.params,
            parsed.query,
            ''  # Remove fragment
        ))
        return normalized
    
    def extract_links(self, content: str, base_url: str) -> List[str]:
        """Extract valid links from HTML content."""
        try:
            soup = BeautifulSoup(content, 'html.parser')
            links = []
            
            # Extract all href attributes from anchor tags
            for link in soup.find_all('a', href=True):  # type: ignore
                href = link.get('href', '').strip()  # type: ignore
                
                # Skip empty, javascript, or anchor links
                if not href or href.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                    continue
                
                # Normalize the URL
                full_url = self.normalize_url(href, base_url)
                
                # Basic URL validation
                parsed = urlparse(full_url)
                if parsed.scheme not in ('http', 'https'):
                    continue
                
                links.append(full_url)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_links = []
            for link in links:
                if link not in seen:
                    seen.add(link)
                    unique_links.append(link)
            
            return unique_links
            
        except Exception as e:
            logger.error(f"Error extracting links: {e}")
            return []
    
    def should_follow_link(self, url: str, base_domain: str) -> bool:
        """Determine if a link should be followed based on configuration."""
        parsed = urlparse(url)
        
        # Check same domain restriction
        if self.config.same_domain_only and parsed.netloc != base_domain:
            return False
        
        # Check external links setting
        if not self.config.follow_external_links and parsed.netloc != base_domain:
            return False
        
        # Check include patterns
        if self.config.link_patterns:
            if not any(re.search(pattern, url, re.IGNORECASE) 
                      for pattern in self.config.link_patterns):
                return False
        
        # Check exclude patterns
        if self.config.exclude_patterns:
            if any(re.search(pattern, url, re.IGNORECASE) 
                  for pattern in self.config.exclude_patterns):
                return False
        
        # Skip common non-content files
        exclude_extensions = {
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.zip', '.rar', '.tar', '.gz', '.7z',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg',
            '.mp3', '.mp4', '.avi', '.mov', '.wmv',
            '.css', '.js', '.xml', '.rss'
        }
        
        if any(url.lower().endswith(ext) for ext in exclude_extensions):
            return False
        
        return True
    
    def extract_page_title(self, content: str) -> str:
        """Extract page title from HTML content."""
        try:
            soup = BeautifulSoup(content, 'html.parser')
            title_tag = soup.find('title')
            if title_tag:
                return title_tag.get_text().strip()
            
            # Fallback to h1
            h1_tag = soup.find('h1')
            if h1_tag:
                return h1_tag.get_text().strip()
            
            return "Untitled"
        except Exception:
            return "Untitled"
    
    async def fetch_page(self, url: str, depth: int) -> TraversalResult:
        """Fetch a single page and extract content and links."""
        try:
            # Add delay between requests
            if depth > 0:
                await asyncio.sleep(self.config.delay_between_requests)
            
            content = await base_fetch_url(url)
            if not content:
                return TraversalResult(
                    url=url, content="", title="", links_found=[], 
                    depth=depth, success=False, error="Empty content"
                )
            
            # Extract title
            title = self.extract_page_title(content)
            
            # Extract links for further traversal
            links = self.extract_links(content, url)
            
            # Limit content length
            if len(content) > self.config.max_content_per_page:
                content = content[:self.config.max_content_per_page] + "...[truncated]"
            
            return TraversalResult(
                url=url,
                content=content,
                title=title,
                links_found=links,
                depth=depth,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return TraversalResult(
                url=url, content="", title="", links_found=[], 
                depth=depth, success=False, error=str(e)
            )
    
    async def traverse_links(self, start_url: str) -> List[TraversalResult]:
        """
        Perform comprehensive link traversal starting from a URL.
        
        Returns a list of TraversalResult objects containing content from
        the starting page and linked pages up to the configured depth.
        """
        logger.info(f"Starting link traversal from {start_url}")
        
        # Refresh proxies before starting
        await refresh_proxies()
        
        # Initialize
        self.visited_urls.clear()
        self.results.clear()
        
        # Queue for BFS traversal: (url, depth)
        queue: List[Tuple[str, int]] = [(start_url, 0)]
        base_domain = urlparse(start_url).netloc
        
        while queue and len(self.results) < self.config.max_pages:
            url, depth = queue.pop(0)
            
            # Skip if already visited
            normalized_url = self.normalize_url(url)
            if normalized_url in self.visited_urls:
                continue
            
            # Skip if max depth exceeded
            if depth > self.config.max_depth:
                continue
            
            # Mark as visited
            self.visited_urls.add(normalized_url)
            
            # Fetch the page
            result = await self.fetch_page(url, depth)
            self.results.append(result)
            
            logger.info(f"Fetched page {len(self.results)}/{self.config.max_pages}: {url} (depth {depth})")
            
            # If successful and not at max depth, add links to queue
            if result.success and depth < self.config.max_depth:
                for link in result.links_found:
                    normalized_link = self.normalize_url(link)
                    
                    # Skip if already visited or queued
                    if normalized_link in self.visited_urls:
                        continue
                    
                    # Skip if any queued URL is the same
                    if any(self.normalize_url(queued_url) == normalized_link 
                          for queued_url, _ in queue):
                        continue
                    
                    # Check if we should follow this link
                    if self.should_follow_link(link, base_domain):
                        queue.append((link, depth + 1))
                        
                        # Limit queue size to prevent infinite expansion
                        if len(queue) > 100:
                            break
        
        logger.info(f"Traversal completed. Visited {len(self.results)} pages")
        return self.results


async def traverse_website(
    start_url: str,
    max_depth: int = 2,
    max_pages: int = 10,
    same_domain_only: bool = True,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    High-level interface for website traversal.
    
    Args:
        start_url: Starting URL for traversal
        max_depth: Maximum depth to traverse (0 = starting page only)
        max_pages: Maximum number of pages to fetch
        same_domain_only: Only follow links within the same domain
        include_patterns: Regex patterns for links to include
        exclude_patterns: Regex patterns for links to exclude
    
    Returns:
        Dictionary with traversal results and metadata
    """
    
    # Configure traversal
    config = TraversalConfig(
        max_depth=max_depth,
        max_pages=max_pages,
        same_domain_only=same_domain_only,
        link_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
        delay_between_requests=0.5  # Be respectful
    )
    
    # Perform traversal
    traverser = LinkTraverser(config)
    results = await traverser.traverse_links(start_url)
    
    # Aggregate results
    all_content = []
    all_links = set()
    successful_pages = 0
    
    for result in results:
        if result.success:
            successful_pages += 1
            all_content.append({
                "url": result.url,
                "title": result.title,
                "content": result.content[:1000] + "..." if len(result.content) > 1000 else result.content,
                "depth": result.depth
            })
            all_links.update(result.links_found)
    
    return {
        "start_url": start_url,
        "pages_fetched": successful_pages,
        "total_attempts": len(results),
        "unique_links_found": len(all_links),
        "max_depth_reached": max(r.depth for r in results) if results else 0,
        "pages": all_content,
        "summary": f"Traversed {successful_pages} pages starting from {start_url}",
        "config": {
            "max_depth": max_depth,
            "max_pages": max_pages,
            "same_domain_only": same_domain_only
        }
    }


# Convenience functions for specific use cases

async def research_topic(url: str, max_pages: int = 5) -> Dict[str, Any]:
    """Research a topic by following related links."""
    return await traverse_website(
        start_url=url,
        max_depth=2,
        max_pages=max_pages,
        same_domain_only=True,
        exclude_patterns=[
            r'/tag/', r'/category/', r'/archive/', r'/search/',
            r'\.pdf$', r'\.doc$', r'/login', r'/register'
        ]
    )


async def explore_documentation(url: str, max_pages: int = 15) -> Dict[str, Any]:
    """Explore documentation by following doc links."""
    return await traverse_website(
        start_url=url,
        max_depth=3,
        max_pages=max_pages,
        same_domain_only=True,
        include_patterns=[
            r'/docs?/', r'/documentation/', r'/guide/', r'/tutorial/',
            r'/api/', r'/reference/', r'/manual/'
        ],
        exclude_patterns=[
            r'/forum/', r'/blog/', r'/news/', r'/download/'
        ]
    )


async def map_website_structure(url: str, max_pages: int = 20) -> Dict[str, Any]:
    """Map the overall structure of a website."""
    return await traverse_website(
        start_url=url,
        max_depth=2,
        max_pages=max_pages,
        same_domain_only=True,
        exclude_patterns=[
            r'\.pdf$', r'\.doc$', r'\.zip$', r'/search\?',
            r'/login', r'/register', r'/cart', r'/checkout'
        ]
    )