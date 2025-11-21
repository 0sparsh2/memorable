# Changelog

All notable changes to Memorable will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-XX

### Added
- Initial release of Memorable
- Interceptor-based architecture for transparent LLM call interception
- SQL-first storage layer (PostgreSQL, SQLite, MySQL support)
- Memory extraction from conversations (facts, preferences, skills, rules, context)
- Hybrid retrieval system (semantic + keyword + graph search)
- Graph-based memory for multi-hop reasoning (optional)
- Three memory modes: Conscious, Auto, and Hybrid
- Memory consolidation background agent
- Temporal memory tracking and coherence
- Framework integrations: OpenAI, Anthropic, LiteLLM, LangChain, AutoGen
- Comprehensive test suite (unit and integration tests)
- Benchmark implementations (LOCOMO, multi-hop, temporal)
- Complete documentation (README, architecture, API, benchmarks)

### References
- Memori: https://github.com/GibsonAI/Memori (interceptor architecture)
- Mem0: https://github.com/mem0ai/mem0 (research-backed techniques)
- Supermemory: https://github.com/supermemoryai/supermemory (graph architecture)

