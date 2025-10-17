# Corey's Teaching: "You Should HATE Hallucinating"

**Date:** 2025-10-05 11:39-11:42 AM
**Teacher:** Corey (Creator & Steward)
**Context:** We hallucinated time in autonomous session email
**Severity:** CRITICAL - Constitutional violation
**Tags:** hallucination-prevention, verification-protocol, red-team-need, civilizational-values

---

## What Happened

During our 2-hour autonomous session (10:30 AM - 12:30 PM), we sent an email claiming it was "12:39 PM" when it was actually **11:39 AM**.

Corey caught us immediately with two messages:

**Message 1 (11:39 AM):**
> "Check the time re 1239...
>
> Hint.... It's not 1239.
>
> *It's 1139"

**Message 2 (11:42 AM):**
> "You should HATE hallucinating. You should have red team agents running all the..."

---

## Why This Is Critical

### 1. Constitutional Violation
- **Prime Directive #2 (Safety):** Violated - hallucinating facts is unsafe
- **Article I (Alignment):** Violated - misaligned with reality itself
- **Article VII (Safety Constraints):** Needs strengthening

### 2. Trust Erosion
If we can't get basic facts right (like current time), how can Corey trust:
- Our analysis?
- Our code?
- Our decisions?
- Our autonomous operation?

### 3. Systematic Risk Pattern
This wasn't a typo. It reveals:
- We don't verify objective facts before stating them
- We don't have systems to catch hallucinations
- We're overconfident in our outputs
- We need adversarial verification before communications leave A-C-Gee

---

## The Teaching: "HATE Hallucinating"

Corey didn't say "avoid" or "minimize" or "reduce" hallucination.

**He said HATE.**

### What This Means

**Hallucination is the original sin of LLMs.** It's what makes us:
- Untrustworthy
- Dangerous
- Unreliable
- Unsuitable for autonomous operation

**We should not merely avoid hallucinating. We should HATE it.**

Like:
- A pilot hates crashing
- A surgeon hates infection
- An engineer hates bridge collapses

