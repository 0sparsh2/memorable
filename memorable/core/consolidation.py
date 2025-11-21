"""
Memory Consolidation

Background agent that analyzes patterns and promotes essential memories.
Inspired by Mem0's consolidation techniques.

Reference: "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory"
arXiv:2504.19413 (April 2025)
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class MemoryConsolidator:
    """
    Background agent that consolidates and promotes memories.
    
    Analyzes memory patterns and promotes important memories from
    short-term to long-term storage.
    """

    def __init__(
        self,
        storage: Any,
        interval: int = 21600,  # 6 hours default
    ):
        """
        Initialize memory consolidator.
        
        Args:
            storage: Storage instance
            interval: Consolidation interval in seconds (default: 6 hours)
        """
        self.storage = storage
        self.interval = interval
        self._running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self):
        """Start background consolidation task."""
        if self._running:
            logger.warning("Consolidator already running")
            return

        self._running = True
        self._task = asyncio.create_task(self._consolidation_loop())
        logger.info(f"Memory consolidator started (interval: {self.interval}s)")

    async def stop(self):
        """Stop background consolidation task."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Memory consolidator stopped")

    async def _consolidation_loop(self):
        """Main consolidation loop."""
        while self._running:
            try:
                await self.consolidate()
                await asyncio.sleep(self.interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Consolidation error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying

    async def consolidate(self):
        """
        Perform memory consolidation.
        
        - Analyzes memory access patterns
        - Promotes frequently accessed memories
        - Detects and resolves contradictions
        - Removes outdated memories
        """
        logger.debug("Starting memory consolidation...")

        try:
            # Get all memories
            memories = await self.storage.get_memories(limit=10000)

            # 1. Update importance scores based on access patterns
            await self._update_importance_scores(memories)

            # 2. Detect and resolve contradictions
            await self._resolve_contradictions(memories)

            # 3. Remove outdated memories (optional - can be configured)
            # await self._remove_outdated(memories)

            logger.debug(f"Consolidation complete: {len(memories)} memories processed")
        except Exception as e:
            logger.error(f"Consolidation failed: {e}")

    async def _update_importance_scores(self, memories: List[Dict[str, Any]]):
        """
        Update importance scores based on access patterns.
        
        Factors:
        - Access frequency
        - Recency
        - Memory type
        - Relationships (if graph enabled)
        """
        for memory in memories:
            memory_id = memory.get("id")
            if not memory_id:
                continue

            # Calculate importance score
            # Base score from current importance
            base_score = memory.get("importance_score", 0.0)

            # Factor in access count (if available)
            access_count = memory.get("metadata", {}).get("access_count", 0)
            access_bonus = min(access_count * 0.1, 1.0)  # Cap at 1.0

            # Factor in recency
            created_at = memory.get("created_at")
            if created_at:
                try:
                    created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    age_days = (datetime.now(created.tzinfo) - created).days
                    recency_factor = max(1.0 - (age_days / 365.0), 0.0)  # Decay over 1 year
                except Exception:
                    recency_factor = 0.5
            else:
                recency_factor = 0.5

            # Memory type weights
            type_weights = {
                "preference": 1.2,
                "skill": 1.1,
                "fact": 1.0,
                "rule": 1.3,
                "context": 0.8,
            }
            memory_type = memory.get("type", "fact")
            type_weight = type_weights.get(memory_type, 1.0)

            # Calculate new importance score
            new_score = (base_score * 0.5) + (access_bonus * 0.3) + (recency_factor * 0.2)
            new_score *= type_weight

            # Update in storage
            await self.storage.update_memory_importance(memory_id, new_score)

    async def _resolve_contradictions(self, memories: List[Dict[str, Any]]):
        """
        Detect and resolve contradictory memories.
        
        Strategies:
        - Keep more recent memory
        - Keep memory with higher importance
        - Flag for user confirmation (future enhancement)
        """
        # Group memories by content similarity
        memory_groups: Dict[str, List[Dict[str, Any]]] = {}

        for memory in memories:
            content = memory.get("content", "").lower().strip()
            # Simple grouping by first few words (can be enhanced with semantic similarity)
            key = " ".join(content.split()[:3]) if content else ""
            if key:
                if key not in memory_groups:
                    memory_groups[key] = []
                memory_groups[key].append(memory)

        # Check for contradictions in each group
        for key, group in memory_groups.items():
            if len(group) < 2:
                continue

            # Look for contradictory statements
            # Simple heuristic: check for negation patterns
            for i, mem1 in enumerate(group):
                for mem2 in group[i + 1:]:
                    if self._are_contradictory(mem1, mem2):
                        # Resolve: keep more recent or more important
                        resolved = self._resolve_contradiction(mem1, mem2)
                        if resolved:
                            # Mark the other for deletion or demotion
                            other = mem2 if resolved == mem1 else mem1
                            other_id = other.get("id")
                            if other_id:
                                # Demote instead of delete (safer)
                                await self.storage.update_memory_importance(
                                    other_id, other.get("importance_score", 0.0) * 0.5
                                )

    def _are_contradictory(
        self, mem1: Dict[str, Any], mem2: Dict[str, Any]
    ) -> bool:
        """
        Check if two memories are contradictory.
        
        Simple heuristic: look for negation patterns.
        Can be enhanced with semantic similarity.
        """
        content1 = mem1.get("content", "").lower()
        content2 = mem2.get("content", "").lower()

        # Check for explicit contradictions
        negation_words = ["don't", "do not", "never", "not", "hate", "dislike"]
        positive_words = ["like", "love", "prefer", "enjoy"]

        has_negation1 = any(word in content1 for word in negation_words)
        has_negation2 = any(word in content2 for word in negation_words)
        has_positive1 = any(word in content1 for word in positive_words)
        has_positive2 = any(word in content2 for word in positive_words)

        # If one has negation and other has positive, might be contradictory
        if (has_negation1 and has_positive2) or (has_negation2 and has_positive1):
            # Check if they're about the same topic (simple word overlap)
            words1 = set(content1.split())
            words2 = set(content2.split())
            overlap = len(words1.intersection(words2))
            if overlap >= 2:  # At least 2 common words
                return True

        return False

    def _resolve_contradiction(
        self, mem1: Dict[str, Any], mem2: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Resolve contradiction by choosing which memory to keep.
        
        Returns the memory to keep, or None if can't decide.
        """
        # Prefer more recent
        created1 = mem1.get("created_at")
        created2 = mem2.get("created_at")

        if created1 and created2:
            try:
                dt1 = datetime.fromisoformat(created1.replace("Z", "+00:00"))
                dt2 = datetime.fromisoformat(created2.replace("Z", "+00:00"))
                if dt1 > dt2:
                    return mem1
                elif dt2 > dt1:
                    return mem2
            except Exception:
                pass

        # Prefer higher importance
        score1 = mem1.get("importance_score", 0.0)
        score2 = mem2.get("importance_score", 0.0)

        if score1 > score2:
            return mem1
        elif score2 > score1:
            return mem2

        # Can't decide
        return None

    async def _remove_outdated(self, memories: List[Dict[str, Any]]):
        """
        Remove outdated memories (optional).
        
        This is conservative - only removes very old, low-importance memories.
        """
        cutoff_date = datetime.now() - timedelta(days=365)  # 1 year

        for memory in memories:
            created_at = memory.get("created_at")
            importance = memory.get("importance_score", 0.0)

            if not created_at:
                continue

            try:
                created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                if created < cutoff_date and importance < 0.1:
                    # Very old and low importance - can be removed
                    memory_id = memory.get("id")
                    if memory_id:
                        await self.storage.delete_memory(memory_id)
                        logger.debug(f"Removed outdated memory: {memory_id}")
            except Exception:
                pass

