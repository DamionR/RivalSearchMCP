#!/usr/bin/env python3
"""
Configuration package for RivalSearchMCP.
"""

from .user_agents import get_user_agents, DEFAULT_UA_LIST
from .paywall import get_paywall_indicators, PAYWALL_INDICATORS
from .archives import get_archive_fallbacks, ARCHIVE_FALLBACKS
from .environment import get_environment_config

__all__ = [
    # User agents
    "get_user_agents",
    "DEFAULT_UA_LIST",
    
    # Paywall detection
    "get_paywall_indicators", 
    "PAYWALL_INDICATORS",
    
    # Archive fallbacks
    "get_archive_fallbacks",
    "ARCHIVE_FALLBACKS",
    
    # Environment
    "get_environment_config"
]
