"""
Auto Mode

Dynamic per-query retrieval - retrieves relevant memories for each query.

Inspired by Memori's auto_ingest mode.

Reference: https://github.com/GibsonAI/Memori
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class AutoMode:
    """
    Auto mode: Dynamic per-query retrieval.
    
    Retrieves relevant memories for each query dynamically.
    """

    def __init__(self, retriever: Any):
        """
        Initialize auto mode.
        
        Args:
            retriever: HybridRetriever instance
        """
        self.retriever = retriever

    async def get_context(self, messages: List[Dict[str, Any]]) -> str:
        """
        Get context for current query.
        
        Retrieves memories dynamically based on current conversation.
        
        Args:
            messages: Current conversation messages
            
        Returns:
            Formatted context string
        """
        # Retrieve memories for current query
        memories = await self.retriever.retrieve(messages, limit=10)

        return self._format_memories(memories)

    def _format_memories(self, memories: List[Dict[str, Any]]) -> str:
        """Format memories for context injection."""
        if not memories:
            return ""

        formatted = ["Relevant memories:"]
        for memory in memories:
            content = memory.get("content", "")
            memory_type = memory.get("type", "fact")
            formatted.append(f"- [{memory_type}] {content}")

        return "\n".join(formatted)

