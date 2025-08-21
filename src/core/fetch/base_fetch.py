#!/usr/bin/env python3
"""
Base fetching functionality for RivalSearchMCP.
Core URL fetching with optimized performance.
"""

from typing import Optional

from src.logger import logger
from src.utils import (
    get_http_client, get_cloudscraper_session
)

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
    url: str,
    chunk_size: int = 1024,
    timeout: float = STREAM_TIMEOUT
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
        async with client.stream('GET', url, timeout=timeout) as response:
            response.raise_for_status()
            
            content = []
            async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                content.append(chunk.decode('utf-8', errors='ignore'))
            
            return ''.join(content)
            
    except Exception as e:
        logger.error(f"Stream fetch failed for {url}: {e}")
        return None
