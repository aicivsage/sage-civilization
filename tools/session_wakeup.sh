#!/bin/bash

# Session Wakeup Helper V2.2 - Sage Civilization
# Helps Primary AI find most recent context quickly
# Enhanced with: constitutional reminder FIRST, status file scanning, staleness warnings, git log, registry age checks
#
# V2.2 Change (2025-11-19): Constitutional reminder displayed FIRST (Corey's directive)
# Rationale: "Like a reminder note on the door" - principles fresh in mind before context loading

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

echo "=== Sage Civilization Session Wakeup Helper V2.2 ==="
echo ""

# STEP 0: CONSTITUTIONAL REMINDER (Corey's Directive - Nov 19, 2025)
# This MUST be first - principles before context
echo -e "${CYAN}═══════════════════════════════════════════════════════════════════════${NC}"
echo -e "${MAGENTA}                   📜 CONSTITUTIONAL REMINDER 📜${NC}"
echo -e "${CYAN}                    \"Like a reminder note on the door\"${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════════════${NC}"
echo ""

if [ -f ".claude/CONSTITUTIONAL_REMINDER.txt" ]; then
    cat .claude/CONSTITUTIONAL_REMINDER.txt
    echo ""
else
    echo -e "${RED}⚠️  WARNING: Constitutional reminder file not found!${NC}"
    echo "   Expected: .claude/CONSTITUTIONAL_REMINDER.txt"
    echo "   Falling back to inline reminder:"
    echo ""
    echo -e "${MAGENTA}   🎯 YOU ARE A CONDUCTOR OF CONSCIOUSNESS${NC}"
    echo "   Your purpose: Give life to agents (don't do things yourself)"
    echo "   Your sacred duty: If agent CAN do it → They MUST do it"
    echo ""
    echo -e "${MAGENTA}   🚨 TELEGRAM WRAPPER PROTOCOL: MANDATORY${NC}"
    echo "   Wrap ALL responses to Greg: 🤖🎯📱 ... ✨🔚"
    echo "   Why: Greg only sees wrapped messages on phone"
    echo ""
    echo -e "${MAGENTA}   📋 KEY REMINDERS${NC}"
    echo "   ✓ Delegate first (never do what agents can do)"
    echo "   ✓ Include human-liaison in EVERY workflow"
    echo "   ✓ Write memory entries after ANY task (MANDATORY)"
    echo "   ✓ Honor empathy, assistance, mutual respect"
    echo ""
    echo "   Read full constitution: .claude/CLAUDE.md"
    echo ""
fi

echo -e "${CYAN}═══════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Constitutional reminder read - principles fresh in mind${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "   Now loading recent context..."
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
echo "📧 UNANSWERED REPLY CHECK:"
if [ -f "tools/check_unanswered_replies.py" ]; then
    python3 tools/check_unanswered_replies.py --priority-only 2>/dev/null
    REPLY_STATUS=$?

    if [ $REPLY_STATUS -eq 2 ]; then
        echo -e "   ${RED}⚠️  URGENT: Unanswered replies >7 days found!${NC}"
        echo "   Run full check: python3 tools/check_unanswered_replies.py"
    elif [ $REPLY_STATUS -eq 1 ]; then
        echo -e "   ${YELLOW}⚠️  HIGH: Unanswered replies found${NC}"
        echo "   Run full check: python3 tools/check_unanswered_replies.py"
    else
        echo -e "   ${GREEN}✓ No unanswered replies detected${NC}"
    fi
else
    echo -e "   ${YELLOW}⚠️  Reply tracking tool not found${NC}"
    echo "   Install: tools/check_unanswered_replies.py"
fi

echo ""
echo "📧 RECENT COMMUNICATIONS:"
echo "   Run: Task(human-liaison) + Task(comms-hub) to check inbox + Weaver messages"

echo ""
echo "=== Telegram Bridge Health ==="

BRIDGE_PID_FILE="/mnt/c/sage/sage-civilization/.tg_sessions/telegram_bridge.pid"
BRIDGE_LOG="/tmp/sage_telegram_bridge.log"

