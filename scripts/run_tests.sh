#!/bin/bash
# Quick test runner script

set -e

echo "Running Memorable tests..."
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "pytest not found. Installing..."
    pip install pytest pytest-cov pytest-asyncio
fi

# Run tests
echo "Running unit tests..."
pytest tests/unit/ -v

echo ""
echo "Running integration tests..."
pytest tests/integration/ -v

echo ""
echo "Running with coverage..."
pytest tests/ --cov=memorable --cov-report=term-missing --cov-report=html

echo ""
echo "Tests complete! Coverage report: htmlcov/index.html"

