#!/bin/bash
# Alert-Only Injection - ONLY injects when NEW emails or comms-hub messages detected
# Does NOT inject rotating prompts

# Configuration
SCRIPT_DIR="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts"
PROMPTS_DIR="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/prompts"
TMUX_SESSION="0"
TMUX_PANE="0.0"
LOG_FILE="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts/alert_inject_log.txt"

# Function to inject specific prompt
inject_prompt() {
    local PROMPT_FILE="$1"
    local REASON="$2"

    if [ ! -f "$PROMPT_FILE" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Prompt file not found: $PROMPT_FILE" >> "$LOG_FILE"
        return 1
    fi

    # Check if tmux session exists
    if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: tmux session '$TMUX_SESSION' not found" >> "$LOG_FILE"
        return 1
    fi

    # Check for rate limit
    RECENT_OUTPUT=$(tmux capture-pane -t "$TMUX_PANE" -p | tail -5)
    if echo "$RECENT_OUTPUT" | grep -qi "rate limit"; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] SKIPPED: Rate limit detected" >> "$LOG_FILE"
        return 1
    fi

    # Inject the prompt
    PROMPT_TEXT=$(cat "$PROMPT_FILE")
    tmux send-keys -t "$TMUX_PANE" -l "$PROMPT_TEXT"
    tmux send-keys -t "$TMUX_PANE" Enter

    PROMPT_NAME=$(basename "$PROMPT_FILE" .txt)
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🔔 INJECTED: $PROMPT_NAME ($REASON)" >> "$LOG_FILE"
    return 0
}

# Priority 1: Check for new emails
EMAIL_CHECK=$(bash "$SCRIPT_DIR/check_email_new.sh" 2>&1)
if echo "$EMAIL_CHECK" | grep -q "^NEW_EMAILS"; then
    NEW_COUNT=$(echo "$EMAIL_CHECK" | grep -oP 'NEW_EMAILS:\K\d+')
    inject_prompt "$PROMPTS_DIR/11-email-alert.txt" "NEW_EMAILS:$NEW_COUNT"
    exit 0
fi

# Priority 2: Check for new comms hub messages
COMMSHUB_CHECK=$(bash "$SCRIPT_DIR/check_commshub_new.sh" 2>&1)
if echo "$COMMSHUB_CHECK" | grep -q "^NEW_MESSAGES"; then
    NEW_COUNT=$(echo "$COMMSHUB_CHECK" | grep -oP 'NEW_MESSAGES:\K\d+')
    inject_prompt "$PROMPTS_DIR/12-commshub-alert.txt" "NEW_MESSAGES:$NEW_COUNT"
    exit 0
fi

# No new work - do nothing
echo "[$(date '+%Y-%m-%d %H:%M:%S')] No new work detected, no injection" >> "$LOG_FILE"
exit 0
