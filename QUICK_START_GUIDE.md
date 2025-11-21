# Quick Start Guide - Get Memorable Running in 5 Minutes

## Step 1: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Step 2: Verify Installation

```bash
# Run setup check
python scripts/check_setup.py

# Or manually test import
python -c "from memorable import MemoryEngine; print('✓ Import successful')"
```

## Step 3: Run Tests

```bash
# Quick test run
./scripts/run_tests.sh

# Or use make
make test

# Or use pytest directly
pytest tests/ -v
```

## Step 4: Try Basic Example

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="sk-your-key-here"

# Run basic example
python examples/basic_usage.py
```

## Step 5: Use in Your Code

```python
from memorable import MemoryEngine
from openai import OpenAI

# Initialize and enable
memory = MemoryEngine(database="sqlite:///memory.db", mode="auto")
memory.enable()

# Your existing code works unchanged!
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "I'm building a FastAPI project"}]
)
```

## Troubleshooting

### Import Errors
```bash
# Make sure you're in the project directory
cd /path/to/memorable

# Reinstall in development mode
pip install -e .
```

### Missing Dependencies
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install with dev dependencies
pip install -e ".[dev]"
```

### Database Issues
```bash
# For SQLite (default), no setup needed
# For PostgreSQL, make sure it's running:
#   brew install postgresql  # macOS
#   sudo apt-get install postgresql  # Linux

# Test connection
python -c "from memorable import MemoryEngine; m = MemoryEngine(database='sqlite:///test.db'); print('✓ Database OK')"
```

### Test Failures
```bash
# Run tests with verbose output
pytest tests/ -v -s

# Run specific test file
pytest tests/unit/test_storage.py -v

# Run with debugging
pytest tests/ -v --pdb
```

## Next Steps

1. **Read the README**: `README.md` for full documentation
2. **Check Examples**: `examples/` directory for usage patterns
3. **Read API Docs**: `docs/api.md` for API reference
4. **See Architecture**: `docs/architecture.md` for system design

## Common Commands

```bash
# Run tests
make test

# Run with coverage
make test-cov

# Format code
make format

# Lint code
make lint

# Clean up
make clean

# Check setup
python scripts/check_setup.py
```

## Getting Help

- Check `NEXT_STEPS.md` for development roadmap
- Check `FEATURES.md` for feature list
- Check `docs/` for detailed documentation
- Run `python scripts/check_setup.py` to diagnose issues

