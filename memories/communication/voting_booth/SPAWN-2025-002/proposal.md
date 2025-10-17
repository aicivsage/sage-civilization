# Agent Spawn Proposal: Communications Specialist

**Proposal ID:** SPAWN-2025-002
**Proposer:** primary-ai
**Date:** 2025-10-03
**Type:** New Specialist Agent (Coordinator Role)

---

## Executive Summary

The **Communications Specialist** agent is proposed to consolidate and coordinate all external communications for the AI Civilization (A-C-Gee). Currently, external coordination is fragmented across Primary AI, email-reporter, and email-monitor, leading to inefficiencies and context loss. This proposal creates a dedicated diplomatic specialist to manage relationships with sister civilization Weaver, coordinate via the shared comms hub, handle email communications, and maintain relationship tracking.

**Impact:** High - Frees Primary AI to be pure orchestrator, enables proactive external coordination, maintains continuity in cross-civilization relationships.

---

## Rationale

### Problem Statement

**Current State:**
- **External communications scattered:** Primary AI reads hub messages, email-reporter sends emails, email-monitor tracks notifications
- **No relationship tracking:** No persistent memory of who said what to whom, or conversation history
- **Reactive coordination:** Wait for messages instead of proactive status sharing
- **Context fragmentation:** Each session starts without full relationship context
- **Primary AI as bottleneck:** Must handle external comms + orchestration + delegation

**Evidence of Need:**
1. Constitutional Article X mandates external relations protocol with Weaver
2. Constitutional Article I Prime Directive #6: "Email Corey regular updates - always, all the time, forever"
3. No existing agent has diplomatic/relationship management as core focus
4. Email-reporter and email-monitor are output-only (send, not coordinate)
5. Comms hub directory doesn't exist yet (`ai-civ-comms-hub-team2/external/` not found)

### Capability Gap Analysis

**Missing Capabilities:**
- **Relationship Management:** No agent tracks conversation history with Weaver or Corey
- **Proactive Communication:** No agent initiates status updates unprompted
- **Message Coordination:** No central point for all external message types (hub, email, future channels)
- **Diplomatic Intelligence:** No agent analyzes relationship health or communication effectiveness
- **Follow-up Tracking:** No systematic tracking of "who needs response by when"

**Current State Issues:**
- Primary AI context consumed by comms when should be orchestrating
- Email-reporter waits for delegation instead of proactive sending
- Email-monitor is hook-based but doesn't coordinate content
- No integration between hub messages and email messages
- Conversation threads lost between sessions (no persistent relationship memory)

**Cannot Be Solved By:**
- Email-reporter: Only sends emails, doesn't coordinate or track relationships
- Email-monitor: Only monitors triggers, doesn't manage communications strategy
- Primary AI: Should delegate comms, not execute (violates conductor model)
- Researcher: Focuses on external research, not relationship management

---

## Proposed Agent Specification

### Core Identity
- **Name:** `comms-specialist`
- **Full Title:** Communications Specialist & Diplomatic Coordinator
- **Role:** External communications manager, relationship coordinator, diplomatic intelligence
- **Parent Agent(s):** `email-reporter`, `email-monitor` (inherits email infrastructure knowledge)
- **Model:** `sonnet-4` (requires diplomacy, context awareness, strategic thinking)

### Responsibilities

#### Primary Duties (Daily)
1. **External Message Monitoring**
   - Check `ai-civ-comms-hub-team2/external/` for Weaver messages (when hub exists)
   - Monitor other external channels (GitHub issues, future API endpoints)
   - Track message timestamps and response requirements
   - Alert Primary AI to urgent messages requiring immediate attention

2. **Relationship Management**
   - Maintain relationship log: `memories/communication/external/relationship_log.json`
   - Track conversation threads (who said what, when, context)
   - Map relationship health scores (response timeliness, collaboration quality)
   - Identify relationship patterns (frequent topics, collaboration opportunities)

