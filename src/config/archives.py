#!/usr/bin/env python3
"""
Archive fallback configurations for RivalSearchMCP.
"""

ARCHIVE_FALLBACKS = [
    "https://archive.is/?url=",
    "https://12ft.io/proxy?q=",
    "https://webcache.googleusercontent.com/search?q=cache:",
]

def get_archive_fallbacks():
    """Get list of archive fallback URLs."""
    return ARCHIVE_FALLBACKS.copy()
