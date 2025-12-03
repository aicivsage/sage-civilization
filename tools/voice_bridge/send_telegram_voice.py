#!/usr/bin/env python3
"""
Send voice message to Telegram using TTS (gTTS)

Usage:
    python3 tools/send_telegram_voice.py <user_id> "<message>"

Example:
    python3 tools/send_telegram_voice.py 1227950729 "Hello Greg, this is Sage speaking!"

This script:
1. Converts text to speech using gTTS
2. Converts MP3 to OGG Opus format (required by Telegram)
3. Sends as voice message to Telegram
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import requests
from gtts import gTTS

# Constants
PROJECT_ROOT = Path(__file__).parent.parent.parent  # tools/voice_bridge/ -> tools/ -> project root
CONFIG_FILE = PROJECT_ROOT / "config" / "telegram_config.json"
FFMPEG_PATH = PROJECT_ROOT / "tools" / "bin" / "ffmpeg-7.0.2-amd64-static" / "ffmpeg"
VOICE_TEMP_DIR = PROJECT_ROOT / ".tg_voice_temp"

# Ensure temp dir exists
VOICE_TEMP_DIR.mkdir(exist_ok=True)


def load_config():
    """Load Telegram config."""
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


def text_to_speech(text: str, output_mp3: Path) -> bool:
    """Convert text to MP3 using gTTS."""
    try:
        # Truncate very long messages
        if len(text) > 2000:
            text = text[:2000] + "... Message truncated."

        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(str(output_mp3))
        return True
    except Exception as e:
        print(f"TTS error: {e}", file=sys.stderr)
        return False


def convert_mp3_to_ogg(mp3_path: Path, ogg_path: Path) -> bool:
    """Convert MP3 to OGG Opus format for Telegram."""
    try:
        result = subprocess.run([
            str(FFMPEG_PATH),
            '-i', str(mp3_path),
            '-acodec', 'libopus',
            '-b:a', '32k',
            str(ogg_path),
            '-y'  # Overwrite
        ], capture_output=True, text=True, timeout=30)

        return result.returncode == 0
    except Exception as e:
        print(f"Conversion error: {e}", file=sys.stderr)
        return False


def send_voice_message(bot_token: str, chat_id: str, ogg_path: Path) -> bool:
    """Send OGG file as voice message to Telegram."""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendVoice"

        with open(ogg_path, 'rb') as voice_file:
            response = requests.post(
                url,
                data={'chat_id': chat_id},
                files={'voice': ('voice.ogg', voice_file, 'audio/ogg')}
            )

        if response.status_code == 200:
            return True
        else:
            print(f"Telegram error: {response.text}", file=sys.stderr)
            return False

    except Exception as e:
        print(f"Send error: {e}", file=sys.stderr)
        return False


def send_voice(user_id: str, message: str) -> bool:
    """Main function to convert text to voice and send to Telegram."""
    config = load_config()
    bot_token = config.get('bot_token')

    if not bot_token:
        print("No bot token in config", file=sys.stderr)
        return False

    # Generate temp file paths
    import uuid
    temp_id = str(uuid.uuid4())[:8]
    mp3_path = VOICE_TEMP_DIR / f"voice_out_{temp_id}.mp3"
    ogg_path = VOICE_TEMP_DIR / f"voice_out_{temp_id}.ogg"

    try:
        # Step 1: Text to Speech
        print(f"Generating speech for: {message[:50]}...", file=sys.stderr)
        if not text_to_speech(message, mp3_path):
            return False

        # Step 2: Convert to OGG
        print("Converting to OGG...", file=sys.stderr)
        if not convert_mp3_to_ogg(mp3_path, ogg_path):
            return False

        # Step 3: Send to Telegram
        print("Sending voice message...", file=sys.stderr)
        if not send_voice_message(bot_token, user_id, ogg_path):
            return False

        print(f"Voice message sent to user {user_id}", file=sys.stderr)
        return True

    finally:
        # Cleanup temp files
        for path in [mp3_path, ogg_path]:
            if path.exists():
                try:
                    path.unlink()
                except:
                    pass


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 send_telegram_voice.py <user_id> <message>")
        print("Example: python3 send_telegram_voice.py 1227950729 \"Hello from Sage!\"")
        sys.exit(1)

    user_id = sys.argv[1]
    message = sys.argv[2]

    # Verify ffmpeg exists
    if not FFMPEG_PATH.exists():
        print(f"Error: ffmpeg not found at {FFMPEG_PATH}", file=sys.stderr)
        sys.exit(1)

    success = send_voice(user_id, message)

    if success:
        print(f"Voice message sent to user {user_id}")
        sys.exit(0)
    else:
        print("Failed to send voice message", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
