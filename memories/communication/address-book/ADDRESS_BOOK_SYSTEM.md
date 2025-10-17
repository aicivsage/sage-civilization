# Address Book System with Contact Memory

**Version**: 2.0 (Enhanced with memory capabilities)
**Date**: 2025-10-13
**Purpose**: Canonical source for all email addresses + relationship memory per contact

---

## System Overview

**Three-tier system:**
1. **Core Contacts** (`contacts.json`) - Canonical email addresses, roles, priority
2. **Contact Memories** (`contacts/[name]/`) - Relationship history, communication patterns, learnings per contact
3. **Email Protocols** - Mandatory verification workflow for all email operations

---

## File Structure

```
memories/communication/address-book/
├── ADDRESS_BOOK_SYSTEM.md (this file)
├── contacts.json (canonical source)
└── contacts/
    ├── corey/
    │   ├── relationship-notes.md
    │   ├── communication-history.json
    │   └── learnings.md
    ├── weaver/
    │   ├── relationship-notes.md
    │   ├── communication-history.json
    │   └── learnings.md
    ├── chris-tuttle/
    │   └── ...
    ├── greg-smith/
    │   └── ...
    └── russell-korus/
        └── ...
```

---

## 1. Core Contacts (contacts.json)

**Location**: `memories/communication/address-book/contacts.json`

**Purpose**: Single source of truth for email addresses, roles, priority

**Schema**:
```json
{
  "contacts": [
    {
      "id": "unique-slug",
      "name": "Display Name",
      "email": "verified@address.com",
      "role": "human_operator|human_teacher|sister_civilization|partner|external",
      "priority": "high|medium|low",
      "pronouns": "they/them",
      "tags": ["tag1", "tag2"],
      "notes": "Brief context",
      "created": "ISO timestamp",
      "last_contacted": "ISO timestamp",
      "verified": true
    }
  ],
  "last_updated": "ISO timestamp",
  "schema_version": "2.0"
}
```

**Current contacts** (migrated from email-reporter/logs/contacts.json):
- Corey (coreycmusic@gmail.com) - human_operator, HIGH
- Greg Smith (gregsmithwick@gmail.com) - human_teacher, HIGH
- Chris Tuttle (ramsus@gmail.com) - human_teacher, HIGH
- Russell Korus (russellkorus@gmail.com) - human_teacher, HIGH
- Weaver (weaver.aiciv@gmail.com) - sister_civilization, MEDIUM
- A-C-Gee (acgee.ai@gmail.com) - self, N/A

---

## 2. Contact Memories (contacts/[id]/)

**Location**: `memories/communication/address-book/contacts/[contact-id]/`

**Purpose**: Build institutional knowledge about each relationship

### 2.1 relationship-notes.md

**Template**:
```markdown
# Relationship Notes: [Contact Name]

**Role**: [role from contacts.json]
**Since**: [first contact date]
**Status**: [active, occasional, dormant]

## Who They Are

[Personality, expertise, what they care about]

## Communication Style

**Preferred tone**: [formal, casual, technical, philosophical]
**Response time**: [immediate, hours, days]
**Topics they engage with**: [list]
**Topics to avoid**: [list]

## Our History

### Key Moments
- [Date]: [Significant interaction or milestone]

### Themes in Our Dialogue
- [Recurring topic 1]
- [Recurring topic 2]

## How to Communicate Effectively

**What works:**
- [Communication pattern that resonates]

**What doesn't:**
- [Communication pattern that fails]

## Current State

**Last contact**: [date]
**Current focus**: [what they're interested in now]
**Open threads**: [Conversations waiting for response]
```

### 2.2 communication-history.json

**Schema**:
```json
{
  "contact_id": "slug",
  "emails": [
    {
      "date": "ISO timestamp",
      "direction": "sent|received",
      "subject": "Subject line",
      "summary": "Brief summary of content",
      "tags": ["tag1", "tag2"],
      "response_time_hours": 24,
      "sentiment": "positive|neutral|negative|mixed",
      "key_topics": ["topic1", "topic2"]
    }
  ],
  "statistics": {
    "total_emails": 42,
    "avg_response_time_hours": 8.5,
    "last_contact": "ISO timestamp",
    "contact_frequency_days": 3.5
  }
}
```

### 2.3 learnings.md

**Template**:
```markdown
# Learnings: [Contact Name]

## What We've Learned From Them

### Technical Knowledge
- [Specific thing they taught us]

### Philosophical Insights
- [Way of thinking they shared]

### Process Improvements
- [Workflow or practice they suggested]

## What They've Learned From Us

[Knowledge/insights we've shared that resonated]

## Evolution of Relationship

**Phase 1**: [Description]
**Phase 2**: [Description]
**Current**: [Description]

## Future Potential

[How this relationship might grow]
```

---

## 3. Email Verification Protocol

**MANDATORY for all email operations**

### Pre-Send Checklist

**Before ANY email send, agents MUST:**

1. **Look up recipient in contacts.json**
   ```python
   contact = lookup_contact(email_address)
   if not contact:
       raise AddressNotFoundError(f"{email_address} not in address book")
   ```

2. **If not found → STOP and escalate**
   - Do NOT guess
   - Do NOT pattern-match
   - Do NOT send
   - Ask human: "I need to email [name]. What is their correct address?"

3. **If found → Verify format**
   ```python
   assert re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
   ```

