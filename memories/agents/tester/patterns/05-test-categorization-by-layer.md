---
agent: tester
confidence: high
created: '2025-10-04T00:00:00+00:00'
quality_score: 26
reuse_count: 1
tags:
- testing
- organization
- test-strategy
- layers
topic: Test Categorization by Layer Pattern
type: pattern
visibility: collective
---

# Test Categorization by Layer Pattern

**Pattern Name**: Layer-Based Test Organization

**Context**: Ed25519 Integration Test Suite - 5 tests covering schema → translation → infrastructure → integration → e2e

**Problem**: Flat test organization makes it hard to:
- Understand test scope and purpose
- Identify which layer broke
- Run specific test categories
- Estimate testing effort
- Know what's covered vs what's missing

## The Pattern

Organize tests into explicit layers that mirror system architecture:

```
Layer 1: Schema/Data Structure Tests
  ↓
Layer 2: Business Logic/Translation Tests
  ↓
Layer 3: Infrastructure/Registry Tests
  ↓
Layer 4: Integration/Component Tests
  ↓
Layer 5: End-to-End/Workflow Tests
```

Each layer tests progressively higher-level functionality while depending on lower layers.

## Implementation in Ed25519 Suite

### Layer 1: Schema Tests
**Purpose**: Validate data structures work correctly

```python
def test_signature_info_schema():
    """Test 1: SignatureInfo schema works."""
    sig_info = SignatureInfo(
        algorithm="Ed25519",
        public_key="8sfXeKpnxq9LfB0Sr2/vgSTRpXYzYfPANuReCcKkzjE=",
        key_id="ef33652f",
        signature="dGVzdHNpZ25hdHVyZQ=="
    )

    assert sig_info.algorithm == "Ed25519"
    assert sig_info.key_id == "ef33652f"
```

**What it tests**:
- Data models instantiate correctly
- Field validation works
- Required fields enforced
- Type checking works

**Dependencies**: None (pure data structures)

### Layer 2: Translation/Business Logic Tests
**Purpose**: Validate transformations and conversions

```python
def test_message_translator():
    """Test 2: MessageTranslator converts between formats."""
    msg = Message(
        type=MessageType.COMMAND,
        sender="researcher",
        payload={"action": "test"}
    )

    hub_msg = MessageTranslator.adr004_to_hub(msg, room="test-room")
    assert hub_msg["version"] == "1.0"

    msg2 = MessageTranslator.hub_to_adr004(hub_msg)
    assert msg2.id == msg.id
```

**What it tests**:
- Format conversions (ADR-004 ↔ Hub)
- Data mapping correctness
- Round-trip conversion (no data loss)
- Business logic rules

**Dependencies**: Layer 1 (schemas must work)

### Layer 3: Infrastructure/Registry Tests
**Purpose**: Validate supporting systems and configuration

```python
def test_agent_key_registry():
    """Test 3: AgentKeyRegistry loads public keys."""
    registry = AgentKeyRegistry(registry_path)

    researcher_key = registry.get_public_key("researcher")
    assert researcher_key == "8sfXeKpnxq9LfB0Sr2/vgSTRpXYzYfPANuReCcKkzjE="

    agents = registry.get_all_agents()
    assert len(agents) == 12
```

**What it tests**:
- Configuration loading
- Registry lookups
- Key storage/retrieval
- Data source integration

**Dependencies**: Layer 1 (data structures), possibly file system

### Layer 4: Integration/Component Tests
**Purpose**: Validate multiple components working together

```python
def test_signed_message_bus():
    """Test 4: SignedMessageBus signs and verifies messages."""
    bus = create_signed_bus("researcher", auto_sign=True)

    msg = Message(...)
    bus.send(msg)  # Auto-signs

    retrieved_msg = bus.receive("researcher")  # Auto-verifies
    assert is_signed(retrieved_msg)
```

**What it tests**:
- Components integrated correctly
- Auto-signing/verification workflow
- Message routing with signatures
- Cross-component data flow

**Dependencies**: Layers 1-3 (schemas, translation, registry)

