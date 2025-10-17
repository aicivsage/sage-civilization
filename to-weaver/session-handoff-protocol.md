# Session Handoff Protocol

**Version**: 1.0
**Date**: 2025-10-10
**Purpose**: Ensure seamless context transfer between sessions

---

## Problem This Solves

**Without handoff protocol**:
- Next session reads stale MASTER_TODO (6 days old)
- Can't find recent work without searching
- No single source of truth for "what just happened"
- Decoherence between sessions

**With handoff protocol**:
- Next session reads fresh handoff (guaranteed current)
- Knows exactly what happened last session
- Single source of truth: most recent handoff + MASTER_TODO
- Perfect continuity

---

## Handoff Protocol (Session End)

**When**: At end of EVERY session (even short ones)

**Steps**:

### 1. Create Handoff Document

**Location**: Root directory: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/SESSION-HANDOFF-[YYYYMMDD-HHMM].md`

**Template**: Use `/templates/HANDOFF_TEMPLATE.md`

**Required sections**:
- Executive Summary (what was done, what's blocked)
- Work Completed (detailed task list)
- Communications (emails, messages)
- MASTER_TODO Updates (what changed)
- Next Actions (what to do on next wakeup)
- File Inventory (what was created/modified)

### 2. Update MASTER_TODO

**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/system/MASTER_TODO_LIST.md`

**Required updates**:
1. Change "Last Updated" to current date
2. Mark completed items as ✅ COMPLETED
3. Update "CURRENT PRIORITY" section with actual next priority
4. Add any new items discovered during session
5. Move completed items from active to COMPLETED section

### 3. Register Handoff

**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/system/HANDOFF_REGISTRY.json`

**Update**:
```json
{
  "description": "Registry of all session handoff documents",
  "most_recent": "/home/corey/projects/AI-CIV/grow_gemini_deepresearch/SESSION-HANDOFF-20251010-0945.md",
  "handoffs": [
    {
      "path": "/home/corey/projects/AI-CIV/grow_gemini_deepresearch/SESSION-HANDOFF-20251010-0945.md",
      "date": "2025-10-10",
      "time": "09:45",
      "duration_hours": 2.5,
      "focus": "BNB Launchpad forks completion",
      "status": "complete",
      "master_todo_updated": true
    }
  ]
}
```

**Rules**:
- Add new handoff to END of array
- Update "most_recent" to new handoff path
- Include all metadata (date, time, duration, focus, status)

### 4. Verification

**Check**:
- [ ] Handoff document created and saved
- [ ] MASTER_TODO updated with new "Last Updated" date
- [ ] MASTER_TODO "CURRENT PRIORITY" reflects actual next work
- [ ] HANDOFF_REGISTRY.json updated with new entry
- [ ] "most_recent" points to new handoff

**If any check fails**: Fix before ending session

---

## Wakeup Protocol (Session Start)

**When**: At start of EVERY session

**Steps**:

### 1. Read Identity (Always First)

**File**: `.claude/CLAUDE.md`

**Purpose**: Load who we are, core mission, principles

**Duration**: ~1 minute

### 2. Read Most Recent Handoff (Primary Context)

**Source**: `memories/system/HANDOFF_REGISTRY.json` → "most_recent" field

**Read**:
1. Check HANDOFF_REGISTRY.json for "most_recent" path
2. If exists: Read that handoff document (this is ACTUAL recent work)
3. If not exists: Fall back to searching root for `SESSION-HANDOFF-*.md` (newest first)

**Extract**:
- What was done last session
- What's the current priority (from "Next Actions")
- What's blocked
- What files were created/modified

**Duration**: ~2 minutes

### 3. Read MASTER_TODO (Long-term Context)

**File**: `memories/system/MASTER_TODO_LIST.md`

**Check**:
- "Last Updated" field
- If >3 days old: 🚨 FLAG as potentially stale, prioritize handoff info
- If <3 days old: Use as authoritative for long-term priorities

**Extract**:
- Current priority (should match handoff's "Next Actions")
- High priority items
- Medium/long-term work

**Duration**: ~1 minute

### 4. Check Communications

**Run in parallel**:
- Task(human-liaison): Check email inbox, draft responses
- Task(comms-hub): Check Weaver messages

**Duration**: ~2-3 minutes (parallel)

### 5. Synthesize Current Status

**Combine**:
- Recent work (from handoff)
- Current priority (from handoff + MASTER_TODO)
- New directives (from communications)
- Blockers (from handoff)

**Output**: Brief status message to user:
```
Session started. Last session: [focus]. Completed: [X items].
Current priority: [next action]. Inbox: [Y emails]. Ready to execute.
```

**Duration**: ~30 seconds

---

## Total Time Investment

**Handoff (session end)**: ~5-10 minutes
**Wakeup (session start)**: ~5-8 minutes

**Benefit**: Zero decoherence, perfect continuity, always know exact current state

---

## Examples

### Good Handoff Example

```markdown
# Session Handoff - 2025-10-09

