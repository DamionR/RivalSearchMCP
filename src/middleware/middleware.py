"""
Middleware module for RivalSearchMCP.
Provides production-ready middleware for monitoring, security, and performance.
"""

import time
import logging
from typing import Dict, Any, Optional
from collections import defaultdict
from datetime import datetime, timedelta

from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.exceptions import ToolError, ResourceError, PromptError


class TimingMiddleware(Middleware):
    """Middleware for timing MCP operations."""
    
    def __init__(self, log_slow_operations: bool = True, slow_threshold_ms: float = 1000.0):
        self.log_slow_operations = log_slow_operations
        self.slow_threshold_ms = slow_threshold_ms
        self.logger = logging.getLogger("timing")
    
    async def on_request(self, context: MiddlewareContext, call_next):
        start_time = time.perf_counter()
        
        try:
            result = await call_next(context)
            duration_ms = (time.perf_counter() - start_time) * 1000
            
            if self.log_slow_operations and duration_ms > self.slow_threshold_ms:
                self.logger.warning(
                    f"Slow operation detected: {context.method} took {duration_ms:.2f}ms"
                )
            else:
                self.logger.info(
                    f"Operation completed: {context.method} in {duration_ms:.2f}ms"
                )
            
            return result
            
        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self.logger.error(
                f"Operation failed: {context.method} after {duration_ms:.2f}ms: {e}"
            )
            raise


class LoggingMiddleware(Middleware):
    """Middleware for comprehensive request/response logging."""
    
    def __init__(self, include_payloads: bool = False, max_payload_length: int = 1000):
        self.include_payloads = include_payloads
        self.max_payload_length = max_payload_length
        self.logger = logging.getLogger("mcp_requests")
    
    async def on_message(self, context: MiddlewareContext, call_next):
        # Log incoming message
        self.logger.info(
            f"Processing {context.method} from {context.source} "
            f"(type: {context.type})"
        )
        
        if self.include_payloads:
            payload_str = str(context.message)[:self.max_payload_length]
            if len(str(context.message)) > self.max_payload_length:
                payload_str += "... [truncated]"
            self.logger.debug(f"Message payload: {payload_str}")
        
        try:
            result = await call_next(context)
            self.logger.info(f"Completed {context.method} successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed {context.method}: {type(e).__name__}: {e}")
            raise


class RateLimitingMiddleware(Middleware):
    """Middleware for rate limiting MCP operations."""
    
    def __init__(self, max_requests_per_minute: int = 60, per_client: bool = True):
        self.max_requests_per_minute = max_requests_per_minute
        self.per_client = per_client
        self.client_requests = defaultdict(list)
        self.logger = logging.getLogger("rate_limiting")
    
    def _get_client_id(self, context: MiddlewareContext) -> str:
        """Extract client identifier from context."""
        if self.per_client and context.fastmcp_context:
            return context.fastmcp_context.client_id or "unknown"
        return "global"
    
    async def on_request(self, context: MiddlewareContext, call_next):
        client_id = self._get_client_id(context)
        current_time = time.time()
        
        # Clean old requests
        cutoff_time = current_time - 60
        self.client_requests[client_id] = [
            req_time for req_time in self.client_requests[client_id]
            if req_time > cutoff_time
        ]
        
        # Check rate limit
        if len(self.client_requests[client_id]) >= self.max_requests_per_minute:
            self.logger.warning(f"Rate limit exceeded for client: {client_id}")
            raise ToolError(
                f"Rate limit exceeded. Maximum {self.max_requests_per_minute} "
                f"requests per minute allowed."
            )
        
        # Add current request
        self.client_requests[client_id].append(current_time)
        
        return await call_next(context)


