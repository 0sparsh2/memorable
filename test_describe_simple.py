"""
Example: Using Memorable with Gemini to demonstrate context injection

This example shows how Memorable automatically injects stored memories
into LLM calls, enabling the model to provide personalized responses
based on previous conversations.

Prerequisites:
    - Set GEMINI_API_KEY environment variable
    - Have some memories stored in the database (or run test_memorable_final.py first)

Usage:
    export GEMINI_API_KEY='your-api-key-here'
    python test_describe_simple.py
"""

import os
from memorable import MemoryEngine
import litellm

# Configuration
# Get API key from environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("⚠️  GEMINI_API_KEY environment variable not set")
    print("   Please set it with: export GEMINI_API_KEY='your-api-key-here'")
    exit(1)

def main():
    """Test 'describe me' with Memorable enabled."""
    
    print("\n" + "=" * 70)
    print("  TEST: 'DESCRIBE ME' WITH MEMORABLE (gemini-2.5-flash)")
    print("=" * 70 + "\n")
    
    # Load existing database
    print("Step 1: Loading database with stored memories...")
    memory = MemoryEngine(
        database="sqlite:///test_memorable_lib.db",
        mode="auto"
    )
    
    stats = memory.get_stats()
    print(f"✓ Database loaded: {stats.get('total_memories', 0)} memories found\n")
    
    # Enable memory (this hooks the interceptor)
    print("Step 2: Enabling memory engine...")
    memory.enable()
    print("✓ Memory enabled - interceptor hooked\n")
    
    # Show what memories will be used
    print("Step 3: Stored memories that should be injected:")
    import asyncio
    async def show_memories():
        memories = await memory.search_memories("", limit=10)
        for i, mem in enumerate(memories, 1):
            print(f"  {i}. [{mem.get('type', 'unknown')}] {mem.get('content', '')}")
        return memories
    
    memories = asyncio.run(show_memories())
    print()
    
    # Make LLM call - the interceptor will inject context
    print("Step 4: Asking LLM to 'describe me'...")
    print("  (Memorable will automatically inject the memories above)\n")
    
    try:
        response = litellm.completion(
            model="gemini/gemini-2.5-flash",
            messages=[
                {"role": "user", "content": "describe me"}
            ],
            api_key=GEMINI_API_KEY
        )
        
        print("=" * 70)
        print("  LLM RESPONSE:")
        print("=" * 70)
        response_text = response.choices[0].message.content
        print(response_text)
        print("=" * 70 + "\n")
        
        # Check if response mentions stored memories
        memory_keywords = ["Python", "FastAPI", "engineer", "PostgreSQL", "TypeScript", "JavaScript"]
        found_keywords = [kw for kw in memory_keywords if kw.lower() in response_text.lower()]
        
        if found_keywords:
            print(f"✓ Response mentions stored memories: {', '.join(found_keywords)}")
            print("  ✓ Context injection appears to be working!\n")
        else:
            print("⚠️  Response doesn't mention stored memories")
            print("  This might be because:")
            print("    - Context injection couldn't run (async/sync issue)")
            print("    - LLM chose not to use the context")
            print("    - Need to check interceptor logs\n")
        
        # Check final stats
        stats_after = memory.get_stats()
        print(f"Final Statistics:")
        print(f"  Total Memories: {stats_after.get('total_memories', 0)}")
        print(f"  Total Conversations: {stats_after.get('total_conversations', 0)}")
        
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "rate limit" in error_msg.lower() or "quota" in error_msg.lower():
            print("⚠️  Rate limit reached (expected for free tier API keys)")
            print("   The interceptor attempted to inject context before the call")
            print("   This is an API quota issue, not a code issue\n")
        else:
            print(f"✗ Error: {error_msg[:300]}\n")
    
    # Cleanup
    memory.disable()
    print("\n✓ Test complete - memory engine disabled\n")


if __name__ == "__main__":
    main()

