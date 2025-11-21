# Memorable Features

## Core Features

### 1. Zero-Code Integration
- **Interceptor-based architecture** - Transparently intercepts LLM calls
- **No code changes required** - Existing code works unchanged
- **Automatic context injection** - Memories injected before LLM calls
- **Automatic memory extraction** - Memories extracted after LLM calls

### 2. SQL-First Storage
- **Multiple database support** - PostgreSQL, SQLite, MySQL, Neon, Supabase
- **Full-text search** - Fast keyword-based retrieval
- **Multi-tenant support** - Namespace isolation
- **Scalable** - Handles thousands of memories efficiently

### 3. Hybrid Retrieval
- **Semantic search** - Vector embeddings for meaning-based retrieval
- **Keyword search** - Full-text search for exact matches
- **Graph traversal** - Relationship-based retrieval (optional)
- **Intelligent ranking** - Combines multiple signals

### 4. Graph Support (Optional)
- **Auto-extract relationships** - Builds knowledge graph automatically
- **Multi-hop reasoning** - Traverse relationships across memories
- **Entity extraction** - Identifies entities and connections
- **NetworkX backend** - Can be extended to Neo4j

### 5. Memory Modes
- **Conscious Mode** - One-shot working memory (fast)
- **Auto Mode** - Dynamic per-query retrieval (accurate)
- **Hybrid Mode** - Combines both approaches (best)

### 6. Advanced Memory Management
- **Memory consolidation** - Background agent promotes important memories
- **Contradiction detection** - Identifies and resolves conflicts
- **Importance scoring** - Tracks memory importance over time
- **Temporal tracking** - Time-stamped memories and sequences

### 7. Framework Integrations
- **OpenAI** - Native support
- **Anthropic** - Native support
- **LiteLLM** - 100+ models supported
- **LangChain** - Callback integration
- **AutoGen** - Multi-agent support

## Advanced Features

### Memory Extraction
- Extracts facts, preferences, skills, rules, and context
- Pattern-based extraction (fast)
- LLM-based extraction (accurate, optional)
- Automatic embedding generation

### Memory Consolidation
- Background agent runs every 6 hours (configurable)
- Updates importance scores based on access patterns
- Detects and resolves contradictions
- Promotes important memories

### Temporal Memory
- Time-stamped memories
- Before/after relationships
- Event sequences
- Temporal coherence checking

### Performance
- <100ms retrieval latency (target)
- 50%+ token savings vs full-context (target)
- Efficient caching
- Optimized queries

## Developer Experience

### CLI Tool
```bash
memorable add "User likes Python" --type preference
memorable search "Python" --limit 10
memorable stats
```

### Configuration
- Environment variables
- Programmatic configuration
- Default values for quick start

### Testing
- Comprehensive unit tests
- Integration tests
- Benchmark tests
- >80% coverage target

### Documentation
- Complete API documentation
- Architecture documentation
- Benchmark reports
- Examples and tutorials

## Comparison with Other Systems

| Feature | Memorable | Memori | Mem0 | Supermemory |
|---------|-----------|--------|------|-------------|
| **Integration** | Interceptor | Interceptor | API | API |
| **Graph** | ✅ Optional | ❌ | ❌ | ✅ |
| **Research** | ✅ Planned | ❌ | ✅ | ❌ |
| **Modes** | 3 | 3 | 1 | 1 |
| **SQL DB** | ✅ Any | ✅ Any | ⚠️ Limited | ⚠️ Limited |
| **Multi-hop** | ✅ | ❌ | ❌ | ✅ |
| **Temporal** | ✅ | ❌ | ❌ | ❌ |
| **Consolidation** | ✅ | ❌ | ✅ | ❌ |

## Use Cases

1. **Personal Assistants** - Remember user preferences and context
2. **Customer Support** - Maintain conversation history
3. **Multi-Agent Systems** - Shared memory across agents
4. **Research Tools** - Long-term knowledge retention
5. **Enterprise Applications** - Multi-tenant memory isolation

## References

- Memori: https://github.com/GibsonAI/Memori
- Mem0: https://github.com/mem0ai/mem0
- Supermemory: https://github.com/supermemoryai/supermemory