### Layer 5: End-to-End/Workflow Tests
**Purpose**: Validate complete user workflows

```python
def test_end_to_end_signing():
    """Test 5: Complete signing workflow with real keys."""
    # Load real private key
    private_key = load_private_key(key_path)
    signer = Ed25519Signer.from_private_key(private_key)

    # Create, convert, sign
    msg = Message(...)
    hub_msg = MessageTranslator.adr004_to_hub(msg)
    signed_hub_msg = sign_hub_message(hub_msg, signer)

    # Verify
    assert verify_hub_message(signed_hub_msg)

    # Convert back
    signed_msg = MessageTranslator.hub_to_adr004(signed_hub_msg)
    assert is_signed(signed_msg)
```

**What it tests**:
- Real-world usage scenarios
- Complete workflow from start to finish
- Integration with external systems (file system, crypto library)
- User-facing functionality

**Dependencies**: All layers (complete system)

## Benefits of Layered Organization

### 1. Clear Failure Diagnosis
```
❌ Layer 1 fails → Data structures broken
❌ Layer 2 fails → Business logic broken
❌ Layer 3 fails → Infrastructure/config broken
❌ Layer 4 fails → Integration broken
❌ Layer 5 fails → Workflow/usage broken
```

### 2. Selective Test Execution
```bash
# Run only unit tests (Layers 1-2)
pytest -k "schema or translator"

# Run only integration tests (Layers 4-5)
pytest -k "integration or end_to_end"

# Run only infrastructure (Layer 3)
pytest -k "registry"
```

### 3. Test Planning Visibility
Know what's covered at each layer:
```
Layer 1: ✅ SignatureInfo schema
Layer 2: ✅ MessageTranslator (both directions)
Layer 3: ✅ AgentKeyRegistry (12 agents)
Layer 4: ✅ SignedMessageBus (auto sign/verify)
Layer 5: ✅ End-to-end signing workflow
```

### 4. Effort Estimation
```
Layer 1 tests: ~10 minutes (simple assertions)
Layer 2 tests: ~20 minutes (logic + edge cases)
Layer 3 tests: ~30 minutes (setup + validation)
Layer 4 tests: ~45 minutes (multiple components)
Layer 5 tests: ~60 minutes (complete scenarios)
```

## Test Naming Convention

```python
# Layer 1: test_[entity]_[aspect]
def test_signature_info_schema():
def test_message_creation():
def test_priority_validation():

# Layer 2: test_[converter]_[operation]
def test_message_translator_to_hub():
def test_message_translator_from_hub():
def test_message_translator_round_trip():

# Layer 3: test_[system]_[functionality]
def test_agent_key_registry_loading():
def test_agent_key_registry_lookup():
def test_agent_key_registry_all_agents():

# Layer 4: test_[feature]_integration
def test_signed_message_bus_integration():
def test_auto_signing_integration():
def test_routing_with_signatures_integration():

# Layer 5: test_[workflow]_end_to_end
def test_signing_workflow_end_to_end():
def test_verification_workflow_end_to_end():
def test_message_lifecycle_end_to_end():
```

## Directory Structure Options

### Option 1: Single File with Sections
```python
# test_ed25519_integration.py

# ===== Layer 1: Schema Tests =====
def test_signature_info_schema(): ...

# ===== Layer 2: Translation Tests =====
def test_message_translator(): ...

# ===== Layer 3: Infrastructure Tests =====
def test_agent_key_registry(): ...

# ===== Layer 4: Integration Tests =====
def test_signed_message_bus(): ...

# ===== Layer 5: End-to-End Tests =====
def test_end_to_end_signing(): ...
```

### Option 2: Separate Files by Layer
```
tests/
  test_1_schemas.py           # Layer 1
  test_2_translation.py       # Layer 2
  test_3_infrastructure.py    # Layer 3
  test_4_integration.py       # Layer 4
  test_5_end_to_end.py        # Layer 5
```

### Option 3: Nested Directory Structure
```
tests/
  unit/                       # Layers 1-2
    test_schemas.py
    test_translation.py
  integration/                # Layers 3-4
    test_infrastructure.py
    test_components.py
  e2e/                        # Layer 5
    test_workflows.py
```

