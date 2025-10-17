"""
Tests for task_tracker.models
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from task_tracker.models import Task, TaskCollection


class TestTask:
    """Test Task model"""

    def test_create_task_with_defaults(self):
        """Test creating a task with default values"""
        task = Task(id=1, title="Test task")

        assert task.id == 1
        assert task.title == "Test task"
        assert task.status == "pending"
        assert isinstance(task.created_at, datetime)
        assert task.completed_at is None

    def test_create_task_with_custom_values(self):
        """Test creating a task with custom values"""
        now = datetime.now()
        task = Task(
            id=1,
            title="Test task",
            status="completed",
            created_at=now,
            completed_at=now
        )

        assert task.id == 1
        assert task.title == "Test task"
        assert task.status == "completed"
        assert task.created_at == now
        assert task.completed_at == now

    def test_task_title_validation_min_length(self):
        """Test task title must not be empty"""
        with pytest.raises(ValidationError):
            Task(id=1, title="")

    def test_task_title_validation_max_length(self):
        """Test task title must not exceed 200 characters"""
        with pytest.raises(ValidationError):
            Task(id=1, title="x" * 201)

    def test_task_status_validation(self):
        """Test task status must be 'pending' or 'completed'"""
        with pytest.raises(ValidationError):
            Task(id=1, title="Test", status="invalid")

    def test_mark_completed(self):
        """Test marking a task as completed"""
        task = Task(id=1, title="Test task")
        assert task.status == "pending"
        assert task.completed_at is None

        task.mark_completed()

        assert task.status == "completed"
        assert isinstance(task.completed_at, datetime)


class TestTaskCollection:
    """Test TaskCollection model"""

    def test_create_empty_collection(self):
        """Test creating an empty task collection"""
        collection = TaskCollection()

        assert collection.version == "1.0.0"
        assert collection.last_id == 0
        assert collection.tasks == []

    def test_create_collection_with_tasks(self):
        """Test creating a collection with tasks"""
        task1 = Task(id=1, title="Task 1")
        task2 = Task(id=2, title="Task 2")

        collection = TaskCollection(
            last_id=2,
            tasks=[task1, task2]
        )

        assert collection.last_id == 2
        assert len(collection.tasks) == 2
        assert collection.tasks[0].title == "Task 1"
        assert collection.tasks[1].title == "Task 2"
