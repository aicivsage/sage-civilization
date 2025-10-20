#!/bin/bash
# URGENT FIX: Telegram monitor stuck detecting old summaries
# Root cause: State file has 5 old hashes from Oct 18, monitor thinks all messages are duplicates
# Solution: Clear state file + restart monitor

PROJECT_ROOT="/home/corey/projects/AI-CIV/grow_gemini_deepresearch"
STATE_FILE="$PROJECT_ROOT/.tg_sessions/monitor_state.json"
PID_FILE="$PROJECT_ROOT/.tg_sessions/acgee_monitor.pid"
MONITOR_LOG="/tmp/acgee_telegram_monitor.log"

echo "=== URGENT FIX: Telegram Monitor Stuck ==="
echo ""

# Step 1: Stop monitor (if running)
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    echo "Step 1: Stopping old monitor (PID: $OLD_PID)..."

    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        kill "$OLD_PID" 2>/dev/null
        sleep 2

        # Force kill if needed
        if ps -p "$OLD_PID" > /dev/null 2>&1; then
            kill -9 "$OLD_PID" 2>/dev/null
            sleep 1
        fi
        echo "✓ Monitor stopped"
    else
        echo "✓ Monitor not running (stale PID)"
    fi

    rm -f "$PID_FILE"
else
    echo "Step 1: No PID file found"

    # Fallback: kill any monitor in our directory
    ORPHAN_PID=$(pgrep -f "grow_gemini_deepresearch/tools/telegram_monitor.py")
    if [ -n "$ORPHAN_PID" ]; then
        echo "Found orphaned monitor (PID: $ORPHAN_PID), killing..."
        kill -9 "$ORPHAN_PID" 2>/dev/null
        sleep 1
        echo "✓ Orphan killed"
    else
        echo "✓ No monitor process running"
    fi
fi

echo ""

# Step 2: Backup and clear state file
if [ -f "$STATE_FILE" ]; then
    echo "Step 2: Clearing state file (backing up first)..."
    cp "$STATE_FILE" "${STATE_FILE}.backup.$(date +%s)"
    echo '{"last_summaries": [], "last_buffer_position": 0}' > "$STATE_FILE"
    echo "✓ State file cleared (old hashes removed)"
    echo "✓ Backup saved: ${STATE_FILE}.backup.*"
else
    echo "Step 2: No state file found (will create fresh)"
    mkdir -p "$PROJECT_ROOT/.tg_sessions"
    echo '{"last_summaries": [], "last_buffer_position": 0}' > "$STATE_FILE"
    echo "✓ Fresh state file created"
fi

echo ""

# Step 3: Clear old log (fresh start)
echo "Step 3: Clearing old monitor log..."
rm -f "$MONITOR_LOG"
echo "✓ Old log cleared"

echo ""

# Step 4: Start monitor with 30-second interval
echo "Step 4: Starting fresh monitor (interval: 30s)..."
cd "$PROJECT_ROOT"
nohup python3 tools/telegram_monitor.py --interval 30 >> "$MONITOR_LOG" 2>&1 &
NEW_PID=$!

sleep 3

# Step 5: Verify running
echo ""
echo "Step 5: Verifying monitor is running..."

if ps -p $NEW_PID > /dev/null 2>&1; then
    echo "✓ Monitor RUNNING (PID: $NEW_PID)"
    echo "✓ PID file: $PID_FILE"
    echo ""
    echo "First 20 lines of new log:"
    tail -20 "$MONITOR_LOG"
    echo ""
    echo "=== FIX COMPLETE ==="
    echo ""
    echo "Next steps:"
    echo "1. Send test wrapped message in tmux:"
    echo "   echo '🤖🎯📱'"
    echo "   echo 'TEST MESSAGE'"
    echo "   echo '✨🔚'"
    echo ""
    echo "2. Wait 30 seconds, check Telegram for delivery"
    echo "3. Check monitor log: tail -f $MONITOR_LOG"
    echo ""
    exit 0
else
    echo "✗ FAILED TO START MONITOR"
    echo ""
    echo "Check monitor log for errors:"
    cat "$MONITOR_LOG"
    echo ""
    exit 1
fi
