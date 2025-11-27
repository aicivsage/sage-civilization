#!/usr/bin/env python3
"""
Token Tracking System - Live Demo

Demonstrates the token tracking system with a realistic session simulation.
Shows how MCP savings accumulate across multiple agent invocations.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.track_mcp_tokens import TokenTracker


def simulate_realistic_session():
    """Simulate a realistic work session with multiple agent invocations"""

    print("\n" + "=" * 63)
    print("🎬 TOKEN TRACKING SYSTEM - LIVE DEMONSTRATION")
    print("=" * 63)
    print()
    print("Simulating realistic Sage civilization work session...")
    print()

    # Create fresh session
    tracker = TokenTracker()
    tracker.reset_session()

    print("=" * 63)
    print("SESSION START")
    print("=" * 63)
    print()

    # Invocation 1: researcher gathers information (HIGH savings agent)
    print("🔍 INVOCATION 1: researcher gathering fundraising data")
    print("-" * 63)
    tracker.session_data["invocations"].append({
        "timestamp": "2025-11-20T09:45:00",
        "agent": "researcher",
        "tokens_used": 3200,
        "mcp_used": True,
        "execution_count": 4,
        "tokens_saved": 26800  # 30K baseline - 3.2K used = 90% savings
    })
    tracker.session_data["total_tokens_used"] += 3200
    tracker.session_data["total_tokens_saved"] += 26800
    tracker._display_tracking(tracker.session_data["invocations"][-1])

    # Invocation 2: coder implements feature (MEDIUM savings agent)
    print("💻 INVOCATION 2: coder implementing blog post generator")
    print("-" * 63)
    tracker.session_data["invocations"].append({
        "timestamp": "2025-11-20T10:15:00",
        "agent": "coder",
        "tokens_used": 10200,
        "mcp_used": True,
        "execution_count": 7,
        "tokens_saved": 24800  # 35K baseline - 10.2K used = 70% savings
    })
    tracker.session_data["total_tokens_used"] += 10200
    tracker.session_data["total_tokens_saved"] += 24800
    tracker._display_tracking(tracker.session_data["invocations"][-1])

    # Invocation 3: tester validates (HIGHEST savings agent)
    print("🧪 INVOCATION 3: tester running test suite")
    print("-" * 63)
    tracker.session_data["invocations"].append({
        "timestamp": "2025-11-20T10:45:00",
        "agent": "tester",
        "tokens_used": 3000,
        "mcp_used": True,
        "execution_count": 5,
        "tokens_saved": 37000  # 40K baseline - 3K used = 92% savings
    })
    tracker.session_data["total_tokens_used"] += 3000
    tracker.session_data["total_tokens_saved"] += 37000
    tracker._display_tracking(tracker.session_data["invocations"][-1])

    # Invocation 4: human-liaison checks email (LOW savings - conversational)
    print("📧 INVOCATION 4: human-liaison checking inbox")
    print("-" * 63)
    tracker.session_data["invocations"].append({
        "timestamp": "2025-11-20T11:00:00",
        "agent": "human-liaison",
        "tokens_used": 8000,
        "mcp_used": False,  # Conversational, no code execution
        "execution_count": 0,
        "tokens_saved": 0
    })
    tracker.session_data["total_tokens_used"] += 8000
    tracker._display_tracking(tracker.session_data["invocations"][-1])

    # Invocation 5: email-monitor analyzes inbox (HIGH savings agent)
    print("📬 INVOCATION 5: email-monitor analyzing messages")
    print("-" * 63)
    tracker.session_data["invocations"].append({
        "timestamp": "2025-11-20T11:15:00",
        "agent": "email-monitor",
        "tokens_used": 2100,
        "mcp_used": True,
        "execution_count": 3,
        "tokens_saved": 12900  # 15K baseline - 2.1K used = 87% savings
    })
    tracker.session_data["total_tokens_used"] += 2100
    tracker.session_data["total_tokens_saved"] += 12900
    tracker._display_tracking(tracker.session_data["invocations"][-1])

    # Invocation 6: auditor system check (MEDIUM savings agent)
    print("🔍 INVOCATION 6: auditor performing system health check")
    print("-" * 63)
    tracker.session_data["invocations"].append({
        "timestamp": "2025-11-20T11:30:00",
        "agent": "auditor",
        "tokens_used": 5200,
        "mcp_used": True,
        "execution_count": 6,
        "tokens_saved": 14800  # 20K baseline - 5.2K used = 75% savings
    })
    tracker.session_data["total_tokens_used"] += 5200
    tracker.session_data["total_tokens_saved"] += 14800
    tracker._display_tracking(tracker.session_data["invocations"][-1])

    # Session summary
    print()
    print("=" * 63)
    print("SESSION SUMMARY")
    print("=" * 63)

    summary = tracker.get_session_summary()

    print(f"Duration: 2.5 hours of work")
    print(f"Total invocations: {summary['invocation_count']}")
    print(f"Agents with MCP: 5/6 (83%)")
    print()
    print(f"Token Economics:")
    print(f"  Tokens used: {summary['total_tokens_used']:,}")
    print(f"  Tokens saved: {summary['total_tokens_saved']:,}")
    print(f"  Effective work: {summary['total_tokens_used'] + summary['total_tokens_saved']:,} tokens")
    print(f"  Budget remaining: {summary['budget_remaining']:,} / 200,000")
    print(f"  Budget used: {(summary['total_tokens_used'] / 200000 * 100):.1f}%")
    print()
    print(f"🔥 MCP MULTIPLIER: {summary['capacity_multiplier']:.1f}x")
    print()
    print(f"Impact Analysis:")
    print(f"  WITHOUT MCP: Would have used ~{summary['total_tokens_used'] + summary['total_tokens_saved']:,} tokens")
    print(f"  WITH MCP: Actually used {summary['total_tokens_used']:,} tokens")
    print(f"  SAVINGS: {(summary['total_tokens_saved'] / (summary['total_tokens_used'] + summary['total_tokens_saved']) * 100):.1f}% reduction")
    print()
    print(f"What This Means:")
    print(f"  • Completed 2.5 hours of work using only 16% of weekly budget")
    print(f"  • Remaining capacity: ~15 hours of intensive work this week")
    print(f"  • MCP enabled 4.8x more work in same token budget")
    print(f"  • Zero risk of token exhaustion before week end")
    print()
    print("=" * 63)
    print("✅ DEMONSTRATION COMPLETE")
    print("=" * 63)
    print()

    tracker._save_session()


if __name__ == "__main__":
    simulate_realistic_session()
