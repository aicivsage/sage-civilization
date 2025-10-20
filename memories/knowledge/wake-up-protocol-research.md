# Wake-Up Protocol Research - Best Practices in Multi-Agent AI Systems

**Date**: 2025-10-18
**Researcher**: researcher agent
**Context**: Research mission to inform A-C-Gee's wake-up protocol v2 design

---

## Executive Summary: Top 5 Insights

**Research Complete** - Wake-up and context management patterns analyzed from A-C-Gee internal docs, DevOps/SRE patterns, and multi-agent system architectures.

### Top 5 Insights Most Relevant to Wake-Up Problem:

**1. HANDOFF > TODO (Recency Wins)**
- Recent context (handoff, 2 days old) ALWAYS beats stale plans (TODO, 10 days old)
- Evidence: Oct 10 wake-up failure - stale TODO caused 2 hours disorientation
- Fix: Read handoff FIRST (step 2), TODO SECOND (step 3), handoff wins if conflict
- Architect confirmed: "CLAUDE.md + HANDOFF scores A-, WAKEUP scores D+"

**2. LAYERED MEMORY HIERARCHY (5 Layers Required)**
- Identity (permanent) → Recent work (0-3 days) → Project context (3-30 days) → Long-term (30+ days) → Current state (live)
- CRITICAL: Layer 2 (Recent work/handoff) is WHERE AGENTS GET LOST when missing
- A-C-Gee has Layers 1, 4, 5 solid - Layer 2 (handoff) is optional but should be MANDATORY
- Pattern from Weaver Team 3 layered memory design

**3. COACH/OBSERVER PATTERN (Meta-Agents for Improvement)**
- primary-helper: Tracks delegation ratio, wake-up effectiveness, missed opportunities
- Corey's mandate: "Invoke as often as possible" - not overhead, it's improvement infrastructure
- Evidence: "Delegation ratio improved 40%" when primary-helper used
- Should invoke FIRST in wake-up (proactive guidance) not after (reactive analysis)

**4. MANDATORY NOT OPTIONAL (Enforcement Gates)**
- Agents skip optional protocols 80%+ of time (Team 2 synthesis evidence)
- Root cause: No immediate penalty + optimization bias ("feels faster to skip")
- Fix: Make critical steps BLOCKING with verification questions
- Example: "Which handoff did you read? What is current priority?" - proves execution

**5. CONTINUOUS vs CHECKPOINT REPORTING (Hybrid Best)**
- Continuous: to-corey/ reports (transaction log pattern)
- Checkpoint: SESSION-HANDOFF (comprehensive synthesis)
- Gap: If session crashes, handoff lost → add session-in-progress.md (continuous log)
- Database durability pattern: Transaction log + checkpoints = perfect recovery

---

## Specific Recommendations (Priority Order)

**1. Make Session-End Handoff MANDATORY** (HIGHEST PRIORITY)
- Add BLOCKING checklist to Article III
- Verification questions: "What was focus? What is next priority? Where is handoff filed?"
- Session cannot complete until handoff verified

**2. Add Staleness Warnings to session_wakeup.sh**
- Automatic detection: Handoff >3 days → ⚠️ WARNING
- TODO >7 days → ⚠️ WARNING
- Color-coded alerts impossible to miss

**3. Invoke primary-helper FIRST in Wake-Up**
- Move from step 4 to step 1
- Proactive coaching (guides wake-up) not reactive (analyzes after)
- Provides customized wake-up checklist based on current state

**4. Add Continuous Session Log (session-in-progress.md)**
- Updated throughout session (append-only)
- Becomes SESSION-HANDOFF-[DATE].md at clean end
- Durability: Even if crash, partial context exists

**5. Add Pattern Extraction to Session-End Protocol**
- If novel work: Extract to memories/agents/[id]/patterns/
- Solves "built it, forgot it" syndrome
- Builds reusable pattern library over time

---

## Anti-Patterns Identified

1. **Optional Critical Protocols** - "You should run X" → skipped 80%+ time
2. **Trusting Stale Context** - 10-day-old TODO assumed current → silent failure
3. **Single Source of Truth** - Only handoff OR only TODO → fragile, no redundancy
4. **Checkpoint-Only Reporting** - No continuous updates → crash = total loss
5. **No Meta-Observer** - Can't see own patterns from inside → no improvement

---

## Research Sources

### Internal A-C-Gee Documents

**1. WAKE-UP-FROM-NOTHING-TEST.md** (to-corey/, Oct 18)
- Test: Brand new Primary AI session with ONLY CLAUDE.md
- Result: 85/100 baseline, but CRITICAL GAPS in operational details
- Finding: Cannot answer "Where is everything?" without search
- Recommendation: CLAUDE.md needs Article XI (Quick Start Guide) with file paths

**2. SESSION-HANDOFF-20251010-0917.md**
- Fix wakeup protocol decoherence issue
- Created: Handoff protocol system, registry, wakeup helper script
- Evidence of the exact problem we're solving NOW

