# Execution State Machine - Quick Reference

## Overview

The execution state machine enables **autonomous continuous execution** by managing the lifecycle of agent work through 6 well-defined states with automatic transitions.

**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/execution/state_machine.py`
**State File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/execution/session_state.json`
**Phase**: ADR-005 Phase 2

---

## States

| State | Purpose | Typical Actions |
|-------|---------|-----------------|
| **STARTUP** | Initialize session | Load context, check health, populate work queue |
| **PLANNING** | Prioritize work | Build execution plan, assign agents, estimate tokens |
| **EXECUTING** | Execute work | Delegate to specialists, track progress |
| **VERIFYING** | Quality check | Run tests, validate results |
| **REPORTING** | Update status | Email summaries, update logs |
| **IDLE** | Wait for work | Monitor queue, wait for new tasks |

---

## Autonomous Transitions

```
STARTUP → PLANNING (always)
PLANNING → EXECUTING (when plan ready)
EXECUTING → VERIFYING (when tasks complete)
VERIFYING → REPORTING (when tests pass)
VERIFYING → PLANNING (on failure, retry)
REPORTING → PLANNING (if more work)
REPORTING → IDLE (if queue empty)
```

---

## Basic Usage

### 1. Initialize Session

```python
from state_machine import initialize_session

# Create new session with 200k token budget
machine = initialize_session(token_budget=200000)

# Session starts in STARTUP state
print(machine.get_current_state())  # ExecutionState.STARTUP
```

### 2. State Transitions

```python
from state_machine import (
    startup_to_planning,
    planning_to_executing,
    executing_to_verifying,
    verifying_to_reporting,
    reporting_to_idle
)

# STARTUP → PLANNING
startup_to_planning(machine, work_loaded=5)

# PLANNING → EXECUTING
from state_machine import ExecutionPlan
plan = ExecutionPlan(
    tasks=["task-001", "task-002"],
    estimated_tokens=50000,
    agent_assignments={"task-001": "coder"}
)
planning_to_executing(machine, plan)

# EXECUTING → VERIFYING
executing_to_verifying(machine, tasks_completed=2)

# VERIFYING → REPORTING (success)
verifying_to_reporting(machine, tests_passed=True)

# REPORTING → IDLE (no more work)
reporting_to_idle(machine)
```

### 3. Error Handling & Retry

```python
from state_machine import verifying_to_planning

# VERIFYING → PLANNING (on failure)
verifying_to_planning(machine, error_msg="Tests failed: assertion error")

# Machine returns to PLANNING to retry
```

### 4. Token Budget Management

```python
# Record token consumption
machine.consume_tokens(50000)

# Check remaining budget
if machine.check_token_budget():
    print(f"Available: {machine.context.token_budget_available}")
else:
    print("Token budget exhausted")
```

### 5. Session Status

```python
# Get complete session status
status = machine.get_session_status()

print(f"State: {status['current_state']}")
print(f"Session ID: {status['session_id']}")
print(f"Duration: {status['session_duration_minutes']:.2f} minutes")
print(f"Token Utilization: {status['token_budget']['utilization_percent']}%")
print(f"Work Queue Size: {status['work_queue_size']}")
print(f"Errors: {len(status['errors'])}")
```

---

## Real-Time Status Dashboard

The state machine automatically persists state to `session_state.json` on every transition. This file serves as a **real-time dashboard** for monitoring autonomous execution.

### View Current Status

```bash
# Pretty-print current state
cat memories/execution/session_state.json | jq

# Monitor state changes
watch -n 1 'cat memories/execution/session_state.json | jq .current_state'

# Check token usage
cat memories/execution/session_state.json | jq .token_budget
```

### Example Session State

```json
{
  "current_state": "executing",
  "session_id": "session-20251005-151034",
  "session_start": "2025-10-05T15:10:34.937067+00:00",
  "work_queue_size": 3,
  "execution_plan": {
    "tasks": ["task-001", "task-002"],
    "estimated_tokens": 50000,
    "agent_assignments": {"task-001": "coder"}
  },
  "token_budget": {
    "total": 200000,
    "used": 50000,
    "available": 130000,
    "reserved": 20000,
    "utilization_percent": 25.0
  },
  "state_history": [...],
  "errors": [],
  "metadata": {...}
}
```

