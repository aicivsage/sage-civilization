#!/bin/bash
# Fix telegram bridge to point to correct tmux session
# Created: 2025-10-20
# Issue: Bridge was pointing to session 3, but Primary is in session 6

set -e

cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch

echo "=== Telegram Bridge Session Fix ==="
echo ""

# Step 1: Find current tmux session
echo "Step 1: Detecting current tmux session..."
CURRENT_SESSION=$(tmux display-message -p '#S:#I.#P')
echo "Current session: $CURRENT_SESSION"
echo ""

# Step 2: Verify config update
echo "Step 2: Verifying config update..."
CONFIGURED_PANE=$(grep -A 1 '"tmux_session"' config/telegram_config.json | grep '"tmux_pane"' | cut -d'"' -f4)
echo "Configured pane: $CONFIGURED_PANE"
echo ""

if [ "$CURRENT_SESSION" != "$CONFIGURED_PANE" ]; then
    echo "WARNING: Config pane ($CONFIGURED_PANE) doesn't match current session ($CURRENT_SESSION)"
    echo "Config should be updated to match current session"
    exit 1
fi

# Step 3: Kill old bridge processes
echo "Step 3: Stopping old telegram_bridge.py processes..."
pkill -f telegram_bridge.py || echo "No telegram_bridge.py processes found (OK)"
sleep 2
echo ""

# Step 4: Restart bridge
echo "Step 4: Starting telegram_bridge.py with correct session..."
nohup python3 tools/telegram_bridge.py > /tmp/telegram_bridge.log 2>&1 &
BRIDGE_PID=$!
echo "Bridge started with PID: $BRIDGE_PID"
echo ""

# Step 5: Verify it started
sleep 2
if ps -p $BRIDGE_PID > /dev/null; then
    echo "✓ Bridge process running (PID: $BRIDGE_PID)"
else
    echo "✗ Bridge failed to start - check /tmp/telegram_bridge.log"
    exit 1
fi

# Step 6: Check logs
echo ""
echo "Step 6: Recent bridge logs:"
tail -10 /tmp/telegram_bridge.log
echo ""

echo "=== Fix Complete ==="
echo ""
echo "Next steps:"
echo "1. Send test message from Telegram: 'test injection'"
echo "2. Check if it appears in tmux session 6"
echo "3. If working, injection is fixed!"
echo ""
echo "Monitor logs: tail -f /tmp/telegram_bridge.log"
