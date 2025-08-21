"""
Headers and cookies utilities for RivalSearchMCP.
Handles HTTP headers and cookies for web requests and bypassing.
"""

import random
from typing import Optional

from .user_agents import get_random_user_agent


def get_advanced_headers(user_agent: Optional[str] = None) -> dict:
    """Get advanced headers for better bypassing."""
    if not user_agent:
        user_agent = get_random_user_agent()
    
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


def get_google_cookies() -> dict:
    """Get Google-specific cookies for search requests."""
    return {
        'CONSENT': 'PENDING+987',
        'SOCS': 'CAESHAgBEhIaAB',
    }
