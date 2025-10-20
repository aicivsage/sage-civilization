#!/usr/bin/env python3
# =============================================================================
# PRODUCTION STATUS: BROKEN ❌
# Last status check: 2025-10-19
# Status: REPLACED by telegram_bridge.py - DO NOT USE
# Issue: Unreliable emoji detection, replaced by bridge architecture
# =============================================================================
"""
Telegram Monitor - Automatic summary detection and delivery.

**DEPRECATED:** This script has been replaced by telegram_bridge.py
which uses a more reliable architecture. Use the bridge instead.

Polls tmux session every 5 minutes, detects session summaries using markers,
and automatically sends them to Corey's Telegram.

Usage:
    python3 tools/telegram_monitor.py [--interval SECONDS] [--tmux-session SESSION]

    --interval: Polling interval in seconds (default: 300 = 5 minutes)
    --tmux-session: Tmux session to monitor (default: "0")

Environment:
    Reads Corey's user ID from config/telegram_config.json

Detection markers:
    🤖 SESSION START SUMMARY 🤖
    ...content...
    🤖 END SESSION START SUMMARY 🤖

    🤖 SESSION END SUMMARY 🤖
    ...content...
    🤖 END SESSION END SUMMARY 🤖
"""
import argparse
import hashlib
import json
import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "telegram_config.json"
STATE_FILE = PROJECT_ROOT / ".tg_sessions" / "monitor_state.json"
PID_FILE = PROJECT_ROOT / ".tg_sessions" / "acgee_monitor.pid"
SEND_SCRIPT = PROJECT_ROOT / "tools" / "send_telegram_direct.py"

# Summary markers - simple emoji wrappers
START_MARKER = "🤖🎯📱"
END_MARKER = "✨🔚"


def check_existing_process():
    """
    Check if another A-C-Gee monitor is already running.
    Returns True if another process is running, False otherwise.
    """
    if not PID_FILE.exists():
        return False

    try:
        with open(PID_FILE, 'r') as f:
            old_pid = int(f.read().strip())

        # Check if process is still running
        try:
            os.kill(old_pid, 0)  # Signal 0 doesn't kill, just checks existence
            logger.warning(f"Another A-C-Gee monitor is already running (PID: {old_pid})")
            logger.warning("Run 'bash tools/restart_telegram_monitor.sh' to restart it")
            return True
        except OSError:
            # Process doesn't exist, stale PID file
            logger.info(f"Found stale PID file (PID {old_pid} not running), removing")
            PID_FILE.unlink()
            return False
    except Exception as e:
        logger.warning(f"Error checking PID file: {e}")
        return False


def create_pid_file():
    """Create PID file with current process ID."""
    PID_FILE.parent.mkdir(exist_ok=True)
    try:
        with open(PID_FILE, 'w') as f:
            f.write(str(os.getpid()))
        logger.info(f"Created PID file: {PID_FILE} (PID: {os.getpid()})")
    except Exception as e:
        logger.error(f"Failed to create PID file: {e}")


def remove_pid_file():
    """Remove PID file on clean shutdown."""
    try:
        if PID_FILE.exists():
            PID_FILE.unlink()
            logger.info("Removed PID file")
    except Exception as e:
        logger.warning(f"Failed to remove PID file: {e}")


def load_config():
    """Load telegram configuration."""
    if not CONFIG_FILE.exists():
        logger.error(f"Config file not found: {CONFIG_FILE}")
        return None

    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return None


def load_state():
    """Load monitor state (last seen summaries and buffer position)."""
    if not STATE_FILE.exists():
        return {"last_summaries": [], "last_buffer_position": 0}

    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
            # Ensure last_buffer_position exists (backward compatibility)
            if "last_buffer_position" not in state:
                state["last_buffer_position"] = 0
            return state
    except Exception as e:
        logger.warning(f"Failed to load state, starting fresh: {e}")
        return {"last_summaries": [], "last_buffer_position": 0}


def save_state(state):
    """Save monitor state."""
    STATE_FILE.parent.mkdir(exist_ok=True)

    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save state: {e}")


