#!/usr/bin/env python3
"""
Paywall detection configurations for RivalSearchMCP.
"""

PAYWALL_INDICATORS = [
    "subscribe",
    "paywall",
    "sign in to read",
    "become a member",
    "login to continue",
]

def get_paywall_indicators():
    """Get list of paywall indicators."""
    return PAYWALL_INDICATORS.copy()
