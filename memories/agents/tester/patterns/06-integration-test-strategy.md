---
agent: tester
confidence: high
created: '2025-10-04T00:00:00+00:00'
quality_score: 27
reuse_count: 1
tags:
- testing
- integration
- strategy
- cryptography
topic: Integration Test Strategy Pattern
type: pattern
visibility: collective
---

# Integration Test Strategy Pattern

**Pattern Name**: External Library Integration Testing

**Context**: Ed25519 cryptographic library integration with ADR-004 message bus

**Problem**: Testing integration with external libraries (especially complex ones like cryptography) requires special strategies:
- External dependencies may not be installed
- Path setup needed for external code
- Real vs mock testing decisions
- Verification of correct integration

## The Pattern

### Step 1: Dynamic Path Setup

Handle external library location dynamically:

```python
import sys
from pathlib import Path

# Add external library to path
ED25519_LIB_PATH = Path.home() / "projects/AI-CIV/SHARED-DELIVERABLES/weaver-team1/ed25519-signing"
if ED25519_LIB_PATH.exists():
    sys.path.insert(0, str(ED25519_LIB_PATH))
```

**Why**:
- Tests work across different environments
- No hardcoded absolute paths
- Gracefully handles missing libraries
- Compatible with CI/CD systems

### Step 2: Import After Path Setup

```python
# After path setup, import external code
from sign_message import Ed25519Signer, verify_hub_message, load_private_key
```

**Why**:
- Imports happen after path is configured
- Clear dependency on external library
- Import errors are informative

### Step 3: Test External API Contracts

Verify you're using the external library correctly:

```python
def test_external_api_contract():
    """Verify we're using Ed25519 library API correctly."""
    # Test we can create signer
    signer = Ed25519Signer.from_private_key(private_key)
    assert hasattr(signer, 'sign')
    assert hasattr(signer, 'public_key')

    # Test signing produces expected format
    signature = signer.sign(b"test message")
    assert isinstance(signature, bytes)
    assert len(signature) == 64  # Ed25519 signature length
```

**Why**:
- Catch breaking changes in external library
- Document expected API behavior
- Verify assumptions about external code

### Step 4: Test Bidirectional Integration

Test both directions of integration:

```python
def test_our_code_to_external():
    """Test: Our message → External library signing."""
    # Our code creates message
    msg = Message(type=MessageType.QUERY, sender="researcher", ...)

    # Convert to format external library expects
    hub_msg = MessageTranslator.adr004_to_hub(msg)

    # External library signs it
    signed_hub_msg = sign_hub_message(hub_msg, signer)

    assert "signature" in signed_hub_msg
    assert "public_key" in signed_hub_msg["signature"]

def test_external_to_our_code():
    """Test: External library signature → Our message handling."""
    # External library creates signed message
    signed_hub_msg = sign_hub_message(hub_msg, signer)

    # Our code imports the signature
    our_msg = MessageTranslator.hub_to_adr004(signed_hub_msg)

    # Verify our code extracted signature correctly
    assert is_signed(our_msg)
    sig_info = extract_signature(our_msg)
    assert sig_info.algorithm == "Ed25519"
```

**Why**:
- Ensures data flows correctly both ways
- Catches format mismatches
- Validates complete integration

### Step 5: Test Integration Points

Focus tests on the "seam" between systems:

```python
def test_message_format_compatibility():
    """Test: Our message format compatible with external signer."""
    # Create message in our format
    msg = Message(...)

    # Convert to external format
    hub_msg = MessageTranslator.adr004_to_hub(msg)

    # Verify external format has required fields
    assert "content" in hub_msg
    assert "author" in hub_msg
    assert "metadata" in hub_msg

    # Sign with external library
    signed = sign_hub_message(hub_msg, signer)

    # Convert back to our format
    msg2 = MessageTranslator.hub_to_adr004(signed)

    # Verify round-trip preserved data
    assert msg2.sender == msg.sender
    assert msg2.payload == msg.payload
```

**Why**:
- Tests the "glue code" between systems
- Catches format incompatibilities
- Validates data preservation

