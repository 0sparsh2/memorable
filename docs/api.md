# Memorable API Documentation

## Core API

### MemoryEngine

Main entry point for Memorable.

#### `MemoryEngine(database, graph_enabled=False, graph_database=None, mode="auto", config=None, **kwargs)`

Initialize memory engine.

**Parameters:**
- `database` (str, optional): Database connection string
- `graph_enabled` (bool): Enable graph-based memory (default: False)
- `graph_database` (str, optional): Graph database connection string
- `mode` (str): Memory mode - "conscious", "auto", or "hybrid" (default: "auto")
- `config` (MemorableConfig, optional): Configuration object
- `**kwargs`: Additional configuration options

**Example:**
```python
from memorable import MemoryEngine

memory = MemoryEngine(
    database="postgresql://user:pass@localhost/memorable",
    mode="auto"
)
```

#### `enable()`

Enable memory engine - starts intercepting LLM calls.

**Example:**
```python
memory.enable()
```

#### `disable()`

Disable memory engine - stops intercepting LLM calls.

#### `add_memory(content, memory_type="fact", **metadata)`

Manually add a memory.

**Parameters:**
- `content` (str): Memory content
- `memory_type` (str): Type of memory (fact, preference, skill, rule, context)
- `**metadata`: Additional metadata

**Example:**
```python
await memory.add_memory(
    content="User prefers Python over JavaScript",
    memory_type="preference",
    source="manual"
)
```

#### `search_memories(query, limit=10, memory_type=None)`

Search memories by query.

**Parameters:**
- `query` (str): Search query
- `limit` (int): Maximum number of results (default: 10)
- `memory_type` (str, optional): Filter by memory type

**Returns:**
- `List[Dict[str, Any]]`: List of matching memories

**Example:**
```python
results = await memory.search_memories("Python", limit=10)
```

#### `get_stats()`

Get memory engine statistics.

**Returns:**
- `Dict[str, Any]`: Statistics dictionary

## Storage API

### Storage

SQL storage layer.

#### `Storage(connection_string, namespace=None)`

Initialize storage.

**Parameters:**
- `connection_string` (str): Database connection string
- `namespace` (str, optional): Namespace for multi-tenant support

#### `store_memories(memories)`

Store memories in database.

**Parameters:**
- `memories` (List[Dict[str, Any]]): List of memory dictionaries

#### `get_memories(memory_type=None, limit=100, offset=0)`

Get memories from database.

**Parameters:**
- `memory_type` (str, optional): Filter by memory type
- `limit` (int): Maximum results (default: 100)
- `offset` (int): Offset for pagination (default: 0)

**Returns:**
- `List[Dict[str, Any]]`: List of memories

#### `search_memories_text(query, limit=10, memory_type=None)`

Full-text search for memories.

**Parameters:**
- `query` (str): Search query
- `limit` (int): Maximum results (default: 10)
- `memory_type` (str, optional): Filter by memory type

**Returns:**
- `List[Dict[str, Any]]`: List of matching memories

## Retrieval API

### HybridRetriever

Hybrid retrieval system.

#### `HybridRetriever(storage, embedding_model="sentence-transformers/all-MiniLM-L6-v2", graph=None)`

Initialize retriever.

**Parameters:**
- `storage`: Storage instance
- `embedding_model` (str): Embedding model name
- `graph`: Optional graph instance

#### `retrieve(messages, limit=10)`

Retrieve relevant memories for conversation.

**Parameters:**
- `messages` (List[Dict[str, Any]]): Conversation messages
- `limit` (int): Maximum results (default: 10)

**Returns:**
- `List[Dict[str, Any]]`: List of relevant memories

#### `search(query, limit=10, memory_type=None)`

Search memories by query.

**Parameters:**
- `query` (str): Search query
- `limit` (int): Maximum results (default: 10)
- `memory_type` (str, optional): Filter by memory type

**Returns:**
- `List[Dict[str, Any]]`: List of matching memories

## Configuration API

### MemorableConfig

Configuration management.

#### `MemorableConfig.from_env()`

Load configuration from environment variables.

**Environment Variables:**
- `MEMORABLE_DATABASE__CONNECTION_STRING`: Database connection string
- `MEMORABLE_GRAPH__ENABLED`: Enable graph (true/false)
- `MEMORABLE_GRAPH__CONNECTION_STRING`: Graph database connection
- `MEMORABLE_MEMORY__MODE`: Memory mode (conscious/auto/hybrid)
- `MEMORABLE_MEMORY__NAMESPACE`: Namespace for multi-tenant
- `MEMORABLE_MEMORY__MAX_CONTEXT_TOKENS`: Max tokens for context
- `MEMORABLE_LLM__OPENAI_API_KEY`: OpenAI API key
- `MEMORABLE_LLM__ANTHROPIC_API_KEY`: Anthropic API key
- `MEMORABLE_LLM__DEFAULT_MODEL`: Default LLM model
- `MEMORABLE_LLM__EMBEDDING_MODEL`: Embedding model

**Example:**
```python
from memorable import MemorableConfig

config = MemorableConfig.from_env()
memory = MemoryEngine(config=config)
```

## Temporal Memory API

### TemporalMemory

Temporal memory tracking.

#### `add_temporal_memory(content, memory_type="fact", timestamp=None, before=None, after=None, **metadata)`

Add memory with temporal information.

**Parameters:**
- `content` (str): Memory content
- `memory_type` (str): Type of memory
- `timestamp` (datetime, optional): When memory occurred
- `before` (List[int], optional): IDs of memories before this
- `after` (List[int], optional): IDs of memories after this
- `**metadata`: Additional metadata

#### `get_temporal_sequence(start_memory_id, direction="forward", limit=10)`

Get temporal sequence of memories.

**Parameters:**
- `start_memory_id` (int): Starting memory ID
- `direction` (str): "forward" or "backward"
- `limit` (int): Maximum results

**Returns:**
- `List[Dict[str, Any]]`: List of memories in temporal order

#### `get_memories_by_time_range(start_time, end_time, memory_type=None)`

Get memories within a time range.

**Parameters:**
- `start_time` (datetime): Start of time range
- `end_time` (datetime): End of time range
- `memory_type` (str, optional): Filter by memory type

**Returns:**
- `List[Dict[str, Any]]`: List of memories in time range

## Graph API

### GraphBuilder

Knowledge graph builder.

#### `GraphBuilder(connection_string=None)`

Initialize graph builder.

**Parameters:**
- `connection_string` (str, optional): Graph database connection

#### `update_graph(memories)`

Update graph with new memories.

**Parameters:**
- `memories` (List[Dict[str, Any]]): List of memories

#### `find_related(query, limit=10)`

Find related memories using graph traversal.

**Parameters:**
- `query` (str): Search query
- `limit` (int): Maximum results

**Returns:**
- `List[Dict[str, Any]]`: List of related memories

## References

- Full source code: https://github.com/yourusername/memorable
- Architecture documentation: [architecture.md](architecture.md)

