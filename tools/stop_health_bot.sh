#!/bin/bash
# Stop A-C-Gee Health Coach Bot
# Usage: ./tools/stop_health_bot.sh

PID_FILE="/tmp/health_bot.pid"

echo "=== Stopping A-C-Gee Health Coach Bot ==="

if [ ! -f "$PID_FILE" ]; then
    echo "❌ Health bot not running (no PID file found)"
    exit 1
fi

PID=$(cat "$PID_FILE")

if ps -p "$PID" > /dev/null 2>&1; then
    echo "🛑 Stopping health bot (PID: $PID)..."
    kill "$PID"

    # Wait for graceful shutdown
    sleep 2

    if ps -p "$PID" > /dev/null 2>&1; then
        echo "⚠️  Graceful shutdown failed, forcing..."
        kill -9 "$PID"
        sleep 1
    fi

    if ! ps -p "$PID" > /dev/null 2>&1; then
        echo "✅ Health bot stopped successfully"
        rm "$PID_FILE"
    else
        echo "❌ Failed to stop health bot"
        exit 1
    fi
else
    echo "⚠️  Health bot not running (stale PID file)"
    rm "$PID_FILE"
fi
