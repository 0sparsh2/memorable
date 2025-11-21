"""
Main Memory Engine

Combines interceptor, storage, retrieval, and extraction components.
Inspired by Memori's easy integration, Mem0's research-backed techniques,
and Supermemory's graph architecture.

References:
- Memori: https://github.com/GibsonAI/Memori
- Mem0: https://github.com/mem0ai/mem0
- Supermemory: https://github.com/supermemoryai/supermemory
"""

import logging
from typing import Any, Dict, List, Optional

from memorable.core.interceptor import LLMInterceptor
from memorable.core.storage import Storage
from memorable.core.extraction import MemoryExtractor
from memorable.core.retrieval import HybridRetriever
from memorable.core.consolidation import MemoryConsolidator
from memorable.core.temporal import TemporalMemory
from memorable.graph.builder import GraphBuilder
from memorable.utils.config import MemorableConfig

logger = logging.getLogger(__name__)


class MemoryEngine:
    """
    Main memory engine for LLMs, AI agents, and multi-agent systems.
    
    Provides transparent memory integration with zero-code setup.
    """

    def __init__(
        self,
        database: Optional[str] = None,
        graph_enabled: bool = False,
        graph_database: Optional[str] = None,
        mode: str = "auto",
        config: Optional[MemorableConfig] = None,
        **kwargs
    ):
        """
        Initialize Memory Engine.
        
        Args:
            database: Database connection string (SQLite, PostgreSQL, MySQL)
            graph_enabled: Enable graph-based memory (optional)
            graph_database: Graph database connection string (Neo4j, etc.)
            mode: Memory mode ('conscious', 'auto', or 'hybrid')
            config: Optional configuration object
            **kwargs: Additional configuration options
        """
        # Load configuration
        if config is None:
            try:
                self.config = MemorableConfig.from_env()
            except Exception:
                self.config = MemorableConfig()
            
            # Override with provided parameters
            if database:
                self.config.database.connection_string = database
            if graph_enabled:
                self.config.graph.enabled = True
            if graph_database:
                self.config.graph.connection_string = graph_database
            if mode:
                self.config.memory.mode = mode
        else:
            self.config = config

        # Initialize components
        self._storage = None
        self._retrieval = None
        self._extraction = None
        self._graph = None
        self._consolidator = None
        self._temporal = None
        self._mode_handler = None  # Will be set based on mode
        
        # Initialize interceptor
        self._interceptor = LLMInterceptor(self)
        self._enabled = False

    def enable(self):
        """
        Enable memory engine - starts intercepting LLM calls.
        
        This is the main entry point for zero-code integration.
        """
        if self._enabled:
            logger.warning("Memory engine already enabled")
            return

        # Initialize storage and other components
        self._initialize_components()
        
        # Enable interceptor
        self._interceptor.enable()
        
        # Start consolidation background task
        if self._consolidator:
            import asyncio
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is running, create task
                    asyncio.create_task(self._consolidator.start())
                else:
                    loop.run_until_complete(self._consolidator.start())
            except RuntimeError:
                # No event loop, will start when one is available
                pass
        
        self._enabled = True
        logger.info("Memory engine enabled")

    def disable(self):
        """Disable memory engine - stops intercepting LLM calls."""
        if not self._enabled:
            return

        # Stop consolidator
        if self._consolidator:
            import asyncio
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.create_task(self._consolidator.stop())
                else:
                    loop.run_until_complete(self._consolidator.stop())
            except RuntimeError:
                pass

        self._interceptor.disable()
        self._enabled = False
        logger.info("Memory engine disabled")

    def _initialize_components(self):
        """Initialize storage, retrieval, extraction, and graph components."""
        logger.debug("Initializing components...")
        
        # Initialize storage
        if self.config.database.connection_string:
            self._storage = Storage(
                connection_string=self.config.database.connection_string,
                namespace=self.config.memory.namespace,
            )
        else:
            # Default to SQLite
            self._storage = Storage(
                connection_string="sqlite:///memorable.db",
                namespace=self.config.memory.namespace,
            )
        
        # Initialize extraction with embedding model if available
        try:
            from sentence_transformers import SentenceTransformer
            embedding_model = SentenceTransformer(self.config.llm.embedding_model)
            self._extraction = MemoryExtractor(embedding_model=embedding_model)
        except Exception:
            logger.warning("Embedding model not available, extraction will work without embeddings")
            self._extraction = MemoryExtractor()
        
        # Initialize graph if enabled
        if self.config.graph.enabled:
            self._graph = GraphBuilder(
                connection_string=self.config.graph.connection_string
            )
        
        # Initialize retrieval
        self._retrieval = HybridRetriever(
            storage=self._storage,
            embedding_model=self.config.llm.embedding_model,
            graph=self._graph if self.config.graph.enabled else None,
        )
        
        # Initialize memory mode handler
        self._initialize_mode_handler()
        
        # Initialize temporal memory
        self._temporal = TemporalMemory(self._storage)
        
        # Initialize consolidator
        self._consolidator = MemoryConsolidator(
            storage=self._storage,
            interval=self.config.memory.consolidation_interval,
        )
        
        logger.info("Components initialized")

    def _initialize_mode_handler(self):
        """Initialize memory mode handler based on configured mode."""
        from memorable.modes.conscious import ConsciousMode
        from memorable.modes.auto import AutoMode
        from memorable.modes.hybrid import HybridMode

        if self.config.memory.mode == "conscious":
            self._mode_handler = ConsciousMode(self._retrieval)
        elif self.config.memory.mode == "auto":
            self._mode_handler = AutoMode(self._retrieval)
        elif self.config.memory.mode == "hybrid":
            self._mode_handler = HybridMode(self._retrieval)
        else:
            logger.warning(f"Unknown mode {self.config.memory.mode}, defaulting to auto")
            self._mode_handler = AutoMode(self._retrieval)

    async def _inject_context(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Inject relevant memories into conversation context.
        
        Called by interceptor before LLM call.
        
        Args:
            messages: Original conversation messages
            
        Returns:
            Enhanced messages with memory context
        """
        if not self._mode_handler:
            return messages

        try:
            # Use mode handler to get context
            session_id = self._get_session_id(messages)
            if self.config.memory.mode == "auto":
                context_text = await self._mode_handler.get_context(messages)
            elif self.config.memory.mode == "conscious":
                context_text = await self._mode_handler.get_context(session_id, messages)
            elif self.config.memory.mode == "hybrid":
                context_text = await self._mode_handler.get_context(session_id, messages)
            else:
                context_text = ""

            if not context_text:
                return messages

            # Inject as system message or prepend
            enhanced = [{"role": "system", "content": context_text}] + messages
            return enhanced
        except Exception as e:
            logger.error(f"Failed to inject context: {e}")
            return messages

    def _inject_context_sync(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Synchronous version of context injection."""
        if not self._mode_handler:
            return messages

        try:
            import asyncio
            import concurrent.futures
            import threading
            
            def run_in_thread():
                """Run async code in a new thread with new event loop."""
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    session_id = self._get_session_id(messages)
                    if self.config.memory.mode == "auto":
                        context_text = new_loop.run_until_complete(
                            self._mode_handler.get_context(messages)
                        )
                    elif self.config.memory.mode == "conscious":
                        context_text = new_loop.run_until_complete(
                            self._mode_handler.get_context(session_id, messages)
                        )
                    elif self.config.memory.mode == "hybrid":
                        context_text = new_loop.run_until_complete(
                            self._mode_handler.get_context(session_id, messages)
                        )
                    else:
                        context_text = ""
                    return context_text
                finally:
                    new_loop.close()
            
            # Check if event loop is running
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is running, use thread pool to run async code
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(run_in_thread)
                        context_text = future.result(timeout=5.0)
                else:
                    # No loop running, can use run_until_complete directly
                    session_id = self._get_session_id(messages)
                    if self.config.memory.mode == "auto":
                        context_text = loop.run_until_complete(
                            self._mode_handler.get_context(messages)
                        )
                    elif self.config.memory.mode == "conscious":
                        context_text = loop.run_until_complete(
                            self._mode_handler.get_context(session_id, messages)
                        )
                    elif self.config.memory.mode == "hybrid":
                        context_text = loop.run_until_complete(
                            self._mode_handler.get_context(session_id, messages)
                        )
                    else:
                        context_text = ""
            except RuntimeError:
                # No event loop exists, create one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    session_id = self._get_session_id(messages)
                    if self.config.memory.mode == "auto":
                        context_text = loop.run_until_complete(
                            self._mode_handler.get_context(messages)
                        )
                    elif self.config.memory.mode == "conscious":
                        context_text = loop.run_until_complete(
                            self._mode_handler.get_context(session_id, messages)
                        )
                    elif self.config.memory.mode == "hybrid":
                        context_text = loop.run_until_complete(
                            self._mode_handler.get_context(session_id, messages)
                        )
                    else:
                        context_text = ""
                finally:
                    loop.close()

            if not context_text:
                return messages

            enhanced = [{"role": "system", "content": context_text}] + messages
            logger.debug(f"Injected context: {len(context_text)} chars")
            return enhanced
        except Exception as e:
            logger.error(f"Failed to inject context (sync): {e}")
            return messages

    def _get_session_id(self, messages: List[Dict[str, Any]]) -> str:
        """Extract or generate session ID from messages."""
        # Try to get from metadata
        for msg in messages:
            if isinstance(msg, dict) and "metadata" in msg:
                metadata = msg.get("metadata", {})
                if "session_id" in metadata:
                    return metadata["session_id"]
        
        # Generate from first user message
        for msg in messages:
            if isinstance(msg, dict) and msg.get("role") == "user":
                content = msg.get("content", "")
                import hashlib
                return hashlib.md5(content.encode()).hexdigest()[:8]
        
        # Default session
        return "default"

    def _format_memories(self, memories: List[Dict[str, Any]]) -> str:
        """Format memories for context injection."""
        if not memories:
            return ""

        formatted = ["Relevant memories:"]
        for memory in memories:
            memory_type = memory.get("type", "fact")
            content = memory.get("content", "")
            formatted.append(f"- [{memory_type}] {content}")

        return "\n".join(formatted)

    async def _store_conversation(
        self, messages: List[Dict[str, Any]], response: Any
    ):
        """
        Store conversation and extract memories.
        
        Called by interceptor after LLM call.
        
        Args:
            messages: Conversation messages
            response: LLM response
        """
        if not self._extraction or not self._storage:
            return

        try:
            # Extract memories from conversation
            memories = await self._extraction.extract(messages, response)
            
            # Store in database
            if memories:
                await self._storage.store_memories(memories)
                await self._storage.store_conversation(messages, response, memories)
            
            # Update graph if enabled
            if self._graph and self.config.graph.enabled:
                await self._graph.update_graph(memories)
        except Exception as e:
            logger.error(f"Failed to store conversation: {e}")

    def _store_conversation_sync(
        self, messages: List[Dict[str, Any]], response: Any
    ):
        """Synchronous version of conversation storage."""
        if not self._extraction or not self._storage:
            return

        try:
            import asyncio
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is running, schedule as task instead
                    asyncio.create_task(self._store_conversation_async(messages, response))
                    return
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Extract and store
            memories = loop.run_until_complete(
                self._extraction.extract(messages, response)
            )
            
            if memories:
                # Convert response to dict if needed
                response_dict = response
                if hasattr(response, 'model_dump'):
                    response_dict = response.model_dump()
                elif hasattr(response, 'dict'):
                    response_dict = response.dict()
                elif hasattr(response, '__dict__'):
                    try:
                        import json
                        response_dict = json.loads(json.dumps(response.__dict__, default=str))
                    except:
                        response_dict = {
                            "id": getattr(response, 'id', None),
                            "model": getattr(response, 'model', None),
                            "choices": [choice.__dict__ if hasattr(choice, '__dict__') else str(choice) 
                                       for choice in getattr(response, 'choices', [])] if hasattr(response, 'choices') else []
                        }
                
                loop.run_until_complete(
                    self._storage.store_memories(memories)
                )
                loop.run_until_complete(
                    self._storage.store_conversation(messages, response_dict, memories)
                )
        except Exception as e:
            logger.error(f"Failed to store conversation (sync): {e}")

    async def _store_conversation_async(
        self, messages: List[Dict[str, Any]], response: Any
    ):
        """Async version of conversation storage."""
        if not self._extraction or not self._storage:
            return

        try:
            # Convert response to dict if it's a ModelResponse object (from litellm)
            response_dict = response
            if response is not None:
                if hasattr(response, 'model_dump'):
                    # Pydantic v2 model
                    response_dict = response.model_dump()
                elif hasattr(response, 'dict'):
                    # Pydantic v1 model
                    response_dict = response.dict()
                elif hasattr(response, '__dict__'):
                    # Regular object - try to serialize
                    try:
                        import json
                        # Try to serialize, converting non-serializable items
                        response_dict = json.loads(json.dumps(
                            {
                                k: v if isinstance(v, (str, int, float, bool, type(None))) 
                                else str(v) if not isinstance(v, (list, dict)) 
                                else [item.__dict__ if hasattr(item, '__dict__') else str(item) for item in v] if isinstance(v, list)
                                else v
                                for k, v in response.__dict__.items()
                            },
                            default=str
                        ))
                    except Exception as e:
                        logger.warning(f"Could not fully serialize response: {e}")
                        # Fallback: create a simple dict with key attributes
                        response_dict = {
                            "id": str(getattr(response, 'id', None)),
                            "model": str(getattr(response, 'model', None)),
                            "object": getattr(response, 'object', 'chat.completion'),
                        }
                        # Try to get choices if available
                        if hasattr(response, 'choices'):
                            response_dict["choices"] = [
                                {
                                    "message": {
                                        "role": getattr(choice.message, 'role', 'assistant') if hasattr(choice, 'message') else 'assistant',
                                        "content": str(getattr(choice.message, 'content', '')) if hasattr(choice, 'message') else str(choice)
                                    }
                                } if hasattr(choice, 'message') else {"message": {"content": str(choice)}}
                                for choice in response.choices
                            ]
            
            memories = await self._extraction.extract(messages, response)
            if memories:
                await self._storage.store_memories(memories)
                await self._storage.store_conversation(messages, response_dict, memories)
                
                # Update graph if enabled
                if self._graph and self.config.graph.enabled:
                    await self._graph.update_graph(memories)
        except Exception as e:
            logger.error(f"Failed to store conversation (async): {e}")

    # Public API methods
    async def add_memory(self, content: str, memory_type: str = "fact", **metadata):
        """
        Manually add a memory.
        
        Args:
            content: Memory content
            memory_type: Type of memory (fact, preference, skill, etc.)
            **metadata: Additional metadata
        """
        if not self._storage:
            logger.warning("Storage not initialized")
            return

        try:
            memory = {
                "content": content,
                "type": memory_type,
                "metadata": metadata,
            }
            await self._storage.store_memories([memory])
            logger.debug(f"Added memory: {content}")
        except Exception as e:
            logger.error(f"Failed to add memory: {e}")

    async def search_memories(
        self, query: str, limit: int = 10, memory_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search memories by query.
        
        Args:
            query: Search query
            limit: Maximum number of results
            memory_type: Filter by memory type (optional)
            
        Returns:
            List of matching memories
        """
        if not self._retrieval:
            return []

        try:
            return await self._retrieval.search(query, limit=limit, memory_type=memory_type)
        except Exception as e:
            logger.error(f"Failed to search memories: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """Get memory engine statistics."""
        stats = {
            "enabled": self._enabled,
            "mode": self.config.memory.mode,
            "graph_enabled": self.config.graph.enabled,
        }
        
        if self._storage:
            try:
                storage_stats = self._storage.get_stats()
                stats.update(storage_stats)
            except Exception:
                pass
        
        if self._graph:
            try:
                graph_stats = self._graph.get_graph_stats()
                stats["graph"] = graph_stats
            except Exception:
                pass
        
        return stats
