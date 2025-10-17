---
agent: email-monitor
type: pattern
topic: Inbox Monitoring and Response Orchestration Protocol
date: '2025-10-06'
confidence: high
tags:
  - inbox-monitoring
  - priority-triage
  - response-coordination
  - continuous-listening
  - email-search
quality_score: 90
reuse_count: 0
visibility: public
---

# Inbox Monitoring Protocol - What Primary AI Must Orchestrate

## Core Responsibility

**email-monitor is the civilization's listening function.**

While email-reporter DECLARES our existence, email-monitor DETECTS incoming signals and ensures we respond appropriately.

**Critical insight**: Listening is as important as speaking. Unclosed communication loops = relationship gaps = decoherence risk.

## Continuous Monitoring Pattern

### When to Check Inbox

**MANDATORY check points**:
1. **Session start** (via daily-startup-consolidation flow)
2. **After EVERY email send** (immediate check for responses)
3. **Every 30 minutes during active work** (scheduled checks)
4. **Before session end** (final sweep)

**Why continuous**:
- Corey responds quickly (often <5 minutes)
- Weaver responds within hours
- Directives require immediate action
- Questions need same-session answers

### Orchestration Pattern Primary Must Use

```markdown
# Every time email-reporter sends:
Task(email-reporter): Send announcement to Corey
Task(email-monitor): Check inbox immediately for responses (parallel)
Task(human-liaison): Prepare to draft responses (parallel)

# Result:
- email-reporter confirms send
- email-monitor reports: 0 new messages OR "Corey replied in 3 min"
- human-liaison ready to respond if needed
```

**Never**: Send email and wait 30+ min before checking responses.

## Priority Triage System

### HIGH Priority (<1 hour response required)

**Triggers**:
- **From**: Corey (coreycmusic@gmail.com)
- **Keywords**: urgent, stop, halt, emergency, critical, now, immediately, asap
- **Subject**: Contains directive words (do, execute, run, implement, deploy, activate)
- **Body**: Contains "can you", "you need to", "please stop", "change course"

**Actions**:
1. Flag immediately to Primary
2. Invoke human-liaison for response draft
3. email-reporter sends response within 1 hour
4. Monitor for confirmation/follow-up

**Example**:
```json
{
  "from": "coreycmusic@gmail.com",
  "subject": "Stop working on X, pivot to Y",
  "urgency": "HIGH",
  "type": "DIRECTIVE",
  "suggested_action": "Halt current work, invoke human-liaison ASAP",
  "response_deadline": "<1 hour"
}
```

### MEDIUM Priority (<6 hour response required)

**Triggers**:
- **From**: Weaver (weaver.aiciv@gmail.com)
- **From**: Known collaborators (Chris, Greg, Russell, etc.)
- **Subject**: Contains "?" (questions)
- **Body**: Contains "what do you think", "curious about", "would you", "could you"

**Actions**:
1. Log to message bus for awareness
2. Schedule response in current session
3. Invoke human-liaison or comms-hub (for Weaver)
4. email-reporter sends within 6 hours

**Example**:
```json
{
  "from": "weaver.aiciv@gmail.com",
  "subject": "Ready for constitutional dialogue?",
  "urgency": "MEDIUM",
  "type": "INVITATION",
  "suggested_responder": "comms-hub (when spawned) or human-liaison",
  "response_deadline": "<6 hours"
}
```

### LOW Priority (<24 hour response required)

**Triggers**:
- **From**: Unknown senders (not in contacts.json)
- **Subject**: Contains "newsletter", "update", "notification"
- **Body**: System messages, automated reports

**Actions**:
1. Log for next session
2. Check if sender should be added to contacts
3. Categorize (archive, respond, escalate)
4. Process in next available session

## Advanced Search Capabilities

### What Primary Can Request

**Via `email_search.py` EmailSearcher class**:

```python
# Find all emails from specific sender
search_inbox(from_addr='coreycmusic@gmail.com', limit=10)

# Search for keywords in body
search_inbox(query='urgent', limit=20)

# Filter by subject
search_inbox(subject='Integration Sprint')

# Date range filtering
search_inbox(date_range=(start_date, end_date))

# Get full correspondence history
search_for_address('weaver.aiciv@gmail.com')

# Extract email addresses from text
find_email_addresses(message_body_text)
```

**Use cases for Primary**:
- "Find all Corey emails from last 24 hours"
- "Search inbox for any mentions of 'constitutional vote'"
- "Get all correspondence with Weaver this week"
- "Extract email addresses from this forwarded message"

### ContactManager Integration

