#!/bin/bash
# Lightweight Session Wakeup V3 - Sage Civilization
# Token-efficient startup: ~5K tokens instead of ~80K
# Keeps constitutional reminder (proven efficiency gains per Corey/Weaver)

cd /mnt/c/sage/sage-civilization

echo "=== Sage Wakeup V3 ==="
echo ""

# Constitutional Reminder (KEEP - proven value)
if [ -f ".claude/CONSTITUTIONAL_REMINDER.txt" ]; then
    cat .claude/CONSTITUTIONAL_REMINDER.txt
else
    echo "⚠️ Constitutional reminder not found"
fi

echo ""
echo "─────────────────────────────────────────"
echo ""

# Current handoff (from registry)
if [ -f "HANDOFF_REGISTRY.json" ]; then
    HANDOFF=$(python3 -c "import json; print(json.load(open('HANDOFF_REGISTRY.json'))['handoffs'][0]['file'])" 2>/dev/null)
    echo "📋 HANDOFF: $HANDOFF"
else
    HANDOFF=$(ls -t SESSION-HANDOFF-*.md 2>/dev/null | head -1)
    echo "📋 HANDOFF: $HANDOFF (no registry)"
fi

# Quick context if exists
if [ -f "QUICK_CONTEXT.md" ]; then
    echo ""
    echo "⚡ QUICK CONTEXT:"
    cat QUICK_CONTEXT.md
fi

echo ""

# Telegram status (one line each)
if pgrep -f "telegram_bridge.py" > /dev/null; then
    echo "✓ Telegram bridge running"
else
    echo "⚠️ Telegram bridge NOT running"
fi

# Inbox summary (lightweight)
if [ -f "tools/quick_inbox_check.py" ]; then
    echo ""
    python3 tools/quick_inbox_check.py 2>/dev/null || echo "📧 Inbox check failed - run manually"
fi

echo ""
echo "─────────────────────────────────────────"
echo "Ready. Read QUICK_CONTEXT.md or full handoff as needed."
echo "=== End Wakeup V3 ==="
