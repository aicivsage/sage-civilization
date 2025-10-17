#!/bin/bash
# Smart Injection Coordinator - Only wakes Primary when NEW work detected
# Checks email and comms hub first, falls back to rotating prompts if nothing new

# Configuration
SCRIPT_DIR="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts"
PROMPTS_DIR="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/prompts"
TMUX_SESSION="claude"
TMUX_PANE="claude.0"
LOG_FILE="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts/smart_inject_log.txt"

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
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] INJECTED: $PROMPT_NAME ($REASON)" >> "$LOG_FILE"
    echo "✅ Injected: $PROMPT_NAME ($REASON)"
    return 0
}

# Priority 1: Check for new emails
if bash "$SCRIPT_DIR/check_email_new.sh" | grep -q "NEW_EMAILS"; then
    inject_prompt "$PROMPTS_DIR/11-email-alert.txt" "NEW_EMAIL_DETECTED"
    exit 0
fi

# Priority 2: Check for new comms hub messages
if bash "$SCRIPT_DIR/check_commshub_new.sh" | grep -q "NEW_MESSAGES"; then
    inject_prompt "$PROMPTS_DIR/12-commshub-alert.txt" "NEW_COMMSHUB_MESSAGE"
    exit 0
fi

# Priority 3: No new work, use rotating prompt system
echo "[$(date '+%Y-%m-%d %H:%M:%S')] No new work detected, using rotating prompt" >> "$LOG_FILE"
bash "$SCRIPT_DIR/inject_prompt.sh"
exit 0
