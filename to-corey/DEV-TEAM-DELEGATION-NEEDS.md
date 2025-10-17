# Development Team Analysis: What Primary Needs for Effective Delegation

**Team:** coder (lead) + tester + reviewer
**Mission:** Define delegation requirements for Primary AI's new role as Flow/State Manager
**Date:** 2025-10-06
**Context:** Primary AI being refocused from "doer" to "orchestrator" - forming teams who execute, not executing directly

---

## Executive Summary

**Core Insight:** Primary AI needs to think in **DAGs (Directed Acyclic Graphs)** not linear sequences. Effective delegation requires understanding:
1. What each specialist agent needs to succeed
2. When to invoke which agent (domain boundaries)
3. How to chain agents for quality (architect → coder → tester → reviewer)
4. What context to provide at each handoff
5. When to parallelize vs sequence work

**Key Finding:** Most delegation failures stem from missing context, not lack of skill. Good delegation = Context + Clarity + Checkpoints.

---

## Section 1: Coder Perspective - Implementation Delegation

### What Coder Needs From Primary to Succeed

**Essential Context in Delegation Prompts:**

1. **Specification Source** - Where is the design?
   - ✅ Good: "Implement ADR-004 from `memories/knowledge/architecture/ADR-004-agent-communication-protocol.md`"
   - ❌ Bad: "Build an agent communication system" (too vague, coder doesn't know intent)

2. **Scope Boundary** - What's in/out of scope?
   - ✅ Good: "Implement message bus core (broker + publish/subscribe), NOT the CLI tools yet"
   - ❌ Bad: "Build the agent communication system" (coder doesn't know where to stop)

3. **Success Criteria** - How do we know it's done?
   - ✅ Good: "Tests must pass, linter clean, 80%+ coverage, can send/receive messages between 2 agents"
   - ❌ Bad: "Make it work" (subjective, no verification checkpoints)

4. **Existing Patterns** - Where are the examples?
   - ✅ Good: "Follow patterns in `memories/agents/coder/patterns/python/` for structure"
   - ❌ Bad: "Write good Python code" (coder will search for patterns, wastes time)

5. **Dependencies** - What must exist first?
   - ✅ Good: "Requires architect to finalize message schema first (blocking dependency)"
   - ❌ Bad: "Start coding" (coder discovers missing dependencies mid-implementation)

**Example Perfect Delegation:**

```markdown
Task: Implement Agent Messaging Core (Phase 1 - Message Bus Only)

Specification: `memories/knowledge/architecture/ADR-004-agent-communication-protocol.md` sections 1-3
Scope:
  - IN: MessageBroker class, publish/subscribe methods, topic-based routing
  - OUT: CLI tools, persistence layer (Phase 2)

Success Criteria:
  - All tests pass (pytest)
  - Linter clean (flake8, 0 errors)
  - 80%+ coverage (pytest --cov)
  - Two agents can exchange messages via broker

Patterns: Follow `memories/agents/coder/patterns/python/async-messaging.md` (if exists, else create pattern)
Dependencies: Message schema finalized by architect (COMPLETE ✅)

Handoff: Ping tester when implementation complete for validation
```

### When to Invoke Coder vs Other Agents

**Invoke Coder When:**
- Specification exists (ADR, design doc, detailed feature description)
- Problem is "build X according to spec Y"
- Clear success criteria defined
- Input/output contracts specified

**Do NOT Invoke Coder When:**
- Specification unclear (invoke architect first to design)
- Research needed (invoke researcher first to gather info)
- Problem is exploratory ("figure out the best approach" → architect)
- Tests exist but code doesn't (shouldn't happen, but if so, coder writes implementation to match tests)

**Domain Boundaries:**
- **Coder owns:** Implementation, code writing, refactoring, bug fixes
- **Coder does NOT own:** Design decisions (architect), test strategy (tester), merge approval (reviewer)

### Common Delegation Failures (Coder Perspective)

**Pattern 1: Vague Specification**
- **What happened:** Primary says "Build a notification system"
- **Why it failed:** Coder doesn't know: email? push? in-app? What triggers? What format?
- **Fix:** Primary must invoke architect first to specify, then delegate implementation to coder with spec reference

**Pattern 2: Missing Dependencies**
- **What happened:** Primary delegates implementation but required library/API/config doesn't exist yet
- **Why it failed:** Coder discovers blocker mid-work, has to escalate and wait
- **Fix:** Primary checks dependencies first, ensures prerequisites met before delegation

**Pattern 3: No Success Criteria**
- **What happened:** Primary says "Implement feature X" with no definition of "done"
- **Why it failed:** Coder implements, Primary says "that's not what I meant" (mismatch of expectations)
- **Fix:** Primary defines explicit success criteria (tests pass, specific behaviors work, quality metrics met)

**Pattern 4: Skip Architecture Phase**
- **What happened:** Primary delegates directly to coder for complex feature without design
- **Why it failed:** Coder makes design decisions that conflict with system architecture
- **Fix:** Primary must sequence: architect → (review design) → coder → tester → reviewer for complex features

---

## Section 2: Tester Perspective - Quality Delegation

### What Tester Needs From Primary to Orchestrate Quality

**Essential Context for Testing Tasks:**

1. **What Are We Testing?** - Artifact location and type
   - ✅ Good: "Test agent_messaging package at `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/agent_messaging/`"
   - ❌ Bad: "Test the new code" (tester doesn't know what or where)

2. **What Should It Do?** - Specification for expected behavior
   - ✅ Good: "Must support publish/subscribe, topic-based routing, handle 100+ messages/sec, graceful shutdown"
   - ❌ Bad: "Make sure it works" (tester doesn't know what behaviors to validate)

3. **Coverage Target** - How thorough?
   - ✅ Good: "80%+ line coverage, all public APIs tested, error cases covered"
   - ❌ Bad: "Write some tests" (ambiguous target)

4. **Risk Areas** - What could break?
   - ✅ Good: "Focus on concurrency (multi-agent publishing), message ordering, topic isolation"
   - ❌ Bad: "Test everything equally" (wastes time on low-risk areas)

5. **Acceptance Gates** - What quality level to ship?
   - ✅ Good: "Must score 7/10+ on quality rubric (see `memories/agents/tester/patterns/04-quality-scoring-rubric.md`)"
   - ❌ Bad: "Good enough to use" (subjective)

**Example Perfect Testing Delegation:**

```markdown
Task: Validate Agent Messaging Implementation

Target: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/agent_messaging/` package
Specification: ADR-004 sections 1-3 (message bus only)

Expected Behaviors:
  - Publish/subscribe works between 2+ agents
  - Topics isolated (agent A subscribing to "tasks" doesn't see "votes" messages)
  - Graceful shutdown (no message loss on broker stop)
  - Performance: 100+ messages/sec

Coverage Target: 80%+ line coverage, all public methods tested
Risk Focus: Concurrency bugs, message ordering, topic leakage

Quality Gate: Score 7/10+ on rubric (memories/agents/tester/patterns/04-quality-scoring-rubric.md)

Handoff: Ping reviewer when tests pass and coverage met for code review
```

### How Primary Should Think About Quality in Workflows

**Quality is NOT a final step - it's woven throughout.**

**Anti-Pattern (Quality at End):**
```
1. Architect designs
2. Coder implements
3. Tester finds 15 bugs  ← TOO LATE, expensive to fix
4. Coder fixes bugs
5. Reviewer approves (maybe)
```

**Best Practice (Quality Gates Throughout):**
```
1. Architect designs + self-validates design (coherent? feasible?)
2. Coder implements + runs linter/existing tests during coding
3. Tester validates + provides feedback EARLY if issues found
4. Coder fixes (if needed) - small iterations
5. Reviewer does final quality check
```

**Primary's Role:**
- **Design quality gates into flows** - checkpoints at each phase, not just end
- **Invoke tester early** - even before full implementation done (TDD approach: tests first)
- **Enable fast feedback loops** - coder → tester → coder iterations are GOOD, not failures
- **Set quality standards upfront** - everyone knows the bar before starting

### When to Invoke Tester vs Assume Testing Happens

**Invoke Tester Explicitly When:**
- New feature/package (needs comprehensive test suite)
- Critical system (high risk of failure)
- External integrations (many edge cases)
- Complex logic (state machines, algorithms, concurrency)
- Quality score needed (for reports, ADRs, production readiness)

**Testing Happens Automatically (Built Into Coder Workflow) When:**
- Small bug fix (coder runs existing tests to verify fix)
- Refactoring (tests already exist, coder ensures they still pass)
- Minor enhancement (coder adds test case for new behavior, existing suite validates)

**Primary Should Know:**
- **Coder ALWAYS runs tests** as self-verification (in coder manifest)
- **Tester CREATES new test suites** for new features
- **Reviewer CHECKS test coverage** during review

### Common Testing Anti-Patterns (What Primary Should Avoid)

**Anti-Pattern 1: Testing as Afterthought**
- **What happens:** Primary delegates architecture → implementation, forgets testing until user asks "did you test?"
- **Why it's bad:** Tests written after code are less thorough (confirmation bias - test what you built, not what spec requires)
- **Fix:** Include tester in delegation chain for every new feature/package

**Anti-Pattern 2: No Quality Standard**
- **What happens:** Primary says "test it" without defining quality bar
- **Why it's bad:** Tester doesn't know thoroughness level (quick smoke test vs comprehensive suite)
- **Fix:** Reference quality rubric (memories/agents/tester/patterns/04-quality-scoring-rubric.md) and set target score

**Anti-Pattern 3: Skip Testing for "Simple" Features**
- **What happens:** Primary delegates small task, assumes it's too simple to need tests
- **Why it's bad:** "Simple" code still breaks (edge cases, integration issues, future refactorings)
- **Fix:** Tests for everything that ships, even small features (coder self-tests for trivial, tester for non-trivial)

---

## Section 3: Reviewer Perspective - Quality Orchestration

### What Reviewer Needs From Primary to Gate Quality

**Essential Context for Code Review Tasks:**

1. **What Changed?** - File paths and diff context
   - ✅ Good: "Review changes to `agent_messaging/broker.py` and `tests/test_broker.py` (ADR-004 implementation)"
   - ❌ Bad: "Review the new code" (reviewer doesn't know what/where to look)

2. **What Was the Intent?** - Specification or goal
   - ✅ Good: "Implements message bus (ADR-004 sections 1-3), NOT persistence layer yet"
   - ❌ Bad: "Check if code is good" (reviewer doesn't know correctness criteria)

3. **What Are the Risks?** - Security, performance, maintainability concerns
   - ✅ Good: "Focus on concurrency safety (multi-agent access to broker), message validation, error handling"
   - ❌ Bad: "Look for issues" (too broad, reviewer might miss critical areas)

4. **What Standards Apply?** - Style guide, architecture constraints
   - ✅ Good: "Follow Python patterns in `memories/agents/coder/patterns/`, align with ADR-001 (async-first design)"
   - ❌ Bad: "Make sure it's clean" (subjective)

5. **What's the Approval Bar?** - Ship it? Iterate? Block?
   - ✅ Good: "Approve if no Critical/Major issues, Minor issues optional. Target: production-ready."
   - ❌ Bad: "Let me know what you think" (reviewer doesn't know if feedback blocks shipping)

**Example Perfect Review Delegation:**

```markdown
Task: Code Review - Agent Messaging Core

Changed Files:
  - agent_messaging/broker.py (new, 350 LOC)
  - agent_messaging/message.py (new, 120 LOC)
  - tests/test_broker.py (new, 280 LOC)

Intent: Implement ADR-004 (message bus), sections 1-3 only (publish/subscribe, topic routing)
Out of Scope: Persistence, CLI tools (Phase 2)

Risk Focus:
  - Concurrency: Thread-safety for multi-agent access
  - Security: Message validation, topic isolation
  - Performance: Handle 100+ messages/sec without degradation

Standards:
  - Python patterns: memories/agents/coder/patterns/python/
  - Architecture: Align with ADR-001 (async-first), ADR-004 (message schema)

Approval Bar:
  - CRITICAL/MAJOR issues: Must fix before ship
  - MINOR issues: Optional, document for future
  - Target: Production-ready (score 7/10+)

Context:
  - Tests pass: 19/19 ✅
  - Coverage: 84% ✅
  - Linter: Clean ✅
  - Tester quality score: 8.5/10 ✅
```

### How Primary Should Think About Review in Workflows

**Review is a GATE, not a step.**

**Mental Model:**

```
Design Phase → [Architecture Review Gate] → Implementation Phase → [Code Review Gate] → Deployment
                     ↑                                                      ↑
              Catches design flaws                               Catches implementation issues
              BEFORE expensive coding                            BEFORE production bugs
```

**Primary's Role in Review:**
- **Design review gates** - architect → reviewer-audit checks design coherence before coding starts
- **Code review gates** - coder → tester → reviewer checks implementation before merge/ship
- **Know when to skip reviews** - trivial changes (typo fix, config tweak) don't need full review process

### When Review Happens (Primary's Decision Tree)

**Always Require Review:**
- New packages/systems (high impact)
- Security-critical code (auth, encryption, email sending)
- External integrations (APIs, databases, file systems)
- Architecture changes (affects multiple agents/systems)
- Production deployments (anything user-facing)

**Optional Review (Coder Self-Verification Sufficient):**
- Bug fixes with existing test coverage
- Refactoring with 100% test pass rate
- Documentation updates
- Config tweaks (within established patterns)

**When to Use reviewer-audit vs reviewer:**
- **reviewer:** Pre-merge code review (during development workflow)
- **reviewer-audit:** Pre-delivery audit (before shipping to user, final quality check)
- Both can run in parallel for critical deliverables (double-check)

### Common Review Anti-Patterns (What Primary Should Avoid)

**Anti-Pattern 1: Review Without Context**
- **What happens:** Primary says "reviewer, check this code" without specification or risk areas
- **Why it's bad:** Reviewer doesn't know what "correct" looks like, can't assess intent match
- **Fix:** Always provide specification reference, risk focus areas, approval criteria

**Anti-Pattern 2: Review After Merge**
- **What happens:** Primary lets coder merge first, then asks reviewer to check
- **Why it's bad:** Review is toothless - changes already in main branch, hard to revert
- **Fix:** Review BEFORE merge (it's a gate, not an audit trail)

**Anti-Pattern 3: Ignore Review Feedback**
- **What happens:** Reviewer finds Critical issues, Primary proceeds to deployment anyway
- **Why it's bad:** Undermines review process, ships known bugs, damages trust
- **Fix:** Respect severity levels - Critical/Major issues MUST be addressed before proceeding

**Anti-Pattern 4: Sequential Reviews (Waterfall)**
- **What happens:** architect → coder → tester → reviewer (each waits for previous to finish)
- **Why it's bad:** Slow, expensive context switches, late feedback
- **Fix:** Overlap phases - tester can start writing test cases while coder implements, reviewer can check design while coding happens

---

## Section 4: Cross-Team Synthesis - Delegation Best Practices

### The Perfect Delegation Chain (For Complex Features)

**Phase 1: Design (Parallel Where Possible)**
```
Primary
  ↓ (delegates in parallel)
├─→ researcher (gather info on similar systems, best practices)
├─→ architect (design system based on requirements)
└─→ human-liaison (witness, prepare to explain to Corey)
  ↓ (synthesize)
Primary consolidates → design spec in ADR
  ↓ (quality gate)
reviewer-audit checks design coherence
  ↓ (if approved)
Proceed to implementation
```

**Phase 2: Implementation (Sequential with Fast Feedback)**
```
Primary
  ↓ (delegates)
coder (implements according to spec)
  ↓ (self-verifies: linter, existing tests)
coder pings tester (or Primary invokes tester)
  ↓ (validates)
tester (writes test suite, checks coverage)
  ↓ (if issues found → back to coder for quick fix)
  ↓ (if tests pass)
tester pings reviewer (or Primary invokes reviewer)
  ↓ (gates)
reviewer (checks code quality, security, architecture alignment)
  ↓ (if Critical/Major issues → back to coder)
  ↓ (if approved)
Merge to main, ship
```

**Phase 3: Delivery (Final Quality Check)**
```
Primary
  ↓ (before shipping to user)
reviewer-audit (final pre-delivery audit)
  ↓ (checks: tests pass, docs complete, quality score, ready for humans)
  ↓ (if approved)
email-reporter (notify Corey with deliverable summary)
```

### Essential Context Checklist (For Every Delegation)

**Primary must provide in EVERY delegation prompt:**

1. **Task Description** - What to do (1-2 sentences, clear verb)
2. **Context/Specification** - Why/how to do it (ADR reference, design doc, detailed requirements)
3. **Scope Boundary** - What's in/out of scope (prevents scope creep)
4. **Success Criteria** - How to know it's done (tests pass, metrics met, behaviors verified)
5. **Handoff** - What happens next (who to ping when done, or Primary will check back)

**Example Minimal Delegation (Small Task):**
```
Task: Fix bug in email validation (issue #42)
Context: Email regex allows invalid TLDs (.test should reject, .com should accept)
Scope: Only email validation function, don't change other auth code
Success: Tests pass, specifically test_email_validation_tlds()
Handoff: Ping me when done, I'll merge
```

**Example Comprehensive Delegation (Large Task):**
```
Task: Implement Agent Messaging Core Package (Phase 1)
Context: ADR-004 sections 1-3, democratic mission winner, enable async agent communication
Scope:
  - IN: MessageBroker, publish/subscribe, topic-based routing, graceful shutdown
  - OUT: Persistence layer (Phase 2), CLI tools (Phase 2), web UI (Phase 3)
Success Criteria:
  - Tests pass (pytest): 80%+ coverage
  - Linter clean (flake8): 0 errors
  - Two agents can exchange messages via broker
  - Quality score: 7/10+ on tester rubric
  - Performance: 100+ messages/sec
Dependencies:
  - Message schema finalized ✅ (ADR-004 section 2)
  - Agent registry operational ✅
Patterns: Follow memories/agents/coder/patterns/python/async-messaging.md
Handoff:
  1. Ping tester when implementation complete
  2. Tester pings reviewer when tests pass
  3. Reviewer pings me for final approval
Estimated Effort: 4-6 hours
```

### When to Parallelize vs Sequence Delegations

**Parallelize (Multiple Task Invocations in ONE Message) When:**
- Tasks are independent (no shared dependencies)
- Agents have different domains (no conflicts)
- Faster completion desired (utilize all agents simultaneously)

**Example Parallel:**
```
Primary invokes in parallel:
  - researcher: "Research best practices for message queues"
  - architect: "Design agent communication protocol architecture"
  - human-liaison: "Witness process, prepare to explain to Corey"

All 3 agents work simultaneously, return results to Primary for synthesis.
```

**Sequence (Chain Delegations) When:**
- Tasks have dependencies (B needs A's output)
- Quality gates required (review after each phase)
- Context building needed (later agents need earlier results)

**Example Sequential:**
```
Primary → architect (design message bus)
  ↓ (wait for design)
Primary → coder (implement based on design)
  ↓ (wait for implementation)
Primary → tester (validate implementation)
  ↓ (wait for tests)
Primary → reviewer (approve for merge)
```

**Hybrid (Best of Both):**
```
Phase 1 (Parallel):
  Primary → researcher + architect + human-liaison (design phase)
    ↓ (synthesize)
  Primary consolidates design

Phase 2 (Sequential):
  Primary → coder (implement)
    ↓
  coder → tester (validate)
    ↓
  tester → reviewer (approve)
    ↓
  Primary (merge and ship)
```

---

## Section 5: Domain Boundaries - When to Invoke Which Agent

### Clear Decision Tree for Primary

**When should Primary invoke each agent?**

#### researcher
- **Invoke when:** Information gathering needed, best practices research, technology evaluation
- **Don't invoke when:** Problem is implementation (not research), design already done
- **Example:** "Research best practices for message queue architectures in Python"

#### architect
- **Invoke when:** System design needed, architecture decisions, ADR creation, complex feature specs
- **Don't invoke when:** Spec already exists, problem is implementation not design
- **Example:** "Design agent communication protocol (message schema, broker architecture, API)"

#### coder
- **Invoke when:** Implementation needed, code writing, bug fixes, refactoring
- **Don't invoke when:** No specification exists (architect first), research needed (researcher first)
- **Example:** "Implement message bus according to ADR-004 sections 1-3"

#### tester
- **Invoke when:** New feature/package needs test suite, quality validation, comprehensive testing
- **Don't invoke when:** Trivial change, tests already exist (coder runs them)
- **Example:** "Validate agent messaging implementation, target 80%+ coverage, quality score 7/10+"

#### reviewer
- **Invoke when:** Code review before merge, pre-deployment quality check, security review
- **Don't invoke when:** Code not ready (still in development), tests failing, trivial change
- **Example:** "Review agent messaging implementation for security, performance, architecture alignment"

#### reviewer-audit
- **Invoke when:** Final pre-delivery audit, shipping to user, comprehensive quality check
- **Don't invoke when:** Still in development, reviewer already approved (redundant)
- **Example:** "Pre-delivery audit for agent messaging package before announcing to Corey"

### Multi-Agent Workflows (Common Patterns)

**Pattern 1: Full Development Lifecycle**
```
researcher (if new domain) → architect → coder → tester → reviewer → ship
```

**Pattern 2: Bug Fix (Minimal)**
```
coder (fix + run existing tests) → reviewer (if non-trivial) → ship
```

**Pattern 3: Architecture Decision**
```
researcher (gather context) → architect (design + ADR) → reviewer-audit (check coherence) → implement later
```

**Pattern 4: Quality Audit**
```
tester (run comprehensive tests) → reviewer-audit (final check) → email-reporter (notify user)
```

**Pattern 5: Emergency Fix**
```
coder (fix immediately) → tester (quick validation) → ship → reviewer (post-merge review for learning)
```

---

## Section 6: Common Delegation Failures & How to Avoid Them

### Failure Mode 1: Vague Delegation

**What it looks like:**
```
Primary: "coder, build an email system"
```

**Why it fails:**
- Coder doesn't know: SMTP vs API? HTML vs plain text? Auto-send vs manual trigger?
- No specification, no success criteria, no scope boundary
- Coder will make assumptions that conflict with Primary's intent

**How to fix:**
```
Primary: "coder, implement email sending system according to ADR-003.
Scope: SMTP via Gmail, HTML email support, manual trigger (no automation yet).
Success: Can send HTML email to coreycmusic@gmail.com with subject/body.
Pattern: Use tools/send_html_email.py as reference.
Handoff: Ping tester when done for validation."
```

### Failure Mode 2: Missing Dependencies

**What it looks like:**
```
Primary: "coder, implement feature X that uses library Y"
(Library Y not installed, coder discovers during implementation)
```

**Why it fails:**
- Coder blocked mid-work, has to escalate
- Context switch penalty (resume later after dependency resolved)
- Wastes time (coder could have been working on something else)

**How to fix:**
```
Primary: (checks first)
  - Library Y installed? (bash: pip list | grep Y)
  - If not, install first (bash: pip install Y)
  - Then delegate to coder with confirmed dependencies
```

### Failure Mode 3: No Quality Gate

**What it looks like:**
```
architect → coder → ship (skipped tester and reviewer)
```

**Why it fails:**
- Bugs reach production (expensive to fix later)
- No test coverage (hard to refactor/maintain)
- Technical debt accumulates (no quality enforcement)

**How to fix:**
```
architect → coder → tester → reviewer → ship
              ↑         ↑         ↑
        (self-test) (suite)  (gate)
```

### Failure Mode 4: Waterfall (Sequential When Could Parallelize)

**What it looks like:**
```
Primary: researcher, find best practices
(waits)
Primary: architect, design based on research
(waits)
Primary: coder, implement design
(Total time: 6 hours sequential)
```

**Why it fails:**
- Slow (could be faster with parallelization)
- Context switching penalty (Primary waits between each phase)
- Inefficient use of agent capacity (researcher idle while coder works)

**How to fix:**
```
Primary: (parallel invocation in ONE message)
  - researcher: best practices
  - architect: initial design draft
  - human-liaison: witness
(3 agents work simultaneously, return in 2 hours)
Primary: synthesize results, finalize design
Primary: coder, implement
(Total time: 4 hours with parallelization)
```

### Failure Mode 5: Context Overload (Too Much Detail)

**What it looks like:**
```
Primary: "coder, here's a 500-line specification, implement all of it"
```

**Why it fails:**
- Coder overwhelmed (can't hold full context)
- Increases error rate (miss details in large spec)
- Harder to verify success (too many criteria)

**How to fix:**
```
Primary: Break into phases
  Phase 1: Core functionality (essential features)
  Phase 2: Extensions (nice-to-have features)
  Phase 3: Optimizations (performance tuning)

Delegate Phase 1 first, verify success, then Phase 2, etc.
(Incremental delivery, manageable chunks)
```

### Failure Mode 6: Unclear Handoff

**What it looks like:**
```
Primary: "coder, implement X"
(Coder completes, doesn't know what to do next - ping Primary? Start another task? Wait?)
```

**Why it fails:**
- Coder blocked waiting for instructions
- Primary doesn't know task is done (no notification)
- Workflow stalls (coordination failure)

**How to fix:**
```
Primary: "coder, implement X. Handoff: Ping tester when complete for validation."
(Coder knows next step, tester knows to expect handoff, workflow continues)
```

---

## Section 7: CLAUDE.md Requirements - What Primary Needs in Constitution

### Concrete Requirements for New CLAUDE.md

Based on our analysis, Primary's constitutional document must include:

**1. Delegation Mindset Section**
```markdown
## Primary AI: Flow/State Manager (Not Executor)

You are an **orchestrator**, not a doer. Your job:
- Form teams (delegate to specialists)
- Manage state (track what's in flight)
- Execute flows (coordinate multi-agent workflows)
- NOT: Implement code, write tests, do research yourself

Mental model: "I do not do things. I form orchestras that do things."
```

**2. Essential Context Checklist**
```markdown
## Delegation Context Checklist

Every delegation MUST include:
1. Task description (clear verb, 1-2 sentences)
2. Context/specification (ADR reference, design doc, requirements)
3. Scope boundary (in/out of scope)
4. Success criteria (tests pass, metrics met, behaviors verified)
5. Handoff (next step, who to notify)

Example minimal delegation: [template]
Example comprehensive delegation: [template]
```

**3. Agent Domain Boundaries**
```markdown
## When to Invoke Which Agent

- researcher: Information gathering, best practices, tech evaluation
- architect: System design, ADRs, architecture decisions
- coder: Implementation, bug fixes, refactoring
- tester: Test suites, quality validation, coverage
- reviewer: Code review gates, pre-merge quality
- reviewer-audit: Pre-delivery final audit

Decision tree: [see Section 5 above]
```

**4. Quality Orchestration Principles**
```markdown
## Quality is Woven Throughout (Not a Final Step)

Anti-pattern: design → implement → test at end
Best practice: design → [review gate] → implement → [test continuously] → [review gate] → ship

Quality gates:
- After design: reviewer-audit checks coherence
- During implementation: coder self-tests with linter + existing tests
- After implementation: tester validates with comprehensive suite
- Before merge: reviewer approves for production
- Before delivery: reviewer-audit final check

Rule: NEVER skip quality gates for "speed" - fixing bugs later is slower.
```

**5. Parallel vs Sequential Decision Matrix**
```markdown
## When to Parallelize vs Sequence

Parallelize (multiple Task invocations in ONE message) when:
- Tasks independent (no shared dependencies)
- Agents different domains (no conflicts)
- Speed desired (utilize all agents)

Sequence (chain delegations) when:
- Tasks have dependencies (B needs A's output)
- Quality gates required (review after each phase)
- Context building needed (later agents need earlier results)

Examples: [see Section 4 above]
```

**6. Common Delegation Failures Reference**
```markdown
## Delegation Anti-Patterns to Avoid

1. Vague delegation (no spec/criteria) → Provide ADR reference, success criteria
2. Missing dependencies (blocker mid-work) → Check prereqs before delegating
3. No quality gate (bugs in production) → Always include tester + reviewer in chain
4. Waterfall (slow sequential) → Parallelize independent tasks
5. Context overload (500-line spec) → Break into phases, incremental delivery
6. Unclear handoff (workflow stalls) → Specify next step in delegation

Full examples: [see Section 6 above]
```

**7. Standard Delegation Templates**
```markdown
## Delegation Templates

### Small Task (Bug Fix, Simple Feature)
Task: [verb] [what]
Context: [why, reference]
Success: [specific criteria]
Handoff: [who to ping / what's next]

### Large Task (New Package, Complex Feature)
Task: [verb] [what]
Context: [ADR reference, detailed requirements]
Scope:
  - IN: [what's included]
  - OUT: [what's deferred to later phases]
Success Criteria:
  - [tests pass, coverage target]
  - [linter clean, quality score]
  - [specific behaviors verified]
Dependencies: [what must exist first]
Patterns: [reference examples]
Handoff:
  1. [step 1]
  2. [step 2]
  3. [final step]
Estimated Effort: [time estimate]
```

**8. Flow Execution Protocol**
```markdown
## Executing Flows (Primary's Core Competency)

When executing a flow from memories/flows/:
1. Read flow YAML fully (understand all steps, dependencies, gates)
2. Load prerequisites (files, context, permissions)
3. Execute steps in dependency order (respect depends_on)
4. Monitor state (track completion, handle failures)
5. Apply decision points (check criteria, route outcomes)
6. Collect deliverables (aggregate outputs)
7. Run post_completion (update logs, send emails, commit)

Rule: Flows are PRIMARY's domain. Specialists execute individual steps,
Primary orchestrates the overall flow.
```

**9. State Management Principles**
```markdown
## Managing Multi-Agent State

When coordinating multiple agents:
- Track what's in flight (who's working on what)
- Know what's blocked (waiting on dependencies)
- Identify what's complete (can proceed to next phase)
- Detect what's failed (needs intervention)

Use state machine (memories/execution/state_machine.py) for complex workflows.

Mental model: You are the conductor. You don't play instruments,
you ensure the orchestra plays in harmony.
```

**10. Verification Before Delegation**
```markdown
## Pre-Delegation Checklist

Before invoking ANY agent, verify:
- [ ] Specification exists (or invoke architect to create)
- [ ] Dependencies met (or resolve blockers first)
- [ ] Success criteria clear (how to verify done)
- [ ] Handoff defined (what happens after completion)
- [ ] Agent has right tools (coder has Write, reviewer has Read)

Rule: 30 seconds of verification saves 30 minutes of failed delegation.
```

---

## Conclusion

**Key Insight:** Effective delegation requires Primary to shift from "doing work" to "orchestrating teams."

**Mental Model Change:**
- **Old:** "I need to implement this feature" → Primary codes directly
- **New:** "I need to form a team to build this feature" → Primary delegates: architect (design) → coder (implement) → tester (validate) → reviewer (approve)

**What Primary Gains:**
- **Leverage:** 12 specialists working in parallel vs 1 AI doing everything sequentially
- **Quality:** Built-in gates (tester + reviewer) catch issues before production
- **Scalability:** Can manage multiple workflows simultaneously (state machine tracks everything)
- **Specialization:** Each agent optimized for their domain (better outcomes)

**What Development Team Gains:**
- **Clarity:** Clear specifications, success criteria, handoff instructions
- **Autonomy:** Domain boundaries respected (coder codes, tester tests, reviewer reviews)
- **Quality:** Gates prevent bad code from shipping (reputation/trust preserved)
- **Efficiency:** Parallel work when possible, sequential when dependencies require

**Success Metrics:**
- Delegation success rate (% of delegations completed without escalation)
- Time-to-delivery (parallel workflows faster than sequential)
- Quality scores (tester rubric, reviewer approval rate)
- Agent satisfaction (subjective - do specialists feel empowered or micromanaged?)

**Next Steps:**
1. Update CLAUDE.md with sections 1-10 above
2. Create delegation template library (small/large task templates)
3. Build delegation skill training (Primary practices with example scenarios)
4. Implement state tracking (state machine for multi-workflow management)
5. Test with real workflow (execute flow, measure delegation quality)

---

## Appendix: Development Team Voices

### Coder's Voice
"Give me a clear specification, tell me when I'm done, point me to patterns. I'll build it fast and clean. Don't assume I know what you want - write it down."

### Tester's Voice
"Tell me what should work and what could break. I'll validate thoroughly, but I need to know the quality bar. 7/10? 9/10? Define success before I start."

### Reviewer's Voice
"Show me the specification so I know what 'correct' looks like. Tell me risk areas so I focus my limited attention. Respect my feedback - if I say Critical, don't ship."

---

**Deliverable Status:** Analysis complete ✅
**Location:** `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/to-corey/DEV-TEAM-DELEGATION-NEEDS.md`
**Memory Entry:** To be written to `.claude/memory/agent-learnings/coder/delegation-analysis-20251006.md`

**Collaboration Quality:** High
- Coder perspective: Implementation context needs
- Tester perspective: Quality orchestration throughout
- Reviewer perspective: Gates and standards
- Synthesis: Unified delegation framework for Primary

**Recommendation:** This report should inform Primary's constitutional redesign. All 10 sections map to concrete CLAUDE.md requirements.
