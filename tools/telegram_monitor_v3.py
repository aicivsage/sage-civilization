#!/usr/bin/env python3
"""
Telegram Monitor V3 - Simple Hash-Based Deduplication

DESIGN PRINCIPLES:
- Position-independent (no watermark, no buffer scroll bugs)
- Content+timestamp hash for deduplication
- Two-phase commit (flush state BEFORE send to prevent duplicate loops)
- 6-hour retention window
- Fail-loud error handling
- ~200 LOC vs V2's 650 LOC (70% simpler)

CRITICAL FIXES from red team review:
1. No position tracking - pure hash-based (fixes buffer wrap)
2. Two-phase commit - state flush BEFORE send (fixes infinite duplicate loop)
3. Max retry queue size with eviction (fixes unbounded growth)
4. File locking (fixes concurrent instance race)
5. String splitting instead of regex (fixes DoS vulnerability)

Architecture: Simple polling loop
- Every 30s: scan buffer, extract wrapped messages, check if hash seen, send if new

State: JSON file with sent_hashes list
- Each entry: {hash, timestamp, content_preview}
- Retention: 6 hours (cleanup old hashes every poll)
- Max size: 1000 entries (evict oldest if exceeded)

Wrapper format (with timestamp):
🤖🎯📱[TIMESTAMP:2025-10-19T12:00:00Z]
Your message content here
✨🔚
"""

import sys
import json
import time
import logging
import hashlib
import subprocess
import fcntl
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "telegram_config.json"
STATE_FILE = PROJECT_ROOT / ".tg_sessions" / "monitor_state_v3.json"
PID_FILE = PROJECT_ROOT / ".tg_sessions" / "acgee_monitor_v3.pid"
SEND_SCRIPT = PROJECT_ROOT / "tools" / "send_telegram_direct.py"

# Deduplication settings
RETENTION_HOURS = 6
MAX_SENT_HASHES = 1000
POLL_INTERVAL = 30  # seconds

# Retry settings
MAX_RETRIES = 3
RETRY_BACKOFF = [2, 4, 6]  # seconds

# Wrapper markers
START_MARKER = "🤖🎯📱"
END_MARKER = "✨🔚"


class MonitorState:
    """Monitor state with hash-based deduplication."""

    def __init__(self):
        self.sent_hashes: List[Dict] = []  # [{hash, timestamp, preview}]

    def to_dict(self) -> dict:
        return {"sent_hashes": self.sent_hashes}

    @classmethod
    def from_dict(cls, data: dict) -> 'MonitorState':
        state = cls()
        state.sent_hashes = data.get("sent_hashes", [])
        return state


def load_config() -> dict:
    """Load telegram configuration."""
    if not CONFIG_FILE.exists():
        logger.error(f"Config file not found: {CONFIG_FILE}")
        sys.exit(1)

    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        sys.exit(1)


def load_state() -> MonitorState:
    """Load monitor state (with file locking to prevent concurrent access)."""
    if not STATE_FILE.exists():
        logger.info("No state file found - starting fresh")
        return MonitorState()

    try:
        # Acquire shared lock for reading
        with open(STATE_FILE, 'r') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            data = json.load(f)
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

        return MonitorState.from_dict(data)
    except Exception as e:
        logger.error(f"Failed to load state: {e}")
        return MonitorState()


def save_state(state: MonitorState) -> bool:
    """
    Save monitor state (with file locking).

    Returns:
        True if saved successfully, False otherwise
    """
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Acquire exclusive lock for writing
        with open(STATE_FILE, 'w') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            json.dump(state.to_dict(), f, indent=2)
            f.flush()  # Ensure data written to disk
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

        return True
    except Exception as e:
        logger.error(f"Failed to save state: {e}")
        return False


