"""
Performance monitoring utilities.
"""

import time
import functools
from typing import Any, Callable, Optional
import logging

logger = logging.getLogger(__name__)


def time_function(func: Callable) -> Callable:
    """
    Decorator to time function execution.
    
    Args:
        func: Function to time
        
    Returns:
        Wrapped function
    """
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = await func(*args, **kwargs)
            elapsed = time.time() - start
            logger.debug(f"{func.__name__} took {elapsed:.3f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start
            logger.error(f"{func.__name__} failed after {elapsed:.3f}s: {e}")
            raise

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            logger.debug(f"{func.__name__} took {elapsed:.3f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start
            logger.error(f"{func.__name__} failed after {elapsed:.3f}s: {e}")
            raise

    import inspect
    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


class PerformanceMonitor:
    """Monitor performance metrics."""

    def __init__(self):
        self.metrics: dict = {}

    def record(self, operation: str, duration: float, **metadata):
        """
        Record a performance metric.
        
        Args:
            operation: Operation name
            duration: Duration in seconds
            **metadata: Additional metadata
        """
        if operation not in self.metrics:
            self.metrics[operation] = {
                "count": 0,
                "total_time": 0.0,
                "min_time": float("inf"),
                "max_time": 0.0,
                "metadata": [],
            }

        metric = self.metrics[operation]
        metric["count"] += 1
        metric["total_time"] += duration
        metric["min_time"] = min(metric["min_time"], duration)
        metric["max_time"] = max(metric["max_time"], duration)
        if metadata:
            metric["metadata"].append(metadata)

    def get_stats(self, operation: Optional[str] = None) -> dict:
        """
        Get performance statistics.
        
        Args:
            operation: Specific operation (optional)
            
        Returns:
            Statistics dictionary
        """
        if operation:
            if operation not in self.metrics:
                return {}
            metric = self.metrics[operation]
            return {
                "operation": operation,
                "count": metric["count"],
                "total_time": metric["total_time"],
                "avg_time": metric["total_time"] / metric["count"] if metric["count"] > 0 else 0,
                "min_time": metric["min_time"] if metric["min_time"] != float("inf") else 0,
                "max_time": metric["max_time"],
            }
        else:
            return {
                op: self.get_stats(op)
                for op in self.metrics.keys()
            }