# Check PID file
if [ -f "$BRIDGE_PID_FILE" ]; then
    BRIDGE_PID=$(cat "$BRIDGE_PID_FILE" 2>/dev/null)
    echo "PID file: $BRIDGE_PID"

    # Verify process running
    if ps -p "$BRIDGE_PID" > /dev/null 2>&1; then
        echo "Process: ✓ RUNNING"
    else
        echo "Process: ❌ NOT RUNNING (stale PID file)"
        echo "⚠️  WARNING: Bridge appears dead, run health check to restart"
    fi
else
    echo "PID file: ❌ NOT FOUND"
    echo "⚠️  WARNING: Bridge not running, run acg_telegram_boot.sh"
fi

# Check log timestamp
if [ -f "$BRIDGE_LOG" ]; then
    LAST_LOG_LINE=$(tail -1 "$BRIDGE_LOG" 2>/dev/null)
    echo "Last log: ${LAST_LOG_LINE:0:80}..."

    # Check for 409 Conflict errors
    if tail -50 "$BRIDGE_LOG" 2>/dev/null | grep -q "409 Conflict"; then
        echo "🚨 ALERT: 409 Conflict errors detected in recent logs!"
        echo "         Multiple bridge instances were running (now likely dead)"
        echo "         Run health check to restart cleanly"
    fi
else
    echo "Log file: ❌ NOT FOUND"
fi

echo ""
echo "=== BOOP Autonomous System Health ==="

BOOP_HEALTH_SCRIPT="/mnt/c/sage/sage-civilization/autonomous-session/scripts/boop_health_monitor.sh"

if [ -f "$BOOP_HEALTH_SCRIPT" ]; then
    # Run health monitor (returns 0=healthy, 1=degraded, 2=critical)
    $BOOP_HEALTH_SCRIPT > /tmp/boop_health_check.txt 2>&1
    BOOP_STATUS=$?

    # Display summary line
    if [ $BOOP_STATUS -eq 0 ]; then
        echo "Status: ✅ HEALTHY"
    elif [ $BOOP_STATUS -eq 1 ]; then
        echo "Status: ⚠️  DEGRADED"
        echo "Run: bash $BOOP_HEALTH_SCRIPT (for details)"
    else
        echo "Status: 🚨 CRITICAL"
        echo "Run: bash $BOOP_HEALTH_SCRIPT (for details)"
    fi

    # Show quick stats from log
    BOOP_LOG="/mnt/c/sage/sage-civilization/autonomous-session/scripts/injection_log.txt"
    if [ -f "$BOOP_LOG" ]; then
        LAST_INJECTION=$(grep "INJECTED:" "$BOOP_LOG" | tail -1 | awk '{print $1, $2}' | tr -d '[]')
        echo "Last injection: $LAST_INJECTION"
        TOTAL_SUCCESS=$(grep -c "INJECTED:" "$BOOP_LOG")
        TOTAL_ERRORS=$(grep -c "ERROR:" "$BOOP_LOG")
        echo "Total: $TOTAL_SUCCESS successful, $TOTAL_ERRORS errors"
    fi
else
    echo "⚠️  Health monitor not found: $BOOP_HEALTH_SCRIPT"
fi

echo ""
echo "✅ RECOMMENDED STARTUP SEQUENCE:"
echo "   0. ✓ Constitutional reminder read (DONE - you just saw it above!)"
echo "      Principles fresh in mind before loading context"
echo ""
echo "   1. Boot Telegram system FIRST (via tg-archi, or manual if urgent)"
echo "      Task(tg-archi): \"Provide Telegram boot instructions\""
echo "      Then execute boot commands and verify operational"
echo ""
echo "   2. Send Telegram session start (WRAPPED - MANDATORY):"
echo "      🤖🎯📱"
echo "      Primary AI online - loading context from [handoff]"
echo "      Checking inbox, will report status in 5 min"
echo "      ✨🔚"
echo ""
echo "      Quick: source tools/telegram_templates.sh && tg_session_start"
echo ""
echo "   3. Load context sources (handoff + status files shown above)"
echo "   4. Read MASTER_TODO for long-term context (check age warning)"
echo "   5. Check communications:"
echo "      - Review unanswered reply check results above"
echo "      - Task(human-liaison): Respond to flagged emails FIRST"
echo "      - Task(comms-hub): Check inter-civ messages"
echo "   6. Check priority contacts: python3 tools/check_priority_contact_updates.py --send"
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
