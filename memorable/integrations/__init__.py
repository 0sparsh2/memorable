"""Framework integrations."""

from memorable.integrations.openai import setup_openai_integration, is_openai_client
from memorable.integrations.anthropic import setup_anthropic_integration, is_anthropic_client
from memorable.integrations.litellm import setup_litellm_integration, is_litellm_call
from memorable.integrations.langchain import setup_langchain_integration
from memorable.integrations.autogen import setup_autogen_integration

__all__ = [
    "setup_openai_integration",
    "is_openai_client",
    "setup_anthropic_integration",
    "is_anthropic_client",
    "setup_litellm_integration",
    "is_litellm_call",
    "setup_langchain_integration",
    "setup_autogen_integration",
]
