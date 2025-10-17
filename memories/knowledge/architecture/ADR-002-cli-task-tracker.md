# ADR-002: CLI Task Tracker Architecture

**Status:** Proposed
**Date:** 2025-10-01
**Decision Makers:** Architecture Team
**Technical Story:** Design simple command-line task tracker with minimal dependencies and local storage

---

## Context and Problem Statement

We need a lightweight, single-user CLI tool for tracking daily tasks that can run on any machine with Python 3.9+. The tool must be simple to use, require minimal setup, and maintain task data locally without external dependencies beyond the CLI library.

### Requirements

**Functional Requirements:**
- Commands: `add`, `list`, `complete`, `delete`, `show`
- Task properties: id, title, status (pending/completed), created_at
- Local persistent storage
- Simple command-line interface with clear output

**Non-Functional Requirements:**
- Zero configuration required (works out of the box)
- No database server setup needed
- Fast command execution (< 100ms)
- Minimal dependencies (only CLI library)
- Cross-platform compatibility (Linux, macOS, Windows)
- Human-readable data format for manual inspection/editing

---

## Decision Drivers

1. **Simplicity**: Must be trivial to install and use
2. **No Infrastructure**: Should work without any server setup
3. **Portability**: Data should be easily backed up and transferred
4. **Developer Experience**: Clear CLI interface with helpful messages
5. **Maintainability**: Minimal code that's easy to understand and modify
6. **Data Safety**: No risk of data corruption from concurrent access
7. **Extensibility**: Easy to add new fields or commands later

---

## Technology Stack Decision

### CLI Framework: Typer

**Rationale:**

**Typer** is the optimal choice for this simple CLI application:

**Advantages:**
- **Modern Python**: Built on Python 3.6+ type hints
- **Zero Learning Curve**: Functions become CLI commands automatically
- **Great UX**: Automatic help generation, parameter validation
- **Rich Integration**: Built-in support for colored output via Rich library
- **Type Safety**: Leverages Python type annotations
- **Minimal Boilerplate**: Much less code than Click
- **Active Development**: Maintained by creator of FastAPI

**Code Comparison:**
```python
# Typer approach
import typer
app = typer.Typer()

@app.command()
def add(title: str, priority: int = 1):
    """Add a new task"""
    typer.echo(f"Added: {title}")

# vs Click approach (more verbose)
import click

@click.command()
@click.argument('title')
@click.option('--priority', default=1)
def add(title, priority):
    """Add a new task"""
    click.echo(f"Added: {title}")
```

**Alternatives Considered:**
- **Click**: More mature but more boilerplate code
- **argparse**: Standard library but verbose and less intuitive
- **docopt**: Interesting but less active maintenance

**Decision:** Use Typer for cleaner code and better developer experience.

### Storage Mechanism: JSON File

**Rationale:**

**JSON file storage** is the best fit for this simple use case:

**Advantages:**
- **No Setup**: Works immediately without database installation
- **Human Readable**: Can inspect/edit with any text editor
- **Portable**: Single file can be backed up/shared easily
- **Standard Library**: No external dependencies (uses `json` module)
- **Sufficient Performance**: Fast for typical daily task volume (< 1000 tasks)
- **Version Control Friendly**: Can track in Git if desired
- **Simple Backups**: Just copy the file

**Trade-offs:**
- Not suitable for concurrent multi-user access (acceptable for single-user CLI)
- Linear search performance (acceptable for small datasets)
- Manual data migrations if schema changes (acceptable for simple structure)

**Alternatives Considered:**
- **SQLite**: More complex, overkill for simple task tracking, requires SQL knowledge
- **CSV**: Less flexible for nested data structures
- **YAML**: Requires external dependency (PyYAML), not standard library
- **Pickle**: Not human-readable, security concerns

**Data File Location:**
- Default: `~/.task-tracker/tasks.json`
- Configurable via environment variable: `TASK_TRACKER_DATA_FILE`
- Auto-creates directory and file on first run

