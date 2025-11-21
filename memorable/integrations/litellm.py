"""
LiteLLM Integration

LiteLLM callback integration for 100+ models.
Inspired by Memori's LiteLLM integration.

Reference: https://github.com/GibsonAI/Memori
"""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


def setup_litellm_integration(memory_engine: Any):
    """
    Setup LiteLLM integration.
    
    The interceptor automatically handles LiteLLM, but this provides
    additional utilities if needed.
    
    Args:
        memory_engine: MemoryEngine instance
    """
    logger.info("LiteLLM integration ready (handled by interceptor)")


def is_litellm_call(func: Any) -> bool:
    """Check if function is LiteLLM completion."""
    try:
        import litellm
        return func == litellm.completion
    except ImportError:
        return False

