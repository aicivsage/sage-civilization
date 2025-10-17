#!/bin/bash
# Autonomous Session Prompt Injector
# Sends rotating prompts to persistent Claude Code tmux session

# Configuration
TMUX_SESSION="claude"
TMUX_PANE="claude.0"
PROMPTS_DIR="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/prompts"
STATE_FILE="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts/injection_state.txt"
LOG_FILE="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts/injection_log.txt"

# Initialize state file if it doesn't exist
if [ ! -f "$STATE_FILE" ]; then
    echo "1" > "$STATE_FILE"
fi

# Read current prompt number
CURRENT=$(cat "$STATE_FILE")

# Get list of all prompts (sorted)
PROMPT_FILES=($(ls -1 "$PROMPTS_DIR"/*.txt | sort))
TOTAL_PROMPTS=${#PROMPT_FILES[@]}

# Calculate which prompt to use (cycles through all)
PROMPT_INDEX=$((($CURRENT - 1) % $TOTAL_PROMPTS))
PROMPT_FILE="${PROMPT_FILES[$PROMPT_INDEX]}"
PROMPT_NAME=$(basename "$PROMPT_FILE" .txt)

# Read the prompt content
PROMPT_TEXT=$(cat "$PROMPT_FILE")

# Check if tmux session exists
if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: tmux session '$TMUX_SESSION' not found" >> "$LOG_FILE"
    echo "ERROR: tmux session '$TMUX_SESSION' not found. Start it with: tmux new-session -s claude 'claude'"
    exit 1
fi

# Check for rate limit banner (basic check - looks for "rate limit" in recent output)
RECENT_OUTPUT=$(tmux capture-pane -t "$TMUX_PANE" -p | tail -5)
if echo "$RECENT_OUTPUT" | grep -qi "rate limit"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SKIPPED: Rate limit detected, waiting..." >> "$LOG_FILE"
    exit 0
fi

# Inject the prompt (using -l for literal text)
tmux send-keys -t "$TMUX_PANE" -l "$PROMPT_TEXT"
tmux send-keys -t "$TMUX_PANE" Enter

# Log the injection
echo "[$(date '+%Y-%m-%d %H:%M:%S')] INJECTED: $PROMPT_NAME (#$CURRENT)" >> "$LOG_FILE"

# Update state for next run (increment counter)
NEXT_COUNT=$((CURRENT + 1))
echo "$NEXT_COUNT" > "$STATE_FILE"

# Output for manual testing
echo "✅ Injected prompt #$CURRENT: $PROMPT_NAME"
NEXT_INDEX=$(( ($NEXT_COUNT - 1) % $TOTAL_PROMPTS ))
echo "Next injection will be #$NEXT_COUNT: $(basename "${PROMPT_FILES[$NEXT_INDEX]}" .txt)"
