#!/usr/bin/env python3
"""
Send voice message to Telegram via Bot API using text-to-speech.

Usage:
    python3 tools/send_telegram_voice.py <user_id> <text>
    python3 tools/send_telegram_voice.py 7585924762 "Hello Greg!"

Environment:
    Reads bot token from config/telegram_config.json

This script enables voice replies to Greg's voice messages.
"""

import json
import sys
import os
import requests
from pathlib import Path
from gtts import gTTS
import tempfile

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


def send_telegram_voice(bot_token: str, user_id: int, text: str) -> bool:
    """
    Generate voice from text and send via Telegram Bot API.

    Args:
        bot_token: Telegram bot token
        user_id: Telegram user ID (chat_id)
        text: Text to convert to speech

    Returns:
        True if sent successfully, False otherwise
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendVoice"

    # Generate speech
    try:
        # Create temporary file for audio
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
            temp_path = temp_audio.name

        # Generate speech using gTTS
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(temp_path)

        # Send voice message
        with open(temp_path, 'rb') as audio_file:
            files = {
                'voice': ('voice.mp3', audio_file, 'audio/mpeg')
            }

            data = {
                'chat_id': user_id,
            }

            response = requests.post(url, data=data, files=files, timeout=30)
            response.raise_for_status()

            result = response.json()

            # Clean up temp file
            os.unlink(temp_path)

            if result.get('ok'):
                return True
            else:
                print(f"ERROR: Telegram API error: {result.get('description')}", file=sys.stderr)
                return False

    except Exception as e:
        print(f"ERROR: Failed to send voice: {e}", file=sys.stderr)
        # Clean up temp file on error
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.unlink(temp_path)
        return False


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python3 send_telegram_voice.py <user_id> <text>", file=sys.stderr)
        print("Example: python3 send_telegram_voice.py 7585924762 'Hello Greg!'", file=sys.stderr)
        sys.exit(1)

    user_id = int(sys.argv[1])
    text = " ".join(sys.argv[2:])

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

    # Send voice
    print(f"Generating voice message: {text[:50]}...", file=sys.stderr)
    print(f"To user: {user_id}", file=sys.stderr)

    success = send_telegram_voice(bot_token, user_id, text)

    if success:
        print(f"✓ Voice message sent successfully to user {user_id}")
        sys.exit(0)
    else:
        print(f"✗ Failed to send voice message to user {user_id}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
