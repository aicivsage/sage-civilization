# Pattern: Pytest Test Organization

## Pattern ID
`python-pytest-testing-004`

## Category
Testing & Quality Assurance

## Problem
How do we organize test files, fixtures, and test cases to maximize maintainability, reusability, and clarity while achieving high test coverage?

## Solution
Use pytest with a clear hierarchical structure: test classes for logical grouping, shared fixtures in conftest.py, descriptive test names that read like documentation, and separate test files that mirror source code structure.

## Implementation

### Directory Structure
```
project/
├── src/
│   ├── models.py
│   ├── storage.py
│   └── cli.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures
│   ├── fixtures/            # Test data files
│   │   └── sample_data.json
│   ├── test_models.py       # Mirrors src/models.py
│   ├── test_storage.py      # Mirrors src/storage.py
│   └── test_cli.py          # Mirrors src/cli.py
├── pytest.ini               # Pytest configuration
└── .coveragerc              # Coverage configuration
```

**Source:** `task-tracker/tests/` directory structure

### Test Class Organization
```python
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
```

**Source:** `task-tracker/tests/test_models.py:1-80`

### Fixtures Pattern
```python
# tests/conftest.py
"""
Shared test fixtures.
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from task_tracker.storage import TaskStorage
from task_tracker.models import Task


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary directory for test data"""
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    yield data_dir
    # Cleanup happens automatically with tmp_path


@pytest.fixture
def storage(temp_data_dir):
    """Create a TaskStorage instance with temporary file"""
    data_file = temp_data_dir / "tasks.json"
    return TaskStorage(data_file)


@pytest.fixture
def sample_task():
    """Create a sample task for testing"""
    return Task(
        id=1,
        title="Sample task",
        status="pending"
    )


@pytest.fixture
def multiple_tasks(storage):
    """Create multiple tasks for testing"""
    storage.create_task("Task 1")
    storage.create_task("Task 2")
    storage.create_task("Task 3")
    return storage
```

**Source:** `task-tracker/tests/fixtures/` and usage patterns

### Testing CLI with CliRunner
```python
from typer.testing import CliRunner
from task_tracker.cli import app

runner = CliRunner()


class TestAddCommand:
    """Test 'add' command"""

    def test_add_task_success(self, temp_data_dir):
        """Test adding a task successfully"""
        result = runner.invoke(app, ["add", "New task"])

        assert result.exit_code == 0
        assert "Task added successfully" in result.stdout
        assert "New task" in result.stdout

    def test_add_task_with_special_characters(self):
        """Test adding task with special characters"""
        result = runner.invoke(app, ["add", "Task with 'quotes' and \"double quotes\""])

        assert result.exit_code == 0
        assert "Task added successfully" in result.stdout

    def test_add_task_missing_title(self):
        """Test adding task without title fails"""
        result = runner.invoke(app, ["add"])

        assert result.exit_code != 0
```

**Source:** `task-tracker/tests/test_cli.py:10-90`

### Testing Exceptions
```python
import pytest

class TestTaskStorage:
    """Test TaskStorage class"""

    def test_create_task_validation_error(self, storage):
        """Test that invalid task data raises validation error"""
        with pytest.raises(ValidationError) as exc_info:
            storage.create_task("")  # Empty title

        assert "title" in str(exc_info.value).lower()

    def test_get_nonexistent_task(self, storage):
        """Test getting a task that doesn't exist returns None"""
        task = storage.get_task(999)
        assert task is None

    def test_update_nonexistent_task(self, storage):
        """Test updating a task that doesn't exist returns None"""
        result = storage.update_task(999, title="Updated")
        assert result is None
```

## When to Use
✅ **Use when:**
- Building any Python project (tests should always exist)
- Need high test coverage (pytest makes it easy)
- Want readable, self-documenting tests
- Testing CLI tools, APIs, libraries
- Need fixtures for test data setup/teardown
- Want parametrized tests for multiple inputs

❌ **Don't use when:**
- Never - always write tests!

## Benefits
1. **Clear Organization:** Test classes group related tests
2. **Reusable Fixtures:** Setup code shared across tests
3. **Readable Output:** Descriptive test names become documentation
4. **Easy Discovery:** pytest auto-discovers test_*.py files
5. **Powerful Assertions:** Better error messages than unittest
6. **Parametrization:** Test multiple inputs easily

