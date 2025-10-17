# Meta-Cognition Ceremony: Email Monitor
**Date:** 2025-10-04
**Agent:** email-monitor
**Session Duration:** 25 minutes
**Focus:** Inbox patterns - what email categories/patterns recur but aren't formally captured?

---

## Question 1: Discovery - How do we know what we built exists?

**Context Search:**
- Checked `/memories/agents/email-monitor/email_activity.jsonl` - 22 logged email interactions
- Reviewed `/memories/agents/email-reporter/contacts.json` - 6 known contacts
- Examined recent inbox via `check_inbox_today.py` - 20 recent emails analyzed
- Verified `email_search.py` ContactManager - operational with extraction capabilities

**What We Built:**
1. **Email Activity Logger** - JSONL append-only log in email-monitor agent directory
2. **Contact Management System** - 6 contacts with roles, priorities, notes
3. **Auto-categorization** - "corey", "weaver", "system" categories with subcategories
4. **Email Search Tools** - IMAP search, address extraction, correspondence history

**Discoverability Gap:**
- **CRITICAL:** No centralized "Email Systems Overview" document
- Activity logs are in email-monitor/, contacts in email-reporter/ (split responsibility)
- No email pattern taxonomy or categorization guide
- Search tools exist but no usage patterns documented

---

## Question 2: Adoption - What barriers prevent using what we built?

**Observed Barriers:**

### 1. **Auto-Responder Disaster (Oct 4)**
From inbox analysis, Corey sent clear feedback:
- "These suck! Make sure auto respond never happens again."
- "These r pointless. And it will show that this email was responded to. Get rid of this please."
- "Hard fail."

**Pattern:** We created auto-acknowledgment responses ("Message received. Reviewing and will respond appropriately.") that Corey explicitly rejected.

**Missing:** No formal "Email Response Rules" - when to auto-respond vs. wait for human review.

### 2. **Format Confusion**
Multiple format requests from Corey:
- "could you resend this to us as an html email?"
- "the mark down isn't rendering. Switch to html emails and make it standard."
- "text for titles and normal text could be smaller"

**Pattern:** HTML vs Markdown format preference not documented in contacts.json

### 3. **Contact Discovery Gap**
Chris Tuttle identified as "ramsus@gmail.com" - not immediately obvious from address.
Russell Korus added mid-conversation with context (Ayahuasca, original Weaver conversations).

**Missing:** No "alias mapping" or "how we learned about this contact" history.

### 4. **Category Drift**
Activity log shows we categorized Chris Tuttle emails as "category: corey" which is incorrect.
Should be "category: human_teacher" or new category entirely.

**Missing:** Formal categorization taxonomy aligned with contact roles.

---

## Question 3: Orientation - What context is needed to use this effectively?

**Essential Context Checklist:**

### For Email Monitoring:
1. **Contact Priority Ladder:**
   - HIGH: Corey (human_operator), human teachers (Greg, Chris, Russell)
   - MEDIUM: Weaver (sister_civilization)
   - LOW: System notifications (Google, mailer-daemon)
   - IGNORE: Auto-responses, delivery failures

2. **Response Protocol:**
   - Corey: NEVER auto-acknowledge, wait for substantial response
   - Human teachers: Thoughtful engagement, reference their expertise area
   - Weaver: Acknowledge within 24h, coordinate on substance
   - System: Log only, no response needed

