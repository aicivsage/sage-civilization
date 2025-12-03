#!/usr/bin/env python3
"""
Telegram Voice Bridge for Sage Civilization
Enables voice input (STT) and voice output (TTS) through Telegram

Architecture:
- Receives voice messages from Telegram
- Converts to text using Google Speech Recognition (free)
- Injects text into Primary AI tmux session
- Converts AI text responses to speech using gTTS
- Sends voice response back to Telegram

This is a SEPARATE module that enhances telegram_bridge.py
DO NOT modify telegram_bridge.py directly!

Dependencies:
- SpeechRecognition (Google Speech Recognition API - free)
- gTTS (Google Text-to-Speech - free)
- pydub (audio conversion)
- ffmpeg (static binary in tools/bin/)

Usage:
    python3 tools/telegram_voice_bridge.py

Registry: memories/agents/tg-archi/telegram_script_registry.json
"""

import asyncio
import json
import logging
import os
import subprocess
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Tuple

import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment

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

# Constants
PROJECT_ROOT = Path(__file__).parent.parent.parent  # tools/voice_bridge/ -> tools/ -> project root
SESSION_DIR = PROJECT_ROOT / ".tg_sessions"
CONFIG_FILE = PROJECT_ROOT / "config" / "telegram_config.json"
VOICE_TEMP_DIR = PROJECT_ROOT / ".tg_voice_temp"
FFMPEG_PATH = PROJECT_ROOT / "tools" / "bin" / "ffmpeg-7.0.2-amd64-static" / "ffmpeg"
FFPROBE_PATH = PROJECT_ROOT / "tools" / "bin" / "ffmpeg-7.0.2-amd64-static" / "ffprobe"

# Set ffmpeg paths for pydub
AudioSegment.converter = str(FFMPEG_PATH)
AudioSegment.ffprobe = str(FFPROBE_PATH)

DEFAULT_CONFIG = {
    "tmux_session": "claude-work",
    "tmux_pane": "claude-work:0.0",
    "working_directory": str(PROJECT_ROOT),
    "response_timeout": 10,
    "max_response_length": 4000,
    "voice_enabled": True,
    "tts_language": "en"
}

# Ensure directories exist
SESSION_DIR.mkdir(exist_ok=True)
VOICE_TEMP_DIR.mkdir(exist_ok=True)


