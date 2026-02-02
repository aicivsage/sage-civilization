#!/bin/bash
# Deploy Telegram Bridge V2 with JSONL Injection
# Date: 2025-12-29
# Critical fix: Input-waiting states block message processing

set -e  # Exit on error

echo "=========================================="
echo "Telegram Bridge V2 Deployment"
echo "Fix: JSONL injection bypasses stdin blocking"
echo "=========================================="
echo ""

# Step 1: Backup existing bridge
echo "[1/6] Backing up existing bridge..."
BACKUP_DIR="/mnt/c/sage/sage-civilization/backups/telegram"
mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp /mnt/c/sage/sage-civilization/tools/telegram_bridge.py "$BACKUP_DIR/telegram_bridge_${TIMESTAMP}.py"
echo "✓ Backup saved: $BACKUP_DIR/telegram_bridge_${TIMESTAMP}.py"
echo ""

# Step 2: Kill existing bridge process
echo "[2/6] Stopping existing bridge..."
pkill -f sage_telegram_bridge || echo "No existing bridge process found"
pkill -f telegram_bridge.py || echo "No old bridge process found"
sleep 2
echo "✓ Existing processes stopped"
echo ""

# Step 3: Verify stopped
echo "[3/6] Verifying clean shutdown..."
if ps aux | grep -E "(sage_telegram_bridge|telegram_bridge.py)" | grep -v grep; then
    echo "ERROR: Bridge processes still running!"
    exit 1
fi
echo "✓ Clean shutdown confirmed"
echo ""

# Step 4: Deploy V2
echo "[4/6] Deploying V2 bridge..."
cp /mnt/c/sage/sage-civilization/tools/telegram_bridge_v2_jsonl.py /mnt/c/sage/sage-civilization/tools/telegram_bridge.py
chmod +x /mnt/c/sage/sage-civilization/tools/telegram_bridge.py
echo "✓ V2 bridge deployed"
echo ""

# Step 5: Start V2
echo "[5/6] Starting V2 bridge..."
cd /mnt/c/sage/sage-civilization
nohup python3 tools/telegram_bridge.py > /tmp/sage_telegram_bridge.log 2>&1 &
BRIDGE_PID=$!
echo "✓ V2 bridge started (PID: $BRIDGE_PID)"
sleep 3
echo ""

# Step 6: Verify running
echo "[6/6] Verifying V2 operational..."
if ! ps aux | grep -E "sage_telegram_bridge" | grep -v grep; then
    echo "ERROR: V2 bridge not running!"
    echo "Check logs: tail -50 /tmp/sage_telegram_bridge.log"
    exit 1
fi

echo "✓ V2 bridge running"
echo ""

# Show recent logs
echo "=========================================="
echo "Recent V2 Bridge Logs:"
echo "=========================================="
tail -20 /tmp/sage_telegram_bridge.log
echo ""

echo "=========================================="
echo "DEPLOYMENT COMPLETE"
echo "=========================================="
echo ""
echo "V2 Features:"
echo "  ✓ JSONL injection (bypasses stdin blocking)"
echo "  ✓ Works when Claude waiting for input"
echo "  ✓ Auto-session detection"
echo "  ✓ Fallback to tmux if JSONL fails"
echo ""
echo "Config: config/telegram_config.json"
echo "  injection_method: jsonl"
echo ""
echo "Logs: /tmp/sage_telegram_bridge.log"
echo ""
echo "Test with: Send Telegram message to Greg's bot"
echo "=========================================="