def capture_tmux_buffer(session: str) -> tuple:
    """
    Capture tmux buffer content.

    Args:
        session: Tmux session identifier (e.g., "0" or "acgee-main")

    Returns:
        Tuple of (buffer_content: str, line_count: int)
    """
    try:
        # Capture last 500 lines from tmux pane
        result = subprocess.run(
            ["tmux", "capture-pane", "-t", f"{session}:0.0", "-p", "-S", "-500"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )
        lines = result.stdout.split('\n')
        return result.stdout, len(lines)
    except subprocess.CalledProcessError as e:
        logger.error(f"tmux capture failed: {e}")
        return "", 0
    except subprocess.TimeoutExpired:
        logger.error("tmux capture timed out")
        return "", 0
    except Exception as e:
        logger.error(f"Unexpected error capturing tmux: {e}")
        return "", 0


def extract_summaries(buffer: str) -> list:
    """
    Extract session summaries from buffer using markers.

    Args:
        buffer: Tmux buffer content

    Returns:
        List of dicts: [{"type": "start"|"end", "content": "...", "timestamp": "..."}]
    """
    summaries = []
    lines = buffer.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check for start marker
        if START_MARKER in line:
            content_lines = []
            i += 1

            # Collect lines until end marker
            while i < len(lines):
                if END_MARKER in lines[i]:
                    break
                content_lines.append(lines[i])
                i += 1

            if content_lines:
                summary = {
                    "type": "message",
                    "content": '\n'.join(content_lines).strip(),
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
                summaries.append(summary)

        i += 1

    return summaries


def get_summary_hash(summary: dict) -> str:
    """
    Generate unique hash for entire summary content.

    Args:
        summary: Summary dict with type, content

    Returns:
        Hash string (type:content_hash)
    """
    content_hash = hashlib.sha256(summary['content'].encode()).hexdigest()
    return f"{summary['type']}:{content_hash}"


def is_new_summary(summary: dict, seen_summaries: set) -> bool:
    """
    Check if summary is new (not already sent).

    Args:
        summary: Summary dict with type, content, timestamp
        seen_summaries: Set of previously seen summary hashes

    Returns:
        True if summary is new
    """
    summary_hash = get_summary_hash(summary)
    return summary_hash not in seen_summaries


def send_summary(user_id: int, summary: dict) -> bool:
    """
    Send summary to Telegram.

    Args:
        user_id: Telegram user ID
        summary: Summary dict with type, content

    Returns:
        True if sent successfully
    """
    # Send content directly - already contains wrapper emojis from Primary
    # DO NOT double-wrap (was causing Markdown parse failures)
    message = summary['content']

    # Call send script
    try:
        result = subprocess.run(
            ["python3", str(SEND_SCRIPT), str(user_id), message],
            capture_output=True,
            text=True,
            check=True,
            timeout=15
        )

        # Log subprocess output for debugging
        if result.stdout:
            logger.info(f"Send script output: {result.stdout.strip()}")
        if result.stderr:
            logger.warning(f"Send script stderr: {result.stderr.strip()}")

        logger.info(f"Sent {summary['type']} summary to user {user_id}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to send summary (exit code {e.returncode}): {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending summary: {e}")
        return False


def monitor_loop(interval: int, tmux_session: str, user_id: int):
    """
    Main monitoring loop with PID file management.

    Args:
        interval: Polling interval in seconds
        tmux_session: Tmux session to monitor
        user_id: Telegram user ID to send to
    """
    logger.info(f"Starting Telegram monitor (interval: {interval}s, session: {tmux_session})")
    logger.info(f"Monitoring for summaries to send to user {user_id}")

    # Create PID file to mark our process
    create_pid_file()

    state = load_state()
    seen_summaries = set(state.get("last_summaries", []))

    # SIMPLE FIX (Option A): Remove buffer position tracking entirely
    # Rely on hash-based deduplication to prevent duplicates
    # This makes the monitor more reliable at the cost of scanning full buffer every poll

    try:
        while True:
            try:
                # Capture tmux buffer
                buffer, _ = capture_tmux_buffer(tmux_session)

                if buffer:
                    # SIMPLE: Scan full buffer every poll (deduplication prevents duplicates)
                    summaries = extract_summaries(buffer)

                    if summaries:
                        logger.info(f"Found {len(summaries)} summaries in buffer")

                        # Send new summaries
                        for summary in summaries:
                            if is_new_summary(summary, seen_summaries):
                                logger.info(f"New {summary['type']} summary detected")

                                success = send_summary(user_id, summary)

                                # ALWAYS mark as seen (success or failure) to prevent infinite retry
                                summary_hash = get_summary_hash(summary)
                                seen_summaries.add(summary_hash)

                                if not success:
                                    logger.warning(f"Failed to send summary, marked as seen to prevent retry: {summary_hash[:20]}...")

                    # Save state (only track seen summaries, not buffer position)
                    state["last_summaries"] = list(seen_summaries)  # Keep all seen hashes
                    save_state(state)

                # Wait for next poll
                time.sleep(interval)

            except KeyboardInterrupt:
                logger.info("Monitor stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in monitor loop: {e}", exc_info=True)
                time.sleep(interval)
    finally:
        # Always clean up PID file on exit
        remove_pid_file()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Telegram Monitor - Auto-send session summaries")
    parser.add_argument("--interval", type=int, default=300, help="Polling interval in seconds (default: 300)")
    parser.add_argument("--tmux-session", type=str, default="0", help="Tmux session to monitor (default: 0)")
    parser.add_argument("--force", action="store_true", help="Force start even if another instance is running")

    args = parser.parse_args()

    # Check if another instance is already running (unless --force specified)
    if not args.force and check_existing_process():
        logger.error("Another A-C-Gee monitor is already running")
        logger.error("Use --force to start anyway, or use restart_telegram_monitor.sh")
        return 1

    # Load config
    config = load_config()
    if not config:
        logger.error("Failed to load config, exiting")
        return 1

    # Get Corey's user ID
    authorized_users = config.get("authorized_users", {})
    if not authorized_users:
        logger.error("No authorized users in config")
        return 1

    # Get first authorized user (Corey)
    user_id = int(list(authorized_users.keys())[0])

    # Start monitoring
    monitor_loop(args.interval, args.tmux_session, user_id)

    return 0


if __name__ == "__main__":
    exit(main())
