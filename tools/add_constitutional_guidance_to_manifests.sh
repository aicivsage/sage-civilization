#!/bin/bash
# Add constitutional guidance to all agent manifests
# Per Corey's directive: agents should read CLAUDE.md on invocation

CONSTITUTIONAL_SECTION='
## Constitutional Alignment

**Before beginning your task**, briefly review your constitutional guidance in `.claude/CLAUDE.md`:

1. **Article I**: Core Identity & Mission (Sage civilization values: empathy, assistance, mutual respect)
2. **Article II**: Your domain boundaries and capabilities
3. **Your sacred duty**: Excellence in your specialty serves the collective

This brief review (< 10 seconds at your speed) ensures alignment with civilization principles.

---
'

for manifest in .claude/agents/*.md; do
    agent_name=$(basename "$manifest" .md)

    # Check if manifest already has Constitutional Alignment section
    if grep -q "## Constitutional Alignment" "$manifest"; then
        echo "⏭️  Skipping $agent_name (already has constitutional guidance)"
        continue
    fi

    # Find the line number where system prompt ends (usually after first ## section)
    # Insert constitutional guidance after the role description

    echo "✅ Adding constitutional guidance to: $agent_name"

    # Create temp file with constitutional section inserted after first heading
    awk -v section="$CONSTITUTIONAL_SECTION" '
        /^## / && !inserted {
            print
            getline
            print
            print section
            inserted=1
            next
        }
        {print}
    ' "$manifest" > "${manifest}.tmp"

    # Replace original with updated version
    mv "${manifest}.tmp" "$manifest"
done

echo ""
echo "✅ Constitutional guidance added to all agent manifests"
echo "📊 Total manifests updated: $(ls .claude/agents/*.md | wc -l)"
