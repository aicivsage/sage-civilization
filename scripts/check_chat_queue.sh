#!/bin/bash
# Helper script for Primary AI to check chat queue

QUEUE_DIR="memories/communication/chat/queue"
PENDING_DIR="$QUEUE_DIR/pending"
RESPONSES_DIR="$QUEUE_DIR/responses"

echo "🔍 Checking chat queue..."
echo ""

# Count pending messages
PENDING_COUNT=$(find "$PENDING_DIR" -name "*.json" 2>/dev/null | wc -l)

if [ $PENDING_COUNT -eq 0 ]; then
    echo "✅ No pending messages"
    exit 0
fi

echo "📬 $PENDING_COUNT pending message(s)"
echo ""

# Show each pending message
for file in "$PENDING_DIR"/*.json; do
    if [ -f "$file" ]; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "File: $(basename "$file")"
        echo ""

        # Extract and display the message
        python3 -c "
import json
import sys
try:
    with open('$file', 'r') as f:
        data = json.load(f)
    print(f\"From: {data['message']['username']}\")
    print(f\"Time: {data['message']['timestamp']}\")
    print(f\"Message: {data['message']['message']}\")
    print('')
    print('Recent context:')
    for msg in data['context'][-3:]:
        sender = msg['username'] if msg['type'] == 'user' else '🤖 Sage'
        text = msg['message'][:80] + '...' if len(msg['message']) > 80 else msg['message']
        print(f\"  {sender}: {text}\")
except Exception as e:
    print(f'Error reading file: {e}', file=sys.stderr)
"
        echo ""
    fi
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "To respond: Read the pending file, then create a response:"
echo "  response_file=\"$RESPONSES_DIR/resp_[msg_id].json\""
echo '  echo "{\"room_id\": \"...\", \"response_text\": \"...\"}" > "$response_file"'
