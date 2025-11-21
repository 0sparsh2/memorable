"""
Multi-Agent Example

Demonstrates Memorable with multi-agent systems.
"""

from memorable import MemoryEngine
from openai import OpenAI

# Initialize with shared memory
memory = MemoryEngine(
    database="sqlite:///multi_agent.db",
    mode="hybrid",  # Hybrid mode for best results
    graph_enabled=True  # Enable graph for relationship tracking
)
memory.enable()

client = OpenAI()

# Agent 1: Project Manager
def project_manager_agent():
    """Agent that manages project information."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a project manager."},
            {"role": "user", "content": "We're starting a new FastAPI project"}
        ]
    )
    return response.choices[0].message.content

# Agent 2: Developer
def developer_agent():
    """Agent that handles development tasks."""
    # This agent automatically has context from project_manager_agent
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a developer."},
            {"role": "user", "content": "What should I add first?"}
        ]
    )
    return response.choices[0].message.content

# Run agents - memories are shared automatically
print("Project Manager:", project_manager_agent())
print("\nDeveloper:", developer_agent())

