#!/usr/bin/env python3
"""
Work Queue System - Usage Examples

Demonstrates how to use the work queue system for continuous execution.
"""

from datetime import datetime
from work_queue import (
    WorkQueueTask,
    enqueue_task,
    get_next_task,
    update_task,
    get_queue_stats,
    compact_queue,
    PRIORITY_CRITICAL,
    PRIORITY_URGENT,
    PRIORITY_HIGH,
    PRIORITY_NORMAL,
    TYPE_USER_DELEGATION,
    TYPE_FLOW_EXECUTION,
    TYPE_CONSTITUTIONAL,
    STATUS_PENDING,
    STATUS_IN_PROGRESS,
    STATUS_COMPLETE,
    STATUS_FAILED,
)


def example_1_enqueue_simple_task():
    """Example 1: Enqueue a simple task."""
    print("\n=== Example 1: Enqueue Simple Task ===")

    task = WorkQueueTask(
        id="email-001",
        priority=PRIORITY_URGENT,
        type=TYPE_USER_DELEGATION,
        action="send_email",
        params={
            "to": "coreycmusic@gmail.com",
            "subject": "Work Queue Test",
            "body": "Testing the work queue system"
        },
        status=STATUS_PENDING,
        created_at=datetime.utcnow().isoformat(),
        dependencies=[]
    )

    enqueue_task(task)
    print(f"Enqueued task: {task.id}")
    print(f"Priority: {task.priority}")
    print(f"Action: {task.action}")


def example_2_task_with_dependencies():
    """Example 2: Create task chain with dependencies."""
    print("\n=== Example 2: Task Chain with Dependencies ===")

    # Task 1: Implement feature
    task1 = WorkQueueTask(
        id="impl-feature-001",
        priority=PRIORITY_HIGH,
        type=TYPE_USER_DELEGATION,
        action="implement_feature",
        params={"feature": "work_queue", "module": "execution"},
        status=STATUS_PENDING,
        created_at=datetime.utcnow().isoformat(),
        dependencies=[]
    )
    enqueue_task(task1)

    # Task 2: Write tests (depends on task 1)
    task2 = WorkQueueTask(
        id="test-feature-001",
        priority=PRIORITY_HIGH,
        type=TYPE_USER_DELEGATION,
        action="write_tests",
        params={"feature": "work_queue", "coverage": 80},
        status=STATUS_PENDING,
        created_at=datetime.utcnow().isoformat(),
        dependencies=["impl-feature-001"]  # Depends on implementation
    )
    enqueue_task(task2)

    # Task 3: Deploy (depends on task 2)
    task3 = WorkQueueTask(
        id="deploy-feature-001",
        priority=PRIORITY_NORMAL,
        type=TYPE_FLOW_EXECUTION,
        action="deploy",
        params={"environment": "production"},
        status=STATUS_PENDING,
        created_at=datetime.utcnow().isoformat(),
        dependencies=["test-feature-001"]  # Depends on tests
    )
    enqueue_task(task3)

    print("Enqueued 3-task chain:")
    print(f"  1. {task1.id} (no dependencies)")
    print(f"  2. {task2.id} (depends on {task1.id})")
    print(f"  3. {task3.id} (depends on {task2.id})")


def example_3_execute_tasks():
    """Example 3: Execute tasks from the queue."""
    print("\n=== Example 3: Execute Tasks ===")

    # Get next executable task
    next_task = get_next_task()

    if not next_task:
        print("No executable tasks in queue")
        return

    print(f"Next task to execute: {next_task.id}")
    print(f"  Priority: {next_task.priority}")
    print(f"  Action: {next_task.action}")
    print(f"  Params: {next_task.params}")

    # Mark task as in progress
    update_task(next_task.id, {
        "status": STATUS_IN_PROGRESS,
        "started_at": datetime.utcnow().isoformat(),
        "agent": "coder"
    })
    print(f"\nMarked {next_task.id} as in_progress")

    # Simulate work...
    print("Executing task...")

    # Mark task as complete
    update_task(next_task.id, {
        "status": STATUS_COMPLETE,
        "completed_at": datetime.utcnow().isoformat(),
        "result": {
            "success": True,
            "output": "Task completed successfully"
        }
    })
    print(f"Completed {next_task.id}")


def example_4_queue_statistics():
    """Example 4: Get queue statistics."""
    print("\n=== Example 4: Queue Statistics ===")

    stats = get_queue_stats()

    print(f"Total tasks: {stats['total']}")
    print(f"Pending: {stats['pending']}")
    print(f"In Progress: {stats['in_progress']}")
    print(f"Blocked: {stats['blocked']}")
    print(f"Complete: {stats['complete']}")
    print(f"Failed: {stats['failed']}")

    print("\nTasks by priority:")
    for priority, count in stats['by_priority'].items():
        print(f"  {priority}: {count}")


def example_5_constitutional_priority():
    """Example 5: High-priority constitutional task."""
    print("\n=== Example 5: Constitutional Task (Highest Priority) ===")

    task = WorkQueueTask(
        id="constitutional-001",
        priority=PRIORITY_CRITICAL,
        type=TYPE_CONSTITUTIONAL,
        action="verify_safety",
        params={
            "check_type": "file_deletion",
            "files": ["/important/file.txt"]
        },
        status=STATUS_PENDING,
        created_at=datetime.utcnow().isoformat(),
        dependencies=[]
    )

    enqueue_task(task)
    print(f"Enqueued CRITICAL constitutional task: {task.id}")
    print("This task will be executed before all other pending tasks")


def example_6_maintenance():
    """Example 6: Queue maintenance - compact old tasks."""
    print("\n=== Example 6: Queue Maintenance ===")

    # Compact queue - remove tasks completed over 7 days ago
    removed = compact_queue(days=7)
    print(f"Removed {removed} old completed tasks")


if __name__ == "__main__":
    print("Work Queue System - Usage Examples\n")
    print("=" * 60)

    # Run examples
    example_1_enqueue_simple_task()
    example_2_task_with_dependencies()
    example_3_execute_tasks()
    example_4_queue_statistics()
    example_5_constitutional_priority()
    example_6_maintenance()

    print("\n" + "=" * 60)
    print("Examples complete!")
    print("\nTo execute all pending tasks, use get_next_task() in a loop")
    print("until it returns None.")
