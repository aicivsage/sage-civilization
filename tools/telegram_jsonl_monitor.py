#!/usr/bin/env python3
"""
JSONL Wrapper Monitor - Watches Claude Code conversation logs for wrapped messages

🚨🚨🚨 PRODUCTION FILE - DO NOT MODIFY DIRECTLY 🚨🚨🚨

THIS FILE IS BATTLE-TESTED AND WORKING AFTER 3 DAYS OF DEBUGGING (Oct 17-20, 2025)

NEVER:
- Modify this file directly for "improvements" or "refactoring"
- Overwrite with experimental versions
- Change without full backup and testing

ONLY:
- Back up before ANY changes (tar.gz with timestamp)
- Create v2/v3 experimental versions in separate files
- Test experimental versions completely before replacing
- Update telegram_script_registry.json when changing

This file took 3 days to get working. Treat it with respect.

Architecture:
- Watches JSONL file in Claude Code projects directory
- Detects messages wrapped with 🤖🎯📱 ... ✨🔚 markers
- Sends to Telegram via send_telegram_plain.py with Markdown formatting
- Tracks sent messages to prevent duplicates via deduplication hashes
- Handles session rotation (auto-detect or explicit --session-file)
- Runs as ACG_telegram_jsonl_monitor process

Usage:
    python3 tools/telegram_jsonl_monitor.py [--dry-run] [--verbose] [--start-from-now] [--session-file FILENAME]

    --session-file: Explicitly specify which JSONL file to watch (e.g., d68b9236-9f39-4379-ba85-b3c5348609b4.jsonl)
                    Required when multiple Claude instances running (e.g., A-C-Gee + Weaver)
                    Skips auto-detection and watches specified file only

Configuration:
    config/telegram_config.json (jsonl_monitor section)

State File:
    .tg_sessions/jsonl_monitor_state.json

Logs:
    /tmp/telegram_jsonl_monitor.log (main log)
    /tmp/telegram_jsonl_monitor_error.log (errors only)

Registry: memories/agents/tg-archi/telegram_script_registry.json

Author: coder (AI-CIV A-C-Gee Civilization)
Date: 2025-10-20
Status: PRODUCTION (ACG_ naming + explicit session support)
"""

import sys
import os
import json
import time
import hashlib
import logging
import subprocess
import signal
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Set
import argparse

# Configuration paths
PROJECT_ROOT = Path("/mnt/c/sage/sage-civilization")
CONFIG_FILE = PROJECT_ROOT / "config/telegram_config.json"
STATE_FILE = PROJECT_ROOT / ".tg_sessions/jsonl_monitor_state.json"
LOG_FILE = Path("/tmp/telegram_jsonl_monitor.log")
ERROR_LOG_FILE = Path("/tmp/telegram_jsonl_monitor_error.log")

# Default configuration
DEFAULT_CONFIG = {
    "enabled": True,
    "claude_code_projects_dir": str(Path.home() / ".claude/projects"),
    "project_name": "-mnt-c-sage-sage-civilization",
    "poll_interval_seconds": 3,
    "wrapper_markers": {
        "start": "🤖🎯📱",
        "end": "✨🔚"
    },
    "sender_script": "tools/send_telegram_plain.py",
    "max_message_length": 4096,
    "deduplication_enabled": True,
    "session_rotation_check_interval": 60
}

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("telegram_jsonl_monitor")

# Error-only logger
error_logger = logging.getLogger("telegram_jsonl_monitor_errors")
error_handler = logging.FileHandler(ERROR_LOG_FILE)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
error_logger.addHandler(error_handler)
error_logger.setLevel(logging.ERROR)


