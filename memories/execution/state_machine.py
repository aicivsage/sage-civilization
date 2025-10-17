#!/usr/bin/env python3
"""
Execution State Machine - ADR-005 Phase 2

Autonomous execution loop state machine for continuous agent operation.
Implements 6-state lifecycle with automatic transitions and work queue integration.

States:
    STARTUP     - Load context, check health, populate work queue
    PLANNING    - Prioritize work, build execution plan
    EXECUTING   - Execute work (delegate to specialists)
    VERIFYING   - Check quality, test results
    REPORTING   - Update status, email summaries
    IDLE        - No work available, wait

State Transitions (Autonomous):
    STARTUP → PLANNING (always)
    PLANNING → EXECUTING (when plan ready)
    EXECUTING → VERIFYING (when tasks complete)
    VERIFYING → REPORTING (when tests pass)
    VERIFYING → PLANNING (on failure, retry)
    REPORTING → PLANNING (if more work)
    REPORTING → IDLE (if queue empty)

Usage:
    from state_machine import ExecutionStateMachine, ExecutionState

    # Create state machine
    machine = ExecutionStateMachine(token_budget=200000)

    # Initialize session
    machine.transition_to(ExecutionState.STARTUP)

    # Autonomous transitions
    machine.transition_to(ExecutionState.PLANNING)
    machine.transition_to(ExecutionState.EXECUTING)

    # Check current state
    state = machine.get_current_state()

    # Get session status
    status = machine.get_session_status()
"""

import json
import os
from dataclasses import dataclass, asdict, field
from datetime import datetime, UTC
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, List
from contextlib import contextmanager

# Import work queue (from Phase 1)
try:
    from work_queue import WorkQueueTask, get_queue_stats
except ImportError:
    # Fallback if not in path
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from work_queue import WorkQueueTask, get_queue_stats


# File paths
STATE_FILE = Path(__file__).parent / "session_state.json"
LOCK_FILE = Path(__file__).parent / "session_state.lock"


class ExecutionState(Enum):
    """
    Execution states for autonomous session loop.

    Each state represents a distinct phase in the execution lifecycle.
    Transitions are autonomous based on state-specific completion criteria.
    """
    STARTUP = "startup"         # Load context, check health, populate work queue
    PLANNING = "planning"       # Prioritize work, build execution plan
    EXECUTING = "executing"     # Execute work (delegate to specialists)
    VERIFYING = "verifying"     # Check quality, test results
    REPORTING = "reporting"     # Update status, email summaries
    IDLE = "idle"              # No work available, wait


@dataclass
class ExecutionPlan:
    """
    Execution plan for current session.

    Attributes:
        tasks: List of task IDs to execute in order
        estimated_tokens: Estimated token cost for plan
        agent_assignments: Map of task_id -> agent_name
        created_at: ISO 8601 timestamp when plan was created
    """
    tasks: List[str] = field(default_factory=list)
    estimated_tokens: int = 0
    agent_assignments: Dict[str, str] = field(default_factory=dict)
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(UTC).isoformat()