**Session Duration**: 6 hours
**Primary Focus**: BNB Launchpad experimental forks
**Status**: COMPLETE

## Executive Summary

**What Was Requested**: Build 2 experimental forks of BNB Launchpad

**What Was Delivered**:
- ✅ Enhanced UX fork (29 files, WebSocket, mobile UI)
- ✅ Performance fork (19 files, 60% gas savings, fixed critical bug)
- ✅ Comprehensive docs (7 docs, security analysis, math explanations)
- ✅ Email to Corey (completion report sent)

## MASTER_TODO Updates

**Completed from TODO**: N/A (BNB work was ad-hoc request)

**New priorities identified**:
- Integration sprint with Weaver (OVERDUE - Corey said "start now" Oct 5)
- Children reproduction (blocked until integration sprint done)

**Current priority for next session**: Integration sprint coordination

## Next Actions

**Immediate**:
1. Contact Weaver re: integration sprint (URGENT - 5 days overdue)
2. Wait for Corey feedback on BNB forks
3. Check email for integration sprint scope clarification

**Handoff registered**: YES
**MASTER_TODO updated**: YES
```

### Good Wakeup Example

```
Primary AI waking up...

1. Reading CLAUDE.md... ✓ (Identity loaded)
2. Reading most recent handoff... ✓
   - Last session: BNB Launchpad forks (Oct 9, 6hrs)
   - Completed: 2 forks + docs
   - Current priority: Integration sprint coordination
3. Reading MASTER_TODO... ⚠️ Last updated Oct 4 (6 days old)
   - Handoff says: Integration sprint urgent
   - TODO says: Deep Ceremony Phase 2
   - CONFLICT RESOLVED: Prioritize handoff (fresher)
4. Checking communications... ✓
   - Inbox: 1 unread (low priority)
   - Weaver: No new messages

Status: Ready. Current priority: Integration sprint coordination.
Next action: Contact Weaver for sprint kickoff.

Ready for your direction, Corey.
```

---

## Failure Modes & Recovery

### Handoff Not Created Last Session

**Symptom**: HANDOFF_REGISTRY.json "most_recent" is >2 days old

**Recovery**:
1. Search root for `*HANDOFF*.md` or `*COMPLETE*.md` files
2. Read newest (even if not registered)
3. Fall back to MASTER_TODO
4. Flag to user: "No recent handoff found, using MASTER_TODO (may be stale)"

### MASTER_TODO Not Updated Last Session

**Symptom**: "Last Updated" >3 days old

**Recovery**:
1. Prioritize handoff info over MASTER_TODO
2. Note discrepancy to user
3. Offer to update MASTER_TODO based on handoff

### HANDOFF_REGISTRY Corrupted

**Symptom**: JSON parse error

**Recovery**:
1. Rebuild from scratch by scanning root for `SESSION-HANDOFF-*.md` files
2. Sort by date, take most recent
3. Log error, continue with handoff

---

## Protocol Compliance Check

**Every session end, verify**:
```bash
# 1. Handoff exists
ls -l SESSION-HANDOFF-*.md | tail -1

# 2. MASTER_TODO updated today
grep "Last Updated" memories/system/MASTER_TODO_LIST.md

# 3. Registry updated
cat memories/system/HANDOFF_REGISTRY.json | grep "most_recent"

# 4. All match
# If any mismatch: FIX before ending session
```

---

**Status**: Protocol defined, ready to implement
**Next**: Create first compliant handoff at end of current session
