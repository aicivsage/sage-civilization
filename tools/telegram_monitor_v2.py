#!/usr/bin/env python3
# =============================================================================
# Telegram Monitor V2 - Event-Driven Watermark Architecture
# =============================================================================
"""
Telegram Monitor V2 - Watermark-based message detection and delivery.

Architecture: ADR-001-telegram-monitor-v2-event-driven-architecture.md

Key improvements over V1:
- Watermark-based deduplication (not hash-based)
- Retry queue with exponential backoff
- Zero message loss guarantee
- Fail-loud error handling
- Graceful restart support

Usage:
    python3 tools/telegram_monitor_v2.py [--interval SECONDS] [--tmux-session SESSION]

    --interval: Polling interval in seconds (default: 30)
    --tmux-session: Tmux session to monitor (default: "0")

Detection markers:
    🤖🎯📱
    ...content...
    ✨🔚
"""
import argparse
import hashlib
import json
import logging
import os
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
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
STATE_FILE = PROJECT_ROOT / ".tg_sessions" / "monitor_state_v2.json"
PID_FILE = PROJECT_ROOT / ".tg_sessions" / "acgee_monitor_v2.pid"
SEND_SCRIPT = PROJECT_ROOT / "tools" / "send_telegram_direct.py"

# Summary markers
START_MARKER = "🤖🎯📱"
END_MARKER = "✨🔚"

# Retry configuration
MAX_RETRIES = 5
INITIAL_BACKOFF_SECONDS = 30
MAX_BACKOFF_SECONDS = 3600  # 1 hour


# =============================================================================
# Data Models
# =============================================================================

@dataclass
class Message:
    """Represents a wrapped message detected in tmux buffer."""
    id: str
    content: str
    timestamp: str
    position: int  # Line number in buffer where message starts
    attempts: int = 0

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'Message':
        return Message(**data)


@dataclass
class RetryEntry:
    """Represents a message in the retry queue."""
    message: Message
    next_retry: str  # ISO format datetime
    backoff_seconds: int

    def to_dict(self) -> dict:
        return {
            'message': self.message.to_dict(),
            'next_retry': self.next_retry,
            'backoff_seconds': self.backoff_seconds
        }

    @staticmethod
    def from_dict(data: dict) -> 'RetryEntry':
        return RetryEntry(
            message=Message.from_dict(data['message']),
            next_retry=data['next_retry'],
            backoff_seconds=data['backoff_seconds']
        )


@dataclass
class State:
    """Monitor state with watermark and retry queue."""
    watermark: int  # Last processed buffer position
    retry_queue: List[RetryEntry]
    dead_letter: List[Dict]
    last_health_check: str

    def to_dict(self) -> dict:
        return {
            'watermark': self.watermark,
            'retry_queue': [entry.to_dict() for entry in self.retry_queue],
            'dead_letter': self.dead_letter,
            'last_health_check': self.last_health_check
        }

    @staticmethod
    def from_dict(data: dict) -> 'State':
        return State(
            watermark=data.get('watermark', 0),
            retry_queue=[RetryEntry.from_dict(e) for e in data.get('retry_queue', [])],
            dead_letter=data.get('dead_letter', []),
            last_health_check=data.get('last_health_check', datetime.now().isoformat())
        )


class CircuitBreaker:
    """Circuit breaker for consecutive Telegram API failures."""

    def __init__(self, threshold: int = 5):
        self.failures = 0
        self.threshold = threshold
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.last_failure_time = None

    def record_success(self):
        """Record successful send - reset failures."""
        self.failures = 0
        self.state = "CLOSED"

    def record_failure(self):
        """Record failed send - increment failures."""
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.threshold:
            self.state = "OPEN"
            logger.error(f"Circuit breaker OPEN - {self.failures} consecutive failures")

    def can_send(self) -> bool:
        """Check if we can attempt to send."""
        if self.state == "OPEN":
            # Try half-open after 5 minutes
            if self.last_failure_time and time.time() - self.last_failure_time > 300:
                logger.info("Circuit breaker entering HALF_OPEN state")
                self.state = "HALF_OPEN"
                return True
            logger.warning("Circuit breaker OPEN - skipping send")
            return False
        return True