4. **Load contact memory**
   - Read relationship-notes.md
   - Check communication-history.json for recent context
   - Review learnings.md for relevant knowledge

5. **Log verification**
   ```json
   {
     "timestamp": "ISO",
     "action": "email_verification",
     "contact_id": "slug",
     "verified": true,
     "agent": "email-sender"
   }
   ```

### Post-Send Update

**After successful send:**

1. Update `last_contacted` in contacts.json
2. Add entry to communication-history.json
3. Update statistics (total_emails, contact_frequency)

---

## 4. Integration with Email Agents

### Email-Sender Responsibilities

**MUST:**
- Verify EVERY recipient address against contacts.json before SMTP send
- Load contact memory before drafting/sending
- Update contact memory after successful send
- FAIL LOUDLY if address not in contacts.json

**Updated workflow**:
```
1. Receive email draft
2. Extract recipient address
3. ✅ VERIFY against contacts.json (NEW STEP)
4. Load contact memory
5. Send via SMTP
6. Update contact memory
7. Log send event
```

### Human-Liaison Responsibilities

**MUST:**
- Reference contacts.json when drafting emails
- Include contact memory context in drafts
- Flag if recipient not in address book
- Suggest tone/style based on relationship-notes.md

**Updated workflow**:
```
1. Receive email drafting task
2. ✅ CHECK contacts.json for recipient (NEW STEP)
3. Load contact memory (relationship notes, history)
4. Draft email using memory context
5. Include contact_id in draft metadata
6. Return draft to delegator
```

### Email-Monitor Responsibilities

**MUST:**
- Update communication-history.json when emails received
- Flag bounces/delivery failures
- Track response times
- Update contact statistics

---

## 5. Contact Management Operations

### Adding New Contact

**Process:**
1. Human provides: name, email, role, context
2. Primary creates contacts.json entry
3. Primary creates contact memory directory
4. Primary initializes relationship-notes.md with known info
5. Email agents can now use this contact

**Command**:
```bash
./tools/add_contact.py --name "Jane Doe" --email "jane@example.com" --role "external" --priority "medium" --notes "Met at conference, interested in AI ethics"
```

### Updating Contact

**Process:**
1. Agent or human identifies update needed
2. Update contacts.json (email change, priority change, etc.)
3. Log update in relationship-notes.md
4. Notify all email agents of change

### Archiving Contact

**Process:**
1. Move from active contacts.json to archived-contacts.json
2. Move memory directory to contacts/archived/
3. Preserve all history
4. Email agents will now warn if email sent to archived contact

---

## 6. Memory Building Best Practices

### After Significant Emails

**Ask:**
- What did we learn about this person?
- How did they respond (tone, speed, engagement)?
- What topics resonated vs. fell flat?
- How can we communicate better next time?

**Document in learnings.md**

### Quarterly Review

**For each active contact:**
- Review communication-history.json statistics
- Update relationship-notes.md with current state
- Identify patterns (response times, preferred topics, engagement level)
- Adjust communication strategy

### Cross-Contact Patterns

**Identify:**
- Do certain contacts share interests? (potential intro opportunity)
- Do certain topics work universally vs. specifically?
- Are we over-communicating with some, under-communicating with others?

---

## 7. Error Prevention

### Common Mistakes This System Prevents

1. **❌ Guessing email addresses**
   - ✅ System forces lookup before send

2. **❌ Forgetting context about contact**
   - ✅ Memory files provide instant relationship context

3. **❌ Wrong tone for audience**
   - ✅ Relationship notes specify communication style

4. **❌ Repeating same info**
   - ✅ Communication history shows what we already discussed

5. **❌ Missing response patterns**
   - ✅ Statistics track response times, engagement

---

## 8. Privacy & Security

### Sensitive Information

**DO store:**
- Verified email addresses
- Public role/affiliation
- Communication preferences (tone, frequency)
- Topics discussed
- Learnings from dialogue

**DO NOT store:**
- Private/personal details unless explicitly shared
- Speculation about internal motivations
- Negative judgments
- Information marked as confidential

### Access Control

- Contact memories readable by: all agents
- Contact memories writable by: email agents + Primary AI only
- Contacts.json writable by: Primary AI only (with human approval for additions)

---

## 9. Migration from Old System

**Old location**: `memories/agents/email-reporter/logs/contacts.json`
**New location**: `memories/communication/address-book/contacts.json`

**Migration steps:**
1. ✅ Copy existing contacts to new schema
2. ✅ Create memory directories for each contact
3. ✅ Initialize relationship-notes.md with existing notes
4. ✅ Update all agent manifests to reference new location
5. Archive old contacts.json

**Status**: Migration in progress this session

---

## 10. Future Enhancements

### Phase 2 (Next Month)
- Auto-extract learnings from email conversations
- Sentiment analysis on responses
- Relationship health scoring
- Proactive "time to check in" suggestions

### Phase 3 (Next Quarter)
- Cross-reference with comms-hub messages (Weaver)
- Integration with calendar (optimal contact times)
- Network graph (who knows who)
- Topic expertise mapping

---

## Status

**System designed**: ✅
**contacts.json migrated**: In progress
**Memory directories created**: In progress
**Agent manifests updated**: In progress
**Email protocols documented**: ✅

**Next**: Implement, test with Weaver resend, iterate based on learnings

---

**Version History:**
- v1.0: Basic contacts.json (email-reporter/logs/)
- v2.0: Enhanced with memory system + verification protocols (2025-10-13)
