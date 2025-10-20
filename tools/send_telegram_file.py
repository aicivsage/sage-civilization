#!/usr/bin/env python3
"""
Send file attachment to Telegram via Bot API.

Usage:
    python3 tools/send_telegram_file.py <file_path> [caption] [user_id]
    python3 tools/send_telegram_file.py handoff.md "Session handoff document" 437939400

Environment:
    Reads bot token from config/telegram_config.json

This script enables tg-archi agent to send files to Corey via Telegram.
"""

import json
import sys
import os
import requests
from pathlib import Path

# Constants
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "telegram_config.json"
DEFAULT_USER_ID = 437939400  # Corey


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


def send_telegram_file(bot_token: str, user_id: int, file_path: str, caption: str = None) -> bool:
    """
    Send file via Telegram Bot API.

    Args:
        bot_token: Telegram bot token
        user_id: Telegram user ID (chat_id)
        file_path: Path to file to send
        caption: Optional caption for the file (max 1024 chars)

    Returns:
        True if sent successfully, False otherwise
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

    # Validate file exists
    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        return False

    # Check file size (50 MB limit for bot uploads)
    file_size = file_path_obj.stat().st_size
    max_size = 50 * 1024 * 1024  # 50 MB in bytes
    if file_size > max_size:
        print(f"ERROR: File too large ({file_size / 1024 / 1024:.2f} MB). Max: 50 MB", file=sys.stderr)
        return False

    # Prepare multipart/form-data
    try:
        with open(file_path, 'rb') as f:
            files = {
                'document': (file_path_obj.name, f, 'application/octet-stream')
            }

            data = {
                'chat_id': user_id,
            }

            # Add caption if provided (truncate to 1024 chars)
            if caption:
                if len(caption) > 1024:
                    caption = caption[:1020] + "..."
                data['caption'] = caption
                data['parse_mode'] = 'Markdown'

            # Send file
            response = requests.post(url, data=data, files=files, timeout=30)
            response.raise_for_status()

            result = response.json()
            if result.get('ok'):
                return True
            else:
                print(f"ERROR: Telegram API error: {result.get('description')}", file=sys.stderr)
                return False

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Network error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"ERROR: Failed to send file: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 send_telegram_file.py <file_path> [caption] [user_id]", file=sys.stderr)
        print("Example: python3 send_telegram_file.py handoff.md 'Session handoff' 437939400", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]
    caption = sys.argv[2] if len(sys.argv) > 2 else None
    user_id = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_USER_ID

    # Load config
    config = load_config()
    bot_token = config.get("bot_token")

    if not bot_token:
        print("ERROR: bot_token not found in config", file=sys.stderr)
        sys.exit(1)

    # Verify user is authorized
    authorized_users = config.get("authorized_users", {})
    if str(user_id) not in authorized_users:
        print(f"WARNING: user_id {user_id} not in authorized_users list", file=sys.stderr)
        print("Proceeding anyway...", file=sys.stderr)

    # Send file
    print(f"Sending file: {file_path}", file=sys.stderr)
    if caption:
        print(f"Caption: {caption}", file=sys.stderr)
    print(f"To user: {user_id}", file=sys.stderr)

    success = send_telegram_file(bot_token, user_id, file_path, caption)

    if success:
        print(f"✓ File sent successfully to user {user_id}")
        sys.exit(0)
    else:
        print(f"✗ Failed to send file to user {user_id}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