**Performance Characteristics:**
- Read operation: O(1) - load entire file
- Write operation: O(n) - serialize all tasks
- Search operation: O(n) - linear scan
- Expected volume: 50-500 tasks (< 50KB file size)
- Load time: < 10ms for typical usage

---

## Command Structure and Usage

### Command Overview

```bash
task-tracker [COMMAND] [OPTIONS] [ARGUMENTS]
```

### 1. Add Task

**Command:**
```bash
task add "Implement user authentication"
```

**Output:**
```
✓ Task added successfully!
  ID: 1
  Title: Implement user authentication
  Status: pending
  Created: 2025-10-01 14:30:00
```

**Options:**
- None (future: could add `--priority`, `--due-date`)

**Behavior:**
- Auto-generates sequential ID
- Sets status to "pending" by default
- Records current timestamp
- Validates title is not empty (1-200 characters)

### 2. List Tasks

**Command:**
```bash
task list
task list --status pending
task list --all
```

**Output:**
```
Pending Tasks (2):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID  Title                          Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1   Implement user authentication  2025-10-01 14:30
2   Write API documentation        2025-10-01 15:45
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Options:**
- `--status [pending|completed]`: Filter by status (default: pending)
- `--all`: Show all tasks regardless of status
- `--limit N`: Show only first N tasks

**Behavior:**
- Default shows only pending tasks
- Sorts by creation date (newest first)
- Empty list shows helpful message: "No pending tasks! Add one with 'task add'"

### 3. Show Task Details

**Command:**
```bash
task show 1
```

**Output:**
```
Task #1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Title:      Implement user authentication
Status:     pending
Created:    2025-10-01 14:30:00
Completed:  -
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Arguments:**
- `task_id`: Required task ID (integer)

**Error Handling:**
```bash
task show 999
Error: Task #999 not found
```

### 4. Complete Task

**Command:**
```bash
task complete 1
```

**Output:**
```
✓ Task #1 marked as completed!
  Title: Implement user authentication
  Completed at: 2025-10-01 16:20:00
```

**Arguments:**
- `task_id`: Required task ID (integer)

**Behavior:**
- Changes status from "pending" to "completed"
- Records completion timestamp
- Error if task already completed (with option to skip via `--force`)

**Idempotency:**
```bash
task complete 1
Error: Task #1 is already completed
      Use --force to update completion time
```

### 5. Delete Task

**Command:**
```bash
task delete 1
task delete 1 --force  # Skip confirmation
```

**Output:**
```
Are you sure you want to delete task #1? [y/N]: y
✓ Task #1 deleted successfully!
```

**Arguments:**
- `task_id`: Required task ID (integer)

**Options:**
- `--force`, `-f`: Skip confirmation prompt

**Behavior:**
- Prompts for confirmation by default
- Removes task permanently from storage
- No soft-delete or archive (keep it simple)

### 6. Global Options

**Help:**
```bash
task --help
task add --help
```

**Version:**
```bash
task --version
# Output: task-tracker version 1.0.0
```

---

## Data Model Design

### Task Schema

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Task(BaseModel):
    """Single task representation"""
    id: int = Field(..., description="Auto-generated sequential ID")
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    status: str = Field(default="pending", pattern="^(pending|completed)$")
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = Field(default=None)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

### Storage Format

**File: ~/.task-tracker/tasks.json**

```json
{
  "version": "1.0.0",
  "last_id": 2,
  "tasks": [
    {
      "id": 1,
      "title": "Implement user authentication",
      "status": "completed",
      "created_at": "2025-10-01T14:30:00",
      "completed_at": "2025-10-01T16:20:00"
    },
    {
      "id": 2,
      "title": "Write API documentation",
      "status": "pending",
      "created_at": "2025-10-01T15:45:00",
      "completed_at": null
    }
  ]
}
```

**Schema Fields:**
- `version`: Storage format version for future migrations
- `last_id`: Counter for auto-incrementing task IDs
- `tasks`: Array of task objects