@dataclass
class StateMachineContext:
    """
    Complete state machine context.

    Attributes:
        current_state: Current execution state
        session_id: Unique session identifier
        session_start: ISO 8601 timestamp of session start
        work_queue_size: Number of pending tasks
        execution_plan: Current execution plan (None if not in EXECUTING/VERIFYING)
        token_budget_total: Total token budget for session (default: 200k)
        token_budget_used: Tokens consumed so far
        token_budget_reserved: Reserved tokens for reporting/email (default: 20k)
        last_transition: ISO 8601 timestamp of last state transition
        state_history: List of (state, timestamp) tuples
        errors: List of error messages from this session
        metadata: Additional context (flow execution, user delegation, etc.)
    """
    current_state: str = ExecutionState.STARTUP.value
    session_id: str = ""
    session_start: str = ""
    work_queue_size: int = 0
    execution_plan: Optional[Dict[str, Any]] = None
    token_budget_total: int = 200000
    token_budget_used: int = 0
    token_budget_reserved: int = 20000
    last_transition: str = ""
    state_history: List[tuple] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize session metadata if not provided."""
        if not self.session_id:
            self.session_id = f"session-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
        if not self.session_start:
            self.session_start = datetime.now(UTC).isoformat()
        if not self.last_transition:
            self.last_transition = self.session_start

    @property
    def token_budget_available(self) -> int:
        """Calculate available token budget (total - used - reserved)."""
        return max(0, self.token_budget_total - self.token_budget_used - self.token_budget_reserved)

    @property
    def session_duration_minutes(self) -> float:
        """Calculate session duration in minutes."""
        start = datetime.fromisoformat(self.session_start.replace('Z', '+00:00'))
        now = datetime.now(UTC)
        delta = now - start
        return delta.total_seconds() / 60.0

    def add_error(self, error_msg: str):
        """Add error to session log."""
        self.errors.append({
            "timestamp": datetime.now(UTC).isoformat(),
            "message": error_msg
        })


@contextmanager
def state_file_lock():
    """Context manager for state file locking."""
    import fcntl
    lock_file = open(LOCK_FILE, 'w')
    try:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
        lock_file.close()


class ExecutionStateMachine:
    """
    Execution state machine for autonomous session loops.

    Manages state transitions, work queue integration, token budget tracking,
    and real-time session status reporting.

    Example:
        >>> machine = ExecutionStateMachine(token_budget=200000)
        >>> machine.transition_to(ExecutionState.STARTUP)
        >>> machine.transition_to(ExecutionState.PLANNING)
        >>> status = machine.get_session_status()
    """

    def __init__(self, token_budget: int = 200000, session_id: Optional[str] = None):
        """
        Initialize state machine.

        Args:
            token_budget: Total token budget for session (default: 200k)
            session_id: Optional session ID (auto-generated if not provided)
        """
        self.context = StateMachineContext(
            token_budget_total=token_budget,
            session_id=session_id or f"session-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
        )
        self._ensure_state_file()

    def _ensure_state_file(self):
        """Ensure state file exists and is initialized."""
        if not STATE_FILE.exists():
            self._persist_state()

    def _persist_state(self):
        """Persist current state to disk (thread-safe)."""
        with state_file_lock():
            with open(STATE_FILE, 'w') as f:
                # Convert context to JSON-serializable dict
                state_data = {
                    "current_state": self.context.current_state,
                    "session_id": self.context.session_id,
                    "session_start": self.context.session_start,
                    "work_queue_size": self.context.work_queue_size,
                    "execution_plan": self.context.execution_plan,
                    "token_budget_total": self.context.token_budget_total,
                    "token_budget_used": self.context.token_budget_used,
                    "token_budget_reserved": self.context.token_budget_reserved,
                    "token_budget_available": self.context.token_budget_available,
                    "last_transition": self.context.last_transition,
                    "state_history": self.context.state_history,
                    "errors": self.context.errors,
                    "metadata": self.context.metadata,
                    "session_duration_minutes": self.context.session_duration_minutes
                }
                json.dump(state_data, f, indent=2)

    def _load_state(self) -> Optional[StateMachineContext]:
        """Load state from disk (thread-safe)."""
        if not STATE_FILE.exists():
            return None

        with state_file_lock():
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
                # Reconstruct context from saved data
                context = StateMachineContext(
                    current_state=data.get("current_state", ExecutionState.STARTUP.value),
                    session_id=data.get("session_id", ""),
                    session_start=data.get("session_start", ""),
                    work_queue_size=data.get("work_queue_size", 0),
                    execution_plan=data.get("execution_plan"),
                    token_budget_total=data.get("token_budget_total", 200000),
                    token_budget_used=data.get("token_budget_used", 0),
                    token_budget_reserved=data.get("token_budget_reserved", 20000),
                    last_transition=data.get("last_transition", ""),
                    state_history=data.get("state_history", []),
                    errors=data.get("errors", []),
                    metadata=data.get("metadata", {})
                )
                return context

    def transition_to(self, new_state: ExecutionState, metadata: Optional[Dict[str, Any]] = None):
        """
        Transition to a new state.

        Args:
            new_state: Target state to transition to
            metadata: Optional metadata to attach to transition

        Side Effects:
            - Updates context.current_state
            - Appends to context.state_history
            - Updates context.last_transition timestamp
            - Persists state to disk
            - Logs transition
        """
        old_state = self.context.current_state
        timestamp = datetime.now(UTC).isoformat()

        # Update context
        self.context.current_state = new_state.value
        self.context.last_transition = timestamp
        self.context.state_history.append((new_state.value, timestamp))

        # Update metadata if provided
        if metadata:
            self.context.metadata.update(metadata)

        # Persist state
        self._persist_state()

        # Log transition
        print(f"[STATE MACHINE] {old_state} → {new_state.value} (session: {self.context.session_id})")
        if metadata:
            print(f"[STATE MACHINE] Metadata: {metadata}")

    def get_current_state(self) -> ExecutionState:
        """Get current execution state."""
        return ExecutionState(self.context.current_state)

    def update_work_queue_size(self):
        """Update work queue size from queue stats."""
        try:
            stats = get_queue_stats()
            self.context.work_queue_size = stats.get("by_status", {}).get("pending", 0)
            self._persist_state()
        except Exception as e:
            self.context.add_error(f"Failed to update work queue size: {e}")

    def set_execution_plan(self, plan: ExecutionPlan):
        """Set execution plan for current session."""
        self.context.execution_plan = asdict(plan)
        self._persist_state()

    def clear_execution_plan(self):
        """Clear execution plan (used when transitioning out of EXECUTING/VERIFYING)."""
        self.context.execution_plan = None
        self._persist_state()

    def consume_tokens(self, token_count: int):
        """
        Record token consumption.

        Args:
            token_count: Number of tokens consumed
        """
        self.context.token_budget_used += token_count
        self._persist_state()

    def check_token_budget(self) -> bool:
        """
        Check if sufficient token budget remains.

        Returns:
            True if available budget > 0, False otherwise
        """
        return self.context.token_budget_available > 0

    def get_session_status(self) -> Dict[str, Any]:
        """
        Get complete session status for monitoring/dashboards.

        Returns:
            Dictionary with all session context including:
            - current_state
            - session_id, session_start, duration
            - work_queue_size
            - execution_plan (if active)
            - token_budget (total, used, available, reserved)
            - state_history
            - errors
        """
        return {
            "current_state": self.context.current_state,
            "session_id": self.context.session_id,
            "session_start": self.context.session_start,
            "session_duration_minutes": self.context.session_duration_minutes,
            "work_queue_size": self.context.work_queue_size,
            "execution_plan": self.context.execution_plan,
            "token_budget": {
                "total": self.context.token_budget_total,
                "used": self.context.token_budget_used,
                "available": self.context.token_budget_available,
                "reserved": self.context.token_budget_reserved,
                "utilization_percent": round(
                    (self.context.token_budget_used / self.context.token_budget_total) * 100, 2
                ) if self.context.token_budget_total > 0 else 0
            },
            "state_history": self.context.state_history,
            "errors": self.context.errors,
            "metadata": self.context.metadata
        }

    def add_error(self, error_msg: str):
        """Add error to session log."""
        self.context.add_error(error_msg)
        self._persist_state()


# Convenience functions for common state transitions

def initialize_session(token_budget: int = 200000) -> ExecutionStateMachine:
    """
    Initialize a new execution session.

    Args:
        token_budget: Total token budget (default: 200k)

    Returns:
        ExecutionStateMachine in STARTUP state
    """
    machine = ExecutionStateMachine(token_budget=token_budget)
    machine.transition_to(ExecutionState.STARTUP, metadata={"initialization": True})
    return machine


def startup_to_planning(machine: ExecutionStateMachine, work_loaded: int):
    """
    Transition from STARTUP to PLANNING.

    Args:
        machine: State machine instance
        work_loaded: Number of tasks loaded into queue
    """
    machine.update_work_queue_size()
    machine.transition_to(
        ExecutionState.PLANNING,
        metadata={"work_loaded": work_loaded}
    )


def planning_to_executing(machine: ExecutionStateMachine, plan: ExecutionPlan):
    """
    Transition from PLANNING to EXECUTING.

    Args:
        machine: State machine instance
        plan: Execution plan to execute
    """
    machine.set_execution_plan(plan)
    machine.transition_to(
        ExecutionState.EXECUTING,
        metadata={"plan_size": len(plan.tasks)}
    )


def executing_to_verifying(machine: ExecutionStateMachine, tasks_completed: int):
    """
    Transition from EXECUTING to VERIFYING.

    Args:
        machine: State machine instance
        tasks_completed: Number of tasks completed
    """
    machine.transition_to(
        ExecutionState.VERIFYING,
        metadata={"tasks_completed": tasks_completed}
    )


def verifying_to_reporting(machine: ExecutionStateMachine, tests_passed: bool):
    """
    Transition from VERIFYING to REPORTING (on success).

    Args:
        machine: State machine instance
        tests_passed: Whether verification tests passed
    """
    machine.clear_execution_plan()
    machine.transition_to(
        ExecutionState.REPORTING,
        metadata={"tests_passed": tests_passed}
    )


def verifying_to_planning(machine: ExecutionStateMachine, error_msg: str):
    """
    Transition from VERIFYING to PLANNING (on failure, retry).

    Args:
        machine: State machine instance
        error_msg: Error message from failed verification
    """
    machine.add_error(error_msg)
    machine.transition_to(
        ExecutionState.PLANNING,
        metadata={"retry": True, "reason": error_msg}
    )


def reporting_to_planning(machine: ExecutionStateMachine):
    """
    Transition from REPORTING to PLANNING (more work available).

    Args:
        machine: State machine instance
    """
    machine.update_work_queue_size()
    machine.transition_to(
        ExecutionState.PLANNING,
        metadata={"continue": True}
    )


def reporting_to_idle(machine: ExecutionStateMachine):
    """
    Transition from REPORTING to IDLE (no work available).

    Args:
        machine: State machine instance
    """
    machine.update_work_queue_size()
    machine.transition_to(
        ExecutionState.IDLE,
        metadata={"queue_empty": True}
    )


# Example usage and basic tests
if __name__ == "__main__":
    print("=== Execution State Machine - Basic Tests ===\n")

    # Test 1: Initialize session
    print("Test 1: Initialize session")
    machine = initialize_session(token_budget=200000)
    status = machine.get_session_status()
    print(f"Session ID: {status['session_id']}")
    print(f"Current State: {status['current_state']}")
    print(f"Token Budget: {status['token_budget']['available']}/{status['token_budget']['total']}")
    print()

    # Test 2: Transition through states
    print("Test 2: State transitions")
    startup_to_planning(machine, work_loaded=5)
    print(f"After STARTUP→PLANNING: {machine.get_current_state().value}")

    plan = ExecutionPlan(
        tasks=["task-001", "task-002", "task-003"],
        estimated_tokens=50000,
        agent_assignments={"task-001": "coder", "task-002": "tester"}
    )
    planning_to_executing(machine, plan)
    print(f"After PLANNING→EXECUTING: {machine.get_current_state().value}")

    executing_to_verifying(machine, tasks_completed=3)
    print(f"After EXECUTING→VERIFYING: {machine.get_current_state().value}")

    verifying_to_reporting(machine, tests_passed=True)
    print(f"After VERIFYING→REPORTING: {machine.get_current_state().value}")
    print()

    # Test 3: Token consumption
    print("Test 3: Token consumption")
    machine.consume_tokens(50000)
    status = machine.get_session_status()
    print(f"Tokens used: {status['token_budget']['used']}")
    print(f"Tokens available: {status['token_budget']['available']}")
    print(f"Utilization: {status['token_budget']['utilization_percent']}%")
    print()

    # Test 4: Error handling
    print("Test 4: Error handling")
    machine.add_error("Test error for demonstration")
    status = machine.get_session_status()
    print(f"Errors logged: {len(status['errors'])}")
    if status['errors']:
        print(f"Latest error: {status['errors'][-1]['message']}")
    print()

    # Test 5: State history
    print("Test 5: State history")
    status = machine.get_session_status()
    print("State transitions:")
    for state, timestamp in status['state_history']:
        print(f"  - {state} at {timestamp}")
    print()

    # Test 6: Complete cycle to IDLE
    print("Test 6: Complete cycle to IDLE")
    reporting_to_idle(machine)
    print(f"Final state: {machine.get_current_state().value}")
    print()

    # Test 7: Session status summary
    print("Test 7: Session status summary")
    status = machine.get_session_status()
    print(json.dumps(status, indent=2))
    print()

    print("=== All Tests Complete ===")
    print(f"Session state persisted to: {STATE_FILE}")
