#!/bin/bash
# Quick voice reply to Greg
# Usage: ./tools/voice_reply.sh "Your message here"

GREG_ID="7585924762"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VOICE_SCRIPT="$SCRIPT_DIR/send_telegram_voice.py"

if [ $# -eq 0 ]; then
    echo "Usage: ./tools/voice_reply.sh 'Your message'"
    exit 1
fi

MESSAGE="$*"

python3 "$VOICE_SCRIPT" "$GREG_ID" "$MESSAGE"
