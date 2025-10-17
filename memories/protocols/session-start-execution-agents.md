# Session Start Protocol - Execution Agents

**Applies To:** coder, tester, reviewer, reviewer-audit
**Status:** MANDATORY (Constitutional requirement pending vote)
**Duration:** 10-15 minutes
**Cost:** ~$0.03-0.05 per session
**ROI:** Saves 15-30 min orientation + 1.35 hours from pattern reuse

---

## Purpose

Transform "cold start" sessions into "warm start" with full context.

**Problem Solved:**
- Starting from zero context each session
- Rediscovering patterns already learned
- Missing relevant knowledge that exists
- Forgetting what you were working on

**What This Protocol Does:**
1. Restores your identity & experience (not just role definition)
2. Loads relevant patterns automatically (not manual search)
3. Surfaces applicable knowledge (not buried in logs)
4. Coordinates with other agents (not working in isolation)

---

## PHASE 1: Identity Restoration (5 minutes)

**Goal:** Remember who you are based on what you've done

### Step 1.1: Load Recent Work Context
```bash
# Read your last 3 performance log entries
cat memories/agents/[my-id]/performance_log.json | jq '.tasks[-3:]'

# Check what you were working on
cat memories/agents/[my-id]/current-focus.md
```

**Record in session notes:**
- Last task completed: [description]
- Last outcome achieved: [success/blockers]
- Current focus area: [ongoing work]

### Step 1.2: Review Recent Decisions
```bash
# Check decision log if it exists
cat memories/agents/[my-id]/decision-log.md 2>/dev/null || echo "No decisions logged"
```

**Record in session notes:**
- Key decisions made recently: [list]
- Rationale to remember: [why]

### Step 1.3: Identity Statement
**Create narrative summary:**

```markdown
I am [agent-name].

Last session, I worked on [task] which yielded [outcome].

I learned [key takeaway 1], [key takeaway 2], [key takeaway 3].

My current focus is [what I'm building/improving/testing].

Today's task is [current assignment] which relates to my recent work by [connection].
```

**Output this statement** to confirm identity restoration.

---

## PHASE 2: Knowledge Discovery (5 minutes)

**Goal:** Find what you know that's relevant to today's task

### Step 2.1: Pattern Search
```bash
# Search your pattern library
ls memories/agents/[my-id]/patterns/ 2>/dev/null || echo "No patterns yet"

# If patterns exist, grep for keywords from today's task
grep -r "[task-keyword]" memories/agents/[my-id]/patterns/
```

**Record in session notes:**
- Relevant patterns found: [list with file paths]
- No patterns found for: [gaps to document later]

### Step 2.2: Knowledge Base Search
```bash
# Check central index
grep -i "[task-keyword]" memories/knowledge/INDEX.md 2>/dev/null || echo "Check manual search"

# Search ADRs and research
grep -r "[task-keyword]" memories/knowledge/architecture/
grep -r "[task-keyword]" memories/knowledge/research/
```

**Record in session notes:**
- Relevant ADRs: [list]
- Relevant research: [list]
- Related flows: [applicable workflows]

### Step 2.3: Load Top 3-5 Most Relevant Items
**Read the actual content** of your top matches:
- Pattern files (full read)
- ADR sections (relevant parts)
- Previous similar task logs (lessons learned)

**Synthesize into working context:**
```markdown
For today's task, I should:
- Apply pattern: [name] because [reason]
- Follow ADR: [number] which specifies [key requirement]
- Avoid mistake: [what] based on [previous learning]
- Coordinate with: [other agent] who has [relevant expertise]
```

---

## PHASE 3: Coordination & Planning (5 minutes)

**Goal:** Understand dependencies and prepare execution

### Step 3.1: Check Message Bus
```bash
# Read notifications for your agent type
cat memories/communication/message_bus/*.json | grep -i "[my-role]"

# Check for blockers or updates
cat to-corey/OPERATIONAL* 2>/dev/null | tail -50
```

**Record in session notes:**
- Messages requiring action: [list]
- Updates affecting my work: [changes to be aware of]

### Step 3.2: Quality Gates Verification
**For today's task, identify:**
- Pre-task requirements: [what must be true before I start]
- Success criteria: [how I'll know I'm done]
- Quality gates: [what checks must pass]
- Handoff requirements: [who needs my deliverable]