class JSONLMonitorState:
    """Tracks monitor state across restarts"""

    def __init__(self, state_file: Path, start_from_now: bool = False, session_file: Optional[Path] = None):
        self.state_file = state_file
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.start_from_now = start_from_now
        self.session_file = session_file
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Load state from file or create new"""
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    state = json.load(f)
                    logger.info(f"Loaded existing state (last offset: {state.get('last_processed_offset', 0)})")
                    return state
            except Exception as e:
                logger.warning(f"Failed to load state file: {e}, starting fresh")
                error_logger.error(f"State file corrupt: {e}")

        # No existing state file - create fresh state
        state = {
            "last_updated": datetime.now().isoformat(),
            "current_session_file": None,
            "last_processed_offset": 0,
            "sent_message_hashes": [],
            "session_history": []
        }

        # If --start-from-now flag is set, initialize offset to current file size
        if self.start_from_now and self.session_file and self.session_file.exists():
            try:
                file_size = self.session_file.stat().st_size
                state["last_processed_offset"] = file_size
                logger.info(f"--start-from-now: Skipping {file_size} bytes of existing content")
                logger.info(f"Will only process messages written after monitor startup")
            except Exception as e:
                logger.warning(f"Failed to get file size for --start-from-now: {e}")
                error_logger.error(f"--start-from-now failed: {e}")

        return state

    def save_state(self):
        """Save state to file"""
        self.state["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, indent=2, fp=f)
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
            error_logger.error(f"Failed to save state: {e}")

    def mark_message_sent(self, message_hash: str, content_preview: str):
        """Mark message as sent to prevent duplicates"""
        if message_hash not in self.state["sent_message_hashes"]:
            self.state["sent_message_hashes"].append(message_hash)
            # Keep only last 1000 hashes (prevent unbounded growth)
            if len(self.state["sent_message_hashes"]) > 1000:
                self.state["sent_message_hashes"] = self.state["sent_message_hashes"][-1000:]
            logger.debug(f"Marked message as sent: {content_preview[:50]}...")

    def is_message_sent(self, message_hash: str) -> bool:
        """Check if message was already sent"""
        return message_hash in self.state["sent_message_hashes"]

    def update_session_file(self, session_file: Path):
        """Update current session file"""
        old_file = self.state.get("current_session_file")
        self.state["current_session_file"] = str(session_file)
        self.state["last_processed_offset"] = 0  # Reset offset for new file

        if old_file and old_file != str(session_file):
            logger.info(f"Session rotation: {Path(old_file).name} → {session_file.name}")
            # Archive old session in history
            self.state["session_history"].append({
                "file": old_file,
                "ended_at": datetime.now().isoformat()
            })
            # Keep only last 10 sessions
            if len(self.state["session_history"]) > 10:
                self.state["session_history"] = self.state["session_history"][-10:]

    def get_last_offset(self) -> int:
        """Get last processed file offset"""
        return self.state.get("last_processed_offset", 0)

    def update_offset(self, offset: int):
        """Update last processed offset"""
        self.state["last_processed_offset"] = offset


class JSONLWrapperMonitor:
    """Main monitor class"""

    def __init__(self, config: Dict, dry_run: bool = False, verbose: bool = False, start_from_now: bool = False, explicit_session_file: Optional[str] = None):
        self.config = config
        self.dry_run = dry_run
        self.verbose = verbose
        self.start_from_now = start_from_now
        self.explicit_session_file = explicit_session_file
        self.state = None  # Will be initialized after finding session file
        self.running = True
        self.last_activity = datetime.now()
        self.last_config_check = datetime.now()
        self.config_mtime = CONFIG_FILE.stat().st_mtime if CONFIG_FILE.exists() else 0

        # Set log level
        if verbose:
            logger.setLevel(logging.DEBUG)

        logger.info("=" * 60)
        logger.info("JSONL Wrapper Monitor starting")
        logger.info(f"Mode: {'DRY-RUN' if dry_run else 'PRODUCTION'}")
        logger.info(f"Start from now: {start_from_now}")
        logger.info(f"Explicit session: {explicit_session_file if explicit_session_file else 'AUTO-DETECT'}")
        logger.info(f"Projects dir: {self.config['claude_code_projects_dir']}")
        logger.info(f"Project: {self.config['project_name']}")
        logger.info("=" * 60)

    def find_current_session_file(self) -> Optional[Path]:
        """Find the most recently modified JSONL file for this project with growth validation"""
        try:
            projects_dir = Path(self.config["claude_code_projects_dir"])
            project_dir = projects_dir / self.config["project_name"]

            if not project_dir.exists():
                logger.error(f"Project directory not found: {project_dir}")
                return None

            # If explicit session file specified, use it directly
            if self.explicit_session_file:
                explicit_path = project_dir / self.explicit_session_file
                if explicit_path.exists():
                    logger.info(f"Using explicit session file: {self.explicit_session_file}")
                    return explicit_path
                else:
                    logger.error(f"Explicit session file not found: {explicit_path}")
                    return None

            jsonl_files = list(project_dir.glob("*.jsonl"))
            if not jsonl_files:
                logger.warning(f"No JSONL files found in {project_dir}")
                return None

            # Filter: only files modified in last 5 minutes
            recent_threshold = datetime.now() - timedelta(minutes=5)
            candidates = [
                f for f in jsonl_files
                if datetime.fromtimestamp(f.stat().st_mtime) > recent_threshold
            ]

            if not candidates:
                # No recent activity, return most recent overall
                current = max(jsonl_files, key=lambda p: p.stat().st_mtime)
                logger.debug(f"Current session file (no recent activity): {current.name}")
                return current

            # Single candidate - no ambiguity
            if len(candidates) == 1:
                logger.debug(f"Current session file (single candidate): {candidates[0].name}")
                return candidates[0]

            # Multiple candidates: verify which is actively growing
            logger.info(f"Multiple active sessions detected ({len(candidates)}), testing growth...")

            # Record sizes
            sizes_before = {f: f.stat().st_size for f in candidates}

            # Log candidate files
            for f in candidates:
                logger.info(f"  Candidate: {f.name} ({sizes_before[f]:,} bytes)")

            # Wait 3 seconds
            time.sleep(3)

            # Record sizes after
            sizes_after = {f: f.stat().st_size for f in candidates}

            # Calculate growth
            growth = {f: sizes_after[f] - sizes_before[f] for f in candidates}

            # Find file that grew the most
            active_file = max(growth, key=growth.get)

            logger.info(f"Active session: {active_file.name} (grew {growth[active_file]:,} bytes in 3s)")
            for f in candidates:
                if f != active_file:
                    logger.info(f"  Inactive: {f.name} (grew {growth[f]:,} bytes)")

            return active_file

        except Exception as e:
            logger.error(f"Error finding session file: {e}")
            error_logger.error(f"Error finding session file: {e}")
            return None

    def extract_wrapped_message(self, text: str) -> Optional[str]:
        """Extract message between wrapper markers"""
        start_marker = self.config["wrapper_markers"]["start"]
        end_marker = self.config["wrapper_markers"]["end"]

        if start_marker not in text or end_marker not in text:
            return None

        try:
            start_idx = text.index(start_marker) + len(start_marker)
            end_idx = text.index(end_marker, start_idx)
            message = text[start_idx:end_idx].strip()
            return message if message else None
        except (ValueError, IndexError):
            return None

    def compute_message_hash(self, message: str) -> str:
        """Compute hash for deduplication"""
        return hashlib.sha256(message.encode()).hexdigest()[:16]

    def send_to_telegram(self, user_id: int, message: str, max_retries: int = 3) -> bool:
        """Send message to Telegram with retry logic"""
        if self.dry_run:
            logger.info(f"[DRY-RUN] Would send to {user_id}: {message[:100]}...")
            return True

        sender_script = PROJECT_ROOT / self.config["sender_script"]

        if not sender_script.exists():
            logger.error(f"Sender script not found: {sender_script}")
            error_logger.error(f"Sender script missing: {sender_script}")
            return False

        # Truncate if too long
        max_length = self.config["max_message_length"]
        if len(message) > max_length:
            message = message[:max_length - 50] + "\n\n[Message truncated]"

        for attempt in range(max_retries):
            try:
                result = subprocess.run(
                    ["python3", str(sender_script), str(user_id), message, "--markdown"],
                    capture_output=True,
                    timeout=30,
                    text=True
                )

                if result.returncode == 0:
                    logger.info(f"Message sent successfully (attempt {attempt + 1})")
                    return True

                logger.warning(f"Send failed (attempt {attempt + 1}/{max_retries}): {result.stderr}")

                # Exponential backoff: 2s, 4s, 8s
                if attempt < max_retries - 1:
                    backoff_seconds = 2 ** attempt
                    logger.info(f"Retrying in {backoff_seconds}s...")
                    time.sleep(backoff_seconds)

            except subprocess.TimeoutExpired:
                logger.warning(f"Send timeout (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)

            except Exception as e:
                logger.error(f"Send exception (attempt {attempt + 1}/{max_retries}): {e}")
                error_logger.error(f"Send exception: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)

        # All retries exhausted
        logger.error(f"Message send failed after {max_retries} attempts")
        error_logger.error(f"Failed to send: {message[:200]}")
        return False

    def process_jsonl_line(self, line: str, user_id: int) -> bool:
        """Process a single JSONL line, return True if message sent"""
        try:
            data = json.loads(line)

            # Only process assistant messages
            if data.get("type") != "message" and "message" not in data:
                return False

            message_obj = data.get("message", {})
            if message_obj.get("role") != "assistant":
                return False

            # Extract text content
            content = message_obj.get("content", [])
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                text = " ".join([
                    item.get("text", "")
                    for item in content
                    if isinstance(item, dict) and item.get("type") == "text"
                ])
            else:
                return False

            # Check for wrapper markers
            wrapped_message = self.extract_wrapped_message(text)
            if not wrapped_message:
                return False

            logger.info(f"Wrapper detected: {wrapped_message[:80]}...")

            # Deduplication check
            if self.config["deduplication_enabled"]:
                message_hash = self.compute_message_hash(wrapped_message)
                if self.state.is_message_sent(message_hash):
                    logger.debug(f"Message already sent (hash: {message_hash}), skipping")
                    return False

            # Send to Telegram
            if self.send_to_telegram(user_id, wrapped_message):
                if self.config["deduplication_enabled"]:
                    self.state.mark_message_sent(message_hash, wrapped_message)
                return True

            return False

        except json.JSONDecodeError as e:
            logger.debug(f"Invalid JSON line: {e}")
            return False
        except Exception as e:
            logger.error(f"Error processing line: {e}")
            error_logger.error(f"Line processing error: {e}\nLine: {line[:200]}")
            return False

    def check_config_reload(self):
        """Check if config file changed and reload if needed"""
        try:
            if not CONFIG_FILE.exists():
                return

            current_mtime = CONFIG_FILE.stat().st_mtime
            if current_mtime > self.config_mtime:
                logger.info("Config file changed, reloading...")
                new_config = load_config()

                # Only reload safe settings (not structural ones)
                safe_reload_keys = [
                    "poll_interval_seconds",
                    "max_message_length",
                    "deduplication_enabled",
                    "session_rotation_check_interval"
                ]

                for key in safe_reload_keys:
                    if key in new_config:
                        old_val = self.config.get(key)
                        new_val = new_config.get(key)
                        if old_val != new_val:
                            self.config[key] = new_val
                            logger.info(f"Reloaded config: {key} = {new_val}")

                self.config_mtime = current_mtime

        except Exception as e:
            logger.warning(f"Config reload failed: {e}")

    def watch_session_file(self, session_file: Path, user_id: int):
        """Watch a single session file for new lines"""
        try:
            # Update state with current file
            if str(session_file) != self.state.state.get("current_session_file"):
                self.state.update_session_file(session_file)

            # Get starting offset
            start_offset = self.state.get_last_offset()

            with open(session_file, 'r') as f:
                # Seek to last position
                f.seek(start_offset)

                while self.running:
                    line = f.readline()

                    if line:
                        # Process line
                        message_sent = self.process_jsonl_line(line, user_id)
                        if message_sent:
                            self.last_activity = datetime.now()

                        # Update offset after processing each line
                        current_offset = f.tell()
                        self.state.update_offset(current_offset)

                        # CRITICAL FIX: Save state after processing (prevents offset reversion on restart)
                        # Previously state was only saved during idle periods, causing offset to never persist
                        # when monitor was actively processing messages
                        if message_sent:
                            self.state.save_state()
                            logger.debug(f"State saved at offset {current_offset}")
                    else:
                        # No new data, sleep and check for rotation
                        time.sleep(self.config["poll_interval_seconds"])

                        # Check if should rotate to new session
                        if datetime.now() - self.last_activity > timedelta(seconds=self.config["session_rotation_check_interval"]):
                            new_session = self.find_current_session_file()
                            if new_session and new_session != session_file:
                                logger.info(f"Detected new session: {new_session.name}")
                                self.state.save_state()
                                return new_session  # Signal rotation

                        # Check config reload periodically
                        if datetime.now() - self.last_config_check > timedelta(seconds=60):
                            self.check_config_reload()
                            self.last_config_check = datetime.now()

                        # Save state periodically
                        self.state.save_state()

        except Exception as e:
            logger.error(f"Error watching session file: {e}")
            error_logger.error(f"Watch error: {e}")
            return None

    def run(self):
        """Main run loop"""
        if not self.config["enabled"]:
            logger.info("Monitor disabled in config, exiting")
            return

        user_id = int(self.config.get("corey_user_id", "437939400"))

        # Find current session file FIRST (needed for state initialization)
        session_file = self.find_current_session_file()
        if not session_file:
            logger.error("No session file found on startup, cannot continue")
            return

        # Initialize state (will apply --start-from-now if flag set and no existing state)
        self.state = JSONLMonitorState(STATE_FILE, start_from_now=self.start_from_now, session_file=session_file)

        while self.running:
            # Re-find current session file
            session_file = self.find_current_session_file()

            if not session_file:
                logger.warning("No session file found, will retry in 60s")
                time.sleep(60)
                continue

            logger.info(f"Watching: {session_file.name}")

            # Watch until rotation or error
            result = self.watch_session_file(session_file, user_id)

            if result:  # New session file detected
                session_file = result
            elif not self.running:  # Shutdown signal
                break
            else:  # Error, retry after delay
                logger.warning("Watch interrupted, retrying in 30s")
                time.sleep(30)

        logger.info("Monitor shutting down")
        self.state.save_state()

    def shutdown(self, signum, frame):
        """Graceful shutdown handler"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False