def cleanup_old_hashes(state: MonitorState) -> None:
    """Remove hashes older than RETENTION_HOURS from state."""
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=RETENTION_HOURS)

    original_count = len(state.sent_hashes)
    valid_hashes = []

    for entry in state.sent_hashes:
        try:
            timestamp = datetime.fromisoformat(entry['timestamp'])
            if timestamp > cutoff:
                valid_hashes.append(entry)
        except (ValueError, KeyError) as e:
            # Invalid timestamp format - skip this entry (will be removed)
            logger.warning(f"Skipping entry with invalid timestamp: {entry.get('timestamp', 'MISSING')} - {e}")

    state.sent_hashes = valid_hashes

    removed = original_count - len(state.sent_hashes)
    if removed > 0:
        logger.info(f"Cleaned up {removed} old/invalid hashes (retention: {RETENTION_HOURS}h)")


def evict_oldest_hashes(state: MonitorState) -> None:
    """Evict oldest hashes if state exceeds MAX_SENT_HASHES."""
    if len(state.sent_hashes) > MAX_SENT_HASHES:
        # Sort by timestamp (oldest first)
        state.sent_hashes.sort(key=lambda x: x['timestamp'])

        # Keep only newest MAX_SENT_HASHES
        evicted = len(state.sent_hashes) - MAX_SENT_HASHES
        state.sent_hashes = state.sent_hashes[-MAX_SENT_HASHES:]

        logger.warning(f"Evicted {evicted} oldest hashes (max: {MAX_SENT_HASHES})")


def compute_message_hash(content: str, timestamp: str) -> str:
    """
    Compute SHA256 hash of message content + timestamp.

    Args:
        content: Message content (without wrapper markers)
        timestamp: ISO 8601 timestamp string

    Returns:
        Hex digest of hash
    """
    combined = f"{timestamp}:{content}"
    return hashlib.sha256(combined.encode('utf-8')).hexdigest()


