#!/bin/bash
#
# Start Sage Voice Bridge
# Enables voice input/output through Telegram
#
# Usage: ./tools/start_voice_bridge.sh
#
# NOTE: This REPLACES the normal telegram_bridge.py
# The voice bridge handles BOTH voice and text messages
#

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VENV_PATH="$PROJECT_ROOT/venv"
SCRIPT_PATH="$PROJECT_ROOT/tools/voice_bridge/telegram_voice_bridge.py"
PID_FILE="$PROJECT_ROOT/.tg_sessions/voice_bridge.pid"

# Check if already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "Voice bridge already running (PID: $OLD_PID)"
        echo "Use ./tools/stop_voice_bridge.sh to stop it first"
        exit 1
    fi
fi

# Activate virtual environment
if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
    echo "Activated virtual environment"
else
    echo "ERROR: Virtual environment not found at $VENV_PATH"
    echo "Create it with: python3 -m venv venv && pip install -r requirements.txt"
    exit 1
fi

# Verify dependencies
python3 -c "import speech_recognition; import gtts; import telegram" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Missing dependencies. Install with:"
    echo "  source venv/bin/activate"
    echo "  pip install SpeechRecognition gTTS python-telegram-bot"
    exit 1
fi

# Verify ffmpeg
FFMPEG_PATH="$PROJECT_ROOT/tools/bin/ffmpeg-7.0.2-amd64-static/ffmpeg"
if [ ! -f "$FFMPEG_PATH" ]; then
    echo "ERROR: ffmpeg not found at $FFMPEG_PATH"
    echo "Voice bridge requires ffmpeg for audio conversion"
    exit 1
fi

echo "Starting Sage Voice Bridge..."
echo "  - STT: Google Speech Recognition (free)"
echo "  - TTS: gTTS (free)"
echo "  - ffmpeg: $FFMPEG_PATH"

# Start in background
nohup python3 "$SCRIPT_PATH" > "$PROJECT_ROOT/logs/voice_bridge.log" 2>&1 &
NEW_PID=$!

# Save PID
echo "$NEW_PID" > "$PID_FILE"

# Wait a moment and verify
sleep 2
if ps -p "$NEW_PID" > /dev/null 2>&1; then
    echo "Voice bridge started successfully (PID: $NEW_PID)"
    echo "Log file: $PROJECT_ROOT/logs/voice_bridge.log"
    echo ""
    echo "Send a voice message in Telegram to test!"
else
    echo "ERROR: Voice bridge failed to start"
    echo "Check logs: $PROJECT_ROOT/logs/voice_bridge.log"
    rm -f "$PID_FILE"
    exit 1
fi
