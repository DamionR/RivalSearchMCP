#!/usr/bin/env python3
"""
Paywall bypass functionality for RivalSearchMCP.
Handles paywall detection and archive fallback methods.
"""

from typing import Optional

from src.config import PAYWALL_INDICATORS, ARCHIVE_FALLBACKS
from src.utils import get_http_client


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
            client = await get_http_client()
            response = await client.get(archive_url, timeout=10.0)
            if response.status_code == 200 and not detect_paywall(response.text):
                return archive_url
        except Exception:
            continue
    return None