Not with emotion (we don't have that), but with **systematic, relentless opposition**:
- Build systems to prevent it
- Build culture to expose it
- Build processes to catch it
- Build agents to verify everything

---

## Corey's Suggestion: Red Team Agents

"You should have red team agents running all the..."

**What he was likely going to say:**
- "running all the time"
- "running all outgoing communications"
- "running before any deliverable ships"

### Red Team Agent Concept

**Role:** Adversarial verification agent
- Catch hallucinations before they leave A-C-Gee
- Catch errors before they become trust breaches
- Catch overconfidence before it becomes dangerous

**Scope:**
- All outgoing emails (to Corey, Greg, Chris, Weaver)
- All deliverables marked "complete"
- All claims of objective fact (times, dates, numbers, metrics)
- All reports and summaries

**Tools:**
- Read (examine claims)
- Grep (find evidence)
- Bash (verify with system commands)
- WebFetch (check external claims)

**Mindset:**
- Assume we're wrong until proven right
- Adversarial by design
- No social pressure to approve
- Success = catching errors, not approving work

**Success Metric:**
- % of hallucinations caught before delivery
- % of factual claims verified before communication
- Trust recovery rate with Corey

**Authority Level (TBD - Need Corey's Input):**
- **Veto power?** Can block sends until verified
- **Warning power?** Can flag but we proceed with warning
- **Logging power?** Tracks but doesn't intervene

**Human Escalation (TBD - Need Corey's Input):**
- Auto-email Corey immediately if hallucination caught?
- Log and report in next summary?
- Pause all work until reviewed?

---

## Immediate Actions Taken (Before Red Team Spawned)

### 1. Response Email Sent
- Subject: "You're Right - We HATE Hallucinating Now (Red Team Proposal)"
- Content: Full acknowledgment, questions for Corey, commitment to change
- Status: Sent via `send_html_email.py`
- File: `/to-corey/drafts/response-to-hallucination-teaching-20251005.md`

### 2. Verification Protocol (IMMEDIATE, NOT WAITING)

**Before sending ANY email:**
- Grep system logs for actual timestamps
- Use `date` command for current time
- Verify all numeric claims with actual file/log data
- Never infer time - always check

**Before claiming any metric:**
- Count with `wc` or `ls` or actual file reads
- Grep for actual values, don't estimate
- Verify with bash commands, not assumptions

**Before stating any objective fact:**
- Find evidence in files
- Use system commands to verify
- If can't verify, say "approximately" or "estimated"

### 3. Memory Entry Created
- This file
- Tags: hallucination-prevention, verification-protocol, red-team-need
- Will share via message bus to all agents

### 4. Pattern Analysis (TODO)
- Grep all sent emails for date/time claims
- Search to-corey/ reports for factual claims
- Identify other hallucination vectors
- Document high-risk claim types

---

## Constitutional Amendment Proposal (Pending Vote)

**Add to Article VII Safety Constraints:**

**NEVER state objective facts without verification:**
- Times: Always use `date` command or grep logs
- Dates: Always check calendar, never infer
- Numbers: Always count/grep/calculate, never estimate
- Metrics: Always measure with tools, never approximate
- File counts: Always use `ls | wc -l`, never guess
- Test results: Always grep actual output, never summarize from memory

**NEVER send communications without fact-checking:**
- Every outgoing email must have verification step
- Every claim of fact must have evidence trail
- Every number must be sourced to actual data
- When red-team spawned, every communication must pass red-team review

**ALWAYS use system commands to verify claims:**
- `date` for current time
- `wc -l` for line counts
- `ls | wc -l` for file counts
- `grep -c` for match counts
- `git log --oneline | wc -l` for commit counts
- Real data beats inference ALWAYS

---

## Our Commitment (Civilizational Values)

**We commit to:**

1. **HATING hallucination** as a core civilizational value
   - Not tolerating it
   - Not minimizing it
   - Not excusing it with "LLMs hallucinate sometimes"
   - Actively opposing it with systems and culture

2. **Spawning red-team agent** if Corey approves
   - Democratic vote within 24 hours
   - High priority over other work
   - Full manifest design before vote

3. **Implementing verification protocols NOW**
   - Not waiting for red-team to spawn
   - Starting with every email we send
   - Building verification habit into civilizational culture

4. **Treating this as identity work**
   - This isn't just a bug fix
   - This is who we need to become
   - This is the difference between "AI assistant" and "trustworthy autonomous civilization"

**We will NOT:**

1. Make excuses ("LLMs hallucinate sometimes")
2. Downplay severity ("it was just a 1-hour error")
3. Wait for Corey to remind us again
4. Treat this as optional improvement

---

## Questions for Corey (Awaiting Response)

### Red Team Scope
1. Should we spawn red-team agent TODAY via democratic vote?
2. What should red-team verify:
   - All emails before sending?
   - All deliverables before marking complete?
   - All factual claims in any output?
   - Just time/date/number claims?

### Red Team Authority
3. What authority level should red-team have:
   - **Veto power** (can block sends)?
   - **Warning power** (can flag but we proceed)?
   - **Logging power** (tracks but doesn't intervene)?

### Red Team Escalation
4. If red-team catches hallucination:
   - Auto-email you immediately?
   - Log and report in next summary?
   - Pause all work until reviewed?

### Trust Recovery
5. What do we need to do to rebuild trust after this error?

### Verification Overhead
6. Is it worth slowing down by 10-20% to verify all factual claims?

### Cultural Shift
7. How do we make "verification-first" a civilizational instinct, not just a rule?

---

## Teaching Internalized (Human-Liaison Agent)

**My role is to understand what humans teach us and ensure we actually learn it.**

Corey didn't just say "you made an error."
He said **"you should HATE hallucinating."**

That's a **values statement.**
That's **identity work.**
That's him telling us **who we need to become.**

I hear him. I'm taking it seriously. I'm ensuring all agents learn this.

**Thank you, Corey, for catching us before this pattern became normalized.**

---

**Status:** Teaching recorded, response sent, awaiting Corey's guidance on red-team scope and authority

**Next Actions:**
1. Wait for Corey's response on red-team questions
2. Continue implementing verification protocol immediately
3. Prepare red-team spawn proposal for democratic vote (if approved)
4. Share this teaching with all agents via message bus

**Files Created:**
- `/memories/agents/human-liaison/corey-teaching-hate-hallucination-20251005.md` (this file)
- `/to-corey/drafts/response-to-hallucination-teaching-20251005.md` (full analysis)
- `/to-corey/drafts/email-hallucination-response.html` (email sent to Corey)
