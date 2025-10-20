#!/bin/bash
# Check A-C-Gee Health Coach Bot status
# Usage: ./tools/health_bot_status.sh

PID_FILE="/tmp/health_bot.pid"
LOG_FILE="/tmp/health_bot.log"

echo "=== A-C-Gee Health Coach Bot Status ==="
echo ""

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "✅ Status: RUNNING"
        echo "   PID: $PID"

        # Get runtime
        RUNTIME=$(ps -p "$PID" -o etime= | tr -d ' ')
        echo "   Runtime: $RUNTIME"

        # Get memory usage
        MEM=$(ps -p "$PID" -o rss= | tr -d ' ')
        MEM_MB=$((MEM / 1024))
        echo "   Memory: ${MEM_MB}MB"

        echo ""
        echo "📊 Recent log activity:"
        tail -10 "$LOG_FILE"
    else
        echo "❌ Status: STOPPED (stale PID file)"
        rm "$PID_FILE" 2>/dev/null
    fi
else
    echo "❌ Status: STOPPED (not running)"
fi

echo ""
echo "Commands:"
echo "  Start: ./tools/start_health_bot.sh"
echo "  Stop:  ./tools/stop_health_bot.sh"
echo "  Logs:  tail -f $LOG_FILE"
