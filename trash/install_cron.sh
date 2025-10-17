#!/usr/bin/env bash
#
# Install Autonomous Cycle Cron Job
#

set -euo pipefail

SCRIPT_PATH="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/run_autonomous_cycle.sh"
CRON_LINE="*/30 * * * * $SCRIPT_PATH >> /home/corey/projects/AI-CIV/grow_gemini_deepresearch/logs/cron.log 2>&1"

echo "=========================================="
echo "🤖 Installing Autonomous Cycle Cron Job"
echo "=========================================="
echo ""

# Check if script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ ERROR: Script not found at $SCRIPT_PATH"
    exit 1
fi

# Check if already installed
if crontab -l 2>/dev/null | grep -q "run_autonomous_cycle.sh"; then
    echo "⚠️  Cron job already installed!"
    echo ""
    echo "Current crontab:"
    crontab -l | grep "run_autonomous_cycle.sh"
    echo ""
    read -p "Remove and reinstall? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing old cron job..."
        crontab -l | grep -v "run_autonomous_cycle.sh" | crontab -
    else
        echo "❌ Installation cancelled"
        exit 0
    fi
fi

# Install cron job
echo "📝 Adding cron job..."
(crontab -l 2>/dev/null || true; echo "$CRON_LINE") | crontab -

echo "✅ Cron job installed successfully!"
echo ""
echo "📋 Cron schedule:"
echo "   - Runs: Every 30 minutes"
echo "   - Script: $SCRIPT_PATH"
echo "   - Logs: /home/corey/projects/AI-CIV/grow_gemini_deepresearch/logs/"
echo ""
echo "🔍 Verify installation:"
echo "   crontab -l | grep autonomous"
echo ""
echo "📊 View logs:"
echo "   tail -f /home/corey/projects/AI-CIV/grow_gemini_deepresearch/logs/latest_cycle.log"
echo ""
echo "⏸️  To disable:"
echo "   crontab -e"
echo "   (comment out or delete the line)"
echo ""
echo "=========================================="
echo "✅ INSTALLATION COMPLETE"
echo "=========================================="
echo ""
echo "⏰ Next run: $(date -d '+30 minutes' '+%Y-%m-%d %H:%M')"
echo ""
