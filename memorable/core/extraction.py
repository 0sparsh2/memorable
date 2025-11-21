"""
Memory Extraction

Extracts entities, facts, preferences, skills, and rules from conversations.
Inspired by Mem0's research-backed extraction techniques.

Reference: "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory"
arXiv:2504.19413 (April 2025)
"""

import logging
from typing import Any, Dict, List, Optional
import re

logger = logging.getLogger(__name__)


class MemoryExtractor:
    """
    Extracts structured memories from conversations.
    
    Categorizes memories into:
    - facts: Objective information
    - preferences: User preferences and likes/dislikes
    - skills: Capabilities and expertise
    - rules: Constraints and guidelines
    - context: Situational context
    """

    def __init__(self, llm_client: Optional[Any] = None, embedding_model: Optional[Any] = None):
        """
        Initialize memory extractor.
        
        Args:
            llm_client: Optional LLM client for advanced extraction
            embedding_model: Optional embedding model for generating embeddings
        """
        self.llm_client = llm_client
        self.embedding_model = embedding_model

    async def extract(
        self, messages: List[Dict[str, Any]], response: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Extract memories from conversation.
        
        Args:
            messages: Conversation messages
            response: LLM response (optional)
            
        Returns:
            List of extracted memories
        """
        memories = []

        # Combine all text from conversation
        conversation_text = self._extract_text(messages, response)

        # Extract different types of memories
        memories.extend(await self._extract_facts(conversation_text))
        memories.extend(await self._extract_preferences(conversation_text))
        memories.extend(await self._extract_skills(conversation_text))
        memories.extend(await self._extract_rules(conversation_text))
        memories.extend(await self._extract_context(conversation_text))

        # Deduplicate and clean
        memories = self._deduplicate_memories(memories)

        # Generate embeddings for memories (if embedding model available)
        if self.embedding_model:
            for memory in memories:
                try:
                    embedding = self.embedding_model.encode(memory["content"]).tolist()
                    memory["embedding"] = embedding
                except Exception as e:
                    logger.debug(f"Failed to generate embedding: {e}")

        logger.debug(f"Extracted {len(memories)} memories from conversation")
        return memories

    def _extract_text(
        self, messages: List[Dict[str, Any]], response: Optional[Any] = None
    ) -> str:
        """Extract text content from messages and response."""
        text_parts = []

        for msg in messages:
            if isinstance(msg, dict):
                content = msg.get("content", "")
                if content:
                    text_parts.append(content)
            elif isinstance(msg, str):
                text_parts.append(msg)

        if response:
            if isinstance(response, dict):
                # Handle OpenAI format
                if "choices" in response:
                    for choice in response["choices"]:
                        if "message" in choice:
                            text_parts.append(choice["message"].get("content", ""))
                # Handle Anthropic format
                elif "content" in response:
                    for block in response["content"]:
                        if isinstance(block, dict) and "text" in block:
                            text_parts.append(block["text"])
            elif isinstance(response, str):
                text_parts.append(response)

        return " ".join(text_parts)

    async def _extract_facts(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract factual information.
        
        Patterns:
        - "I am...", "I have...", "I work at..."
        - "My name is...", "I live in..."
        """
        facts = []
        
        # Simple pattern matching (can be enhanced with LLM)
        patterns = [
            r"I (?:am|have|work at|live in|use|build|create) ([^\.]+)",
            r"My (?:name is|email is|phone is|address is) ([^\.]+)",
            r"I'm (?:a|an) ([^\.]+)",
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                fact_text = match.group(1).strip()
                if len(fact_text) > 5:  # Filter very short matches
                    facts.append({
                        "content": fact_text,
                        "type": "fact",
                        "metadata": {"extraction_method": "pattern"},
                    })

        return facts

    async def _extract_preferences(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract user preferences.
        
        Patterns:
        - "I like...", "I prefer...", "I love..."
        - "I don't like...", "I hate..."
        """
        preferences = []

        patterns = [
            r"I (?:like|love|prefer|enjoy|favorite) ([^\.]+)",
            r"I (?:don't|do not) (?:like|enjoy) ([^\.]+)",
            r"I (?:hate|dislike) ([^\.]+)",
            r"My favorite ([^\.]+) is ([^\.]+)",
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                pref_text = match.group(1).strip()
                if len(pref_text) > 3:
                    sentiment = "positive" if "don't" not in pattern and "hate" not in pattern else "negative"
                    preferences.append({
                        "content": pref_text,
                        "type": "preference",
                        "metadata": {
                            "sentiment": sentiment,
                            "extraction_method": "pattern",
                        },
                    })

        return preferences

    async def _extract_skills(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract skills and capabilities.
        
        Patterns:
        - "I can...", "I know how to...", "I'm good at..."
        """
        skills = []

        patterns = [
            r"I (?:can|know how to|am good at|excel at) ([^\.]+)",
            r"I (?:have experience with|am skilled in) ([^\.]+)",
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                skill_text = match.group(1).strip()
                if len(skill_text) > 5:
                    skills.append({
                        "content": skill_text,
                        "type": "skill",
                        "metadata": {"extraction_method": "pattern"},
                    })

        return skills

    async def _extract_rules(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract rules and constraints.
        
        Patterns:
        - "Always...", "Never...", "Don't..."
        """
        rules = []

        patterns = [
            r"(?:Always|Never|Don't|Do not) ([^\.]+)",
            r"Rule: ([^\.]+)",
            r"Constraint: ([^\.]+)",
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                rule_text = match.group(1).strip()
                if len(rule_text) > 5:
                    rules.append({
                        "content": rule_text,
                        "type": "rule",
                        "metadata": {"extraction_method": "pattern"},
                    })

        return rules

    async def _extract_context(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract contextual information.
        
        Patterns:
        - "Currently...", "Right now...", "I'm working on..."
        """
        contexts = []

        patterns = [
            r"(?:Currently|Right now|I'm working on|I'm building) ([^\.]+)",
            r"Context: ([^\.]+)",
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                context_text = match.group(1).strip()
                if len(context_text) > 5:
                    contexts.append({
                        "content": context_text,
                        "type": "context",
                        "metadata": {"extraction_method": "pattern"},
                    })

        return contexts

    def _deduplicate_memories(
        self, memories: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Remove duplicate memories based on content similarity."""
        seen = set()
        unique_memories = []

        for memory in memories:
            content_lower = memory["content"].lower().strip()
            if content_lower not in seen:
                seen.add(content_lower)
                unique_memories.append(memory)

        return unique_memories

    async def extract_with_llm(
        self, text: str, memory_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Use LLM for advanced memory extraction.
        
        This is more accurate than pattern matching but requires LLM calls.
        
        Args:
            text: Text to extract from
            memory_types: Types of memories to extract (optional)
            
        Returns:
            List of extracted memories
        """
        if not self.llm_client:
            logger.warning("LLM client not available, using pattern matching")
            return []

        # TODO: Implement LLM-based extraction
        # This would use the LLM to identify and categorize memories
        # More accurate but slower and costs tokens
        
        return []