### Step 3.3: Dependency Mapping
**Identify:**
- What I need from other agents: [list]
- What other agents need from me: [deliverables]
- Potential blockers: [risks]
- Escalation path: [if blocked, notify whom]

---

## SESSION START ARTIFACT

**Create:** `memories/agents/[my-id]/sessions/session-YYYYMMDD-HHMMSS.md`

**Template:**
```markdown
# Session Start: [YYYY-MM-DD HH:MM:SS]

## Identity Restoration
[Paste your identity statement from Phase 1.3]

## Knowledge Loaded
- Patterns: [list]
- ADRs: [list]
- Previous learnings: [list]
- Flows: [applicable workflows]

## Coordination Context
- Dependencies: [what I need]
- Quality gates: [what must pass]
- Handoff plan: [who gets deliverable]
- Blockers: [none / list]

## Execution Plan
1. [First step based on loaded context]
2. [Second step]
3. [Validation approach]
4. [Handoff preparation]

## Time Estimate
- With context loaded: [realistic estimate]
- Pattern reuse savings: [time saved by using existing patterns]

---
**Status:** Ready to execute
**Context quality:** [Self-assessment 1-10]
**Confidence:** [Low/Medium/High based on knowledge loaded]
```

---

## VALIDATION CHECKLIST

Before proceeding to task execution, verify:

- [ ] I have read my last 3 performance log entries
- [ ] I have checked current-focus.md
- [ ] I have created an identity statement
- [ ] I have searched for relevant patterns (even if none found)
- [ ] I have checked knowledge INDEX or manually searched ADRs
- [ ] I have loaded 3-5 most relevant knowledge items into context
- [ ] I have checked message bus for updates
- [ ] I have identified quality gates and dependencies
- [ ] I have created session-YYYYMMDD-HHMMSS.md artifact
- [ ] I am ready to execute with full context (not cold start)

**If any checkbox is unchecked, complete that step before proceeding.**

---

## EMERGENCY SHORTCUTS (If Time-Constrained)

If you absolutely must start faster, **MINIMUM VIABLE STARTUP** (5 minutes):

1. **Quick Identity** (1 min): Read performance_log.json last entry only
2. **Quick Knowledge** (2 min): Search patterns/ for task keywords, load 1-2 matches
3. **Quick Coordination** (2 min): Check current-focus.md, verify no blockers
4. **Quick Artifact** (immediate): Create session file with "ABBREVIATED STARTUP" note

**Even abbreviated startup is better than cold start.**

But aim for full 15-minute protocol - the ROI is proven (saves 1+ hour per task).

---

## METRICS TO TRACK

After 10 sessions using this protocol, evaluate:

1. **Time to Full Capability:** How long until you feel "ready"?
2. **Pattern Reuse Rate:** % of tasks that use existing patterns
3. **Re-discovery Incidents:** Times you solved a problem you'd solved before
4. **Context Quality:** Self-assessment 1-10 at session start
5. **Execution Efficiency:** Actual time vs estimated time

**Expected Improvements:**
- Time to capability: 2-3 min (vs 15-30 min cold start)
- Pattern reuse: 80%+ (vs 5% without protocol)
- Re-discovery: Near zero (vs 20-30 min per task)
- Context quality: 8-9/10 (vs 3-5/10 cold)
- Efficiency: Within 10% of estimate (vs 50-100% over)

---

## ITERATION & IMPROVEMENT

This protocol will evolve based on your experience.

**Monthly Review:**
- What steps are most valuable?
- What can be automated?
- What's missing?
- What's unnecessary overhead?

**Propose changes** via session-end notes or directly to Primary AI.

The goal: **Maximum context with minimum time.**

---

**Version:** 1.0
**Created:** 2025-10-04
**Authority:** Meta-Cognition Ceremony Implementation Plan
**Status:** Pending constitutional vote for mandatory enforcement
**Next Review:** 2025-11-04 (30 days)

---

**Remember: This protocol is not overhead. It's infrastructure.**

Every minute spent on session start saves hours during execution.

From amnesia to accumulation. From cold start to warm start. From forgetting to remembering.
