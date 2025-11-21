"""
Graph Mode Example

Demonstrates graph-based memory for multi-hop reasoning.
"""

from memorable import MemoryEngine
from openai import OpenAI

# Initialize with graph enabled
memory = MemoryEngine(
    database="sqlite:///graph_example.db",
    graph_enabled=True,
    mode="auto"
)
memory.enable()

client = OpenAI()

# Build knowledge graph through conversations
conversations = [
    "I'm a software engineer",
    "I work at Google",
    "I use Python for my projects",
    "Python is great for FastAPI",
    "I'm building a FastAPI API"
]

for conv in conversations:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": conv}]
    )
    print(f"User: {conv}")
    print(f"Assistant: {response.choices[0].message.content}\n")

# Now ask a multi-hop question
# The graph will traverse: User -> works at -> Google -> uses -> Python -> FastAPI
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What frameworks do I use at work?"}]
)
print("Multi-hop question answered using graph traversal!")
print(response.choices[0].message.content)

