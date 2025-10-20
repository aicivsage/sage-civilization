#!/bin/bash
# Test script for Telegram file sending capability
# Run this to verify send_telegram_file.py works correctly

set -e  # Exit on error

PROJECT_ROOT="/home/corey/projects/AI-CIV/grow_gemini_deepresearch"
SCRIPT="$PROJECT_ROOT/tools/send_telegram_file.py"
TEST_FILE="$PROJECT_ROOT/HANDOFF-TG-ARCHI-REBOOT-TEST-20251017.md"

echo "=========================================="
echo "Telegram File Sending Test Suite"
echo "=========================================="
echo ""

# Test 1: Basic file send
echo "Test 1: Send handoff document to Corey"
echo "File: $TEST_FILE"
echo "Caption: Testing file attachment capability - TG-Archi learning complete!"
echo ""

if [ ! -f "$TEST_FILE" ]; then
    echo "ERROR: Test file not found: $TEST_FILE"
    exit 1
fi

python3 "$SCRIPT" \
    "$TEST_FILE" \
    "Testing file attachment capability - TG-Archi learning complete!" \
    437939400

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ TEST 1 PASSED: File sent successfully"
    echo ""
else
    echo ""
    echo "❌ TEST 1 FAILED: File sending failed"
    echo ""
    exit 1
fi

# Test 2: File not found
echo "=========================================="
echo "Test 2: File not found error handling"
echo ""

python3 "$SCRIPT" "nonexistent_file.txt" 2>&1 | grep -q "ERROR: File not found"

if [ $? -eq 0 ]; then
    echo "✅ TEST 2 PASSED: File not found error handled correctly"
    echo ""
else
    echo "❌ TEST 2 FAILED: File not found error not detected"
    echo ""
    exit 1
fi

# Test 3: Check script is executable
echo "=========================================="
echo "Test 3: Script executable check"
echo ""

if [ -x "$SCRIPT" ]; then
    echo "✅ TEST 3 PASSED: Script is executable"
else
    echo "⚠️  TEST 3 WARNING: Script not executable (still works via python3)"
    echo "   Suggestion: chmod +x $SCRIPT"
fi
echo ""

# Summary
echo "=========================================="
echo "Test Suite Complete!"
echo "=========================================="
echo ""
echo "Results:"
echo "  Test 1 (File send): PASSED"
echo "  Test 2 (Error handling): PASSED"
echo "  Test 3 (Executable): PASSED/WARNING"
echo ""
echo "Next steps:"
echo "  1. Check Corey's Telegram for received file"
echo "  2. Verify caption is properly formatted"
echo "  3. Confirm file is downloadable/readable"
echo ""
echo "If all looks good, update capability status to: PRODUCTION READY ✅"
echo ""
