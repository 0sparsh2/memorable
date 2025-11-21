# Contributing to Memorable

Thank you for your interest in contributing to Memorable! This document provides guidelines and instructions for contributing.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/memorable.git
cd memorable
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e ".[dev]"
```

## Code Style

- Follow PEP 8 style guidelines
- Use `black` for code formatting
- Use `flake8` for linting
- Type hints are encouraged

## Testing

- Write tests for all new features
- Ensure test coverage > 90%
- Run tests with: `pytest tests/`
- Run with coverage: `pytest --cov=memorable tests/`

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Add tests
4. Update documentation
5. Submit a pull request with a clear description

## References

When contributing, please cite relevant sources:
- Memori: https://github.com/GibsonAI/Memori
- Mem0: https://github.com/mem0ai/mem0
- Supermemory: https://github.com/supermemoryai/supermemory

