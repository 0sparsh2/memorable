# Quick Start Guide

Get up and running with Memorable in 5 minutes!

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

Or for development:

```bash
pip install -e ".[dev]"
```

## Basic Usage (30 seconds)

```python
from memorable import MemoryEngine
from openai import OpenAI

# 1. Initialize and enable (that's it!)
memory = MemoryEngine(database="sqlite:///memory.db", mode="auto")
memory.enable()

# 2. Your existing code works unchanged!
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "I'm building a FastAPI project"}]
)

# 3. Later conversation - memories automatically injected!
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Help me add authentication"}]
# LLM automatically knows about your FastAPI project!
```

## With Graph Support (1 minute)

```python
from memorable import MemoryEngine

memory = MemoryEngine(
    database="sqlite:///memory.db",
    graph_enabled=True,  # Enable graph for multi-hop reasoning
    mode="hybrid"        # Best accuracy
)
memory.enable()

# Now supports multi-hop reasoning through relationships!
```

## With PostgreSQL (1 minute)

```python
from memorable import MemoryEngine

memory = MemoryEngine(
    database="postgresql://user:pass@localhost/memorable",
    mode="auto"
)
memory.enable()
```

## Environment Variables

```bash
export MEMORABLE_DATABASE__CONNECTION_STRING="postgresql://..."
export MEMORABLE_MEMORY__MODE="auto"
export MEMORABLE_GRAPH__ENABLED="true"
export OPENAI_API_KEY="sk-your-key-here"
```

```python
from memorable import MemoryEngine, MemorableConfig

config = MemorableConfig.from_env()
memory = MemoryEngine(config=config)
memory.enable()
```

## Testing

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test
pytest tests/unit/test_storage.py -v
```

## Examples

See `examples/` directory:
- `basic_usage.py` - Simple example
- `multi_agent.py` - Multi-agent systems
- `graph_mode.py` - Graph-based memory
- `enterprise.py` - Enterprise configuration

## Next Steps

1. Read [README.md](README.md) for full documentation
2. Check [docs/architecture.md](docs/architecture.md) for system design
3. See [docs/api.md](docs/api.md) for API reference
4. Review [ROADMAP.md](ROADMAP.md) for future features

## Need Help?

- Check documentation in `docs/`
- Review examples in `examples/`
- See tests in `tests/` for usage patterns

