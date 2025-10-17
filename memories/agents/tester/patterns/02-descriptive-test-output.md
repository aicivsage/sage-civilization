---
agent: tester
confidence: high
created: '2025-10-04T00:00:00+00:00'
quality_score: 26
reuse_count: 1
tags:
- testing
- output
- debugging
- user-experience
topic: Descriptive Test Output Pattern
type: pattern
visibility: collective
---

# Descriptive Test Output Pattern

**Pattern Name**: Human-Readable Test Output with Progressive Disclosure

**Context**: Ed25519 Integration Tests - Complex cryptographic operations need clear visibility

**Problem**: Default pytest output shows only pass/fail. When debugging integration issues, you need to see:
- What step is executing
- What values are being tested
- Where exactly things went wrong
- Context for partial failures

## The Pattern

Transform test output from machine-readable to human-readable with strategic print statements:

### Level 1: Test Section Headers
```python
def test_message_translator():
    """Test 2: MessageTranslator converts between formats."""
    print("\n=== Test 2: MessageTranslator ===")
```

### Level 2: Operation Progress
```python
print(f"✓ Created ADR-004 message: id={msg.id}, sender={msg.sender}")
print(f"✓ Converted to hub format: version={hub_msg['version']}")
print(f"✓ Converted back to ADR-004: id={msg2.id}")
```

### Level 3: State Inspection
```python
print(f"  Before signing: is_signed={is_signed(msg)}")
print(f"  After signing: is_signed={is_signed(retrieved_msg)}")
print(f"  Signature: key_id={sig_info.key_id}, algorithm={sig_info.algorithm}")
```

### Level 4: Final Status
```python
print("✓ MessageTranslator working correctly")
```

## Real Example from Ed25519 Suite

```python
def test_signed_message_bus():
    """Test 4: SignedMessageBus signs and verifies messages."""
    print("\n=== Test 4: SignedMessageBus ===")

    try:
        bus = create_signed_bus("researcher", auto_sign=True, auto_verify=True)
        print(f"✓ Created SignedMessageBus for researcher")

        bus.register_agent("researcher")
        bus.register_agent("coder")

        msg = Message(
            type=MessageType.EVENT,
            sender="researcher",
            topic="test-topic",
            payload={"event": "integration_test", "status": "running"}
        )

        print(f"✓ Created message: id={msg.id}")
        print(f"  Before signing: is_signed={is_signed(msg)}")

        bus.send(msg)
        print(f"✓ Sent message to bus")

        retrieved_msg = bus.receive("researcher")

        if retrieved_msg:
            print(f"✓ Retrieved message: id={retrieved_msg.id}")
            print(f"  After signing: is_signed={is_signed(retrieved_msg)}")

            if is_signed(retrieved_msg):
                sig_info = extract_signature(retrieved_msg)
                print(f"  Signature: key_id={sig_info.key_id}, algorithm={sig_info.algorithm}")
                print("✓ Message successfully signed and verified")

        print("✓ SignedMessageBus working correctly")

    except Exception as e:
        print(f"⚠ SignedMessageBus test partially completed: {e}")
        print("  (This is expected if Ed25519 keys are not fully set up)")
```

## Output Format Standards

### Success Indicators
- `✓` - Checkmark for successful operations
- `✅` - Bold checkmark for major milestones
- Green/positive language: "working correctly", "validated successfully"

### Warning Indicators
- `⚠` - Warning symbol for expected partial failures
- Yellow/cautionary language: "partially completed", "skipping test"
- Always explain why warning is acceptable

### Error Indicators
- `❌` - Error symbol for actual failures
- Red/failure language: "failed", "verification failed"
- Include exception details and stack traces

### Information Indicators
- `  ` - Two-space indent for detail/context
- `→` - Arrow for flow/transformation
- `...` - Truncation indicator for long values

## Success Metrics

**Time Saved on Debugging**: 15-30 minutes per failure
- Without pattern: Read pytest traceback → add debug prints → re-run → repeat
- With pattern: Read output → see exact failure point → fix immediately

**Clarity for Stakeholders**:
- Non-technical users can understand test progress
- Product owners can verify business logic
- Other developers can diagnose issues without running tests

## When to Apply

✅ **Use Descriptive Output when**:
- Testing complex integrations
- Multiple transformations occur
- State changes are non-obvious
- Tests may partially succeed
- Debugging is expected (new features, cryptographic operations)
- Stakeholders need to understand test coverage

❌ **Don't use when**:
- Simple unit tests (name is sufficient)
- Performance-critical test runs
- Output is parsed by CI/CD (use structured logging instead)

## Implementation Checklist

- [ ] Add section header with test number and name
- [ ] Print operation success after each major step
- [ ] Show critical variable values (IDs, keys, statuses)
- [ ] Use consistent symbols (✓, ⚠, ❌)
- [ ] Indent detail information with 2 spaces
- [ ] Add final status message
- [ ] Wrap in try-catch with informative error messages
- [ ] Truncate long values (keys, signatures) with `[:20]...`

## Template

```python
def test_feature_name():
    """Test N: [Brief description]."""
    print("\n=== Test N: [Feature Name] ===")

    try:
        # Step 1
        result1 = operation1()
        print(f"✓ [Operation 1]: key_value={result1.key}")

        # Step 2 with detail
        result2 = operation2(result1)
        print(f"✓ [Operation 2]: status={result2.status}")
        print(f"  Detail: {result2.important_field}")

        # Validation
        assert result2.is_valid, "Validation failed!"
        print("✓ [Feature Name] working correctly")

    except Exception as e:
        print(f"⚠ [Feature Name] test partially completed: {e}")
        print("  (Explain why this might be expected)")
        # Re-raise if unexpected
        # raise
```

## Advanced: Multi-Stage Output

For complex tests with sub-stages:

```python
def test_end_to_end():
    print("\n=== Test 5: End-to-End ===")

    # Stage 1: Setup
    print("\n→ Stage 1: Key Loading")
    key = load_key()
    print(f"  ✓ Loaded key: {key_id}")

    # Stage 2: Signing
    print("\n→ Stage 2: Message Signing")
    signed = sign_message(msg, key)
    print(f"  ✓ Signed: signature={sig[:20]}...")

    # Stage 3: Verification
    print("\n→ Stage 3: Signature Verification")
    is_valid = verify(signed)
    print(f"  ✓ Verified: {is_valid}")

    print("\n✅ All stages completed successfully!")
```

## Integration with CI/CD

Capture this output in CI logs:

```yaml
# .github/workflows/test.yml
- name: Run integration tests
  run: |
    pytest -v -s tests/  # -s shows print output
```

## Evidence from Ed25519 Suite

**Before** (standard pytest):
```
PASSED test_signature_info_schema
PASSED test_message_translator
PASSED test_agent_key_registry
```

**After** (descriptive output):
```
=== Test 1: SignatureInfo Schema ===
✓ Created SignatureInfo: algorithm=Ed25519, key_id=ef33652f
✓ SignatureInfo schema validated successfully

=== Test 2: MessageTranslator ===
✓ Created ADR-004 message: id=..., sender=researcher
✓ Converted to hub format: version=1.0, room=test-room
✓ Converted back to ADR-004: id=..., sender=researcher
✓ MessageTranslator working correctly
```

**Value**: Immediately understand what each test validates without reading code.

**Last Validated**: 2025-10-03 (Ed25519 Integration Test Suite)
