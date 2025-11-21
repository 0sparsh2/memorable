"""
Advanced Configuration Example

Demonstrates advanced configuration options.
"""

import os
from memorable import MemoryEngine, MemorableConfig, DatabaseConfig, GraphConfig, MemoryConfig, LLMConfig

# Build configuration programmatically
config = MemorableConfig(
    database=DatabaseConfig(
        connection_string="postgresql://user:pass@localhost/memorable",
        pool_size=10,
        max_overflow=20
    ),
    graph=GraphConfig(
        enabled=True,
        connection_string="neo4j://localhost:7687"  # Optional Neo4j
    ),
    memory=MemoryConfig(
        mode="hybrid",
        namespace="production",
        max_context_tokens=4000,
        consolidation_interval=21600  # 6 hours
    ),
    llm=LLMConfig(
        # API keys should be set via environment variables for security
        # openai_api_key=os.getenv("OPENAI_API_KEY"),
        default_model="gpt-4o",
        embedding_model="sentence-transformers/all-mpnet-base-v2"
    )
)

# Initialize with advanced config
memory = MemoryEngine(config=config)
memory.enable()

# Or use environment variables
# export MEMORABLE_DATABASE__CONNECTION_STRING=postgresql://...
# export MEMORABLE_GRAPH__ENABLED=true
# export MEMORABLE_MEMORY__MODE=hybrid

config_from_env = MemorableConfig.from_env()
memory2 = MemoryEngine(config=config_from_env)

