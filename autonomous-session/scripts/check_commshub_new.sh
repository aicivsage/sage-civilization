#!/bin/bash
# Comms Hub Detection Script - Checks for NEW Weaver messages since last check
# Returns 0 if new messages found, 1 if no new messages

# Configuration
COMMS_HUB="/home/corey/projects/AI-CIV/ai-civ-comms-hub-team2/rooms/partnerships/messages"
STATE_FILE="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts/commshub_check_state.txt"
LOG_FILE="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts/commshub_check_log.txt"

# Check if comms hub directory exists
if [ ! -d "$COMMS_HUB" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Comms hub not found at $COMMS_HUB" >> "$LOG_FILE"
    echo "ERROR:COMMS_HUB_NOT_FOUND"
    exit 1
fi

# Count message files (both JSON from Weaver and MD from A-C-Gee)
CURRENT_COUNT=$(find "$COMMS_HUB" -type f \( -name "*.json" -o -name "*.md" \) | wc -l)

# Initialize state file if it doesn't exist
if [ ! -f "$STATE_FILE" ]; then
    echo "$CURRENT_COUNT" > "$STATE_FILE"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Initialized: $CURRENT_COUNT messages" >> "$LOG_FILE"
    echo "INITIALIZED:$CURRENT_COUNT"
    exit 1  # First run, not "new" messages
fi

# Get previous count
PREV_COUNT=$(cat "$STATE_FILE")

# Log the check
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checked: $CURRENT_COUNT messages (prev: $PREV_COUNT)" >> "$LOG_FILE"

# Update state
echo "$CURRENT_COUNT" > "$STATE_FILE"

# If count increased, we have NEW messages
if [ "$CURRENT_COUNT" -gt "$PREV_COUNT" ]; then
    NEW_COUNT=$((CURRENT_COUNT - PREV_COUNT))
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🌐 NEW MESSAGES DETECTED: +$NEW_COUNT" >> "$LOG_FILE"
    echo "NEW_MESSAGES:$NEW_COUNT"
    exit 0
else
    echo "NO_NEW_MESSAGES"
    exit 1
fi
