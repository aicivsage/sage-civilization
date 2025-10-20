#!/usr/bin/env bash
#
# Telegram System Restoration Script
# Restores telegram scripts to Oct 17 working state (commit 9069c81)
# while preserving all today's learning and documentation
#
# Date: 2025-10-18
# Agent: git-specialist
# Priority: URGENT
#

set -e  # Exit on error

PROJECT_ROOT="/home/corey/projects/AI-CIV/grow_gemini_deepresearch"
OCT17_COMMIT="9069c81"

echo "========================================="
echo "Telegram System Restoration to Oct 17"
echo "========================================="
echo ""
echo "Commit: $OCT17_COMMIT"
echo "Working Directory: $PROJECT_ROOT"
echo ""

cd "$PROJECT_ROOT"

echo "Step 1: List telegram files in Oct 17 commit..."
echo "--------------------------------------"
git ls-tree "$OCT17_COMMIT" -- tools/ | grep telegram
echo ""

echo "Step 2: Restore telegram scripts to Oct 17 state..."
echo "--------------------------------------"

# Restore each telegram script
for script in telegram_bridge.py telegram_monitor.py send_telegram_direct.py send_telegram_file.py send_telegram_plain.py; do
    if git ls-tree "$OCT17_COMMIT" -- "tools/$script" &>/dev/null; then
        echo "Restoring tools/$script from $OCT17_COMMIT..."
        git checkout "$OCT17_COMMIT" -- "tools/$script" 2>&1 || echo "  (file may not exist in that commit)"
    else
        echo "Skipping tools/$script (not in Oct 17 commit)"
    fi
done

echo ""
echo "Step 3: Stop all running telegram processes..."
echo "--------------------------------------"

# Kill telegram bridge
if pgrep -f telegram_bridge.py >/dev/null; then
    echo "Stopping telegram_bridge.py..."
    pkill -f telegram_bridge.py
    sleep 2
else
    echo "telegram_bridge.py not running"
fi

# Kill telegram monitor
if pgrep -f telegram_monitor.py >/dev/null; then
    echo "Stopping telegram_monitor.py..."
    pkill -f telegram_monitor.py
    sleep 2
else
    echo "telegram_monitor.py not running"
fi

echo ""
echo "Step 4: Clear old state..."
echo "--------------------------------------"

if [ -f "$PROJECT_ROOT/.tg_sessions/monitor_state.json" ]; then
    echo "Removing monitor_state.json..."
    rm -f "$PROJECT_ROOT/.tg_sessions/monitor_state.json"
else
    echo "monitor_state.json already clear"
fi

echo ""
echo "Step 5: Start telegram bridge (Oct 17 version)..."
echo "--------------------------------------"

nohup python3 "$PROJECT_ROOT/tools/telegram_bridge.py" > /tmp/telegram_bridge.log 2>&1 &
BRIDGE_PID=$!
echo "Bridge started: PID $BRIDGE_PID"
sleep 2

# Verify bridge is running
if ps -p $BRIDGE_PID > /dev/null; then
    echo "✓ Bridge confirmed running"
else
    echo "✗ Bridge failed to start - check /tmp/telegram_bridge.log"
    exit 1
fi

echo ""
echo "Step 6: Start telegram monitor (Oct 17 version)..."
echo "--------------------------------------"

nohup python3 "$PROJECT_ROOT/tools/telegram_monitor.py" --interval 30 > /tmp/telegram_monitor.log 2>&1 &
MONITOR_PID=$!
echo "Monitor started: PID $MONITOR_PID"
sleep 2

# Verify monitor is running
if ps -p $MONITOR_PID > /dev/null; then
    echo "✓ Monitor confirmed running"
else
    echo "✗ Monitor failed to start - check /tmp/telegram_monitor.log"
    exit 1
fi

echo ""
echo "========================================="
echo "RESTORATION COMPLETE"
echo "========================================="
echo ""
echo "Bridge PID: $BRIDGE_PID"
echo "Monitor PID: $MONITOR_PID"
echo ""
echo "Logs:"
echo "  Bridge: /tmp/telegram_bridge.log"
echo "  Monitor: /tmp/telegram_monitor.log"
echo ""
echo "Verify processes:"
echo "  ps aux | grep telegram"
echo ""
echo "Test with wrapped message:"
echo '  tmux send-keys -t 0:0 "echo '"'"'🤖🎯📱'"'"'" Enter'
echo '  tmux send-keys -t 0:0 "echo '"'"'Test after restoration'"'"'" Enter'
echo '  tmux send-keys -t 0:0 "echo '"'"'✨🔚'"'"'" Enter'
echo ""
echo "Expected: Message appears in Telegram within 30 seconds"
echo ""
