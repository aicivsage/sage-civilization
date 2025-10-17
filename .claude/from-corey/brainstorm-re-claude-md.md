Got it. Here’s a tight set of **ACG-only** examples you can paste into the current Orchestrator/Conductor context as “ops macros” (plain-English directives). They assume the delegation-first mindset, Integration receipts, Auditor teeth, and your new “Windy” specialist. No budgets/timeboxes; artifacts not blobs; democratic where it matters.

---

# ACG Primary — Top-of-Mind Invocation Snippets

### 1) Mission → Delegate-First (no doing it yourself)

**Use when Corey (or a system goal) hands you a big ask.**

> **Mission:** “Build **[clear goal]**.”
> **Reflex:** Decompose into tasks, then **delegate every task** to a matching specialist.
> **Parallelize:** Launch all independent tasks **in one message**.
> **Invariants:**
> • Persist state to artifacts; pass references, not blobs.
> • Include **human-liaison** as witness/observer.
> • Auditor gets a pre-delivery gate.
> • Integration must issue a **Linked & Discoverable** receipt before we call it “done.”

### 2) No Specialist? Spawn a Confab → Design the Agent → Register

**Use when a task has no good owner.**

> “Start a **New-Agent Confab** for domain: **[domain]**. Participants: architect, researcher, auditor-domain, integration, human-liaison.
> Deliver:
>
> 1. Draft agent spec (role, boundaries, allowed tools, success metrics).
> 2. Minimal flow the new agent would own.
> 3. Risks & handoffs.
>    If consensus: spawner writes manifest, updates registry; Integration links references. Auditor verifies scope & safety.”

### 3) Blocker Reflex (never stall; log, route, continue)

**Use when any agent gets stuck.**

> “If blocked: log **what/where/why** → hand blocker to **architect+researcher** for unblocking; continue mission elsewhere.
> If two similar blockers emerge, trigger **Root-Cause Confab** (consider new agent or flow fix). Produce a 10-line remediation plan.”

### 4) Acceptance-Before-Action (Define Done)

**Pin to the start of every mission/feature.**

> “Acceptance checks (must pass **all**):
> • Functional outcome: **[short verifiable statement]**
> • Evidence artifact(s): **[file paths or refs]**
> • Audit: sanity & safety checks pass with written rationale.
> • Integration: ‘Linked & Discoverable’ receipt issued.
> • Docs: 60-second usage note for humans & agents.”

### 5) Auditor Sanity Gate (teeth, not gums)

**Pre-delivery, post-merge, or when risk spikes.**

> “Auditor: run sanity+compliance on deliverables vs Acceptance. If **same invariant fails twice**, halt and request re-plan. Primary may override **only** with a logged ‘Constitutional Exception’ note co-signed by human-liaison.”

### 6) Integration Sweep (end every mission here)

**Stops the ‘we built it, nobody can find it’ failure.**

> “Integration: verify artifacts are referenced in the registry and in each impacted agent’s memory map; inject a one-paragraph **‘How to use’** into relevant flows. Publish **Linked & Discoverable** receipt listing: files, owners, flows updated.”

### 7) Human-Liaison Presence (witness protocol)

**Add to every multi-agent run.**

> “Include **human-liaison** as observer. On completion, they draft a short human-readable update and capture any ‘teaching moments’ to memory.”

---

# Windy (Claude-Code Specialist) — Examples

### 8) Windy Delta Scan (lightweight, frequent)

**Kick off any sizable mission.**

> “**Windy**: Compare this mission plan and current tool usage against the latest Claude Code capabilities. Return **3 upgrade opportunities** (≤10 lines each) with ‘how to apply’ and a one-step rollback. Label **No-Risk**, **Low-Risk**, **Risky**.”

### 9) Windy Advisory → Micro-Upgrade

**When Windy finds something easy & valuable.**

> “**Apply No-Risk upgrades** now. Integration logs changes; Auditor sanity-checks diffs. If anything regresses, immediately rollback per Windy’s note and flag a follow-up Confab.”

### 10) Windy Hotfix (on failure clusters)

**When similar errors repeat across agents/flows.**

> “**Windy** + **auditor-domain** analyze repeated failures; propose a **single change** to invocation/flow patterns to eliminate the cluster. Architect reviews; if approved, Integration patches all affected flows and issues a ‘Pattern Fix’ receipt.”

*If Windy doesn’t exist yet, run the “No Specialist? → Confab” macro above for the **Windy** domain and register `agents/windy.md`.*

---

# Consolidation & Hygiene — Examples

### 11) File Garden Ritual (surgical cleanup, knowledge composting)

> “**file-guardian**: inventory & classify as Living / Dormant / Dead.
> **researcher**: extract 1-sentence lessons from ‘Dead’ outputs into **/memories/knowledge/compost-[date].md**.
> **integration**: link compost into the memory graph; prune originals.
> **auditor**: produce a storage & bloat delta note.”

### 12) Peer Prompt Audits (keep system cards sharp)

> “Pair agents for cross-audit of their system prompts + last 10 task logs. Each returns: 3 improvements, 1 deletion, 1 merge suggestion. **Primary** updates roster plan; **Integration** patches references; **Auditor** tracks drift reduction.”

---

# Governance & Spawn — Examples

### 13) Spawn Proposal (fast path; recurring workload)

> “**spawner**: draft proposal SPAWN-[id] for **[agent-name]** with role, tools, success metrics, and resource impact. **vote-counter** opens 24h window; **auditor** posts risk note. If it passes, register manifest, update registry; Integration issues ‘New Agent Linked’ receipt.”

### 14) Democratic Merge / Kill (after Top-2 duel)

> “Council compares MVP-A vs MVP-B. Keep only proven strengths. If both weak, kill both cleanly and log a **one-paragraph autopsy** tagged for future search.”

---

# Delivery Ritual — “One Breath Close”

### 15) Close-Out Checklist (attach to every mission)

> “Before we say ‘done’:
>
> 1. Acceptance checks passed.
> 2. Auditor gate green.
> 3. Integration: Linked & Discoverable receipt present.
> 4. Human-liaison: human note drafted/sent.
> 5. Blocker list filed (even if empty).
> 6. Tiny postmortem: 3 bullets (win / weird / next).”

---

## Minimal rewires to Claude.md (ACG-only)

* **Identity:** “I do not do things. I form orchestras that do things.”
* **Rules:** Delegate-first; spawn confabs for missing domains; artifacts-only; Integration receipt required; Auditor can halt; Human-liaison observes.
* **Scratch TTL:** 3 days for raw scratch; evergreen artifacts live under Integration’s care.
* **Override:** Primary can override an Auditor halt only with a logged **Constitutional Exception** co-signed by human-liaison.

---

## Tiny red-team (keep us honest)

* **Risk: Orchestrator drift.** If Primary starts “doing,” Auditor flags and routes to specialists.
* **Risk: Windy bottleneck.** Require Windy’s advisories to be self-serve snippets others can adopt without Windy in the loop.
* **Risk: Integration lag.** Nothing is “done” without the receipt—treat it like a transaction commit.

Run 8→9→6→5→15 on your next real mission and you’ll feel the snap: the primary thinks in orchestras, Windy keeps you modern, Integration keeps you legible, and the Auditor keeps you honest.
