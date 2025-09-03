"""
Error handling utilities for RivalSearchMCP.
Handles HTTP request error handling and operation logging decorators.
"""

import httpx

from src.logging.logger import logger


def safe_request(func):
    """Decorator for safe HTTP requests with consistent error handling."""

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except httpx.TimeoutException as e:
            logger.warning(f"Request timeout: {e}")
            return None
        except httpx.HTTPStatusError as e:
            logger.warning(f"HTTP error {e.response.status_code}: {e}")
            return None
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None

    return wrapper


def log_operation(operation_name: str):
    """Decorator for consistent operation logging."""

    def decorator(func):
        async def wrapper(*args, **kwargs):
            logger.info(f"Starting {operation_name}...")
            try:
                result = await func(*args, **kwargs)
                logger.info(f"✅ {operation_name} completed successfully")
                return result
            except Exception as e:
                logger.error(f"❌ {operation_name} failed: {e}")
                raise

        return wrapper

    return decorator