---

## Integration with Work Queue

The state machine integrates with the work queue from Phase 1:

```python
# Update work queue size automatically
machine.update_work_queue_size()

# Work queue size reflects in status
status = machine.get_session_status()
print(f"Pending tasks: {status['work_queue_size']}")
```

---

## Execution Plan Schema

```python
@dataclass
class ExecutionPlan:
    tasks: List[str]                    # Task IDs to execute
    estimated_tokens: int               # Estimated token cost
    agent_assignments: Dict[str, str]   # task_id → agent_name
    created_at: str                     # ISO 8601 timestamp
```

**Example**:

```python
plan = ExecutionPlan(
    tasks=["task-001", "task-002", "task-003"],
    estimated_tokens=75000,
    agent_assignments={
        "task-001": "coder",
        "task-002": "tester",
        "task-003": "reviewer"
    }
)
```

---

## Advanced: Manual Transitions

For custom workflows, use direct transition method:

```python
from state_machine import ExecutionState

# Manual transition
machine.transition_to(
    ExecutionState.PLANNING,
    metadata={"reason": "custom_trigger"}
)

# Transition with custom metadata
machine.transition_to(
    ExecutionState.EXECUTING,
    metadata={
        "flow_id": "daily-startup-consolidation",
        "trigger": "scheduled"
    }
)
```

---

## Error Logging

```python
# Add error to session log
machine.add_error("Agent delegation failed: timeout")

# Errors persist with timestamps
status = machine.get_session_status()
for error in status['errors']:
    print(f"{error['timestamp']}: {error['message']}")
```

---

## Token Budget Configuration

Default budget: **200,000 tokens** (20k reserved for reporting)

```python
# Custom budget
machine = initialize_session(token_budget=100000)

# Reserved tokens (not consumed during execution)
machine.context.token_budget_reserved = 15000

# Calculate available budget
available = machine.context.token_budget_available
# = total - used - reserved
```

---

## State History Tracking

All state transitions are logged with timestamps:

```python
status = machine.get_session_status()

for state, timestamp in status['state_history']:
    print(f"{state} @ {timestamp}")

# Output:
# startup @ 2025-10-05T15:10:34.939040+00:00
# planning @ 2025-10-05T15:10:34.939597+00:00
# executing @ 2025-10-05T15:10:34.940250+00:00
# ...
```

---

## Best Practices

1. **Always initialize with `initialize_session()`** - Sets up proper context
2. **Use convenience functions** - `startup_to_planning()`, etc. handle metadata correctly
3. **Track token consumption** - Call `consume_tokens()` after each agent delegation
4. **Monitor `session_state.json`** - Real-time dashboard for debugging
5. **Check token budget** - Use `check_token_budget()` before expensive operations
6. **Log errors immediately** - Call `add_error()` on any failure

---

## Next Steps (Phase 3)

Phase 2 provides the **state machine foundation**. Phase 3 will add:

1. **Full Execution Loop** - Autonomous execution using state machine + work queue
2. **Agent Delegation** - Auto-assign tasks to appropriate agents
3. **Retry Logic** - Automatic retry with exponential backoff
4. **Flow Integration** - Connect to flows system (`memories/flows/`)
5. **Monitoring** - Health checks, stuck task detection
6. **Email Reporting** - Auto-send status updates via email-reporter

---

## Testing

Run built-in tests:

```bash
python3 memories/execution/state_machine.py
```

Expected output:
- ✅ Session initialization
- ✅ State transitions (STARTUP → PLANNING → EXECUTING → VERIFYING → REPORTING → IDLE)
- ✅ Token consumption tracking
- ✅ Error logging
- ✅ State history
- ✅ Status dashboard

---

**Implementation**: ADR-005 Phase 2
**Status**: Complete
**Dependencies**: `work_queue.py` (Phase 1)
**Next**: Full execution loop (Phase 3)
