#!/bin/bash
# Test Telegram V2 Fix - Input-Waiting State Handling
# Date: 2025-12-29

echo "=========================================="
echo "Telegram V2 Blocking Fix Test"
echo "=========================================="
echo ""

echo "This test verifies Telegram works when Claude waiting for input"
echo ""

# Test 1: Normal operation (regression test)
echo "[Test 1] Normal operation (no blocking)"
echo "----------------------------------------"
echo "Action: Send Telegram message 'ping' now"
echo "Expected: Message processed, response received"
echo ""
read -p "Press Enter after sending test message..."
echo ""

# Test 2: Blocking prompt (critical test)
echo "[Test 2] Blocking prompt (CRITICAL FIX)"
echo "----------------------------------------"
echo "Creating input-waiting state..."
echo ""
echo "ACTION REQUIRED:"
echo "1. Send Telegram message 'Check inbox' now (before answering prompt)"
echo "2. Wait 5 seconds"
echo "3. Press Enter below to cancel prompt"
echo ""
echo "EXPECTED RESULT:"
echo "  - Telegram message processed as NEW command (not answer)"
echo "  - Primary responds to 'Check inbox' command"
echo "  - Response sent back via Telegram"
echo ""
echo "PROMPT (creates blocking state):"
read -p "Enter test input (DON'T ANSWER - send Telegram instead): " TEST_INPUT

echo ""
echo "Prompt cancelled. Telegram message should have been processed."
echo ""

# Test 3: Verify logs
echo "[Test 3] Verify JSONL injection logs"
echo "----------------------------------------"
echo "Recent bridge logs:"
echo ""
tail -20 /tmp/sage_telegram_bridge.log | grep -E "(JSONL|injection|@gregsmithwick)" || echo "No injection logs found yet"
echo ""

# Test 4: Verify session file
echo "[Test 4] Verify JSONL session file"
echo "----------------------------------------"
PROJECTS_DIR="/home/gregs/.claude/projects/-mnt-c-sage-sage-civilization"
if [ -d "$PROJECTS_DIR" ]; then
    echo "Session directory: $PROJECTS_DIR"
    echo ""
    echo "Recent JSONL files:"
    ls -lt "$PROJECTS_DIR"/*.jsonl 2>/dev/null | head -3 || echo "No JSONL files found"
    echo ""

    echo "Recent entries in active session:"
    ACTIVE_SESSION=$(ls -t "$PROJECTS_DIR"/*.jsonl 2>/dev/null | head -1)
    if [ -n "$ACTIVE_SESSION" ]; then
        echo "Active session: $(basename $ACTIVE_SESSION)"
        echo ""
        echo "Last 3 entries:"
        tail -3 "$ACTIVE_SESSION" | python3 -m json.tool 2>/dev/null || tail -3 "$ACTIVE_SESSION"
    fi
else
    echo "ERROR: Projects directory not found: $PROJECTS_DIR"
    echo "Check config/telegram_config.json claude_code_projects_dir setting"
fi
echo ""

echo "=========================================="
echo "TEST COMPLETE"
echo "=========================================="
echo ""
echo "Verification checklist:"
echo "  [ ] Test 1: Normal message processed"
echo "  [ ] Test 2: Blocking message processed (CRITICAL)"
echo "  [ ] Logs show JSONL injection"
echo "  [ ] Session file updated with TELEGRAM entry"
echo ""
echo "If all tests pass: FIX VERIFIED WORKING"
echo "If Test 2 fails: Check logs for errors"
echo "=========================================="
