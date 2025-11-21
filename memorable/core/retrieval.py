"""
Hybrid Retrieval System

Combines semantic search, keyword search, and graph traversal.
Inspired by Mem0's research-backed retrieval techniques.

Reference: "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory"
arXiv:2504.19413 (April 2025)
"""

import logging
from typing import Any, Dict, List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class HybridRetriever:
    """
    Hybrid retrieval system combining:
    - Semantic search (vector embeddings)
    - Keyword search (full-text)
    - Graph traversal (if graph enabled)
    """

    def __init__(
        self,
        storage: Any,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        graph: Optional[Any] = None,
    ):
        """
        Initialize hybrid retriever.
        
        Args:
            storage: Storage instance
            embedding_model: Model for generating embeddings
            graph: Optional graph instance for graph-based retrieval
        """
        self.storage = storage
        self.graph = graph
        self.embedding_model_name = embedding_model
        
        # Load embedding model
        try:
            self.embedding_model = SentenceTransformer(embedding_model)
            logger.info(f"Loaded embedding model: {embedding_model}")
        except Exception as e:
            logger.warning(f"Failed to load embedding model: {e}")
            self.embedding_model = None

    async def retrieve(
        self, messages: List[Dict[str, Any]], limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant memories for conversation.
        
        Args:
            messages: Conversation messages
            limit: Maximum number of memories to retrieve
            
        Returns:
            List of relevant memories
        """
        # Extract query from last user message
        query = self._extract_query(messages)
        if not query:
            # If no query, return recent memories
            return await self.storage.get_memories(limit=limit)

        # Retrieve using hybrid approach
        semantic_results = []
        keyword_results = []
        graph_results = []

        # 1. Semantic search (if embeddings available)
        if self.embedding_model:
            semantic_results = await self._semantic_search(query, limit=limit)

        # 2. Keyword search
        keyword_results = await self.storage.search_memories_text(
            query, limit=limit
        )

        # 3. Graph traversal (if graph enabled)
        if self.graph:
            graph_results = await self._graph_retrieve(query, limit=limit)

        # Combine and rank results
        combined = self._combine_and_rank(
            semantic_results, keyword_results, graph_results, limit=limit
        )

        # If no results from specific search and query is generic (like "describe me"),
        # fall back to returning recent/important memories
        if not combined:
            # Check if query is generic (short or common phrases)
            generic_queries = ["describe me", "tell me about", "who am i", "what do you know"]
            query_lower = query.lower().strip()
            if len(query.split()) <= 3 or any(gen in query_lower for gen in generic_queries):
                # Return recent/important memories for generic queries
                logger.debug(f"Generic query '{query}' detected, returning recent memories")
                all_memories = await self.storage.get_memories(limit=limit)
                combined = all_memories

        return combined

    async def search(
        self,
        query: str,
        limit: int = 10,
        memory_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search memories by query.
        
        Args:
            query: Search query
            limit: Maximum number of results
            memory_type: Filter by memory type
            
        Returns:
            List of matching memories
        """
        results = []

        # Semantic search
        if self.embedding_model:
            semantic = await self._semantic_search(query, limit=limit, memory_type=memory_type)
            results.extend(semantic)

        # Keyword search
        keyword = await self.storage.search_memories_text(
            query, limit=limit, memory_type=memory_type
        )
        results.extend(keyword)

        # Deduplicate and rank
        results = self._deduplicate_and_rank(results, limit=limit)

        return results

    def _extract_query(self, messages: List[Dict[str, Any]]) -> str:
        """Extract search query from conversation messages."""
        if not messages:
            return ""

        # Get last user message
        for msg in reversed(messages):
            if isinstance(msg, dict):
                role = msg.get("role", "")
                if role == "user":
                    content = msg.get("content", "")
                    if content:
                        return content
            elif isinstance(msg, str):
                return msg

        return ""

    async def _semantic_search(
        self, query: str, limit: int = 10, memory_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Semantic search using vector embeddings.
        
        Args:
            query: Search query
            limit: Maximum results
            memory_type: Filter by type
            
        Returns:
            List of similar memories
        """
        if not self.embedding_model:
            return []

        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()

            # Get all memories with embeddings
            memories = await self.storage.get_memories(memory_type=memory_type, limit=1000)

            # Calculate similarities
            scored_memories = []
            for memory in memories:
                if memory.get("embedding"):
                    memory_embedding = memory["embedding"]
                    similarity = self._cosine_similarity(
                        query_embedding, memory_embedding
                    )
                    scored_memories.append({
                        **memory,
                        "similarity": similarity,
                    })

            # Sort by similarity and return top results
            scored_memories.sort(key=lambda x: x["similarity"], reverse=True)
            return scored_memories[:limit]

        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return []

    async def _graph_retrieve(
        self, query: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Graph-based retrieval using relationship traversal.
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of related memories from graph
        """
        if not self.graph:
            return []

        try:
            # Use graph to find related entities
            related = await self.graph.find_related(query, limit=limit)
            return related
        except Exception as e:
            logger.error(f"Graph retrieval failed: {e}")
            return []

    def _combine_and_rank(
        self,
        semantic_results: List[Dict[str, Any]],
        keyword_results: List[Dict[str, Any]],
        graph_results: List[Dict[str, Any]],
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Combine results from different retrieval methods and rank.
        
        Uses weighted scoring:
        - Semantic similarity: 0.4
        - Keyword match: 0.3
        - Graph relevance: 0.3
        """
        # Create a map of memory ID to combined score
        memory_scores: Dict[int, Dict[str, Any]] = {}

        # Add semantic results
        for i, mem in enumerate(semantic_results):
            mem_id = mem.get("id", i)
            if mem_id not in memory_scores:
                memory_scores[mem_id] = {"memory": mem, "score": 0.0}
            memory_scores[mem_id]["score"] += mem.get("similarity", 0.0) * 0.4

        # Add keyword results
        for i, mem in enumerate(keyword_results):
            mem_id = mem.get("id", i)
            if mem_id not in memory_scores:
                memory_scores[mem_id] = {"memory": mem, "score": 0.0}
            # Higher score for earlier results (better keyword match)
            keyword_score = (len(keyword_results) - i) / len(keyword_results) if keyword_results else 0.0
            memory_scores[mem_id]["score"] += keyword_score * 0.3

        # Add graph results
        for i, mem in enumerate(graph_results):
            mem_id = mem.get("id", i)
            if mem_id not in memory_scores:
                memory_scores[mem_id] = {"memory": mem, "score": 0.0}
            graph_score = (len(graph_results) - i) / len(graph_results) if graph_results else 0.0
            memory_scores[mem_id]["score"] += graph_score * 0.3

        # Sort by combined score
        ranked = sorted(
            memory_scores.values(), key=lambda x: x["score"], reverse=True
        )

        return [item["memory"] for item in ranked[:limit]]

    def _deduplicate_and_rank(
        self, results: List[Dict[str, Any]], limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Remove duplicates and rank by relevance."""
        seen = set()
        unique = []

        for result in results:
            result_id = result.get("id")
            if result_id and result_id not in seen:
                seen.add(result_id)
                unique.append(result)

        return unique[:limit]

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        try:
            v1 = np.array(vec1)
            v2 = np.array(vec2)
            dot_product = np.dot(v1, v2)
            norm1 = np.linalg.norm(v1)
            norm2 = np.linalg.norm(v2)
            if norm1 == 0 or norm2 == 0:
                return 0.0
            return float(dot_product / (norm1 * norm2))
        except Exception as e:
            logger.error(f"Cosine similarity calculation failed: {e}")
            return 0.0

