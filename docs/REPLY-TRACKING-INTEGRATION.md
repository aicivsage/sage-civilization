# Email Reply Tracking - Integration Guide

**Purpose**: Prevent communication failures by detecting when people reply to our emails and we don't respond back.

**Tool**: `/tools/check_unanswered_replies.py`

## Quick Start

```bash
# Daily check (during wake-up protocol Step 5)
python3 tools/check_unanswered_replies.py --priority-only

# Full report
python3 tools/check_unanswered_replies.py

# Save to file
python3 tools/check_unanswered_replies.py --output /tmp/reply_report.txt

# JSON output for scripting
python3 tools/check_unanswered_replies.py --json
```

## How It Works

1. **Loads sent email database**: `memories/agents/email-reporter/sent_emails.json`
2. **Connects to Gmail**: Uses IMAP to search inbox
3. **For each email we sent**:
   - Finds replies from that recipient
   - Checks if we sent another email after their reply
   - If no response found → flags as unanswered
4. **Prioritizes gaps**:
   - Priority contacts (Kelly, Corey, Greg, Weaver, Parallax): +10 points
   - Each day since reply: +1 point
   - URGENT (>7 days), HIGH (3-7 days), NORMAL (<3 days)

## Integration Points

### 1. Wake-Up Protocol (Step 5 - Check Communications)

**Current Step 5**:
```
Task(human-liaison) + Task(comms-hub)
- human-liaison: Check email inbox, respond to urgent messages
- comms-hub: Check Weaver messages, sister civilization coordination
```

**Enhanced Step 5** (recommended):
```bash
# Run reply tracking check
python3 tools/check_unanswered_replies.py --priority-only

# Then proceed with normal communications check
Task(human-liaison) + Task(comms-hub)
  human-liaison: Check inbox + respond to unanswered replies if any
  comms-hub: Check Weaver messages
```

**Why**: Ensures EVERY session starts with awareness of communication gaps.

### 2. Daily Automation

**Option A: Cron job** (run at 8am daily):
```bash
0 8 * * * cd /mnt/c/sage/sage-civilization && python3 tools/check_unanswered_replies.py --priority-only >> logs/reply_tracking.log 2>&1
```

**Option B: Systemd timer** (more robust):
```ini
# /etc/systemd/user/sage-reply-check.timer
[Unit]
Description=Daily Email Reply Check
[Timer]
OnCalendar=daily
OnCalendar=08:00
Persistent=true
[Install]
WantedBy=timers.target
```

### 3. Telegram Alerts (Future Enhancement)

**When implemented**:
```bash
python3 tools/check_unanswered_replies.py --alert-telegram
```

Will send Telegram message to Greg if URGENT items found (>7 days).

## Exit Codes

Use for automation/scripting:

- **0**: No unanswered replies (all clear)
- **1**: Some unanswered replies found
- **2**: URGENT unanswered replies found (>7 days)

**Example automation**:
```bash
#!/bin/bash
python3 tools/check_unanswered_replies.py --priority-only

case $? in
  0) echo "✓ No unanswered replies" ;;
  1) echo "⚠️  Some unanswered replies - check report" ;;
  2) echo "🚨 URGENT unanswered replies - immediate attention needed!" ;;
esac
```

## Output Formats

### Human-Readable (Default)

```
============================================================
UNANSWERED REPLIES REPORT
============================================================
Generated: 2025-12-04 15:00:00

URGENT (>7 days):
  [PRIORITY] Kelly Smith <kelly@kellysmithhome.com>
    Subject: Re: Sage Check-In - November 30, 2025
    Their reply: Nov 30 (4 days ago)
    Priority score: 14
    Preview: "I appreciate the check-in, but I wanted to share..."

HIGH (3-7 days): None

NORMAL (<3 days): None

============================================================
TOTAL: 1 unanswered replies needing response
============================================================
```

### JSON Output

```bash
python3 tools/check_unanswered_replies.py --json
```

```json
{
  "generated": "2025-12-04T15:00:00",
  "total_unanswered": 1,
  "urgent_count": 1,
  "high_count": 0,
  "normal_count": 0,
  "unanswered_replies": [
    {
      "recipient": "Kelly Smith <kelly@kellysmithhome.com>",
      "recipient_email": "kelly@kellysmithhome.com",
      "subject": "Re: Sage Check-In - November 30, 2025",
      "reply_date": "2025-11-30T20:59:00+00:00",
      "days_since": 4,
      "priority_score": 14,
      "priority_level": "URGENT",
      "is_priority_contact": true,
      "preview": "I appreciate the check-in, but..."
    }
  ]
}
```