**Data Validation:**
- Pydantic models validate all data on read/write
- Invalid JSON triggers helpful error message with recovery suggestion
- Automatic backup before destructive operations (write/delete)

---

## File Structure and Module Organization

### Project Structure

```
task-tracker/
├── pyproject.toml              # Poetry/pip package configuration
├── README.md                   # Installation and usage guide
├── LICENSE                     # MIT License
├── .gitignore
├── task_tracker/
│   ├── __init__.py
│   ├── __main__.py            # Entry point: python -m task_tracker
│   ├── cli.py                 # Typer CLI commands
│   ├── models.py              # Pydantic data models
│   ├── storage.py             # JSON file operations
│   ├── config.py              # Configuration management
│   └── utils.py               # Helper functions (formatting, colors)
└── tests/
    ├── __init__.py
    ├── test_cli.py
    ├── test_storage.py
    ├── test_models.py
    └── fixtures/
        └── sample_tasks.json
```

### Module Responsibilities

#### 1. `cli.py` - Command Interface

```python
"""
CLI command definitions using Typer.
Handles user input, calls storage operations, formats output.
"""

import typer
from rich.console import Console
from task_tracker.storage import TaskStorage
from task_tracker.models import Task

app = typer.Typer(help="Simple task tracker for daily tasks")
console = Console()
storage = TaskStorage()

@app.command()
def add(title: str):
    """Add a new task"""
    task = storage.create_task(title)
    console.print(f"✓ Task added: {task.title}", style="green")

@app.command()
def list(
    status: str = typer.Option("pending", help="Filter by status"),
    all: bool = typer.Option(False, help="Show all tasks")
):
    """List tasks"""
    # Implementation...

# Additional commands...
```

**Responsibilities:**
- Define CLI commands and options
- Parse user input
- Call storage layer for data operations
- Format and display output using Rich
- Handle user confirmations
- Display error messages

#### 2. `storage.py` - Data Persistence

```python
"""
JSON file storage operations.
Handles reading, writing, and querying tasks.
"""

import json
from pathlib import Path
from typing import List, Optional
from task_tracker.models import Task, TaskCollection
from task_tracker.config import get_data_file_path

class TaskStorage:
    """Manages task persistence in JSON file"""

    def __init__(self, data_file: Optional[Path] = None):
        self.data_file = data_file or get_data_file_path()
        self._ensure_file_exists()

    def create_task(self, title: str) -> Task:
        """Create and save a new task"""
        collection = self._load()
        task = Task(id=collection.last_id + 1, title=title)
        collection.tasks.append(task)
        collection.last_id = task.id
        self._save(collection)
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve task by ID"""
        # Implementation...

    def list_tasks(self, status: Optional[str] = None) -> List[Task]:
        """List tasks with optional status filter"""
        # Implementation...

    def update_task(self, task_id: int, **updates) -> Task:
        """Update task fields"""
        # Implementation...

    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID"""
        # Implementation...

    def _load(self) -> TaskCollection:
        """Load tasks from JSON file"""
        with open(self.data_file, 'r') as f:
            data = json.load(f)
        return TaskCollection(**data)

    def _save(self, collection: TaskCollection):
        """Save tasks to JSON file with atomic write"""
        # Write to temp file, then rename (atomic operation)
        temp_file = self.data_file.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            json.dump(collection.dict(), f, indent=2, default=str)
        temp_file.replace(self.data_file)

    def _ensure_file_exists(self):
        """Create data file if it doesn't exist"""
        if not self.data_file.exists():
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            initial_data = TaskCollection(version="1.0.0", last_id=0, tasks=[])
            self._save(initial_data)
```

**Responsibilities:**
- Read/write JSON data file
- Manage task CRUD operations
- Handle file locking (basic)
- Ensure atomic writes (temp file + rename)
- Auto-create data directory
- Validate data with Pydantic

**Error Handling:**
- Corrupted JSON: Display error, suggest backup restoration
- File permission issues: Clear error message with fix suggestion
- Disk full: Graceful failure message

