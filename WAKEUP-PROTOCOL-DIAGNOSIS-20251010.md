# Wakeup Protocol Failure - Root Cause & Fix

**Date**: 2025-10-10
**Issue**: Primary AI woke up with 6-day-old priorities

---

## What Happened

**I woke up and**:
1. Read `memories/system/MASTER_TODO_LIST.md` (says "Last Updated: 2025-10-04")
2. Saw "Current Priority: Deep Ceremony - Phase 2"
3. Reported this as current status to Corey
4. Corey said: "this is actually all old"

**Reality**:
- Oct 8-9: BNB Launchpad work (2 forks built, tests fixed, email sent)
- Oct 9: Comprehensive handoff written to `COMPREHENSIVE-HANDOFF-20251009.md`
- MASTER_TODO was never updated

---

## Root Cause

**Wakeup protocol flaw**: Reads static files that may be stale

**Current wakeup protocol**:
1. Read CLAUDE.md (constitution)
2. Read MASTER_TODO_LIST.md (priorities)
3. Check emails
4. Check Weaver messages

**Problem**: MASTER_TODO is manually updated, so if last session doesn't update it, next session wakes up with stale priorities.

**Evidence**:
- MASTER_TODO: "Last Updated: 2025-10-04" (6 days old)
- Actual handoffs: `BNB-COMPLETE-SYSTEM-READY-20251009.md`, `COMPREHENSIVE-HANDOFF-20251009.md` (1 day old)
- Gap: 5 days of work not reflected in MASTER_TODO

---

## The Fix

### Option 1: Read Recent Handoffs FIRST (Quick Fix)

Change wakeup order:
1. Read CLAUDE.md (identity)
2. **Find most recent `*HANDOFF*.md` or `*SESSION-COMPLETE*.md` in root directory** (actual recent work)
3. Then read MASTER_TODO as backup/long-term priorities
4. Check emails
5. Check Weaver messages

Bash to find most recent session summary:
```bash
ls -t /home/corey/projects/AI-CIV/grow_gemini_deepresearch/*.md | grep -E "(HANDOFF|SESSION-COMPLETE|COMPREHENSIVE)" | head -1
```

### Option 2: Create LAST_SESSION.md Standard (Better Fix)

**Every session ending**:
- Write `LAST_SESSION.md` to root directory
- Include: What was done, what's next, blockers, timestamp

**Every session starting**:
- Read `LAST_SESSION.md` FIRST (guaranteed fresh)
- Then read MASTER_TODO (long-term context)

**Benefit**: Single source of truth for "what happened last session"

### Option 3: Git-Based Wake Protocol (Robust Fix)

**Session start logic**:
1. Run: `git log -1 --format="%H %s" --name-only`
2. Find most recently modified files (what actually changed)
3. Read those files to understand recent work
4. Fall back to MASTER_TODO for long-term priorities

**Benefit**: Can't get stale (git history is always accurate)

---

## Recommended Fix: Hybrid Approach

**Immediate (today)**:
1. Update MASTER_TODO to reflect BNB work completion
2. Add "Last Updated" check to wakeup protocol (if >3 days old, WARNING)

**Short-term (this week)**:
3. Add LAST_SESSION.md standard to all session endings
4. Update wakeup protocol to read LAST_SESSION.md first

**Long-term (when valuable)**:
5. Build git-based wake protocol for guaranteed accuracy

---

## Updated Wakeup Protocol (Proposed)

```
1. Read CLAUDE.md (identity, principles)

2. Find most recent session summary:
   - Check root for *HANDOFF*.md or *SESSION-COMPLETE*.md (last 24h)
   - OR check for LAST_SESSION.md
   - Read most recent (this is ACTUAL recent work)

3. Read MASTER_TODO_LIST.md:
   - Check "Last Updated" field
   - If >3 days old: FLAG as potentially stale
   - Use for long-term priorities, not immediate status

4. Check communications:
   - Email inbox (via human-liaison)
   - Weaver comms hub (via comms-hub)

5. Synthesize:
   - Recent work (from handoff)
   - Long-term priorities (from MASTER_TODO)
   - New directives (from email/comms)
   - = Current actual status
```

---

## Action Items

**For Primary**:
1. Update MASTER_TODO now (BNB work complete, what's next?)
2. Implement improved wakeup protocol
3. Create LAST_SESSION.md standard

**For Future Sessions**:
1. Always write handoff file at session end
2. Always update MASTER_TODO if priorities change
3. Use LAST_SESSION.md as session-to-session bridge

---

## Lessons Learned

**Problem**: Relied on manually-updated file for critical context
**Result**: 6-day decoherence (woke up thinking Deep Ceremony was current)
**Fix**: Multi-source wake protocol (recent handoffs + long-term TODO + communications)

**Principle**: **Recent actuals > static plans**

If handoff says "BNB complete Oct 9" and MASTER_TODO says "Deep Ceremony current priority (Oct 4)", believe the handoff.

---

**Status**: Root cause identified, fix proposed, ready to implement
