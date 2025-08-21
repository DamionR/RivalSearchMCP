"""
Web bypass functionality for RivalSearchMCP.
Componentized bypass functionality for proxy management and paywall bypassing.
"""

from .proxy_management import get_proxies, test_proxy, refresh_proxies, select_proxy
from .paywall_bypass import detect_paywall, get_archive_url

__all__ = [
    # Proxy Management
    'get_proxies',
    'test_proxy',
    'refresh_proxies',
    'select_proxy',
    
    # Paywall Bypass
    'detect_paywall',
    'get_archive_url'
]
