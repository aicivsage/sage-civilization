"""
Pytest configuration and shared fixtures for Ed25519 integration tests.

This module provides common test fixtures and configuration
used across the test suite.
"""

import os
import sys
from pathlib import Path

import pytest

# Add task-tracker to Python path for imports
task_tracker_path = Path(__file__).parent.parent / "task-tracker"
sys.path.insert(0, str(task_tracker_path))


@pytest.fixture(scope="session")
def sample_agent_registry():
    """Sample agent registry data for testing."""
    return {
        "agent-alpha": {
            "name": "agent-alpha",
            "role": "researcher",
            "model": "sonnet-4",
            "status": "active",
        },
        "agent-beta": {
            "name": "agent-beta",
            "role": "coder",
            "model": "sonnet-4",
            "status": "active",
        },
        "agent-gamma": {
            "name": "agent-gamma",
            "role": "tester",
            "model": "sonnet-4",
            "status": "active",
        },
    }


@pytest.fixture
def clean_test_env(tmp_path, monkeypatch):
    """Set up clean test environment with isolated directories."""
    test_home = tmp_path / ".aiciv"
    test_home.mkdir()

    test_keys = test_home / "keys"
    test_keys.mkdir()

    test_messages = test_home / "messages"
    test_messages.mkdir()

    # Set environment variables
    monkeypatch.setenv("AICIV_HOME", str(test_home))
    monkeypatch.setenv("AICIV_KEYS_DIR", str(test_keys))

    return {
        "home": test_home,
        "keys": test_keys,
        "messages": test_messages,
    }


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