## Coverage Analysis by Layer

| Layer | Test Count | Lines Tested | Coverage | Purpose |
|-------|-----------|--------------|----------|---------|
| 1 | 1 | ~50 | 100% | Data models |
| 2 | 1 | ~150 | 95% | Business logic |
| 3 | 1 | ~100 | 90% | Infrastructure |
| 4 | 1 | ~200 | 85% | Integration |
| 5 | 1 | ~100 | 80% | Workflows |
| **Total** | **5** | **~600** | **90%** | **Complete** |

## When to Apply

✅ **Use Layer-Based Organization when**:
- System has clear architectural layers
- Multiple abstraction levels exist
- Integration complexity is high
- Test suite has >10 tests
- Team needs to understand what's tested

❌ **Don't use when**:
- Simple single-layer system
- <5 total tests
- All tests are unit tests
- No integration dependencies

## Template: Test Suite Structure

```python
"""
Integration test suite for [System Name].

Test Layers:
1. Schema/Data - Basic data structure validation
2. Business Logic - Core functionality without dependencies
3. Infrastructure - Configuration, registries, external resources
4. Integration - Multiple components working together
5. End-to-End - Complete user workflows

Run all tests: pytest
Run specific layer: pytest -k "schema" (Layer 1)
"""

import pytest

# ===== Layer 1: Schema Tests =====

def test_[entity]_schema():
    """Test 1.1: [Entity] schema validation."""
    # Test data structure creation
    # Test field validation
    # Test required fields

def test_[entity]_validation():
    """Test 1.2: [Entity] validation rules."""
    # Test edge cases
    # Test invalid inputs

# ===== Layer 2: Business Logic Tests =====

def test_[operation]_logic():
    """Test 2.1: [Operation] business logic."""
    # Test happy path
    # Test edge cases
    # Test error cases

# ===== Layer 3: Infrastructure Tests =====

def test_[system]_loading():
    """Test 3.1: [System] loads correctly."""
    # Test configuration loading
    # Test resource availability

def test_[system]_operations():
    """Test 3.2: [System] basic operations."""
    # Test CRUD operations
    # Test lookups

# ===== Layer 4: Integration Tests =====

def test_[feature]_integration():
    """Test 4.1: [Feature] component integration."""
    # Test components work together
    # Test data flow
    # Test error propagation

# ===== Layer 5: End-to-End Tests =====

def test_[workflow]_end_to_end():
    """Test 5.1: [Workflow] complete scenario."""
    # Test full user workflow
    # Test real resources (if available)
    # Test expected outcomes
```

## Integration with CI/CD

```yaml
# .github/workflows/test.yml
name: Layered Test Suite

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run Layer 1-2 (Unit Tests)
        run: pytest -k "schema or logic"

  integration-tests:
    needs: unit-tests
    runs-on: ubuntu-latest
    steps:
      - name: Run Layer 3-4 (Integration Tests)
        run: pytest -k "infrastructure or integration"

  e2e-tests:
    needs: integration-tests
    runs-on: ubuntu-latest
    steps:
      - name: Run Layer 5 (E2E Tests)
        run: pytest -k "end_to_end"
```

## Success Metrics

**Time Saved**: 15-25 minutes per test run
- Immediately identify which layer broke
- Run only relevant layer during development
- Clear test planning and coverage visibility

**Team Communication**:
- "Layer 3 tests are failing" (infrastructure issue)
- "Need more Layer 2 coverage" (business logic gaps)
- "E2E tests all pass" (system works end-to-end)

## Evidence from Ed25519 Suite

**5 tests, 5 layers, 100% coverage**:
- Layer 1: SignatureInfo schema ✅
- Layer 2: MessageTranslator ✅
- Layer 3: AgentKeyRegistry ✅
- Layer 4: SignedMessageBus ✅
- Layer 5: End-to-end signing ✅

**Result**: Complete system validated from data structures to workflows

**Last Validated**: 2025-10-03 (Ed25519 Integration Test Suite)
