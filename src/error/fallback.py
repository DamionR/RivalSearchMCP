#!/usr/bin/env python3
"""
Fallback strategies for RivalSearchMCP.
"""

import logging
from typing import Any, Callable, Dict, Optional
from .recovery import ErrorRecoveryStrategy

class SearchFallbackStrategy(ErrorRecoveryStrategy):
    """Fallback strategy for search operations."""
    
    def __init__(self, fallback_engines: Optional[list[str]] = None):
        super().__init__(max_retries=2, backoff_factor=1.5)
        self.fallback_engines = fallback_engines or ["google", "bing", "duckduckgo"]
        self.logger = logging.getLogger("SearchFallback")
    
    async def execute_with_fallback(
        self, 
        primary_operation: Callable,
        fallback_operations: Dict[str, Callable],
        *args, 
        **kwargs
    ) -> Any:
        """Execute primary operation with fallback to alternatives."""
        
        # Try primary operation first
        try:
            self.logger.info("Attempting primary search operation")
            return await primary_operation(*args, **kwargs)
            
        except Exception as e:
            self.logger.warning(f"Primary operation failed: {e}")
            
            # Try fallback operations
            for engine_name, fallback_op in fallback_operations.items():
                try:
                    self.logger.info(f"Trying fallback: {engine_name}")
                    result = await fallback_op(*args, **kwargs)
                    
                    if result:
                        self.logger.info(f"Fallback {engine_name} successful")
                        return {
                            "status": "fallback_success",
                            "method": engine_name,
                            "data": result,
                            "fallback_reason": str(e)
                        }
                        
                except Exception as fallback_error:
                    self.logger.warning(f"Fallback {engine_name} failed: {fallback_error}")
                    continue
            
            # All fallbacks failed
            raise e

class ContentRetrievalFallback(ErrorRecoveryStrategy):
    """Fallback strategy for content retrieval operations."""
    
    def __init__(self, fallback_methods: Optional[list[str]] = None):
        super().__init__(max_retries=2, backoff_factor=1.0)
        self.fallback_methods = fallback_methods or ["direct", "proxy", "archive"]
        self.logger = logging.getLogger("ContentRetrievalFallback")
    
    async def execute_with_fallback(
        self, 
        primary_operation: Callable,
        fallback_operations: Dict[str, Callable],
        *args, 
        **kwargs
    ) -> Any:
        """Execute primary operation with fallback to alternatives."""
        
        # Try primary operation first
        try:
            self.logger.info("Attempting primary content retrieval")
            return await primary_operation(*args, **kwargs)
            
        except Exception as e:
            self.logger.warning(f"Primary operation failed: {e}")
            
            # Try fallback operations
            for method_name, fallback_op in fallback_operations.items():
                try:
                    self.logger.info(f"Trying fallback: {method_name}")
                    result = await fallback_op(*args, **kwargs)
                    
                    if result:
                        self.logger.info(f"Fallback {method_name} successful")
                        return {
                            "status": "fallback_success",
                            "method": method_name,
                            "data": result,
                            "fallback_reason": str(e)
                        }
                        
                except Exception as fallback_error:
                    self.logger.warning(f"Fallback {method_name} failed: {fallback_error}")
                    continue
            
            # All fallbacks failed
            raise e
