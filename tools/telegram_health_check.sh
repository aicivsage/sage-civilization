#!/bin/bash
# Telegram Bridge Health Check & Auto-Recovery
# Returns: 0=healthy, 1=restarted, 2=failed

echo "=== Telegram Bridge Health Check ==="
echo ""

BRIDGE_PID_FILE=".tg_sessions/telegram_bridge.pid"
BRIDGE_LOG="/tmp/sage_telegram_bridge.log"
HEALTHY=true

# Check PID file
if [ -f "$BRIDGE_PID_FILE" ]; then
    BRIDGE_PID=$(cat "$BRIDGE_PID_FILE" 2>/dev/null)
    echo "PID file found: $BRIDGE_PID"

    # Check if process running
    if ps -p "$BRIDGE_PID" > /dev/null 2>&1; then
        echo "Process status: ✓ RUNNING"
    else
        echo "Process status: ❌ DEAD (PID $BRIDGE_PID not found)"
        HEALTHY=false
    fi
else
    echo "PID file: ❌ NOT FOUND (bridge not running)"
    HEALTHY=false
fi

# Check for 409 errors in recent logs
if [ -f "$BRIDGE_LOG" ]; then
    if tail -50 "$BRIDGE_LOG" 2>/dev/null | grep -q "409 Conflict"; then
        echo "🚨 ALERT: 409 Conflict detected in recent logs"
        echo "         Multiple instances were running - bridge likely dead"
        HEALTHY=false
    fi
fi

# If unhealthy, attempt recovery
if [ "$HEALTHY" = false ]; then
    echo ""
    echo "=== ATTEMPTING AUTO-RECOVERY ==="

    # Kill any existing bridge processes
    echo "1. Killing any existing bridge processes..."
    pkill -f "telegram_bridge.py" 2>/dev/null
    sleep 2

    # Remove stale PID file
    echo "2. Removing stale PID file..."
    rm -f "$BRIDGE_PID_FILE"

    # Restart via boot script
    echo "3. Restarting bridge via boot script..."
    bash tools/acg_telegram_boot.sh

    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ Recovery successful - bridge restarted"
        exit 1  # Return 1 to indicate restart occurred
    else
        echo ""
        echo "❌ Recovery failed - manual intervention required"
        exit 2  # Return 2 to indicate failure
    fi
else
    echo ""
    echo "✓ Bridge is healthy"
    exit 0  # Return 0 to indicate healthy
fi
