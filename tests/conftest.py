"""
Pytest configuration and shared fixtures.
"""

import pytest
import os


@pytest.fixture(scope="session")
def test_environment():
    """Set up test environment variables."""
    os.environ["MEMORABLE_DATABASE__CONNECTION_STRING"] = "sqlite:///test.db"
    os.environ["MEMORABLE_MEMORY__MODE"] = "auto"
    yield
    # Cleanup
    if os.path.exists("test.db"):
        os.remove("test.db")

