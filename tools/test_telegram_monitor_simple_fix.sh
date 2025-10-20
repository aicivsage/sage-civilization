#!/bin/bash
# Test script for telegram_monitor.py simple fix (Option A)
# This validates that the monitor can detect wrapped messages after the fix

set -e

PROJECT_ROOT="/home/corey/projects/AI-CIV/grow_gemini_deepresearch"
cd "$PROJECT_ROOT"

echo "=========================================="
echo "Telegram Monitor Simple Fix Test"
echo "=========================================="
echo ""

# Step 1: Kill existing monitor
echo "Step 1: Stopping existing monitor..."
pkill -f telegram_monitor.py 2>/dev/null && echo "✓ Existing monitor stopped" || echo "✓ No monitor was running"
sleep 2

# Step 2: Clear state to simulate fresh start
echo ""
echo "Step 2: Clearing monitor state for fresh test..."
if [ -f .tg_sessions/monitor_state.json ]; then
    mv .tg_sessions/monitor_state.json .tg_sessions/monitor_state.json.backup
    echo "✓ State backed up and cleared"
else
    echo "✓ No existing state"
fi

# Step 3: Start monitor with 30-second interval for faster testing
echo ""
echo "Step 3: Starting monitor with 30-second interval..."
nohup python3 tools/telegram_monitor.py --interval 30 > /tmp/telegram_monitor_test.log 2>&1 &
MONITOR_PID=$!
echo "✓ Monitor started (PID: $MONITOR_PID)"
echo "  Log: /tmp/telegram_monitor_test.log"

# Step 4: Wait a moment for initialization
echo ""
echo "Step 4: Waiting for monitor initialization (5 seconds)..."
sleep 5

# Step 5: Check monitor is running
echo ""
echo "Step 5: Checking monitor status..."
if ps -p $MONITOR_PID > /dev/null; then
    echo "✓ Monitor is running"
else
    echo "✗ Monitor failed to start!"
    cat /tmp/telegram_monitor_test.log
    exit 1
fi

# Step 6: Inject test wrapped message into tmux
echo ""
echo "Step 6: Injecting test wrapped message..."
TEST_MESSAGE="Monitor simple fix test - $(date)"
tmux send-keys -t 0:0 "echo '🤖🎯📱'" C-m
sleep 1
tmux send-keys -t 0:0 "echo '$TEST_MESSAGE'" C-m
sleep 1
tmux send-keys -t 0:0 "echo '✨🔚'" C-m
echo "✓ Test message injected into tmux"

# Step 7: Wait for monitor polling (35 seconds to ensure it polls)
echo ""
echo "Step 7: Waiting for monitor to poll (35 seconds)..."
for i in {1..35}; do
    echo -n "."
    sleep 1
done
echo ""

# Step 8: Check monitor logs
echo ""
echo "Step 8: Checking monitor logs..."
echo "----------------------------------------"
tail -30 /tmp/telegram_monitor_test.log
echo "----------------------------------------"

# Step 9: Check state file for sent summaries
echo ""
echo "Step 9: Checking state file..."
if [ -f .tg_sessions/monitor_state.json ]; then
    echo "State file contents:"
    cat .tg_sessions/monitor_state.json | jq '.'
else
    echo "⚠ State file not created yet"
fi

# Step 10: Manual verification prompt
echo ""
echo "=========================================="
echo "TEST COMPLETE"
echo "=========================================="
echo ""
echo "Manual verification needed:"
echo "1. Check your Telegram for message: '$TEST_MESSAGE'"
echo "2. Monitor PID: $MONITOR_PID (still running)"
echo "3. Monitor log: /tmp/telegram_monitor_test.log"
echo ""
echo "To stop monitor: pkill -f telegram_monitor.py"
echo "To restore state: mv .tg_sessions/monitor_state.json.backup .tg_sessions/monitor_state.json"
echo ""
