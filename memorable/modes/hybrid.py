"""
Hybrid Mode

Combines conscious and auto modes for best of both approaches.

Inspired by Memori's combined mode.

Reference: https://github.com/GibsonAI/Memori
"""

import logging
from typing import Any, Dict, List

from memorable.modes.conscious import ConsciousMode
from memorable.modes.auto import AutoMode

logger = logging.getLogger(__name__)


class HybridMode:
    """
    Hybrid mode: Combines conscious and auto retrieval.
    
    Uses conscious mode for session-level context and
    auto mode for query-specific context.
    """

    def __init__(self, retriever: Any):
        """
        Initialize hybrid mode.
        
        Args:
            retriever: HybridRetriever instance
        """
        self.conscious = ConsciousMode(retriever)
        self.auto = AutoMode(retriever)

    async def get_context(
        self, session_id: str, messages: List[Dict[str, Any]]
    ) -> str:
        """
        Get context combining both modes.
        
        Args:
            session_id: Session identifier
            messages: Current conversation messages
            
        Returns:
            Combined formatted context
        """
        # Get conscious (session-level) context
        conscious_context = await self.conscious.get_context(session_id, messages)
        
        # Get auto (query-specific) context
        auto_context = await self.auto.get_context(messages)
        
        # Combine
        if conscious_context and auto_context:
            return f"{conscious_context}\n\n{auto_context}"
        elif conscious_context:
            return conscious_context
        elif auto_context:
            return auto_context
        else:
            return ""

    def clear_session(self, session_id: str):
        """Clear cached memories for a session."""
        self.conscious.clear_session(session_id)

