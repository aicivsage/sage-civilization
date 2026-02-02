#!/usr/bin/env python3
"""
Telegram Bridge for Sage Civilization - V2 with JSONL Injection
CRITICAL FIX: Bypasses stdin blocking by writing directly to Claude conversation file

🚨🚨🚨 PRODUCTION FILE V2 - CRITICAL FIX DEPLOYMENT 🚨🚨🚨

Date: 2025-12-29
Fix: Input-waiting states block tmux send-keys injection
Solution: Write directly to JSONL conversation file (bypasses stdin)

Architecture:
- Receives messages from Telegram
- Injects them into Claude conversation via JSONL file append
- NO tmux dependency for message injection
- Works even when Claude waiting for input (stdin blocked)

For full technical details, see:
memories/agents/tg-archi/CRITICAL-telegram-bridge-failure-20251229.md

Registry: memories/agents/tg-archi/telegram_script_registry.json
"""

import asyncio
import json
import logging
import os
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
PROJECT_ROOT = Path("/mnt/c/sage/sage-civilization")
SESSION_DIR = PROJECT_ROOT / ".tg_sessions"
PID_FILE = SESSION_DIR / "telegram_bridge.pid"
CONFIG_FILE = PROJECT_ROOT / "config" / "telegram_config.json"
DEFAULT_CONFIG = {
    "tmux_session": "sage-main",
    "tmux_pane": "sage-main:0.0",
    "working_directory": str(PROJECT_ROOT),
    "response_timeout": 10,
    "max_response_length": 4000,
    "injection_method": "jsonl",  # NEW: "jsonl" or "tmux"
    "claude_code_projects_dir": str(Path.home() / ".claude/projects"),
    "project_name": "-mnt-c-sage-sage-civilization"
}

# Ensure session directory exists
SESSION_DIR.mkdir(exist_ok=True)