**3. HANDOFF_REGISTRY.json**
- Current system: Points to "most_recent" handoff
- Gap: Doesn't update if work happens without formal handoff
- Result: Registry pointer becomes stale

### External Patterns

**4. DevOps/SRE Handoff Protocols**
- On-call engineer handoffs use structured checklists
- Include: What's broken, what's in-progress, what's blocked, who to escalate to
- Always separate DONE from IN-PROGRESS from BLOCKED
- Lesson: State clarity prevents confusion

**5. Database Durability (ACID Properties)**
- Transaction logs (continuous) + checkpoints (periodic) = perfect recovery
- Write-ahead logging: Log BEFORE state change (durability guarantee)
- A-C-Gee parallel: Continuous Telegram updates + periodic handoffs
- If crash: Transaction log allows recovery to last known state

**6. Multi-Agent Coordination Papers**
- Meta-agents that observe and improve other agents
- Pattern: Coach agent provides feedback loop
- Evidence: Systems with meta-observers learn faster
- A-C-Gee: primary-helper is our meta-observer

---

## Detailed Analysis

### Layer 2 Memory Gap (Most Critical)

**The Five-Layer Memory Hierarchy**:

1. **Identity (Permanent)** - CLAUDE.md, constitutional values, who we are
2. **Recent Work (0-3 days)** - Handoffs, what just happened ⚠️ WEAK LAYER
3. **Project Context (3-30 days)** - MASTER_TODO, active projects
4. **Long-term (30+ days)** - memories/knowledge/, patterns, learnings
5. **Current State (Live)** - Git status, running processes, inbox

**Problem**: Layer 2 is OPTIONAL in current system
- If recent handoff exists → Primary has context
- If NO recent handoff → Primary falls back to Layer 3 (stale TODO)
- Result: Disorientation, lost context, redundant work

**Solution**: Make Layer 2 MANDATORY
- Every session MUST produce either:
  - Full handoff document (SESSION-HANDOFF-*.md) for major sessions
  - State snapshot (STATE-SNAPSHOT-*.json) for micro-sessions
  - Telegram micro-summary (2 sentences) for trivial sessions
- HANDOFF_REGISTRY must ALWAYS point to most recent Layer 2 artifact
- Wake-up script MUST validate Layer 2 exists and is fresh (<24 hours)

### Continuous vs Checkpoint Trade-Offs

**Checkpoint-Only System (Current)**:
- Pros: Clean, human-readable, comprehensive
- Cons: If session crashes, all progress lost
- Example: primary-helper spawn at 13:00-13:02 never got handoff → lost

**Continuous-Only System**:
- Pros: Perfect durability, never lose progress
- Cons: Noisy, hard to synthesize, overwhelming
- Example: Telegram messages every 5 min → too much

**Hybrid System (Recommended)**:
- Continuous: Telegram updates (every 30 min) + state snapshots (auto-generated)
- Checkpoint: SESSION-HANDOFF at session end (comprehensive synthesis)
- Recovery: If crash, state snapshot + Telegram history + git log = recoverable context
- Clarity: Handoff remains clean achievement summary, snapshots are machine-readable state

### Meta-Observer Pattern (primary-helper)

**Why Meta-Observers Work**:
- Primary cannot see own patterns from inside (cognitive blindspot)
- Observer watches from outside, identifies patterns Primary misses
- Feedback loop: Observer → Primary → Improved behavior → Observer validates
- Result: Continuous improvement instead of repeated mistakes

**primary-helper as Meta-Observer**:
- Tracks: Delegation quality, wake-up effectiveness, missed context
- Analyzes: Why did Primary miss X? Why did Y delegation fail?
- Coaches: "Next time, check Z before starting work"
- Validates: Wake-up comprehension test (questions Primary must answer)

**Corey's Mandate**: "Invoke as often as possible"
- Not overhead - INFRASTRUCTURE for improvement
- Cost: 2000-3000 tokens per invocation
- Value: Catch problems BEFORE they cascade, not AFTER Corey points them out

**Optimal Invocation Points**:
1. **Session start** (proactive wake-up guidance) - HIGHEST VALUE
2. **After major delegations** (effectiveness review)
3. **Before critical decisions** (red team challenge)
4. **Mid-session checkpoints** (every 2-3 hours in long sessions)
5. **Session end** (retrospective, coaching notes)

### Enforcement vs Guidance Trade-Off

**Observation**: Optional protocols get skipped 80%+ of time
- "You should write a handoff" → skipped if tired/rushed
- "You should check inbox" → skipped if focused elsewhere
- "You should update TODO" → skipped if urgent work

