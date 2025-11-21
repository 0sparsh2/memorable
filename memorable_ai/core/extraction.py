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
        """
        Extract text content from messages and response.
        
        Focuses on the latest user message and LLM response to extract new memories,
        avoiding re-extraction from historical conversation.
        """
        text_parts = []

        # Extract text from the latest user message (most recent information)
        # Look for the last user message in the conversation
        for msg in reversed(messages):
            if isinstance(msg, dict):
                role = msg.get("role", "")
                # Focus on user messages (they contain new information)
                if role == "user":
                    content = msg.get("content", "")
                    if content:
                        text_parts.append(content)
                        # Only extract from the latest user message to avoid duplicates
                        break
            elif isinstance(msg, str):
                text_parts.append(msg)
                break

        # If no user message found, fall back to all messages
        if not text_parts:
            for msg in messages:
                if isinstance(msg, dict):
                    content = msg.get("content", "")
                    if content:
                        text_parts.append(content)
                elif isinstance(msg, str):
                    text_parts.append(msg)

        # Extract text from LLM response (may contain additional facts)
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
        - Third-person: "[Name] lives in...", "[Name] works at...", etc.
        """
        facts = []
        
        # Simple pattern matching (can be enhanced with LLM)
        # First-person patterns
        first_person_patterns = [
            r"I (?:am|have|work at|live in|use|build|create) ([^\.\?]+)",
            r"My (?:name is|email is|phone is|address is) ([^\.\?]+)",
            r"I'm (?:a|an) ([^\.\?]+)",
        ]
        
        # Third-person patterns - extract full statement
        # Pattern: "[Name] [verb] [location/description]"
        # These patterns match the full statement including the name
        # Match capitalized names (proper nouns) at word boundaries
        third_person_patterns = [
            # "[Name] lives in [place]"
            r"([A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+)?) (?:lives in|lives at|lives) ([^\.\?]+)",
            # "[Name] works at/in [place]"
            r"([A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+)?) (?:works at|works in|works) ([^\.\?]+)",
            # "[Name] is from [place]"
            r"([A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+)?) (?:is from|is) ([^\.\?]+)",
            # "[Name] has [attribute]"
            r"([A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+)?) (?:has|has a|has an) ([^\.\?]+)",
        ]
        
        # Extract first-person facts
        for pattern in first_person_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                fact_text = match.group(1).strip()
                if len(fact_text) > 5:  # Filter very short matches
                    facts.append({
                        "content": fact_text,
                        "type": "fact",
                        "metadata": {"extraction_method": "pattern"},
                    })
        
        # Extract third-person facts - store full statement
        for pattern in third_person_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                person = match.group(1).strip()
                description = match.group(2).strip()
                # Create a complete fact statement: "Person [verb] description"
                # Get the full matched text and clean it
                full_match = match.group(0).strip().rstrip('?').strip()
                
                if len(full_match) > 5:  # Filter very short matches
                    facts.append({
                        "content": full_match,
                        "type": "fact",
                        "metadata": {"extraction_method": "pattern", "person": person},
                    })

        return facts

    async def _extract_preferences(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract user preferences.
        
        Patterns:
        - "I like...", "I prefer...", "I love..."
        - "I don't like...", "I hate..."
        - Third-person: "[Name] likes...", "[Name] prefers...", etc.
        """
        preferences = []

        # First-person patterns
        first_person_patterns = [
            r"I (?:like|love|prefer|enjoy|favorite) ([^\.\?]+)",
            r"I (?:don't|do not) (?:like|enjoy) ([^\.\?]+)",
            r"I (?:hate|dislike) ([^\.\?]+)",
            r"My favorite ([^\.\?]+) is ([^\.\?]+)",
        ]
        
        # Third-person patterns
        third_person_patterns = [
            # "[Name] likes [thing]"
            r"([A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+)?) (?:likes|loves|prefers|enjoys) ([^\.\?]+)",
            # "[Name] hates [thing]"
            r"([A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+)?) (?:hates|dislikes) ([^\.\?]+)",
        ]

        # Extract first-person preferences
        for pattern in first_person_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if match.groups():
                    pref_text = match.group(1).strip() if match.group(1) else ""
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
        
        # Extract third-person preferences - store full statement
        for pattern in third_person_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                person = match.group(1).strip() if match.group(1) else ""
                thing = match.group(2).strip() if len(match.groups()) > 1 and match.group(2) else ""
                # Get the full matched text
                full_match = match.group(0).strip().rstrip('?').strip()
                
                if len(full_match) > 5:
                    sentiment = "positive" if "hates" not in pattern and "dislikes" not in pattern else "negative"
                    preferences.append({
                        "content": full_match,
                        "type": "preference",
                        "metadata": {
                            "sentiment": sentiment,
                            "extraction_method": "pattern",
                            "person": person,
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
        """
        Remove duplicate memories based on content similarity.
        
        Handles both exact duplicates and partial duplicates (e.g., "he lives in Seattle" 
        vs "sparsh, he lives in Seattle"). Keeps the longer, more complete version.
        """
        if not memories:
            return []
        
        # First pass: filter empty and sort by length (longer first)
        valid_memories = []
        for memory in memories:
            content = memory.get("content", "").strip()
            if content:
                valid_memories.append((len(content), memory))
        
        # Sort by length descending (longer memories first)
        valid_memories.sort(key=lambda x: x[0], reverse=True)
        
        seen = set()
        unique_memories = []

        for _, memory in valid_memories:
            content = memory["content"].strip()
            content_lower = content.lower().strip()
            
            # Skip exact duplicates
            if content_lower in seen:
                continue
            
            # Check for partial duplicates (one contains the other)
            is_subset = False
            for seen_content in seen:
                seen_lower = seen_content.lower()
                # If current content is a substring of an existing (longer) memory, skip it
                # We prefer longer, more complete memories
                if len(content_lower) < len(seen_lower) and content_lower in seen_lower:
                    # Current is a substring of existing, skip it
                    is_subset = True
                    break
            
            if not is_subset:
                # Also check if any existing memory is a substring of current
                # If so, remove the shorter one and keep the longer
                to_remove = []
                for idx, existing_mem in enumerate(unique_memories):
                    existing_content_lower = existing_mem["content"].lower().strip()
                    if existing_content_lower in content_lower and len(existing_content_lower) < len(content_lower):
                        # Existing is a substring of current, mark for removal
                        to_remove.append((idx, existing_content_lower))
                
                # Remove shorter versions
                for idx, content_to_remove in reversed(to_remove):
                    unique_memories.pop(idx)
                    seen.remove(content_to_remove)
                
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