class ErrorHandlingMiddleware(Middleware):
    """Middleware for consistent error handling and logging."""
    
    def __init__(self, include_traceback: bool = False, transform_errors: bool = True):
        self.include_traceback = include_traceback
        self.transform_errors = transform_errors
        self.logger = logging.getLogger("error_handling")
        self.error_counts = defaultdict(int)
    
    async def on_message(self, context: MiddlewareContext, call_next):
        try:
            return await call_next(context)
            
        except Exception as error:
            # Track error statistics
            error_key = f"{type(error).__name__}:{context.method}"
            self.error_counts[error_key] += 1
            
            # Log error details
            self.logger.error(
                f"Error in {context.method}: {type(error).__name__}: {error}",
                exc_info=self.include_traceback
            )
            
            # Transform errors if enabled
            if self.transform_errors:
                if isinstance(error, (ToolError, ResourceError, PromptError)):
                    # FastMCP errors are already properly formatted
                    raise
                else:
                    # Transform generic errors to FastMCP errors
                    method = context.method or ""
                    if method.startswith("tools/"):
                        raise ToolError(f"Tool execution failed: {str(error)}")
                    elif method.startswith("resources/"):
                        raise ResourceError(f"Resource access failed: {str(error)}")
                    elif method.startswith("prompts/"):
                        raise PromptError(f"Prompt execution failed: {str(error)}")
                    else:
                        raise ToolError(f"Operation failed: {str(error)}")
            else:
                raise


class PerformanceMonitoringMiddleware(Middleware):
    """Middleware for performance monitoring and metrics collection."""
    
    def __init__(self):
        self.operation_times = defaultdict(list)
        self.operation_counts = defaultdict(int)
        self.error_counts = defaultdict(int)
        self.logger = logging.getLogger("performance")
    
    async def on_request(self, context: MiddlewareContext, call_next):
        start_time = time.perf_counter()
        operation = context.method
        
        try:
            result = await call_next(context)
            duration = time.perf_counter() - start_time
            
            # Record successful operation
            self.operation_times[operation].append(duration)
            self.operation_counts[operation] += 1
            
            # Keep only recent measurements (last 100)
            if len(self.operation_times[operation]) > 100:
                self.operation_times[operation] = self.operation_times[operation][-100:]
            
            return result
            
        except Exception as e:
            duration = time.perf_counter() - start_time
            self.error_counts[operation] += 1
            
            # Record failed operation timing
            self.operation_times[operation].append(duration)
            self.operation_counts[operation] += 1
            
            raise
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        metrics = {}
        
        for operation in self.operation_counts:
            times = self.operation_times[operation]
            if times:
                metrics[operation] = {
                    "count": self.operation_counts[operation],
                    "error_count": self.error_counts[operation],
                    "avg_time_ms": (sum(times) / len(times)) * 1000,
                    "min_time_ms": min(times) * 1000,
                    "max_time_ms": max(times) * 1000,
                    "success_rate": 1 - (self.error_counts[operation] / self.operation_counts[operation])
                }
        
        return metrics


class SecurityMiddleware(Middleware):
    """Middleware for security monitoring and validation."""
    
    def __init__(self, block_suspicious_requests: bool = True):
        self.block_suspicious_requests = block_suspicious_requests
        self.logger = logging.getLogger("security")
        self.suspicious_patterns = [
            "script", "javascript", "eval", "exec", "system",
            "rm -rf", "drop table", "union select"
        ]
    
    def _is_suspicious(self, context: MiddlewareContext) -> bool:
        """Check if request contains suspicious patterns."""
        message_str = str(context.message).lower()
        return any(pattern in message_str for pattern in self.suspicious_patterns)
    
    async def on_request(self, context: MiddlewareContext, call_next):
        if self._is_suspicious(context):
            self.logger.warning(f"Suspicious request detected: {context.method}")
            
            if self.block_suspicious_requests:
                raise ToolError("Request blocked due to security concerns")
        
        return await call_next(context)


def register_middleware(mcp) -> None:
    """Register all middleware with the FastMCP server."""
    
    # Add middleware in logical order (last added runs first)
    mcp.add_middleware(SecurityMiddleware(block_suspicious_requests=True))
    mcp.add_middleware(ErrorHandlingMiddleware(include_traceback=False, transform_errors=True))
    mcp.add_middleware(RateLimitingMiddleware(max_requests_per_minute=120, per_client=True))
    mcp.add_middleware(PerformanceMonitoringMiddleware())
    mcp.add_middleware(TimingMiddleware(log_slow_operations=True, slow_threshold_ms=2000.0))
    mcp.add_middleware(LoggingMiddleware(include_payloads=True, max_payload_length=500))
    
    # Log middleware registration
    logging.getLogger("middleware").info("All middleware registered successfully")
