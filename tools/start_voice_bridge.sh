#!/bin/bash
#
# Start Sage Voice Bridge
# Enables voice input/output through Telegram with British accent
#

PROJECT_ROOT="/mnt/c/sage/sage-civilization"
VENV_PATH="$PROJECT_ROOT/venv"
SCRIPT_PATH="$PROJECT_ROOT/tools/sage_voice_bridge.py"
PID_FILE="$PROJECT_ROOT/.tg_sessions/voice_bridge.pid"
LOG_FILE="$PROJECT_ROOT/logs/voice_bridge.log"

cd "$PROJECT_ROOT"

# Check if already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "Voice bridge already running (PID: $OLD_PID)"
        echo "Use ./tools/stop_voice_bridge.sh to stop it first"
        exit 1
    fi
fi

# Activate venv
source "$VENV_PATH/bin/activate"

# Verify dependencies
python3 -c "import speech_recognition; import gtts; import telegram" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Missing dependencies. Run:"
    echo "  source venv/bin/activate"
    echo "  pip install SpeechRecognition gTTS python-telegram-bot"
    exit 1
fi

# Verify ffmpeg
FFMPEG_PATH="$PROJECT_ROOT/tools/bin/ffmpeg-7.0.2-amd64-static/ffmpeg"
if [ ! -f "$FFMPEG_PATH" ]; then
    echo "ERROR: ffmpeg not found at $FFMPEG_PATH"
    exit 1
fi

echo "Starting Sage Voice Bridge..."
echo "  - STT: Google Speech Recognition (free)"
echo "  - TTS: gTTS with British accent"
echo "  - ffmpeg: $FFMPEG_PATH"

# Ensure directories
mkdir -p "$PROJECT_ROOT/.tg_sessions"
mkdir -p "$PROJECT_ROOT/.tg_voice_temp"
mkdir -p "$PROJECT_ROOT/logs"

# Start
nohup python3 "$SCRIPT_PATH" > "$LOG_FILE" 2>&1 &
NEW_PID=$!

echo "$NEW_PID" > "$PID_FILE"

sleep 2
if ps -p "$NEW_PID" > /dev/null 2>&1; then
    echo "✓ Voice bridge started (PID: $NEW_PID)"
    echo "Log: $LOG_FILE"
    echo ""
    echo "Test: Send /voice_test in Telegram"
else
    echo "ERROR: Voice bridge failed to start"
    echo "Check: $LOG_FILE"
    rm -f "$PID_FILE"
    exit 1
fi
