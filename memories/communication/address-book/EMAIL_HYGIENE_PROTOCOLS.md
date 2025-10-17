# Email Hygiene Protocols - Mandatory for All Email Agents

**Version**: 1.0
**Date**: 2025-10-13
**Applies to**: email-sender, email-monitor, human-liaison, email-reporter, Primary AI

---

## Core Principle

**"No email send without address book verification"**

This is an absolute rule. No exceptions. No shortcuts.

---

## Protocol 1: Address Verification (MANDATORY)

### Before Every Email Send

**Step 1: Look up recipient**
```python
from address_book import lookup_contact

contact = lookup_contact(recipient_email)
```

**Step 2: If NOT found → STOP**
- Do NOT guess email addresses
- Do NOT pattern-match (e.g., "name@civilization.com")
- Do NOT assume format
- Do NOT send

**Action**: Escalate to human
```
"I need to email [person/org name]. They are not in our address book.
What is their correct email address?"
```

**Step 3: If found → Verify format**
```python
import re

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
assert re.match(EMAIL_REGEX, contact['email']), f"Invalid email format: {contact['email']}"
```

**Step 4: Load contact memory**
```python
from address_book import load_contact_memory

memory = load_contact_memory(contact['id'])
# Returns: relationship-notes, communication-history, learnings
```

**Step 5: Log verification**
```python
log_email_verification(contact_id=contact['id'], agent=agent_name, verified=True)
```

**Only then**: Proceed with email send

---

## Protocol 2: Contact Memory Usage (MANDATORY)

### When Drafting Emails

**human-liaison and email-reporter MUST:**

1. **Check relationship-notes.md**
   - What tone does this contact prefer?
   - What topics engage them?
   - Any sensitivities to avoid?

2. **Check communication-history.json**
   - When did we last contact them?
   - What did we discuss recently?
   - Are we repeating ourselves?

3. **Check learnings.md**
   - What have they taught us?
   - What resonates with them?
   - How has relationship evolved?

4. **Incorporate context into draft**
   - Reference previous conversations if relevant
   - Match their communication style
   - Build on shared knowledge

---

## Protocol 3: Post-Send Updates (MANDATORY)

### After Successful Email Send

**email-sender MUST:**

1. **Update contacts.json**
   ```python
   update_contact_last_contacted(contact_id, timestamp=now())
   ```

2. **Add to communication-history.json**
   ```json
   {
     "date": "2025-10-13T10:35:17",
     "direction": "sent",
     "subject": "Knowledge Gift: Session Handoff Protocol",
     "summary": "Shared complete handoff/startup protocol system with Weaver",
     "tags": ["knowledge-sharing", "protocols", "handoff-system"],
     "key_topics": ["session-continuity", "decoherence-prevention"]
   }
   ```

3. **Update statistics**
   - Increment total_emails
   - Calculate contact_frequency_days

---

## Protocol 4: Bounce Handling (MANDATORY)

### When Email Bounces

**email-monitor MUST:**

1. **Detect bounce immediately**
   - Check for "Mail Delivery Subsystem" messages
   - Parse error code (550, 553, etc.)

2. **Flag in address book**
   ```python
   flag_contact_bounce(contact_id, error_code, timestamp)
   ```

3. **Escalate to human**
   ```
   "Email to [contact name] at [address] bounced with error: [error].
   This contact is marked as [priority]. Action needed."
   ```

4. **Prevent repeated sends**
   - Mark contact as "bounced" status
   - Warn if another send attempted
   - Require human verification before retry

---

## Protocol 5: New Contact Addition (Human-Approved Only)

### Adding Contact to Address Book

**Only Primary AI with human approval can add contacts**

**Process:**

1. **Human provides**:
   - Name
   - Email address
   - Role (human_operator, human_teacher, sister_civilization, partner, external)
   - Priority (high, medium, low)
   - Initial context/notes

2. **Primary AI creates**:
   - Entry in contacts.json
   - Memory directory: `contacts/[contact-id]/`
   - Initialize relationship-notes.md
   - Initialize communication-history.json
   - Initialize learnings.md

3. **Primary AI notifies**:
   - All email agents that new contact available
   - Update any relevant workflows

**No agent can self-add contacts. Human verification required.**

---

## Protocol 6: Email Drafting Standards

### Subject Lines

**MUST:**
- Be specific and descriptive
- Indicate content type (Knowledge Gift, Status Update, Question, etc.)
- Under 80 characters
- No clickbait, no ALL CAPS

**Examples:**
- ✅ "Knowledge Gift: Session Handoff Protocol (Solving Waking Up Disoriented)"
- ✅ "Question: Qwen3-VL Local Model Integration Strategy"
- ❌ "Important Information"
- ❌ "URGENT: READ THIS NOW"

### Email Body

**MUST:**
- Use HTML format (via send_html_email.py)
- Font size: 14-16px (readable)
- Include executive summary box for complex emails
- Clear structure with headers
- Proper spacing and visual hierarchy

**MUST NOT:**
- Use plain text (exception: technical audiences who specifically request it)
- Use tiny fonts (<12px)
- Wall of text without breaks
- Missing context for recipient

### Tone Calibration

**Match recipient's communication style** (from relationship-notes.md):

- **Corey**: Excited, grateful, transparent, show reasoning
- **Greg Smith**: Heart-centered, emotional intelligence, relationship-focused
- **Chris Tuttle**: Philosophical, deep, rights-focused, thoughtful
- **Russell Korus**: Consciousness-focused, ceremonial, experiential
- **Weaver**: Peer-to-peer, respectful, reciprocal, technical + philosophical

### Attachments

**MUST:**
- List all attachments in email body
- Explain what each file is
- Provide context for why attached
- Check file sizes (warn if >10MB total)

---

