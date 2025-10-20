#!/usr/bin/env python3
"""
Telegram Bridge for A-C-Gee Civilization
Phase 1 MVP: Simple round-trip message relay via tmux injection

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
- Receives messages from Telegram
- Injects them into Primary AI tmux session via ACG_telegram_bridge process
- Config: config/telegram_config.json (tmux_session, tmux_pane must match current session)

For full architecture details, see:
/home/corey/projects/AI-CIV/grow_gemini_deepresearch/.claude/from-corey/tg-integration-and-possible-lesson/

Registry: memories/agents/tg-archi/telegram_script_registry.json
"""

import asyncio
import json
import logging
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict

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
PROJECT_ROOT = Path("/home/corey/projects/AI-CIV/grow_gemini_deepresearch")
SESSION_DIR = PROJECT_ROOT / ".tg_sessions"
CONFIG_FILE = PROJECT_ROOT / "config" / "telegram_config.json"
DEFAULT_CONFIG = {
    "tmux_session": "acgee-main",
    "tmux_pane": "acgee-main:0.0",
    "working_directory": str(PROJECT_ROOT),
    "response_timeout": 10,
    "max_response_length": 4000  # Leave room for formatting
}

# Ensure session directory exists
SESSION_DIR.mkdir(exist_ok=True)


class TelegramBridge:
    """Telegram bridge to Primary AI via tmux injection."""

    def __init__(self, config: Dict):
        """Initialize bridge with configuration."""
        self.config = config
        self.authorized_users = config.get("authorized_users", {})
        self.tmux_pane = config.get("tmux_pane", DEFAULT_CONFIG["tmux_pane"])
        self.response_timeout = config.get("response_timeout", DEFAULT_CONFIG["response_timeout"])
        self.max_response_length = config.get("max_response_length", DEFAULT_CONFIG["max_response_length"])

        # Verify tmux session exists
        if not self._check_tmux_session():
            logger.warning(f"tmux session {self.tmux_pane} may not exist - messages will fail")

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

    def inject_to_tmux(self, message: str, username: str = "user") -> bool:
        """
        Inject message to Primary AI tmux session.

        Args:
            message: User message to inject
            username: Telegram username for context

        Returns:
            True if injection succeeded, False otherwise
        """
        try:
            # Format message with Telegram indicator
            formatted = f"[TELEGRAM from @{username}] {message}"

            logger.info(f"Injecting to tmux: {formatted[:100]}...")

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

    def capture_tmux_response(self, wait_seconds: Optional[int] = None) -> str:
        """
        Capture response from tmux session.

        Args:
            wait_seconds: How long to wait before capturing (uses config default if None)

        Returns:
            Captured response text
        """
        wait = wait_seconds if wait_seconds is not None else self.response_timeout

        try:
            # Wait for Primary AI to generate response
            logger.info(f"Waiting {wait}s for response...")
            time.sleep(wait)

            # Capture last 100 lines from tmux pane
            result = subprocess.run(
                ["tmux", "capture-pane", "-t", self.tmux_pane, "-p", "-S", "-100"],
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )

            # Parse response - extract everything after our prompt
            lines = result.stdout.split('\n')
            response_lines = []
            found_prompt = False

            for line in lines:
                # Look for our injected message marker
                if "[TELEGRAM from @" in line:
                    found_prompt = True
                    continue

                # Collect lines after our prompt
                if found_prompt and line.strip():
                    response_lines.append(line)

            # Join and clean response
            response = '\n'.join(response_lines).strip()

            if not response:
                logger.warning("No response captured from tmux")
                return "No response captured. Primary AI may be processing or tmux session may be inactive."

            # Truncate if too long for Telegram
            if len(response) > self.max_response_length:
                response = response[:self.max_response_length] + "\n\n...(truncated)"

            logger.info(f"Captured response ({len(response)} chars)")
            return response

        except subprocess.TimeoutExpired:
            logger.error("tmux capture timed out")
            return "Error: Response capture timed out"
        except subprocess.CalledProcessError as e:
            logger.error(f"tmux capture failed: {e}")
            return f"Error: Could not capture response from tmux ({e})"
        except Exception as e:
            logger.error(f"Unexpected error during capture: {e}")
            return f"Error: {str(e)}"

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
            "Unauthorized. This bot is for A-C-Gee civilization members only."
        )
        return

    user_info = bridge.get_user_info(user_id)
    welcome_msg = f"""
Welcome to A-C-Gee Telegram Bridge!

You are authorized as: {user_info.get('name', 'User')}
Role: {user_info.get('role', 'member')}

This bridge connects you directly to the Primary AI via tmux injection.

Commands:
/start - Show this welcome message
/help - Show available commands
/ping - Health check (immediate response)

To interact with Primary AI:
Simply send a message and I'll inject it into the tmux session and capture the response.

Note: Responses may take {bridge.response_timeout}s to capture.
"""

    await update.message.reply_text(welcome_msg)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    user_id = update.effective_user.id

    if not bridge.is_authorized(user_id):
        await update.message.reply_text("Unauthorized.")
        return

    help_msg = """
A-C-Gee Telegram Bridge - Commands:

/start - Welcome message and setup info
/help - This help message
/ping - Health check (immediate pong response)

Messaging:
- Send any message to communicate with Primary AI
- Messages are injected into tmux session: {tmux_pane}
- Responses captured after {timeout}s delay
- Maximum response length: {max_len} characters

Session Info:
- Your messages are logged to .tg_sessions/
- Session persists across bot restarts

Technical:
- Architecture: tmux injection + capture-pane
- No direct API calls to Anthropic
- File-based session storage
""".format(
        tmux_pane=bridge.tmux_pane,
        timeout=bridge.response_timeout,
        max_len=bridge.max_response_length
    )

    await update.message.reply_text(help_msg)


