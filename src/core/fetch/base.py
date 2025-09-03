#!/usr/bin/env python3
"""
Base fetching functionality for RivalSearchMCP.
Core URL fetching with optimized performance.
"""

from typing import Any, Dict, List, Optional, Union

from src.logging.logger import logger
from src.utils import get_cloudscraper_session, get_http_client

# Performance configuration
STREAM_TIMEOUT = 30.0


async def base_fetch_url(url: str, use_cloudscraper: bool = False) -> Optional[str]:
    """
    Fetch content from a URL with optimized performance.

    Args:
        url: URL to fetch
        use_cloudscraper: Whether to use cloudscraper for bypassing

    Returns:
        HTML content or None if failed
    """
    try:
        if use_cloudscraper:
            scraper = await get_cloudscraper_session()
            response = scraper.get(url, timeout=STREAM_TIMEOUT)
            response.raise_for_status()
            return response.text
        else:
            client = await get_http_client()
            response = await client.get(url, timeout=STREAM_TIMEOUT)
            response.raise_for_status()
            return response.text

    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None


async def stream_fetch(
    url: str, chunk_size: int = 1024, timeout: float = STREAM_TIMEOUT
) -> Optional[str]:
    """
    Stream fetch content from a URL with timeout.

    Args:
        url: URL to fetch
        chunk_size: Size of chunks to read
        timeout: Request timeout

    Returns:
        Streamed content or None if failed
    """
    try:
        client = await get_http_client()
        async with client.stream("GET", url, timeout=timeout) as response:
            response.raise_for_status()

            content = []
            async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                content.append(chunk.decode("utf-8", errors="ignore"))

            return "".join(content)

    except Exception as e:
        logger.error(f"Stream fetch failed for {url}: {e}")
        return None


# Unified Fetcher Classes
class BaseFetcher:
    """Base class for all fetchers."""
    
    def __init__(self):
        """Initialize the fetcher."""
        pass
    
    async def fetch(self, resource: str, **kwargs) -> Any:
        """Fetch content using the fetcher's method."""
        raise NotImplementedError("Subclasses must implement fetch method")


class URLFetcher(BaseFetcher):
    """Base URL fetching with optimized performance."""
    
    async def fetch(self, url: str, **kwargs) -> Optional[str]:
        """Fetch content from a URL with optimized performance."""
        return await base_fetch_url(url, **kwargs)


class BatchFetcher(BaseFetcher):
    """Batch URL fetching with concurrency control."""
    
    async def fetch(self, urls: List[str], **kwargs) -> List[Dict[str, Any]]:
        """Batch retrieve content from multiple URLs with concurrency control."""
        from .batch import batch_rival_retrieve
        return await batch_rival_retrieve(urls, **kwargs)


class EnhancedFetcher(BaseFetcher):
    """Enhanced fetching with search integration and fallback logic."""
    
    async def fetch(self, resource: str, **kwargs) -> Any:
        """Enhanced retrieval that handles URLs, search queries, and Google search integration."""
        from .enhanced import rival_retrieve
        return await rival_retrieve(resource, **kwargs)


class UnifiedFetcher(BaseFetcher):
    """Unified fetcher with multiple strategies and fallbacks."""
    
    def __init__(self):
        """Initialize the unified fetcher."""
        super().__init__()
        self.url_fetcher = URLFetcher()
        self.batch_fetcher = BatchFetcher()
        self.enhanced_fetcher = EnhancedFetcher()
    
    async def fetch(self, resource: Union[str, List[str]], **kwargs) -> Any:
        """Fetch content using the best available method."""
        if isinstance(resource, list):
            return await self.batch_fetcher.fetch(resource, **kwargs)
        elif resource.startswith(("http://", "https://")):
            return await self.url_fetcher.fetch(resource, **kwargs)
        else:
            return await self.enhanced_fetcher.fetch(resource, **kwargs)
