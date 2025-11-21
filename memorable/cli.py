"""
Command-line interface for Memorable.
"""

import argparse
import asyncio
import sys
from typing import Optional
from memorable import MemoryEngine, MemorableConfig


async def cmd_add_memory(args):
    """Add a memory via CLI."""
    memory = MemoryEngine(database=args.database, mode=args.mode)
    memory.enable()
    
    await memory.add_memory(
        content=args.content,
        memory_type=args.type,
    )
    print(f"✓ Added memory: {args.content}")


async def cmd_search(args):
    """Search memories via CLI."""
    memory = MemoryEngine(database=args.database, mode=args.mode)
    memory.enable()
    
    results = await memory.search_memories(args.query, limit=args.limit)
    
    if not results:
        print("No memories found.")
        return
    
    print(f"\nFound {len(results)} memories:\n")
    for i, mem in enumerate(results, 1):
        print(f"{i}. [{mem.get('type', 'fact')}] {mem.get('content', '')}")


async def cmd_stats(args):
    """Show statistics."""
    memory = MemoryEngine(database=args.database, mode=args.mode)
    memory.enable()
    
    stats = memory.get_stats()
    print("\nMemory Engine Statistics:")
    print(f"  Enabled: {stats.get('enabled', False)}")
    print(f"  Mode: {stats.get('mode', 'unknown')}")
    print(f"  Graph Enabled: {stats.get('graph_enabled', False)}")
    print(f"  Total Memories: {stats.get('total_memories', 0)}")
    print(f"  Namespace Memories: {stats.get('namespace_memories', 0)}")
    
    if "graph" in stats:
        graph = stats["graph"]
        print(f"\nGraph Statistics:")
        print(f"  Nodes: {graph.get('nodes', 0)}")
        print(f"  Edges: {graph.get('edges', 0)}")
        print(f"  Entity Nodes: {graph.get('entity_nodes', 0)}")
        print(f"  Memory Nodes: {graph.get('memory_nodes', 0)}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Memorable - Advanced Memory Engine for LLMs"
    )
    parser.add_argument(
        "--database",
        default="sqlite:///memorable.db",
        help="Database connection string"
    )
    parser.add_argument(
        "--mode",
        default="auto",
        choices=["conscious", "auto", "hybrid"],
        help="Memory mode"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Add memory command
    add_parser = subparsers.add_parser("add", help="Add a memory")
    add_parser.add_argument("content", help="Memory content")
    add_parser.add_argument(
        "--type",
        default="fact",
        choices=["fact", "preference", "skill", "rule", "context"],
        help="Memory type"
    )

    # Search command
    search_parser = subparsers.add_parser("search", help="Search memories")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum results"
    )

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show statistics")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Run command
    if args.command == "add":
        asyncio.run(cmd_add_memory(args))
    elif args.command == "search":
        asyncio.run(cmd_search(args))
    elif args.command == "stats":
        asyncio.run(cmd_stats(args))


if __name__ == "__main__":
    main()

