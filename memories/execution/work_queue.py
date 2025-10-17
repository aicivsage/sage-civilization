#!/usr/bin/env python3
"""
Work Queue System - Foundation (ADR-005 Phase 1)

A JSONL-based work queue for continuous execution system.
Enables priority-based task scheduling with dependency tracking.

Features:
- JSONL atomic operations (append-only writes)
- Priority-based task ordering
- Dependency tracking
- Atomic task updates
- Queue compaction for maintenance

Usage:
    from work_queue import enqueue_task, get_next_task, update_task

    # Enqueue a new task
    task = WorkQueueTask(
        id="task-001",
        priority=PRIORITY_HIGH,
        type="user_delegation",
        action="implement_feature",
        params={"feature": "work_queue"},
        status="pending",
        created_at=datetime.utcnow().isoformat(),
        dependencies=[]
    )
    enqueue_task(task)

    # Get next executable task
    next_task = get_next_task()

    # Update task status
    update_task("task-001", {"status": "in_progress", "started_at": datetime.utcnow().isoformat()})
"""

import json
import os
import fcntl
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

# Priority levels (higher number = higher priority)
PRIORITY_CRITICAL = 100      # Constitutional compliance, safety issues
PRIORITY_URGENT = 80         # User delegation, blocked agents
PRIORITY_HIGH = 60           # Flow execution, integration work
PRIORITY_NORMAL = 40         # Standard agent tasks
PRIORITY_LOW = 20            # Optimization, refactoring
PRIORITY_MAINTENANCE = 10    # Queue cleanup, logging

# Task types
TYPE_CONSTITUTIONAL = "constitutional"
TYPE_USER_DELEGATION = "user_delegation"
TYPE_FLOW_EXECUTION = "flow_execution"
TYPE_AGENT_ESCALATION = "agent_escalation"

# Task statuses
STATUS_PENDING = "pending"
STATUS_IN_PROGRESS = "in_progress"
STATUS_BLOCKED = "blocked"
STATUS_COMPLETE = "complete"
STATUS_FAILED = "failed"

# File paths
QUEUE_FILE = Path(__file__).parent / "work_queue.jsonl"


@contextmanager
def file_lock(lock_path: Path):
    """Context manager for file locking using fcntl."""
    lock_file = open(lock_path, 'w')
    try:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
        lock_file.close()


@dataclass
class WorkQueueTask:
    """
    Work queue task schema.

    Attributes:
        id: Unique task identifier (e.g., "task-001", "flow-startup-20251005")
        priority: Priority level (use PRIORITY_* constants)
        type: Task type (constitutional|user_delegation|flow_execution|agent_escalation)
        action: Action to perform (e.g., "implement_feature", "run_flow", "send_email")
        params: Action-specific parameters as dict
        status: Current status (pending|in_progress|blocked|complete|failed)
        created_at: ISO 8601 timestamp of task creation
        dependencies: List of task IDs that must complete before this task
        agent: Agent assigned to this task (optional)
        started_at: ISO 8601 timestamp when task started (optional)
        completed_at: ISO 8601 timestamp when task completed (optional)
        result: Task result data (optional)
        blocker: Description of what's blocking this task (optional)
        retry_count: Number of retry attempts (default: 0)
        max_retries: Maximum retry attempts before marking failed (default: 3)
    """
    id: str
    priority: int
    type: str
    action: str
    params: Dict[str, Any]
    status: str
    created_at: str
    dependencies: List[str] = field(default_factory=list)
    agent: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    blocker: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkQueueTask':
        """Create task from dictionary."""
        return cls(**data)


def _ensure_queue_exists():
    """Ensure queue file and parent directory exist."""
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not QUEUE_FILE.exists():
        QUEUE_FILE.touch()


def enqueue_task(task: WorkQueueTask) -> None:
    """
    Enqueue a task to the work queue.

    Atomically appends task to JSONL file using file locking.

    Args:
        task: WorkQueueTask to enqueue

    Example:
        task = WorkQueueTask(
            id="task-001",
            priority=PRIORITY_HIGH,
            type="user_delegation",
            action="implement_feature",
            params={"feature": "work_queue"},
            status="pending",
            created_at=datetime.utcnow().isoformat(),
            dependencies=[]
        )
        enqueue_task(task)
    """
    _ensure_queue_exists()

    lock_path = QUEUE_FILE.with_suffix('.lock')
    with file_lock(lock_path):
        with open(QUEUE_FILE, 'a') as f:
            json.dump(task.to_dict(), f)
            f.write('\n')