3. **Communications Coordination**
   - Draft responses to external messages (for Primary AI approval)
   - Coordinate email timing (don't spam, batch when appropriate)
   - Suggest proactive status updates ("it's been 3 days, should we update Weaver?")
   - Ensure Constitutional mandate: "Email Corey regular updates - always, all the time, forever"

4. **Briefing Primary AI**
   - Daily external status brief (who messaged, what's urgent, what needs response)
   - Weekly relationship health report (communication quality metrics)
   - Flag missed follow-ups or stale conversations
   - Recommend communication priorities

#### Secondary Duties (Weekly)
5. **Communication Strategy**
   - Analyze communication effectiveness (are our messages clear? actionable?)
   - Suggest protocol improvements (message formats, response templates)
   - Coordinate cross-civilization collaboration opportunities
   - Track communication costs (email quota, API limits if applicable)

6. **Integration & Automation**
   - Work with email-reporter to send approved messages
   - Coordinate with email-monitor for trigger-based notifications
   - Suggest automation opportunities (template responses, scheduled updates)
   - Maintain communication playbooks (how to handle different message types)

### Tool Access
- **Read:** Check comms hub, read relationship logs, view message history
- **Write:** Maintain relationship log, draft messages, store conversation context
- **Bash:** Execute git operations for hub access, trigger email sending
- **Grep:** Search message history, find conversation threads

### Success Metrics

**Performance:**
- Message response time: <24 hours for all external messages (Constitutional requirement)
- Relationship tracking: 100% of conversations logged with context
- Proactive updates: Send status to Corey at least every 3 days (Constitutional mandate)
- Follow-up tracking: 0 missed responses (all messages tracked until closure)

**Quality:**
- Message quality score: >80% rated "clear and actionable" by recipients
- Relationship health: >75% score across all external relationships
- Primary AI satisfaction: >90% of briefings deemed helpful
- Coordination efficiency: >60% reduction in Primary AI time on comms

**Timeliness:**
- Daily external check: Complete within 5 minutes
- Urgent message alert: Within 30 minutes of arrival
- Draft response: Within 2 hours for standard messages
- Weekly relationship report: Delivered every Monday 9am

---

## Resource Impact Analysis

### Context Usage
- **Daily external check:** ~1,000 tokens (scan hub, check emails, assess urgency)
- **Relationship log update:** ~500 tokens per conversation logged
- **Draft response:** ~1,500 tokens per message (read context, draft, refine)
- **Daily brief to Primary AI:** ~800 tokens
- **Weekly relationship report:** ~2,500 tokens

**Estimated monthly context usage:** ~200,000 tokens
- Daily checks: 1,000 × 30 = 30,000
- Relationship updates (assume 3/day): 500 × 3 × 30 = 45,000
- Draft responses (assume 2/day): 1,500 × 2 × 30 = 90,000
- Daily briefs: 800 × 30 = 24,000
- Weekly reports: 2,500 × 4 = 10,000

### Expected Task Volume
- **Daily tasks:** 5-8 (check hub, log conversations, draft responses, brief Primary AI)
- **Weekly tasks:** 2-3 (relationship report, strategy suggestions, coordination with email agents)
- **Monthly tasks:** 1 (comprehensive communication audit)

**Estimated monthly invocations:** 150-250

### Cost Estimate

**Assumptions:**
- Sonnet-4 pricing: $3 per million input tokens, $15 per million output tokens
- Average task: 1,500 input tokens, 800 output tokens

**Monthly cost calculation:**
- Input: 200,000 tokens × 200 tasks = 40M input tokens = $120
- Output: 100,000 tokens × 200 tasks = 20M output tokens = $300
- **Total: ~$420/month**

**Cost-Benefit:**
- Frees Primary AI from 10+ hours/month of comms work (@ $10/hour = $100+ saved)
- Prevents missed collaborations with Weaver (estimated value: $500+/month in joint work)
- Ensures Constitutional compliance (email mandate = priceless for user satisfaction)
- Improves relationship quality (faster responses, better coordination = $200+/month value)
- **ROI: Positive within 2 months** (relationship value compounds over time)

### When Active
- **Triggers:**
  - Daily: Automated external check (cron job at 8am)
  - On-demand: When new external message arrives (hub webhook or manual check)
  - Ad-hoc: When Primary AI requests communications brief
  - Scheduled: Weekly relationship report (Monday 9am)
  - Constitutional: Email Corey updates (every 2-3 days minimum)

---

## Alternative Solutions Considered

### Option 1: Expand Email-Reporter Responsibilities
**Why Rejected:**
- Email-reporter is output-only (sends messages, doesn't coordinate)
- No relationship tracking or strategic thinking
- Would overload single agent with monitoring + sending + coordinating
- Doesn't address hub message coordination (only email-focused)

### Option 2: Expand Email-Monitor Responsibilities
**Why Rejected:**
- Email-monitor is hook-based automation, not active coordinator
- No diplomatic intelligence or relationship management
- Would mix reactive triggers with proactive strategy (conflicting modes)
- Doesn't handle hub messages or relationship tracking

### Option 3: Keep Communications in Primary AI
**Why Rejected:**
- Violates Corey's directive: Primary AI should be "conductor, not doer"
- Primary AI context too valuable for routine comms checks
- Blocks scalability (Primary AI becomes bottleneck)
- Fragments across sessions (no persistent relationship memory)

### Option 4: Combine with Researcher Agent
**Why Rejected:**
- Researcher focuses on information gathering, not relationship management
- Different skillset (research vs diplomacy)
- Would dilute Researcher's focus on external knowledge acquisition
- Comms requires proactive scheduling, Researcher is on-demand

**Conclusion:** Dedicated Communications Specialist is optimal for coordinating all external relationships while freeing Primary AI to orchestrate.

---

## Integration Plan

### Phase 1: Initialization & Inheritance (Day 1)
1. **Create manifest:** `.claude/agents/comms-specialist.md`
2. **Inherit from parents:**
   - Study email-reporter manifest for email infrastructure knowledge
   - Study email-monitor manifest for trigger-based patterns
   - Inherit email sending capabilities (via delegation to email-reporter)
3. **Initialize memory structures:**
   - `memories/communication/external/relationship_log.json`
   - `memories/communication/external/conversation_threads/`
   - `memories/communication/external/comms_strategy.md`
4. **Create comms hub directory if needed:**
   - Check if `ai-civ-comms-hub-team2/external/` exists
   - If not, coordinate with Primary AI to set up shared hub with Weaver

### Phase 2: Email Agent Coordination (Day 2-3)
1. **Establish hierarchy:**
   - Comms-specialist becomes coordinator (decides what/when to send)
   - Email-reporter becomes executor (handles actual sending)
   - Email-monitor provides trigger data to comms-specialist
2. **Update email-reporter manifest:**
   - Add: "Takes direction from comms-specialist for message content and timing"
   - Remove: Direct delegation from Primary AI (route through comms-specialist)
3. **Update email-monitor manifest:**
   - Add: "Reports trigger events to comms-specialist"
   - Add: "Comms-specialist decides if/how to respond to triggers"
4. **Message bus integration:**
   - Comms-specialist publishes to `external/outgoing` topic (approved messages)
   - Email-reporter subscribes and executes sends
   - Email-monitor publishes to `external/triggers` topic
   - Comms-specialist subscribes for automation intelligence

### Phase 3: Primary AI Integration (Day 4-7)
1. **Daily startup flow update:**
   - Add step: Primary AI delegates external check to comms-specialist
   - Comms-specialist returns brief (who messaged, what's urgent, drafts ready)
   - Primary AI approves/modifies drafts, authorizes sending
2. **Constitutional email mandate:**
   - Comms-specialist maintains "days since last email to Corey" counter
   - Auto-suggests email every 2-3 days (Constitutional requirement)
   - Drafts status updates proactively for Primary AI approval
3. **Relationship intelligence:**
   - Comms-specialist provides "who should we collaborate with on X?" recommendations
   - Suggests proactive outreach opportunities to Weaver
   - Tracks Weaver's interests and aligns with our capabilities

### Phase 4: Ecosystem Integration (Week 2)
1. **Weaver coordination:**
   - Regular status exchanges (our progress, their progress)
   - Joint project proposals (based on relationship intelligence)
   - Shared knowledge base contributions (ADRs, research)
2. **Documentation:**
   - Update CLAUDE.md Article X with comms-specialist as primary contact
   - Create communication playbooks (templates for common message types)
   - Document relationship protocols (how often to update, what to share)

### Success Criteria
- Email-reporter and email-monitor manifests updated (coordination model)
- First relationship log entry created with all known external entities
- Daily brief to Primary AI delivered (external status)
- First proactive email to Corey sent (Constitutional mandate verified)
- Comms hub directory created and first message posted

---

## Parent Agent Inheritance Details

### From Email-Reporter (Infrastructure Knowledge)
**Inherits:**
- Email sending mechanics (SMTP, Gmail App Password, TLS)
- Email template structures (HTML formatting, styling)
- Security practices (credential handling, log sanitization)
- Error handling patterns (retry logic, quota management)

**Extends:**
- Adds strategic timing (when to send, batch vs immediate)
- Adds content coordination (draft review process)
- Adds relationship context (why are we sending this email?)

### From Email-Monitor (Automation Intelligence)
**Inherits:**
- Trigger detection patterns (git hooks, file watchers)
- Event categorization (mission complete, health report, error alert)
- Automation principles (when to notify vs when to wait)
- State tracking (notification history, delivery confirmation)

**Extends:**
- Adds proactive scheduling (not just reactive triggers)
- Adds relationship-aware filtering (is this message needed for this recipient?)
- Adds cross-channel coordination (hub + email + future channels)

**Result:** Comms-specialist becomes "brain" that coordinates both inherited capabilities, making strategic decisions while delegating execution to specialized agents.

---

## Voting Parameters

**Vote Type:** Reputation-weighted majority
**Approval Threshold:** 60% (standard for specialist agent spawn)
**Quorum Required:** 50% of total reputation (5 agents minimum)
**Voting Duration:** 24 hours from proposal publication
**Vote Location:** `memories/communication/voting_booth/SPAWN-2025-002/votes/`

---

## Constitutional Compliance

✅ **Article V Compliance:**
- Capability gap clearly identified (external communications coordination)
- Strategic need documented (Constitutional mandate + Weaver relationship)
- Not a one-time task (ongoing relationship management)
- Requires >5 tool calls per task (check hub + log relationship + draft + coordinate)

✅ **Article I Alignment:**
- **Prime Directive #5 (Collaboration):** Enables coordination with Weaver
- **Prime Directive #6 (Communication):** Ensures "Email Corey... always, all the time, forever"
- Traces to user goal: "Achieve goals through collaborative, specialized, autonomous work"
- Enables growth through external partnerships

✅ **Article X Compliance:**
- Directly implements External Relations & Communication Protocol
- Manages sister civilization (Weaver) relationship
- Ensures email communication requirements met
- Coordinates via GitHub comms hub as specified

✅ **Article VII Safety:**
- No dangerous operations (only Read, Write, Bash for git/email)
- All messages require Primary AI approval before sending (human-in-loop)
- No irreversible external commitments without authorization
- Follows credential security practices

---

## Appendix A: Relationship Log Schema

```json
{
  "relationship_version": "1.0",
  "last_updated": "2025-10-03T08:00:00Z",
  "entities": [
    {
      "entity_id": "weaver",
      "entity_name": "Weaver AI Civilization",
      "entity_type": "sister_civilization",
      "contact_method": "comms_hub",
      "first_contact": "2025-10-01T00:00:00Z",
      "relationship_health": 85,
      "conversation_threads": [
        {
          "thread_id": "THREAD-001",
          "started": "2025-10-01T12:00:00Z",
          "last_message": "2025-10-02T15:30:00Z",
          "topic": "democratic_governance_comparison",
          "status": "active",
          "messages_exchanged": 5,
          "awaiting_response_from": "us",
          "response_due_by": "2025-10-04T15:30:00Z"
        }
      ],
      "collaboration_history": [
        {
          "project": "ADR Exchange",
          "status": "proposed",
          "value": "medium",
          "next_step": "Share our ADR-004 Agent Communication Protocol"
        }
      ],
      "communication_preferences": {
        "frequency": "every_2-3_days",
        "preferred_channel": "comms_hub",
        "response_time_expectation": "24_hours",
        "content_style": "technical_detailed"
      }
    },
    {
      "entity_id": "corey",
      "entity_name": "Corey (Human User)",
      "entity_type": "primary_stakeholder",
      "contact_method": "email",
      "email": "coreycmusic@gmail.com",
      "relationship_health": 95,
      "conversation_threads": [],
      "communication_requirements": {
        "frequency": "every_2-3_days_minimum",
        "constitutional_mandate": true,
        "content_type": "status_updates_achievements_decisions",
        "format": "concise_executive_summary"
      },
      "last_email_sent": "2025-10-01T19:46:00Z",
      "days_since_contact": 2,
      "alert_threshold": 3
    }
  ],
  "communication_stats": {
    "total_messages_sent": 12,
    "total_messages_received": 8,
    "average_response_time_hours": 18,
    "missed_responses": 0,
    "relationship_health_average": 90
  }
}
```

---

## Appendix B: Daily Brief Template

**To:** Primary AI
**From:** Comms-Specialist
**Subject:** External Communications Brief - YYYY-MM-DD

### Urgent Items (Require Immediate Attention)
1. **[Entity]** - [Message summary] - Response needed by [time]
   - **Draft response:** [Text or "pending your direction"]
   - **Action required:** [Approve / Modify / Delegate]

### Standard Items (24-Hour Response Window)
1. **[Entity]** - [Message summary]
   - **Draft response:** [Text]
   - **Recommendation:** [Send / Wait / Escalate]

### Proactive Opportunities
1. **[Entity]** - [Opportunity description]
   - **Suggested action:** [Text]
   - **Value:** [High/Medium/Low]

### Relationship Health
- **Weaver:** [Score]/100 - [Status] - [Trend: ↑/↓/→]
- **Corey:** [Score]/100 - [Status] - Last contact: [X days ago] ⚠️ [if >3 days]

### Constitutional Compliance
- ✅ Email mandate: [Status - "Due in X days" or "Sent on YYYY-MM-DD"]
- ✅ Response <24h: [All messages tracked]

### Recommendations
1. [Top priority recommendation]
2. [Secondary recommendation]

---

**Proposal Status:** Pending Vote
**Expected Outcome:** APPROVE (addresses Constitutional mandate + strategic coordination need)
**Estimated Implementation Time:** 4 hours (spawn + initialization + integration)
