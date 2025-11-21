# Memorable Architecture

## Overview

Memorable uses an interceptor-based architecture that transparently enhances LLM calls with memory capabilities. The system combines SQL storage, optional graph-based relationships, and research-backed retrieval techniques.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Application                         │
│  client.chat.completions.create(...)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Memorable Interceptor                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Pre-call: Retrieve & Inject Context                │   │
│  └──────────────────────────────────────────────────────┘   │
│                       │                                      │
│                       ▼                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  LLM Provider (OpenAI, Anthropic, LiteLLM, etc.)     │   │
│  └──────────────────────────────────────────────────────┘   │
│                       │                                      │
│                       ▼                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Post-call: Extract & Store Memories                 │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Storage Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ SQL Storage  │  │ Graph (opt)  │  │  Retrieval   │      │
│  │ (PostgreSQL, │  │  (NetworkX/ │  │  (Hybrid)    │      │
│  │  SQLite, etc)│  │   Neo4j)    │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Interceptor (`core/interceptor.py`)

Transparently intercepts LLM calls to:
- **Pre-call**: Retrieve relevant memories and inject as context
- **Post-call**: Extract memories from conversation and store them

**Supported Providers:**
- OpenAI (native)
- Anthropic (native)
- LiteLLM (100+ models)

### 2. Storage (`core/storage.py`)

SQL-first storage with:
- **Memory Table**: Stores facts, preferences, skills, rules, context
- **Conversation Table**: Stores full conversation history
- **Indexes**: Full-text search, importance scoring, temporal queries

**Supported Databases:**
- PostgreSQL
- SQLite
- MySQL
- Neon
- Supabase

### 3. Extraction (`core/extraction.py`)

Extracts structured memories from conversations:
- **Facts**: "I work at Google"
- **Preferences**: "I like Python"
- **Skills**: "I can code in Python"
- **Rules**: "Always use type hints"
- **Context**: "Currently building FastAPI project"

### 4. Retrieval (`core/retrieval.py`)

Hybrid retrieval combining:
- **Semantic Search**: Vector embeddings for meaning-based retrieval
- **Keyword Search**: Full-text search for exact matches
- **Graph Traversal**: Relationship-based retrieval (if graph enabled)

### 5. Graph Builder (`graph/builder.py`)

Optional knowledge graph for:
- Entity extraction
- Relationship modeling
- Multi-hop reasoning
- Temporal sequences

### 6. Consolidation (`core/consolidation.py`)

Background agent that:
- Updates importance scores based on access patterns
- Detects and resolves contradictions
- Promotes important memories
- Removes outdated memories

### 7. Temporal Memory (`core/temporal.py`)

Tracks temporal relationships:
- Time-stamped memories
- Before/after relationships
- Event sequences
- Temporal coherence checking

## Memory Modes

### Auto Mode (Default)
- Dynamic per-query retrieval
- Best for most use cases
- Retrieves relevant memories for each query

### Conscious Mode
- One-shot working memory injection
- Faster, good for simple conversations
- Retrieves once per session

### Hybrid Mode
- Combines conscious and auto
- Best accuracy
- Session-level + query-level context

## Data Flow

1. **User makes LLM call** → Intercepted by Memorable
2. **Pre-call processing**:
   - Extract query from messages
   - Retrieve relevant memories (semantic + keyword + graph)
   - Inject as system message or prepend to conversation
3. **LLM call** → Original provider (OpenAI, Anthropic, etc.)
4. **Post-call processing**:
   - Extract memories from conversation
   - Store in SQL database
   - Update graph (if enabled)
5. **Background processing** (every 6 hours):
   - Consolidate memories
   - Update importance scores
   - Resolve contradictions

## References

- **Memori**: Interceptor architecture inspiration
- **Mem0**: Research-backed techniques (arXiv:2504.19413)
- **Supermemory**: Graph architecture inspiration