async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ping command - immediate health check."""
    user_id = update.effective_user.id

    if not bridge.is_authorized(user_id):
        await update.message.reply_text("Unauthorized.")
        return

    # Check tmux session status
    tmux_ok = bridge._check_tmux_session()

    status_msg = f"""
Pong!

Bridge Status: Online
tmux Session: {'Connected' if tmux_ok else 'WARNING: Not found'}
Session: {bridge.tmux_pane}
Response Timeout: {bridge.response_timeout}s

Your user ID: {user_id}
Session messages: {bridge.load_session(user_id).get('message_count', 0)}
"""

    await update.message.reply_text(status_msg)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle regular messages - inject to tmux and capture response.

    This is the core MVP functionality.
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

    # Inject message to tmux (silently - no response)
    injection_success = bridge.inject_to_tmux(message_text, username)

    if not injection_success:
        logger.error(f"Failed to inject message from user {user_id}")
        # Don't send error response - just log it
        return

    # Update session
    session = bridge.load_session(user_id)
    session["message_count"] = session.get("message_count", 0) + 1
    bridge.save_session(user_id, session["message_count"])

    logger.info(f"Round-trip complete for user {user_id}")


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


def main():
    """Main entry point."""
    global bridge

    # Set process name to distinguish from Weaver's processes
    try:
        import setproctitle
        setproctitle.setproctitle("ACG_telegram_bridge")
    except ImportError:
        pass  # setproctitle not available, skip naming

    logger.info("Starting A-C-Gee Telegram Bridge (Phase 1 MVP)")

    # Load configuration
    try:
        config = load_config()
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        logger.error("See docs/TELEGRAM_SETUP.md for setup instructions")
        return 1

    # Initialize bridge
    bridge = TelegramBridge(config)
    logger.info(f"Bridge initialized for tmux session: {bridge.tmux_pane}")

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

    return 0


if __name__ == "__main__":
    exit(main())