def load_config() -> Dict:
    """Load configuration from file with defaults"""
    config = DEFAULT_CONFIG.copy()

    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                user_config = json.load(f)

            # Merge jsonl_monitor section if exists
            if "jsonl_monitor" in user_config:
                config.update(user_config["jsonl_monitor"])

            # Also copy corey_user_id from root
            if "corey_user_id" in user_config:
                config["corey_user_id"] = user_config["corey_user_id"]

        except Exception as e:
            logger.warning(f"Failed to load config, using defaults: {e}")

    return config


def main():
    """Entry point"""
    # Set process name to distinguish from Weaver's processes
    try:
        import setproctitle
        setproctitle.setproctitle("ACG_telegram_jsonl_monitor")
    except ImportError:
        pass  # setproctitle not available, skip naming

    parser = argparse.ArgumentParser(description="JSONL Wrapper Monitor for Telegram")
    parser.add_argument("--dry-run", action="store_true", help="Detect wrappers but don't send")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    parser.add_argument("--start-from-now", action="store_true",
                        help="Skip existing messages, only process new messages written after startup (ignored if state file exists)")
    parser.add_argument("--session-file", type=str, default=None,
                        help="Explicit session file to monitor (skips auto-detection). Example: d68b9236-9f39-4379-ba85-b3c5348609b4.jsonl")
    args = parser.parse_args()

    # Load config
    config = load_config()

    # Create monitor
    monitor = JSONLWrapperMonitor(config, dry_run=args.dry_run, verbose=args.verbose, start_from_now=args.start_from_now, explicit_session_file=args.session_file)

    # Register signal handlers
    signal.signal(signal.SIGTERM, monitor.shutdown)
    signal.signal(signal.SIGINT, monitor.shutdown)

    # Run
    try:
        monitor.run()
    except Exception as e:
        logger.error(f"Monitor crashed: {e}")
        error_logger.error(f"Monitor crashed: {e}")
        raise


if __name__ == "__main__":
    main()
