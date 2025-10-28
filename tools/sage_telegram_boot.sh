#!/bin/bash
# Sage Telegram System Boot Script
# Starts both telegram_bridge and telegram_jsonl_monitor
# Created: 2025-10-28 (adapted from A-C-Gee template)
# Enhanced with auto-tmux-detection (tg-archi)

echo "=== Sage Civilization Telegram System Boot ==="
echo ""

# Step 0: Auto-detect and update tmux session in config
echo "Step 0: Auto-detecting current tmux session..."

# Detect current tmux session and pane
if [ -z "$TMUX" ]; then
    echo "❌ ERROR: Not running inside tmux. This script must be run from within a tmux session."
    exit 1
fi

CURRENT_SESSION=$(tmux display-message -p '#S')
CURRENT_PANE=$(tmux display-message -p '#S:#I.#P')

echo "  Detected session: $CURRENT_SESSION"
echo "  Detected pane: $CURRENT_PANE"

# Update config with current session (using jq for safe JSON modification)
CONFIG_FILE="config/telegram_config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ ERROR: Config file not found: $CONFIG_FILE"
    exit 1
fi

# Create backup
cp "$CONFIG_FILE" "$CONFIG_FILE.backup-$(date +%s)"

# Update config
jq --arg session "$CURRENT_SESSION" \
   --arg pane "$CURRENT_PANE" \
   '.tmux_session = $session | .tmux_pane = $pane' \
   "$CONFIG_FILE" > "$CONFIG_FILE.tmp"

if [ $? -eq 0 ]; then
    mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    echo "✓ Config updated with current tmux session"
else
    echo "❌ ERROR: Failed to update config"
    rm -f "$CONFIG_FILE.tmp"
    exit 1
fi
echo ""

# Step 1: Detect current session file
echo "Step 1: Detecting current Sage session file..."
# Adapt this path to match Sage's actual Claude Code project path
PROJECT_DIR="$HOME/.claude/projects/-mnt-c-sage-sage-civilization"
CURRENT_SESSION=$(ls -t "$PROJECT_DIR"/*.jsonl 2>/dev/null | head -1 | xargs basename)

if [ -z "$CURRENT_SESSION" ]; then
    echo "⚠️  WARNING: No JSONL session files found in $PROJECT_DIR"
    echo "   Attempting to find project directory..."
    # Try to find the actual project directory
    FOUND_DIR=$(find "$HOME/.claude/projects" -type d -name "*sage*" 2>/dev/null | head -1)
    if [ -n "$FOUND_DIR" ]; then
        echo "   Found: $FOUND_DIR"
        PROJECT_DIR="$FOUND_DIR"
        CURRENT_SESSION=$(ls -t "$PROJECT_DIR"/*.jsonl 2>/dev/null | head -1 | xargs basename)
    fi

    if [ -z "$CURRENT_SESSION" ]; then
        echo "❌ ERROR: No JSONL session files found"
        echo "   Expected path: $HOME/.claude/projects/-mnt-c-sage-sage-civilization/"
        echo "   Please verify Claude Code project path and update this script"
        exit 1
    fi
fi

echo "✓ Found session: $CURRENT_SESSION"
echo ""

# Step 2: Kill any existing Sage Telegram processes
echo "Step 2: Stopping any existing Sage Telegram processes..."
pkill -f "telegram_bridge.py" 2>/dev/null && echo "  Stopped: telegram_bridge"
pkill -f "telegram_jsonl_monitor.py" 2>/dev/null && echo "  Stopped: telegram_jsonl_monitor"
sleep 2
echo ""

# Step 3: Start telegram bridge (INBOUND)
echo "Step 3: Starting Sage telegram_bridge (INBOUND: Telegram → tmux)..."
python3 tools/telegram_bridge.py > /tmp/sage_telegram_bridge.log 2>&1 &
BRIDGE_PID=$!
sleep 2

if ps -p $BRIDGE_PID > /dev/null; then
    echo "✓ Bridge started (PID: $BRIDGE_PID)"
else
    echo "❌ Bridge failed to start. Check /tmp/sage_telegram_bridge.log"
    exit 1
fi
echo ""

# Step 4: Start JSONL monitor (OUTBOUND)
echo "Step 4: Starting Sage telegram_jsonl_monitor (OUTBOUND: tmux → Telegram)..."
echo "  Watching session: $CURRENT_SESSION"
python3 tools/telegram_jsonl_monitor.py --start-from-now --session-file "$CURRENT_SESSION" > /tmp/sage_telegram_monitor.log 2>&1 &
MONITOR_PID=$!
sleep 2

if ps -p $MONITOR_PID > /dev/null; then
    echo "✓ Monitor started (PID: $MONITOR_PID)"
else
    echo "❌ Monitor failed to start. Check /tmp/sage_telegram_monitor.log"
    exit 1
fi
echo ""

# Step 5: Verify both running
echo "Step 5: Verifying processes..."
ps auxww | grep "telegram_bridge\|telegram_jsonl_monitor" | grep -v grep
echo ""

echo "=== Sage Telegram System READY ==="
echo ""
echo "Logs:"
echo "  Bridge:  /tmp/sage_telegram_bridge.log"
echo "  Monitor: /tmp/sage_telegram_monitor.log"
echo ""
echo "Test:"
echo "  Inbound:  Send message from Telegram → should appear in tmux"
echo "  Outbound: Send wrapped message 🤖🎯📱 ... ✨🔚 → should appear on Telegram"
echo ""
echo "To stop:"
echo "  pkill -f telegram_bridge.py"
echo "  pkill -f telegram_jsonl_monitor.py"
