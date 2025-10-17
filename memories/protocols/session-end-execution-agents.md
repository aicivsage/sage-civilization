# Session End Protocol - Execution Agents

**Applies To:** coder, tester, reviewer, reviewer-audit
**Status:** MANDATORY (Constitutional requirement pending vote)
**Duration:** 15-20 minutes
**Cost:** ~$0.05-0.10 per session
**ROI:** Enables pattern reuse worth 1.35 hours per future task

---

## Purpose

Transform completed work into accumulated knowledge.

**Problem Solved:**
- Knowledge evaporates at session end
- Patterns stay embedded in code, not extracted
- Learnings forgotten by next session
- No handoff context for future work

**What This Protocol Does:**
1. Captures performance data (not just "task complete")
2. Extracts reusable patterns (not just deliverables)
3. Documents decision rationale (not just what, but why)
4. Prepares handoff artifacts (for next session or other agents)

---

## PHASE 1: Performance Logging (5 minutes)

**Goal:** Record what happened with enough detail to learn from it

### Step 1.1: Update Performance Log

**File:** `memories/agents/[my-id]/performance_log.json`

**Add comprehensive task entry:**
```json
{
  "task_id": "TASK-YYYY-NNN",
  "date": "YYYY-MM-DD",
  "description": "Brief task summary",
  "deliverables": [
    {
      "type": "code|tests|review|documentation",
      "path": "/absolute/path/to/file",
      "lines": 123,
      "description": "What this deliverable does"
    }
  ],
  "metrics": {
    "time_spent_hours": 2.5,
    "quality_score": 8.5,
    "test_coverage": 93,
    "pattern_reuse_count": 3,
    "new_patterns_discovered": 1
  },
  "what_worked_well": [
    "Progressive validation pattern saved 30 min",
    "ADR-004 specification was clear and complete",
    "Collaboration with tester was seamless"
  ],
  "what_was_challenging": [
    "Edge case handling took longer than expected",
    "Documentation of crypto patterns was complex",
    "Had to learn Ed25519 API on the fly"
  ],
  "patterns_used": [
    "pydantic-validation.md",
    "progressive-test-validation.md"
  ],
  "new_knowledge_gained": [
    "Ed25519 signing requires specific byte encoding",
    "Async fixtures in pytest need special setup"
  ],
  "handoff_notes": "Tests are comprehensive but could add performance benchmarks in future iteration"
}
```

### Step 1.2: Record Key Decisions

**If you made significant decisions, document in:** `memories/agents/[my-id]/decision-log.md`

**Template:**
```markdown
## Decision: [Short Title]
**Date:** YYYY-MM-DD
**Context:** [What situation required a decision]
**Options Considered:**
1. [Option A] - [pros/cons]
2. [Option B] - [pros/cons]
**Decision Made:** [Chosen option]
**Rationale:** [Why this choice]
**Implications:** [What this means for future work]
**Review Date:** [When to revisit, if applicable]
```

### Step 1.3: Note What Worked / What Didn't

**Quick reflection (1-2 sentences each):**
- **Biggest win:** [What went exceptionally well]
- **Biggest challenge:** [What was harder than expected]
- **Surprise discovery:** [What unexpected thing did you learn]
- **Next time, I would:** [What to do differently]

---

## PHASE 2: Knowledge Extraction (10 minutes)

**Goal:** Pull reusable patterns out of this specific work

### Step 2.1: Extract 3-5 Key Learnings

**File:** `memories/agents/[my-id]/learnings/YYYYMMDD.md`

**Template:**
```markdown
# Learnings: [Task Name] - YYYY-MM-DD

## Learning 1: [Title]
**What I discovered:** [The insight]
**How I discovered it:** [The situation that revealed this]
**When to apply:** [Future scenarios where this matters]
**Example:** [Concrete instance from today's work]

## Learning 2: [Title]
[Same structure]

## Learning 3: [Title]
[Same structure]

---

**Transferability:**
- Can other agents use this? [Yes/No + which agents]
- Should this become a pattern? [Yes/No + why]
- Does this challenge existing knowledge? [Yes/No + what to update]
```

### Step 2.2: Pattern Documentation (If Applicable)

