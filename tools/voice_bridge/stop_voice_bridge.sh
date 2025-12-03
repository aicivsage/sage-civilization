#!/bin/bash
#
# Stop Sage Voice Bridge
#

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PID_FILE="$PROJECT_ROOT/.tg_sessions/voice_bridge.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "Voice bridge not running (no PID file found)"

    # Check for any python processes running the script anyway
    ORPHAN_PID=$(pgrep -f "telegram_voice_bridge.py" 2>/dev/null)
    if [ -n "$ORPHAN_PID" ]; then
        echo "Found orphan voice bridge process (PID: $ORPHAN_PID)"
        echo "Stopping..."
        kill "$ORPHAN_PID"
        echo "Stopped."
    fi
    exit 0
fi

PID=$(cat "$PID_FILE")

if ps -p "$PID" > /dev/null 2>&1; then
    echo "Stopping voice bridge (PID: $PID)..."
    kill "$PID"
    sleep 2

    # Force kill if still running
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "Force stopping..."
        kill -9 "$PID"
    fi

    echo "Voice bridge stopped."
else
    echo "Voice bridge was not running (stale PID file)"
fi

rm -f "$PID_FILE"
