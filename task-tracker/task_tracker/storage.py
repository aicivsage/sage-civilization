"""
JSON file storage operations.
Handles reading, writing, and querying tasks.
"""

import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from task_tracker.models import Task, TaskCollection
from task_tracker.config import get_data_file_path


class TaskStorage:
    """Manages task persistence in JSON file"""

    def __init__(self, data_file: Optional[Path] = None):
        """
        Initialize storage with data file path.

        Args:
            data_file: Optional custom path to data file. If not provided,
                      uses default from config.
        """
        self.data_file = data_file or get_data_file_path()
        self._ensure_file_exists()

    def create_task(self, title: str) -> Task:
        """
        Create and save a new task.

        Args:
            title: Task title

        Returns:
            Newly created Task object
        """
        collection = self._load()
        task = Task(id=collection.last_id + 1, title=title)
        collection.tasks.append(task)
        collection.last_id = task.id
        self._save(collection)
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve task by ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task object if found, None otherwise
        """
        collection = self._load()
        for task in collection.tasks:
            if task.id == task_id:
                return task
        return None

    def list_tasks(self, status: Optional[str] = None) -> List[Task]:
        """
        List tasks with optional status filter.

        Args:
            status: Optional status filter ('pending' or 'completed')

        Returns:
            List of tasks matching the filter criteria, sorted by creation date (newest first)
        """
        collection = self._load()
        tasks = collection.tasks

        if status:
            tasks = [t for t in tasks if t.status == status]

        # Sort by creation date, newest first
        tasks.sort(key=lambda t: t.created_at, reverse=True)

        return tasks

    def update_task(self, task_id: int, **updates) -> Optional[Task]:
        """
        Update task fields.

        Args:
            task_id: ID of the task to update
            **updates: Field updates to apply

        Returns:
            Updated Task object if found, None otherwise
        """
        collection = self._load()

        for task in collection.tasks:
            if task.id == task_id:
                # Apply updates
                for key, value in updates.items():
                    if hasattr(task, key):
                        setattr(task, key, value)

                self._save(collection)
                return task

        return None

    def complete_task(self, task_id: int, force: bool = False) -> Optional[Task]:
        """
        Mark task as completed.

        Args:
            task_id: ID of the task to complete
            force: If True, update completion time even if already completed

        Returns:
            Updated Task object if successful, None if not found

        Raises:
            ValueError: If task is already completed and force is False
        """
        collection = self._load()

        for task in collection.tasks:
            if task.id == task_id:
                if task.status == "completed" and not force:
                    raise ValueError(f"Task #{task_id} is already completed")

                task.mark_completed()
                self._save(collection)
                return task

        return None

    def delete_task(self, task_id: int) -> bool:
        """
        Delete task by ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if task was deleted, False if not found
        """
        collection = self._load()
        initial_count = len(collection.tasks)

        collection.tasks = [t for t in collection.tasks if t.id != task_id]

        if len(collection.tasks) < initial_count:
            self._save(collection)
            return True

        return False

    def _load(self) -> TaskCollection:
        """
        Load tasks from JSON file.

        Returns:
            TaskCollection object with all tasks

        Raises:
            ValueError: If JSON file is corrupted or invalid
        """
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            return TaskCollection(**data)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Corrupted task data file: {self.data_file}\n"
                f"Error: {e}\n"
                f"Consider restoring from backup or deleting the file to start fresh."
            )
        except Exception as e:
            raise ValueError(f"Error loading tasks: {e}")

    def _save(self, collection: TaskCollection) -> None:
        """
        Save tasks to JSON file with atomic write.

        Uses temp file + rename for atomic operation to prevent corruption.

        Args:
            collection: TaskCollection to save
        """
        # Write to temp file first
        temp_file = self.data_file.with_suffix('.tmp')

        try:
            with open(temp_file, 'w') as f:
                # Convert to dict and handle datetime serialization
                data = collection.model_dump(mode='json')
                json.dump(data, f, indent=2, default=str)

            # Atomic rename
            temp_file.replace(self.data_file)
        except Exception as e:
            # Clean up temp file if something went wrong
            if temp_file.exists():
                temp_file.unlink()
            raise ValueError(f"Error saving tasks: {e}")

    def _ensure_file_exists(self) -> None:
        """Create data file and directory if they don't exist"""
        if not self.data_file.exists():
            # Create parent directory
            self.data_file.parent.mkdir(parents=True, exist_ok=True)

            # Initialize with empty task collection
            initial_data = TaskCollection(version="1.0.0", last_id=0, tasks=[])
            self._save(initial_data)
