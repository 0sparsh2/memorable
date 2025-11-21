"""
Anthropic Integration

Native Anthropic client integration.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def setup_anthropic_integration(memory_engine: Any):
    """
    Setup Anthropic integration.
    
    The interceptor automatically handles Anthropic, but this provides
    additional utilities if needed.
    
    Args:
        memory_engine: MemoryEngine instance
    """
    logger.info("Anthropic integration ready (handled by interceptor)")


def is_anthropic_client(obj: Any) -> bool:
    """Check if object is an Anthropic client."""
    try:
        from anthropic import Anthropic
        return isinstance(obj, Anthropic)
    except ImportError:
        return False

