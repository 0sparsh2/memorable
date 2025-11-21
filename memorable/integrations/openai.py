"""
OpenAI Integration

Native OpenAI client integration.
"""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


def setup_openai_integration(memory_engine: Any):
    """
    Setup OpenAI integration.
    
    The interceptor automatically handles OpenAI, but this provides
    additional utilities if needed.
    
    Args:
        memory_engine: MemoryEngine instance
    """
    logger.info("OpenAI integration ready (handled by interceptor)")


def is_openai_client(obj: Any) -> bool:
    """Check if object is an OpenAI client."""
    try:
        from openai import OpenAI
        return isinstance(obj, OpenAI)
    except ImportError:
        return False

