#!/usr/bin/env python3
"""
Sage Voice Bridge for Telegram
Enables voice input (STT) and voice output (TTS) through Telegram

Based on Parallax implementation by Russell Korus
Adapted for Sage Civilization with British accent

Dependencies:
- SpeechRecognition (Google Speech Recognition API - free)
- gTTS (Google Text-to-Speech - free)
- pydub (audio conversion)
- ffmpeg (static binary)

Usage:
    source venv/bin/activate
    python3 tools/sage_voice_bridge.py
"""

import asyncio
import json
import logging
import os
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict

import speech_recognition as sr
from gtts import gTTS

from telegram import Update, Voice
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

# Paths - Sage specific
PROJECT_ROOT = Path("/mnt/c/sage/sage-civilization")
CONFIG_FILE = PROJECT_ROOT / "config" / "telegram_config.json"
VOICE_TEMP_DIR = PROJECT_ROOT / ".tg_voice_temp"
FFMPEG_PATH = PROJECT_ROOT / "tools" / "bin" / "ffmpeg-7.0.2-amd64-static" / "ffmpeg"
LOG_DIR = PROJECT_ROOT / "logs"

# Sage voice settings - British accent
VOICE_LANG = "en"
VOICE_TLD = "co.uk"  # British accent
VOICE_SLOW = False   # Normal speed

# Ensure directories exist
VOICE_TEMP_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


class SageVoiceBridge:
    """Voice bridge for Sage civilization with British accent."""

    def __init__(self, config: Dict):
        self.config = config
        self.bot_token = config.get("bot_token")
        self.authorized_users = {str(k): v for k, v in config.get("authorized_users", {}).items()}
        self.tmux_session = config.get("tmux_session", "sage-session")
        self.tmux_pane = f"{self.tmux_session}:0.0"

        # Greg's chat ID
        self.greg_chat_id = config.get("greg_chat_id", 7585924762)

        # Speech recognition
        self.recognizer = sr.Recognizer()

        # Verify ffmpeg
        if not FFMPEG_PATH.exists():
            raise FileNotFoundError(f"ffmpeg not found at {FFMPEG_PATH}")

        logger.info(f"Sage Voice Bridge initialized (British accent)")

    def is_authorized(self, user_id: int) -> bool:
        return str(user_id) in self.authorized_users

    async def download_voice(self, voice: Voice, context: ContextTypes.DEFAULT_TYPE) -> Optional[Path]:
        """Download voice message from Telegram."""
        try:
            file = await context.bot.get_file(voice.file_id)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ogg_path = VOICE_TEMP_DIR / f"voice_{timestamp}.ogg"
            await file.download_to_drive(ogg_path)
            logger.info(f"Downloaded voice to {ogg_path}")
            return ogg_path
        except Exception as e:
            logger.error(f"Download failed: {e}")
            return None

    def convert_to_wav(self, ogg_path: Path) -> Optional[Path]:
        """Convert OGG to WAV for speech recognition."""
        try:
            wav_path = ogg_path.with_suffix('.wav')
            result = subprocess.run([
                str(FFMPEG_PATH),
                '-i', str(ogg_path),
                '-acodec', 'pcm_s16le',
                '-ar', '16000',
                '-ac', '1',
                str(wav_path),
                '-y'
            ], capture_output=True, text=True, timeout=30)

            if result.returncode != 0:
                logger.error(f"ffmpeg failed: {result.stderr}")
                return None
            return wav_path
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            return None

    def transcribe(self, wav_path: Path) -> Optional[str]:
        """Transcribe WAV to text using Google Speech Recognition."""
        try:
            with sr.AudioFile(str(wav_path)) as source:
                audio = self.recognizer.record(source)
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Transcribed: {text[:100]}...")
            return text
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return None

    def inject_to_tmux(self, message: str, username: str = "Greg") -> bool:
        """Inject voice message to Primary AI tmux session."""
        try:
            formatted = f"[VOICE from {username}] {message}"
            subprocess.run(
                ["tmux", "send-keys", "-t", self.tmux_pane, "-l", formatted],
                check=True, timeout=5
            )
            subprocess.run(
                ["tmux", "send-keys", "-t", self.tmux_pane, "Enter"],
                check=True, timeout=5
            )
            logger.info("Injected to tmux")
            return True
        except Exception as e:
            logger.error(f"Injection failed: {e}")
            return False

    def text_to_speech(self, text: str) -> Optional[Path]:
        """Convert text to speech with British accent."""
        try:
            # Truncate long responses
            if len(text) > 2000:
                text = text[:2000] + "... Message truncated."

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            mp3_path = VOICE_TEMP_DIR / f"response_{timestamp}.mp3"

            # British accent via tld parameter
            tts = gTTS(text=text, lang=VOICE_LANG, tld=VOICE_TLD, slow=VOICE_SLOW)
            tts.save(str(mp3_path))

            logger.info(f"Generated speech: {mp3_path}")
            return mp3_path
        except Exception as e:
            logger.error(f"TTS failed: {e}")
            return None

    def cleanup_temp_files(self, *paths):
        """Clean up temporary audio files."""
        for path in paths:
            if path and path.exists():
                try:
                    path.unlink()
                except Exception:
                    pass


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming voice messages."""
    bridge: SageVoiceBridge = context.bot_data['bridge']
    user = update.effective_user

    if not bridge.is_authorized(user.id):
        logger.warning(f"Unauthorized voice from {user.id}")
        return

    await update.message.reply_text("🎤 Processing voice message...")

    # Download voice
    ogg_path = await bridge.download_voice(update.message.voice, context)
    if not ogg_path:
        await update.message.reply_text("❌ Failed to download voice message")
        return

    # Convert to WAV
    wav_path = bridge.convert_to_wav(ogg_path)
    if not wav_path:
        await update.message.reply_text("❌ Failed to convert audio")
        bridge.cleanup_temp_files(ogg_path)
        return

    # Transcribe
    text = bridge.transcribe(wav_path)
    if not text:
        await update.message.reply_text("❌ Could not understand audio. Please try again.")
        bridge.cleanup_temp_files(ogg_path, wav_path)
        return

    # Show transcription
    await update.message.reply_text(f"📝 You said: {text}")

    # Inject to tmux
    username = user.username or user.first_name or "User"
    if bridge.inject_to_tmux(text, username):
        await update.message.reply_text("✅ Message sent to Sage")
    else:
        await update.message.reply_text("⚠️ Could not inject to session")

    # Cleanup
    bridge.cleanup_temp_files(ogg_path, wav_path)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages - inject directly to tmux."""
    bridge: SageVoiceBridge = context.bot_data['bridge']
    user = update.effective_user

    if not bridge.is_authorized(user.id):
        await update.message.reply_text("⛔ Unauthorized")
        return

    text = update.message.text
    if not text:
        return

    # Inject to tmux
    username = user.username or user.first_name or "User"
    if bridge.inject_to_tmux(text, username):
        logger.info(f"Text message from {username} injected to tmux: {text[:50]}...")
    else:
        await update.message.reply_text("⚠️ Could not inject to session")
        logger.error(f"Failed to inject text to tmux")


