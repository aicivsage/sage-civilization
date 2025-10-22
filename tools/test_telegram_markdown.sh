#!/bin/bash
# Test Telegram Markdown formatting implementation
# Date: 2025-10-20
# Agent: tg-archi

set -e  # Exit on error

PROJECT_ROOT="/home/corey/projects/AI-CIV/grow_gemini_deepresearch"
USER_ID="437939400"

echo "========================================="
echo "Telegram Markdown Formatting Test Suite"
echo "========================================="
echo ""

# Test 1: Plain text (backward compatibility)
echo "Test 1: Plain text (no --markdown flag)"
echo "----------------------------------------"
python3 "$PROJECT_ROOT/tools/send_telegram_plain.py" "$USER_ID" "Test 1: Plain text message (no formatting)"
echo "✓ Plain text test sent"
echo ""
sleep 2

# Test 2: Bold text
echo "Test 2: Bold text"
echo "----------------"
python3 "$PROJECT_ROOT/tools/send_telegram_plain.py" "$USER_ID" "Test 2: *Bold text* should be bold" --markdown
echo "✓ Bold test sent"
echo ""
sleep 2

# Test 3: Italic text
echo "Test 3: Italic text"
echo "------------------"
python3 "$PROJECT_ROOT/tools/send_telegram_plain.py" "$USER_ID" "Test 3: _Italic text_ should be italic" --markdown
echo "✓ Italic test sent"
echo ""
sleep 2

# Test 4: Inline code
echo "Test 4: Inline code"
echo "------------------"
python3 "$PROJECT_ROOT/tools/send_telegram_plain.py" "$USER_ID" "Test 4: \`inline code\` should be monospace" --markdown
echo "✓ Inline code test sent"
echo ""
sleep 2

# Test 5: Link
echo "Test 5: Link"
echo "-----------"
python3 "$PROJECT_ROOT/tools/send_telegram_plain.py" "$USER_ID" "Test 5: [Click here](https://example.com) for link" --markdown
echo "✓ Link test sent"
echo ""
sleep 2

# Test 6: Combined formatting
echo "Test 6: Combined formatting"
echo "--------------------------"
python3 "$PROJECT_ROOT/tools/send_telegram_plain.py" "$USER_ID" "Test 6: *Bold*, _italic_, and \`code\` all together" --markdown
echo "✓ Combined formatting test sent"
echo ""
sleep 2

# Test 7: Realistic wrapped message format
echo "Test 7: Realistic wrapped message"
echo "---------------------------------"
MSG=$(cat <<'EOF'
Telegram Markdown Test

*Status:* Testing complete
_Agent:_ tg-archi
\`Feature:\` Markdown formatting

*Next steps:*
- Verify display on phone
- Check all formats
- Deploy to production

[Documentation](https://core.telegram.org/bots/api#markdown-style)
EOF
)

python3 "$PROJECT_ROOT/tools/send_telegram_plain.py" "$USER_ID" "$MSG" --markdown
echo "✓ Realistic message test sent"
echo ""
sleep 2

# Test 8: Fallback behavior (special chars that might fail)
echo "Test 8: Fallback behavior"
echo "------------------------"
python3 "$PROJECT_ROOT/tools/send_telegram_plain.py" "$USER_ID" "Test 8: Price $5_00 with_unmatched_underscores" --markdown
echo "✓ Fallback test sent (may show warning in logs)"
echo ""

echo "========================================="
echo "All tests completed!"
echo "========================================="
echo ""
echo "Check your Telegram for results:"
echo "1. Test 1: Plain text (no formatting)"
echo "2. Test 2: Bold text should be bold"
echo "3. Test 3: Italic text should be italic"
echo "4. Test 4: Inline code should be monospace"
echo "5. Test 5: Link should be clickable"
echo "6. Test 6: Multiple formats together"
echo "7. Test 7: Realistic wrapped message"
echo "8. Test 8: Fallback (may be plain text)"
echo ""
echo "Check logs for any warnings:"
echo "  tail -20 /tmp/telegram_jsonl_monitor.log"
