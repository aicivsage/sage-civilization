#!/usr/bin/env python3
"""
Automatic Token Tracking Integration System

Enables automatic token tracking display after EVERY agent invocation without
Primary having to remember to call tracker manually.

This system provides two approaches:
1. Session-based auto-tracking (initialize once, tracks all invocations)
2. Bash hook wrapper (wraps Task invocations for automatic tracking)

Usage:
    # Approach 1: Python initialization (simplest)
    from tools.auto_token_tracking import AutoTokenTracker

    tracker = AutoTokenTracker()
    tracker.enable()  # Enable for this session

    # Then after any Task invocation:
    tracker.auto_track("researcher", tokens_used=3200)

    # OR use convenience method
    tracker.track_agent("researcher")  # Auto-estimates tokens

    # Approach 2: Bash command wrapping
    python3 tools/auto_token_tracking.py wrap researcher 3200

Author: coder agent
Date: 2025-11-20
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Tuple

# Fix import path to work from any location
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from track_mcp_tokens import TokenTracker


class AutoTokenTracker:
    """
    Automatic token tracking wrapper that eliminates manual tracking calls.

    Provides two mechanisms:
    1. Python API for easy integration into Primary's delegation workflow
    2. CLI wrapper for bash-based integrations
    """

    # Singleton instance for session-wide tracking
    _instance = None
    _enabled = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize auto-tracker (singleton pattern)"""
        if self._initialized:
            return

        self.tracker = TokenTracker()
        self.enabled = False
        self.session_config_file = Path.home() / ".sage_auto_tracking"
        self._initialized = True
        self._load_session_config()

    def _load_session_config(self):
        """Load session config to check if auto-tracking was previously enabled"""
        if self.session_config_file.exists():
            try:
                with open(self.session_config_file, 'r') as f:
                    config = json.load(f)
                    if config.get('enabled') and config.get('session_date') == str(datetime.now().date()):
                        self.enabled = True
            except (json.JSONDecodeError, OSError):
                pass

    def _save_session_config(self):
        """Persist session config"""
        try:
            with open(self.session_config_file, 'w') as f:
                json.dump({
                    'enabled': self.enabled,
                    'session_date': str(datetime.now().date()),
                    'timestamp': datetime.now().isoformat()
                }, f)
        except OSError as e:
            print(f"Warning: Could not save session config: {e}")

    def enable(self) -> str:
        """
        Enable automatic token tracking for this session.

        Returns:
            Status message confirming activation
        """
        self.enabled = True
        self._save_session_config()

        message = """
╔════════════════════════════════════════════════════════════╗
║         AUTOMATIC TOKEN TRACKING ENABLED ✅                 ║
╚════════════════════════════════════════════════════════════╝

Setup: Complete in 1 second

Instructions:
  After EVERY Task() invocation, call one of:

  Option A (Simple estimation):
    tracker.track_agent("researcher")

  Option B (With actual tokens):
    tracker.auto_track("researcher", tokens_used=3200)

  Option C (Bash wrapper):
    python3 tools/auto_token_tracking.py wrap researcher 3200

Features:
  ✓ Automatic MCP detection
  ✓ Savings calculation
  ✓ Session totals tracking
  ✓ Capacity multiplier display

Each invocation displays:
  - MCP status (✅ YES / ❌ NO)
  - Tokens saved this task
  - Session cumulative totals
  - Capacity boost multiplier

Ready to track! 🚀
"""
        print(message)
        return message

    def disable(self) -> str:
        """Disable automatic tracking"""
        self.enabled = False
        self._save_session_config()
        return "✓ Automatic token tracking disabled"

    def is_enabled(self) -> bool:
        """Check if auto-tracking is currently enabled"""
        return self.enabled

    def auto_track(
        self,
        agent_name: str,
        tokens_used: Optional[int] = None,
        force_mcp_detection: bool = True
    ) -> Dict:
        """
        Track an agent invocation automatically.

        Args:
            agent_name: Name of the invoked agent
            tokens_used: Actual tokens consumed (auto-estimated if None)
            force_mcp_detection: Whether to detect MCP usage

        Returns:
            Tracking result dictionary
        """
        if not self.enabled:
            return {
                "error": "Auto-tracking not enabled. Call tracker.enable() first."
            }

        # Auto-estimate tokens if not provided
        if tokens_used is None:
            tokens_used = self._estimate_tokens(agent_name)

        # Track via main tracker
        result = self.tracker.track_invocation(
            agent_name=agent_name,
            tokens_used=tokens_used,
            force_mcp_detection=force_mcp_detection
        )

        return result

    def track_agent(
        self,
        agent_name: str,
        force_mcp_detection: bool = True
    ) -> Dict:
        """
        Track an agent invocation with automatic token estimation.

        Convenience method - estimates tokens based on agent type,
        then tracks with auto-detected MCP usage.

        Args:
            agent_name: Name of the invoked agent
            force_mcp_detection: Whether to detect MCP usage

        Returns:
            Tracking result dictionary
        """
        if not self.enabled:
            return {
                "error": "Auto-tracking not enabled. Call tracker.enable() first."
            }

        estimated_tokens = self._estimate_tokens(agent_name)
        return self.auto_track(
            agent_name=agent_name,
            tokens_used=estimated_tokens,
            force_mcp_detection=force_mcp_detection
        )

    def _estimate_tokens(self, agent_name: str) -> int:
        """
        Estimate tokens for an agent based on baseline data.

        Uses "with_mcp" baseline as estimation (actual measured usage).

        Args:
            agent_name: Name of the agent

        Returns:
            Estimated tokens for this agent
        """
        # Baselines from track_mcp_tokens.py
        agent_baselines = {
            "researcher": 3000,
            "tester": 3000,
            "email-monitor": 2000,
            "email-sender": 3000,
            "coder": 10000,
            "auditor": 5000,
            "project-manager": 8000,
            "architect": 10000,
            "blogger": 10000,
            "human-liaison": 8000,
            "file-guardian": 6000,
            "comms-hub": 4000,
            "marketer": 7000,
            "reviewer": 6000,
            "reviewer-audit": 8000,
        }

        # Return agent-specific or default
        return agent_baselines.get(agent_name, 8000)

    def get_session_summary(self) -> Dict:
        """Get current session tracking summary"""
        return self.tracker.get_session_summary()

    def print_session_summary(self):
        """Print formatted session summary"""
        summary = self.get_session_summary()

        invocation_count = summary.get('invocation_count', 0)
        tokens_used = summary.get('total_tokens_used', 0)
        tokens_saved = summary.get('total_tokens_saved', 0)
        multiplier = summary.get('capacity_multiplier', 1.0)
        budget_remaining = summary.get('budget_remaining', 200000)

        print("\n" + "=" * 63)
        print("📊 SESSION SUMMARY - Auto Tracking")
        print("=" * 63)
        print(f"Invocations tracked: {invocation_count}")
        print(f"Tokens used: {tokens_used:,} / 200,000")
        print(f"Tokens saved: ~{tokens_saved:,}")
        print(f"Budget remaining: {budget_remaining:,}")
        print(f"Capacity multiplier: {multiplier:.1f}x")
        print("=" * 63 + "\n")


