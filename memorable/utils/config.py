"""
Configuration management for Memorable.

Supports environment variables, config files, and programmatic configuration.
"""

import os
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DatabaseConfig(BaseModel):
    """Database configuration."""

    connection_string: Optional[str] = Field(
        default=None, description="Database connection string"
    )
    pool_size: int = Field(default=5, description="Connection pool size")
    max_overflow: int = Field(default=10, description="Max overflow connections")


class GraphConfig(BaseModel):
    """Graph database configuration (optional)."""

    enabled: bool = Field(default=False, description="Enable graph storage")
    connection_string: Optional[str] = Field(
        default=None, description="Graph database connection string (Neo4j, etc.)"
    )


class MemoryConfig(BaseModel):
    """Memory engine configuration."""

    mode: str = Field(
        default="auto", description="Memory mode: 'conscious', 'auto', or 'hybrid'"
    )
    namespace: Optional[str] = Field(
        default=None, description="Memory namespace for multi-tenant support"
    )
    max_context_tokens: int = Field(
        default=2000, description="Maximum tokens to inject as context"
    )
    consolidation_interval: int = Field(
        default=21600, description="Memory consolidation interval in seconds (6 hours)"
    )


class LLMConfig(BaseModel):
    """LLM provider configuration."""

    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    anthropic_api_key: Optional[str] = Field(
        default=None, description="Anthropic API key"
    )
    default_model: str = Field(
        default="gpt-4o-mini", description="Default LLM model"
    )
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Embedding model for semantic search",
    )


class MemorableConfig(BaseModel):
    """Main configuration for Memorable."""

    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    graph: GraphConfig = Field(default_factory=GraphConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)

    @classmethod
    def from_env(cls) -> "MemorableConfig":
        """Load configuration from environment variables."""
        return cls(
            database=DatabaseConfig(
                connection_string=os.getenv("MEMORABLE_DATABASE__CONNECTION_STRING"),
                pool_size=int(os.getenv("MEMORABLE_DATABASE__POOL_SIZE", "5")),
                max_overflow=int(os.getenv("MEMORABLE_DATABASE__MAX_OVERFLOW", "10")),
            ),
            graph=GraphConfig(
                enabled=os.getenv("MEMORABLE_GRAPH__ENABLED", "false").lower() == "true",
                connection_string=os.getenv("MEMORABLE_GRAPH__CONNECTION_STRING"),
            ),
            memory=MemoryConfig(
                mode=os.getenv("MEMORABLE_MEMORY__MODE", "auto"),
                namespace=os.getenv("MEMORABLE_MEMORY__NAMESPACE"),
                max_context_tokens=int(
                    os.getenv("MEMORABLE_MEMORY__MAX_CONTEXT_TOKENS", "2000")
                ),
                consolidation_interval=int(
                    os.getenv("MEMORABLE_MEMORY__CONSOLIDATION_INTERVAL", "21600")
                ),
            ),
            llm=LLMConfig(
                openai_api_key=os.getenv("OPENAI_API_KEY")
                or os.getenv("MEMORABLE_LLM__OPENAI_API_KEY"),
                anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
                or os.getenv("MEMORABLE_LLM__ANTHROPIC_API_KEY"),
                default_model=os.getenv("MEMORABLE_LLM__DEFAULT_MODEL", "gpt-4o-mini"),
                embedding_model=os.getenv(
                    "MEMORABLE_LLM__EMBEDDING_MODEL",
                    "sentence-transformers/all-MiniLM-L6-v2",
                ),
            ),
        )

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "MemorableConfig":
        """Load configuration from dictionary."""
        return cls(**config_dict)

