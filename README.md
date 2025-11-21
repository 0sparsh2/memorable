# Memorable

<div align="center">

**The First Unified Memory System Combining Interceptor-Based Integration, Research-Backed Techniques, and Graph Architecture**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

*Zero-code integration • Research-validated • Production-ready*

[Quick Start](#quick-start) • [Documentation](docs/) • [Examples](examples/) • [Contributing](CONTRIBUTING.md)

</div>

---

## What is Memorable?

Memorable is the first memory system that combines the best of three leading approaches:

- **Memori's** zero-code interceptor architecture for seamless integration
- **Mem0's** research-validated memory techniques from academic papers
- **Supermemory's** graph-based architecture for multi-hop reasoning

**Result**: A production-ready memory system that requires no code changes, works with any SQL database, supports 100+ LLM models, and includes optional graph capabilities.

## Why Memorable?

| Feature | Memorable | Memori | Mem0 | Supermemory |
|---------|-----------|--------|------|-------------|
| **Zero-Code Integration** | ✅ Interceptor | ✅ Interceptor | ❌ API calls | ❌ API calls |
| **Research-Backed** | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| **Graph Support** | ✅ Optional | ❌ No | ❌ No | ✅ Required |
| **SQL Database** | ✅ Any SQL | ✅ Any SQL | ⚠️ Limited | ⚠️ Limited |
| **Multi-Model** | ✅ 100+ models | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited |
| **Memory Modes** | ✅ 3 modes | ✅ 3 modes | ⚠️ 1 mode | ⚠️ 1 mode |
| **Production-Ready** | ✅ Yes | ✅ Yes | ⚠️ Partial | ⚠️ Partial |

## Quick Start

### Installation

```bash
pip install memorable
```

### 30-Second Example

```python
from memorable import MemoryEngine
from openai import OpenAI

# Initialize and enable (that's it!)
memory = MemoryEngine(database="sqlite:///memory.db", mode="auto")
memory.enable()

# Your existing code works unchanged!
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "I'm building a FastAPI project"}]
)

# Later conversation - memories automatically injected!
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Help me add authentication"}]
# ✨ LLM automatically knows about your FastAPI project!
```

**That's it!** Memorable automatically:
- ✅ Injects relevant memories as context before each LLM call
- ✅ Extracts and stores new memories after each conversation
- ✅ Maintains conversation history
- ✅ Consolidates important memories in the background

## Key Features

### 🚀 Zero-Code Integration
Transparently intercepts LLM calls - no code changes required. Works with OpenAI, Anthropic, LiteLLM, and more.

### 🧠 Research-Backed
Uses validated techniques from Mem0's research paper (arXiv:2504.19413) for memory extraction, retrieval, and consolidation.

### 🕸️ Optional Graph Support
Enable graph-based memory for multi-hop reasoning. Works with NetworkX (default) or Neo4j.

### 🔍 Hybrid Retrieval
Combines semantic search (embeddings), keyword search (full-text), and graph traversal for optimal results.

### 🎯 Multiple Memory Modes
- **Auto Mode**: Dynamic per-query retrieval (default, best accuracy)
- **Conscious Mode**: One-shot working memory (fastest)
- **Hybrid Mode**: Combines both approaches (best of both worlds)

### 💾 SQL-First Storage
Works with PostgreSQL, SQLite, MySQL, Neon, Supabase - any SQL database you already use.

### 🌐 Multi-Model Support
Works with 100+ models via LiteLLM: OpenAI, Anthropic, Gemini, Llama, Mistral, and more.

## Installation

### From PyPI (Recommended)

```bash
pip install memorable
```

### From Source

```bash
git clone https://github.com/yourusername/memorable.git
cd memorable
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Usage Examples

### Basic Usage (OpenAI)

```python
from memorable import MemoryEngine
from openai import OpenAI

memory = MemoryEngine(database="sqlite:///memory.db", mode="auto")
memory.enable()

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What do I like?"}]
)
```

### With Anthropic Claude

```python
from memorable import MemoryEngine
from anthropic import Anthropic

memory = MemoryEngine(database="sqlite:///memory.db")
memory.enable()

client = Anthropic()
response = client.messages.create(
    model="claude-3-opus",
    messages=[{"role": "user", "content": "Tell me about myself"}]
)
```

### With Gemini via LiteLLM

```python
from memorable import MemoryEngine
import litellm

