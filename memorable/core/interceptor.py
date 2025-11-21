"""
LLM Call Interceptor

Transparently intercepts LLM calls to inject context and record conversations.
Inspired by Memori's interceptor-based architecture.

Reference: https://github.com/GibsonAI/Memori
"""

import functools
import inspect
from typing import Any, Callable, Dict, List, Optional, Union
import logging

logger = logging.getLogger(__name__)


class LLMInterceptor:
    """
    Intercepts LLM API calls transparently to inject memory context
    and record conversations for memory storage.
    
    This allows zero-code integration - existing code works unchanged.
    """

    def __init__(self, memory_engine: Any):
        """
        Initialize interceptor with memory engine.
        
        Args:
            memory_engine: MemoryEngine instance for context injection and storage
        """
        self.memory_engine = memory_engine
        self._original_methods: Dict[str, Callable] = {}
        self._enabled = False

    def enable(self):
        """Enable interception of LLM calls."""
        if self._enabled:
            logger.warning("Interceptor already enabled")
            return

        self._enabled = True
        self._hook_openai()
        self._hook_anthropic()
        self._hook_litellm()
        logger.info("LLM interceptor enabled")

    def disable(self):
        """Disable interception and restore original methods."""
        if not self._enabled:
            return

        self._restore_openai()
        self._restore_anthropic()
        self._restore_litellm()
        self._enabled = False
        logger.info("LLM interceptor disabled")

    def _hook_openai(self):
        """Hook OpenAI client methods."""
        try:
            from openai import OpenAI

            # Hook the chat.completions.create method
            if hasattr(OpenAI, "chat") and hasattr(OpenAI.chat, "completions"):
                original_create = OpenAI.chat.completions.create

                @functools.wraps(original_create)
                def sync_wrapper(*args, **kwargs):
                    return self._intercept_call_sync(original_create, *args, **kwargs)

                # Replace with wrapper
                OpenAI.chat.completions.create = sync_wrapper
                self._original_methods["openai.chat.completions.create"] = original_create
                logger.debug("OpenAI interceptor hooked")
        except ImportError:
            logger.debug("OpenAI not available, skipping hook")

    def _hook_anthropic(self):
        """Hook Anthropic client methods."""
        try:
            from anthropic import Anthropic

            if hasattr(Anthropic, "messages") and hasattr(Anthropic.messages, "create"):
                original_create = Anthropic.messages.create

                @functools.wraps(original_create)
                def sync_wrapper(*args, **kwargs):
                    return self._intercept_call_sync(original_create, *args, **kwargs)

                Anthropic.messages.create = sync_wrapper
                self._original_methods["anthropic.messages.create"] = original_create
                logger.debug("Anthropic interceptor hooked")
        except ImportError:
            logger.debug("Anthropic not available, skipping hook")

    def _hook_litellm(self):
        """Hook LiteLLM completion function."""
        try:
            import litellm
            from litellm import completion

            original_completion = completion

            @functools.wraps(original_completion)
            def sync_wrapper(*args, **kwargs):
                return self._intercept_call_sync(original_completion, *args, **kwargs)

            litellm.completion = sync_wrapper
            self._original_methods["litellm.completion"] = original_completion
            logger.debug("LiteLLM interceptor hooked")
        except ImportError:
            logger.debug("LiteLLM not available, skipping hook")

    def _restore_openai(self):
        """Restore original OpenAI methods."""
        if "openai.chat.completions.create" in self._original_methods:
            try:
                from openai import OpenAI
                OpenAI.chat.completions.create = self._original_methods["openai.chat.completions.create"]
                logger.debug("OpenAI methods restored")
            except ImportError:
                pass

    def _restore_anthropic(self):
        """Restore original Anthropic methods."""
        if "anthropic.messages.create" in self._original_methods:
            try:
                from anthropic import Anthropic
                Anthropic.messages.create = self._original_methods["anthropic.messages.create"]
                logger.debug("Anthropic methods restored")
            except ImportError:
                pass

    def _restore_litellm(self):
        """Restore original LiteLLM function."""
        if "litellm.completion" in self._original_methods:
            try:
                import litellm
                litellm.completion = self._original_methods["litellm.completion"]
                logger.debug("LiteLLM function restored")
            except ImportError:
                pass

    def _intercept_call_sync(self, original_func: Callable, *args, **kwargs):
        """
        Intercept sync LLM call: inject context, call LLM, store response.
        
        Args:
            original_func: Original LLM function to call
            *args: Positional arguments
            **kwargs: Keyword arguments (messages, etc.)
            
        Returns:
            LLM response
        """
        # Extract messages from kwargs
        messages = kwargs.get("messages", [])
        if not messages and args:
            if isinstance(args[0], list):
                messages = args[0]

        # Pre-call: Retrieve relevant memories and inject context
        if messages and self.memory_engine:
            try:
                enhanced_messages = self.memory_engine._inject_context_sync(messages)
                if enhanced_messages and len(enhanced_messages) > len(messages):
                    logger.info(f"Context injected: {len(enhanced_messages)} messages (original: {len(messages)})")
                    if enhanced_messages[0].get("role") == "system":
                        context_preview = enhanced_messages[0].get("content", "")[:200]
                        logger.debug(f"Injected context preview: {context_preview}...")
                    kwargs["messages"] = enhanced_messages
                elif enhanced_messages:
                    logger.debug(f"No context injected, returning original messages")
            except Exception as e:
                logger.warning(f"Failed to inject context: {e}")
                import traceback
                logger.debug(traceback.format_exc())

        # Call original LLM function
        try:
            response = original_func(*args, **kwargs)
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise

        # Post-call: Extract and store memories from conversation
        if messages and response and self.memory_engine:
            try:
                self.memory_engine._store_conversation_sync(messages, response)
            except Exception as e:
                logger.warning(f"Failed to store conversation: {e}")

        return response
