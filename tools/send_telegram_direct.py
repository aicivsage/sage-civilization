#!/usr/bin/env python3
# =============================================================================
# PRODUCTION STATUS: LOCKED ✅
# Last verified working: 2025-10-19
# Status: STABLE - Primary's canonical message sender with Markdown support
# DO NOT MODIFY without explicit approval and testing
# =============================================================================
"""
Send message directly to Telegram via Bot API.

Usage:
    python3 tools/send_telegram_direct.py <user_id> <message>
    python3 tools/send_telegram_direct.py 437939400 "Hello from Primary AI!"

Environment:
    Reads bot token from config/telegram_config.json

This script is invoked by telegram-sender agent to send messages to Corey.
"""
import sys
import json
import logging
import requests
from pathlib import Path

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "telegram_config.json"


def load_config():
    """Load telegram configuration."""
    if not CONFIG_FILE.exists():
        print(f"ERROR: Config file not found: {CONFIG_FILE}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to load config: {e}", file=sys.stderr)
        sys.exit(1)


def send_telegram_message(bot_token: str, user_id: int, message: str) -> bool:
    """
    Send message via Telegram Bot API.

    Args:
        bot_token: Telegram bot token
        user_id: Telegram user ID (chat_id)
        message: Message text to send

    Returns:
        True if sent successfully, False otherwise
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    # Telegram message length limit
    MAX_LENGTH = 4096

    # Split message if too long
    if len(message) > MAX_LENGTH:
        chunks = []
        current_chunk = ""

        for line in message.split('\n'):
            if len(current_chunk) + len(line) + 1 > MAX_LENGTH - 100:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = line
            else:
                if current_chunk:
                    current_chunk += '\n' + line
                else:
                    current_chunk = line

        if current_chunk:
            chunks.append(current_chunk)

        # Send all chunks
        for i, chunk in enumerate(chunks):
            if i > 0:
                chunk = f"(continued {i+1}/{len(chunks)})\n\n{chunk}"

            payload = {
                "chat_id": user_id,
                "text": chunk,
                "parse_mode": "Markdown"
            }

            try:
                response = requests.post(url, json=payload, timeout=10)
                response.raise_for_status()
            except requests.HTTPError as e:
                if e.response.status_code == 400:
                    # Markdown parse error - fall back to plain text for this chunk
                    logger.info(f"Markdown parse failed for chunk {i+1}, retrying as plain text")
                    payload = {"chat_id": user_id, "text": chunk}
                    try:
                        response = requests.post(url, json=payload, timeout=10)
                        response.raise_for_status()
                    except Exception as fallback_error:
                        print(f"ERROR: Failed to send chunk {i+1} (plain text fallback): {fallback_error}", file=sys.stderr)
                        return False
                else:
                    print(f"ERROR: Failed to send chunk {i+1} (HTTP {e.response.status_code}): {e}", file=sys.stderr)
                    return False
            except Exception as e:
                print(f"ERROR: Failed to send chunk {i+1}: {e}", file=sys.stderr)
                return False

        return True

    else:
        # Send single message - try Markdown first, fall back to plain text
        payload = {
            "chat_id": user_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.HTTPError as e:
            if e.response.status_code == 400:
                # Markdown parse error - fall back to plain text
                logger.info("Markdown parse failed (400 error), retrying as plain text")
                payload = {"chat_id": user_id, "text": message}
                try:
                    response = requests.post(url, json=payload, timeout=10)
                    response.raise_for_status()
                    print(f"✓ Message sent to user {user_id} (plain text fallback)")
                    return True
                except Exception as fallback_error:
                    print(f"ERROR: Failed to send plain text fallback: {fallback_error}", file=sys.stderr)
                    return False
            else:
                print(f"ERROR: Failed to send message (HTTP {e.response.status_code}): {e}", file=sys.stderr)
                return False
        except Exception as e:
            print(f"ERROR: Failed to send message: {e}", file=sys.stderr)
            return False


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python3 send_telegram_direct.py <user_id> <message>", file=sys.stderr)
        print("Example: python3 send_telegram_direct.py 437939400 'Hello!'", file=sys.stderr)
        sys.exit(1)

    user_id = sys.argv[1]
    message = sys.argv[2]

    # Validate user_id is numeric
    try:
        user_id = int(user_id)
    except ValueError:
        print(f"ERROR: user_id must be numeric, got: {user_id}", file=sys.stderr)
        sys.exit(1)

    # Load config
    config = load_config()
    bot_token = config.get("bot_token")

    if not bot_token:
        print("ERROR: bot_token not found in config", file=sys.stderr)
        sys.exit(1)

    # Send message
    success = send_telegram_message(bot_token, user_id, message)

    if success:
        print(f"✓ Message sent to user {user_id}")
        sys.exit(0)
    else:
        print(f"✗ Failed to send message to user {user_id}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
