#!/bin/bash
#
# Test runner script for Ed25519 integration tests
# Usage: ./run_tests.sh [options]
#

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=================================================="
echo "Ed25519 Integration Test Suite"
echo "=================================================="
echo ""

# Check if pytest is installed
if ! python3 -m pytest --version &> /dev/null; then
    echo "ERROR: pytest not found. Installing test dependencies..."
    pip3 install -r "$SCRIPT_DIR/requirements.txt"
fi

# Add task-tracker to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT/task-tracker:$PYTHONPATH"

# Parse command-line arguments
TEST_TARGET="${1:-test_ed25519_integration.py}"
PYTEST_ARGS="${@:2}"

# Default args if none provided
if [ -z "$PYTEST_ARGS" ]; then
    PYTEST_ARGS="-v"
fi

echo "Running tests: $TEST_TARGET"
echo "Pytest args: $PYTEST_ARGS"
echo ""

# Run tests
cd "$SCRIPT_DIR"
python3 -m pytest "$TEST_TARGET" $PYTEST_ARGS

echo ""
echo "=================================================="
echo "Test run complete"
echo "=================================================="