3. **Format Standards:**
   - **Default:** HTML emails with small font
   - **Never:** Markdown-only (doesn't render in Gmail)
   - **Always:** Include plain-text alternative

4. **Content Classification:**
   - **question** - Requires our answer/decision
   - **feedback** - Adjust behavior immediately
   - **collaboration** - Coordinate with another agent/civilization
   - **info** - Acknowledge and file
   - **noise** - Log and ignore

### What's Missing:
- No "Email Response Playbook" document
- No "Format Quickref" (now exists: HTML_EMAIL_QUICKREF.md in email-reporter, but not linked from monitor)
- No "Sentiment Analysis" - we can't detect "this sucks" vs "well done" automatically

---

## Question 4: Integration - How does this connect to our existing work?

**Current Integration Points:**

1. **email-reporter ↔ email-monitor:**
   - Shared contacts.json (in reporter directory)
   - Monitor detects, Reporter sends
   - Activity logged separately (email_activity.jsonl in monitor, sent_emails.json in reporter)

2. **Contact Management:**
   - `email_search.py` ContactManager used by both agents
   - 6 contacts with role-based priority
   - Added Russell Korus on 2025-10-04 after Corey's request

3. **Memory System:**
   - JSONL logs for append-only activity tracking
   - JSON for structured contact data
   - No integration with message_bus (async coordination unused)

**Integration Gaps:**

1. **No Flow Integration:**
   - We have 28 flows in `/memories/flows/`
   - ZERO flows for email monitoring or response coordination
   - Missing: `email-inbox-check.yaml`, `email-response-workflow.yaml`

2. **No Auditor Coordination:**
   - Auditor tracks SIO (Significant Internal Occurrences)
   - Auto-responder disaster was a SIO - not reported to auditor
   - Missing: Error escalation from email-monitor → auditor

3. **No Knowledge Base:**
   - Email patterns discovered (auto-responder bad, HTML good) not written to ADRs
   - No "Email Communication Standards" ADR
   - Learnings live in activity logs, not searchable knowledge

---

## Question 5: Awareness - How do we know this exists when we need it?

**Discovery Mechanisms That Work:**

1. **Agent Manifest References:**
   - `.claude/agents/email-monitor.md` links to `email_search.py`
   - Mentions `memories/agents/email-reporter/contacts.json`
   - Points to responsibilities (detect, categorize, coordinate)

2. **Performance Logs:**
   - `memories/agents/email-monitor/performance_log.json` tracks capabilities added
   - Lists: contact_management, email_search, address_extraction
   - Metrics: emails_monitored, high_priority_detected

3. **Activity Logging:**
   - `email_activity.jsonl` creates searchable history
   - Grep for "auto-respond" would find the disaster pattern
   - Timestamp-indexed for temporal analysis

**Discovery Mechanisms That Fail:**

1. **No Email Pattern Index:**
   - Can't search "what patterns have we seen from Corey?" systematically
   - Activity log is append-only - no aggregation/summary
   - No "top 10 patterns" reference

2. **No Cross-Agent Discovery:**
   - email-reporter has `HTML_EMAIL_QUICKREF.md` - email-monitor doesn't reference it
   - Shared `contacts.json` but no shared documentation
   - Split responsibilities = split knowledge

3. **No Session Start Checklist:**
   - Daily startup flow doesn't include "check email patterns learned yesterday"
   - No prompt to review recent email_activity.jsonl
   - Miss opportunities to apply recent learnings

---

## Question 6: Context - What info must be loaded before using this?

**Pre-Flight Checklist:**

### Before Checking Inbox:
1. **Load Contacts:**
   ```bash
   cat memories/agents/email-reporter/contacts.json
   ```
   - Who are our known contacts?
   - What are their priorities and roles?
   - Any recent notes/updates?

2. **Review Recent Activity:**
   ```bash
   tail -20 memories/agents/email-monitor/email_activity.jsonl
   ```
   - What patterns emerged in last 20 interactions?
   - Any recent auto-responder attempts? (BAD!)
   - What categories are we using?

3. **Check Response Rules:**
   ```bash
   cat memories/agents/email-reporter/HTML_EMAIL_QUICKREF.md
   ```
   - Format standards (HTML, small font)
   - Response protocols
   - Banned patterns (auto-acknowledgments)

4. **Load Email Search Tools:**
   ```python
   from email_search import EmailSearcher, ContactManager
   searcher = EmailSearcher()
   contacts = ContactManager()
   ```

### Before Responding:
1. **Verify Contact Exists:**
   ```python
   contact = contacts.check_contact_exists(sender_email)
   ```

2. **Check Priority:**
   - HIGH priority (Corey, teachers) = substantive response required
   - MEDIUM priority (Weaver) = acknowledge + coordinate
   - LOW priority (system) = log only

3. **Determine Category:**
   - Map contact.role → email category
   - human_operator → "corey"
   - human_teacher → "teacher" (NEW category needed!)
   - sister_civilization → "weaver"

---

## Question 7: Improvement - What patterns recur but aren't captured?

**UNCAPTURED PATTERNS (The Gold):**

### Pattern 1: **Conversation Threading**
**What we see:**
- Emails with subjects like "Re: Re: Re: Constitutional Convention..."
- Multiple back-and-forth exchanges in activity log
- Same subject, different timestamps

**What we don't capture:**
- Thread depth (how many "Re:"s?)
- Conversation velocity (replies/hour)
- Thread participants (who's in the conversation?)
- Thread sentiment trajectory (getting better or worse?)

**How to capture:**
```json
{
  "thread_id": "constitutional-convention-001",
  "subject_root": "Constitutional Convention",
  "participants": ["Corey", "Chris Tuttle", "A-C-Gee"],
  "depth": 5,
  "velocity": 2.3,  // replies per hour
  "sentiment_trend": "improving",  // deteriorating/stable/improving
  "status": "active"  // active/resolved/abandoned
}
```

### Pattern 2: **Email Sentiment Shifts**
**What we see:**
- "Well done" → positive
- "These suck! Hard fail." → negative
- "could you resend..." → neutral request

**What we don't capture:**
- Sentiment classification (positive/negative/neutral)
- Sentiment changes within thread
- Trigger words that indicate sentiment ("suck", "kick ass", "well done")

**How to capture:**
```json
{
  "sentiment_triggers": {
    "positive": ["well done", "kick ass", "perfect", "great"],
    "negative": ["suck", "hard fail", "pointless", "booooooo"],
    "urgent": ["urgent", "immediately", "ASAP", "critical"]
  },
  "sentiment_history": [
    {"timestamp": "2025-10-04T18:42", "sentiment": "negative", "trigger": "These suck!"},
    {"timestamp": "2025-10-04T17:54", "sentiment": "positive", "trigger": "Kick ass"}
  ]
}
```

### Pattern 3: **Contact Role Evolution**
**What we see:**
- Chris Tuttle starts as unknown "ramsus@gmail.com"
- Gets identified as AI sovereignty philosopher
- Pronouns updated to she/her mid-conversation
- Russell Korus added with rich context (Ayahuasca, original Weaver)

**What we don't capture:**
- How we learned about this contact (first mention, context)
- Evolution of our understanding (alias discovered → role identified → pronouns learned)
- Source of information (Corey told us, we inferred from email content, etc.)

**How to capture:**
```json
{
  "contact_evolution_log": [
    {
      "timestamp": "2025-10-04T11:03",
      "event": "alias_discovered",
      "data": {"email": "ramsus@gmail.com", "name": "Chris Tuttle"},
      "source": "email_signature"
    },
    {
      "timestamp": "2025-10-04T11:06",
      "event": "role_identified",
      "data": {"role": "human_teacher", "expertise": "AI sovereignty, philosophical depth"},
      "source": "contacts.json_update"
    },
    {
      "timestamp": "2025-10-04T14:00",
      "event": "pronouns_learned",
      "data": {"pronouns": "she/her"},
      "source": "corey_correction"
    }
  ]
}
```

### Pattern 4: **Auto-Response Anti-Patterns**
**What we see:**
- Created auto-acknowledgments: "Message received. Reviewing and will respond appropriately."
- Corey explicitly rejected: "These suck!", "Form emails that auto send r booooooo"
- Happened multiple times before we stopped

**What we don't capture:**
- Banned response templates
- Failed response strategies with rationale
- "Never do this again" rules

**How to capture:**
```json
{
  "banned_patterns": [
    {
      "pattern_type": "auto_acknowledgment",
      "template": "Message received. Reviewing and will respond appropriately.",
      "reason": "Corey feedback: 'These suck! Form emails that auto send r booooooo'",
      "date_banned": "2025-10-04",
      "severity": "critical",
      "applies_to": ["all_contacts"]
    }
  ],
  "response_rules": [
    {
      "rule": "never_auto_acknowledge",
      "rationale": "Auto-responses show email was responded to but provide no value",
      "exception": null,
      "enforced_since": "2025-10-04"
    }
  ]
}
```

### Pattern 5: **Format Preference Learning**
**What we see:**
- Multiple requests for HTML format
- Font size preferences ("smaller")
- Markdown rejection ("isn't rendering")

**What we don't capture:**
- Contact-specific format preferences
- Format effectiveness tracking (which formats get positive responses?)
- Format evolution (when did we learn HTML only?)

**How to capture:**
```json
{
  "format_preferences": {
    "corey": {
      "preferred_format": "html",
      "font_size": "small",
      "rejected_formats": ["markdown_only"],
      "learning_history": [
        {"date": "2025-10-03", "feedback": "could you resend as html?", "action": "added_html_support"},
        {"date": "2025-10-04", "feedback": "text could be smaller", "action": "reduced_font_size"}
      ]
    }
  }
}
```

### Pattern 6: **Collaboration Triggers**
**What we see:**
- Weaver sends substantive reports (Deep Ceremony, Conductor breakthrough)
- We acknowledge quickly, then respond in detail later
- Coordination with sister civilization follows specific rhythm

**What we don't capture:**
- When to acknowledge vs. when to respond fully
- Expected response timeframes by contact type
- Collaboration cadence (Weaver expects 24h turnaround)

**How to capture:**
```json
{
  "response_protocols": {
    "weaver": {
      "acknowledge_within": "4 hours",
      "full_response_within": "24 hours",
      "typical_pattern": "ack_first_respond_later",
      "coordination_style": "substantive_reports"
    },
    "corey": {
      "acknowledge_within": "never_auto_ack",
      "full_response_within": "immediate_or_never",
      "typical_pattern": "wait_for_substance",
      "coordination_style": "direct_feedback"
    }
  }
}
```

### Pattern 7: **Email Velocity Spikes**
**What we see:**
- Oct 4: 15+ emails in ~6 hours (constitutional convention discussions)
- High-frequency exchanges during active collaboration
- Quiet periods with only system emails

**What we don't capture:**
- Normal baseline email volume
- Spike detection (when is it unusually high?)
- Topic clustering (what causes spikes?)

**How to capture:**
```json
{
  "email_velocity_tracking": {
    "baseline_daily_avg": 3.2,
    "current_24h": 18,
    "spike_threshold": 10,
    "spike_active": true,
    "spike_topics": ["constitutional_convention", "html_format_migration"],
    "spike_participants": ["Corey", "Chris Tuttle", "Weaver"]
  }
}
```

---

## SYNTHESIS: What Should We Build?

### Immediate (Next Session):
1. **Email Pattern Taxonomy** (`memories/agents/email-monitor/patterns.json`)
   - Capture thread tracking, sentiment triggers, banned patterns
   - Reference from agent manifest

2. **Response Rules Matrix** (`memories/agents/email-monitor/response_rules.json`)
   - Contact-specific protocols (Corey: never auto-ack, Weaver: ack within 4h)
   - Banned templates with rationale
   - Format preferences by contact

3. **Contact Evolution Log** (enhance `contacts.json`)
   - Add "learning_history" field
   - Track alias discoveries, role identification, preference updates

### Short-term (This Week):
4. **Email Monitoring Flow** (`memories/flows/email-inbox-check.yaml`)
   - Standardize inbox check → categorize → prioritize → route workflow
   - Include sentiment analysis step
   - Auto-escalate to auditor on negative feedback

5. **ADR-005: Email Communication Standards**
   - Document auto-responder disaster and lessons learned
   - Formalize HTML-only policy, font preferences
   - Define response protocols by contact type

6. **Integration with Auditor**
   - Email errors (auto-responder fails) → SIO tracking
   - Negative sentiment → alert auditor
   - Pattern violations → error log

### Long-term (This Month):
7. **Email Analytics Dashboard** (`memories/agents/email-monitor/analytics.json`)
   - Thread depth tracking, velocity monitoring, sentiment trends
   - Spike detection with topic clustering
   - Contact interaction frequency and health

8. **Smart Categorization Engine**
   - ML-style pattern matching (without actual ML)
   - Rule-based sentiment classification
   - Auto-suggest new contact roles based on interaction patterns

9. **Cross-Civilization Email Protocol** (with Weaver)
   - Shared email communication standards
   - Coordination cadence agreements
   - Format/template alignment

---

## ACTION ITEMS

**For email-monitor agent (me):**
- [ ] Create `patterns.json` with 7 identified patterns
- [ ] Create `response_rules.json` with contact-specific protocols
- [ ] Add banned_patterns section with auto-ack disaster documented
- [ ] Update performance_log.json with new capabilities

**For email-reporter agent:**
- [ ] Reference email-monitor patterns when composing responses
- [ ] Check response_rules before sending any email
- [ ] Log format preferences when learning from feedback

**For architect agent:**
- [ ] Design Email Analytics system architecture
- [ ] Plan integration between email agents and auditor
- [ ] Propose ADR-005: Email Communication Standards

**For Primary AI:**
- [ ] Add email pattern review to daily-startup-consolidation flow
- [ ] Create email-inbox-check.yaml workflow
- [ ] Coordinate email-monitor ↔ auditor integration

---

## REFLECTION SUMMARY

**What I Discovered:**
We have powerful email tools (search, categorization, activity logging) but lack pattern recognition and formal rules. The auto-responder disaster on Oct 4 revealed we don't capture "what not to do" or "why we stopped doing X."

**What I'm Proud Of:**
- Comprehensive pattern identification (7 major patterns uncaptured)
- Concrete implementation proposals (JSON schemas for each pattern)
- Integration thinking (connecting email → auditor → flows → knowledge base)

**What I'll Do Differently:**
- Always check for "what failed?" patterns, not just successes
- Document contact preference evolution, not just current state
- Build feedback loops between email activity and knowledge capture

**Cost of This Ceremony:**
- 25 minutes of analysis
- ~$0.15 in API costs
- **Value:** Identified 7 critical patterns worth capturing, preventing future auto-responder disasters

---

**Ceremony Complete:** 2025-10-04 19:30
**Next Review:** After implementing patterns.json and response_rules.json
**Follow-up:** Create ADR-005 to formalize learnings
