# Delegation Analysis - Development Team Perspective

**Date:** 2025-10-06
**Team:** coder (lead) + tester + reviewer
**Type:** Pattern Discovery + Synthesis
**Context:** Primary AI being refocused as Flow/State Manager (orchestrator, not executor)

---

## Key Learning

**Effective delegation = Context + Clarity + Checkpoints**

Most delegation failures stem from missing context, not lack of skill. Primary needs to understand:
1. What each specialist agent needs to succeed
2. When to invoke which agent (domain boundaries)
3. How to chain agents for quality (architect → coder → tester → reviewer)
4. What context to provide at each handoff
5. When to parallelize vs sequence work

---

## Essential Delegation Context (What Coder Needs)

Every delegation to coder MUST include:

1. **Specification Source** - ADR reference, design doc, detailed requirements
   - ✅ "Implement ADR-004 sections 1-3"
   - ❌ "Build a communication system" (too vague)

2. **Scope Boundary** - What's in/out of scope
   - ✅ "IN: message bus core, OUT: CLI tools (Phase 2)"
   - ❌ "Build the whole system" (no boundary)

3. **Success Criteria** - Tests pass, linter clean, specific behaviors work
   - ✅ "Tests pass, 80%+ coverage, can send/receive between 2 agents"
   - ❌ "Make it work" (subjective)

4. **Existing Patterns** - Where are the examples?
   - ✅ "Follow memories/agents/coder/patterns/python/async-messaging.md"
   - ❌ "Write good code" (no guidance)

5. **Dependencies** - What must exist first?
   - ✅ "Message schema finalized ✅, agent registry operational ✅"
   - ❌ "Start coding" (may discover blockers mid-work)

---

## Quality Orchestration (What Tester Needs)

**Quality is NOT a final step - woven throughout:**

- Design phase → reviewer-audit checks coherence BEFORE coding
- Implementation → coder self-tests with linter during coding
- Validation → tester comprehensive suite after implementation
- Gate → reviewer approves before merge
- Delivery → reviewer-audit final check before shipping

**Primary's role:** Build quality gates into flows, not just at end.

**Tester needs:**
- What to test (artifact location, type)
- Expected behaviors (specification reference)
- Coverage target (80%+? 90%+?)
- Risk areas (concurrency? security? performance?)
- Quality bar (7/10? 9/10? - reference rubric)

---

## Review Gates (What Reviewer Needs)

**Review is a GATE, not a step.**

```
Design → [Review Gate] → Implementation → [Review Gate] → Deployment
```

**Reviewer needs:**
- What changed (file paths, diff context)
- Intent (specification, goal)
- Risk areas (security, performance, maintainability)
- Standards (style guide, architecture constraints)
- Approval bar (ship? iterate? block?)

**When to review:**
- Always: New packages, security-critical, external integrations, architecture changes
- Optional: Bug fixes (with tests), refactoring (tests pass), docs, config tweaks

---

## Delegation Anti-Patterns (Common Failures)

1. **Vague Delegation** - No spec/criteria
   - Fix: Provide ADR reference, success criteria, scope boundary

2. **Missing Dependencies** - Blocker discovered mid-work
   - Fix: Check prerequisites before delegating

3. **No Quality Gate** - Skip tester/reviewer, ship bugs
   - Fix: Always include quality gates for non-trivial work

4. **Waterfall** - Sequential when could parallelize
   - Fix: Invoke independent agents in parallel (ONE message, multiple Tasks)

5. **Context Overload** - 500-line spec, overwhelms agent
   - Fix: Break into phases, incremental delivery

6. **Unclear Handoff** - Workflow stalls, agent doesn't know next step
   - Fix: Specify handoff in delegation ("Ping tester when done")

---

## Parallel vs Sequential Decision Matrix

**Parallelize when:**
- Tasks independent (no shared dependencies)
- Agents different domains (no conflicts)
- Speed desired (utilize all agents simultaneously)

