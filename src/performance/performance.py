"""
Performance optimization module for RivalSearchMCP.
Provides caching, concurrent processing, and performance monitoring.
"""

import asyncio
import time
import functools
import logging
from typing import Dict, Any, Optional, List, Callable, TypeVar, Generic
from datetime import datetime, timedelta
from collections import OrderedDict
import hashlib
import json

from src.logging.logger import logger

T = TypeVar('T')


class LRUCache(Generic[T]):
    """Least Recently Used cache implementation."""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: Optional[int] = None):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self.logger = logging.getLogger("LRUCache")
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from function arguments."""
        key_data = {
            "args": args,
            "kwargs": sorted(kwargs.items())
        }
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[T]:
        """Get value from cache."""
        if key in self.cache:
            item = self.cache[key]
            
            # Check TTL
            if self.ttl_seconds and "timestamp" in item:
                if datetime.now().timestamp() - item["timestamp"] > self.ttl_seconds:
                    del self.cache[key]
                    return None
            
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return item["value"]
        
        return None
    
    def put(self, key: str, value: T) -> None:
        """Put value in cache."""
        # Remove oldest if at capacity
        if len(self.cache) >= self.max_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[key] = {
            "value": value,
            "timestamp": datetime.now().timestamp()
        }
        # Move to end (most recently used)
        self.cache.move_to_end(key)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
    
    def size(self) -> int:
        """Get current cache size."""
        return len(self.cache)
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "ttl_seconds": self.ttl_seconds,
            "utilization": len(self.cache) / self.max_size if self.max_size > 0 else 0
        }


def cache_result(
    max_size: int = 1000,
    ttl_seconds: Optional[int] = None,
    key_generator: Optional[Callable] = None
):
    """Decorator for caching function results."""
    
    cache = LRUCache(max_size=max_size, ttl_seconds=ttl_seconds)
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            if key_generator:
                cache_key = key_generator(*args, **kwargs)
            else:
                cache_key = cache._generate_key(*args, **kwargs)
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache.put(cache_key, result)
            logger.debug(f"Cache miss for {func.__name__}, result cached")
            
            return result
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generate cache key
            if key_generator:
                cache_key = key_generator(*args, **kwargs)
            else:
                cache_key = cache._generate_key(*args, **kwargs)
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.put(cache_key, result)
            logger.debug(f"Cache miss for {func.__name__}, result cached")
            
            return result
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


class ConcurrentProcessor:
    """Handles concurrent processing of multiple operations."""
    
    def __init__(self, max_concurrent: int = 10, timeout_seconds: Optional[float] = None):
        self.max_concurrent = max_concurrent
        self.timeout_seconds = timeout_seconds
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.logger = logging.getLogger("ConcurrentProcessor")
    
    async def process_concurrently(
        self,
        operations: List[Callable],
        *args,
        **kwargs
    ) -> List[Any]:
        """Process multiple operations concurrently."""
        
        async def process_single(operation: Callable) -> Any:
            async with self.semaphore:
                try:
                    if asyncio.iscoroutinefunction(operation):
                        return await operation(*args, **kwargs)
                    else:
                        # Run sync functions in thread pool
                        loop = asyncio.get_event_loop()
                        return await loop.run_in_executor(None, operation, *args, **kwargs)
                except Exception as e:
                    self.logger.error(f"Operation {operation.__name__} failed: {e}")
                    return {"error": str(e), "operation": operation.__name__}
        
        # Create tasks for all operations
        tasks = [process_single(op) for op in operations]
        
        # Execute with timeout if specified
        if self.timeout_seconds:
            try:
                results = await asyncio.wait_for(
                    asyncio.gather(*tasks, return_exceptions=True),
                    timeout=self.timeout_seconds
                )
            except asyncio.TimeoutError:
                self.logger.warning(f"Concurrent processing timed out after {self.timeout_seconds}s")
                # Note: Cannot cancel regular function calls, just log timeout
                raise
        else:
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return results
    
    async def process_batch(
        self,
        items: List[Any],
        processor_func: Callable,
        batch_size: int = 10,
        *args,
        **kwargs
    ) -> List[Any]:
        """Process items in batches with concurrent processing within each batch."""
        
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_operations = [lambda item=item: processor_func(item, *args, **kwargs) for item in batch]
            
            try:
                batch_results = await self.process_concurrently(batch_operations)
                results.extend(batch_results)
                
                self.logger.info(f"Processed batch {i//batch_size + 1}/{(len(items) + batch_size - 1)//batch_size}")
                
            except Exception as e:
                self.logger.error(f"Batch {i//batch_size + 1} failed: {e}")
                # Add error results for failed batch
                results.extend([{"error": str(e)} for _ in batch])
        
        return results


class PerformanceMonitor:
    
    def start(self):
        """Start performance monitoring."""
        self.logger.info("Performance monitoring started")
    
    def stop(self):
        """Stop performance monitoring."""
        self.logger.info("Performance monitoring stopped")
    
    def monitor(self, operation_name: str):
        """Context manager for monitoring operations."""
        return PerformanceMonitorContext(self, operation_name)
    """Monitors and tracks performance metrics."""
    
    def __init__(self):
        self.operation_times: Dict[str, List[float]] = {}
        self.operation_counts: Dict[str, int] = {}
        self.error_counts: Dict[str, int] = {}
        self.start_time = datetime.now()
        self.logger = logging.getLogger("PerformanceMonitor")
    
    def record_operation(
        self,
        operation_name: str,
        duration: float,
        success: bool = True
    ) -> None:
        """Record operation performance metrics."""
        
        if operation_name not in self.operation_times:
            self.operation_times[operation_name] = []
            self.operation_counts[operation_name] = 0
            self.error_counts[operation_name] = 0
        
        self.operation_times[operation_name].append(duration)
        self.operation_counts[operation_name] += 1
        
        if not success:
            self.error_counts[operation_name] += 1
        
        # Keep only recent measurements (last 100)
        if len(self.operation_times[operation_name]) > 100:
            self.operation_times[operation_name] = self.operation_times[operation_name][-100:]
    
    def get_operation_stats(self, operation_name: str) -> Dict[str, Any]:
        """Get performance statistics for a specific operation."""
        
        if operation_name not in self.operation_times:
            return {"error": f"Operation '{operation_name}' not found"}
        
        times = self.operation_times[operation_name]
        total_count = self.operation_counts[operation_name]
        error_count = self.error_counts[operation_name]
        
        if not times:
            return {"error": "No timing data available"}
        
        return {
            "operation": operation_name,
            "total_count": total_count,
            "success_count": total_count - error_count,
            "error_count": error_count,
            "success_rate": (total_count - error_count) / total_count if total_count > 0 else 0,
            "avg_time_ms": (sum(times) / len(times)) * 1000,
            "min_time_ms": min(times) * 1000,
            "max_time_ms": max(times) * 1000,
            "recent_times_ms": [t * 1000 for t in times[-10:]]  # Last 10 measurements
        }
    
    def get_overall_stats(self) -> Dict[str, Any]:
        """Get overall performance statistics."""
        
        total_operations = sum(self.operation_counts.values())
        total_errors = sum(self.error_counts.values())
        
        if total_operations == 0:
            return {"error": "No operations recorded"}
        
        # Calculate overall averages
        all_times = []
        for times in self.operation_times.values():
            all_times.extend(times)
        
        overall_avg = sum(all_times) / len(all_times) if all_times else 0
        
        return {
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "total_operations": total_operations,
            "total_errors": total_errors,
            "overall_success_rate": (total_operations - total_errors) / total_operations,
            "overall_avg_time_ms": overall_avg * 1000,
            "operations_tracked": list(self.operation_counts.keys()),
            "summary_timestamp": datetime.now().isoformat()
        }
    
    def reset_stats(self) -> None:
        """Reset all performance statistics."""
        self.operation_times.clear()
        self.operation_counts.clear()
        self.error_counts.clear()
        self.start_time = datetime.now()
        self.logger.info("Performance statistics reset")


class PerformanceMonitorContext:
    """Context manager for performance monitoring."""
    
    def __init__(self, monitor: PerformanceMonitor, operation_name: str):
        self.monitor = monitor
        self.operation_name = operation_name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = time.perf_counter() - self.start_time
            success = exc_type is None
            self.monitor.record_operation(self.operation_name, duration, success)

# Global performance monitor instance
performance_monitor = PerformanceMonitor()


def monitor_performance(operation_name: Optional[str] = None):
    """Decorator for monitoring function performance."""
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            op_name = operation_name or func.__name__
            
            try:
                result = await func(*args, **kwargs)
                duration = time.perf_counter() - start_time
                performance_monitor.record_operation(op_name, duration, success=True)
                return result
            except Exception as e:
                duration = time.perf_counter() - start_time
                performance_monitor.record_operation(op_name, duration, success=False)
                raise
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            op_name = operation_name or func.__name__
            
            try:
                result = func(*args, **kwargs)
                duration = time.perf_counter() - start_time
                performance_monitor.record_operation(op_name, duration, success=True)
                return result
            except Exception as e:
                duration = time.perf_counter() - start_time
                performance_monitor.record_operation(op_name, duration, success=False)
                raise
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


# Example usage functions
async def example_concurrent_processing():
    """Example of concurrent processing."""
    
    processor = ConcurrentProcessor(max_concurrent=5, timeout_seconds=30.0)
    
    # Example operations
    async def sample_operation(item: str) -> str:
        await asyncio.sleep(0.1)  # Simulate work
        return f"Processed: {item}"
    
    items = [f"item_{i}" for i in range(20)]
    results = await processor.process_batch(items, sample_operation, batch_size=5)
    
    return results


# Performance optimization utilities
def optimize_search_queries(queries: List[str], max_concurrent: int = 5) -> List[str]:
    """Optimize search queries for better performance."""
    
    # Remove duplicates while preserving order
    seen = set()
    optimized = []
    
    for query in queries:
        normalized = query.strip().lower()
        if normalized and normalized not in seen:
            seen.add(normalized)
            optimized.append(query)
    
    # Limit concurrent queries
    if len(optimized) > max_concurrent:
        optimized = optimized[:max_concurrent]
    
    return optimized


def create_performance_report() -> Dict[str, Any]:
    """Create a comprehensive performance report."""
    
    return {
        "overall_stats": performance_monitor.get_overall_stats(),
        "operation_details": {
            op: performance_monitor.get_operation_stats(op)
            for op in performance_monitor.operation_counts.keys()
        },
        "recommendations": generate_performance_recommendations()
    }


def generate_performance_recommendations() -> List[str]:
    """Generate performance improvement recommendations."""
    
    recommendations = []
    overall_stats = performance_monitor.get_overall_stats()
    
    if "error" in overall_stats:
        return ["Unable to generate recommendations - no performance data available"]
    
    # Analyze success rate
    if overall_stats["overall_success_rate"] < 0.95:
        recommendations.append("Consider improving error handling and retry logic")
    
    # Analyze response times
    if overall_stats["overall_avg_time_ms"] > 1000:
        recommendations.append("Consider implementing caching for slow operations")
    
    # Analyze operation distribution
    if len(overall_stats["operations_tracked"]) > 10:
        recommendations.append("Consider consolidating similar operations")
    
    # General recommendations
    recommendations.extend([
        "Monitor cache hit rates and adjust cache sizes as needed",
        "Use concurrent processing for I/O-bound operations",
        "Implement request batching where possible",
        "Consider async processing for long-running operations"
    ])
    
    return recommendations
