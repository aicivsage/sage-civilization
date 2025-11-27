#!/bin/bash
# Disable old daily email scripts (boring morning/evening emails)
# They're not deleted - just renamed so they won't run accidentally

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Disabling old daily email scripts..."

# Rename the old scripts (add .DISABLED suffix)
if [ -f "$SCRIPT_DIR/send_day_start_email.py" ]; then
    mv "$SCRIPT_DIR/send_day_start_email.py" "$SCRIPT_DIR/send_day_start_email.py.DISABLED"
    echo "✓ Disabled send_day_start_email.py"
fi

if [ -f "$SCRIPT_DIR/send_end_of_day_email.py" ]; then
    mv "$SCRIPT_DIR/send_end_of_day_email.py" "$SCRIPT_DIR/send_end_of_day_email.py.DISABLED"
    echo "✓ Disabled send_end_of_day_email.py"
fi

# Check for any cron jobs that might call these
echo ""
echo "Checking for cron jobs..."
if crontab -l 2>/dev/null | grep -q "send_day_start_email\|send_end_of_day_email"; then
    echo "⚠️  WARNING: Found cron jobs that reference old scripts!"
    echo "   Run: crontab -e"
    echo "   And remove/comment out lines with:"
    echo "   - send_day_start_email.py"
    echo "   - send_end_of_day_email.py"
else
    echo "✓ No cron jobs found for old scripts"
fi

echo ""
echo "Old daily email scripts disabled."
echo "They're preserved with .DISABLED suffix for reference."
echo ""
echo "Next: Use send_session_accomplishment_email.py for exciting session summaries!"
