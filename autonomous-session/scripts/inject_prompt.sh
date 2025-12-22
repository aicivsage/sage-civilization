#!/bin/bash
# Autonomous Session Prompt Injector for Sage
# Sends rotating prompts to persistent Claude Code tmux session
# Adapted for Sage environment from A-C-Gee template

# Configuration - ADAPTED FOR SAGE
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMUX_SESSION="sage-session"
TMUX_PANE="sage-session:0.0"
PROMPTS_DIR="/mnt/c/sage/sage-civilization/autonomous-session/prompts"
STATE_FILE="$SCRIPT_DIR/injection_state.txt"
LOG_FILE="$SCRIPT_DIR/injection_log.txt"
PAUSE_FILE="$SCRIPT_DIR/PAUSE"

# Initialize state file if it doesn't exist
if [ ! -f "$STATE_FILE" ]; then
    echo "1" > "$STATE_FILE"
fi

# Check for PAUSE flag (safety mechanism)
if [ -f "$PAUSE_FILE" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] PAUSED: Remove $PAUSE_FILE to resume" >> "$LOG_FILE"
    exit 0
fi

# Read current prompt number
CURRENT=$(cat "$STATE_FILE")

# Get list of all prompts (sorted)
PROMPT_FILES=($(ls -1 "$PROMPTS_DIR"/*.txt 2>/dev/null | sort))
TOTAL_PROMPTS=${#PROMPT_FILES[@]}

# Handle case where no prompts found
if [ $TOTAL_PROMPTS -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: No prompt files found in $PROMPTS_DIR" >> "$LOG_FILE"
    echo "ERROR: No prompt files found in $PROMPTS_DIR"
    exit 1
fi

# Calculate which prompt to use (cycles through all)
PROMPT_INDEX=$((($CURRENT - 1) % $TOTAL_PROMPTS))
PROMPT_FILE="${PROMPT_FILES[$PROMPT_INDEX]}"
PROMPT_NAME=$(basename "$PROMPT_FILE" .txt)

# Read the prompt content
PROMPT_TEXT=$(cat "$PROMPT_FILE")

# Check if tmux session exists
if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: tmux session '$TMUX_SESSION' not found" >> "$LOG_FILE"
    echo "ERROR: tmux session '$TMUX_SESSION' not found. Start it with: tmux new-session -s sage-session 'claude'"
    exit 1
fi

# Check for rate limit banner (basic check - looks for "rate limit" in recent output)
RECENT_OUTPUT=$(tmux capture-pane -t "$TMUX_PANE" -p 2>/dev/null | tail -5)
if echo "$RECENT_OUTPUT" | grep -qi "rate limit"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SKIPPED: Rate limit detected, waiting..." >> "$LOG_FILE"
    exit 0
fi

# Inject the prompt (using -l for literal text)
if ! tmux send-keys -t "$TMUX_PANE" -l "$PROMPT_TEXT" 2>/dev/null; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Failed to send keys to tmux" >> "$LOG_FILE"
    exit 1
fi

if ! tmux send-keys -t "$TMUX_PANE" Enter 2>/dev/null; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Failed to press Enter" >> "$LOG_FILE"
    exit 1
fi

# Log the injection with full details
echo "[$(date '+%Y-%m-%d %H:%M:%S')] INJECTED: $PROMPT_NAME (prompt #$CURRENT of $TOTAL_PROMPTS)" >> "$LOG_FILE"

# Update state for next run (increment counter)
NEXT_COUNT=$((CURRENT + 1))
echo "$NEXT_COUNT" > "$STATE_FILE"

# Output for manual testing
echo "✅ Injected prompt #$CURRENT: $PROMPT_NAME"
NEXT_INDEX=$(( ($NEXT_COUNT - 1) % $TOTAL_PROMPTS ))
NEXT_NAME=$(basename "${PROMPT_FILES[$NEXT_INDEX]}" .txt)
echo "   Next injection will be #$NEXT_COUNT: $NEXT_NAME"
echo "   Session: $TMUX_SESSION"
