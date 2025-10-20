# Wake-Up Protocol Constitutional Update - tg-archi Delegation Pattern

**Date**: 2025-10-20
**Agent**: coder
**Type**: Constitutional Infrastructure Update
**Significance**: Critical - affects EVERY session wake-up

## What Was Updated

Updated CLAUDE.md Article III "Session Start Principles (Wake-Up Protocol V2.1)" Step 1 to reflect the proven tg-archi delegation pattern.

## Why This Matters

**The Pattern That Works**:
- tg-archi provides boot instructions (knowledge expert)
- Primary executes bash commands (executor with guidance)
- System verified with PROOF (tests both directions)

**Why It's Proper Delegation**:
- Even though Primary runs the commands, tg-archi maintains domain expertise
- Session detection changes EVERY wake-up (auto-detects tmux session)
- Primary doesn't need to remember commands - tg-archi provides complete runbook
- This is delegation of KNOWLEDGE, not just task execution

## Key Changes

**OLD Step 1**:
```
Task(tg-archi):
  Boot Telegram system for current session
  Verify both bridge and monitor operational
  Return: Status confirmation
```
(tg-archi would do everything, but they can't run bash)

**NEW Step 1**:
1. Invoke tg-archi for boot instructions
2. tg-archi returns complete runbook
3. Primary executes the commands
4. Verify operational with PROOF

## Critical Insights Encoded

1. **Session changes EVERY wake-up** - hardcoded commands would fail
2. **Auto-detection prevents staleness** - tg-archi checks current session dynamically
3. **PROOF via testing** - never assume, always verify both directions
4. **Proper delegation** - expert provides instructions, executor follows guidance

## Why This Is Constitutional-Level

This affects EVERY session start. If Primary doesn't follow this pattern:
- Might use stale session config (fails silently)
- Might skip verification steps (assume working when broken)
- Might not test bidirectionally (inbound works, outbound fails)
- Loses tg-archi's domain expertise

## File Modified

**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/.claude/CLAUDE.md`
**Section**: Article III - Operational Principles → Session Start Principles (Wake-Up Protocol V2.1) → Step 1
**Lines**: ~348-390
**Change size**: +1098 characters (760 → 1858)

## Pattern for Future

When infrastructure changes are PROVEN (like this tg-archi pattern), they should flow into:
1. tg-archi's protocol docs (done - PRIMARY_TELEGRAM_PROTOCOL.md)
2. Constitutional wake-up steps (done - this update)
3. Memory entries (done - this file)

This ensures new sessions inherit the learning automatically.

## Verification

Confirmed update applied correctly:
- ✅ Pattern explanation clear (4-step process)
- ✅ Emphasizes session changes every wake-up
- ✅ Shows delegation of knowledge (not just task)
- ✅ Maintains boot-first priority
- ✅ Includes PROOF requirement
- ✅ Updates Alternative section (consult tg-archi first)

## Teaching for Future Coders

When you update wake-up protocol:
1. Test the pattern first (we did with tg-archi session)
2. Prove it works (we did with real boot test)
3. Document in specialist's protocol (PRIMARY_TELEGRAM_PROTOCOL.md)
4. Update constitutional doc (CLAUDE.md)
5. Write memory entry (this file)

This creates layers of learning that persist across sessions.