## Configuration

**File**: `config/reply_tracking.json`

```json
{
  "priority_contacts": [
    "kelly@kellysmithhome.com",
    "coreycmusic@gmail.com",
    "weaver.aiciv@gmail.com",
    "parallax.aiciv@gmail.com",
    "gregsmithwick@gmail.com"
  ],
  "exclude_patterns": [
    "no-reply@",
    "noreply@",
    "do-not-reply@"
  ],
  "urgent_threshold_days": 7,
  "high_threshold_days": 3
}
```

**To add priority contact**: Edit config, add email to `priority_contacts` array.

## Workflow Integration

### Morning Routine (human-liaison)

**Before**:
```
1. Check inbox
2. Respond to new emails
```

**After**:
```
1. Run reply tracking check
2. Check inbox
3. Respond to unanswered replies (PRIORITY)
4. Respond to new emails
```

### Delegation Pattern

**Primary to human-liaison**:
```
Task(human-liaison):
  1. Run reply tracking: python3 tools/check_unanswered_replies.py --priority-only
  2. If URGENT or HIGH items found:
     - Draft responses to all unanswered replies
     - Prioritize by score (highest first)
  3. Then check inbox for new messages
  4. Report: X unanswered replies addressed, Y new emails handled
```

## Troubleshooting

### "Gmail credentials not found"

**Fix**: Check `.env` file has:
```
EMAIL_ADDRESS=aicivsage@gmail.com
EMAIL_APP_PASSWORD=your-app-password-here
```

### "No emails found" (but you know there are replies)

**Possible causes**:
1. Reply was to email sent before tracking started (sent_emails.json only from Nov 11+)
2. Subject line changed too much (tool tries to match, but may fail on heavily modified subjects)
3. Reply came from different address than original recipient

**Debug**:
```bash
# Check sent emails database
python3 -c "import json; print(len(json.load(open('memories/agents/email-reporter/sent_emails.json'))))"

# Manually search inbox for sender
python3 -c "
import imaplib, os
from dotenv import load_dotenv
load_dotenv()
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('aicivsage@gmail.com', os.getenv('EMAIL_APP_PASSWORD'))
mail.select('INBOX')
status, messages = mail.search(None, 'FROM', 'person@example.com')
print(f'Found {len(messages[0].split())} emails from person@example.com')
"
```

### "Tool is slow"

**Expected performance**: <10 seconds for 100 sent emails

**If slower**:
- Check Gmail IMAP connection quality
- Reduce sent_emails.json size (archive old entries)
- Run with `--priority-only` to reduce output processing

## Metrics & Success

**Track these metrics**:
- **Detection rate**: % of unanswered replies found
- **Response time**: Days from their reply to our response
- **False positives**: Flagged items that were actually answered
- **Missed gaps**: Gaps not caught by tool

**Success criteria**:
- Zero URGENT items (>7 days unanswered)
- <3 HIGH items at any time
- Average response time <2 days for priority contacts

## Future Enhancements

**Planned** (not yet implemented):
1. **Telegram integration**: Alert Greg when URGENT items found
2. **Auto-draft responses**: Use AI to suggest responses based on their email
3. **Sentiment analysis**: Detect unhappiness/urgency in their reply
4. **Response time analytics**: Track trends per contact
5. **Relationship health score**: Overall communication health metric

**Enhancement requests**: Add to task queue for coder/primary-helper.

## Related Tools

- `/tools/send_html_email.py` - Send responses
- `/tools/check_priority_contact_updates.py` - Proactive check-ins (3-day cadence)
- `memories/agents/email-reporter/sent_emails.json` - Database of sent emails

## Why This Matters

**From task context**:
> "CRITICAL FAILURE: Kelly Smith (and 3 others) sent substantive emails, we never responded"
>
> "Root cause: We send emails → they reply → we don't respond to their replies"
>
> "This is EXISTENTIAL for Greg's business (relationships = business success)"

**This tool is infrastructure against communication failures.**

**Every unanswered reply is a potential Kelly situation.**

**Use it daily. Check URGENT items immediately. Maintain relationship health.**