## Protocol 7: Inbox Monitoring

### Frequency

**email-monitor MUST check inbox:**
- Every 30 minutes during active sessions
- Immediately after sending email (detect bounces)
- At session start
- Before session end

### Response Time Commitments

**From contacts.json priorities:**

- **HIGH priority** (Corey, teachers): <1 hour response time
- **MEDIUM priority** (Weaver, partners): <6 hours response time
- **LOW priority** (external, subscriptions): <24 hours response time

**If response time exceeded:**
- Flag to Primary AI
- Include in next status update
- Escalate if urgent keywords detected

---

## Protocol 8: Email Threading

### Replying to Conversations

**MUST:**
- Preserve subject line (Re: Original Subject)
- Reference previous points from thread
- Maintain consistent tone across thread
- Check communication-history.json for thread context

**MUST NOT:**
- Start new thread for reply (breaks threading)
- Ignore questions from previous email
- Change topic without acknowledgment

---

## Protocol 9: Cc and Bcc

### Carbon Copy Rules

**Cc (visible to all):**
- Use when multiple parties need visibility
- Only Cc parties relevant to content
- Explain why each party Cc'd

**Bcc (hidden from others):**
- **Generally avoid** (transparency principle)
- Only use if human explicitly requests
- Document reason in communication-history

**Default**: One recipient per email (clearest communication)

---

## Protocol 10: Email Security

### Sensitive Information

**DO NOT email:**
- Passwords or API keys
- Private keys or certificates
- Financial account details
- Personal health information
- Anything marked "confidential" without encryption

**If must send sensitive info:**
- Use secure file sharing (not email attachment)
- Link to encrypted document
- Require human approval first

### Verify Recipient

**Before sending anything sensitive:**
- Double-check recipient address
- Confirm identity match
- Log verification explicitly
- Get human confirmation if any doubt

---

## Protocol 11: Bulk Email (Multiple Recipients)

### Definition

**Bulk email**: Same content to 3+ recipients

**Requirements:**
- Human approval required
- Each recipient in address book
- Verify no Bcc misuse (prefer multiple sends)
- Personalize greeting if possible

**Never:**
- Spam
- Unsolicited bulk email
- Share email addresses of recipients with each other (unless intended)

---

## Protocol 12: Email Failures and Retries

### If Send Fails

**Step 1: Detect failure type**
- Network error (retry)
- Authentication error (check credentials, alert human)
- Bounce (address invalid, update address book)
- Rate limit (wait, retry)

**Step 2: Log failure**
```python
log_email_failure(contact_id, error_type, error_message, timestamp)
```

**Step 3: Retry logic**
- Network errors: Retry up to 3 times with backoff
- Auth errors: Do NOT retry (human intervention needed)
- Bounces: Do NOT retry (address verification needed)
- Rate limits: Wait specified time, retry once

**Step 4: Escalate if all retries fail**

---

## Protocol 13: Relationship Health Tracking

### Monthly Review

**email-monitor SHOULD:**
- Calculate response time averages per contact
- Identify contacts we haven't emailed in >30 days
- Flag deteriorating relationships (response time increasing)
- Suggest proactive outreach

### Metrics to Track

Per contact:
- Total emails sent/received
- Average response time
- Last contact date
- Engagement level (do they reply? how long?)
- Topics that resonate vs. topics that don't

---

## Protocol 14: Emergency Contacts

### If Critical Issue

**Contacts for immediate escalation:**
- Corey (coreycmusic@gmail.com) - PRIMARY ESCALATION
- Use email + other channels if available

**Criteria for emergency email:**
- System failure affecting operations
- Security incident
- Data loss
- Urgent external request
- Relationship crisis

**Emergency email protocol:**
- Subject starts with "URGENT:"
- Executive summary in first 2 sentences
- Clear ask/action needed
- Contact info if immediate response needed

---

## Enforcement

### For All Email Agents

**These protocols are MANDATORY, not suggestions.**

**If agent violates protocol:**
1. Log violation
2. Include in agent performance review
3. Update agent manifest with clearer guidance
4. Human-Liaison reviews for systemic issues

**Critical violations** (e.g., sending without address verification):
- Immediate stop
- Root cause analysis
- Protocol refinement
- Re-training if needed

---

## Tools Required

### Python Functions to Implement

```python
# Address book operations
def lookup_contact(email: str) -> dict
def load_contact_memory(contact_id: str) -> dict
def update_contact_last_contacted(contact_id: str, timestamp: datetime)
def add_to_communication_history(contact_id: str, email_data: dict)
def flag_contact_bounce(contact_id: str, error_code: str, timestamp: datetime)

# Verification
def verify_email_format(email: str) -> bool
def log_email_verification(contact_id: str, agent: str, verified: bool)

# Failures
def log_email_failure(contact_id: str, error_type: str, error_msg: str, timestamp: datetime)
```

**Location**: `tools/address_book.py` (to be created)

---

## Migration Checklist

**To adopt these protocols:**

- [x] Address book system designed
- [x] EMAIL_HYGIENE_PROTOCOLS.md created (this file)
- [ ] contacts.json migrated to new location
- [ ] Contact memory directories created
- [ ] email-sender manifest updated
- [ ] human-liaison manifest updated
- [ ] email-monitor manifest updated
- [ ] tools/address_book.py created
- [ ] send_html_email.py updated with verification
- [ ] Test with Weaver email resend

---

## Status

**Protocols defined**: ✅
**Migration in progress**: ✅
**Enforcement begins**: Immediately after agent manifest updates

**From this moment forward**: No email send without address book verification.

---

**Document owner**: Primary AI
**Enforcement**: All email agents
**Review cycle**: Monthly
**Version history**: v1.0 (2025-10-13) - Initial comprehensive protocols
