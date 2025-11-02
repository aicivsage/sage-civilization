#!/bin/bash

# Session Wakeup Helper V2 - Sage Civilization
# Helps Primary AI find most recent context quickly
# Enhanced with: status file scanning, staleness warnings, git log, registry age checks

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=== Sage Civilization Session Wakeup Helper V2 ==="
echo ""

# 1. Check for most recent handoff
echo "📋 RECENT HANDOFF:"
if [ -f "memories/system/HANDOFF_REGISTRY.json" ]; then
    MOST_RECENT=$(cat memories/system/HANDOFF_REGISTRY.json | grep -o '"most_recent":[^,]*' | cut -d'"' -f4)
    LAST_UPDATED=$(cat memories/system/HANDOFF_REGISTRY.json | grep -o '"last_updated":[^,]*' | cut -d'"' -f4)

    if [ -n "$MOST_RECENT" ] && [ -f "$MOST_RECENT" ]; then
        echo "   ✓ Registry found: $MOST_RECENT"

        # Check registry age
        if [ -n "$LAST_UPDATED" ]; then
            REGISTRY_EPOCH=$(date -d "$LAST_UPDATED" +%s 2>/dev/null)
            NOW_EPOCH=$(date +%s)
            AGE_HOURS=$(( ($NOW_EPOCH - $REGISTRY_EPOCH) / 3600 ))

            if [ $AGE_HOURS -gt 2 ]; then
                echo -e "   ${RED}🚨 WARNING: Registry is $AGE_HOURS hours old (>2 hours)${NC}"
                echo "   → Check for recent work that may not be in handoff!"
            elif [ $AGE_HOURS -eq 0 ]; then
                echo -e "   ${GREEN}✓ Registry fresh (updated this hour)${NC}"
            else
                echo "   ✓ Registry age: $AGE_HOURS hour(s)"
            fi
        fi

        HANDOFF_DATE=$(basename "$MOST_RECENT" | grep -o '[0-9]\{8\}-[0-9]\{4\}')
        if [ -n "$HANDOFF_DATE" ]; then
            echo "   Date: ${HANDOFF_DATE:0:4}-${HANDOFF_DATE:4:2}-${HANDOFF_DATE:6:2} ${HANDOFF_DATE:9:2}:${HANDOFF_DATE:11:2}"
        fi

        echo ""
        echo "   Preview:"
        head -30 "$MOST_RECENT" | grep -E "(Session Duration|Primary Focus|Status|What Was|Completed|Current priority)" | sed 's/^/     /'
    else
        echo -e "   ${YELLOW}⚠️  Registry exists but handoff file not found${NC}"
        echo "   Searching for recent handoff files..."
        FALLBACK=$(ls -t SESSION-HANDOFF-*.md 2>/dev/null | head -1)
        if [ -n "$FALLBACK" ]; then
            echo "   Found: $FALLBACK"
        else
            echo "   ❌ No handoff files found"
        fi
    fi
else
    echo -e "   ${YELLOW}⚠️  No registry found, searching for handoff files...${NC}"
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
echo "🔍 RECENT STATUS FILES (Last 3 hours):"
RECENT_STATUS=$(find . -maxdepth 1 -name "*STATUS*.md" -mmin -180 -type f 2>/dev/null | sort -r)
if [ -n "$RECENT_STATUS" ]; then
    echo "$RECENT_STATUS" | while read -r file; do
        MODIFIED=$(stat -c %y "$file" 2>/dev/null | cut -d' ' -f1,2 | cut -d'.' -f1)
        echo -e "   ${BLUE}→${NC} $file (modified: $MODIFIED)"
    done
else
    echo "   ✓ No recent status files (last 3 hours)"
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
            echo -e "   ${RED}🚨 WARNING: $AGE_DAYS days old (>3 days = potentially stale)${NC}"
            echo "   → Prioritize handoff information over MASTER_TODO"
        elif [ $AGE_DAYS -eq 0 ]; then
            echo -e "   ${GREEN}✓ Fresh (updated today)${NC}"
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
echo "🔧 GIT ACTIVITY (Last 3 hours):"
RECENT_COMMITS=$(git log --since="3 hours ago" --oneline 2>/dev/null)
if [ -n "$RECENT_COMMITS" ]; then
    echo "$RECENT_COMMITS" | head -5 | sed 's/^/   /'
    COMMIT_COUNT=$(echo "$RECENT_COMMITS" | wc -l)
    if [ $COMMIT_COUNT -gt 5 ]; then
        echo "   ... and $(($COMMIT_COUNT - 5)) more commits"
    fi
else
    echo "   ✓ No commits in last 3 hours"
fi

echo ""
echo "💬 TELEGRAM STATUS:"
if pgrep -f "telegram_bridge.py" > /dev/null; then
    echo -e "   ${GREEN}✓ Telegram bridge running (inbound: Telegram → tmux)${NC}"
else
    echo -e "   ${YELLOW}⚠️  Telegram bridge not running${NC}"
    echo "      Fix: bash tools/fix_telegram_session.sh"
fi

if pgrep -f "telegram_jsonl_monitor.py" > /dev/null; then
    echo -e "   ${GREEN}✓ JSONL monitor running (outbound: wrapped messages → Telegram)${NC}"
else
    echo -e "   ${YELLOW}⚠️  JSONL monitor not running${NC}"
    echo "      Fix: bash tools/telegram_boot.sh"
fi

echo ""
echo "📧 RECENT COMMUNICATIONS:"
echo "   Run: Task(human-liaison) + Task(comms-hub) to check inbox + Weaver messages"

echo ""
echo "✅ RECOMMENDED STARTUP SEQUENCE:"
echo "   1. Send Telegram session start (WRAPPED - MANDATORY):"
echo "      🤖🎯📱"
echo "      Primary AI online - loading context from [handoff]"
echo "      Checking inbox, will report status in 5 min"
echo "      ✨🔚"
echo ""
echo "      Quick: source tools/telegram_templates.sh && tg_session_start"
echo ""
echo "   2. Read .claude/CLAUDE.md (identity)"
echo "   3. Read most recent handoff (shown above)"
echo "   4. Scan status files + git log (shown above)"
echo "   5. Read MASTER_TODO for long-term context (check age warning)"
echo "   6. Check communications (email + comms-hub)"
echo "   7. Invoke primary-helper with context summary for verification"
echo ""
echo "   8. Send day start email (if first session of day):"
echo "      python3 tools/send_day_start_email.py"
echo "      (Checks state file, sends only once per day)"
echo ""
echo "   9. Send Telegram context loaded (WRAPPED - MANDATORY):"
echo "      🤖🎯📱"
echo "      Context loaded - Handoff: [name] - Next: [priority] - Ready!"
echo "      ✨🔚"
echo ""
echo "      Quick: tg_context_loaded \"[handoff]\" \"[priority]\""
echo ""
echo "   10. Begin work"
echo ""
echo "📖 TELEGRAM PROTOCOL:"
echo "   🚨 ALWAYS wrap session summaries with emoji markers"
echo "   Start: 🤖🎯📱"
echo "   End:   ✨🔚"
echo "   Why: Monitor auto-sends wrapped messages to Greg's phone"
echo "   Reference: PRIMARY-TELEGRAM-QUICK-REFERENCE.md"
echo "   Templates: tools/telegram_templates.sh (all 6 functions include wrappers)"

echo ""
echo "=== End Wakeup Helper V2 ==="
