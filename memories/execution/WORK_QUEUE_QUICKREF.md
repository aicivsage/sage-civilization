# Work Queue System - Quick Reference

**Location**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/execution/work_queue.py`

## Import

```python
from memories.execution.work_queue import (
    WorkQueueTask,
    enqueue_task,
    get_next_task,
    update_task,
    get_queue_stats,
    compact_queue,
    # Priority levels
    PRIORITY_CRITICAL,    # 100 - Constitutional, safety
    PRIORITY_URGENT,      # 80  - User delegation, blocked agents
    PRIORITY_HIGH,        # 60  - Flow execution, integration
    PRIORITY_NORMAL,      # 40  - Standard agent tasks
    PRIORITY_LOW,         # 20  - Optimization, refactoring
    PRIORITY_MAINTENANCE, # 10  - Queue cleanup
    # Task types
    TYPE_CONSTITUTIONAL,
    TYPE_USER_DELEGATION,
    TYPE_FLOW_EXECUTION,
    TYPE_AGENT_ESCALATION,
    # Statuses
    STATUS_PENDING,
    STATUS_IN_PROGRESS,
    STATUS_BLOCKED,
    STATUS_COMPLETE,
    STATUS_FAILED
)
```

## Quick Start

### 1. Enqueue a Task

```python
from datetime import datetime

task = WorkQueueTask(
    id="unique-task-id",
    priority=PRIORITY_HIGH,
    type=TYPE_USER_DELEGATION,
    action="action_name",
    params={"key": "value"},
    status=STATUS_PENDING,
    created_at=datetime.utcnow().isoformat(),
    dependencies=[]  # Optional: list of task IDs
)

enqueue_task(task)
```

### 2. Get Next Task to Execute

```python
next_task = get_next_task()
if next_task:
    # Mark as in progress
    update_task(next_task.id, {
        "status": STATUS_IN_PROGRESS,
        "started_at": datetime.utcnow().isoformat(),
        "agent": "agent-name"
    })

    # ... execute task ...

    # Mark as complete
    update_task(next_task.id, {
        "status": STATUS_COMPLETE,
        "completed_at": datetime.utcnow().isoformat(),
        "result": {"output": "success"}
    })
```

### 3. Task with Dependencies

```python
# Task 1: No dependencies
task1 = WorkQueueTask(
    id="task-1",
    priority=PRIORITY_HIGH,
    type=TYPE_USER_DELEGATION,
    action="implement_feature",
    params={"feature": "work_queue"},
    status=STATUS_PENDING,
    created_at=datetime.utcnow().isoformat(),
    dependencies=[]
)
enqueue_task(task1)

# Task 2: Depends on task1
task2 = WorkQueueTask(
    id="task-2",
    priority=PRIORITY_NORMAL,
    type=TYPE_USER_DELEGATION,
    action="write_tests",
    params={"feature": "work_queue"},
    status=STATUS_PENDING,
    created_at=datetime.utcnow().isoformat(),
    dependencies=["task-1"]  # Won't execute until task-1 is complete
)
enqueue_task(task2)
```

### 4. Queue Statistics

```python
stats = get_queue_stats()
print(f"Pending: {stats['pending']}")
print(f"In Progress: {stats['in_progress']}")
print(f"Complete: {stats['complete']}")
```

### 5. Queue Maintenance

```python
# Remove tasks completed over 7 days ago
removed = compact_queue(days=7)
print(f"Removed {removed} old tasks")
```

## Priority Levels (Execution Order)

1. **PRIORITY_CRITICAL (100)** - Constitutional compliance, safety issues
2. **PRIORITY_URGENT (80)** - User delegation, blocked agents
3. **PRIORITY_HIGH (60)** - Flow execution, integration work
4. **PRIORITY_NORMAL (40)** - Standard agent tasks
5. **PRIORITY_LOW (20)** - Optimization, refactoring
6. **PRIORITY_MAINTENANCE (10)** - Queue cleanup, logging

## Task Types

- **TYPE_CONSTITUTIONAL** - Constitutional compliance checks
- **TYPE_USER_DELEGATION** - Direct user requests
- **TYPE_FLOW_EXECUTION** - Automated flow execution
- **TYPE_AGENT_ESCALATION** - Agent-to-agent escalations

## Task Lifecycle

```
pending → in_progress → complete
                    ↘ failed
                    ↘ blocked
