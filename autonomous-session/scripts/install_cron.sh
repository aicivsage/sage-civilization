#!/bin/bash
# Install cron job for autonomous session injection - Sage Edition
# Adapted for Sage environment from A-C-Gee template

SCRIPT_DIR="/mnt/c/sage/sage-civilization/autonomous-session/scripts"
INJECT_SCRIPT="$SCRIPT_DIR/inject_prompt.sh"

# Make inject script executable
chmod +x "$INJECT_SCRIPT"

# Cron schedule options (uncomment ONE to use)

# Option 1: Every 30 minutes (DEFAULT)
CRON_SCHEDULE="*/30 * * * *"

# Option 2: Every hour
# CRON_SCHEDULE="0 * * * *"

# Option 3: Every 2 hours
# CRON_SCHEDULE="0 */2 * * *"

# Option 4: Every 45 minutes
# CRON_SCHEDULE="*/45 * * * *"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "inject_prompt.sh"; then
    echo "⚠️  Cron job already exists. Remove it first with: crontab -e"
    echo "Then run this script again."
    exit 1
fi

# Add cron job for Sage
(crontab -l 2>/dev/null; echo "$CRON_SCHEDULE $INJECT_SCRIPT >> $SCRIPT_DIR/cron_output.log 2>&1") | crontab -

echo "✅ Cron job installed successfully!"
echo ""
echo "Schedule: $CRON_SCHEDULE (every 30 minutes)"
echo "Script: $INJECT_SCRIPT"
echo "Logs: $SCRIPT_DIR/injection_log.txt"
echo "Cron output: $SCRIPT_DIR/cron_output.log"
echo ""
echo "To view cron jobs: crontab -l"
echo "To remove: crontab -e (then delete the line)"
echo ""
echo "⚠️  IMPORTANT: Make sure tmux session 'sage-session' is running!"
echo "It should be: tmux new-session -s sage-session 'claude'"
echo ""
echo "To pause BOOP temporarily without removing cron:"
echo "  touch $SCRIPT_DIR/PAUSE"
echo "To resume:"
echo "  rm $SCRIPT_DIR/PAUSE"
