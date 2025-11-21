"""
Conscious Mode

One-shot working memory injection - retrieves and injects relevant memories
once per conversation session.

Inspired by Memori's conscious_ingest mode.

Reference: https://github.com/GibsonAI/Memori
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ConsciousMode:
    """
    Conscious mode: One-shot memory injection.
    
    Retrieves relevant memories at the start of conversation
    and injects them as context.
    """

    def __init__(self, retriever: Any):
        """
        Initialize conscious mode.
        
        Args:
            retriever: HybridRetriever instance
        """
        self.retriever = retriever
        self._injected_memories: Dict[str, List[Dict[str, Any]]] = {}

    async def get_context(
        self, session_id: str, messages: List[Dict[str, Any]]
    ) -> str:
        """
        Get context for conversation session.
        
        Retrieves memories once per session and caches them.
        
        Args:
            session_id: Unique session identifier
            messages: Conversation messages
            
        Returns:
            Formatted context string
        """
        # Check if already injected for this session
        if session_id in self._injected_memories:
            memories = self._injected_memories[session_id]
        else:
            # Retrieve memories once
            memories = await self.retriever.retrieve(messages, limit=10)
            self._injected_memories[session_id] = memories

        return self._format_memories(memories)

    def _format_memories(self, memories: List[Dict[str, Any]]) -> str:
        """Format memories for context injection."""
        if not memories:
            return ""

        formatted = ["Relevant memories from previous conversations:"]
        for memory in memories:
            content = memory.get("content", "")
            memory_type = memory.get("type", "fact")
            formatted.append(f"- [{memory_type}] {content}")

        return "\n".join(formatted)

    def clear_session(self, session_id: str):
        """Clear cached memories for a session."""
        if session_id in self._injected_memories:
            del self._injected_memories[session_id]