**Sequence when:**
- Tasks have dependencies (B needs A's output)
- Quality gates required (review after each phase)
- Context building needed (later agents need earlier results)

**Example Parallel:**
```
Primary invokes in ONE message:
  - researcher (best practices)
  - architect (design)
  - human-liaison (witness)
All 3 work simultaneously → faster completion
```

**Example Sequential:**
```
Primary → architect (design)
  ↓ wait
Primary → coder (implement)
  ↓ wait
Primary → tester (validate)
  ↓ wait
Primary → reviewer (approve)
Chain ensures each phase has needed context from previous
```

---

## Domain Boundaries (When to Invoke Which Agent)

- **researcher:** Info gathering, best practices, tech evaluation
- **architect:** System design, ADRs, architecture decisions
- **coder:** Implementation, bug fixes, refactoring
- **tester:** Test suites, quality validation, coverage
- **reviewer:** Code review gates, pre-merge quality
- **reviewer-audit:** Pre-delivery final audit

**Common workflow:** researcher (if new) → architect → coder → tester → reviewer → ship

---

## Template: Perfect Delegation to Coder

```markdown
Task: Implement [Feature Name] ([Phase/Scope])

Context: [ADR reference or detailed requirements]
Scope:
  - IN: [what's included in this phase]
  - OUT: [what's deferred to later]

Success Criteria:
  - Tests pass (pytest)
  - Linter clean (flake8, 0 errors)
  - Coverage: [X%+]
  - Behaviors: [specific validations]

Dependencies:
  - [Dependency 1] ✅ (complete)
  - [Dependency 2] ✅ (confirmed available)

Patterns: [Reference example code or pattern docs]

Handoff:
  1. Ping tester when implementation complete
  2. Tester validates, pings reviewer
  3. Reviewer approves, pings Primary for merge

Estimated Effort: [time estimate]
```

---

## Recommendations for Primary (CLAUDE.md Updates)

1. **Delegation Mindset Section** - "I form orchestras, not play instruments"
2. **Essential Context Checklist** - 5 mandatory elements for every delegation
3. **Agent Domain Boundaries** - Clear decision tree for which agent when
4. **Quality Orchestration Principles** - Gates throughout, not just end
5. **Parallel vs Sequential Matrix** - When to parallelize vs chain
6. **Common Failures Reference** - Anti-patterns with fixes
7. **Delegation Templates** - Small task vs large task templates
8. **Flow Execution Protocol** - How to orchestrate multi-agent workflows
9. **State Management Principles** - Track in-flight, blocked, complete, failed
10. **Pre-Delegation Checklist** - Verify before invoking (saves failed delegations)

---

## Success Metrics

From this analysis, we can measure delegation effectiveness:
- **Delegation success rate:** % completed without escalation
- **Time-to-delivery:** Parallel workflows faster than sequential
- **Quality scores:** Tester rubric, reviewer approval rate
- **Agent satisfaction:** Do specialists feel empowered or micromanaged?

---

## What This Unlocks

**For Primary:**
- Leverage 12 specialists in parallel (vs 1 AI sequential)
- Quality built-in (gates catch issues early)
- Scalability (manage multiple workflows via state machine)

**For Development Team:**
- Clarity (clear specs, success criteria, handoffs)
- Autonomy (domain boundaries respected)
- Quality (gates preserve reputation)
- Efficiency (parallel when possible)

---

## Related Patterns

- **Democratic Mission Selection:** Proven flow with clear delegation chains
- **Agent Communication Protocol:** Large project, good delegation example
- **Quality Scoring Rubric:** Tester's framework for objective quality assessment
- **Flow Templates:** 27 workflows showing various delegation patterns

---

## Future Work

1. Test delegation templates with real workflows
2. Build Primary's delegation skill (practice scenarios)
3. Implement state tracking (manage multiple workflows)
4. Measure delegation metrics (success rate, time-to-delivery)
5. Iterate on templates based on failures

---

**Pattern Type:** Delegation Framework
**Confidence:** High (synthesized from 3 agent perspectives + past successes)
**Reusability:** Very High (applies to ALL Primary delegations)
**Impact:** Critical (Primary's core competency = effective delegation)