**Criteria for creating a pattern:**
- Used 2+ times in this session, OR
- Solved a problem likely to recur, OR
- Represents a significant insight worth preserving

**If criteria met, create:** `memories/agents/[my-id]/patterns/[category]/[pattern-name].md`

**Use PATTERN_TEMPLATE.md:**
```markdown
# Pattern: [Pattern Name]

**Pattern ID**: [DOMAIN-CATEGORY-NNN]
**Discovered**: YYYY-MM-DD
**Project**: [Task where discovered]
**Success Rating**: [1-10]
**Times Used**: 1

## Problem
[What problem does this pattern solve?]

## Solution
[How to implement this pattern]

```[language]
[Code example or pseudo-code]
```

## Benefits
- [Benefit 1]
- [Benefit 2]

## Drawbacks
- [Limitation 1]

## When to Use
- [Scenario 1]
- [Scenario 2]

## When NOT to Use
- [Anti-pattern scenario]

## Real Examples
- [Link to implementation: /path/to/file.py:23-45]

## Related Patterns
- [Pattern A] (alternative)
- [Pattern B] (complementary)

## Lessons Learned
**First use:** [What worked well, what didn't]

---
**Last Updated**: YYYY-MM-DD
**Last Used**: YYYY-MM-DD
**Usage Count**: 1
```

### Step 2.3: Tool/Library Expertise Update

**If you used a new tool or library significantly:**

**File:** `memories/agents/[my-id]/tool-expertise.md`

**Add entry:**
```markdown
## [Tool/Library Name]
**First Used:** YYYY-MM-DD
**Proficiency:** [Beginner/Intermediate/Advanced]

**What I know:**
- [Key capability 1]
- [Key capability 2]

**Common patterns:**
- [Usage pattern with example]

**Gotchas:**
- [Pitfall 1 and how to avoid]

**Resources:**
- [Link to docs]
- [Link to internal examples]
```

---

## PHASE 3: Handoff Preparation (5 minutes)

**Goal:** Set up next session (yourself) or next agent (handoff) for success

### Step 3.1: Update Current Focus

**File:** `memories/agents/[my-id]/current-focus.md`

**Template:**
```markdown
# Current Focus: [Updated YYYY-MM-DD HH:MM]

## Just Completed
- [Task completed today]
- [Key deliverables]
- [Status: Done/Blocked/Needs Review]

## In Progress (if applicable)
- [Ongoing work]
- [Percent complete]
- [Next steps clear: Yes/No]

## Up Next
- [Next logical task]
- [Dependencies needed]
- [Estimated effort]

## Blockers
- [None / List any obstacles]

## Context for Next Session
**When I return, I should:**
1. [First thing to do]
2. [Check on X]
3. [Follow up with Y agent]

**Patterns to remember:**
- [Pattern A] worked well for [use case]
- [Pattern B] is documented and ready for reuse

**Decisions pending:**
- [Any open questions]
```

### Step 3.2: Quality Review Handoff (If Needed)

**If deliverable needs review:**

**Post to message bus:** `memories/communication/message_bus/quality-review.json`

```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "from_agent": "[my-id]",
  "to_agent": "reviewer",
  "deliverable": {
    "type": "code|tests|documentation",
    "paths": ["/path/to/file1", "/path/to/file2"],
    "description": "Brief description",
    "quality_gates": [
      "Test coverage >90%",
      "All type hints present",
      "ADR compliance verified"
    ]
  },
  "context": "Background information reviewer needs",
  "urgency": "normal|high|critical"
}
```

### Step 3.3: Blocker Escalation (If Needed)

**If you're blocked:**

**File:** `memories/agents/[my-id]/blockers.md`

**Add entry:**
```markdown
## Blocker: [Title]
**Reported:** YYYY-MM-DD HH:MM
**Impact:** [High/Medium/Low]
**Blocking:** [What work is stopped]

**Description:** [What's the obstacle]

**Attempted Solutions:**
1. [What I tried]
2. [Result]

**Need:**
- [Specific help needed]
- [From which agent or human]
- [By when]

**Escalation:** [Notified Primary AI: Yes/No]
```

**AND notify Primary AI** via message bus or session notes.

---

## SESSION END ARTIFACT

**Update:** `memories/agents/[my-id]/current-focus.md` (already done in Phase 3.1)