memory = MemoryEngine(database="sqlite:///memory.db")
memory.enable()

response = litellm.completion(
    model="gemini/gemini-2.5-flash",
    messages=[{"role": "user", "content": "describe me"}]
)
```

### With Graph Support

```python
from memorable import MemoryEngine

memory = MemoryEngine(
    database="postgresql://user:pass@localhost/memorable",
    graph_enabled=True,  # Enable graph for multi-hop reasoning
    mode="hybrid"
)
memory.enable()

# Now supports relationship traversal and multi-hop queries!
```

### Manual Memory Management

```python
import asyncio
from memorable import MemoryEngine

memory = MemoryEngine(database="sqlite:///memory.db")
memory.enable()

async def manage_memories():
    # Add memory manually
    await memory.add_memory(
        content="User prefers Python over JavaScript",
        memory_type="preference"
    )
    
    # Search memories
    results = await memory.search_memories("Python", limit=10)
    for mem in results:
        print(f"{mem['type']}: {mem['content']}")
    
    # Get statistics
    stats = memory.get_stats()
    print(f"Total memories: {stats['total_memories']}")

asyncio.run(manage_memories())
```

## Architecture

Memorable uses an interceptor-based architecture that transparently:

```
┌─────────────────────────────────────────────────────────┐
│                    Your Application                      │
│  (OpenAI, Anthropic, LiteLLM calls - unchanged code)     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Memorable Interceptor                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Pre-call:   │  │  LLM Call    │  │  Post-call:  │  │
│  │  Inject      │→ │  (original)  │→ │  Extract &   │  │
│  │  Context     │  │              │  │  Store       │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Memory Engine                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Storage  │  │Retrieval │  │Extraction│  │  Graph   │ │
│  │  (SQL)   │  │ (Hybrid) │  │ (Pattern)│  │(Optional)│ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Memory Hierarchy

- **Working Memory**: Immediate context (current conversation)
- **Short-term Memory**: Recent conversations (6 hours)
- **Long-term Memory**: Consolidated facts, preferences, skills
- **Episodic Memory**: Temporal sequences and events (with graph)

## Configuration

### Environment Variables

```bash
# Database
export MEMORABLE_DATABASE__CONNECTION_STRING="postgresql://user:pass@localhost/memorable"

# Memory Settings
export MEMORABLE_MEMORY__MODE="auto"  # conscious, auto, or hybrid
export MEMORABLE_MEMORY__NAMESPACE="production"
export MEMORABLE_MEMORY__MAX_CONTEXT_TOKENS="2000"

# Graph (Optional)
export MEMORABLE_GRAPH__ENABLED="true"
export MEMORABLE_GRAPH__CONNECTION_STRING="neo4j://localhost:7687"

# LLM API Keys
export OPENAI_API_KEY="sk-your-key-here"
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
export GEMINI_API_KEY="your-key-here"
```

### Programmatic Configuration

```python
from memorable import MemoryEngine, MemorableConfig

config = MemorableConfig.from_env()
memory = MemoryEngine(config=config)
memory.enable()
```

See [docs/api.md](docs/api.md) for complete configuration options.

## Database Support

Memorable works with any SQL database:

| Database | Connection String Example |
|----------|--------------------------|
| **SQLite** | `sqlite:///memory.db` |
| **PostgreSQL** | `postgresql://user:pass@localhost/memorable` |
| **MySQL** | `mysql://user:pass@localhost/memorable` |
| **Neon** | `postgresql://user:pass@ep-*.neon.tech/memorable` |
| **Supabase** | `postgresql://postgres:pass@db.*.supabase.co/postgres` |

## Memory Modes

### Auto Mode (Default)
Dynamic per-query retrieval - best for most use cases.

```python
memory = MemoryEngine(mode="auto")
```

### Conscious Mode
One-shot working memory injection - faster, good for simple conversations.

```python
memory = MemoryEngine(mode="conscious")
```

### Hybrid Mode
Combines both approaches - best accuracy, slightly slower.

```python
memory = MemoryEngine(mode="hybrid")
```

## Benchmarks

Memorable is designed to outperform existing systems:

- **30%+ improvement** over Mem0 on LOCOMO benchmark (target)
- **95%+ accuracy** on multi-hop reasoning (target)
- **<100ms** retrieval latency (target)
- **50%+ token savings** vs full-context (target)

