"""
Tests for task_tracker.storage
"""

import pytest
import json
from pathlib import Path
from datetime import datetime

from task_tracker.storage import TaskStorage
from task_tracker.models import Task, TaskCollection


@pytest.fixture
def temp_storage(tmp_path):
    """Create a temporary storage instance"""
    data_file = tmp_path / "tasks.json"
    return TaskStorage(data_file=data_file)


@pytest.fixture
def storage_with_tasks(tmp_path):
    """Create a storage instance with sample tasks"""
    data_file = tmp_path / "tasks.json"
    storage = TaskStorage(data_file=data_file)

    # Add sample tasks
    storage.create_task("Task 1")
    storage.create_task("Task 2")
    storage.create_task("Task 3")

    # Complete one task
    storage.complete_task(2)

    return storage


class TestTaskStorage:
    """Test TaskStorage class"""

    def test_initialization_creates_file(self, tmp_path):
        """Test that initialization creates the data file"""
        data_file = tmp_path / "tasks.json"
        assert not data_file.exists()

        storage = TaskStorage(data_file=data_file)

        assert data_file.exists()

    def test_create_task(self, temp_storage):
        """Test creating a task"""
        task = temp_storage.create_task("Test task")

        assert task.id == 1
        assert task.title == "Test task"
        assert task.status == "pending"
        assert isinstance(task.created_at, datetime)

    def test_create_multiple_tasks_increments_id(self, temp_storage):
        """Test that creating multiple tasks increments ID"""
        task1 = temp_storage.create_task("Task 1")
        task2 = temp_storage.create_task("Task 2")
        task3 = temp_storage.create_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_get_task_existing(self, storage_with_tasks):
        """Test retrieving an existing task"""
        task = storage_with_tasks.get_task(1)

        assert task is not None
        assert task.id == 1
        assert task.title == "Task 1"

    def test_get_task_non_existing(self, temp_storage):
        """Test retrieving a non-existing task"""
        task = temp_storage.get_task(999)

        assert task is None

    def test_list_tasks_all(self, storage_with_tasks):
        """Test listing all tasks"""
        tasks = storage_with_tasks.list_tasks()

        assert len(tasks) == 3

    def test_list_tasks_pending(self, storage_with_tasks):
        """Test listing pending tasks"""
        tasks = storage_with_tasks.list_tasks(status="pending")

        assert len(tasks) == 2
        assert all(t.status == "pending" for t in tasks)

    def test_list_tasks_completed(self, storage_with_tasks):
        """Test listing completed tasks"""
        tasks = storage_with_tasks.list_tasks(status="completed")

        assert len(tasks) == 1
        assert all(t.status == "completed" for t in tasks)

    def test_list_tasks_sorted_by_date(self, storage_with_tasks):
        """Test that tasks are sorted by creation date (newest first)"""
        tasks = storage_with_tasks.list_tasks()

        # Tasks should be in reverse order (newest first)
        assert tasks[0].id == 3
        assert tasks[1].id == 2
        assert tasks[2].id == 1

    def test_update_task_existing(self, storage_with_tasks):
        """Test updating an existing task"""
        task = storage_with_tasks.update_task(1, title="Updated title")

        assert task is not None
        assert task.title == "Updated title"

        # Verify the update persisted
        reloaded_task = storage_with_tasks.get_task(1)
        assert reloaded_task.title == "Updated title"

    def test_update_task_non_existing(self, temp_storage):
        """Test updating a non-existing task"""
        task = temp_storage.update_task(999, title="Updated")

        assert task is None

    def test_complete_task_existing(self, temp_storage):
        """Test completing an existing task"""
        temp_storage.create_task("Test task")
        task = temp_storage.complete_task(1)

        assert task is not None
        assert task.status == "completed"
        assert task.completed_at is not None

    def test_complete_task_already_completed(self, storage_with_tasks):
        """Test completing an already completed task"""
        with pytest.raises(ValueError, match="already completed"):
            storage_with_tasks.complete_task(2)

    def test_complete_task_force(self, storage_with_tasks):
        """Test force completing an already completed task"""
        task = storage_with_tasks.complete_task(2, force=True)

        assert task is not None
        assert task.status == "completed"

    def test_complete_task_non_existing(self, temp_storage):
        """Test completing a non-existing task"""
        task = temp_storage.complete_task(999)

        assert task is None

    def test_delete_task_existing(self, storage_with_tasks):
        """Test deleting an existing task"""
        success = storage_with_tasks.delete_task(1)

        assert success is True

        # Verify task is deleted
        task = storage_with_tasks.get_task(1)
        assert task is None

    def test_delete_task_non_existing(self, temp_storage):
        """Test deleting a non-existing task"""
        success = temp_storage.delete_task(999)

        assert success is False

    def test_atomic_write(self, tmp_path):
        """Test that writes are atomic (temp file + rename)"""
        data_file = tmp_path / "tasks.json"
        temp_file = tmp_path / "tasks.tmp"

        storage = TaskStorage(data_file=data_file)
        storage.create_task("Test task")

        # Temp file should not exist after save
        assert not temp_file.exists()
        assert data_file.exists()

    def test_data_persistence(self, tmp_path):
        """Test that data persists across storage instances"""
        data_file = tmp_path / "tasks.json"

        # Create tasks with first instance
        storage1 = TaskStorage(data_file=data_file)
        storage1.create_task("Task 1")
        storage1.create_task("Task 2")

        # Load with second instance
        storage2 = TaskStorage(data_file=data_file)
        tasks = storage2.list_tasks()

        assert len(tasks) == 2
        assert tasks[0].title == "Task 2"
        assert tasks[1].title == "Task 1"

    def test_corrupted_json_error(self, tmp_path):
        """Test handling of corrupted JSON file"""
        data_file = tmp_path / "tasks.json"

        # Create valid storage first
        storage = TaskStorage(data_file=data_file)

        # Corrupt the file
        with open(data_file, 'w') as f:
            f.write("invalid json {")

        # Should raise ValueError with helpful message
        with pytest.raises(ValueError, match="Corrupted task data file"):
            storage._load()
