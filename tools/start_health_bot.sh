#!/bin/bash
# Start A-C-Gee Health Coach Bot as background service
# Usage: ./tools/start_health_bot.sh

PROJECT_ROOT="/home/corey/projects/AI-CIV/grow_gemini_deepresearch"
cd "$PROJECT_ROOT" || exit 1

BOT_TOKEN="8472258805:AAFdYmIlJozyqIVjNC8PHEDAK_-XZ1vO3T4"
LOG_FILE="/tmp/health_bot.log"
PID_FILE="/tmp/health_bot.pid"

echo "=== Starting A-C-Gee Health Coach Bot ==="

# Check if already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "❌ Health bot already running (PID: $PID)"
        echo "   To restart, run: ./tools/stop_health_bot.sh && ./tools/start_health_bot.sh"
        exit 1
    else
        echo "⚠️  Stale PID file found, removing..."
        rm "$PID_FILE"
    fi
fi

# Ensure pyTelegramBotAPI is installed
if ! python3 -c "import telebot" 2>/dev/null; then
    echo "📦 Installing pyTelegramBotAPI..."
    pip3 install pyTelegramBotAPI
fi

# Start bot in background
echo "🚀 Starting health bot..."
export HEALTH_BOT_TOKEN="$BOT_TOKEN"
nohup python3 -u tools/health_bot_handler.py > "$LOG_FILE" 2>&1 &
PID=$!

# Save PID
echo "$PID" > "$PID_FILE"

# Wait a moment and verify it started
sleep 2
if ps -p "$PID" > /dev/null 2>&1; then
    echo "✅ Health bot started successfully!"
    echo "   PID: $PID"
    echo "   Log: $LOG_FILE"
    echo ""
    echo "Monitor logs: tail -f $LOG_FILE"
    echo "Stop bot: ./tools/stop_health_bot.sh"
else
    echo "❌ Failed to start health bot"
    echo "   Check logs: cat $LOG_FILE"
    rm "$PID_FILE" 2>/dev/null
    exit 1
fi