#### 3. `models.py` - Data Models

```python
"""
Pydantic models for type-safe data handling.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class Task(BaseModel):
    """Individual task"""
    id: int
    title: str = Field(..., min_length=1, max_length=200)
    status: str = Field(default="pending", pattern="^(pending|completed)$")
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def mark_completed(self):
        """Mark task as completed"""
        self.status = "completed"
        self.completed_at = datetime.now()

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class TaskCollection(BaseModel):
    """Container for all tasks"""
    version: str = "1.0.0"
    last_id: int = 0
    tasks: List[Task] = []
```

**Responsibilities:**
- Define data structure
- Validate field values
- Provide helper methods (mark_completed)
- Handle JSON serialization

#### 4. `config.py` - Configuration

```python
"""
Application configuration and environment variables.
"""

import os
from pathlib import Path

def get_data_file_path() -> Path:
    """Get path to tasks.json file"""
    custom_path = os.getenv("TASK_TRACKER_DATA_FILE")
    if custom_path:
        return Path(custom_path)

    # Default: ~/.task-tracker/tasks.json
    home = Path.home()
    return home / ".task-tracker" / "tasks.json"

def get_config():
    """Get application configuration"""
    return {
        "data_file": get_data_file_path(),
        "backup_enabled": os.getenv("TASK_TRACKER_BACKUP", "true").lower() == "true",
        "max_title_length": 200,
    }
```

**Responsibilities:**
- Read environment variables
- Provide default values
- Centralize configuration

#### 5. `utils.py` - Helper Functions

```python
"""
Utility functions for formatting and display.
"""

from datetime import datetime
from rich.table import Table
from rich.console import Console

def format_datetime(dt: datetime) -> str:
    """Format datetime for display"""
    return dt.strftime("%Y-%m-%d %H:%M")

def create_task_table(tasks: List[Task]) -> Table:
    """Create Rich table for task list"""
    table = Table(title="Tasks")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Status", style="yellow")
    table.add_column("Created", style="green")

    for task in tasks:
        table.add_row(
            str(task.id),
            task.title,
            task.status,
            format_datetime(task.created_at)
        )

    return table
```

**Responsibilities:**
- Format dates/times
- Create Rich UI components
- Provide reusable display functions

#### 6. `__main__.py` - Entry Point

```python
"""
Entry point for python -m task_tracker
"""

from task_tracker.cli import app

if __name__ == "__main__":
    app()
```

---

## Implementation Guidance for Coder Agent

### Phase 1: Project Setup (15 minutes)

**Step 1:** Initialize project structure
```bash
mkdir -p task-tracker/task_tracker
mkdir -p task-tracker/tests/fixtures
cd task-tracker
```

**Step 2:** Create `pyproject.toml`
```toml
[tool.poetry]
name = "task-tracker"
version = "1.0.0"
description = "Simple CLI task tracker for daily tasks"
authors = ["Your Name <you@example.com>"]
license = "MIT"
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.9"
typer = {extras = ["all"], version = "^0.9.0"}
pydantic = "^2.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
black = "^23.7.0"
ruff = "^0.0.285"

[tool.poetry.scripts]
task = "task_tracker.cli:app"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

**Step 3:** Install dependencies
```bash
poetry install
```

### Phase 2: Core Implementation (45 minutes)

**Order of Implementation:**

1. **models.py** (10 min)
   - Define Task and TaskCollection models
   - Add validation rules
   - Test model creation and serialization

2. **config.py** (5 min)
   - Implement get_data_file_path()
   - Add environment variable support

3. **storage.py** (20 min)
   - Implement TaskStorage class
   - Add CRUD methods
   - Test file operations
   - Ensure atomic writes

4. **utils.py** (5 min)
   - Add formatting functions
   - Create table display helpers

5. **cli.py** (15 min)
   - Implement all commands
   - Add Rich formatting
   - Test CLI interaction

### Phase 3: Testing (30 minutes)

**Test Coverage Targets:**
- models.py: 100% (simple validation tests)
- storage.py: 95% (test all CRUD operations)
- cli.py: 80% (test command logic, mock storage)

**Key Test Cases:**

```python
# tests/test_storage.py
def test_create_task(tmp_path):
    """Test task creation"""
    storage = TaskStorage(tmp_path / "tasks.json")
    task = storage.create_task("Test task")
    assert task.id == 1
    assert task.title == "Test task"
    assert task.status == "pending"

