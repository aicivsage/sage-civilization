# Chat Queue Integration Tests

## Overview

Comprehensive integration test suite for the Sage chat queue system, which routes messages between Greg (human user) and the Sage AI civilization via a file-based queue.

## Test Coverage

**Target**: 60%+ coverage across all chat queue components

**Components Tested**:
- `scripts/chat_queue_monitor.py` - Main queue monitor
- `scripts/auto_queue_responder.py` - Automated alert system
- `web/chat.py` - Chat server and Socket.IO integration

## Running Tests

### Quick Start

```bash
# Install test dependencies (if not already installed)
pip install -r tests/requirements.txt

# Run all chat queue tests
pytest tests/test_chat_queue_integration.py -v

# Run with coverage report
pytest tests/test_chat_queue_integration.py --cov=scripts.chat_queue_monitor --cov=scripts.auto_queue_responder --cov-report=html --cov-report=term

# Run specific test class
pytest tests/test_chat_queue_integration.py::TestEndToEndFlow -v

# Run only fast tests (exclude slow/performance tests)
pytest tests/test_chat_queue_integration.py -v -m "not slow"
```

### Coverage Report

After running with `--cov-report=html`, open:
```
htmlcov/index.html
```

## Test Structure

### Test Classes

1. **TestChatQueueMonitorInit** - Initialization and setup
   - Directory creation
   - Processed messages loading
   - Error handling for corrupted state

2. **TestMessageHistory** - Message history operations
   - Saving messages to history
   - Retrieving room history
   - History size limits (1000 message cap)
   - I/O error handling

3. **TestMessageQueueing** - Queueing messages for Primary AI
   - Queue file creation
   - Context inclusion (last 10 messages)
   - Error handling during queueing

4. **TestResponseProcessing** - Processing Primary AI responses
   - Valid response delivery
   - Invalid format handling
   - Corrupted JSON handling
   - Multiple response processing
   - Socket.IO integration

5. **TestNewMessageDetection** - Detecting new messages from Greg
   - User identification (by user_id and username)
   - Deduplication (processed messages)
   - Agent message filtering
   - Multiple message processing

6. **TestProcessedMessagesPersistence** - State management
   - Saving processed message IDs
   - Loading processed message IDs
   - Error handling

7. **TestAutoQueueResponder** - Auto-responder functionality
   - Pending message counting
   - Message preview generation
   - Alert formatting
   - Truncation and limits

8. **TestEndToEndFlow** - Complete integration scenarios
   - Full message flow (user → queue → response → delivery)
   - Concurrent messages
   - Deduplication
   - Empty message handling

9. **TestPerformance** - Performance characteristics
   - Large history handling (500+ messages)
   - Many pending messages (50+)
   - Response time verification

10. **TestEdgeCases** - Boundary conditions
    - Special characters and emojis
    - Very long messages (10k+ chars)
    - Rapid message succession
    - Message ID collisions

## Test Scenarios Covered

### Happy Path
✅ User sends message → Monitor detects → Queues for Primary AI
✅ Primary AI writes response → Monitor delivers via Socket.IO
✅ Message history preserved correctly
✅ Context (last 10 messages) included in queue

### Error Handling
✅ Corrupted JSON files (processed gracefully)
✅ Missing required fields (moved to error directory)
✅ I/O errors (disk full, permissions)
✅ Network errors (Socket.IO timeout, connection failure)
✅ Malformed messages (missing fields)

### Edge Cases
✅ Empty messages
✅ Very long messages (10k+ characters)
✅ Special characters and emojis
✅ Duplicate message IDs (deduplication)
✅ Rapid message succession (race conditions)
✅ Multiple concurrent messages

### Integration Points
✅ File system operations (pending/, responses/, processed/)
✅ Socket.IO message delivery (mocked HTTP calls)
✅ Message history persistence (JSON files)
✅ Processed messages tracking (state file)

## Key Testing Patterns

