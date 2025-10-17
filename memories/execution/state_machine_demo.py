#!/usr/bin/env python3
"""
State Machine Demo - Practical Usage Example

Demonstrates how the execution state machine enables autonomous continuous execution.
Shows a realistic session lifecycle with work queue integration.
"""

from state_machine import (
    initialize_session,
    startup_to_planning,
    planning_to_executing,
    executing_to_verifying,
    verifying_to_reporting,
    verifying_to_planning,
    reporting_to_planning,
    reporting_to_idle,
    ExecutionPlan,
    ExecutionState
)

from work_queue import (
    enqueue_task,
    WorkQueueTask,
    PRIORITY_HIGH,
    PRIORITY_NORMAL,
    TYPE_USER_DELEGATION,
    STATUS_PENDING
)

from datetime import datetime, UTC
import json


def simulate_session():
    """Simulate a realistic autonomous execution session."""

    print("=" * 60)
    print("EXECUTION STATE MACHINE - REALISTIC SESSION DEMO")
    print("=" * 60)
    print()

    # ========================================
    # PHASE 1: SESSION INITIALIZATION
    # ========================================
    print("PHASE 1: SESSION INITIALIZATION")
    print("-" * 40)

    # Initialize session with 200k token budget
    machine = initialize_session(token_budget=200000)
    print(f"✅ Session initialized: {machine.context.session_id}")
    print(f"   Token budget: {machine.context.token_budget_total:,}")
    print(f"   Current state: {machine.get_current_state().value}")
    print()

    # ========================================
    # PHASE 2: LOAD WORK QUEUE
    # ========================================
    print("PHASE 2: LOAD WORK QUEUE")
    print("-" * 40)

    # Enqueue some realistic tasks
    tasks = [
        WorkQueueTask(
            id="task-001",
            priority=PRIORITY_HIGH,
            type=TYPE_USER_DELEGATION,
            action="implement_feature",
            params={"feature": "email_reporter", "requirements": "send_html_emails"},
            status=STATUS_PENDING,
            created_at=datetime.now(UTC).isoformat(),
            dependencies=[]
        ),
        WorkQueueTask(
            id="task-002",
            priority=PRIORITY_NORMAL,
            type=TYPE_USER_DELEGATION,
            action="write_tests",
            params={"target": "email_reporter", "coverage": "80%"},
            status=STATUS_PENDING,
            created_at=datetime.now(UTC).isoformat(),
            dependencies=["task-001"]  # Depends on implementation
        )
    ]

    for task in tasks:
        enqueue_task(task)
        print(f"✅ Enqueued: {task.id} ({task.action})")

    print()

    # ========================================
    # PHASE 3: STARTUP → PLANNING
    # ========================================
    print("PHASE 3: STARTUP → PLANNING")
    print("-" * 40)

    startup_to_planning(machine, work_loaded=len(tasks))
    print(f"✅ Transitioned to PLANNING")
    print(f"   Work loaded: {len(tasks)} tasks")
    print(f"   Current state: {machine.get_current_state().value}")
    print()

    # ========================================
    # PHASE 4: PLANNING → EXECUTING
    # ========================================
    print("PHASE 4: PLANNING → EXECUTING")
    print("-" * 40)

    # Build execution plan
    plan = ExecutionPlan(
        tasks=["task-001"],  # Only execute task-001 (task-002 blocked by dependency)
        estimated_tokens=50000,
        agent_assignments={"task-001": "coder"}
    )

    planning_to_executing(machine, plan)
    print(f"✅ Transitioned to EXECUTING")
    print(f"   Execution plan:")
    print(f"     - Tasks: {plan.tasks}")
    print(f"     - Estimated tokens: {plan.estimated_tokens:,}")
    print(f"     - Agent assignments: {plan.agent_assignments}")
    print(f"   Current state: {machine.get_current_state().value}")
    print()

    # ========================================
    # PHASE 5: SIMULATE EXECUTION
    # ========================================
    print("PHASE 5: SIMULATE EXECUTION")
    print("-" * 40)

    # Simulate token consumption during execution
    machine.consume_tokens(45000)
    print(f"✅ Executed task-001 (coder agent)")
    print(f"   Tokens consumed: 45,000")
    print(f"   Tokens remaining: {machine.context.token_budget_available:,}")
    print()

    # ========================================
    # PHASE 6: EXECUTING → VERIFYING
    # ========================================
    print("PHASE 6: EXECUTING → VERIFYING")
    print("-" * 40)

    executing_to_verifying(machine, tasks_completed=1)
    print(f"✅ Transitioned to VERIFYING")
    print(f"   Tasks completed: 1")
    print(f"   Current state: {machine.get_current_state().value}")
    print()

    # ========================================
    # PHASE 7: VERIFYING → REPORTING (SUCCESS)
    # ========================================
    print("PHASE 7: VERIFYING → REPORTING (SUCCESS)")
    print("-" * 40)

    verifying_to_reporting(machine, tests_passed=True)
    print(f"✅ Transitioned to REPORTING")
    print(f"   Verification: PASSED")
    print(f"   Current state: {machine.get_current_state().value}")
    print()

    # ========================================
    # PHASE 8: REPORTING → PLANNING (MORE WORK)
    # ========================================
    print("PHASE 8: REPORTING → PLANNING (MORE WORK)")
    print("-" * 40)

    # Simulate sending report
    machine.consume_tokens(5000)
    print(f"✅ Sent status report (5,000 tokens)")

    reporting_to_planning(machine)
    print(f"✅ Transitioned to PLANNING (more work available)")
    print(f"   Current state: {machine.get_current_state().value}")
    print()

    # ========================================
    # PHASE 9: SECOND EXECUTION CYCLE
    # ========================================
    print("PHASE 9: SECOND EXECUTION CYCLE (TASK-002)")
    print("-" * 40)

    # Build second execution plan
    plan2 = ExecutionPlan(
        tasks=["task-002"],  # Now unblocked (task-001 complete)
        estimated_tokens=30000,
        agent_assignments={"task-002": "tester"}
    )

    planning_to_executing(machine, plan2)
    print(f"✅ Transitioned to EXECUTING")
    print(f"   Execution plan:")
    print(f"     - Tasks: {plan2.tasks}")
    print(f"     - Agent assignments: {plan2.agent_assignments}")

    machine.consume_tokens(28000)
    print(f"✅ Executed task-002 (tester agent)")
    print(f"   Tokens consumed: 28,000")

    executing_to_verifying(machine, tasks_completed=1)
    print(f"✅ Transitioned to VERIFYING")

    verifying_to_reporting(machine, tests_passed=True)
    print(f"✅ Transitioned to REPORTING")
    print()

    # ========================================
    # PHASE 10: REPORTING → IDLE (DONE)
    # ========================================
    print("PHASE 10: REPORTING → IDLE (DONE)")
    print("-" * 40)

    # Simulate sending final report
    machine.consume_tokens(5000)
    print(f"✅ Sent final status report (5,000 tokens)")

    reporting_to_idle(machine)
    print(f"✅ Transitioned to IDLE (no more work)")
    print(f"   Current state: {machine.get_current_state().value}")
    print()

    # ========================================
    # PHASE 11: SESSION SUMMARY
    # ========================================
    print("PHASE 11: SESSION SUMMARY")
    print("-" * 40)

    status = machine.get_session_status()

    print(f"Session ID: {status['session_id']}")
    print(f"Duration: {status['session_duration_minutes']:.4f} minutes")
    print(f"Final State: {status['current_state']}")
    print()

    print("Token Budget:")
    print(f"  Total: {status['token_budget']['total']:,}")
    print(f"  Used: {status['token_budget']['used']:,}")
    print(f"  Available: {status['token_budget']['available']:,}")
    print(f"  Reserved: {status['token_budget']['reserved']:,}")
    print(f"  Utilization: {status['token_budget']['utilization_percent']}%")
    print()

    print("State History:")
    for i, (state, timestamp) in enumerate(status['state_history'], 1):
        print(f"  {i}. {state} @ {timestamp}")
    print()

    print("Errors:", "None" if not status['errors'] else len(status['errors']))
    print()

    # ========================================
    # PHASE 12: DEMONSTRATE RETRY FLOW
    # ========================================
    print("=" * 60)
    print("BONUS: RETRY FLOW DEMONSTRATION")
    print("=" * 60)
    print()

    print("Simulating failure scenario...")
    print()

    # Reset to EXECUTING state
    machine.transition_to(ExecutionState.EXECUTING)
    machine.set_execution_plan(ExecutionPlan(
        tasks=["task-003"],
        estimated_tokens=20000,
        agent_assignments={"task-003": "coder"}
    ))

    # Simulate execution failure
    executing_to_verifying(machine, tasks_completed=1)
    print(f"✅ Executed task-003 (but tests will fail)")

    # Verify fails, retry from PLANNING
    verifying_to_planning(machine, error_msg="Tests failed: assertion error in test_feature.py")
    print(f"❌ Verification FAILED")
    print(f"✅ Transitioned to PLANNING for retry")
    print()

    # Check error log
    final_status = machine.get_session_status()
    if final_status['errors']:
        print("Error Log:")
        for error in final_status['errors']:
            print(f"  [{error['timestamp']}] {error['message']}")
    print()

    print("=" * 60)
    print("SESSION COMPLETE")
    print("=" * 60)
    print()
    print(f"Session state persisted to: {machine.context.session_id}")
    print(f"Real-time dashboard: memories/execution/session_state.json")


def demonstrate_error_handling():
    """Demonstrate error handling and retry logic."""

    print()
    print("=" * 60)
    print("ERROR HANDLING DEMO")
    print("=" * 60)
    print()

    machine = initialize_session()

    # Simulate execution failure
    startup_to_planning(machine, work_loaded=1)
    plan = ExecutionPlan(tasks=["task-fail"], estimated_tokens=10000, agent_assignments={"task-fail": "coder"})
    planning_to_executing(machine, plan)
    executing_to_verifying(machine, tasks_completed=1)

    # Verification fails
    verifying_to_planning(machine, error_msg="Linter errors: 5 issues found")
    print("✅ Error logged and retried from PLANNING")

    status = machine.get_session_status()
    print(f"\nErrors in session: {len(status['errors'])}")
    for error in status['errors']:
        print(f"  - {error['message']}")


if __name__ == "__main__":
    # Run main demo
    simulate_session()

    # Run error handling demo
    demonstrate_error_handling()

    print("\n✨ Demo complete! Check memories/execution/session_state.json for live state.")
