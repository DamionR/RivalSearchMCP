#!/usr/bin/env python3
"""
Batch retrieval functionality for RivalSearchMCP.
Handles concurrent fetching of multiple URLs.
"""

import asyncio
from typing import List, Dict, Any
from datetime import datetime

from src.logger import logger
from .base_fetch import base_fetch_url


async def batch_rival_retrieve(
    urls: List[str],
    max_concurrent: int = 10,
    use_cloudscraper: bool = False
) -> List[Dict[str, Any]]:
    """
    Batch retrieve content from multiple URLs with concurrency control.
    
    Args:
        urls: List of URLs to fetch
        max_concurrent: Maximum concurrent requests
        use_cloudscraper: Whether to use cloudscraper
        
    Returns:
        List of results with URL and content
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def fetch_single(url: str) -> Dict[str, Any]:
        async with semaphore:
            try:
                content = await base_fetch_url(url, use_cloudscraper)
                return {
                    'url': url,
                    'content': content,
                    'success': content is not None,
                    'timestamp': datetime.now().isoformat()
                }
            except Exception as e:
                logger.error(f"Error fetching {url}: {e}")
                return {
                    'url': url,
                    'content': None,
                    'success': False,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
    
    # Fetch all URLs concurrently
    tasks = [fetch_single(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out exceptions
    valid_results = []
    for result in results:
        if isinstance(result, Exception):
            logger.error(f"Task failed with exception: {result}")
        else:
            valid_results.append(result)
    
    return valid_results