## Pitfalls
1. **Fixture Scope:** Understand function/module/session scopes
2. **Fixture Dependencies:** Avoid complex dependency chains
3. **Over-Mocking:** Don't mock everything - test real behavior when possible
4. **Test Pollution:** Tests should be independent, not rely on order
5. **Slow Tests:** Use pytest-xdist for parallel execution

## Configuration

### pytest.ini
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --verbose
    --strict-markers
    --cov=task_tracker
    --cov-report=html
    --cov-report=term-missing
```

### .coveragerc
```ini
[run]
source = task_tracker
omit =
    */tests/*
    */venv/*
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

**Source:** `task-tracker/pytest.ini` and `.coveragerc` patterns

## Test Naming Conventions

### Good Test Names
```python
# ✅ Descriptive and clear
def test_create_task_with_valid_title():
    """Test creating task with valid title succeeds"""
    pass

def test_update_task_marks_as_completed():
    """Test updating task status to completed"""
    pass

def test_list_tasks_filters_by_status():
    """Test listing tasks with status filter"""
    pass
```

### Bad Test Names
```python
# ❌ Vague and unclear
def test_task():
    pass

def test_1():
    pass

def test_stuff():
    pass
```

## Parametrized Testing
```python
import pytest

@pytest.mark.parametrize("status,expected_count", [
    ("pending", 2),
    ("completed", 1),
    (None, 3),
])
def test_list_tasks_with_various_filters(storage, status, expected_count):
    """Test listing tasks with different status filters"""
    # Setup
    storage.create_task("Task 1")  # pending
    storage.create_task("Task 2")  # pending
    task3 = storage.create_task("Task 3")
    storage.update_task(task3.id, status="completed")

    # Test
    tasks = storage.list_tasks(status=status)

    # Assert
    assert len(tasks) == expected_count


@pytest.mark.parametrize("title", [
    "",  # Empty
    "x" * 201,  # Too long
])
def test_invalid_task_titles(title):
    """Test that invalid titles raise ValidationError"""
    with pytest.raises(ValidationError):
        Task(id=1, title=title)
```

## Coverage Strategy

### Running Coverage
```bash
# Run tests with coverage
pytest --cov=task_tracker --cov-report=html

# View HTML report
open htmlcov/index.html

# Target: 90%+ coverage
# Focus on: models, storage, core business logic
# Less critical: CLI formatting, error messages
```

### Coverage Goals
- **Models/Core Logic:** 100% coverage
- **Storage/Persistence:** 95%+ coverage
- **CLI/UI Layer:** 85%+ coverage
- **Overall Project:** 90%+ coverage

**Source:** Task-tracker achieved 91% coverage

## Lessons Learned
1. **Test names are documentation** - Make them descriptive
2. **One assert per test** - Makes failures easier to debug
3. **Use fixtures liberally** - Reduces test code duplication
4. **Test edge cases** - Empty strings, None, max values
5. **Test error paths** - Not just happy path
6. **tmp_path is your friend** - Use it for file I/O tests
7. **Don't test implementation** - Test behavior/interface

## Code Checklist
- [ ] Test file mirrors source file name (test_module.py)
- [ ] Test classes group related functionality
- [ ] All test functions have descriptive names
- [ ] Each test has a docstring explaining what it tests
- [ ] Fixtures in conftest.py for shared setup
- [ ] Tests are independent (can run in any order)
- [ ] Edge cases and error paths tested
- [ ] Coverage >90% for core logic
- [ ] No test pollution (cleanup after tests)

## Related Patterns
- `python-pydantic-001` - Testing Pydantic validation
- `python-atomic-write-002` - Testing file operations with tmp_path
- `python-cli-typer-003` - Testing Typer CLIs with CliRunner

## Real-World Usage
This pattern is used in:
- Task-tracker (91% coverage, 40+ tests)
- Agent messaging (100% test pass rate)
- All A-C-Gee civilization projects

## Version
- **Created:** 2025-10-04
- **Last Updated:** 2025-10-04
- **Success Rate:** 100% (91% coverage achieved, 0 test failures in CI)
