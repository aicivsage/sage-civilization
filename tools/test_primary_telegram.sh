#!/bin/bash
# Test script for Primary AI to verify Telegram capability
# Run this to confirm send_telegram_plain.py works correctly

set -e  # Exit on error

PROJECT_ROOT="/home/corey/projects/AI-CIV/grow_gemini_deepresearch"
SCRIPT="$PROJECT_ROOT/tools/send_telegram_plain.py"
USER_ID="437939400"  # Corey's Telegram ID

echo "=========================================="
echo "Primary AI - Telegram Capability Test"
echo "=========================================="
echo ""
echo "Testing: send_telegram_plain.py"
echo "Target: Corey (user_id: $USER_ID)"
echo ""

# Check script exists
if [ ! -f "$SCRIPT" ]; then
    echo "❌ ERROR: Script not found: $SCRIPT"
    exit 1
fi

# Check config exists
CONFIG_FILE="$PROJECT_ROOT/config/telegram_config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ ERROR: Config not found: $CONFIG_FILE"
    exit 1
fi

echo "✅ Script found: $SCRIPT"
echo "✅ Config found: $CONFIG_FILE"
echo ""

# Test 1: Simple message
echo "=========================================="
echo "Test 1: Simple Status Message"
echo "=========================================="
echo ""
echo "Sending: 'Primary AI learning complete - Telegram capability verified'"
echo ""

python3 "$SCRIPT" "$USER_ID" "Primary AI learning complete - Telegram capability verified - wake-up protocol now includes mobile notification"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ TEST 1 PASSED: Message sent successfully"
    echo ""
else
    echo ""
    echo "❌ TEST 1 FAILED: Message sending failed"
    echo ""
    exit 1
fi

# Test 2: Multi-line message
echo "=========================================="
echo "Test 2: Multi-line Status Update"
echo "=========================================="
echo ""

python3 "$SCRIPT" "$USER_ID" "Session Status Test:

Capabilities verified:
- Plain text messaging working
- Multi-line formatting working
- Special characters safe

Status: All systems operational"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ TEST 2 PASSED: Multi-line message sent successfully"
    echo ""
else
    echo ""
    echo "❌ TEST 2 FAILED: Multi-line message failed"
    echo ""
    exit 1
fi

# Test 3: Message with special characters
echo "=========================================="
echo "Test 3: Special Characters Test"
echo "=========================================="
echo ""
echo "Testing: underscores, asterisks, brackets"
echo ""

python3 "$SCRIPT" "$USER_ID" "Special characters test: task_name with *asterisks* and [brackets] - all should work"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ TEST 3 PASSED: Special characters handled correctly"
    echo ""
else
    echo ""
    echo "❌ TEST 3 FAILED: Special characters failed"
    echo ""
    exit 1
fi

# Summary
echo "=========================================="
echo "Test Suite Complete!"
echo "=========================================="
echo ""
echo "Results:"
echo "  ✅ Test 1: Simple message"
echo "  ✅ Test 2: Multi-line message"
echo "  ✅ Test 3: Special characters"
echo ""
echo "Next steps:"
echo "  1. Check Corey's Telegram for 3 test messages"
echo "  2. Verify all messages are readable"
echo "  3. Add Telegram ping to wake-up protocol"
echo "  4. Update session automation scripts"
echo ""
echo "Wake-up protocol command:"
echo "  python3 tools/send_telegram_plain.py 437939400 \"Primary AI online - session started\""
echo ""
echo "Session end command:"
echo "  python3 tools/send_telegram_plain.py 437939400 \"Session complete - handoff document ready\""
echo ""
echo "✅ Primary is now ready for Telegram communication!"
echo ""
