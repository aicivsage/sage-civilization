#!/bin/bash
# Manual BOOP Injection Test Script for Sage
# Tests single prompt injection without affecting state
# Safe for testing - doesn't update injection_state.txt

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMUX_SESSION="sage-session"
TMUX_PANE="sage-session:0.0"
PROMPTS_DIR="/mnt/c/sage/sage-civilization/autonomous-session/prompts"
STATE_FILE="$SCRIPT_DIR/injection_state.txt"
TEST_LOG_FILE="$SCRIPT_DIR/test_injection_log.txt"

echo "=== BOOP Injection Test for Sage ==="
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Verify prompts directory exists
if [ ! -d "$PROMPTS_DIR" ]; then
    echo "ERROR: Prompts directory not found: $PROMPTS_DIR"
    exit 1
fi

# Get list of available prompts
PROMPT_FILES=($(ls -1 "$PROMPTS_DIR"/*.txt 2>/dev/null | sort))
TOTAL_PROMPTS=${#PROMPT_FILES[@]}

if [ $TOTAL_PROMPTS -eq 0 ]; then
    echo "ERROR: No prompt files found in $PROMPTS_DIR"
    exit 1
fi

echo "Found $TOTAL_PROMPTS prompts:"
for i in "${!PROMPT_FILES[@]}"; do
    name=$(basename "${PROMPT_FILES[$i]}" .txt)
    printf "  %2d. %s\n" $((i+1)) "$name"
done
echo ""

# Check current state
if [ -f "$STATE_FILE" ]; then
    CURRENT=$(cat "$STATE_FILE")
    echo "Current injection state: $CURRENT"
else
    echo "State file not found. Will initialize to 1."
    CURRENT=1
fi

PROMPT_INDEX=$((($CURRENT - 1) % $TOTAL_PROMPTS))
PROMPT_FILE="${PROMPT_FILES[$PROMPT_INDEX]}"
PROMPT_NAME=$(basename "$PROMPT_FILE" .txt)

echo ""
echo "Prompt to inject: #$CURRENT -> $PROMPT_NAME"
echo "Preview:"
echo "---"
head -3 "$PROMPT_FILE"
echo "---"
echo ""

# Check if tmux session exists
if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    echo "ERROR: tmux session '$TMUX_SESSION' not found!"
    echo "Start it with: tmux new-session -s sage-session 'claude'"
    exit 1
fi

echo "tmux session check: PASS"
echo ""

# Verify tmux pane
if ! tmux send-keys -t "$TMUX_PANE" "" 2>/dev/null; then
    echo "ERROR: Cannot access tmux pane $TMUX_PANE"
    exit 1
fi

echo "tmux pane check: PASS"
echo ""

# Show current tmux output (context)
echo "Current tmux pane output (last 5 lines):"
echo "---"
tmux capture-pane -t "$TMUX_PANE" -p 2>/dev/null | tail -5
echo "---"
echo ""

# Check for rate limit
RECENT_OUTPUT=$(tmux capture-pane -t "$TMUX_PANE" -p 2>/dev/null | tail -5)
if echo "$RECENT_OUTPUT" | grep -qi "rate limit"; then
    echo "⚠️  WARNING: Rate limit detected in recent output!"
    echo "Test will SKIP injection (safety mechanism active)"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] TEST: Rate limit detected, skipping injection" >> "$TEST_LOG_FILE"
    exit 0
fi

# Read the prompt
PROMPT_TEXT=$(cat "$PROMPT_FILE")

# Confirm with user
echo "Ready to inject? (Press ENTER to continue, Ctrl+C to abort)"
read -r

echo ""
echo "Injecting prompt..."
echo ""

# Inject the prompt
if ! tmux send-keys -t "$TMUX_PANE" -l "$PROMPT_TEXT" 2>/dev/null; then
    echo "ERROR: Failed to send prompt text"
    exit 1
fi

if ! tmux send-keys -t "$TMUX_PANE" Enter 2>/dev/null; then
    echo "ERROR: Failed to press Enter"
    exit 1
fi

# Log the test
echo "[$(date '+%Y-%m-%d %H:%M:%S')] TEST: Injected $PROMPT_NAME (prompt #$CURRENT)" >> "$TEST_LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] TEST: State NOT incremented (test mode)" >> "$TEST_LOG_FILE"

echo "✅ Test injection successful!"
echo ""
echo "Prompt has been sent to tmux session: $TMUX_SESSION"
echo "Pane: $TMUX_PANE"
echo "Prompt: $PROMPT_NAME"
echo ""
echo "NOTE: Injection state was NOT incremented (test mode)"
echo "Running production inject_prompt.sh will use current state: $CURRENT"
echo ""
echo "To view the injected prompt in the tmux session:"
echo "  tmux attach -t $TMUX_SESSION"
echo "  (Press Ctrl+B then D to detach)"
echo ""
echo "Test log: $TEST_LOG_FILE"