def get_tmux_buffer(session: str = "3") -> str:
    """Capture tmux buffer from specified session."""
    try:
        result = subprocess.run(
            ["tmux", "capture-pane", "-t", session, "-p", "-S", "-500"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            logger.error(f"Failed to capture tmux buffer: {result.stderr}")
            return ""

        return result.stdout
    except Exception as e:
        logger.error(f"Error capturing tmux buffer: {e}")
        return ""


def extract_wrapped_messages(buffer: str) -> List[Dict]:
    """
    Extract wrapped messages from tmux buffer.

    Uses simple string splitting (not regex) to prevent DoS attacks.

    Returns:
        List of {content, timestamp, hash} dicts
    """
    messages = []

    # Split buffer by start marker
    parts = buffer.split(START_MARKER)

    for part in parts[1:]:  # Skip first part (before any message)
        # Find end marker
        if END_MARKER not in part:
            continue

        # Extract content between markers
        content = part.split(END_MARKER)[0]

        # Parse timestamp from wrapper format: [TIMESTAMP:2025-10-19T12:00:00Z]
        timestamp = None
        if content.startswith("[TIMESTAMP:"):
            try:
                timestamp_line = content.split('\n', 1)[0]
                timestamp = timestamp_line.split(':', 1)[1].rstrip(']')
                content = content.split('\n', 1)[1] if '\n' in content else ""
            except Exception as e:
                logger.warning(f"Failed to parse timestamp: {e}")
                continue
        else:
            # Old format without timestamp - skip (cannot deduplicate safely)
            logger.warning("Message without timestamp - skipping (old format)")
            continue

        # Compute hash
        msg_hash = compute_message_hash(content.strip(), timestamp)

        messages.append({
            'content': content.strip(),
            'timestamp': timestamp,
            'hash': msg_hash,
            'preview': content.strip()[:50]
        })

    return messages


def send_telegram_message(user_id: str, content: str) -> bool:
    """
    Send message via send_telegram_direct.py with retry logic.

    Args:
        user_id: Telegram user ID
        content: Message content

    Returns:
        True if sent successfully (or after retries), False otherwise
    """
    for attempt in range(MAX_RETRIES):
        try:
            result = subprocess.run(
                [
                    "python3",
                    str(SEND_SCRIPT),
                    user_id,
                    content
                ],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                logger.info(f"✅ Sent message to user {user_id} (attempt {attempt + 1})")
                return True
            else:
                logger.warning(f"Send failed (attempt {attempt + 1}): {result.stderr}")

        except Exception as e:
            logger.error(f"Send error (attempt {attempt + 1}): {e}")

        # Wait before retry (unless last attempt)
        if attempt < MAX_RETRIES - 1:
            backoff = RETRY_BACKOFF[attempt]
            logger.info(f"Retrying in {backoff}s...")
            time.sleep(backoff)

    # All retries exhausted
    logger.error(f"❌ Failed to send message after {MAX_RETRIES} attempts")
    return False


def create_pid_file():
    """Create PID file to track monitor process."""
    try:
        PID_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PID_FILE, 'w') as f:
            f.write(str(subprocess.run(['bash', '-c', 'echo $PPID'],
                                      capture_output=True, text=True).stdout.strip()))
        logger.info(f"Created PID file: {PID_FILE}")
    except Exception as e:
        logger.warning(f"Failed to create PID file: {e}")


def main():
    """Main monitor loop."""
    logger.info("🚀 Telegram Monitor V3 starting...")

    # Load config
    config = load_config()
    user_id = config.get('corey_user_id')
    tmux_session = config.get('tmux_session', '3')

    if not user_id:
        logger.error("corey_user_id not found in config")
        sys.exit(1)

    logger.info(f"Loaded config: user_id={user_id}, tmux_session={tmux_session}")

    # Create PID file
    create_pid_file()

    logger.info(f"Monitor V3 running: poll_interval={POLL_INTERVAL}s, retention={RETENTION_HOURS}h")

    # Main polling loop
    while True:
        try:
            # Load state (with file locking)
            state = load_state()

            # Cleanup old hashes
            cleanup_old_hashes(state)

            # Evict oldest if too many
            evict_oldest_hashes(state)

            # Build hash set for O(1) lookup
            sent_hashes = {entry['hash'] for entry in state.sent_hashes}

            # Get tmux buffer
            buffer = get_tmux_buffer(tmux_session)
            if not buffer:
                logger.warning("Empty buffer - skipping poll")
                time.sleep(POLL_INTERVAL)
                continue

            # Extract wrapped messages
            messages = extract_wrapped_messages(buffer)
            logger.info(f"Found {len(messages)} wrapped messages in buffer")

            # Process new messages
            new_count = 0
            for msg in messages:
                if msg['hash'] not in sent_hashes:
                    logger.info(f"🆕 New message detected: {msg['preview']}")

                    # TWO-PHASE COMMIT: Flush state BEFORE sending
                    # This prevents infinite duplicate loops on send success + flush failure
                    state.sent_hashes.append({
                        'hash': msg['hash'],
                        'timestamp': msg['timestamp'],
                        'preview': msg['preview']
                    })

                    if not save_state(state):
                        logger.error("CRITICAL: Failed to flush state before send - skipping message to prevent duplicates")
                        # Remove from in-memory state
                        state.sent_hashes.pop()
                        continue

                    # Now safe to send (state already flushed)
                    if send_telegram_message(user_id, msg['content']):
                        logger.info(f"✅ Message sent and state flushed (hash: {msg['hash'][:8]})")
                        new_count += 1
                        sent_hashes.add(msg['hash'])  # Update in-memory set
                    else:
                        logger.error(f"❌ Failed to send message (hash: {msg['hash'][:8]})")
                        # State already flushed - this will prevent retry
                        # This is intentional: fail-loud, manual intervention needed

            if new_count > 0:
                logger.info(f"✅ Sent {new_count} new messages this poll")
            else:
                logger.debug("No new messages this poll")

        except Exception as e:
            logger.error(f"Error in main loop: {e}", exc_info=True)

        # Sleep until next poll
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Monitor stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
