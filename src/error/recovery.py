#!/usr/bin/env python3
"""
Error recovery strategies for RivalSearchMCP.
"""

import logging
import asyncio
from typing import Any, Callable
from functools import wraps

class ErrorRecoveryStrategy:
    """Base class for error recovery strategies."""
    
    def __init__(self, max_retries: int = 3, backoff_factor: float = 2.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
    
    async def execute_with_recovery(
        self, 
        operation: Callable, 
        *args, 
        **kwargs
    ) -> Any:
        """Execute operation with automatic retry and recovery."""
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                if attempt > 0:
                    self.logger.info(f"Retry attempt {attempt}/{self.max_retries}")
                    await asyncio.sleep(self.backoff_factor ** (attempt - 1))
                
                return await operation(*args, **kwargs)
                
            except Exception as e:
                last_error = e
                self.logger.warning(
                    f"Attempt {attempt + 1} failed: {type(e).__name__}: {e}"
                )
                
                if attempt == self.max_retries:
                    self.logger.error(f"All retry attempts failed: {e}")
                    break
        
        if last_error is not None:
            raise last_error
        else:
            raise RuntimeError("Operation failed but no specific error was captured")
