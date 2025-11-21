"""
Validation utilities for Memorable.
"""

from typing import Any, Dict, List, Optional
import re


def validate_connection_string(connection_string: str) -> bool:
    """
    Validate database connection string format.
    
    Args:
        connection_string: Connection string to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not connection_string:
        return False

    # Check for valid database prefixes
    valid_prefixes = [
        "sqlite:///",
        "postgresql://",
        "postgres://",
        "mysql://",
        "mysql+pymysql://",
    ]

    return any(connection_string.startswith(prefix) for prefix in valid_prefixes)


def validate_memory_type(memory_type: str) -> bool:
    """
    Validate memory type.
    
    Args:
        memory_type: Memory type to validate
        
    Returns:
        True if valid, False otherwise
    """
    valid_types = ["fact", "preference", "skill", "rule", "context"]
    return memory_type in valid_types


def validate_mode(mode: str) -> bool:
    """
    Validate memory mode.
    
    Args:
        mode: Memory mode to validate
        
    Returns:
        True if valid, False otherwise
    """
    valid_modes = ["conscious", "auto", "hybrid"]
    return mode in valid_modes


def sanitize_content(content: str, max_length: int = 10000) -> str:
    """
    Sanitize memory content.
    
    Args:
        content: Content to sanitize
        max_length: Maximum content length
        
    Returns:
        Sanitized content
    """
    if not content:
        return ""

    # Trim whitespace
    content = content.strip()

    # Limit length
    if len(content) > max_length:
        content = content[:max_length] + "..."

    return content


def validate_messages(messages: List[Dict[str, Any]]) -> bool:
    """
    Validate conversation messages format.
    
    Args:
        messages: List of message dictionaries
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(messages, list):
        return False

    for msg in messages:
        if not isinstance(msg, dict):
            return False
        if "role" not in msg or "content" not in msg:
            return False
        if not isinstance(msg["content"], str):
            return False

    return True

