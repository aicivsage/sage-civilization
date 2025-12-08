#!/bin/bash
#
# Stop Sage Voice Bridge
#

PROJECT_ROOT="/mnt/c/sage/sage-civilization"
PID_FILE="$PROJECT_ROOT/.tg_sessions/voice_bridge.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        kill "$PID"
        echo "✓ Voice bridge stopped (PID: $PID)"
    else
        echo "Process $PID not running"
    fi
    rm -f "$PID_FILE"
else
    echo "No PID file found"
    # Try to kill by process name
    pkill -f "sage_voice_bridge.py" && echo "Killed by process name"
fi