### Fixture Usage

**temp_chat_dir**: Isolated temporary directory structure
- Prevents test pollution
- Simulates production directory layout
- Automatic cleanup

**sample_message**: Realistic message fixture
- Greg's user_id
- Proper timestamp format
- Required fields

**sample_context_messages**: Conversation context
- Multiple message history
- Mixed user/agent messages

### Mocking Strategy

**Requests mocking**: All HTTP calls mocked
- `requests.post` for Socket.IO delivery
- Prevents actual network calls during testing
- Validates request parameters

**Monkey-patching**: Directory paths redirected
- Uses pytest's `monkeypatch` fixture
- Isolates tests from production directories
- Allows testing without setup

## Coverage Goals by Component

| Component | Target | Key Areas |
|-----------|--------|-----------|
| chat_queue_monitor.py | 70%+ | All methods, error paths |
| auto_queue_responder.py | 80%+ | All functions |
| Integration flows | 100% | End-to-end scenarios |

## Adding New Tests

When adding features, ensure tests cover:

1. **Happy path** - Normal operation
2. **Error cases** - All exception paths
3. **Edge cases** - Boundary conditions
4. **Integration** - End-to-end flow
5. **Performance** - Large data handling

### Test Template

```python
def test_new_feature_happy_path(temp_chat_dir, sample_message):
    """Test [feature] works correctly in normal case"""
    monitor = ChatQueueMonitor()

    # Setup
    # ... prepare test data

    # Action
    # ... call the feature

    # Assertions
    assert expected_result

def test_new_feature_error_handling(temp_chat_dir):
    """Test [feature] handles errors gracefully"""
    monitor = ChatQueueMonitor()

    # Setup error condition
    with patch('some.module.function', side_effect=IOError()):
        # Action - should not raise
        # ... call the feature

        # Verify error logged but didn't crash
```

## Dependencies

Required packages (in `tests/requirements.txt`):
- pytest >= 7.4.0
- pytest-cov >= 4.1.0
- pytest-mock >= 3.11.0

## CI/CD Integration

These tests are designed to run in CI/CD pipelines:

```bash
# Run in CI (with coverage threshold)
pytest tests/test_chat_queue_integration.py \
  --cov=scripts.chat_queue_monitor \
  --cov=scripts.auto_queue_responder \
  --cov-report=term \
  --cov-fail-under=60
```

Exit code will be non-zero if coverage falls below 60%.

## Troubleshooting

### Import Errors

If tests fail with import errors:
```bash
# Ensure scripts/ and web/ are in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/scripts:$(pwd)/web"
pytest tests/test_chat_queue_integration.py
```

### File Permission Errors

Tests use temporary directories, but if you see permission errors:
```bash
# Clean up any stale temp directories
rm -rf /tmp/pytest-of-*
```

### Coverage Not Showing

Ensure you're running from the project root:
```bash
cd /path/to/sage-civilization
pytest tests/test_chat_queue_integration.py --cov=scripts --cov-report=term
```

## Test Execution Time

Expected test execution time:
- **Fast tests** (~40 tests): < 5 seconds
- **All tests** (~50 tests): < 10 seconds
- **With coverage**: +2-3 seconds

## Contributing

When adding new chat queue features:

1. Write tests FIRST (TDD approach)
2. Ensure coverage doesn't drop below 60%
3. Add edge cases and error handling tests
4. Update this README if adding new test classes
5. Run full suite before committing

## Test Philosophy

**Partnership Testing**: Tests serve multiple purposes
- **For humans**: Confidence in system reliability
- **For agents**: Safe experimentation space
- **For descendants**: Documented behavior patterns

**Quality Standard**: 60%+ coverage is not just a metric - it's a commitment to system reliability for critical human-AI communication.

---

**Last Updated**: 2025-10-26
**Test Count**: 50+ integration tests
**Coverage Target**: 60%+
**Maintenance**: Living document - update with new tests
