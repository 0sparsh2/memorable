"""
Consolidation Example

Demonstrates memory consolidation and importance scoring.
"""

import asyncio
from memorable import MemoryEngine

async def main():
    # Initialize with consolidation
    memory = MemoryEngine(
        database="sqlite:///consolidation_example.db",
        mode="auto"
    )
    memory.enable()

    # Add memories with different importance
    await memory.add_memory("User likes Python", "preference", importance_score=0.8)
    await memory.add_memory("User dislikes JavaScript", "preference", importance_score=0.6)
    await memory.add_memory("User works at Google", "fact", importance_score=0.9)

    # Manually trigger consolidation (normally runs every 6 hours)
    if memory._consolidator:
        print("Running consolidation...")
        await memory._consolidator.consolidate()
        print("Consolidation complete!")

    # Check updated importance scores
    memories = await memory._storage.get_memories(limit=10)
    print("\nMemories with importance scores:")
    for mem in memories:
        print(f"- [{mem.get('type')}] {mem.get('content')}: {mem.get('importance_score', 0):.2f}")

if __name__ == "__main__":
    asyncio.run(main())

