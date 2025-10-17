#!/bin/bash
# Email Detection Script - Checks for NEW emails since last check
# Returns 0 if new emails found, 1 if no new emails

# Configuration
STATE_FILE="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts/email_check_state.txt"
PYTHON_CHECKER="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/check_inbox_direct.py"
LOG_FILE="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts/email_check_log.txt"

# Initialize state file if it doesn't exist (timestamp of last check)
if [ ! -f "$STATE_FILE" ]; then
    echo "0" > "$STATE_FILE"
fi

# Get last check timestamp
LAST_CHECK=$(cat "$STATE_FILE")
CURRENT_TIME=$(date +%s)

# Check inbox using Python script (gets count of unread emails)
# The script outputs: "Unread messages: X"
EMAIL_OUTPUT=$(python3 "$PYTHON_CHECKER" 2>&1)
EMAIL_COUNT=$(echo "$EMAIL_OUTPUT" | grep -oP 'Unread messages: \K\d+' | head -1)

# If we can't parse count, assume 0
if [ -z "$EMAIL_COUNT" ]; then
    EMAIL_COUNT=0
fi

# Get previous email count
PREV_STATE_FILE="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts/email_count_state.txt"
if [ ! -f "$PREV_STATE_FILE" ]; then
    echo "0" > "$PREV_STATE_FILE"
fi
PREV_COUNT=$(cat "$PREV_STATE_FILE")

# Log the check
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checked: $EMAIL_COUNT emails (prev: $PREV_COUNT)" >> "$LOG_FILE"

# Update state files
echo "$CURRENT_TIME" > "$STATE_FILE"
echo "$EMAIL_COUNT" > "$PREV_STATE_FILE"

# If count increased, we have NEW emails
if [ "$EMAIL_COUNT" -gt "$PREV_COUNT" ]; then
    NEW_COUNT=$((EMAIL_COUNT - PREV_COUNT))
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🔔 NEW EMAILS DETECTED: +$NEW_COUNT" >> "$LOG_FILE"
    echo "NEW_EMAILS:$NEW_COUNT"
    exit 0
else
    echo "NO_NEW_EMAILS"
    exit 1
fi
