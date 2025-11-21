#!/bin/bash

# Script to help publish Memorable to PyPI
# Usage: ./scripts/publish_to_pypi.sh [test|production]

set -e

echo "================================================"
echo "Memorable PyPI Publishing Helper"
echo "================================================"
echo ""

# Check if build tools are installed
if ! command -v twine &> /dev/null; then
    echo "❌ twine not found. Installing..."
    pip install build twine
fi

# Build the package
echo "📦 Building package..."
python3 -m build

# Check the package
echo "✅ Checking package..."
twine check dist/*

# Determine which PyPI to use
ENV=${1:-production}

if [ "$ENV" = "test" ]; then
    echo ""
    echo "🧪 Publishing to Test PyPI..."
    echo "URL: https://test.pypi.org/project/memorable/"
    echo ""
    echo "Enter your Test PyPI token (starts with pypi-):"
    read -s TEST_TOKEN
    export TWINE_USERNAME=__token__
    export TWINE_PASSWORD=$TEST_TOKEN
    twine upload --repository testpypi dist/*
    echo ""
    echo "✅ Published to Test PyPI!"
    echo "Test installation with:"
    echo "  pip install --index-url https://test.pypi.org/simple/ memorable"
elif [ "$ENV" = "production" ]; then
    echo ""
    echo "🚀 Publishing to Production PyPI..."
    echo "URL: https://pypi.org/project/memorable/"
    echo ""
    echo "⚠️  WARNING: This will publish to production PyPI!"
    echo "Make sure you've tested on Test PyPI first!"
    echo ""
    read -p "Continue? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "❌ Cancelled."
        exit 1
    fi
    echo ""
    echo "Enter your PyPI token (starts with pypi-):"
    read -s PROD_TOKEN
    export TWINE_USERNAME=__token__
    export TWINE_PASSWORD=$PROD_TOKEN
    twine upload dist/*
    echo ""
    echo "✅ Published to PyPI!"
    echo "Users can now install with: pip install memorable"
else
    echo "Usage: $0 [test|production]"
    exit 1
fi

