"""
Helper utilities for Memorable.
"""

import hashlib
from typing import Any, Dict, List, Optional
from datetime import datetime


def generate_memory_id(content: str, memory_type: str) -> str:
    """
    Generate a unique ID for a memory.
    
    Args:
        content: Memory content
        memory_type: Memory type
        
    Returns:
        Unique memory ID
    """
    combined = f"{content}:{memory_type}"
    return hashlib.md5(combined.encode()).hexdigest()


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """
    Format timestamp for storage.
    
    Args:
        dt: Datetime object (default: now)
        
    Returns:
        ISO format timestamp string
    """
    if dt is None:
        dt = datetime.utcnow()
    return dt.isoformat()


def parse_timestamp(timestamp_str: str) -> datetime:
    """
    Parse timestamp string.
    
    Args:
        timestamp_str: ISO format timestamp string
        
    Returns:
        Datetime object
    """
    # Handle various timestamp formats
    timestamp_str = timestamp_str.replace("Z", "+00:00")
    return datetime.fromisoformat(timestamp_str)


def chunk_text(text: str, max_length: int = 1000) -> List[str]:
    """
    Chunk text into smaller pieces.
    
    Args:
        text: Text to chunk
        max_length: Maximum length per chunk
        
    Returns:
        List of text chunks
    """
    if len(text) <= max_length:
        return [text]

    chunks = []
    words = text.split()
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk + [word])) <= max_length:
            current_chunk.append(word)
        else:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate simple text similarity (Jaccard similarity).
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        Similarity score between 0 and 1
    """
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    if not words1 or not words2:
        return 0.0

    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))

    return intersection / union if union > 0 else 0.0


def merge_memories(memories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Merge similar memories.
    
    Args:
        memories: List of memory dictionaries
        
    Returns:
        Merged list of memories
    """
    if not memories:
        return []

    merged = []
    seen = set()

    for memory in memories:
        content = memory.get("content", "").lower().strip()
        if content in seen:
            continue

        # Check for similar memories
        similar_found = False
        for existing in merged:
            similarity = calculate_similarity(content, existing.get("content", ""))
            if similarity > 0.8:  # 80% similarity threshold
                # Merge metadata
                existing_meta = existing.get("metadata", {})
                memory_meta = memory.get("metadata", {})
                existing_meta.update(memory_meta)
                similar_found = True
                break

        if not similar_found:
            merged.append(memory)
            seen.add(content)

    return merged

