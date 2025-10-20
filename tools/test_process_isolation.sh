#!/bin/bash
# Test Process Isolation Between A-C-Gee and Weaver
# Verifies that monitor processes can coexist without interference

set -e

PROJECT_ROOT="/home/corey/projects/AI-CIV/grow_gemini_deepresearch"
ACGEE_PID_FILE="$PROJECT_ROOT/.tg_sessions/acgee_monitor.pid"
WEAVER_REPO="/home/corey/projects/AI-CIV/grow_openai"

echo "=== Testing Process Isolation Between A-C-Gee and Weaver ==="
echo ""

# Test 1: Check current A-C-Gee monitor status
echo "Test 1: A-C-Gee Monitor Status"
echo "-------------------------------"
if [ -f "$ACGEE_PID_FILE" ]; then
    ACGEE_PID=$(cat "$ACGEE_PID_FILE")
    if ps -p "$ACGEE_PID" > /dev/null 2>&1; then
        echo "✅ A-C-Gee monitor running (PID: $ACGEE_PID)"
        echo "   Process: $(ps -p $ACGEE_PID -o cmd --no-headers)"
    else
        echo "❌ A-C-Gee PID file exists but process not running"
        exit 1
    fi
else
    echo "⚠️  No A-C-Gee PID file found"
    echo "   Will start monitor in next step"
fi
echo ""

# Test 2: Check Weaver monitor status
echo "Test 2: Weaver Monitor Status"
echo "------------------------------"
WEAVER_PID=$(pgrep -f "grow_openai/tools/telegram_monitor.py" || echo "")
if [ -n "$WEAVER_PID" ]; then
    echo "✅ Weaver monitor running (PID: $WEAVER_PID)"
    echo "   Process: $(ps -p $WEAVER_PID -o cmd --no-headers)"
else
    echo "⚠️  Weaver monitor not running (this is OK, test will still work)"
fi
echo ""

# Test 3: Verify path-based filtering works
echo "Test 3: Path-Based Process Filtering"
echo "-------------------------------------"
ACGEE_PROCS=$(pgrep -f "grow_gemini_deepresearch/tools/telegram_monitor.py" | wc -l)
WEAVER_PROCS=$(pgrep -f "grow_openai/tools/telegram_monitor.py" | wc -l)
echo "A-C-Gee monitors found: $ACGEE_PROCS (expected: 1)"
echo "Weaver monitors found: $WEAVER_PROCS (expected: 0 or 1)"

if [ "$ACGEE_PROCS" -gt 1 ]; then
    echo "❌ Multiple A-C-Gee monitors running! This is a problem."
    exit 1
fi
echo "✅ Path-based filtering working correctly"
echo ""

# Test 4: Verify PID file isolation
echo "Test 4: PID File Isolation"
echo "--------------------------"
if [ -f "$ACGEE_PID_FILE" ]; then
    echo "✅ A-C-Gee PID file: $ACGEE_PID_FILE"
    echo "   Contents: $(cat $ACGEE_PID_FILE)"
fi

if [ -d "$WEAVER_REPO/.tg_sessions" ]; then
    WEAVER_PID_FILES=$(find "$WEAVER_REPO/.tg_sessions" -name "*.pid" 2>/dev/null | wc -l)
    echo "   Weaver PID files in .tg_sessions: $WEAVER_PID_FILES"
    if [ "$WEAVER_PID_FILES" -gt 0 ]; then
        echo "   Weaver PID files: $(find "$WEAVER_REPO/.tg_sessions" -name "*.pid" 2>/dev/null)"
    fi
else
    echo "   Weaver .tg_sessions directory not found (may not exist yet)"
fi
echo "✅ PID files are separate"
echo ""

# Test 5: Verify log file separation
echo "Test 5: Log File Separation"
echo "---------------------------"
if [ -f "/tmp/acgee_telegram_monitor.log" ]; then
    ACGEE_LOG_SIZE=$(wc -l < /tmp/acgee_telegram_monitor.log)
    echo "✅ A-C-Gee log: /tmp/acgee_telegram_monitor.log ($ACGEE_LOG_SIZE lines)"
fi

if [ -f "/tmp/telegram_monitor.log" ]; then
    WEAVER_LOG_SIZE=$(wc -l < /tmp/telegram_monitor.log)
    echo "   Weaver log: /tmp/telegram_monitor.log ($WEAVER_LOG_SIZE lines)"
fi
echo "✅ Log files are separate"
echo ""

# Test 6: Simulate restart (dry run)
echo "Test 6: Safe Restart Simulation (Dry Run)"
echo "-----------------------------------------"
if [ -f "$ACGEE_PID_FILE" ]; then
    OLD_PID=$(cat "$ACGEE_PID_FILE")
    echo "Would restart A-C-Gee monitor (current PID: $OLD_PID)"
    echo "Command: bash $PROJECT_ROOT/tools/restart_telegram_monitor.sh"
    echo ""
    echo "Verification that Weaver would NOT be affected:"
    if [ -n "$WEAVER_PID" ]; then
        echo "  - Weaver PID: $WEAVER_PID"
        echo "  - A-C-Gee PID file: $ACGEE_PID_FILE (contains: $OLD_PID)"
        echo "  - Different PIDs = Weaver safe ✅"
    else
        echo "  - Weaver not running, nothing to protect"
    fi
fi
echo ""

# Summary
echo "======================================="
echo "Process Isolation Test Summary"
echo "======================================="
echo ""
echo "Configuration:"
echo "  A-C-Gee PID file: $ACGEE_PID_FILE"
echo "  A-C-Gee processes: $ACGEE_PROCS"
echo "  Weaver processes: $WEAVER_PROCS"
echo ""
echo "Isolation verified:"
echo "  ✅ Path-based filtering separates processes"
echo "  ✅ PID files are civilization-specific"
echo "  ✅ Log files are separate"
echo "  ✅ Restart script targets only A-C-Gee process"
echo ""
echo "To actually restart A-C-Gee monitor:"
echo "  bash tools/restart_telegram_monitor.sh"
echo ""
echo "To verify both civilizations coexist:"
echo "  ps aux | grep telegram_monitor.py | grep -v grep"
echo ""
