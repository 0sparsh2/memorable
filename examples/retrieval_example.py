"""
Retrieval Example

Demonstrates different retrieval strategies.
"""

import asyncio
from memorable import MemoryEngine

async def main():
    # Initialize
    memory = MemoryEngine(
        database="sqlite:///retrieval_example.db",
        mode="auto"
    )
    memory.enable()

    # Add various memories
    await memory.add_memory("User likes Python programming", "preference")
    await memory.add_memory("User works at Google", "fact")
    await memory.add_memory("User can code in Python", "skill")
    await memory.add_memory("User is building a FastAPI project", "context")

    # Search by keyword
    print("=== Keyword Search ===")
    results = await memory.search_memories("Python", limit=5)
    for mem in results:
        print(f"- [{mem.get('type')}] {mem.get('content')}")

    # Search by type
    print("\n=== Search Preferences ===")
    preferences = await memory.search_memories("programming", memory_type="preference", limit=5)
    for pref in preferences:
        print(f"- {pref.get('content')}")

    # Get stats
    print("\n=== Statistics ===")
    stats = memory.get_stats()
    print(f"Total memories: {stats.get('total_memories', 0)}")
    print(f"Mode: {stats.get('mode')}")

if __name__ == "__main__":
    asyncio.run(main())