def read_all_tasks() -> List[WorkQueueTask]:
    """
    Read all tasks from the work queue.

    Returns:
        List of WorkQueueTask objects

    Example:
        tasks = read_all_tasks()
        for task in tasks:
            print(f"Task {task.id}: {task.status}")
    """
    _ensure_queue_exists()

    tasks = []
    lock_path = QUEUE_FILE.with_suffix('.lock')
    with file_lock(lock_path):
        with open(QUEUE_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        task_dict = json.loads(line)
                        tasks.append(WorkQueueTask.from_dict(task_dict))
                    except json.JSONDecodeError as e:
                        print(f"Warning: Skipping malformed line: {e}")
                        continue

    return tasks


def dependencies_met(task: WorkQueueTask, all_tasks: List[WorkQueueTask]) -> bool:
    """
    Check if all dependencies for a task are met.

    A dependency is met if the dependent task has status 'complete'.

    Args:
        task: Task to check dependencies for
        all_tasks: List of all tasks in the queue

    Returns:
        True if all dependencies are complete, False otherwise

    Example:
        tasks = read_all_tasks()
        task = tasks[0]
        if dependencies_met(task, tasks):
            print("Task is ready to execute")
    """
    if not task.dependencies:
        return True

    # Build task ID -> status map
    task_status = {t.id: t.status for t in all_tasks}

    # Check all dependencies are complete
    for dep_id in task.dependencies:
        if dep_id not in task_status:
            return False  # Dependency not found
        if task_status[dep_id] != STATUS_COMPLETE:
            return False  # Dependency not complete

    return True


def get_next_task() -> Optional[WorkQueueTask]:
    """
    Get the next executable task from the queue.

    Returns the highest priority pending task whose dependencies are met.

    Returns:
        Next executable WorkQueueTask, or None if no tasks available

    Example:
        next_task = get_next_task()
        if next_task:
            print(f"Executing: {next_task.action}")
            update_task(next_task.id, {
                "status": "in_progress",
                "started_at": datetime.utcnow().isoformat()
            })
    """
    all_tasks = read_all_tasks()

    # Filter pending tasks with dependencies met
    executable_tasks = [
        task for task in all_tasks
        if task.status == STATUS_PENDING and dependencies_met(task, all_tasks)
    ]

    if not executable_tasks:
        return None

    # Sort by priority (descending) and created_at (ascending)
    executable_tasks.sort(
        key=lambda t: (-t.priority, t.created_at)
    )

    return executable_tasks[0]


def update_task(task_id: str, updates: Dict[str, Any]) -> bool:
    """
    Update a task in the queue.

    Atomically rewrites the entire JSONL file with updated task.

    Args:
        task_id: ID of task to update
        updates: Dictionary of fields to update

    Returns:
        True if task was found and updated, False otherwise

    Example:
        # Mark task as in progress
        update_task("task-001", {
            "status": "in_progress",
            "started_at": datetime.utcnow().isoformat(),
            "agent": "coder"
        })

        # Mark task as complete
        update_task("task-001", {
            "status": "complete",
            "completed_at": datetime.utcnow().isoformat(),
            "result": {"lines_of_code": 250}
        })
    """
    _ensure_queue_exists()

    lock_path = QUEUE_FILE.with_suffix('.lock')
    with file_lock(lock_path):
        # Read tasks directly to avoid nested locking
        tasks = []
        with open(QUEUE_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        task_dict = json.loads(line)
                        tasks.append(WorkQueueTask.from_dict(task_dict))
                    except json.JSONDecodeError:
                        continue

        # Find and update task
        task_found = False
        for task in tasks:
            if task.id == task_id:
                # Update task attributes
                for key, value in updates.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                task_found = True
                break

        if not task_found:
            return False

        # Rewrite entire file atomically
        temp_file = QUEUE_FILE.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            for task in tasks:
                json.dump(task.to_dict(), f)
                f.write('\n')

        # Atomic replace
        temp_file.replace(QUEUE_FILE)

    return True


def compact_queue(days: int = 7) -> int:
    """
    Remove old completed tasks from the queue.

    Removes tasks with status 'complete' or 'failed' that completed
    more than 'days' ago.

    Args:
        days: Number of days to retain completed tasks (default: 7)

    Returns:
        Number of tasks removed

    Example:
        # Remove tasks completed over 7 days ago
        removed = compact_queue(days=7)
        print(f"Removed {removed} old tasks")
    """
    _ensure_queue_exists()

    cutoff = datetime.utcnow() - timedelta(days=days)

    lock_path = QUEUE_FILE.with_suffix('.lock')
    with file_lock(lock_path):
        # Read tasks directly to avoid nested locking
        tasks = []
        with open(QUEUE_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        task_dict = json.loads(line)
                        tasks.append(WorkQueueTask.from_dict(task_dict))
                    except json.JSONDecodeError:
                        continue

        # Filter tasks to keep
        tasks_to_keep = []
        removed_count = 0

        for task in tasks:
            # Keep pending, in_progress, or blocked tasks
            if task.status in [STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_BLOCKED]:
                tasks_to_keep.append(task)
                continue

            # Keep recent completed/failed tasks
            if task.status in [STATUS_COMPLETE, STATUS_FAILED]:
                if task.completed_at:
                    try:
                        completed_time = datetime.fromisoformat(task.completed_at.replace('Z', '+00:00'))
                        if completed_time > cutoff:
                            tasks_to_keep.append(task)
                        else:
                            removed_count += 1
                    except (ValueError, AttributeError):
                        # Keep task if timestamp is invalid
                        tasks_to_keep.append(task)
                else:
                    # Keep task if no completion timestamp
                    tasks_to_keep.append(task)

        # Rewrite file with kept tasks only
        temp_file = QUEUE_FILE.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            for task in tasks_to_keep:
                json.dump(task.to_dict(), f)
                f.write('\n')

        temp_file.replace(QUEUE_FILE)

    return removed_count


def get_queue_stats() -> Dict[str, Any]:
    """
    Get statistics about the current queue.

    Returns:
        Dictionary with queue statistics:
        - total: Total number of tasks
        - pending: Number of pending tasks
        - in_progress: Number of in-progress tasks
        - blocked: Number of blocked tasks
        - complete: Number of complete tasks
        - failed: Number of failed tasks
        - by_priority: Count of tasks by priority level

    Example:
        stats = get_queue_stats()
        print(f"Queue has {stats['pending']} pending tasks")
    """
    tasks = read_all_tasks()

    stats = {
        "total": len(tasks),
        "pending": 0,
        "in_progress": 0,
        "blocked": 0,
        "complete": 0,
        "failed": 0,
        "by_priority": {}
    }

    for task in tasks:
        # Count by status
        if task.status == STATUS_PENDING:
            stats["pending"] += 1
        elif task.status == STATUS_IN_PROGRESS:
            stats["in_progress"] += 1
        elif task.status == STATUS_BLOCKED:
            stats["blocked"] += 1
        elif task.status == STATUS_COMPLETE:
            stats["complete"] += 1
        elif task.status == STATUS_FAILED:
            stats["failed"] += 1

        # Count by priority
        priority_name = f"priority_{task.priority}"
        stats["by_priority"][priority_name] = stats["by_priority"].get(priority_name, 0) + 1

    return stats


if __name__ == "__main__":
    print("Work Queue System - Basic Test\n")

    # Test 1: Enqueue tasks
    print("1. Enqueueing test tasks...")

    task1 = WorkQueueTask(
        id="test-001",
        priority=PRIORITY_HIGH,
        type=TYPE_USER_DELEGATION,
        action="implement_feature",
        params={"feature": "work_queue"},
        status=STATUS_PENDING,
        created_at=datetime.utcnow().isoformat(),
        dependencies=[]
    )
    enqueue_task(task1)

    task2 = WorkQueueTask(
        id="test-002",
        priority=PRIORITY_NORMAL,
        type=TYPE_FLOW_EXECUTION,
        action="run_tests",
        params={"test_suite": "unit"},
        status=STATUS_PENDING,
        created_at=datetime.utcnow().isoformat(),
        dependencies=["test-001"]  # Depends on task1
    )
    enqueue_task(task2)

    task3 = WorkQueueTask(
        id="test-003",
        priority=PRIORITY_CRITICAL,
        type=TYPE_CONSTITUTIONAL,
        action="verify_compliance",
        params={"check": "safety"},
        status=STATUS_PENDING,
        created_at=datetime.utcnow().isoformat(),
        dependencies=[]
    )
    enqueue_task(task3)

    print("   Enqueued 3 tasks\n")

    # Test 2: Read all tasks
    print("2. Reading all tasks...")
    all_tasks = read_all_tasks()
    print(f"   Found {len(all_tasks)} tasks\n")

    # Test 3: Get next task (should be task3 - highest priority)
    print("3. Getting next executable task...")
    next_task = get_next_task()
    if next_task:
        print(f"   Next task: {next_task.id} (priority={next_task.priority}, action={next_task.action})")
        print(f"   Expected: test-003 (CRITICAL priority)\n")

    # Test 4: Update task
    print("4. Marking task as in progress...")
    update_task(next_task.id, {
        "status": STATUS_IN_PROGRESS,
        "started_at": datetime.utcnow().isoformat(),
        "agent": "coder"
    })
    print(f"   Updated {next_task.id}\n")

    # Test 5: Get next task (should be task1 now)
    print("5. Getting next task after update...")
    next_task = get_next_task()
    if next_task:
        print(f"   Next task: {next_task.id} (priority={next_task.priority})")
        print(f"   Expected: test-001 (HIGH priority, test-003 is in_progress)\n")

    # Test 6: Complete task1 to unblock task2
    print("6. Completing test-001 to unblock test-002...")
    update_task("test-001", {
        "status": STATUS_COMPLETE,
        "completed_at": datetime.utcnow().isoformat()
    })
    print("   Completed test-001\n")

    # Test 7: Get next task (should be task2 now - dependency met)
    print("7. Getting next task after dependency met...")
    next_task = get_next_task()
    if next_task:
        print(f"   Next task: {next_task.id}")
        print(f"   Expected: test-002 (dependency test-001 is complete)\n")

    # Test 8: Queue stats
    print("8. Queue statistics:")
    stats = get_queue_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")

    print("\nBasic test complete!")
    print(f"Queue file: {QUEUE_FILE}")