async def cmd_voice_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test voice output with British accent."""
    bridge: SageVoiceBridge = context.bot_data['bridge']

    if not bridge.is_authorized(update.effective_user.id):
        return

    test_text = "Hello Greg, this is Sage speaking with a British accent. The voice bridge is working perfectly."

    mp3_path = bridge.text_to_speech(test_text)
    if mp3_path:
        await update.message.reply_voice(voice=open(mp3_path, 'rb'))
        bridge.cleanup_temp_files(mp3_path)
    else:
        await update.message.reply_text("❌ TTS test failed")


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show voice bridge status."""
    bridge: SageVoiceBridge = context.bot_data['bridge']

    if not bridge.is_authorized(update.effective_user.id):
        return

    status = f"""🎤 Sage Voice Bridge Status

Voice Settings:
- Language: {VOICE_LANG}
- Accent: British (tld={VOICE_TLD})
- Speed: {'Slow' if VOICE_SLOW else 'Normal'}

Infrastructure:
- ffmpeg: {'✅' if FFMPEG_PATH.exists() else '❌'}
- tmux session: {bridge.tmux_session}
- Temp dir: {VOICE_TEMP_DIR}

Commands:
/voice_test - Test voice output
/status - This message
"""
    await update.message.reply_text(status)


def main():
    # Load config
    with open(CONFIG_FILE) as f:
        config = json.load(f)

    # Create bridge
    bridge = SageVoiceBridge(config)

    # Create application
    app = Application.builder().token(config['bot_token']).build()
    app.bot_data['bridge'] = bridge

    # Add handlers
    app.add_handler(CommandHandler("voice_test", cmd_voice_test))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    logger.info("Starting Sage Voice Bridge...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
