#!/usr/bin/env python3
"""
Error handling package for RivalSearchMCP.
"""

from .recovery import ErrorRecoveryStrategy
from .fallback import SearchFallbackStrategy, ContentRetrievalFallback
from .handler import RobustOperationWrapper, ErrorHandler

__all__ = [
    # Recovery strategies
    "ErrorRecoveryStrategy",
    
    # Fallback strategies
    "SearchFallbackStrategy",
    "ContentRetrievalFallback",
    
    # Error handling
    "RobustOperationWrapper",
    "ErrorHandler"
]