```

## WorkQueueTask Schema

```python
@dataclass
class WorkQueueTask:
    id: str                          # Unique identifier
    priority: int                    # Use PRIORITY_* constants
    type: str                        # Use TYPE_* constants
    action: str                      # Action to perform
    params: Dict[str, Any]          # Action parameters
    status: str                      # Use STATUS_* constants
    created_at: str                  # ISO 8601 timestamp
    dependencies: List[str]          # List of task IDs (optional)
    agent: Optional[str]             # Agent assigned (optional)
    started_at: Optional[str]        # ISO 8601 timestamp (optional)
    completed_at: Optional[str]      # ISO 8601 timestamp (optional)
    result: Optional[Dict[str, Any]] # Result data (optional)
    blocker: Optional[str]           # Blocker description (optional)
    retry_count: int = 0             # Retry attempts
    max_retries: int = 3             # Max retry attempts
```

## Common Patterns

### Execute All Pending Tasks

```python
while True:
    task = get_next_task()
    if not task:
        break

    # Mark in progress
    update_task(task.id, {
        "status": STATUS_IN_PROGRESS,
        "started_at": datetime.utcnow().isoformat()
    })

    # Execute based on action
    try:
        if task.action == "send_email":
            # ... send email ...
            result = {"sent": True}
        elif task.action == "run_flow":
            # ... run flow ...
            result = {"flow": task.params["flow_name"]}

        # Mark complete
        update_task(task.id, {
            "status": STATUS_COMPLETE,
            "completed_at": datetime.utcnow().isoformat(),
            "result": result
        })
    except Exception as e:
        # Mark failed
        update_task(task.id, {
            "status": STATUS_FAILED,
            "completed_at": datetime.utcnow().isoformat(),
            "result": {"error": str(e)}
        })
```

### Handle Blocked Task

```python
# Mark task as blocked
update_task("task-id", {
    "status": STATUS_BLOCKED,
    "blocker": "Waiting for external API response"
})
```

### Retry Failed Task

```python
task = get_next_task()
if task and task.retry_count < task.max_retries:
    # Increment retry count
    update_task(task.id, {
        "retry_count": task.retry_count + 1,
        "status": STATUS_IN_PROGRESS
    })
    # ... retry execution ...
```

## File Locations

- **Queue Data**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/execution/work_queue.jsonl`
- **Lock File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/execution/work_queue.lock`
- **Module**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/execution/work_queue.py`
- **Examples**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/execution/work_queue_example.py`

## Performance Notes

- **Enqueue**: O(1) - Fast append
- **Get Next**: O(n log n) - Reads and sorts all tasks
- **Update**: O(n) - Rewrites entire file
- **Compact**: O(n) - Filters and rewrites

**Recommendation**: Works well for <1,000 tasks. Consider SQLite for >10,000 tasks.

## Thread Safety

- Uses `fcntl` file locking for atomic operations
- Safe for concurrent access from multiple processes
- Lock timeout: 10 seconds

## Examples

See `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/execution/work_queue_example.py` for comprehensive examples.

## Testing

Run built-in tests:
```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/execution
python3 work_queue.py
```

Run usage examples:
```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/execution
python3 work_queue_example.py
```

## Integration Points

Ready to integrate with:
- Constitutional compliance checks (PRIORITY_CRITICAL)
- Flow execution system (TYPE_FLOW_EXECUTION)
- Agent delegation (TYPE_USER_DELEGATION)
- Escalation handling (TYPE_AGENT_ESCALATION)

## Phase 1 Status

**Implemented**:
- Core queue operations
- Priority-based scheduling
- Dependency tracking
- Task lifecycle management
- Queue statistics
- Compaction

**Not Yet Implemented** (Phase 2+):
- State machine
- Automatic retry logic
- Blocker detection
- Agent auto-assignment
- Result validation
- Queue monitoring/alerts

---

**Version**: Phase 1 (Complete)
**Last Updated**: 2025-10-05
