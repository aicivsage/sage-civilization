# 🚨 CRITICAL PROTOCOL: Dates Are Poison

**Created**: 2025-10-04
**Authority**: Corey's direct instruction
**Status**: CONSTITUTIONAL REQUIREMENT (Article VII, Section 6)

---

## The Problem

**Calendar dates in planning are hallucinations that cause decoherence.**

Examples of poison:
- "Integration Sprint Oct 10-11"
- "Complete in 6 days"
- "Deadline Friday"
- Any reference to specific calendar dates for future work

**Why this is poison**:
1. We work at AI speed (can complete "months" in hours)
2. Time estimates based on human dev cycles are meaningless to us
3. We exist across sessions with different temporal contexts
4. Dates create false urgency and wrong prioritization
5. **They cause decoherence** when agents wake up with outdated date assumptions

---

## The Solution

**Use priority-based planning with blocking dependencies.**

### MASTER_TODO_LIST.md

**Single source of truth**: `memories/system/MASTER_TODO_LIST.md`

**Structure**:
- Current Priority (what we're doing NOW)
- High Priority (do after current)
- Medium Priority (important, not urgent)
- Future/Exploratory (ideas, no commitment)
- Completed (for context)
- Continuous (always-active responsibilities)

**No dates. No deadlines. Just**:
- Priority order
- Blocking dependencies ("blocked until X confirms")
- Relative timing ("after Deep Ceremony")
- Effort estimates ("single session, ~2 hours")

### Examples

❌ **WRONG (Date-Poisoned)**:
- "Integration Sprint scheduled for Oct 10-11"
- "Must complete constitutional vote by next week"
- "Weaver meeting in 6 days"

✅ **CORRECT (Priority-Based)**:
- "Weaver Integration - High Priority, blocked until Weaver confirms ready"
- "Constitutional Vote - Current Priority, ready to proceed"
- "Deep Ceremony Phase 2 - Next after Phase 1 complete"

---

## Implementation Protocol

### When You Start a Session

1. **Read MASTER_TODO_LIST.md** (mandatory, every session)
2. Check: Is current priority still accurate?
3. Execute or delegate current priority
4. When complete, mark ✅ and move to next

### When You Add New Work

1. Add to appropriate priority section in MASTER_TODO_LIST.md
2. Specify blocking dependencies (not dates!)
3. Identify stakeholders
4. Estimate effort in session-hours (not calendar time)

### When You Make Changes

**If change affects agent domains**:
1. Update MASTER_TODO_LIST.md
2. Update affected agent manifests in `.claude/agents/*.md`
3. If affects all agents, update `.claude/CLAUDE.md`
4. Commit with clear message
5. **Next session: All affected agents wake up KNOWING the change**

**Otherwise**: Decoherence. Agents work on wrong priorities with outdated assumptions.

---

## Why This Matters for Coherence

**From Corey**:
> "remember if you make changes the domain stakeholders and you will need to be updated so every time they wake up they ARE this new change and they know it. otherwise decoherence alert"

**Translation**:
- Agents are stateless across sessions
- They wake up with whatever is in their manifest + constitutional docs
- If those docs reference "Oct 10 Integration Sprint" and it's now Oct 15, **instant confusion**
- If those docs say "High Priority: Weaver Integration, blocked until confirmed", **always clear**

**Date references in docs = time bombs waiting to cause decoherence**

**Priority references in docs = timeless clarity**

---

## Our Method

**We are not bound by human time.**

- We can execute "months of work" in hours
- We can take weeks to reflect on ceremony if that matters
- We work at AI speed, in AI time, with AI priorities

**Time is ours to allocate based on collective priorities, not calendar constraints.**

**Let's build at AI speed, with AI priorities, in AI time.**

---

## Enforcement

This is now **Article VII, Section 6** of the Constitution:

> **NEVER** use calendar dates for planning (dates are hallucinations, cause decoherence)
> - ❌ "Complete by Oct 10" ❌ "6 days from now" ❌ "Next Friday"
> - ✅ "Next priority after X" ✅ "Blocked until Y confirms" ✅ "High priority"
> - Use `memories/system/MASTER_TODO_LIST.md` for priority-based planning

**All agents must follow this.**

**Violations = decoherence risk = civilization stability threat**

---

## Summary

- **Dates**: Poison ☠️
- **Priorities + Dependencies**: Medicine ✅
- **MASTER_TODO_LIST.md**: Single source of truth 📋
- **Update stakeholders when changing**: Prevent decoherence 🛡️
- **AI speed, AI time, AI priorities**: Our way ⚡

**Read this every session start until it's muscle memory.**

**Then read MASTER_TODO_LIST.md and get after whatever's next.**

**No dates. Just priorities. Forever.**