class TelegramBridge:
    """Telegram bridge to Primary AI via JSONL file injection."""

    def __init__(self, config: Dict):
        """Initialize bridge with configuration."""
        self.config = config
        self.authorized_users = config.get("authorized_users", {})
        self.tmux_pane = config.get("tmux_pane", DEFAULT_CONFIG["tmux_pane"])
        self.response_timeout = config.get("response_timeout", DEFAULT_CONFIG["response_timeout"])
        self.max_response_length = config.get("max_response_length", DEFAULT_CONFIG["max_response_length"])
        self.injection_method = config.get("injection_method", DEFAULT_CONFIG["injection_method"])
        self.claude_projects_dir = Path(config.get("claude_code_projects_dir", DEFAULT_CONFIG["claude_code_projects_dir"]))
        self.project_name = config.get("project_name", DEFAULT_CONFIG["project_name"])

        logger.info(f"Bridge initialized with injection method: {self.injection_method}")

        # Verify tmux session exists (still needed for fallback)
        if not self._check_tmux_session():
            logger.warning(f"tmux session {self.tmux_pane} may not exist - fallback will fail")

    def _check_tmux_session(self) -> bool:
        """Check if tmux session exists."""
        try:
            result = subprocess.run(
                ["tmux", "has-session", "-t", self.tmux_pane.split(':')[0]],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"tmux session check failed: {e}")
            return False

    def is_authorized(self, user_id: int) -> bool:
        """Check if user is authorized."""
        return str(user_id) in self.authorized_users

    def get_user_info(self, user_id: int) -> Optional[Dict]:
        """Get user information."""
        return self.authorized_users.get(str(user_id))

    def find_current_session_file(self) -> Optional[Path]:
        """
        Find the most recently modified JSONL file for this project.
        Adapted from telegram_jsonl_monitor.py with growth validation.
        """
        try:
            project_dir = self.claude_projects_dir / self.project_name

            if not project_dir.exists():
                logger.error(f"Project directory not found: {project_dir}")
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

            # Wait 2 seconds (shorter than monitor's 3s for faster response)
            time.sleep(2)

            # Record sizes after
            sizes_after = {f: f.stat().st_size for f in candidates}

            # Calculate growth
            growth = {f: sizes_after[f] - sizes_before[f] for f in candidates}

            # Find file that grew the most
            active_file = max(growth, key=growth.get)

            logger.info(f"Active session: {active_file.name} (grew {growth[active_file]:,} bytes)")
            return active_file

        except Exception as e:
            logger.error(f"Error finding session file: {e}")
            return None

    def inject_to_jsonl(self, message: str, username: str = "user") -> bool:
        """
        Inject message to Claude conversation via JSONL file.

        This bypasses stdin completely, allowing messages to be processed
        even when Claude CLI is waiting for input (blocking read).

        Args:
            message: User message to inject
            username: Telegram username for context

        Returns:
            True if injection succeeded, False otherwise
        """
        try:
            # Find current session file
            session_file = self.find_current_session_file()
            if not session_file:
                logger.error("Could not find current Claude session file")
                return False

            # Format message with Telegram indicator
            formatted = f"[TELEGRAM from @{username}] {message}"

            logger.info(f"Injecting to JSONL: {formatted[:100]}...")
            logger.info(f"Target file: {session_file.name}")

            # Create JSONL entry matching Claude CLI format
            entry = {
                "type": "message",
                "message": {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": formatted
                        }
                    ]
                },
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }

            # Append to JSONL file
            with open(session_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + '\n')
                f.flush()  # Ensure written immediately

            logger.info("JSONL injection successful")
            return True

        except Exception as e:
            logger.error(f"JSONL injection failed: {e}")
            return False

    def inject_to_tmux(self, message: str, username: str = "user") -> bool:
        """
        FALLBACK: Inject message to Primary AI tmux session.

        This is the old method (V1). Works when Claude NOT waiting for input,
        but fails when stdin is blocked.

        Args:
            message: User message to inject
            username: Telegram username for context

        Returns:
            True if injection succeeded, False otherwise
        """
        try:
            # Format message with Telegram indicator
            formatted = f"[TELEGRAM from @{username}] {message}"

            logger.info(f"Injecting to tmux (FALLBACK): {formatted[:100]}...")

            # Send to tmux using literal mode (-l) for special characters
            subprocess.run(
                ["tmux", "send-keys", "-t", self.tmux_pane, "-l", formatted],
                check=True,
                timeout=5
            )

            # Press Enter to submit
            subprocess.run(
                ["tmux", "send-keys", "-t", self.tmux_pane, "Enter"],
                check=True,
                timeout=5
            )

            logger.info("tmux injection successful")
            return True

        except subprocess.TimeoutExpired:
            logger.error("tmux injection timed out")
            return False
        except subprocess.CalledProcessError as e:
            logger.error(f"tmux injection failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during tmux injection: {e}")
            return False

    def inject_message(self, message: str, username: str = "user") -> bool:
        """
        Main injection method - routes to JSONL or tmux based on config.

        Args:
            message: User message to inject
            username: Telegram username for context

        Returns:
            True if injection succeeded, False otherwise
        """
        if self.injection_method == "jsonl":
            success = self.inject_to_jsonl(message, username)
            if not success:
                logger.warning("JSONL injection failed, attempting tmux fallback...")
                success = self.inject_to_tmux(message, username)
            return success
        else:
            # tmux mode (backward compatibility)
            return self.inject_to_tmux(message, username)

    def save_session(self, user_id: int, message_count: int):
        """Save minimal session data."""
        session_file = SESSION_DIR / f"{user_id}.json"

        data = {
            "user_id": user_id,
            "message_count": message_count,
            "last_active": datetime.utcnow().isoformat() + "Z"
        }

        try:
            with open(session_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save session: {e}")

    def load_session(self, user_id: int) -> Dict:
        """Load session data."""
        session_file = SESSION_DIR / f"{user_id}.json"

        if not session_file.exists():
            return {"user_id": user_id, "message_count": 0}

        try:
            with open(session_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load session: {e}")
            return {"user_id": user_id, "message_count": 0}


# Global bridge instance
bridge: Optional[TelegramBridge] = None


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user
    user_id = user.id

    if not bridge.is_authorized(user_id):
        await update.message.reply_text(
            "Unauthorized. This bot is for Sage civilization members only."
        )
        return

    user_info = bridge.get_user_info(user_id)
    welcome_msg = f"""
Welcome to Sage Telegram Bridge V2!

You are authorized as: {user_info.get('name', 'User')}
Role: {user_info.get('role', 'member')}

This bridge connects you directly to Primary AI via JSONL injection.

NEW in V2: Messages work even when Claude is waiting for input!

Commands:
/start - Show this welcome message
/help - Show available commands
/ping - Health check (immediate response)

To interact with Primary AI:
Simply send a message and I'll inject it into the conversation.

Note: JSONL injection bypasses stdin blocking (critical fix).
"""

    await update.message.reply_text(welcome_msg)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    user_id = update.effective_user.id

    if not bridge.is_authorized(user_id):
        await update.message.reply_text("Unauthorized.")
        return

    help_msg = """
Sage Telegram Bridge V2 - Commands:

/start - Welcome message and setup info
/help - This help message
/ping - Health check (immediate pong response)

Messaging:
- Send any message to communicate with Primary AI
- Messages are injected into Claude conversation via JSONL
- Works even when Claude waiting for input (stdin blocked)
- No response capture (use JSONL monitor for outbound)

Technical V2 Features:
- Injection method: {method}
- JSONL file detection: Automatic (growth validation)
- Session rotation: Supported
- Fallback: tmux injection if JSONL fails

Session Info:
- Your messages are logged to .tg_sessions/
- Session persists across bot restarts
""".format(method=bridge.injection_method)

    await update.message.reply_text(help_msg)


async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ping command - immediate health check."""
    user_id = update.effective_user.id

    if not bridge.is_authorized(user_id):
        await update.message.reply_text("Unauthorized.")
        return

    # Check tmux session status
    tmux_ok = bridge._check_tmux_session()

    # Check JSONL session file
    session_file = bridge.find_current_session_file()
    jsonl_ok = session_file is not None

    status_msg = f"""
Pong!

Bridge Status: Online
Injection Method: {bridge.injection_method}
tmux Session: {'Connected' if tmux_ok else 'WARNING: Not found'}
JSONL Session: {'Found ({})'.format(session_file.name if session_file else 'N/A') if jsonl_ok else 'WARNING: Not found'}

Your user ID: {user_id}
Session messages: {bridge.load_session(user_id).get('message_count', 0)}

V2 Features: ✅ JSONL injection (bypasses stdin blocking)
"""

    await update.message.reply_text(status_msg)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle regular messages - inject to Claude via JSONL.

    This is the core V2 functionality.
    """
    user = update.effective_user
    user_id = user.id

    # Authorization check
    if not bridge.is_authorized(user_id):
        await update.message.reply_text(
            "Unauthorized. Contact administrator for access."
        )
        return

    message_text = update.message.text
    username = user.username or user.first_name or "user"

    logger.info(f"Message from @{username} (ID: {user_id}): {message_text[:50]}...")

    # Inject message (JSONL or tmux based on config)
    injection_success = bridge.inject_message(message_text, username)

    if not injection_success:
        logger.error(f"Failed to inject message from user {user_id}")
        # Don't send error response - just log it
        # (User will see no response from Primary, not from bridge)
        return

    # Update session
    session = bridge.load_session(user_id)
    session["message_count"] = session.get("message_count", 0) + 1
    bridge.save_session(user_id, session["message_count"])

    logger.info(f"Injection complete for user {user_id} (method: {bridge.injection_method})")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")

    if update and update.effective_message:
        await update.effective_message.reply_text(
            f"An error occurred: {str(context.error)}"
        )


def load_config() -> Dict:
    """
    Load configuration from file or environment.

    Priority:
    1. config/telegram_config.json
    2. Environment variables
    3. Defaults
    """
    config = DEFAULT_CONFIG.copy()

    # Try loading from file
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                file_config = json.load(f)
                config.update(file_config)
                logger.info(f"Loaded config from {CONFIG_FILE}")
        except Exception as e:
            logger.error(f"Failed to load config file: {e}")
    else:
        logger.warning(f"Config file not found: {CONFIG_FILE}")

    # Check for bot token
    bot_token = config.get("bot_token") or os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise ValueError(
            "No bot token found. Set TELEGRAM_BOT_TOKEN env var or add to config file."
        )

    config["bot_token"] = bot_token

    # Check for authorized users
    if not config.get("authorized_users"):
        raise ValueError(
            "No authorized users configured. Add to config/telegram_config.json"
        )

    return config


def check_pid_file() -> bool:
    """
    Check if another bridge instance is running via PID file.

    Returns:
        True if another instance is running (should not start)
        False if safe to start
    """
    if not PID_FILE.exists():
        return False  # No PID file, safe to start

    try:
        with open(PID_FILE, 'r') as f:
            old_pid = int(f.read().strip())

        # Check if process is still running
        try:
            os.kill(old_pid, 0)  # Signal 0 checks existence without killing
            logger.error(f"Another bridge instance is already running (PID: {old_pid})")
            logger.error(f"PID file: {PID_FILE}")
            logger.error(f"Refusing to start duplicate instance")
            return True  # Process is running, fail-fast
        except OSError:
            # Process doesn't exist, stale PID file
            logger.warning(f"Found stale PID file (PID {old_pid} not running)")
            PID_FILE.unlink()
            logger.info(f"Removed stale PID file")
            return False  # Safe to start
    except Exception as e:
        logger.error(f"Error checking PID file: {e}")
        return False  # On error, allow start (fail-open for recovery)


def create_pid_file():
    """Create PID file with current process ID."""
    try:
        PID_FILE.parent.mkdir(exist_ok=True)
        with open(PID_FILE, 'w') as f:
            f.write(str(os.getpid()))
        logger.info(f"Created PID file: {PID_FILE} (PID: {os.getpid()})")
    except Exception as e:
        logger.error(f"Failed to create PID file: {e}")
        raise  # Fail-loud: PID file creation is critical


def remove_pid_file():
    """Remove PID file on shutdown."""
    try:
        if PID_FILE.exists():
            PID_FILE.unlink()
            logger.info("Removed PID file")
    except Exception as e:
        logger.warning(f"Failed to remove PID file: {e}")


def main():
    """Main entry point."""
    global bridge

    # Set process name to distinguish from other bridges
    try:
        import setproctitle
        setproctitle.setproctitle("sage_telegram_bridge_v2")
    except ImportError:
        pass  # setproctitle not available, skip naming

    # CHECK PID FILE FIRST (CRITICAL - prevents 409 conflicts)
    if check_pid_file():
        logger.error("Exiting due to duplicate instance detection")
        return 1

    logger.info("Starting Sage Telegram Bridge V2 (JSONL Injection)")

    # Load configuration
    try:
        config = load_config()
        logger.info("Configuration loaded successfully")
        logger.info(f"Injection method: {config.get('injection_method', 'jsonl')}")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        logger.error("See memories/agents/tg-archi/PRIMARY_TELEGRAM_PROTOCOL.md for setup")
        return 1

    # Initialize bridge
    bridge = TelegramBridge(config)
    logger.info(f"Bridge initialized (method: {bridge.injection_method})")

    # CREATE PID FILE (CRITICAL - marks this instance as running)
    create_pid_file()

    # Create application
    application = Application.builder().token(config["bot_token"]).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    # Start bot
    logger.info("Starting bot polling...")
    logger.info(f"Authorized users: {list(bridge.authorized_users.keys())}")

    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        return 1
    finally:
        # CLEANUP PID FILE (CRITICAL - allows restart)
        remove_pid_file()

    return 0


if __name__ == "__main__":
    exit(main())
