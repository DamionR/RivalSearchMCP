import random
import asyncio
import httpx
from typing import List, Optional
from src.config import PAYWALL_INDICATORS, ARCHIVE_FALLBACKS
from src.logger import logger

# Enhanced user agent list (no external dependency)
def get_enhanced_ua_list() -> List[str]:
    """Get enhanced user agent list with realistic agents."""
    return [
        # Modern Chrome agents
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        
        # Modern Firefox agents
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        
        # Safari agents
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        
        # Edge agents
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        
        # Mobile agents
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
        
        # Legacy agents for compatibility
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    ]

# Enhanced proxy sources
PROXY_SOURCES = [
    "https://free-proxy-list.net/",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt"
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
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(source)
                if response.status_code == 200:
                    content = response.text
                    
                    # Extract IP:PORT patterns
                    import re
                    proxy_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+)'
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
        async with httpx.AsyncClient(
            proxy=proxy_url,
            timeout=5.0
        ) as client:
            response = await client.get("http://httpbin.org/ip")
            return response.status_code == 200
    except Exception:
        return False

async def refresh_proxies():
    """Refresh the proxy list."""
    global proxies
    proxies = await get_proxies(20)

def select_ua() -> str:
    """Select a random user agent from the enhanced list."""
    ua_list = get_enhanced_ua_list()
    return random.choice(ua_list)

def select_proxy() -> Optional[str]:
    """Select a random proxy from the available list."""
    if not proxies:
        return None
    return random.choice(proxies)

def detect_paywall(content: str) -> bool:
    """Enhanced paywall detection with more indicators."""
    content_lower = content.lower()
    
    # Enhanced paywall indicators
    enhanced_indicators = PAYWALL_INDICATORS + [
        "subscribe to continue",
        "become a member",
        "premium content",
        "exclusive access",
        "member only",
        "sign in to read",
        "login required",
        "registration required",
        "free trial",
        "limited access",
        "premium article",
        "subscriber only",
        "pay to read",
        "purchase article",
        "buy access",
        "upgrade to read",
        "premium subscription",
        "digital subscription",
        "newsletter signup",
        "create account",
        "join now",
        "unlock article",
        "premium content",
        "exclusive story",
        "member exclusive"
    ]
    
    return any(indicator in content_lower for indicator in enhanced_indicators)

async def get_archive_url(url: str) -> Optional[str]:
    """Get archive URL for bypassing paywalls."""
    for archive in ARCHIVE_FALLBACKS:
        try:
            archive_url = archive + url
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(archive_url)
                if response.status_code == 200 and not detect_paywall(response.text):
                    return archive_url
        except Exception:
            continue
    return None

def get_advanced_headers(user_agent: Optional[str] = None) -> dict:
    """Get advanced headers for better bypassing."""
    if not user_agent:
        user_agent = select_ua()
    
    return {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
        "Referer": "https://www.google.com/"
    }

def get_advanced_cookies() -> dict:
    """Get advanced cookies for bypassing protection."""
    return {
        "CONSENT": "YES+cb.20231231-07-p0.en+FX+{}".format(random.randint(100, 999)),
        "SOCS": "CAESHAgBEhJnd3NfMjAyNTAzMjAtMF9SQzEaAmhyIAEaBgiA-_e-Bg",
        "__Secure-ENID": "26.SE=E11y2NVkgAIHFQhBo6NIEWXowdKAqBlC7jgTI4SmEkZPeaiYTVxGTwH58I_HQZJETqHrOX8tZfB-b1WRrngoymx8ge7XPctkcG_AVWImTm8UziZVe14Vci8ozFhzm9iu9DlUVh3VTOsd4FcCBbavTonHe2vMxN1olFRLAtz6zklzCSaABwhIxpMerzBDRH-Yz3m4qnaxLLWg___1YBb8nhQLzD97yG7HXkT3XvPA91535qkn7CI0P0BmQ_sOiTvmQ2-d4TwLx1WggkpE2EavBe3FO3MYSehbA_H-qYqG6FqSl1D6DglEPey9"
    }
