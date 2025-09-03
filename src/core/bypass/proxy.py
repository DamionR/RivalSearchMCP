#!/usr/bin/env python3
"""
Proxy management functionality for RivalSearchMCP.
Handles proxy fetching, testing, and selection.
"""

import asyncio
import random
import re
from typing import List, Optional

import httpx

from src.logging.logger import logger
from src.utils import get_http_client

# Enhanced proxy sources
PROXY_SOURCES = [
    "https://free-proxy-list.net/",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
]

proxies = []
last_proxy_refresh = 0


async def get_proxies(count: int = 20) -> List[str]:
    """Get proxies from multiple sources with enhanced reliability."""
    global proxies, last_proxy_refresh

    # Check if we need to refresh (every 30 minutes)
    current_time = asyncio.get_event_loop().time()
    if current_time - last_proxy_refresh < 1800 and len(proxies) > 5:
        return proxies[:count]

    all_proxies = []

    for source in PROXY_SOURCES:
        try:
            client = await get_http_client()
            response = await client.get(source, timeout=10.0)
            if response.status_code == 200:
                content = response.text

                # Extract IP:PORT patterns
                proxy_pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+)"
                found_proxies = re.findall(proxy_pattern, content)

                # Validate proxies
                valid_proxies = []
                for proxy in found_proxies[:10]:  # Test first 10 from each source
                    if await test_proxy(proxy):
                        valid_proxies.append(proxy)

                all_proxies.extend(valid_proxies)
                logger.info(f"Found {len(valid_proxies)} valid proxies from {source}")

        except Exception as e:
            logger.warning(f"Failed to fetch proxies from {source}: {e}")
            continue

    # If no proxies found from online sources, use some fallback proxies
    if not all_proxies:
        fallback_proxies = [
            "127.0.0.1:8080",  # Local proxy (if available)
            "127.0.0.1:1080",  # SOCKS proxy (if available)
        ]
        all_proxies = fallback_proxies

    proxies = all_proxies
    last_proxy_refresh = current_time
    logger.info(f"Total valid proxies: {len(proxies)}")

    return proxies[:count]


async def test_proxy(proxy: str) -> bool:
    """Test if a proxy is working."""
    try:
        proxy_url = f"http://{proxy}"
        async with httpx.AsyncClient(proxy=proxy_url, timeout=5.0) as client:
            response = await client.get("http://httpbin.org/ip")
            return response.status_code == 200
    except Exception:
        return False


async def refresh_proxies():
    """Refresh the proxy list."""
    global proxies
    proxies = await get_proxies(20)


def select_proxy() -> Optional[str]:
    """Select a random proxy from the available list."""
    if not proxies:
        return None
    return random.choice(proxies)
