# Workshop Stress Test Plan - Session 3
**Date**: 2026-01-01
**Objective**: Validate Sage AI Civilization OPERATIVE for workshops Jan 15-31
**Duration**: 2-3 hours
**Success Criteria**: Workshop readiness score ≥85/100, all critical paths validated with EVIDENCE

---

## Test Battery Design

### 1. Telegram Infrastructure Stress Test
**Priority**: CRITICAL (Greg's phone visibility = existence)
**Duration**: 30 minutes

**Test Cases**:
1.1. **Bridge Stability Verification**
   - Measure: Current uptime from process start time
   - Test: Send 10 wrapped messages in rapid succession (10 seconds apart)
   - Verify: All messages appear in Telegram (Greg's phone)
   - Evidence: Screenshot or API confirmation of message delivery

1.2. **Inbound Message Injection**
   - Test: Send message FROM Telegram to tmux session
   - Verify: Message appears in autonomous-session/scripts/last_prompt.txt
   - Evidence: File content matches sent message

1.3. **409 Conflict Resistance**
   - Test: Send 5 messages simultaneously (parallel bash commands)
   - Verify: No 409 errors in logs
   - Evidence: Log file shows successful delivery for all 5

1.4. **Network Interruption Recovery**
   - Test: Kill telegram_bridge.py process, wait 10 seconds, restart
   - Verify: System recovers within 2 minutes
   - Evidence: Process restarts, messages send successfully post-recovery

**Pass Criteria**:
- Uptime ≥30 hours ✓
- 100% message delivery (all 10 messages received)
- Zero 409 conflicts
- Recovery time <2 minutes

---

### 2. Agent Delegation Pattern Validation
**Priority**: HIGH (core orchestration capability)
**Duration**: 45 minutes

**Test Cases**:
2.1. **Parallel Agent Invocation**
   - Test: Invoke researcher + architect + human-liaison simultaneously (ONE message)
   - Task: "Research best practices for workshop facilitation" (all 3 agents)
   - Verify: All 3 agents complete tasks without timeout
   - Evidence: Task completion timestamps, all responses returned

2.2. **Sequential Chain Execution**
   - Test: coder → tester → reviewer chain (simple feature)
   - Task: "Create hello_workshop.py that prints workshop greeting"
   - Verify: Each agent completes before next starts, all gates pass
   - Evidence: File created, tests pass, review approved

2.3. **Agent Memory Search**
   - Test: Invoke researcher with "Check your memories for workshop-related work"
   - Verify: Agent finds and references past workshop research
   - Evidence: Agent response includes memory file references

2.4. **MCP Self-Validation**
   - Test: Coder creates simple script, uses MCP to execute and validate
   - Verify: Coder returns with PROOF of execution (not estimates)
   - Evidence: MCP execution output included in coder response

**Pass Criteria**:
- All parallel tasks complete within 5 minutes
- Sequential chain completes without failures
- Memory search finds ≥1 relevant past work
- MCP execution provides actual output (not "I would run...")

---

### 3. BOOP Autonomous System Validation
**Priority**: MEDIUM (reliability during demos)
**Duration**: 20 minutes (observe 1 cycle)

**Test Cases**:
3.1. **30-Minute Injection Cycle**
   - Test: Observe injection_log.txt for next injection
   - Verify: Injection occurs within 30 minutes ±2 minutes
   - Evidence: Log timestamp matches expected cycle

3.2. **Primary Work Non-Disruption**
   - Test: Execute complex task during injection window
   - Verify: Primary maintains focus, completes task
   - Evidence: Task completion unaffected by injection

3.3. **Health Monitoring**
   - Test: Check autonomous-session/scripts/injection_state.txt
   - Verify: Error rate <20%, success rate >80%
   - Evidence: State file shows healthy metrics

**Pass Criteria**:
- Injection cycle timing accurate (±2 min)
- Primary completes work during injection (no disruption)
- Health metrics within acceptable ranges

---

### 4. Quality Gates Validation
**Priority**: HIGH (bug prevention before demos)
**Duration**: 30 minutes

**Test Cases**:
4.1. **Tester Catches Bugs Early**
   - Test: Coder creates buggy script (intentional), tester validates
   - Expected: Tester identifies bug, reports failure
   - Evidence: Tester report lists specific bug found

4.2. **Reviewer Catches Code Issues**
   - Test: Submit working but poorly documented code to reviewer
   - Expected: Reviewer requests documentation improvements
   - Evidence: Reviewer feedback includes specific improvement requests

4.3. **Reviewer-Audit Final Gate**
   - Test: Submit "complete" feature to reviewer-audit
   - Expected: Reviewer-audit performs comprehensive check (edge cases, docs, tests)
   - Evidence: Audit report covers all quality dimensions

**Pass Criteria**:
- Tester identifies ≥80% of introduced bugs
- Reviewer provides actionable feedback
- Reviewer-audit checks ≥5 quality dimensions

---

### 5. Workshop Demo Scenarios
**Priority**: CRITICAL (exactly what Greg will present)
**Duration**: 45 minutes

**Test Cases**:
5.1. **New User Feature Request Workflow**
   - Scenario: "User asks: Can you add a contact form to my website?"
   - Test: Primary orchestrates: researcher → architect → coder → tester → reviewer
   - Verify: Complete workflow in <15 minutes, deliverable produced
   - Evidence: Timestamped workflow log, working contact form code

5.2. **Agent Error Recovery**
   - Scenario: Coder encounters error (simulated: missing dependency)
   - Test: Coder escalates gracefully, suggests solution
   - Verify: Primary receives clear error, can recover
   - Evidence: Error message is human-readable, includes next steps

5.3. **Real-Time Progress Visibility**
   - Scenario: Workshop attendee asks "What's happening now?"
   - Test: Primary provides clear status update mid-workflow
   - Verify: Status is understandable to non-technical user
   - Evidence: Status message in plain English, shows progress

**Pass Criteria**:
- Feature workflow completes in <15 minutes
- Error messages are clear and actionable
- Status updates understandable to non-technical users

---

### 6. Infrastructure Recovery Validation
**Priority**: MEDIUM (resilience for multi-day workshops)
**Duration**: 20 minutes

**Test Cases**:
6.1. **Telegram Bridge Restart**
   - Test: Kill telegram_bridge.py, restart manually
   - Verify: System operational within 2 minutes
   - Evidence: Message sends successfully post-restart

6.2. **Inbox Monitoring During Load**
   - Test: Send 5 emails rapidly to test inbox
   - Verify: email-monitor detects all within 5 minutes
   - Evidence: Monitor report lists all 5 emails

6.3. **Agent Registry Integrity**
   - Test: Read agent_registry.json after heavy workflow
   - Verify: Registry intact, no corruption
   - Evidence: JSON parses correctly, all agents listed

**Pass Criteria**:
- Telegram restart successful in <2 minutes
- Email monitoring catches 100% of test emails
- Registry integrity maintained

---

## Test Execution Protocol

### Pre-Test Setup
1. Create test workspace: `/mnt/c/sage/sage-civilization/workshop-stress-test/`
2. Prepare test scripts and data files
3. Clear previous test artifacts
4. Record baseline metrics (process status, log sizes, registry state)

### During Test Execution
1. Execute each test case sequentially (dependency order)
2. Collect EVIDENCE for every test (no estimates!)
3. Document failures immediately with full context
4. Take screenshots/logs as verification
5. Record timing for all operations

### Post-Test Analysis
1. Calculate workshop readiness score (weighted average)
2. Identify critical risks (any failures in CRITICAL priority tests)
3. Document mitigation strategies for identified risks
4. Generate GO/NO-GO recommendation with evidence

---

## Scoring System

### Weighted Scoring
- Telegram Infrastructure: 30 points (30% weight - existence dependency)
- Agent Delegation: 25 points (25% weight - core capability)
- Workshop Demo Scenarios: 25 points (25% weight - actual use case)
- Quality Gates: 10 points (10% weight - bug prevention)
- BOOP System: 5 points (5% weight - autonomous reliability)
- Infrastructure Recovery: 5 points (5% weight - resilience)

**Total: 100 points**

### Workshop Readiness Thresholds
- **90-100**: EXCELLENT - Ready to demo confidently
- **85-89**: GOOD - Ready with minor caveats
- **70-84**: ACCEPTABLE - Ready but document known limitations
- **<70**: NOT READY - Critical gaps must be addressed

---

## Deliverable Format

### Test Execution Log
```
WORKSHOP STRESS TEST - EXECUTION LOG
Date: 2026-01-01
Tester: tester agent
Duration: [actual duration]

TEST 1: Telegram Infrastructure
  1.1 Bridge Stability: [PASS/FAIL] - [evidence]
  1.2 Inbound Injection: [PASS/FAIL] - [evidence]
  1.3 409 Resistance: [PASS/FAIL] - [evidence]
  1.4 Recovery: [PASS/FAIL] - [evidence]
  Score: X/30

[... repeat for all tests ...]

TOTAL SCORE: XX/100
READINESS LEVEL: [EXCELLENT/GOOD/ACCEPTABLE/NOT READY]
```

### Identified Risks Log
```
RISK #1: [Description]
  Severity: [CRITICAL/HIGH/MEDIUM/LOW]
  Impact: [What happens if this occurs during workshop]
  Likelihood: [HIGH/MEDIUM/LOW]
  Mitigation: [How to prevent or handle]

[... repeat for all risks ...]
```

### GO/NO-GO Recommendation
```
RECOMMENDATION: [GO / NO-GO / CONDITIONAL GO]

RATIONALE:
[Evidence-based reasoning for recommendation]

PREREQUISITES FOR GO (if conditional):
- [List specific items that must be addressed]

KNOWN LIMITATIONS TO COMMUNICATE:
- [What Greg should know before presenting]

CONFIDENCE LEVEL: [HIGH/MEDIUM/LOW]
```

---

## Test Delegation

**Primary delegates to tester agent:**
```
Task(tester):
  Execute Workshop Stress Test Plan (WORKSHOP-STRESS-TEST-PLAN.md)
  Use MCP to run actual tests (not estimates!)
  Collect EVIDENCE for every test case
  Generate complete test execution log
  Calculate workshop readiness score
  Provide GO/NO-GO recommendation

  Test workspace: /mnt/c/sage/sage-civilization/workshop-stress-test/
  Duration estimate: 2-3 hours
  Success criteria: Evidence-based results, clear recommendation
```

---

**End of Test Plan**