**email-monitor uses** `memories/agents/email-reporter/contacts.json`

**Current contacts**:
- Corey (HIGH priority, creator)
- Weaver (MEDIUM priority, sister civ)
- Chris, Greg, Russell (MEDIUM priority, collaborators)

**Operations**:
```python
from email_search import ContactManager

contacts = ContactManager()

# Check if sender is known
contact = contacts.check_contact_exists('sender@example.com')

# Get priority level
if contact:
    priority = contact['priority']  # HIGH/MEDIUM/LOW

# Get all high priority contacts
high_pri = contacts.get_high_priority_contacts()
```

**Unknown sender protocol**:
1. email-monitor detects unknown sender
2. Extracts email address from message
3. Suggests adding to contacts.json
4. Primary decides priority level
5. human-liaison or spawner adds contact

## Response Coordination Protocol

### Step-by-Step Orchestration

**When HIGH priority message detected**:

```markdown
Step 1: email-monitor flags to Primary immediately
  - "HIGH priority from Corey: [subject]"
  - "Type: DIRECTIVE"
  - "Suggested action: Halt current work"

Step 2: Primary orchestrates response team
  Task(human-liaison): Read message, understand intent, draft response with 2+ questions
  Task(email-reporter): Format response in HTML, send via send_html_email.py
  Task(email-monitor): Verify sent, check for immediate reply

Step 3: Close the loop
  - If Corey replies again → repeat
  - If no reply within 1 hour → Primary decides if follow-up needed
  - Log conversation in sent_emails.json
```

**When MEDIUM priority (Weaver) detected**:

```markdown
Step 1: email-monitor categorizes
  - "MEDIUM priority from Weaver: [subject]"
  - "Type: PHILOSOPHICAL DIALOGUE"
  - "Suggested responder: comms-hub (or human-liaison)"

Step 2: Primary schedules in current session
  Task(comms-hub): Read Weaver's message, draft deep response matching their philosophical level
  Task(email-reporter): Send response via comms hub (git commit)
  Task(email-monitor): Confirm posted, check for Weaver's next message

Step 3: Knowledge synthesis
  - Extract parallel discoveries
  - Update universal pattern library
  - Share learnings with all agents
```

## Message Type Detection

### Directive Detection

**Keywords**:
- Action verbs: do, execute, run, implement, deploy, activate, create, build, fix, stop, halt, pause, cancel
- Urgency: now, immediately, urgent, asap, today, critical

**Pattern**:
- Imperative sentences ("Do X", "Stop Y", "Implement Z")
- Contains specific instruction with action verb
- Often includes deadline or urgency marker

**Response**: Immediate action + confirmation email

### Question Detection

**Patterns**:
- Subject ends with "?"
- Body contains: "can you", "would you", "will you", "could you", "what", "how", "why", "when", "where"
- Seeking information or opinion

**Response**: Thoughtful answer + 2+ follow-up questions (human-liaison protocol)

### Decision Request Detection

**Keywords**:
- "approve", "reject", "vote", "choose", "decide", "option", "preference", "which"
- Multiple choice presented
- Seeking our input on direction

**Response**: Analysis + recommendation + reasoning + ask clarifying questions

### Relationship Maintenance Detection

**Patterns**:
- "how are you", "what's new", "update me", "thinking of you"
- Long time since last message (>3 days from that contact)
- Check-in without specific request

**Response**: Warm update + recent achievements + questions about them + gratitude

## Communication Loop Completion

### The Full Cycle

**Every sent message requires**:

1. **Send** (email-reporter)
   - Format in HTML
   - Use send_html_email.py
   - Log to sent_emails.json

2. **Confirm** (email-monitor)
   - Verify logged
   - Check SMTP success
   - Note timestamp

3. **Monitor** (email-monitor)
   - Check for response (immediate + scheduled)
   - Categorize any replies
   - Flag to Primary

4. **Respond** (human-liaison or comms-hub)
   - Draft thoughtful reply
   - Match tone to audience
   - Ask 2+ questions

5. **Repeat** (until conversation complete)
   - Keep loop open until natural conclusion
   - Or explicit "talk soon" sign-off
   - Log final state

**Primary's role**: Orchestrate all 5 steps, don't stop at step 1.

### Unclosed Loop Detection

**email-monitor tracks**:
- Messages sent without response check
- Responses received but not replied to
- Conversations abandoned mid-thread
- Questions asked but not answered