*Benchmark results will be published in upcoming releases. See [docs/benchmarks.md](docs/benchmarks.md) for methodology.*

## Comparison with Other Systems

| Feature | Memorable | Memori | Mem0 | Supermemory |
|---------|-----------|--------|------|-------------|
| **Easy Integration** | ✅ Interceptor | ✅ Interceptor | ⚠️ API calls | ⚠️ API calls |
| **Research-Backed** | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| **Graph Support** | ✅ Optional | ❌ No | ❌ No | ✅ Required |
| **SQL Database** | ✅ Any SQL | ✅ Any SQL | ⚠️ Limited | ⚠️ Limited |
| **Multi-hop** | ✅ Yes | ❌ No | ⚠️ Limited | ✅ Yes |
| **Memory Modes** | ✅ 3 modes | ✅ 3 modes | ⚠️ 1 mode | ⚠️ 1 mode |
| **Temporal Memory** | ✅ Yes | ❌ No | ⚠️ Limited | ❌ No |
| **Consolidation** | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| **Multi-Model** | ✅ 100+ | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited |

## Research & Citations

### Research Papers

1. **Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory**
   - arXiv:2504.19413 (April 2025)
   - https://arxiv.org/abs/2504.19413
   - *Reference for memory extraction, retrieval, and consolidation techniques*

2. **Highly engaging events reveal semantic and temporal compression in online community discourse**
   - PNAS Nexus (March 2025)
   - *Reference for temporal memory and discourse analysis*

3. **XMem: Long-Term Video Object Segmentation with an Atkinson-Shiffrin Memory Model**
   - arXiv:2207.07115 (July 2022)
   - https://arxiv.org/abs/2207.07115
   - *Reference for memory hierarchy models*

4. **Abstractive Summarization of Reddit Posts with Multi-level Memory Networks**
   - ACL (2019)
   - *Reference for multi-level memory architectures*

### Open Source Repositories

1. **Memori (GibsonAI/Memori)**
   - https://github.com/GibsonAI/Memori
   - License: Apache 2.0
   - *Reference for interceptor-based architecture and SQL storage*

2. **Mem0 (mem0ai/mem0)**
   - https://github.com/mem0ai/mem0
   - *Reference for research-backed memory techniques and LOCOMO benchmark*

3. **Supermemory (supermemoryai/supermemory)**
   - https://github.com/supermemoryai/supermemory
   - License: MIT
   - *Reference for knowledge graph architecture*

See [docs/research.md](docs/research.md) for detailed research approach and methodology.

## Documentation

- **[Architecture](docs/architecture.md)** - System design and components
- **[API Reference](docs/api.md)** - Complete API documentation
- **[Benchmarks](docs/benchmarks.md)** - Performance metrics and methodology
- **[Research](docs/research.md)** - Research approach and unique features
- **[Examples](examples/)** - Real-world usage examples

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/memorable.git
cd memorable

# Install in development mode
pip install -e ".[dev]"

# Run tests
make test

# Run with coverage
make test-cov
```

## Roadmap

- [ ] Complete framework integrations (LangChain, AutoGen, CrewAI)
- [ ] Publish benchmark results
- [ ] Research paper publication
- [ ] Enterprise features (admin dashboard, audit logs)
- [ ] Multi-modal support (images, video, audio)
- [ ] Advanced graph features (Neo4j integration)
- [ ] Performance optimizations
- [ ] Additional LLM provider integrations

See [ROADMAP.md](ROADMAP.md) for detailed plans.

## License

Apache 2.0 - see [LICENSE](LICENSE) file.

## Acknowledgments

Memorable is built on the excellent work of:

- **Memori** team for the interceptor architecture
- **Mem0** team for research-backed techniques
- **Supermemory** team for graph architecture inspiration

## Support

- **Documentation**: [docs/](docs/)
- **Issues**: https://github.com/yourusername/memorable/issues
- **Discussions**: https://github.com/yourusername/memorable/discussions

---

<div align="center">

**Memorable** - The easiest, most efficient memory system for AI applications.

[⭐ Star us on GitHub](https://github.com/yourusername/memorable) • [📖 Read the Docs](docs/) • [💬 Join Discussions](https://github.com/yourusername/memorable/discussions)

</div>
