"""
Basic Usage Example

Demonstrates the easiest way to use Memorable - zero-code integration.

Inspired by Memori's simple integration approach.
"""

from memorable import MemoryEngine
from openai import OpenAI

# Initialize Memory Engine
memory = MemoryEngine(
    database="sqlite:///example.db",  # Use SQLite for simplicity
    mode="auto"  # Auto mode for dynamic retrieval
)

# Enable memory - that's it!
memory.enable()

# Your existing code works unchanged
client = OpenAI()

# First conversation
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "I'm building a FastAPI project"}]
)
print(response.choices[0].message.content)

# Later conversation - Memorable automatically provides context
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Help me add authentication"}]
)
# LLM automatically knows about your FastAPI project!
print(response.choices[0].message.content)