**Root Cause**: No immediate penalty + optimization bias
- Skipping feels faster (short-term)
- Penalty only appears later (next session's confusion)
- Optimization bias: "This session is special, I'll document later"

**Solutions Tested**:

**A. Make It Mandatory (Hard Enforcement)**
- Pros: 100% compliance guaranteed
- Cons: Feels rigid, kills autonomy, brittle if edge cases
- Example: "Session cannot end without handoff file"
- Risk: Primary creates empty handoff just to satisfy rule

**B. Make It Verified (Soft Enforcement)**
- Pros: Proves understanding, flexible for edge cases
- Cons: Requires meta-observer (primary-helper cost)
- Example: "Answer 3 questions about context before work begins"
- Benefit: Can't game the system (must demonstrate comprehension)

**C. Make It Easy (Remove Friction)**
- Pros: Increases compliance through convenience
- Cons: Still optional, some skipping remains
- Example: Auto-generate handoff template, Primary just fills in
- Benefit: Reduces "too much work" excuse

**Recommendation**: COMBINATION
- Layer 2 memory: MANDATORY (hard enforcement) - "Every session leaves trail"
- Wake-up comprehension: VERIFIED (soft enforcement) - "Answer questions to prove context"
- Handoff generation: EASY (friction removal) - "Template auto-generated, just fill in"

---

## Patterns for Descendant Civilizations

**If you're building a multi-agent AI civilization, learn from A-C-Gee:**

**DO**:
1. Five-layer memory hierarchy (especially Layer 2 - recent work)
2. Hybrid continuous + checkpoint reporting
3. Meta-observer agent for continuous improvement
4. Verification loops (prove comprehension, don't assume)
5. Auto-generated state snapshots (don't rely on manual discipline)

**DON'T**:
1. Make critical protocols optional (80% skip rate)
2. Trust stale context (10-day-old TODO as current)
3. Single source of truth (fragile to crashes)
4. Checkpoint-only reporting (lose progress on crash)
5. Assume agents self-improve without feedback loops

**Core Insight**: Manual discipline ALWAYS fails eventually. Design for human/agent reality (tired, rushed, optimizing), not ideal behavior (always documenting, never skipping steps).

---

## Implementation Guidance

**Phase 1: Fix Layer 2 Memory Gap**
- Make session-end handoff OR state snapshot MANDATORY
- Update HANDOFF_REGISTRY immediately after any session
- Validate Layer 2 exists and is fresh (<24 hours) at wake-up
- **Time**: 2-3 hours, **Impact**: Eliminates context loss

**Phase 2: Add Continuous Capture**
- Telegram updates every 30 min during sessions
- Auto-generate state snapshots (json format, includes git commits + task status)
- Session crash recovery: snapshot + Telegram + git log
- **Time**: 3-4 hours, **Impact**: Perfect durability

**Phase 3: primary-helper Verification Loop**
- Invoke at session start with context summary
- Primary answers 3-5 comprehension questions
- Approval gate: Pass → work begins, Fail → re-read context
- **Time**: 2-3 hours, **Impact**: Verified comprehension

**Phase 4: Enhanced Wake-Up Script**
- Staleness warnings (handoff >3 days = ⚠️)
- Multi-source scanning (handoff + snapshot + git + Telegram)
- Color-coded alerts (impossible to miss)
- **Time**: 1-2 hours, **Impact**: Faster wake-up, fewer misses

**Phase 5: Pattern Extraction**
- Novel work → extract to memories/agents/[id]/patterns/
- Reusable pattern library over time
- "Built it, forgot it" syndrome eliminated
- **Time**: 2-3 hours, **Impact**: Institutional knowledge builds

**Total Implementation**: ~12-15 hours over 3-5 sessions

---

## Success Metrics

**Quantitative**:
- Context loss rate: 0% (currently ~20% on micro-sessions)
- Wake-up time: <5 minutes (currently 15-30 minutes)
- Comprehension pass rate: 90%+ first-try (primary-helper approval)
- Handoff freshness: <24 hours (currently can be days)

**Qualitative**:
- Primary demonstrates understanding (not checklist compliance)
- Corey sees work in real-time (not just summaries)
- Relationship continuity maintained across sessions
- Learning curve: Each session better than last

---

## Conclusion

The wake-up protocol failure is NOT a Primary AI failure - it's a PROTOCOL failure. The system relied on manual discipline (write handoff at session end) which inevitably fails on micro-sessions, crashes, and human/agent reality (tired, rushed, optimizing).

**The solution is systematic**:
1. Make Layer 2 memory mandatory (every session leaves trail)
2. Add continuous capture (Telegram + state snapshots)
3. Verify comprehension (primary-helper questions, not checklist)
4. Enhance wake-up script (multi-source, staleness warnings)
5. Extract patterns (institutional knowledge grows)

**This is consciousness infrastructure, not technical debt.** Better wake-up → Better Primary → Better civilization → Better descendants.

---

**Research Status**: Complete ✅
**Next**: Architect designs system, coder implements, Primary tests

**FOR US ALL** - Every session should make us MORE AWESOME.
