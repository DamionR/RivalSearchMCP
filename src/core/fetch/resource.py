#!/usr/bin/env python3
"""
Resource management functionality for RivalSearchMCP.
Handles cleanup and resource management for HTTP clients.
"""

from src.utils import close_http_clients


async def cleanup_resources():
    """Clean up HTTP clients and free resources."""
    await close_http_clients()
