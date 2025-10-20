#!/bin/bash
# Restart A-C-Gee telegram_monitor.py
# Usage: bash tools/restart_telegram_monitor.sh

MONITOR_LOG="/tmp/acgee_telegram_monitor.log"
PROJECT_ROOT="/home/corey/projects/AI-CIV/grow_gemini_deepresearch"
PID_FILE="$PROJECT_ROOT/.tg_sessions/acgee_monitor.pid"

echo "=== Restarting A-C-Gee telegram_monitor.py ==="

# Check PID file first (civilization-specific)
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    echo "Found PID file with PID: $OLD_PID"

    # Check if process is actually running
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "Stopping existing A-C-Gee monitor (PID: $OLD_PID)..."
        kill "$OLD_PID"
        sleep 2

        # Force kill if still running
        if ps -p "$OLD_PID" > /dev/null 2>&1; then
            echo "Force killing..."
            kill -9 "$OLD_PID"
            sleep 1
        fi
        echo "✓ Stopped"
    else
        echo "Process $OLD_PID not running (stale PID file)"
    fi

    # Remove PID file
    rm -f "$PID_FILE"
else
    echo "No PID file found"

    # Fallback: Check for any monitor in our directory (safety check)
    MONITOR_PID=$(pgrep -f "grow_gemini_deepresearch/tools/telegram_monitor.py")
    if [ -n "$MONITOR_PID" ]; then
        echo "Found orphaned monitor process (PID: $MONITOR_PID)..."
        kill "$MONITOR_PID"
        sleep 2

        # Force kill if still running
        if ps -p "$MONITOR_PID" > /dev/null 2>&1; then
            echo "Force killing..."
            kill -9 "$MONITOR_PID"
            sleep 1
        fi
        echo "✓ Stopped"
    else
        echo "No existing A-C-Gee monitor process found"
    fi
fi

# Start new process
echo "Starting new A-C-Gee telegram_monitor.py (interval: 30s)..."
cd "$PROJECT_ROOT"
nohup python3 tools/telegram_monitor.py --interval 30 >> "$MONITOR_LOG" 2>&1 &
NEW_PID=$!

sleep 2

# Verify it's running
if ps -p $NEW_PID > /dev/null; then
    echo "✓ A-C-Gee telegram_monitor.py restarted successfully (PID: $NEW_PID)"
    echo "✓ PID file: $PID_FILE"
    echo ""
    echo "Tailing last 10 lines of log:"
    tail -10 "$MONITOR_LOG"
    exit 0
else
    echo "✗ Failed to restart telegram_monitor.py"
    echo "Check log: $MONITOR_LOG"
    exit 1
fi