def setup_auto_tracking() -> AutoTokenTracker:
    """
    Setup and enable automatic token tracking for this session.

    Returns:
        Configured AutoTokenTracker instance
    """
    tracker = AutoTokenTracker()
    tracker.enable()
    return tracker


def wrap_task_invocation(agent_name: str, tokens_used: int) -> None:
    """
    Bash wrapper function for automatic tracking after Task invocation.

    Usage: python3 tools/auto_token_tracking.py wrap researcher 3200

    Args:
        agent_name: Name of the invoked agent
        tokens_used: Tokens consumed by this invocation
    """
    tracker = AutoTokenTracker()

    # Check if tracking is enabled for this session
    if not tracker.is_enabled():
        # Auto-enable if first-time use
        tracker.enable()

    # Track the invocation
    tracker.auto_track(agent_name, tokens_used)


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """Command-line interface for auto-tracking"""
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    command = sys.argv[1]

    if command == "enable":
        tracker = AutoTokenTracker()
        tracker.enable()
        sys.exit(0)

    elif command == "disable":
        tracker = AutoTokenTracker()
        print(tracker.disable())
        sys.exit(0)

    elif command == "status":
        tracker = AutoTokenTracker()
        status = "✅ ENABLED" if tracker.is_enabled() else "❌ DISABLED"
        print(f"Auto-tracking status: {status}")
        tracker.print_session_summary()
        sys.exit(0)

    elif command == "wrap":
        if len(sys.argv) < 4:
            print("Usage: auto_token_tracking.py wrap <agent_name> <tokens_used>")
            print("Example: auto_token_tracking.py wrap researcher 3200")
            sys.exit(1)

        agent_name = sys.argv[2]
        try:
            tokens_used = int(sys.argv[3])
        except ValueError:
            print(f"Error: tokens_used must be an integer, got '{sys.argv[3]}'")
            sys.exit(1)

        wrap_task_invocation(agent_name, tokens_used)
        sys.exit(0)

    elif command == "track":
        if len(sys.argv) < 3:
            print("Usage: auto_token_tracking.py track <agent_name> [tokens_used]")
            print("Example: auto_token_tracking.py track researcher 3200")
            sys.exit(1)

        agent_name = sys.argv[2]
        tokens_used = int(sys.argv[3]) if len(sys.argv) > 3 else None

        tracker = AutoTokenTracker()
        if tokens_used:
            tracker.auto_track(agent_name, tokens_used)
        else:
            tracker.track_agent(agent_name)
        sys.exit(0)

    elif command == "summary":
        tracker = AutoTokenTracker()
        tracker.print_session_summary()
        sys.exit(0)

    else:
        print(f"Unknown command: {command}")
        print_help()
        sys.exit(1)


def print_help():
    """Print CLI help"""
    print("""
Auto Token Tracking - CLI Interface

Commands:
  enable              Enable automatic tracking for this session
  disable             Disable automatic tracking
  status              Show current tracking status and session summary
  wrap <agent> <tokens>   Wrap a Task invocation (for bash integration)
  track <agent> [tokens]  Track an agent invocation
  summary             Print formatted session summary

Examples:
  python3 tools/auto_token_tracking.py enable
  python3 tools/auto_token_tracking.py wrap researcher 3200
  python3 tools/auto_token_tracking.py track coder 10000
  python3 tools/auto_token_tracking.py summary

For Primary AI:
  1. At session start:
     python3 tools/auto_token_tracking.py enable

  2. After every Task invocation:
     python3 tools/auto_token_tracking.py wrap <agent> <tokens>

  3. At session end:
     python3 tools/auto_token_tracking.py summary
""")


if __name__ == "__main__":
    main()