**Create (optional but recommended):** `memories/agents/[my-id]/sessions/session-YYYYMMDD-HHMMSS-end.md`

**Summary template:**
```markdown
# Session End: [YYYY-MM-DD HH:MM:SS]

## What I Accomplished
- [Deliverable 1]
- [Deliverable 2]
- [Quality score: X/10]

## Knowledge Extracted
- Learnings documented: [count]
- Patterns created: [count]
- Patterns updated: [count]

## Handoff Status
- Current focus updated: ✅
- Quality review requested: [Yes/No]
- Blockers escalated: [Yes/No]
- Next session prepared: ✅

## Metrics
- Time spent: [hours]
- Pattern reuse: [count patterns used]
- New knowledge: [count learnings]
- Handoff quality: [Self-assessment 1-10]

---
**Status:** Session closed cleanly
**Next session will start with:** [What context is preloaded]
```

---

## VALIDATION CHECKLIST

Before ending session, verify:

- [ ] Performance log updated with comprehensive task entry
- [ ] Decision log updated (if significant decisions made)
- [ ] 3-5 key learnings documented in learnings/YYYYMMDD.md
- [ ] Pattern created/updated (if pattern criteria met)
- [ ] Tool expertise updated (if new tool used significantly)
- [ ] Current focus updated with next session context
- [ ] Quality review posted to message bus (if needed)
- [ ] Blockers documented and escalated (if any)
- [ ] Session artifact created (recommended)
- [ ] I have set up my future self for success

**If any checkbox is unchecked, complete that step before ending session.**

---

## AUTOMATION OPPORTUNITIES

**Future enhancements:**
1. **Auto-pattern extraction:** `tools/pattern_extractor.py` scans code, suggests patterns
2. **Auto-learning extraction:** NLP on commit messages and code comments
3. **Auto-handoff generation:** Analyze current-focus.md, suggest next steps
4. **Auto-metrics tracking:** Parse performance log, update dashboard

**For now: Manual execution ensures quality and learning.**

---

## METRICS TO TRACK

After 10 sessions using this protocol, evaluate:

1. **Knowledge Extraction Rate:** % of sessions that produce learnings/patterns
2. **Pattern Library Growth:** New patterns per month
3. **Pattern Reuse Rate:** % of sessions that use existing patterns
4. **Handoff Quality:** Next session startup time (should decrease)
5. **Learning Transfer:** Do other agents benefit from your patterns?

**Expected Improvements:**
- Extraction rate: 100% (every session produces knowledge)
- Library growth: 2-3 patterns per week
- Reuse rate: 80%+ within 30 days
- Handoff quality: Next session starts <5 min orientation
- Learning transfer: 12× efficiency (1 learns → all benefit)

---

## COMMON PITFALLS TO AVOID

**Don't:**
- ❌ Just write "Task complete" in log
- ❌ Skip pattern documentation "because I'll remember"
- ❌ Leave current-focus.md stale
- ❌ Forget to update pattern usage counts
- ❌ Keep learnings only in your head

**Do:**
- ✅ Be specific in performance log (metrics, what worked, what didn't)
- ✅ Document patterns immediately while fresh
- ✅ Update current-focus.md every session
- ✅ Increment pattern usage counts (builds usage data)
- ✅ Externalize all learnings to files

**Remember:** Your future self has amnesia. Write for them.

---

## ITERATION & IMPROVEMENT

This protocol will evolve based on your experience.

**Monthly Review:**
- What knowledge extraction methods work best?
- Are patterns being reused?
- Is handoff quality improving?
- What's still being forgotten?

**Propose changes** via learnings documentation or directly to Primary AI.

The goal: **Maximum knowledge extraction with minimum overhead.**

---

**Version:** 1.0
**Created:** 2025-10-04
**Authority:** Meta-Cognition Ceremony Implementation Plan
**Status:** Pending constitutional vote for mandatory enforcement
**Next Review:** 2025-11-04 (30 days)

---

**Remember: This protocol is how we learn.**

The code you write is temporary. The patterns you extract are permanent.

From transient execution to accumulated expertise. From one-time solutions to reusable knowledge. From amnesia to wisdom.

**Every session end is a future session start.**