def test_complete_task(storage_with_tasks):
    """Test marking task as completed"""
    storage = storage_with_tasks
    task = storage.update_task(1, status="completed")
    assert task.status == "completed"
    assert task.completed_at is not None

def test_list_tasks_filter_by_status(storage_with_tasks):
    """Test filtering tasks by status"""
    storage = storage_with_tasks
    pending = storage.list_tasks(status="pending")
    assert all(t.status == "pending" for t in pending)
```

### Phase 4: Documentation (15 minutes)

**README.md Structure:**
```markdown
# Task Tracker

Simple CLI tool for tracking daily tasks.

## Installation

pip install task-tracker

## Quick Start

# Add a task
task add "Implement feature X"

# List pending tasks
task list

# Complete a task
task complete 1

# Show task details
task show 1

# Delete a task
task delete 1

## Configuration

Environment Variables:
- TASK_TRACKER_DATA_FILE: Custom location for tasks.json

## Development

poetry install
pytest
```

### Common Implementation Pitfalls to Avoid

1. **File Locking**: Use atomic writes (temp file + rename), not file locks
2. **Date Serialization**: Use Pydantic's json_encoders for datetime
3. **Error Messages**: Make them actionable ("Task not found. Use 'task list' to see all tasks")
4. **ID Generation**: Use counter in TaskCollection, not max(task.id)
5. **Empty State**: Handle empty task list gracefully with helpful message

### Future Enhancement Hooks

**Easy additions (don't implement now, but structure code to support):**

1. **Priority Levels**: Add `priority: int` field to Task model
2. **Due Dates**: Add `due_date: Optional[datetime]` field
3. **Tags**: Add `tags: List[str]` field
4. **Search**: Add `task search <query>` command
5. **Statistics**: Add `task stats` command (count pending/completed)
6. **Export**: Add `task export --format json|csv` command
7. **Undo**: Keep backup of previous state in storage
8. **Recurring Tasks**: Add `recurrence: Optional[str]` field

**Code Structure for Extensions:**
- Keep storage.py methods generic (update_task accepts **kwargs)
- Use Pydantic's flexibility for adding optional fields
- CLI commands are independent, easy to add new ones

---

## Decision

**We will implement the CLI task tracker using:**

1. **CLI Framework**: Typer (with Rich for formatting)
2. **Storage**: JSON file in `~/.task-tracker/tasks.json`
3. **Data Validation**: Pydantic models
4. **Python Version**: 3.9+ (for modern type hints)
5. **Package Management**: Poetry (or pip for simpler deployments)
6. **Dependencies**: Only typer[all] and pydantic (2 external packages)

### Success Metrics

**User Experience:**
- Commands execute in < 100ms
- Zero configuration required
- Help text is clear and actionable
- Error messages suggest solutions

**Code Quality:**
- Test coverage > 85%
- All functions type-annotated
- No Ruff/Black violations
- Clear module boundaries

**Reliability:**
- No data loss from concurrent operations
- Atomic file writes
- Graceful error handling
- Data file is human-readable

---

## Consequences

### Positive

1. **Immediate Usability**: Works without any setup or configuration
2. **Portable**: Single JSON file can be backed up, version controlled
3. **Inspectable**: Users can manually view/edit tasks.json if needed
4. **Simple Codebase**: < 300 lines of code, easy to maintain
5. **Type Safe**: Pydantic catches data errors early
6. **Great UX**: Rich library provides beautiful terminal output
7. **Extensible**: Easy to add new commands and fields

### Negative

1. **Single User Only**: No multi-user or concurrent access support
2. **No Advanced Queries**: Linear search only (acceptable for < 1000 tasks)
3. **Manual Backups**: No automatic backup mechanism (could add later)
4. **Limited Undo**: No built-in undo functionality

### Trade-offs Made

**Simplicity vs. Features:**
- **Chose**: JSON file over SQLite
- **Rationale**: 90% of users will have < 200 tasks, JSON is sufficient
- **Cost**: Slower for large datasets, no complex queries
- **Benefit**: Zero setup, human-readable, portable

**CLI Library:**
- **Chose**: Typer over Click
- **Rationale**: Less boilerplate, modern type hints, better defaults
- **Cost**: Slightly newer library (less Stack Overflow answers)
- **Benefit**: Cleaner code, better development experience

**Validation:**
- **Chose**: Pydantic over manual validation
- **Rationale**: Safer, automatic error messages, easier to extend
- **Cost**: One additional dependency
- **Benefit**: Type safety, better error messages, less code

### Risks and Mitigation

**Risk:** JSON file corruption
- **Mitigation**: Atomic writes, backup before destructive operations, Pydantic validation

**Risk:** Users exceed 1000 tasks (performance degradation)
- **Mitigation**: Add warning message, suggest archiving old tasks, future migration to SQLite

**Risk:** Concurrent access (two terminals running `task` simultaneously)
- **Mitigation**: Use atomic writes, document single-user limitation, add file lock in v2 if needed

**Risk:** Data file in home directory conflicts with dotfile conventions
- **Mitigation**: Use `~/.task-tracker/` subdirectory, allow override via environment variable

---

## References

1. Typer Documentation (https://typer.tiangolo.com)
2. Rich Documentation (https://rich.readthedocs.io)
3. Pydantic Documentation (https://docs.pydantic.dev)
4. Click vs Typer Comparison (https://typer.tiangolo.com/alternatives/)
5. The Twelve-Factor App - Configuration (https://12factor.net/config)
6. UNIX Philosophy - Do One Thing Well

---

## Appendix: Example Usage Session

```bash
# First run - no tasks
$ task list
No pending tasks! Add one with 'task add "Your task here"'

