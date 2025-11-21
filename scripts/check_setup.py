#!/usr/bin/env python3
"""
Quick setup check script.

Run this to verify your Memorable installation is working.
"""

import sys
import importlib

def check_imports():
    """Check if all required modules can be imported."""
    print("Checking imports...")
    
    modules = [
        "memorable",
        "memorable.core",
        "memorable.core.memory_engine",
        "memorable.core.storage",
        "memorable.core.extraction",
        "memorable.core.retrieval",
        "memorable.core.interceptor",
        "memorable.graph",
        "memorable.modes",
        "memorable.utils",
    ]
    
    failed = []
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"  ✓ {module}")
        except ImportError as e:
            print(f"  ✗ {module}: {e}")
            failed.append(module)
    
    return len(failed) == 0


def check_dependencies():
    """Check if required dependencies are installed."""
    print("\nChecking dependencies...")
    
    dependencies = [
        "sqlalchemy",
        "sentence_transformers",
        "numpy",
        "networkx",
    ]
    
    failed = []
    for dep in dependencies:
        try:
            importlib.import_module(dep.replace("-", "_"))
            print(f"  ✓ {dep}")
        except ImportError:
            print(f"  ✗ {dep} (not installed)")
            failed.append(dep)
    
    return len(failed) == 0


def check_basic_functionality():
    """Check if basic functionality works."""
    print("\nChecking basic functionality...")
    
    try:
        from memorable import MemoryEngine
        
        # Try to create an instance
        memory = MemoryEngine(database="sqlite:///:memory:", mode="auto")
        print("  ✓ MemoryEngine creation")
        
        # Try to get stats
        stats = memory.get_stats()
        print("  ✓ get_stats()")
        
        return True
    except Exception as e:
        print(f"  ✗ Basic functionality failed: {e}")
        return False


def main():
    """Run all checks."""
    print("=" * 50)
    print("Memorable Setup Check")
    print("=" * 50)
    
    all_passed = True
    
    # Check imports
    if not check_imports():
        all_passed = False
    
    # Check dependencies
    if not check_dependencies():
        all_passed = False
        print("\n⚠ Some dependencies are missing. Install with: pip install -r requirements.txt")
    
    # Check basic functionality
    if not check_basic_functionality():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All checks passed!")
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

