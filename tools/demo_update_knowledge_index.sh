#!/bin/bash
# Demonstration script for update_knowledge_index.py

set -e

BASE_DIR="/home/corey/projects/AI-CIV/grow_gemini_deepresearch"
TOOL="$BASE_DIR/tools/update_knowledge_index.py"
INDEX="$BASE_DIR/memories/knowledge/INDEX.md"

echo "============================================"
echo "Knowledge Index Update Tool - Demo"
echo "============================================"
echo

# 1. Show current status
echo "1. Current Index Status:"
echo "----------------------------------------"
if [ -f "$INDEX" ]; then
    LAST_UPDATE=$(grep "LAST_UPDATE" "$INDEX" | head -1)
    echo "   $LAST_UPDATE"
    echo "   File size: $(du -h "$INDEX" | cut -f1)"
    echo "   Lines: $(wc -l < "$INDEX")"
else
    echo "   Index does not exist yet"
fi
echo

# 2. Run dry-run mode
echo "2. Running in DRY-RUN mode (preview changes):"
echo "----------------------------------------"
python3 "$TOOL" --dry-run | head -20
echo "   ... (truncated output)"
echo

# 3. Run actual update
echo "3. Running actual update:"
echo "----------------------------------------"
python3 "$TOOL"
echo

# 4. Show what changed
echo "4. Index Statistics:"
echo "----------------------------------------"
echo "   ADRs: $(grep -c "ADR-" "$INDEX" || true)"
echo "   Tools: $(grep -c "\[.*\](../tools/" "$INDEX" || true)"
echo "   Flows: $(grep -c "flows/.*\.yaml" "$INDEX" || true)"
echo

# 5. Demonstrate preservation of curated content
echo "5. Curated Sections (preserved by tool):"
echo "----------------------------------------"
echo "   Navigation section:"
grep -A 5 "CURATED:NAVIGATION:START" "$INDEX" | sed 's/^/      /'
echo
echo "   Search tips section:"
grep -A 3 "CURATED:TIPS:START" "$INDEX" | sed 's/^/      /'
echo

# 6. Show incremental mode
echo "6. Running incremental update (faster):"
echo "----------------------------------------"
python3 "$TOOL" --incremental
echo

echo "============================================"
echo "Demo Complete!"
echo "============================================"
echo
echo "Next steps:"
echo "  - View full index: cat $INDEX"
echo "  - Add to cron: 0 2 * * * python3 $TOOL --incremental"
echo "  - Customize curated sections in INDEX.md"
echo
