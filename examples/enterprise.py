"""
Enterprise Example

Demonstrates enterprise features like namespaces and multi-user support.
"""

from memorable import MemoryEngine, MemorableConfig
from openai import OpenAI

# Enterprise configuration
config = MemorableConfig(
    database=MemorableConfig.DatabaseConfig(
        connection_string="postgresql://user:pass@localhost/memorable",
        pool_size=10,
        max_overflow=20
    ),
    memory=MemorableConfig.MemoryConfig(
        mode="hybrid",
        namespace="production",  # Multi-tenant support
        max_context_tokens=4000,
        consolidation_interval=21600  # 6 hours
    )
)

# Initialize with enterprise config
memory = MemoryEngine(config=config)
memory.enable()

client = OpenAI()

# User 1 conversation (isolated by namespace)
memory.config.memory.namespace = "user_1"
response1 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "I prefer Python"}]
)

# User 2 conversation (isolated by namespace)
memory.config.memory.namespace = "user_2"
response2 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "I prefer JavaScript"}]
)

# Memories are isolated per namespace
print("User 1 memories:", await memory.search_memories("Python"))
print("User 2 memories:", await memory.search_memories("JavaScript"))

