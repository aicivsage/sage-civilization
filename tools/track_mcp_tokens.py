#!/usr/bin/env python3
"""
MCP Token Tracking System - Real-time savings display

Tracks token usage and MCP savings after each agent invocation.
Displays cumulative session statistics and capacity multiplier.

Usage:
    from tools.track_mcp_tokens import TokenTracker

    tracker = TokenTracker()
    tracker.track_invocation(agent_name="researcher", tokens_used=3200)
    # Automatically detects MCP usage and displays savings
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# Token savings baselines from MCP-TOKEN-SAVINGS-REPORT.md
BASELINE_TOKENS = {
    "researcher": {"without_mcp": 30000, "with_mcp": 3000, "savings_pct": 90},
    "tester": {"without_mcp": 40000, "with_mcp": 3000, "savings_pct": 92},
    "email-monitor": {"without_mcp": 15000, "with_mcp": 2000, "savings_pct": 87},
    "email-sender": {"without_mcp": 12000, "with_mcp": 3000, "savings_pct": 75},
    "coder": {"without_mcp": 35000, "with_mcp": 10000, "savings_pct": 70},
    "auditor": {"without_mcp": 20000, "with_mcp": 5000, "savings_pct": 75},
    "project-manager": {"without_mcp": 25000, "with_mcp": 8000, "savings_pct": 68},
    "architect": {"without_mcp": 25000, "with_mcp": 10000, "savings_pct": 60},
    "blogger": {"without_mcp": 20000, "with_mcp": 10000, "savings_pct": 50},
    "human-liaison": {"without_mcp": 15000, "with_mcp": 8000, "savings_pct": 47},
    "file-guardian": {"without_mcp": 18000, "with_mcp": 6000, "savings_pct": 67},
    "comms-hub": {"without_mcp": 12000, "with_mcp": 4000, "savings_pct": 67},
    "marketer": {"without_mcp": 18000, "with_mcp": 7000, "savings_pct": 61},
    "reviewer": {"without_mcp": 15000, "with_mcp": 6000, "savings_pct": 60},
    "reviewer-audit": {"without_mcp": 20000, "with_mcp": 8000, "savings_pct": 60},
    # Default for agents without specific baseline
    "default": {"without_mcp": 20000, "with_mcp": 8000, "savings_pct": 60},
}

WEEKLY_TOKEN_BUDGET = 200000
SESSION_TRACKING_FILE = "/tmp/sage_token_session.json"


class TokenTracker:
    """Tracks token usage and MCP savings across a session"""

    def __init__(self, session_file: str = SESSION_TRACKING_FILE):
        self.session_file = session_file
        self.session_data = self._load_or_create_session()
        self.sage_root = Path(__file__).parent.parent

    def _load_or_create_session(self) -> Dict:
        """Load existing session or create new one"""
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    data = json.load(f)
                    # Check if session is from today
                    session_date = datetime.fromisoformat(data.get('session_start', ''))
                    if (datetime.now() - session_date).days == 0:
                        return data
            except (json.JSONDecodeError, ValueError, OSError):
                pass

        # Create new session
        return {
            "session_start": datetime.now().isoformat(),
            "total_tokens_used": 0,
            "total_tokens_saved": 0,
            "invocations": []
        }

    def _save_session(self):
        """Persist session data to file"""
        try:
            with open(self.session_file, 'w') as f:
                json.dump(self.session_data, f, indent=2)
        except OSError as e:
            print(f"Warning: Could not save session data: {e}")

    def _detect_mcp_usage(self, agent_name: str, lookback_minutes: int = 5) -> Tuple[bool, int]:
        """
        Detect if agent used MCP in recent invocation

        Returns:
            (mcp_used: bool, execution_count: int)
        """
        execution_log_path = self.sage_root / "memories" / "agents" / agent_name / "execution_log.jsonl"

        if not execution_log_path.exists():
            return False, 0

        cutoff_time = datetime.now() - timedelta(minutes=lookback_minutes)
        recent_executions = []

        try:
            with open(execution_log_path, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        timestamp = datetime.fromisoformat(entry.get('timestamp', ''))
                        if timestamp >= cutoff_time:
                            recent_executions.append(entry)
                    except (json.JSONDecodeError, ValueError):
                        continue
        except OSError:
            return False, 0

        # Count successful executions
        execution_count = len([e for e in recent_executions if e.get('result', {}).get('success', False)])

        return execution_count > 0, execution_count

    def _get_baseline(self, agent_name: str) -> Dict:
        """Get token baseline for agent"""
        return BASELINE_TOKENS.get(agent_name, BASELINE_TOKENS["default"])

    def _calculate_savings(self, agent_name: str, tokens_used: int, mcp_used: bool) -> int:
        """Calculate estimated token savings"""
        if not mcp_used:
            return 0

        baseline = self._get_baseline(agent_name)

        # Estimate what this task would have cost without MCP
        # If agent used less than expected with_mcp, scale proportionally
        without_mcp_estimate = baseline["without_mcp"]
        with_mcp_estimate = baseline["with_mcp"]

        if tokens_used <= with_mcp_estimate:
            # Normal MCP usage, return full baseline savings
            return without_mcp_estimate - tokens_used
        else:
            # Higher token usage, scale savings proportionally
            scaling_factor = tokens_used / with_mcp_estimate
            scaled_baseline = int(without_mcp_estimate * scaling_factor)
            return scaled_baseline - tokens_used

    def track_invocation(
        self,
        agent_name: str,
        tokens_used: int,
        force_mcp_detection: bool = True
    ) -> Dict:
        """
        Track an agent invocation and display statistics

        Args:
            agent_name: Name of the invoked agent
            tokens_used: Actual tokens consumed
            force_mcp_detection: Whether to check execution logs (default: True)

        Returns:
            Dictionary with tracking statistics
        """
        # Detect MCP usage
        mcp_used, execution_count = self._detect_mcp_usage(agent_name) if force_mcp_detection else (False, 0)

        # Calculate savings
        tokens_saved = self._calculate_savings(agent_name, tokens_used, mcp_used)

        # Update session totals
        self.session_data["total_tokens_used"] += tokens_used
        self.session_data["total_tokens_saved"] += tokens_saved

        # Record invocation
        invocation_record = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "tokens_used": tokens_used,
            "mcp_used": mcp_used,
            "execution_count": execution_count,
            "tokens_saved": tokens_saved
        }
        self.session_data["invocations"].append(invocation_record)

        # Save session data
        self._save_session()

        # Display tracking output
        self._display_tracking(invocation_record)

        return invocation_record

    def _display_tracking(self, invocation: Dict):
        """Display formatted token tracking output"""
        agent = invocation["agent"]
        tokens_used = invocation["tokens_used"]
        mcp_used = invocation["mcp_used"]
        execution_count = invocation["execution_count"]
        tokens_saved = invocation["tokens_saved"]

        session_total = self.session_data["total_tokens_used"]
        session_saved = self.session_data["total_tokens_saved"]

        # Calculate percentages
        budget_pct = (session_total / WEEKLY_TOKEN_BUDGET) * 100
        effective_work = session_total + session_saved
        capacity_multiplier = effective_work / session_total if session_total > 0 else 1.0

        savings_pct = (tokens_saved / (tokens_used + tokens_saved) * 100) if tokens_saved > 0 else 0

        # MCP status indicator
        mcp_indicator = f"✅ YES ({execution_count} code executions detected)" if mcp_used else "❌ NO"

        # Build output
        print("\n" + "=" * 63)
        print("📊 TOKEN TRACKING - Session Total")
        print("=" * 63)
        print(f"This Task:")
        print(f"  Agent: {agent}")
        print(f"  Tokens used: {tokens_used:,}")
        print(f"  MCP used: {mcp_indicator}")
        if tokens_saved > 0:
            print(f"  Tokens saved: ~{tokens_saved:,} ({savings_pct:.0f}% reduction)")
        print()
        print(f"Session Total:")
        print(f"  Used: {session_total:,} / {WEEKLY_TOKEN_BUDGET:,} ({budget_pct:.0f}%)")
        print(f"  Saved via MCP: ~{session_saved:,}")
        print(f"  Effective capacity: {effective_work:,} tokens of work completed")
        print()
        print(f"🔥 MCP multiplier: {capacity_multiplier:.1f}x capacity boost this session")
        print("=" * 63)
        print()

    def get_session_summary(self) -> Dict:
        """Get current session statistics"""
        return {
            "session_start": self.session_data["session_start"],
            "total_tokens_used": self.session_data["total_tokens_used"],
            "total_tokens_saved": self.session_data["total_tokens_saved"],
            "invocation_count": len(self.session_data["invocations"]),
            "budget_remaining": WEEKLY_TOKEN_BUDGET - self.session_data["total_tokens_used"],
            "capacity_multiplier": (
                (self.session_data["total_tokens_used"] + self.session_data["total_tokens_saved"])
                / self.session_data["total_tokens_used"]
            ) if self.session_data["total_tokens_used"] > 0 else 1.0
        }

    def reset_session(self):
        """Reset session tracking (use with caution)"""
        self.session_data = {
            "session_start": datetime.now().isoformat(),
            "total_tokens_used": 0,
            "total_tokens_saved": 0,
            "invocations": []
        }
        self._save_session()
        print("✅ Session tracking reset")


def display_token_tracking(agent_name: str, tokens_used: int, session_total: int = None):
    """
    Convenience function for quick token tracking

    Args:
        agent_name: Name of invoked agent
        tokens_used: Tokens consumed by this invocation
        session_total: Optional override for session total (for testing)
    """
    tracker = TokenTracker()

    # Override session total if provided (for testing)
    if session_total is not None:
        tracker.session_data["total_tokens_used"] = session_total - tokens_used
        tracker.session_data["total_tokens_saved"] = int(session_total * 0.3)  # Estimate

    tracker.track_invocation(agent_name, tokens_used)


if __name__ == "__main__":
    # CLI interface for manual testing
    import sys

    if len(sys.argv) < 3:
        print("Usage: track_mcp_tokens.py <agent_name> <tokens_used>")
        print("Example: track_mcp_tokens.py researcher 3200")
        sys.exit(1)

    agent_name = sys.argv[1]
    tokens_used = int(sys.argv[2])

    display_token_tracking(agent_name, tokens_used)
