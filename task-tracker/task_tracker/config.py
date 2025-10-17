"""
Application configuration and environment variables.
"""

import os
from pathlib import Path
from typing import Dict, Any


def get_data_file_path() -> Path:
    """
    Get path to tasks.json file.

    Returns:
        Path to the task data file. Checks TASK_TRACKER_DATA_FILE environment
        variable first, otherwise defaults to ~/.task-tracker/tasks.json
    """
    custom_path = os.getenv("TASK_TRACKER_DATA_FILE")
    if custom_path:
        return Path(custom_path)

    # Default: ~/.task-tracker/tasks.json
    home = Path.home()
    return home / ".task-tracker" / "tasks.json"


def get_config() -> Dict[str, Any]:
    """
    Get application configuration.

    Returns:
        Dictionary containing all configuration values
    """
    return {
        "data_file": get_data_file_path(),
        "backup_enabled": os.getenv("TASK_TRACKER_BACKUP", "true").lower() == "true",
        "max_title_length": 200,
        "version": "1.0.0",
    }
