#!/bin/bash
# Telegram Message Templates for Wake-Up Protocol
# Quick access to standard messages Primary sends during sessions

CHAT_ID="437939400"  # Corey
SEND_CMD="python3 tools/send_telegram_plain.py"
TMUX_SESSION="3"  # A-C-Gee session

# Function to send message (direct send)
send_tg() {
    $SEND_CMD $CHAT_ID "$1"
}

# Function to send wrapped message (auto-forwarded by monitor)
# Uses echo to avoid capturing CLI formatting from conversation output
send_tg_wrapped() {
    local MESSAGE="$1"
    local TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Echo directly to avoid Claude Code UI formatting
    # Monitor will detect and forward to Telegram automatically
    echo "🤖🎯📱[TIMESTAMP:$TIMESTAMP]"
    echo "$MESSAGE"
    echo "✨🔚"
}

# Template functions
tg_session_start() {
    send_tg "🤖🎯📱
Primary AI online - loading context from handoff, checking inbox, will report status in 5 min
✨🔚"
}

tg_context_loaded() {
    local HANDOFF="$1"
    local PRIORITY="$2"
    send_tg "🤖🎯📱
Context loaded

Handoff: $HANDOFF
Next priority: $PRIORITY

Ready for session!
✨🔚"
}

tg_progress_update() {
    local COMPLETED="$1"
    local IN_PROGRESS="$2"
    local NEXT="$3"
    send_tg "🤖🎯📱
Progress update

Completed: $COMPLETED
In progress: $IN_PROGRESS
Next: $NEXT
✨🔚"
}

tg_blocker() {
    local ISSUE="$1"
    send_tg "🤖🎯📱
Blocker identified: $ISSUE

Pausing work, awaiting input
✨🔚"
}

tg_session_complete() {
    local DURATION="$1"
    local ACHIEVEMENTS="$2"
    send_tg "🤖🎯📱
Session complete

Duration: $DURATION
Achievements: $ACHIEVEMENTS

Handoff document written, ready for next session
✨🔚"
}

tg_micro_session() {
    local SUMMARY="$1"
    send_tg "🤖🎯📱
Micro-session complete: $SUMMARY
✨🔚"
}

# Export functions for use in other scripts
export -f send_tg
export -f send_tg_wrapped
export -f tg_session_start
export -f tg_context_loaded
export -f tg_progress_update
export -f tg_blocker
export -f tg_session_complete
export -f tg_micro_session

# If called directly with argument, execute that function
if [ $# -gt 0 ]; then
    "$@"
fi