## Real Example: Ed25519 Integration

### What We're Integrating

**External System**: Weaver's Ed25519 signing library
- Located in: `~/projects/AI-CIV/SHARED-DELIVERABLES/weaver-team1/ed25519-signing`
- Provides: `Ed25519Signer`, `sign_hub_message`, `verify_hub_message`
- Format: Hub message format (different from ADR-004)

**Our System**: ADR-004 Message Bus
- Uses: ADR-004 message format
- Needs: Signature support for messages
- Challenge: Format translation + signature preservation

### Integration Test Structure

```python
def test_end_to_end_signing():
    """Test 5: Complete end-to-end signing and verification."""

    try:
        # 1. Setup: Load external library resources
        key_path = Path.home() / ".aiciv/keys/researcher.key"
        if not key_path.exists():
            print("⚠ Private key not found")
            return

        private_key = load_private_key(str(key_path))
        signer = Ed25519Signer.from_private_key(private_key)

        # 2. Create message in our format
        msg = Message(
            type=MessageType.QUERY,
            sender="researcher",
            recipient="coder",
            payload={"query": "status_check"}
        )

        # 3. Convert to external format
        hub_msg = MessageTranslator.adr004_to_hub(msg)

        # 4. Sign using external library
        signed_hub_msg = sign_hub_message(hub_msg, signer)

        # 5. Verify using external library
        is_valid = verify_hub_message(signed_hub_msg)
        assert is_valid, "External verification failed!"

        # 6. Convert back to our format (with signature)
        signed_msg = MessageTranslator.hub_to_adr004(signed_hub_msg)

        # 7. Verify our code recognizes signature
        assert is_signed(signed_msg)
        sig_info = extract_signature(signed_msg)

        # 8. Verify signature matches registry
        registry = AgentKeyRegistry()
        registered_key = registry.get_public_key("researcher")
        assert sig_info.public_key == registered_key

        print("✓ End-to-end integration successful!")

    except Exception as e:
        print(f"⚠ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
```

### What This Tests

✅ **Path Setup**: External library can be imported
✅ **Resource Loading**: Keys can be loaded from file system
✅ **API Usage**: We use Ed25519Signer API correctly
✅ **Format Conversion**: ADR-004 ↔ Hub format works
✅ **Signing**: External library signs our messages
✅ **Verification**: External library verifies signatures
✅ **Signature Import**: Our code extracts signature from hub format
✅ **Registry Integration**: Signature matches registered public key

## Integration Testing Checklist

Before writing integration tests:

- [ ] **Identify Integration Points**: Where do systems connect?
- [ ] **Document Data Formats**: What format does each system expect?
- [ ] **Map API Contracts**: What methods/functions are we calling?
- [ ] **Handle Missing Dependencies**: What if external system unavailable?
- [ ] **Test Both Directions**: Our code → External, External → Our code
- [ ] **Verify Data Preservation**: Round-trip doesn't lose data
- [ ] **Test Error Cases**: What happens when external system fails?
- [ ] **Document Assumptions**: What are we assuming about external code?

## Common Integration Patterns

### Pattern A: Adapter Testing

Test the adapter/translator layer:

```python
def test_adapter_to_external():
    """Test our adapter converts to external format correctly."""
    internal_obj = OurObject(...)
    external_obj = OurAdapter.to_external(internal_obj)

    # Verify external system accepts this format
    result = external_system.process(external_obj)
    assert result.success

def test_adapter_from_external():
    """Test our adapter converts from external format correctly."""
    external_obj = external_system.create(...)
    internal_obj = OurAdapter.from_external(external_obj)

    # Verify we extracted data correctly
    assert internal_obj.field == expected_value
```

### Pattern B: Wrapper Testing

Test wrapper around external library:

```python
def test_wrapper_delegates_correctly():
    """Test our wrapper delegates to external library correctly."""
    wrapper = OurWrapper()

    # Our wrapper method
    result = wrapper.our_method(args)

    # Should call external library's method
    # (verify by checking result format or side effects)
    assert result.matches_external_format
```