class VoiceBridge:
    """Voice bridge for Telegram with STT and TTS capabilities."""

    def __init__(self, config: Dict):
        """Initialize voice bridge with configuration."""
        self.config = config
        self.authorized_users = config.get("authorized_users", {})
        self.tmux_pane = config.get("tmux_pane", DEFAULT_CONFIG["tmux_pane"])
        self.response_timeout = config.get("response_timeout", DEFAULT_CONFIG["response_timeout"])
        self.max_response_length = config.get("max_response_length", DEFAULT_CONFIG["max_response_length"])
        self.tts_language = config.get("tts_language", DEFAULT_CONFIG["tts_language"])

        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()

        # Verify ffmpeg exists
        if not FFMPEG_PATH.exists():
            raise FileNotFoundError(f"ffmpeg not found at {FFMPEG_PATH}")

        logger.info(f"Voice bridge initialized with ffmpeg at {FFMPEG_PATH}")

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

    async def download_voice_message(self, voice: Voice, context: ContextTypes.DEFAULT_TYPE) -> Optional[Path]:
        """
        Download voice message from Telegram.

        Returns path to downloaded .ogg file.
        """
        try:
            # Get file from Telegram
            file = await context.bot.get_file(voice.file_id)

            # Create temp file path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ogg_path = VOICE_TEMP_DIR / f"voice_{timestamp}.ogg"

            # Download file
            await file.download_to_drive(ogg_path)
            logger.info(f"Downloaded voice message to {ogg_path}")

            return ogg_path

        except Exception as e:
            logger.error(f"Failed to download voice message: {e}")
            return None

    def convert_ogg_to_wav(self, ogg_path: Path) -> Optional[Path]:
        """
        Convert OGG file to WAV format for speech recognition.

        Returns path to WAV file.
        """
        try:
            wav_path = ogg_path.with_suffix('.wav')

            # Use ffmpeg directly for conversion
            result = subprocess.run([
                str(FFMPEG_PATH),
                '-i', str(ogg_path),
                '-acodec', 'pcm_s16le',
                '-ar', '16000',
                '-ac', '1',
                str(wav_path),
                '-y'  # Overwrite if exists
            ], capture_output=True, text=True, timeout=30)

            if result.returncode != 0:
                logger.error(f"ffmpeg conversion failed: {result.stderr}")
                return None

            logger.info(f"Converted {ogg_path} to {wav_path}")
            return wav_path

        except Exception as e:
            logger.error(f"Failed to convert audio: {e}")
            return None

    def transcribe_audio(self, wav_path: Path) -> Optional[str]:
        """
        Transcribe WAV audio to text using Google Speech Recognition.

        Returns transcribed text or None on failure.
        """
        try:
            with sr.AudioFile(str(wav_path)) as source:
                audio = self.recognizer.record(source)

            # Use Google Speech Recognition (free, no API key needed)
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Transcribed: {text[:100]}...")
            return text

        except sr.UnknownValueError:
            logger.warning("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition: {e}")
            return None
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return None

    def inject_to_tmux(self, message: str, username: str = "user") -> bool:
        """
        Inject message to Primary AI tmux session.
        """
        try:
            # Format message with voice indicator
            formatted = f"[VOICE from @{username}] {message}"

            logger.info(f"Injecting voice message to tmux: {formatted[:100]}...")

            # Send to tmux
            subprocess.run(
                ["tmux", "send-keys", "-t", self.tmux_pane, "-l", formatted],
                check=True,
                timeout=5
            )

            # Press Enter
            subprocess.run(
                ["tmux", "send-keys", "-t", self.tmux_pane, "Enter"],
                check=True,
                timeout=5
            )

            logger.info("tmux injection successful")
            return True

        except Exception as e:
            logger.error(f"tmux injection failed: {e}")
            return False

    def text_to_speech(self, text: str) -> Optional[Path]:
        """
        Convert text to speech using gTTS.

        Returns path to MP3 file.
        """
        try:
            # Truncate very long responses for TTS
            if len(text) > 2000:
                text = text[:2000] + "... Message truncated for voice response."

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            mp3_path = VOICE_TEMP_DIR / f"response_{timestamp}.mp3"

            # Generate speech
            tts = gTTS(text=text, lang=self.tts_language, slow=False)
            tts.save(str(mp3_path))

            logger.info(f"Generated TTS audio: {mp3_path}")
            return mp3_path

        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            return None

    def convert_mp3_to_ogg(self, mp3_path: Path) -> Optional[Path]:
        """
        Convert MP3 to OGG Opus format for Telegram voice message.

        Returns path to OGG file.
        """
        try:
            ogg_path = mp3_path.with_suffix('.ogg')

            # Convert using ffmpeg with Opus codec
            result = subprocess.run([
                str(FFMPEG_PATH),
                '-i', str(mp3_path),
                '-acodec', 'libopus',
                '-b:a', '32k',
                str(ogg_path),
                '-y'
            ], capture_output=True, text=True, timeout=30)

            if result.returncode != 0:
                logger.error(f"ffmpeg OGG conversion failed: {result.stderr}")
                return None

            logger.info(f"Converted {mp3_path} to {ogg_path}")
            return ogg_path

        except Exception as e:
            logger.error(f"MP3 to OGG conversion failed: {e}")
            return None

    def cleanup_temp_files(self, *paths):
        """Remove temporary audio files."""
        for path in paths:
            if path and path.exists():
                try:
                    path.unlink()
                    logger.debug(f"Cleaned up {path}")
                except Exception as e:
                    logger.warning(f"Failed to cleanup {path}: {e}")

    def save_session(self, user_id: int, message_count: int, voice_count: int = 0):
        """Save session data."""
        session_file = SESSION_DIR / f"{user_id}.json"

        data = {
            "user_id": user_id,
            "message_count": message_count,
            "voice_count": voice_count,
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
            return {"user_id": user_id, "message_count": 0, "voice_count": 0}

        try:
            with open(session_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load session: {e}")
            return {"user_id": user_id, "message_count": 0, "voice_count": 0}


# Global bridge instance
bridge: Optional[VoiceBridge] = None


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
Welcome to Sage Voice Bridge!

You are authorized as: {user_info.get('name', 'User')}
Role: {user_info.get('role', 'member')}

This bridge supports VOICE interaction:
- Send a voice message and I'll transcribe it to text
- Your message will be sent to Sage
- Responses can be sent back as voice or text

Commands:
/start - Show this welcome message
/help - Show available commands
/ping - Health check
/voice_status - Check voice system status

Simply send a voice message or text to communicate with Sage!
"""

    await update.message.reply_text(welcome_msg)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    user_id = update.effective_user.id

    if not bridge.is_authorized(user_id):
        await update.message.reply_text("Unauthorized.")
        return

    help_msg = """
Sage Voice Bridge - Commands:

/start - Welcome message
/help - This help message
/ping - Health check
/voice_status - Voice system status

Voice Messaging:
- Send a voice message (hold mic button)
- I'll transcribe it and send to Sage
- Text responses sent back (voice TTS coming soon)

Session Info:
- Voice and text messages tracked
- Session persists across restarts

Technical:
- STT: Google Speech Recognition (free)
- TTS: gTTS (Google Text-to-Speech, free)
- Audio: ffmpeg for format conversion
"""

    await update.message.reply_text(help_msg)


async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ping command."""
    user_id = update.effective_user.id

    if not bridge.is_authorized(user_id):
        await update.message.reply_text("Unauthorized.")
        return

    tmux_ok = bridge._check_tmux_session()
    session = bridge.load_session(user_id)

    status_msg = f"""
Pong!

Bridge Status: Online
Voice: Enabled
tmux Session: {'Connected' if tmux_ok else 'WARNING: Not found'}
Session: {bridge.tmux_pane}

Your Stats:
- User ID: {user_id}
- Text Messages: {session.get('message_count', 0)}
- Voice Messages: {session.get('voice_count', 0)}
"""

    await update.message.reply_text(status_msg)


async def voice_status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /voice_status command."""
    user_id = update.effective_user.id

    if not bridge.is_authorized(user_id):
        await update.message.reply_text("Unauthorized.")
        return

    ffmpeg_ok = FFMPEG_PATH.exists()

    status_msg = f"""
Voice System Status:

STT Engine: Google Speech Recognition
- Status: Ready (free, no API key needed)
- Language: Auto-detect

TTS Engine: gTTS (Google TTS)
- Status: Ready
- Language: {bridge.tts_language}

Audio Processing:
- ffmpeg: {'OK' if ffmpeg_ok else 'MISSING'}
- Path: {FFMPEG_PATH}

Temp Directory: {VOICE_TEMP_DIR}
"""

    await update.message.reply_text(status_msg)


async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle voice messages - transcribe and inject to tmux.
    """
    user = update.effective_user
    user_id = user.id

    if not bridge.is_authorized(user_id):
        await update.message.reply_text("Unauthorized.")
        return

    voice = update.message.voice
    username = user.username or user.first_name or "user"

    logger.info(f"Voice message from @{username} (ID: {user_id}), duration: {voice.duration}s")

    # Send processing indicator
    processing_msg = await update.message.reply_text("Processing voice message...")

    ogg_path = None
    wav_path = None

    try:
        # Download voice message
        ogg_path = await bridge.download_voice_message(voice, context)
        if not ogg_path:
            await processing_msg.edit_text("Failed to download voice message.")
            return

        # Convert to WAV
        wav_path = bridge.convert_ogg_to_wav(ogg_path)
        if not wav_path:
            await processing_msg.edit_text("Failed to convert audio format.")
            return

        # Transcribe
        transcription = bridge.transcribe_audio(wav_path)
        if not transcription:
            await processing_msg.edit_text(
                "Could not transcribe voice message. Please try again or speak more clearly."
            )
            return

        # Show transcription
        await processing_msg.edit_text(f"Transcribed: \"{transcription}\"\n\nSending to Sage...")

        # Inject to tmux
        injection_success = bridge.inject_to_tmux(transcription, username)

        if not injection_success:
            await update.message.reply_text("Failed to send message to Sage.")
            return

        # Update session
        session = bridge.load_session(user_id)
        session["voice_count"] = session.get("voice_count", 0) + 1
        bridge.save_session(user_id, session.get("message_count", 0), session["voice_count"])

        # Confirm delivery
        await processing_msg.edit_text(
            f"Transcribed: \"{transcription}\"\n\n"
            f"Message delivered to Sage. Response will be sent shortly."
        )

        logger.info(f"Voice message processed successfully for user {user_id}")

    finally:
        # Cleanup temp files
        bridge.cleanup_temp_files(ogg_path, wav_path)


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle text messages - inject to tmux (same as original bridge).
    """
    user = update.effective_user
    user_id = user.id

    if not bridge.is_authorized(user_id):
        await update.message.reply_text("Unauthorized.")
        return

    message_text = update.message.text
    username = user.username or user.first_name or "user"

    logger.info(f"Text message from @{username} (ID: {user_id}): {message_text[:50]}...")

    # Inject message to tmux
    injection_success = bridge.inject_to_tmux(message_text.replace("[VOICE from @", "[TELEGRAM from @"), username)

    if not injection_success:
        logger.error(f"Failed to inject message from user {user_id}")
        return

    # Update session
    session = bridge.load_session(user_id)
    session["message_count"] = session.get("message_count", 0) + 1
    bridge.save_session(user_id, session["message_count"], session.get("voice_count", 0))

    logger.info(f"Text message processed for user {user_id}")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")

    if update and update.effective_message:
        await update.effective_message.reply_text(
            f"An error occurred: {str(context.error)}"
        )


def load_config() -> Dict:
    """Load configuration from file."""
    config = DEFAULT_CONFIG.copy()

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

    bot_token = config.get("bot_token") or os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise ValueError("No bot token found.")

    config["bot_token"] = bot_token

    if not config.get("authorized_users"):
        raise ValueError("No authorized users configured.")

    return config


def main():
    """Main entry point."""
    global bridge

    # Set process name
    try:
        import setproctitle
        setproctitle.setproctitle("sage_voice_bridge")
    except ImportError:
        pass

    logger.info("Starting Sage Voice Bridge")

    # Load configuration
    try:
        config = load_config()
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        return 1

    # Initialize voice bridge
    try:
        bridge = VoiceBridge(config)
        logger.info(f"Voice bridge initialized for tmux session: {bridge.tmux_pane}")
    except FileNotFoundError as e:
        logger.error(f"Voice bridge initialization failed: {e}")
        logger.error("Please ensure ffmpeg is installed in tools/bin/")
        return 1

    # Create application
    application = Application.builder().token(config["bot_token"]).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(CommandHandler("voice_status", voice_status_command))

    # Voice message handler (PRIORITY)
    application.add_handler(MessageHandler(filters.VOICE, handle_voice_message))

    # Text message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    application.add_error_handler(error_handler)

    # Start bot
    logger.info("Starting voice bot polling...")
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
