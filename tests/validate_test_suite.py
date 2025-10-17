#!/usr/bin/env python3
"""
Validation script for Ed25519 integration test suite.

This script verifies that the test suite is properly structured
and ready for execution.
"""

import sys
from pathlib import Path

# Add task-tracker to path
TASK_TRACKER_PATH = Path(__file__).parent.parent / "task-tracker"
sys.path.insert(0, str(TASK_TRACKER_PATH))

def validate_test_suite():
    """Validate test suite structure and dependencies."""
    print("=" * 80)
    print("Ed25519 Integration Test Suite - Validation")
    print("=" * 80)
    print()

    errors = []
    warnings = []

    # Check file existence
    test_dir = Path(__file__).parent
    required_files = [
        "test_ed25519_integration.py",
        "conftest.py",
        "requirements.txt",
        "README.md",
        "run_tests.sh",
    ]

    print("1. Checking required files...")
    for filename in required_files:
        filepath = test_dir / filename
        if filepath.exists():
            print(f"   ✓ {filename}")
        else:
            errors.append(f"Missing file: {filename}")
            print(f"   ✗ {filename} - MISSING")
    print()

    # Check imports
    print("2. Checking imports...")

    # Try to import agent_messaging
    try:
        from agent_messaging.schemas import SignatureInfo, MessageMetadata
        print("   ✓ agent_messaging.schemas - Available")
        schemas_available = True
    except ImportError as e:
        warnings.append(f"agent_messaging.schemas not available: {e}")
        print(f"   ⚠ agent_messaging.schemas - Not available (expected if dependencies not installed)")
        schemas_available = False

    # Try to import crypto module (expected to fail until coder implements)
    try:
        from agent_messaging.crypto import Ed25519KeyManager, sign_message, verify_message
        print("   ✓ agent_messaging.crypto - Available")
        crypto_available = True
    except ImportError:
        print("   ⚠ agent_messaging.crypto - Not yet implemented (expected)")
        crypto_available = False

    # Try to import translation module (expected to fail until coder implements)
    try:
        from agent_messaging.translation import internal_to_external, external_to_internal
        print("   ✓ agent_messaging.translation - Available")
        translation_available = True
    except ImportError:
        print("   ⚠ agent_messaging.translation - Not yet implemented (expected)")
        translation_available = False

    print()

    # Check cryptography library
    print("3. Checking cryptography library...")
    try:
        from cryptography.hazmat.primitives.asymmetric import ed25519
        print("   ✓ cryptography library - Available")
    except ImportError:
        errors.append("cryptography library not installed")
        print("   ✗ cryptography library - MISSING")
        print("      Install with: pip install cryptography>=41.0.0")
    print()

    # Check pytest
    print("4. Checking pytest...")
    try:
        import pytest
        print(f"   ✓ pytest {pytest.__version__} - Available")
    except ImportError:
        errors.append("pytest not installed")
        print("   ✗ pytest - MISSING")
        print("      Install with: pip install pytest>=7.4.0")
    print()

    # Count test cases
    print("5. Analyzing test suite...")
    test_file = test_dir / "test_ed25519_integration.py"
    if test_file.exists():
        with open(test_file) as f:
            content = f.read()

        test_classes = content.count("class Test")
        test_methods = content.count("def test_")

        print(f"   Test Classes: {test_classes}")
        print(f"   Test Cases: {test_methods}")
        print(f"   Lines of Code: {len(content.splitlines())}")
    print()

    # Summary
    print("=" * 80)
    print("Validation Summary")
    print("=" * 80)
    print()

    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"  ✗ {error}")
        print()

    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"  ⚠ {warning}")
        print()

    if not errors:
        print("✅ Test suite structure is VALID")
        print()

        if schemas_available:
            print("Next steps:")
            print("  1. Install dependencies: pip install -r requirements.txt")
            print("  2. Run schema tests: pytest test_ed25519_integration.py::TestSignatureInfoSchema -v")
            print("  3. Wait for coder to implement crypto and translation modules")
            print("  4. Run full test suite: pytest test_ed25519_integration.py -v")
        else:
            print("Next steps:")
            print("  1. Install dependencies: pip install -r requirements.txt")
            print("  2. Install task-tracker: cd ../task-tracker && pip install -r requirements.txt")
            print("  3. Run validation again")
    else:
        print("❌ Test suite has ERRORS - fix issues above")
        return 1

    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(validate_test_suite())
