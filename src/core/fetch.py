import asyncio
import random
import httpx
import cloudscraper
from typing import List
from src.core.bypass import (
    select_proxy, detect_paywall, get_archive_url,
    get_advanced_headers, get_advanced_cookies
)
from src.config import ARCHIVE_FALLBACKS
from src.core.multi_modal import process_images_ocr
from src.core.search_engines import MultiSearchEngine, multi_search, duckduckgo_search
from bs4 import BeautifulSoup
import websockets
from src.logger import logger

async def base_fetch_url(url: str, timeout: int = 30) -> str:
    """Enhanced web fetching with advanced bypass techniques."""
    # Get advanced headers and cookies
    headers = get_advanced_headers()
    cookies = get_advanced_cookies()
    
    # Get proxy
    proxy = select_proxy()
    proxy_url = f"http://{proxy}" if proxy else None
    
    # Add random delay
    await asyncio.sleep(random.uniform(1, 3))
    
    try:
        # Try with cloudscraper first (30% chance)
        if cloudscraper and random.random() < 0.3:
            try:
                scraper = cloudscraper.create_scraper()
                proxies_dict = {'http': proxy_url, 'https': proxy_url} if proxy_url else None
                response = scraper.get(url, proxies=proxies_dict, timeout=timeout, headers=headers)
                content = response.text
                logger.info(f"Cloudscraper successful for {url}")
            except Exception as e:
                logger.warning(f"Cloudscraper failed for {url}: {e}")
                content = None
        else:
            content = None
        
        # If cloudscraper failed or wasn't used, try with httpx
        if not content:
            try:
                async with httpx.AsyncClient(
                    proxy=proxy_url,
                    headers=headers,
                    cookies=cookies,
                    timeout=timeout,
                    follow_redirects=True,
                    verify=False
                ) as client:
                    response = await client.get(url)
                    content = response.text
                    logger.info(f"HTTPX successful for {url}: {response.status_code}")
            except Exception as e:
                logger.warning(f"HTTPX failed for {url}: {e}")
                content = None
        
        # If still no content, try archive fallback
        if not content:
            logger.info(f"Trying archive fallback for {url}")
            archive_url = await get_archive_url(url)
            if archive_url:
                try:
                    async with httpx.AsyncClient(timeout=timeout) as client:
                        response = await client.get(archive_url)
                        content = response.text
                        logger.info(f"Archive fallback successful for {url}")
                except Exception as e:
                    logger.warning(f"Archive fallback failed for {url}: {e}")
        
        # Check for paywall
        if content and detect_paywall(content):
            logger.info(f"Paywall detected for {url}, trying archive services")
            for archive in ARCHIVE_FALLBACKS:
                try:
                    archive_url = archive + url
                    async with httpx.AsyncClient(timeout=timeout) as client:
                        response = await client.get(archive_url)
                        if response.status_code == 200:
                            archive_content = response.text
                            if not detect_paywall(archive_content):
                                content = archive_content
                                logger.info(f"Paywall bypassed using {archive}")
                                break
                except Exception as e:
                    logger.warning(f"Archive service {archive} failed: {e}")
                    continue
        
        if not content:
            raise ValueError(f"Failed to fetch content from {url}")
        
        # Process images with OCR
        try:
            soup = BeautifulSoup(content, 'html.parser')
            ocr_results = await process_images_ocr(soup, url)
            if ocr_results:
                content += "\n\nImage Texts:\n" + "\n".join(ocr_results)
        except Exception as e:
            logger.warning(f"OCR processing failed for {url}: {e}")
        
        return content
        
    except Exception as e:
        logger.error(f"Fetch failed for {url}: {e}")
        raise ValueError(f"Fetch failed: {str(e)}")

async def batch_rival_retrieve(resources: List[str], opts: dict) -> List[str]:
    """Enhanced batch retrieval with better error handling."""
    tasks = []
    for resource in resources:
        task = asyncio.create_task(base_fetch_url(resource))
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Convert exceptions to error messages
    processed_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            processed_results.append(f"Error fetching {resources[i]}: {str(result)}")
        else:
            processed_results.append(result)
    
    return processed_results

async def stream_fetch(url: str) -> str:
    """Enhanced streaming fetch with better error handling."""
    chunks = []
    try:
        async with websockets.connect(url) as ws:
            for _ in range(10):
                chunk = await ws.recv()
                chunks.append(str(chunk))
    except Exception as e:
        logger.warning(f"Stream fetch failed for {url}: {e}")
        return f"Stream fetch error: {str(e)}"
    
    return "\n".join(chunks)

async def google_search_fetch(query: str, max_results: int = 10) -> List[dict]:
    """Enhanced multi-engine search using DuckDuckGo and fallbacks."""
    try:
        results = await multi_search(query, max_results)
        # Convert SearchResult objects to dict format for backward compatibility
        return [
            {
                'title': result.title,
                'url': result.url,
                'snippet': result.snippet,
                'source': result.source_engine,
                'rank': result.rank
            }
            for result in results
        ]
    except Exception as e:
        logger.error(f"Multi-engine search failed: {e}")
        return []

async def smart_fetch(url: str, use_advanced_bypass: bool = True) -> str:
    """Smart fetching that automatically chooses the best method."""
    if use_advanced_bypass:
        # Use enhanced bypass techniques
        return await base_fetch_url(url)
    else:
        # Use simple fetching
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                return response.text
        except Exception as e:
            raise ValueError(f"Simple fetch failed: {str(e)}")