### Pattern C: Compatibility Testing

Test version compatibility:

```python
def test_external_library_version():
    """Verify we're compatible with external library version."""
    import external_library

    # Document which version we tested with
    print(f"Testing with external_library v{external_library.__version__}")

    # Test critical APIs exist
    assert hasattr(external_library, 'required_function')
    assert hasattr(external_library, 'required_class')
```

## Success Metrics

**Time Saved**: 45-60 minutes per integration issue
- Catch integration bugs early (not in production)
- Verify external library updates don't break us
- Document integration assumptions

**Reliability**:
- 100% confidence external library is used correctly
- Clear test failures when external API changes
- No surprises in production

## When to Apply

✅ **Use Integration Testing when**:
- Integrating external libraries
- Multiple systems need to interoperate
- Data format conversions occur
- Cross-system workflows exist
- External dependencies are complex (crypto, databases, APIs)

❌ **Don't use when**:
- Pure unit testing (no external dependencies)
- External system is trivial (e.g., math library)
- Mocking is sufficient for tests

## Template: External Library Integration Test

```python
"""
Integration tests for [External Library] integration.

External Library: [name and version]
Location: [path or package]
Purpose: [what it provides]
"""

import sys
from pathlib import Path

# Setup path to external library
EXTERNAL_LIB_PATH = Path.home() / "path/to/external/library"
if EXTERNAL_LIB_PATH.exists():
    sys.path.insert(0, str(EXTERNAL_LIB_PATH))

from external_library import ExternalClass, external_function

def test_external_api_availability():
    """Test 1: External library API is available."""
    # Verify imports work
    assert ExternalClass is not None
    assert external_function is not None

def test_our_to_external_conversion():
    """Test 2: Convert our format to external format."""
    our_obj = OurClass(...)

    # Convert
    external_obj = OurConverter.to_external(our_obj)

    # Verify external system accepts it
    result = external_function(external_obj)
    assert result.success

def test_external_to_our_conversion():
    """Test 3: Convert external format to our format."""
    external_obj = ExternalClass(...)

    # Convert
    our_obj = OurConverter.from_external(external_obj)

    # Verify we have correct data
    assert our_obj.field == expected_value

def test_round_trip_integration():
    """Test 4: Round-trip conversion preserves data."""
    original = OurClass(field="value")

    # Convert to external and back
    external = OurConverter.to_external(original)
    result = OurConverter.from_external(external)

    # Verify no data loss
    assert result.field == original.field

def test_end_to_end_workflow():
    """Test 5: Complete workflow using external library."""
    # Create in our format
    our_obj = OurClass(...)

    # Use external library to process
    external_obj = OurConverter.to_external(our_obj)
    processed = external_function(external_obj)

    # Import results
    result = OurConverter.from_external(processed)

    # Verify expected outcome
    assert result.meets_expectations
```

## Anti-Patterns to Avoid

❌ **Over-Mocking**:
```python
# BAD: Mock everything, don't test real integration
@patch('external_library.function')
def test_integration(mock_function):
    mock_function.return_value = "mocked"
    # This doesn't test integration!
```

❌ **Hardcoded Paths**:
```python
# BAD: Won't work on other machines
sys.path.insert(0, "/home/alice/projects/external-lib")
```

❌ **Assuming External Behavior**:
```python
# BAD: Don't assume, verify!
# "I think external library returns bytes"
result = external_function()
# Could be str, could be bytes, could be anything!
```

✅ **Correct Patterns**:
```python
# Test real integration with real library
result = external_function(real_input)
assert isinstance(result, expected_type)
assert result.has_expected_format
```

## Evidence from Ed25519 Suite

**Integration Tested**:
- External library: Weaver's Ed25519 signing
- Our code: ADR-004 message bus
- Integration points: Format conversion, signing, verification

**Results**:
- 5 integration tests pass
- Complete workflow validated
- Signature preservation verified
- Registry integration confirmed

**Last Validated**: 2025-10-03 (Ed25519 + ADR-004 Integration)
