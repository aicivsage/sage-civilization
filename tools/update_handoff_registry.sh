#!/bin/bash
# Update HANDOFF_REGISTRY.json with new handoff/status document
# Usage: ./tools/update_handoff_registry.sh /path/to/handoff.md
#
# This ensures the registry NEVER lags behind real work
# Call this IMMEDIATELY after creating any handoff/status document

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REGISTRY="$PROJECT_ROOT/memories/system/HANDOFF_REGISTRY.json"

# Validate input
if [ $# -eq 0 ]; then
    echo "❌ Error: No handoff path provided"
    echo "Usage: $0 /path/to/handoff.md"
    exit 1
fi

HANDOFF_PATH="$1"

# Convert to absolute path if relative
if [[ "$HANDOFF_PATH" != /* ]]; then
    HANDOFF_PATH="$PROJECT_ROOT/$HANDOFF_PATH"
fi

# Validate handoff file exists
if [ ! -f "$HANDOFF_PATH" ]; then
    echo "❌ Error: Handoff file not found: $HANDOFF_PATH"
    exit 1
fi

# Validate registry exists
if [ ! -f "$REGISTRY" ]; then
    echo "❌ Error: Registry not found: $REGISTRY"
    exit 1
fi

# Get timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Update registry with new most_recent pointer
echo "📝 Updating registry..."
jq --arg path "$HANDOFF_PATH" --arg ts "$TIMESTAMP" \
  '.most_recent = $path | .last_updated = $ts' \
  "$REGISTRY" > "$REGISTRY.tmp"

# Atomic move
mv "$REGISTRY.tmp" "$REGISTRY"

echo "✅ Registry updated"
echo "   Most recent: $HANDOFF_PATH"
echo "   Timestamp: $TIMESTAMP"
echo ""
echo "Registry is now synchronized with real work."
