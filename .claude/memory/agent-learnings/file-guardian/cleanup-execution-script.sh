#!/bin/bash
# File System Cleanup Execution Script
# Generated: 2025-10-18 by file-guardian
# Purpose: Execute the cleanup plan for Oct 18 files

set -e  # Exit on error

WORKSPACE="/home/corey/projects/AI-CIV/grow_gemini_deepresearch"
cd "$WORKSPACE"

echo "=== Phase 1: Create Archive Structure ==="
mkdir -p archive/2025-10-18-telegram-restoration
mkdir -p archive/2025-10-18-spawn-work
mkdir -p archive/handoffs
echo "Directories created."

echo ""
echo "=== Phase 2: Archive Files (17 total) ==="

# Telegram restoration work (12 files)
echo "Moving Telegram restoration files..."
mv TELEGRAM-RESTORATION-REPORT.md archive/2025-10-18-telegram-restoration/ 2>/dev/null || echo "  - TELEGRAM-RESTORATION-REPORT.md already moved or missing"
mv TELEGRAM-RESTART-NOT-ROLLBACK.md archive/2025-10-18-telegram-restoration/ 2>/dev/null || echo "  - TELEGRAM-RESTART-NOT-ROLLBACK.md already moved or missing"
mv TELEGRAM-MONITOR-FIX-REPORT-20251018.md archive/2025-10-18-telegram-restoration/ 2>/dev/null || echo "  - TELEGRAM-MONITOR-FIX-REPORT-20251018.md already moved or missing"
mv TELEGRAM-MONITOR-FIXED-READY-TO-RESTART.md archive/2025-10-18-telegram-restoration/ 2>/dev/null || echo "  - TELEGRAM-MONITOR-FIXED-READY-TO-RESTART.md already moved or missing"
mv TELEGRAM-BEFORE-AFTER-GUIDE.md archive/2025-10-18-telegram-restoration/ 2>/dev/null || echo "  - TELEGRAM-BEFORE-AFTER-GUIDE.md already moved or missing"
mv TG-ARCHI-INFRASTRUCTURE-HARDENING-20251018.md archive/2025-10-18-telegram-restoration/ 2>/dev/null || echo "  - TG-ARCHI-INFRASTRUCTURE-HARDENING-20251018.md already moved or missing"
mv TG-ARCHI-STATUS-REPORT-20251018.md archive/2025-10-18-telegram-restoration/ 2>/dev/null || echo "  - TG-ARCHI-STATUS-REPORT-20251018.md already moved or missing"
mv TG-ARCHI-MONITOR-FIX-20251018.md archive/2025-10-18-telegram-restoration/ 2>/dev/null || echo "  - TG-ARCHI-MONITOR-FIX-20251018.md already moved or missing"
mv TG-ARCHI-TEACHING-REPORT-20251018.md archive/2025-10-18-telegram-restoration/ 2>/dev/null || echo "  - TG-ARCHI-TEACHING-REPORT-20251018.md already moved or missing"
mv GIT-SPECIALIST-TELEGRAM-ROLLBACK-ANALYSIS.md archive/2025-10-18-telegram-restoration/ 2>/dev/null || echo "  - GIT-SPECIALIST-TELEGRAM-ROLLBACK-ANALYSIS.md already moved or missing"
mv MONITOR-FIX-APPLIED.md archive/2025-10-18-telegram-restoration/ 2>/dev/null || echo "  - MONITOR-FIX-APPLIED.md already moved or missing"
mv VERIFICATION-CHECKLIST-MONITOR-FIXES.md archive/2025-10-18-telegram-restoration/ 2>/dev/null || echo "  - VERIFICATION-CHECKLIST-MONITOR-FIXES.md already moved or missing"

# Spawn work (2 files)
echo "Moving spawn work files..."
mv HEALTH-BOT-SETUP-COMPLETE.md archive/2025-10-18-spawn-work/ 2>/dev/null || echo "  - HEALTH-BOT-SETUP-COMPLETE.md already moved or missing"
mv SPAWN-PRIMARY-HELPER-INCOMPLETE.md archive/2025-10-18-spawn-work/ 2>/dev/null || echo "  - SPAWN-PRIMARY-HELPER-INCOMPLETE.md already moved or missing"

# Handoffs (3 files)
echo "Moving old handoff files..."
mv SESSION-HANDOFF-20251018-PRE-REBOOT.md archive/handoffs/ 2>/dev/null || echo "  - SESSION-HANDOFF-20251018-PRE-REBOOT.md already moved or missing"
mv SESSION-HANDOFF-20251018-POST-SPAWN.md archive/handoffs/ 2>/dev/null || echo "  - SESSION-HANDOFF-20251018-POST-SPAWN.md already moved or missing"
mv SESSION-HANDOFF-20251018-GREG-SPAWN-HEALTH-BOT.md archive/handoffs/ 2>/dev/null || echo "  - SESSION-HANDOFF-20251018-GREG-SPAWN-HEALTH-BOT.md already moved or missing"

echo ""
echo "=== Phase 3: Delete Redundant Files (3 total) ==="
rm -f RESTORE-TELEGRAM-QUICKSTART.md
rm -f SPAWN-HANDOFF.md
rm -f PRIMARY-HELPER-SPAWN-STATUS.md
echo "Redundant files deleted."

echo ""
echo "=== Phase 4: Verification ==="
ROOT_MD_COUNT=$(ls -1 *.md 2>/dev/null | wc -l)
TELEGRAM_COUNT=$(ls -1 archive/2025-10-18-telegram-restoration/*.md 2>/dev/null | wc -l)
SPAWN_COUNT=$(ls -1 archive/2025-10-18-spawn-work/*.md 2>/dev/null | wc -l)
HANDOFF_COUNT=$(ls -1 archive/handoffs/*.md 2>/dev/null | wc -l)

echo "Root .md files: $ROOT_MD_COUNT (target: ~61)"
echo "Telegram restoration archive: $TELEGRAM_COUNT (target: 12)"
echo "Spawn work archive: $SPAWN_COUNT (target: 2)"
echo "Handoffs archive: $HANDOFF_COUNT (target: 3+)"

echo ""
echo "=== Cleanup Complete ==="
echo "Review archive directories to verify all files preserved correctly."
