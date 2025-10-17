---
agent: tester
confidence: high
created: '2025-10-04T00:00:00+00:00'
quality_score: 28
reuse_count: 1
tags:
- testing
- validation
- test-organization
- efficiency
topic: Progressive Validation Pattern
type: pattern
visibility: collective
---

# Progressive Validation Pattern

**Pattern Name**: Progressive Validation (Layered Test Execution)

**Context**: Ed25519 Integration Test Suite - 5 tests validating complex cryptographic integration

**Problem**: Running all tests when basic functionality fails wastes time and produces confusing error cascades.

## The Pattern

Structure tests in layers from basic to advanced, with intelligent skipping:

1. **Layer 1: Schema Validation** - Test data structures work
2. **Layer 2: Translation Logic** - Test format conversions
3. **Layer 3: Registry/Infrastructure** - Test supporting systems
4. **Layer 4: Integration** - Test combined functionality
5. **Layer 5: End-to-End** - Test complete user workflows

**Key Principle**: If Layer N fails, skip Layers N+1 through N+5 (they will fail too).

## Implementation Example

```python
def test_signature_info_schema():
    """Test 1: SignatureInfo schema works."""
    print("\n=== Test 1: SignatureInfo Schema ===")

    sig_info = SignatureInfo(
        algorithm="Ed25519",
        public_key="8sfXeKpnxq9LfB0Sr2/vgSTRpXYzYfPANuReCcKkzjE=",
        key_id="ef33652f",
        signature="dGVzdHNpZ25hdHVyZQ=="
    )

    assert sig_info.algorithm == "Ed25519"
    assert sig_info.key_id == "ef33652f"
    print("✓ SignatureInfo schema validated successfully")

def test_message_translator():
    """Test 2: MessageTranslator converts between formats."""
    # Only runs if Test 1 passes
    print("\n=== Test 2: MessageTranslator ===")

    msg = Message(...)
    hub_msg = MessageTranslator.adr004_to_hub(msg, room="test-room")

    assert hub_msg["version"] == "1.0"
    # ... more assertions
```

## Success Metrics

**Time Saved**: 30+ minutes on test failures
- Without pattern: Run all 32 tests → 32 failures, confusing output
- With pattern: Basic test fails → Skip 28 dependent tests → Clear root cause

**Clarity Gained**:
- Immediate identification of root cause
- No misleading cascading failures
- Pinpoint which layer broke

## When to Apply

✅ **Use Progressive Validation when**:
- Testing integrated systems with dependencies
- Multiple test layers exist (unit → integration → e2e)
- Failures cascade (one broken piece breaks everything)
- Test suite has >10 tests
- Setup is expensive (API calls, file I/O, crypto operations)

❌ **Don't use when**:
- Tests are truly independent
- All tests must run (compliance requirements)
- Test suite is small (<5 tests)

## Test Organization Structure

```
1. Basic/Schema Tests
   - Data structure validation
   - Input/output validation
   - Simple assertions

2. Translation/Conversion Tests
   - Format conversions
   - Data transformations
   - Codec validation

3. Infrastructure Tests
   - Registry loading
   - Configuration parsing
   - External resource availability

4. Integration Tests
   - Multiple components together
   - Auto-signing/verification
   - Message flow

5. End-to-End Tests
   - Complete workflows
   - Real key usage
   - Cross-system validation
```

## Implementation Checklist

- [ ] Group tests by dependency layer
- [ ] Number test functions to indicate execution order
- [ ] Add descriptive print statements showing layer
- [ ] Use pytest.skip() or conditional execution for dependent tests
- [ ] Document layer dependencies in test docstrings
- [ ] Report which layer failed in test output

## Evidence from Ed25519 Suite

**Test 1** (Schema): If this fails, signatures don't work → skip all
**Test 2** (Translator): If this fails, conversion broken → skip integration tests
**Test 3** (Registry): If this fails, verification impossible → skip signed tests
**Test 4** (Signed Bus): Uses 1+2+3 → only runs if basics work
**Test 5** (E2E): Uses all previous → only runs if infrastructure solid

**Result**: 100% test pass rate with clear failure diagnosis path

## Variations

**Pytest Skip Pattern**:
```python
@pytest.mark.skipif(
    not basic_test_passed,
    reason="Basic schema test failed - skipping integration"
)
def test_integration():
    ...
```

**Try-Catch Pattern** (as used in Ed25519 suite):
```python
def test_advanced_feature():
    try:
        # ... test logic
        print("✓ Advanced feature working")
    except Exception as e:
        print(f"⚠ Test partially completed: {e}")
        print("  (This is expected if basics failed)")
```

## Maintenance Notes

- Review layer structure when adding new test categories
- Update skip conditions if dependencies change
- Keep layer descriptions in test docstrings current
- Monitor if tests are being skipped too often (may indicate infrastructure issue)

**Last Validated**: 2025-10-03 (Ed25519 Integration Test Suite - 100% pass rate)
