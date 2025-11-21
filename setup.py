"""Setup configuration for Memorable."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt if it exists, otherwise use pyproject.toml dependencies
try:
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
except FileNotFoundError:
    # Fallback: dependencies are defined in pyproject.toml
    requirements = [
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.0",
        "aiosqlite>=0.19.0",
        "sentence-transformers>=2.2.0",
        "numpy>=1.24.0",
        "openai>=1.0.0",
        "anthropic>=0.7.0",
        "litellm>=1.0.0",
        "networkx>=3.0",
        "aiohttp>=3.9.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "structlog>=23.0.0",
    ]

setup(
    name="memorable-ai",
    version="0.1.1",
    author="Memorable Team",
    description="Advanced Memory Engine for LLMs, AI Agents & Multi-Agent Systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0sparsh2/memorable-ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "memorable=memorable_ai.cli:main",
        ],
    },
    extras_require={
        "graph": [
            "neo4j>=5.0.0",
            "networkx>=3.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "all": [
            "neo4j>=5.0.0",
            "networkx>=3.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
        ],
    },
)