# =============================================================================
# Core Functions
# =============================================================================

def calculate_message_id(content: str, position: int) -> str:
    """
    Generate stable message ID from content + buffer position.

    Args:
        content: Message content
        position: Line number in buffer where message starts

    Returns:
        16-character hex hash
    """
    combined = f"{position}:{content}"
    return hashlib.sha256(combined.encode()).hexdigest()[:16]


def extract_position_from_id(message_id: str, content: str) -> int:
    """
    Extract buffer position from message ID.

    This is a reverse lookup - not perfect but sufficient for watermark logic.
    We'll store position explicitly in Message dataclass instead.
    """
    # NOTE: Position is stored in Message.position, this function not needed
    raise NotImplementedError("Use Message.position instead")


def get_tmux_buffer(session: str = "0") -> Optional[str]:
    """
    Capture tmux buffer content.

    Args:
        session: Tmux session name or number

    Returns:
        Buffer content as string, or None on failure
    """
    try:
        result = subprocess.run(
            ["tmux", "capture-pane", "-t", session, "-p", "-S", "-500"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to capture tmux buffer: {e}")
        return None
    except FileNotFoundError:
        logger.error("tmux not found - is it installed?")
        return None


def extract_summaries(buffer: str) -> List[Message]:
    """
    Extract wrapped messages from tmux buffer.

    Args:
        buffer: Tmux buffer content

    Returns:
        List of Message objects with IDs, content, timestamps, positions
    """
    messages = []
    lines = buffer.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i]

        if START_MARKER in line:
            # Found start marker - capture position
            start_position = i
            content_lines = []
            i += 1
            found_end = False

            # Collect content until end marker
            while i < len(lines):
                if END_MARKER in lines[i]:
                    found_end = True
                    break
                content_lines.append(lines[i])
                i += 1

            # Create message only if we found both start and end markers
            if content_lines and found_end:
                content = '\n'.join(content_lines).strip()
                message_id = calculate_message_id(content, start_position)
                timestamp = datetime.now().isoformat()

                message = Message(
                    id=message_id,
                    content=content,
                    timestamp=timestamp,
                    position=start_position,
                    attempts=0
                )
                messages.append(message)

        i += 1

    return messages


def filter_new_messages(messages: List[Message], watermark: int) -> List[Message]:
    """
    Filter messages to only those after watermark position.

    Args:
        messages: All messages detected in buffer
        watermark: Last processed buffer position

    Returns:
        Messages with position > watermark
    """
    new_messages = [msg for msg in messages if msg.position > watermark]
    if new_messages:
        logger.info(f"Filtered {len(new_messages)} new messages (watermark: {watermark})")
    return new_messages


def send_telegram_message(message: Message, user_id: str) -> bool:
    """
    Send message to Telegram.

    Args:
        message: Message to send
        user_id: Telegram user ID

    Returns:
        True if sent successfully, False otherwise
    """
    try:
        result = subprocess.run(
            [
                "python3",
                str(SEND_SCRIPT),
                user_id,
                message.content,
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        logger.info(f"✅ Sent message {message.id[:8]} to user {user_id}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to send message {message.id[:8]}: {e.stderr}")
        return False
    except subprocess.TimeoutExpired:
        logger.error(f"❌ Timeout sending message {message.id[:8]}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error sending message {message.id[:8]}: {e}")
        return False


def load_state() -> State:
    """Load monitor state from file."""
    if not STATE_FILE.exists():
        logger.info("No state file found - starting fresh")
        return State(
            watermark=0,
            retry_queue=[],
            dead_letter=[],
            last_health_check=datetime.now().isoformat()
        )

    try:
        with open(STATE_FILE, 'r') as f:
            data = json.load(f)
        state = State.from_dict(data)
        logger.info(f"Loaded state: watermark={state.watermark}, retry_queue={len(state.retry_queue)}")
        return state
    except Exception as e:
        logger.error(f"Failed to load state file: {e}")
        logger.warning("Starting with fresh state")
        return State(
            watermark=0,
            retry_queue=[],
            dead_letter=[],
            last_health_check=datetime.now().isoformat()
        )


def flush_state(state: State):
    """
    Flush state to disk immediately.

    CRITICAL: This must be called after EVERY watermark update.
    """
    try:
        STATE_FILE.parent.mkdir(exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(state.to_dict(), f, indent=2)
        logger.debug(f"Flushed state: watermark={state.watermark}")
    except Exception as e:
        logger.error(f"CRITICAL: Failed to flush state: {e}")
        raise  # Fail-loud: state flush failure is critical


def process_retry_queue(state: State, user_id: str, circuit_breaker: CircuitBreaker) -> None:
    """
    Process retry queue with exponential backoff.

    Args:
        state: Current monitor state
        user_id: Telegram user ID
        circuit_breaker: Circuit breaker for failure handling
    """
    if not state.retry_queue:
        return

    now = datetime.now()
    processed = 0

    # Process entries ready for retry
    for entry in state.retry_queue[:]:  # Copy to allow removal during iteration
        next_retry = datetime.fromisoformat(entry.next_retry)

        if next_retry <= now:
            # Check circuit breaker
            if not circuit_breaker.can_send():
                logger.warning("Circuit breaker open - skipping retry queue processing")
                break

            logger.info(f"Retrying message {entry.message.id[:8]} (attempt {entry.message.attempts + 1})")

            if send_telegram_message(entry.message, user_id):
                # Success: remove from retry queue, advance watermark
                state.retry_queue.remove(entry)
                state.watermark = max(state.watermark, entry.message.position)
                flush_state(state)
                circuit_breaker.record_success()
                processed += 1
                logger.info(f"✅ Retry successful - watermark advanced to {state.watermark}")
            else:
                # Failure: exponential backoff
                entry.message.attempts += 1
                circuit_breaker.record_failure()

                if entry.message.attempts >= MAX_RETRIES:
                    # Move to dead letter queue
                    logger.error(f"Message {entry.message.id[:8]} exceeded max retries - moving to dead letter")
                    state.dead_letter.append({
                        'message': entry.message.to_dict(),
                        'reason': 'Max retries exceeded',
                        'timestamp': now.isoformat()
                    })
                    state.retry_queue.remove(entry)
                else:
                    # Increase backoff
                    entry.backoff_seconds = min(entry.backoff_seconds * 2, MAX_BACKOFF_SECONDS)
                    entry.next_retry = (now + timedelta(seconds=entry.backoff_seconds)).isoformat()
                    logger.warning(f"Retry failed - next attempt in {entry.backoff_seconds}s")

                flush_state(state)

    if processed > 0:
        logger.info(f"Processed {processed} messages from retry queue")


def check_existing_process() -> bool:
    """
    Check if another V2 monitor is already running.

    Returns:
        True if another process is running, False otherwise
    """
    if not PID_FILE.exists():
        return False

    try:
        with open(PID_FILE, 'r') as f:
            old_pid = int(f.read().strip())

        # Check if process is still running
        try:
            os.kill(old_pid, 0)  # Signal 0 doesn't kill, just checks existence
            logger.warning(f"Another V2 monitor is already running (PID: {old_pid})")
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
        raise


def remove_pid_file():
    """Remove PID file on clean shutdown."""
    try:
        if PID_FILE.exists():
            PID_FILE.unlink()
            logger.info("Removed PID file")
    except Exception as e:
        logger.warning(f"Failed to remove PID file: {e}")


def load_user_config() -> Optional[str]:
    """Load Corey's Telegram user ID from config."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        user_id = config.get('corey_user_id')
        if not user_id:
            logger.error("corey_user_id not found in config")
            return None
        logger.info(f"Loaded user config: user_id={user_id}")
        return str(user_id)
    except FileNotFoundError:
        logger.error(f"Config file not found: {CONFIG_FILE}")
        return None
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return None


# =============================================================================
# Main Loop
# =============================================================================

def monitor_loop(interval: int, tmux_session: str):
    """
    Main monitoring loop.

    Args:
        interval: Polling interval in seconds
        tmux_session: Tmux session to monitor
    """
    # Check for existing process
    if check_existing_process():
        logger.error("Another V2 monitor is already running - exiting")
        sys.exit(1)

    # Create PID file
    create_pid_file()

    # Load user config
    user_id = load_user_config()
    if not user_id:
        logger.error("Failed to load user config - exiting")
        remove_pid_file()
        sys.exit(1)

    # Load state
    state = load_state()

    # Initialize circuit breaker
    circuit_breaker = CircuitBreaker(threshold=5)

    logger.info(f"🚀 Monitor V2 started: interval={interval}s, session={tmux_session}")
    logger.info(f"   Watermark: {state.watermark}")
    logger.info(f"   Retry queue: {len(state.retry_queue)} messages")
    logger.info(f"   Dead letter: {len(state.dead_letter)} messages")

    try:
        while True:
            # Process retry queue first
            process_retry_queue(state, user_id, circuit_breaker)

            # Get tmux buffer
            buffer = get_tmux_buffer(tmux_session)
            if buffer is None:
                logger.warning("Failed to get tmux buffer - skipping poll")
                time.sleep(interval)
                continue

            # Check for buffer shrink (scroll): Reset watermark if buffer smaller than watermark
            buffer_lines = len(buffer.split('\n'))
            if buffer_lines < state.watermark:
                logger.warning(f"Buffer shrunk ({buffer_lines} lines < watermark {state.watermark}) - resetting watermark to 0")
                state.watermark = 0
                flush_state(state)

            # Extract all messages
            all_messages = extract_summaries(buffer)

            if all_messages:
                logger.info(f"Found {len(all_messages)} total messages in buffer")

                # Filter to new messages only
                new_messages = filter_new_messages(all_messages, state.watermark)

                if new_messages:
                    logger.info(f"🆕 {len(new_messages)} new messages detected")

                    # Process new messages
                    for message in new_messages:
                        # Check circuit breaker
                        if not circuit_breaker.can_send():
                            logger.warning("Circuit breaker open - adding to retry queue")
                            retry_entry = RetryEntry(
                                message=message,
                                next_retry=(datetime.now() + timedelta(seconds=INITIAL_BACKOFF_SECONDS)).isoformat(),
                                backoff_seconds=INITIAL_BACKOFF_SECONDS
                            )
                            state.retry_queue.append(retry_entry)
                            flush_state(state)
                            continue

                        # Attempt to send
                        logger.info(f"Sending message {message.id[:8]} (position {message.position})")
                        if send_telegram_message(message, user_id):
                            # Success: advance watermark
                            state.watermark = max(state.watermark, message.position)
                            flush_state(state)
                            circuit_breaker.record_success()
                            logger.info(f"✅ Watermark advanced to {state.watermark}")
                        else:
                            # Failure: add to retry queue
                            circuit_breaker.record_failure()
                            message.attempts += 1
                            retry_entry = RetryEntry(
                                message=message,
                                next_retry=(datetime.now() + timedelta(seconds=INITIAL_BACKOFF_SECONDS)).isoformat(),
                                backoff_seconds=INITIAL_BACKOFF_SECONDS
                            )
                            state.retry_queue.append(retry_entry)
                            flush_state(state)
                            logger.warning(f"Send failed - added to retry queue")

            # Update health check timestamp
            state.last_health_check = datetime.now().isoformat()
            flush_state(state)

            # Sleep until next poll
            time.sleep(interval)

    except KeyboardInterrupt:
        logger.info("Received interrupt signal - shutting down")
    except Exception as e:
        logger.error(f"Unexpected error in monitor loop: {e}")
        raise
    finally:
        remove_pid_file()
        logger.info("Monitor V2 stopped")


# =============================================================================
# CLI Entry Point
# =============================================================================

def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Telegram Monitor V2 - Watermark-based message detection"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Polling interval in seconds (default: 30)"
    )
    parser.add_argument(
        "--tmux-session",
        type=str,
        default="0",
        help="Tmux session to monitor (default: 0)"
    )

    args = parser.parse_args()

    # Validate interval
    if args.interval < 10:
        logger.warning(f"Interval {args.interval}s is too low - setting to 10s minimum")
        args.interval = 10

    # Start monitor
    monitor_loop(args.interval, args.tmux_session)


if __name__ == "__main__":
    main()
