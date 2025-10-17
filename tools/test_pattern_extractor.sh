#!/bin/bash
# Test suite for pattern_extractor.py

echo "=========================================="
echo "Pattern Extractor Test Suite"
echo "=========================================="
echo ""

# Test 1: Basic extraction
echo "Test 1: Extract patterns from sample file"
python3 tools/pattern_extractor.py \
  --files "task-tracker/task_tracker/models.py" \
  --output /tmp/pattern_test \
  > /tmp/test1.out 2>&1

if grep -q "Pattern Extraction Complete" /tmp/test1.out; then
  echo "✅ PASS: Pattern extraction works"
else
  echo "❌ FAIL: Pattern extraction failed"
  cat /tmp/test1.out
fi
echo ""

# Test 2: Similarity detection
echo "Test 2: Similarity detection"
python3 tools/pattern_extractor.py \
  --similarity "task-tracker/task_tracker/models.py" \
  --codebase task-tracker \
  > /tmp/test2.out 2>&1

if grep -q "Similar Code" /tmp/test2.out; then
  echo "✅ PASS: Similarity detection works"
else
  echo "❌ FAIL: Similarity detection failed"
  cat /tmp/test2.out
fi
echo ""

# Test 3: Pattern suggestions
echo "Test 3: Pattern suggestions"
python3 tools/pattern_extractor.py \
  --task-description "pydantic model validation" \
  --suggest-from memories/agents/coder/patterns \
  > /tmp/test3.out 2>&1

if grep -q "Pattern Suggestions" /tmp/test3.out; then
  echo "✅ PASS: Pattern suggestions work"
else
  echo "❌ FAIL: Pattern suggestions failed"
  cat /tmp/test3.out
fi
echo ""

# Test 4: Help text
echo "Test 4: Help text displays"
python3 tools/pattern_extractor.py --help > /tmp/test4.out 2>&1

if grep -q "Extract code patterns" /tmp/test4.out; then
  echo "✅ PASS: Help text works"
else
  echo "❌ FAIL: Help text failed"
fi
echo ""

# Test 5: Pattern file creation
echo "Test 5: Pattern files created correctly"
if [ -d "/tmp/pattern_test" ] && [ "$(find /tmp/pattern_test -name '*.md' | wc -l)" -gt 0 ]; then
  echo "✅ PASS: Pattern files created"
  echo "   Files: $(find /tmp/pattern_test -name '*.md' | wc -l)"
else
  echo "❌ FAIL: Pattern files not created"
fi
echo ""

# Cleanup
rm -rf /tmp/pattern_test /tmp/test*.out

echo "=========================================="
echo "Test Suite Complete"
echo "=========================================="
