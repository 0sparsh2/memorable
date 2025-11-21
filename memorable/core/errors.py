"""
Error classes for Memorable.
"""


class MemorableError(Exception):
    """Base exception for Memorable."""

    pass


class StorageError(MemorableError):
    """Storage-related errors."""

    pass


class RetrievalError(MemorableError):
    """Retrieval-related errors."""

    pass


class ExtractionError(MemorableError):
    """Memory extraction errors."""

    pass


class ConfigurationError(MemorableError):
    """Configuration errors."""

    pass


class InterceptorError(MemorableError):
    """Interceptor-related errors."""

    pass


class GraphError(MemorableError):
    """Graph-related errors."""

    pass

