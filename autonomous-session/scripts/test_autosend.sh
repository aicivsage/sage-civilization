#!/bin/bash
# Test script for hourly_email_autosend.sh
# Verifies script can run without errors

echo "========================================"
echo "Testing Email Auto-Send Script"
echo "========================================"

SCRIPT_PATH="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts/hourly_email_autosend.sh"

# Check script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ ERROR: Script not found at $SCRIPT_PATH"
    exit 1
fi

# Check script is executable
if [ ! -x "$SCRIPT_PATH" ]; then
    echo "⚠️  WARNING: Script not executable, making executable..."
    chmod +x "$SCRIPT_PATH"
fi

# Check tmux session exists
if ! tmux has-session -t claude 2>/dev/null; then
    echo "❌ ERROR: tmux session 'claude' not found"
    echo "Start Claude Code first: tmux new-session -s claude 'claude'"
    exit 1
fi

echo "✅ Script exists and is executable"
echo "✅ tmux session 'claude' is active"
echo ""

# Dry run - show what would be injected
echo "Dry run - showing task that would be injected:"
echo "--------------------------------------"
cat << 'EOF'
Task(human-liaison):

**AUTONOMOUS MODE - AUTO-SEND ENABLED**
Constitutional authority: CLAUDE.md Article IV (blanket email approval)

Your task:

1. Check inbox for new messages (HIGH/MEDIUM priority: Corey, Greg, Chris, Weaver)
2. For each priority email:
   - Draft HTML response (templates/email_template.html)
   - SEND IMMEDIATELY via tools/send_html_email.py (NO approval needed)
   - Log to memories/agents/email-reporter/sent_emails.json

3. Duplicate prevention:
   - Check sent_emails.json before sending
   - Skip same thread within 24h

4. Return JSON summary:
{
  "emails_checked": N,
  "priority_emails_found": N,
  "emails_sent": N,
  "send_log": ["recipient: subject", ...]
}

Success criteria: All priority emails responded within 1 hour, zero drafts lingering unsent.
EOF
echo "--------------------------------------"
echo ""

echo "Ready to test?"
echo "Options:"
echo "  1) Run script for REAL (will inject task into Claude session)"
echo "  2) Exit (don't run)"
echo ""
read -p "Choose (1 or 2): " choice

if [ "$choice" == "1" ]; then
    echo ""
    echo "Running script..."
    echo "Watch your tmux session for task execution!"
    echo ""

    # Run the actual script
    "$SCRIPT_PATH"

    EXIT_CODE=$?

    echo ""
    echo "========================================"
    if [ $EXIT_CODE -eq 0 ]; then
        echo "✅ Script executed successfully"
        echo ""
        echo "Next steps:"
        echo "1. Check your tmux session (tmux attach -t claude)"
        echo "2. Watch human-liaison execute the task"
        echo "3. Check logs: tail -f autonomous-session/scripts/hourly_email_check_log.txt"
        echo "4. Verify sends: cat memories/agents/email-reporter/sent_emails.json | jq '.[-3:]'"
    else
        echo "❌ Script failed with exit code: $EXIT_CODE"
        echo "Check logs: tail -20 autonomous-session/scripts/hourly_email_check_log.txt"
    fi
    echo "========================================"
else
    echo "Cancelled - no changes made"
    exit 0
fi
