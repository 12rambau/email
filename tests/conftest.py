"""Pytest configuration."""

import pytest
from sphinx.testing.path import path

pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture(scope="session")
def rootdir():
    """Get the root directory for the whole test session."""
    return path(__file__).parent.abspath() / "roots"
