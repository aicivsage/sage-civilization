#!/bin/bash
# Manual monitoring check - Run when you want to check for new work
# Does NOT inject prompts, just reports status

SCRIPT_DIR="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts"

echo "=== A-C-Gee Monitoring Check ==="
echo ""

# Check emails
echo "📧 Checking emails..."
EMAIL_STATUS=$(bash "$SCRIPT_DIR/check_email_new.sh" 2>&1)
if echo "$EMAIL_STATUS" | grep -q "NEW_EMAILS"; then
    NEW_COUNT=$(echo "$EMAIL_STATUS" | grep -oP 'NEW_EMAILS:\K\d+')
    echo "   ✨ NEW EMAILS DETECTED: $NEW_COUNT"
else
    echo "   ✓ No new emails"
fi

echo ""

# Check comms hub
echo "🌐 Checking comms hub..."
COMMSHUB_STATUS=$(bash "$SCRIPT_DIR/check_commshub_new.sh" 2>&1)
if echo "$COMMSHUB_STATUS" | grep -q "NEW_MESSAGES"; then
    NEW_COUNT=$(echo "$COMMSHUB_STATUS" | grep -oP 'NEW_MESSAGES:\K\d+')
    echo "   ✨ NEW MESSAGES DETECTED: $NEW_COUNT"
else
    echo "   ✓ No new messages"
fi

echo ""
echo "=== Check complete ==="
