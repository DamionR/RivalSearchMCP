#!/usr/bin/env python3
"""
Error handling and wrapping for RivalSearchMCP.
"""

import logging
import functools
from typing import Any, Callable, Dict, Optional, Type, Union
from datetime import datetime, timedelta

from fastmcp.exceptions import ToolError, ResourceError, PromptError

class RobustOperationWrapper:
    """Wrapper for making operations more robust with error handling."""
    
    def __init__(self, 
                 max_retries: int = 3,
                 timeout: Optional[float] = None,
                 fallback_value: Any = None):
        self.max_retries = max_retries
        self.timeout = timeout
        self.fallback_value = fallback_value
        self.logger = logging.getLogger("RobustOperationWrapper")
    
    def __call__(self, func: Callable) -> Callable:
        """Decorator to wrap functions with robust error handling."""
        
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                if self.timeout:
                    import asyncio
                    return await asyncio.wait_for(func(*args, **kwargs), timeout=self.timeout)
                else:
                    return await func(*args, **kwargs)
                    
            except Exception as e:
                self.logger.error(f"Operation {func.__name__} failed: {e}")
                
                if self.fallback_value is not None:
                    self.logger.info(f"Returning fallback value: {self.fallback_value}")
                    return self.fallback_value
                else:
                    raise e
        
        return wrapper

class ErrorHandler:
    """Central error handler for RivalSearchMCP."""
    
    def __init__(self):
        self.logger = logging.getLogger("ErrorHandler")
        self.error_counts: Dict[str, int] = {}
        self.last_errors: Dict[str, datetime] = {}
    
    def handle_error(self, 
                    error: Exception, 
                    context: str = "unknown",
                    operation: str = "unknown") -> Dict[str, Any]:
        """Handle an error and return structured error information."""
        
        error_key = f"{context}:{operation}"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
        self.last_errors[error_key] = datetime.now()
        
        error_info = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "operation": operation,
            "timestamp": datetime.now().isoformat(),
            "count": self.error_counts[error_key],
            "last_occurrence": self.last_errors[error_key].isoformat()
        }
        
        # Log based on error type
        if isinstance(error, ToolError):
            self.logger.error(f"Tool error in {context}: {error}")
        elif isinstance(error, ResourceError):
            self.logger.error(f"Resource error in {context}: {error}")
        elif isinstance(error, PromptError):
            self.logger.error(f"Prompt error in {context}: {error}")
        else:
            self.logger.error(f"Unexpected error in {context}: {error}")
        
        return error_info
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics."""
        return {
            "total_errors": sum(self.error_counts.values()),
            "error_counts": self.error_counts.copy(),
            "last_errors": {k: v.isoformat() for k, v in self.last_errors.items()}
        }
    
    def clear_errors(self, context: Optional[str] = None):
        """Clear error history."""
        if context:
            keys_to_remove = [k for k in self.error_counts.keys() if k.startswith(context)]
            for key in keys_to_remove:
                del self.error_counts[key]
                del self.last_errors[key]
        else:
            self.error_counts.clear()
            self.last_errors.clear()
