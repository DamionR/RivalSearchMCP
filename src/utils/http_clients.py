"""
HTTP client management utilities for RivalSearchMCP.
Handles HTTP client and cloudscraper session management with connection pooling.
"""

import httpx
import cloudscraper
from typing import Optional

from .user_agents import get_random_user_agent


# Global connection pools
_http_client: Optional[httpx.AsyncClient] = None
_cloudscraper_session: Optional[cloudscraper.CloudScraper] = None


async def get_http_client() -> httpx.AsyncClient:
    """Get or create a reusable HTTP client with connection pooling."""
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={'User-Agent': get_random_user_agent()}
        )
    return _http_client


async def get_cloudscraper_session() -> cloudscraper.CloudScraper:
    """Get or create a reusable cloudscraper session."""
    global _cloudscraper_session
    if _cloudscraper_session is None:
        _cloudscraper_session = cloudscraper.create_scraper()
    return _cloudscraper_session


async def close_http_clients():
    """Close all HTTP clients and free resources."""
    global _http_client, _cloudscraper_session
    
    if _http_client:
        await _http_client.aclose()
        _http_client = None
    
    if _cloudscraper_session:
        _cloudscraper_session = None
