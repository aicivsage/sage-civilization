#!/bin/bash

# Session Wakeup Helper
# Helps Primary AI find most recent context quickly

echo "=== A-C-Gee Session Wakeup Helper ==="
echo ""

# 1. Check for most recent handoff
echo "📋 RECENT HANDOFF:"
if [ -f "memories/system/HANDOFF_REGISTRY.json" ]; then
    MOST_RECENT=$(cat memories/system/HANDOFF_REGISTRY.json | grep -o '"most_recent":[^,]*' | cut -d'"' -f4)
    if [ -n "$MOST_RECENT" ] && [ -f "$MOST_RECENT" ]; then
        echo "   ✓ Registry found: $MOST_RECENT"
        HANDOFF_DATE=$(basename "$MOST_RECENT" | grep -o '[0-9]\{8\}-[0-9]\{4\}')
        echo "   Date: ${HANDOFF_DATE:0:4}-${HANDOFF_DATE:4:2}-${HANDOFF_DATE:6:2} ${HANDOFF_DATE:9:2}:${HANDOFF_DATE:11:2}"
        echo ""
        echo "   Preview:"
        head -30 "$MOST_RECENT" | grep -E "(Session Duration|Primary Focus|Status|What Was|Completed|Current priority)" | sed 's/^/     /'
    else
        echo "   ⚠️  Registry exists but handoff file not found"
        echo "   Searching for recent handoff files..."
        FALLBACK=$(ls -t SESSION-HANDOFF-*.md 2>/dev/null | head -1)
        if [ -n "$FALLBACK" ]; then
            echo "   Found: $FALLBACK"
        else
            echo "   ❌ No handoff files found"
        fi
    fi
else
    echo "   ⚠️  No registry found, searching for handoff files..."
    RECENT_HANDOFF=$(ls -t SESSION-HANDOFF-*.md 2>/dev/null | head -1)
    if [ -n "$RECENT_HANDOFF" ]; then
        echo "   Found: $RECENT_HANDOFF"
    else
        echo "   Searching for other summary files..."
        RECENT_SUMMARY=$(ls -t *HANDOFF*.md *COMPLETE*.md 2>/dev/null | head -1)
        if [ -n "$RECENT_SUMMARY" ]; then
            echo "   Found: $RECENT_SUMMARY"
        else
            echo "   ❌ No recent handoff or summary files found"
        fi
    fi
fi

echo ""
echo "📝 MASTER TODO STATUS:"
if [ -f "memories/system/MASTER_TODO_LIST.md" ]; then
    LAST_UPDATED=$(grep "Last Updated" memories/system/MASTER_TODO_LIST.md | head -1)
    echo "   $LAST_UPDATED"

    # Calculate age
    TODO_DATE=$(echo "$LAST_UPDATED" | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}')
    if [ -n "$TODO_DATE" ]; then
        TODO_EPOCH=$(date -d "$TODO_DATE" +%s 2>/dev/null)
        NOW_EPOCH=$(date +%s)
        AGE_DAYS=$(( ($NOW_EPOCH - $TODO_EPOCH) / 86400 ))

        if [ $AGE_DAYS -gt 3 ]; then
            echo "   🚨 WARNING: $AGE_DAYS days old (>3 days = potentially stale)"
            echo "   → Prioritize handoff information over MASTER_TODO"
        elif [ $AGE_DAYS -eq 0 ]; then
            echo "   ✓ Fresh (updated today)"
        else
            echo "   ✓ Recent ($AGE_DAYS days old)"
        fi
    fi

    echo ""
    echo "   Current Priority:"
    sed -n '/## 🎯 CURRENT PRIORITY/,/##/p' memories/system/MASTER_TODO_LIST.md | head -10 | tail -8 | sed 's/^/     /'
else
    echo "   ❌ MASTER_TODO_LIST.md not found"
fi

echo ""
echo "📧 RECENT COMMUNICATIONS:"
echo "   Run: Task(human-liaison) + Task(comms-hub) to check inbox + Weaver messages"

echo ""
echo "✅ RECOMMENDED STARTUP SEQUENCE:"
echo "   1. Read .claude/CLAUDE.md (identity)"
echo "   2. Read most recent handoff (shown above)"
echo "   3. Read MASTER_TODO for long-term context (check age warning)"
echo "   4. Check communications (email + comms-hub)"
echo "   5. Synthesize status and report to Corey"

echo ""
echo "=== End Wakeup Helper ==="
