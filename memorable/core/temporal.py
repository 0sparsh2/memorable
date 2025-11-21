"""
Temporal Memory Tracking

Tracks temporal relationships and maintains coherence over time.
Inspired by research on temporal compression in discourse.

Reference: "Highly engaging events reveal semantic and temporal compression 
in online community discourse" - PNAS Nexus (March 2025)
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class TemporalMemory:
    """
    Tracks temporal relationships between memories.
    
    Maintains:
    - Time-stamped memories
    - Before/after relationships
    - Event sequences
    - Temporal coherence
    """

    def __init__(self, storage: Any):
        """
        Initialize temporal memory tracker.
        
        Args:
            storage: Storage instance
        """
        self.storage = storage

    async def add_temporal_memory(
        self,
        content: str,
        memory_type: str = "fact",
        timestamp: Optional[datetime] = None,
        before: Optional[List[int]] = None,
        after: Optional[List[int]] = None,
        **metadata
    ) -> Dict[str, Any]:
        """
        Add a memory with temporal information.
        
        Args:
            content: Memory content
            memory_type: Type of memory
            timestamp: When this memory occurred (default: now)
            before: IDs of memories that happened before this
            after: IDs of memories that happened after this
            **metadata: Additional metadata
            
        Returns:
            Created memory dictionary
        """
        if timestamp is None:
            timestamp = datetime.now()

        memory = {
            "content": content,
            "type": memory_type,
            "metadata": {
                **metadata,
                "timestamp": timestamp.isoformat(),
                "before": before or [],
                "after": after or [],
            },
        }

        await self.storage.store_memories([memory])
        return memory

    async def get_temporal_sequence(
        self, start_memory_id: int, direction: str = "forward", limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get temporal sequence of memories.
        
        Args:
            start_memory_id: Starting memory ID
            direction: "forward" (after) or "backward" (before)
            limit: Maximum number of memories to retrieve
            
        Returns:
            List of memories in temporal order
        """
        memories = await self.storage.get_memories(limit=1000)
        start_memory = next((m for m in memories if m.get("id") == start_memory_id), None)

        if not start_memory:
            return []

        sequence = [start_memory]
        visited = {start_memory_id}

        if direction == "forward":
            # Get memories that come after
            after_ids = start_memory.get("metadata", {}).get("after", [])
            for mem_id in after_ids[:limit]:
                if mem_id not in visited:
                    mem = next((m for m in memories if m.get("id") == mem_id), None)
                    if mem:
                        sequence.append(mem)
                        visited.add(mem_id)
        else:
            # Get memories that come before
            before_ids = start_memory.get("metadata", {}).get("before", [])
            for mem_id in before_ids[:limit]:
                if mem_id not in visited:
                    mem = next((m for m in memories if m.get("id") == mem_id), None)
                    if mem:
                        sequence.insert(0, mem)
                        visited.add(mem_id)

        return sequence

    async def get_memories_by_time_range(
        self,
        start_time: datetime,
        end_time: datetime,
        memory_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get memories within a time range.
        
        Args:
            start_time: Start of time range
            end_time: End of time range
            memory_type: Filter by memory type (optional)
            
        Returns:
            List of memories in time range
        """
        memories = await self.storage.get_memories(
            memory_type=memory_type, limit=10000
        )

        result = []
        for memory in memories:
            metadata = memory.get("metadata", {})
            timestamp_str = metadata.get("timestamp")

            if not timestamp_str:
                continue

            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                if start_time <= timestamp <= end_time:
                    result.append(memory)
            except Exception as e:
                logger.debug(f"Failed to parse timestamp: {e}")
                continue

        # Sort by timestamp
        result.sort(
            key=lambda m: m.get("metadata", {}).get("timestamp", ""), reverse=True
        )

        return result

    def extract_temporal_relationships(self, text: str) -> Dict[str, Any]:
        """
        Extract temporal relationships from text.
        
        Patterns:
        - "Before...", "After...", "Then...", "Next..."
        - "In 2020...", "Last year...", "Recently..."
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with temporal information
        """
        import re

        relationships = {
            "before": [],
            "after": [],
            "timestamp": None,
        }

        # Extract time references
        time_patterns = [
            r"(?:in|on|at) (\d{4})",  # "in 2020"
            r"(?:last|next) (?:year|month|week)",  # "last year"
            r"recently|yesterday|today|tomorrow",
        ]

        for pattern in time_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if match.group(0):
                    relationships["timestamp"] = match.group(0)

        # Extract sequence markers
        sequence_patterns = [
            (r"before ([^\.]+)", "before"),
            (r"after ([^\.]+)", "after"),
            (r"then ([^\.]+)", "after"),
            (r"next ([^\.]+)", "after"),
        ]

        for pattern, rel_type in sequence_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if match.group(1):
                    relationships[rel_type].append(match.group(1).strip())

        return relationships

    async def check_temporal_coherence(
        self, memories: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Check temporal coherence of memories.
        
        Detects:
        - Out-of-order sequences
        - Missing temporal links
        - Inconsistent timestamps
        
        Args:
            memories: List of memories to check
            
        Returns:
            Dictionary with coherence analysis
        """
        issues = []
        warnings = []

        # Check for timestamps
        memories_with_time = [
            m for m in memories if m.get("metadata", {}).get("timestamp")
        ]
        memories_without_time = [
            m for m in memories if not m.get("metadata", {}).get("timestamp")
        ]

        if memories_without_time:
            warnings.append(
                f"{len(memories_without_time)} memories missing timestamps"
            )

        # Check for out-of-order sequences
        if len(memories_with_time) > 1:
            timestamps = []
            for mem in memories_with_time:
                try:
                    ts_str = mem.get("metadata", {}).get("timestamp")
                    if ts_str:
                        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                        timestamps.append((mem.get("id"), ts))
                except Exception:
                    pass

            # Check if sorted
            if len(timestamps) > 1:
                sorted_timestamps = sorted(timestamps, key=lambda x: x[1])
                if timestamps != sorted_timestamps:
                    issues.append("Memories are out of temporal order")

        return {
            "coherent": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "memories_with_time": len(memories_with_time),
            "memories_without_time": len(memories_without_time),
        }

