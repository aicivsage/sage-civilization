#!/bin/bash
# Test script for generate_startup_summary.py
# Demonstrates all functionality with various agents and tasks

echo "=============================================="
echo "Testing Startup Summary Generator"
echo "=============================================="
echo ""

# Test 1: Coder with REST API task
echo "TEST 1: Coder agent - REST API authentication"
echo "----------------------------------------------"
python3 tools/generate_startup_summary.py \
  --agent coder \
  --task "implement REST API authentication middleware with JWT tokens"
echo ""
echo ""

# Test 2: Researcher with async task
echo "TEST 2: Researcher agent - Async frameworks"
echo "----------------------------------------------"
python3 tools/generate_startup_summary.py \
  --agent researcher \
  --task "research Python async frameworks for web scraping"
echo ""
echo ""

# Test 3: Tester (might have less history)
echo "TEST 3: Tester agent - Integration testing"
echo "----------------------------------------------"
python3 tools/generate_startup_summary.py \
  --agent tester \
  --task "write integration tests for email notification system"
echo ""
echo ""

# Test 4: File output test
echo "TEST 4: File output test - Email Monitor"
echo "----------------------------------------------"
OUTPUT_FILE="/tmp/email_monitor_summary.md"
python3 tools/generate_startup_summary.py \
  --agent email-monitor \
  --task "monitor inbox and categorize incoming emails" \
  --output "$OUTPUT_FILE"

if [ -f "$OUTPUT_FILE" ]; then
    echo "✅ File created successfully: $OUTPUT_FILE"
    echo "File size: $(wc -c < "$OUTPUT_FILE") bytes"
    echo "Line count: $(wc -l < "$OUTPUT_FILE") lines"
else
    echo "❌ File creation failed"
fi
echo ""
echo ""

# Test 5: Performance test (10 runs)
echo "TEST 5: Performance test (10 runs)"
echo "----------------------------------------------"
total_time=0
for i in {1..10}; do
    start=$(date +%s%N)
    python3 tools/generate_startup_summary.py \
      --agent coder \
      --task "test task" > /dev/null 2>&1
    end=$(date +%s%N)
    elapsed=$((($end - $start) / 1000000))  # Convert to milliseconds
    total_time=$(($total_time + $elapsed))
    echo "Run $i: ${elapsed}ms"
done

average=$(($total_time / 10))
echo "Average execution time: ${average}ms"
if [ $average -lt 2000 ]; then
    echo "✅ Performance: PASSED (< 2000ms)"
else
    echo "❌ Performance: FAILED (>= 2000ms)"
fi
echo ""
echo ""

echo "=============================================="
echo "All tests completed!"
echo "=============================================="
