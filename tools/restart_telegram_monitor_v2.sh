#!/bin/bash
# =============================================================================
# Restart Telegram Monitor V2
# =============================================================================
#
# Stops existing V2 monitor (if running) and starts fresh instance.
#
# Usage:
#   bash tools/restart_telegram_monitor_v2.sh [INTERVAL]
#
# Arguments:
#   INTERVAL: Polling interval in seconds (default: 30)
#
# =============================================================================

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

MONITOR_SCRIPT="tools/telegram_monitor_v2.py"
PID_FILE=".tg_sessions/acgee_monitor_v2.pid"
LOG_FILE="/tmp/acgee_telegram_monitor_v2.log"
INTERVAL="${1:-30}"

echo "🔄 Restarting Telegram Monitor V2"
echo "   Project: $PROJECT_ROOT"
echo "   Interval: ${INTERVAL}s"
echo

# Stop existing monitor
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    echo "Stopping existing V2 monitor (PID: $OLD_PID)..."

    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        kill "$OLD_PID" 2>/dev/null || true
        sleep 1

        # Force kill if still running
        if ps -p "$OLD_PID" > /dev/null 2>&1; then
            echo "   Force killing..."
            kill -9 "$OLD_PID" 2>/dev/null || true
        fi
    fi

    rm -f "$PID_FILE"
    echo "   ✅ Stopped"
else
    echo "No existing V2 monitor found"
fi

# Clear old log
echo "Clearing old log..."
> "$LOG_FILE"

# Start monitor
echo
echo "Starting V2 monitor..."
nohup python3 "$MONITOR_SCRIPT" --interval "$INTERVAL" --tmux-session "3" >> "$LOG_FILE" 2>&1 &
NEW_PID=$!

# Wait for PID file creation
sleep 2

# Verify running
if ps -p "$NEW_PID" > /dev/null 2>&1; then
    echo "   ✅ Started (PID: $NEW_PID)"
    echo
    echo "Monitor V2 running!"
    echo
    echo "Check status:"
    echo "   ps aux | grep telegram_monitor_v2.py"
    echo
    echo "View logs:"
    echo "   tail -f $LOG_FILE"
    echo
    echo "Recent log output:"
    sleep 1
    tail -20 "$LOG_FILE"
else
    echo "   ❌ Failed to start"
    echo
    echo "Check log for errors:"
    echo "   cat $LOG_FILE"
    exit 1
fi