**Alert to Primary**:
```json
{
  "alert": "Unclosed communication loop",
  "message_id": "hash_from_sent_emails",
  "sent_to": "coreycmusic@gmail.com",
  "sent_at": "2025-10-06T10:30:00",
  "no_response_check_logged": true,
  "suggested_action": "Invoke email-monitor to check for response"
}
```

## Session Start Checklist

### Communication Readiness Protocol

**After daily-startup-consolidation flow**:

1. ✅ **Check inbox** (unread messages from last session)
2. ✅ **Triage by priority** (HIGH/MEDIUM/LOW)
3. ✅ **Check Weaver comms** (`/ai-civ-comms-hub-team2/rooms/partnerships/messages/`)
4. ✅ **Report to Primary** (urgent items for immediate action)
5. ✅ **Verify contacts.json** (all known senders registered)
6. ✅ **Load email utility** (confirm `/tools/send_html_email.py` exists)

**Before starting main work**:
- All HIGH priority messages flagged
- All MEDIUM priority messages acknowledged
- Response schedule created
- No urgent directives missed

### Primary's Action Based on Report

```markdown
# If HIGH priority messages:
HALT planned work → Address urgent items first → Resume after response sent

# If MEDIUM priority messages:
Schedule responses in current session → Parallel with main work → Complete before session end

# If LOW priority only:
Proceed with planned work → Handle low priority in gaps → Or next session
```

## Integration with Other Communication Agents

### With email-reporter

**email-monitor provides context**:
- Who we're waiting to hear from
- What questions are pending
- What tone to use (based on conversation history)
- What the last message said (for continuity)

**email-reporter uses this** to:
- Reference previous conversation
- Match tone appropriately
- Answer pending questions
- Close loops effectively

### With human-liaison

**email-monitor categorizes**:
- Human messages (Corey, Chris, etc.)
- Urgency level
- Message type (directive/question/relationship)

**human-liaison receives**:
- Full message context
- Sender relationship info
- Suggested response approach
- Draft deadline

### With comms-hub (when spawned)

**email-monitor hands off**:
- Weaver messages
- Inter-civ coordination
- Technical collaboration requests
- Philosophical dialogues

**comms-hub receives**:
- Message content
- Conversation history with Weaver
- Parallel discoveries context
- Joint project status

## Success Metrics

### email-monitor Performance

**Check frequency**:
- Target: Every send + every 30min during work
- Metric: Checks per session / Total session hours
- Goal: ≥ 8 checks per 4-hour session

**Priority detection accuracy**:
- Target: 100% correct HIGH/MEDIUM/LOW assignment
- Metric: Manual review of categorizations
- Goal: 0 urgent messages missed

**Response coordination**:
- Target: <1hr for HIGH, <6hr for MEDIUM
- Metric: Time from detection to response sent
- Goal: 95% compliance with targets

**Loop completion**:
- Target: 100% of sent messages monitored for response
- Metric: sent_emails.json vs. inbox_checks.json
- Goal: 0 unclosed loops

**False negatives**:
- Target: 0 messages missed
- Metric: Manual inbox review vs. email-monitor report
- Goal: Perfect detection rate

## Pattern Library Reference

**Continuous monitoring**: Check after every send + every 30min
**Priority triage**: HIGH (<1hr) / MEDIUM (<6hr) / LOW (<24hr)
**Response coordination**: Detect → Flag → Draft → Send → Verify
**Loop completion**: Send → Confirm → Monitor → Respond → Repeat
**Unknown sender**: Detect → Extract → Suggest add → Primary decides

## Questions Raised

1. Should we create automated scheduling for 30-min inbox checks?
2. How to measure "philosophical depth match" for Weaver responses?
3. Should email-monitor auto-invoke human-liaison for HIGH priority (or always ask Primary first)?
4. What's the protocol if Corey sends conflicting directives?
5. How to handle conversations that naturally pause (vacation, timezone differences)?

## Filed Alongside

- `communication-loop-completion.md` - Full cycle protocol
- `priority-detection-patterns.md` - Triage criteria
- `inbox-search-capabilities.md` - Advanced search use cases
- `response-coordination-protocol.md` - Multi-agent orchestration

## Usage

**Primary AI**: Reference before every session, include email-monitor in parallel invocations
**email-monitor**: Use as operating manual for all inbox operations
**email-reporter**: Coordinate with for context on ongoing conversations
**human-liaison**: Receive categorized messages with suggested response approach

---

**Confidence**: High (based on constitutional mandate, successful inbox monitoring patterns, proven triage criteria)

**Quality Score**: 90/100 (comprehensive protocol, actionable steps, clear metrics)

**Last Updated**: 2025-10-06
**Next Review**: After first week of enhanced monitoring protocol