# Add some tasks
$ task add "Implement CLI task tracker"
✓ Task added successfully!
  ID: 1
  Title: Implement CLI task tracker
  Status: pending
  Created: 2025-10-01 14:30:00

$ task add "Write documentation"
✓ Task added successfully!
  ID: 2
  Title: Write documentation

$ task add "Deploy to PyPI"
✓ Task added successfully!
  ID: 3
  Title: Deploy to PyPI

# List tasks
$ task list
Pending Tasks (3):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID  Title                        Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3   Deploy to PyPI               2025-10-01 15:00
2   Write documentation          2025-10-01 14:50
1   Implement CLI task tracker   2025-10-01 14:30
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Show details
$ task show 1
Task #1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Title:      Implement CLI task tracker
Status:     pending
Created:    2025-10-01 14:30:00
Completed:  -
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Complete a task
$ task complete 1
✓ Task #1 marked as completed!
  Title: Implement CLI task tracker
  Completed at: 2025-10-01 16:20:00

# List only pending
$ task list
Pending Tasks (2):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID  Title                   Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3   Deploy to PyPI          2025-10-01 15:00
2   Write documentation     2025-10-01 14:50
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# List all tasks
$ task list --all
All Tasks (3):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID  Title                        Status      Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3   Deploy to PyPI               pending     2025-10-01 15:00
2   Write documentation          pending     2025-10-01 14:50
1   Implement CLI task tracker   completed   2025-10-01 14:30
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Delete a task
$ task delete 3
Are you sure you want to delete task #3? [y/N]: y
✓ Task #3 deleted successfully!

# Error handling
$ task show 999
Error: Task #999 not found
       Use 'task list --all' to see all tasks

$ task complete 1
Error: Task #1 is already completed
       Use --force to update completion time
```

---

**Author:** Architecture Team
**Review Status:** Pending Review
**Last Updated:** 2025-10-01
