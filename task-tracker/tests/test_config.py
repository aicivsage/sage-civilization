"""
Tests for task_tracker.config
"""

import os
import pytest
from pathlib import Path

from task_tracker.config import get_data_file_path, get_config


class TestConfig:
    """Test configuration functions"""

    def test_get_data_file_path_default(self):
        """Test default data file path"""
        # Clear environment variable
        os.environ.pop("TASK_TRACKER_DATA_FILE", None)

        path = get_data_file_path()

        assert isinstance(path, Path)
        assert path == Path.home() / ".task-tracker" / "tasks.json"

    def test_get_data_file_path_custom(self):
        """Test custom data file path from environment variable"""
        custom_path = "/tmp/custom-tasks.json"
        os.environ["TASK_TRACKER_DATA_FILE"] = custom_path

        try:
            path = get_data_file_path()
            assert path == Path(custom_path)
        finally:
            # Clean up
            os.environ.pop("TASK_TRACKER_DATA_FILE", None)

    def test_get_config_default(self):
        """Test getting default configuration"""
        # Clear environment variables
        os.environ.pop("TASK_TRACKER_DATA_FILE", None)
        os.environ.pop("TASK_TRACKER_BACKUP", None)

        config = get_config()

        assert config["data_file"] == Path.home() / ".task-tracker" / "tasks.json"
        assert config["backup_enabled"] is True
        assert config["max_title_length"] == 200
        assert config["version"] == "1.0.0"

    def test_get_config_custom_backup(self):
        """Test configuration with custom backup setting"""
        os.environ["TASK_TRACKER_BACKUP"] = "false"

        try:
            config = get_config()
            assert config["backup_enabled"] is False
        finally:
            os.environ.pop("TASK_TRACKER_BACKUP", None)
