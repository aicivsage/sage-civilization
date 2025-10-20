#!/bin/bash
# Generalized Tmux Prompt Injector for A-C-Gee
# Injects a prompt into Primary AI's tmux session
# Usage: bash tools/inject_prompt_to_acg.sh "Your prompt here"
# Example: bash tools/inject_prompt_to_acg.sh "Check inbox and respond to urgent emails"

PROMPT="$1"

if [ -z "$PROMPT" ]; then
    echo "Usage: $0 \"Your prompt here\""
    echo ""
    echo "Example:"
    echo "  $0 \"Check inbox and respond to urgent emails\""
    exit 1
fi

# Load config to get current tmux session
CONFIG_FILE="config/telegram_config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ ERROR: Config file not found: $CONFIG_FILE"
    exit 1
fi

# Extract tmux pane from config
TMUX_PANE=$(jq -r '.tmux_pane' "$CONFIG_FILE")

if [ -z "$TMUX_PANE" ] || [ "$TMUX_PANE" = "null" ]; then
    echo "❌ ERROR: Could not read tmux_pane from config"
    exit 1
fi

echo "=== ACG Tmux Prompt Injector ==="
echo "Target pane: $TMUX_PANE"
echo "Prompt: $PROMPT"
echo ""

# Format the prompt with [INJECTED] prefix
FORMATTED_PROMPT="[INJECTED] $PROMPT"

# Inject into tmux (two steps: text then Enter, like telegram_bridge.py does)
if ! tmux send-keys -t "$TMUX_PANE" -l "$FORMATTED_PROMPT"; then
    echo "❌ ERROR: Failed to inject prompt. Is tmux session $TMUX_PANE running?"
    exit 1
fi

# Press Enter to submit
if ! tmux send-keys -t "$TMUX_PANE" Enter; then
    echo "❌ ERROR: Failed to press Enter"
    exit 1
fi

echo "✓ Prompt injected successfully!"
echo ""
echo "Check your tmux session to see the prompt."
