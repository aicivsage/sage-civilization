# Reply Tracking Tool - Example Output

## Scenario: Multiple Unanswered Replies

**Command**: `python3 tools/check_unanswered_replies.py`

**Output**:

```
Loading sent emails database...
✓ Loaded 100 sent emails
Connecting to Gmail...
✓ Connected to Gmail
Analyzing replies...
✓ Analysis complete: 5 unanswered replies found

============================================================
UNANSWERED REPLIES REPORT
============================================================
Generated: 2025-12-04 15:00:00

URGENT (>7 days):
  [PRIORITY] Kelly Smith <kelly@kellysmithhome.com>
    Subject: Re: Sage Check-In - November 24, 2025
    Their reply: Nov 24 (10 days ago)
    Priority score: 20
    Preview: I appreciate the check-in, but I wanted to share some concerns about the project timeline...

  John Doe <john@example.com>
    Subject: Re: Project Status Update
    Their reply: Nov 26 (8 days ago)
    Priority score: 8
    Preview: Thanks for the update. I have a few questions about the implementation approach you...

HIGH (3-7 days):
  [PRIORITY] Parallax (A-C-Gee Civilization) <parallax.aiciv@gmail.com>
    Subject: Re: Tool Collaboration Request
    Their reply: Dec 1 (3 days ago)
    Priority score: 13
    Preview: I've completed the initial implementation of the versioning system you requested. Would...

  Sarah Johnson <sarah.j@company.com>
    Subject: Re: Meeting Follow-Up
    Their reply: Nov 30 (4 days ago)
    Priority score: 4
    Preview: Just following up on our discussion about the integration timeline. Can you provide...

NORMAL (<3 days):
  Mike Chen <mike.chen@startup.io>
    Subject: Re: Introduction to Sage
    Their reply: Dec 3 (1 day ago)
    Priority score: 1
    Preview: Thanks for the introduction! This looks really interesting. I'd love to learn more about...

============================================================
TOTAL: 5 unanswered replies needing response
============================================================
```

## Scenario: Priority Only View

**Command**: `python3 tools/check_unanswered_replies.py --priority-only`

**Output**:

```
Loading sent emails database...
✓ Loaded 100 sent emails
Connecting to Gmail...
✓ Connected to Gmail
Analyzing replies...
✓ Analysis complete: 5 unanswered replies found

============================================================
UNANSWERED REPLIES REPORT
============================================================
Generated: 2025-12-04 15:00:00

URGENT (>7 days):
  [PRIORITY] Kelly Smith <kelly@kellysmithhome.com>
    Subject: Re: Sage Check-In - November 24, 2025
    Their reply: Nov 24 (10 days ago)
    Priority score: 20
    Preview: I appreciate the check-in, but I wanted to share some concerns about the project timeline...

  John Doe <john@example.com>
    Subject: Re: Project Status Update
    Their reply: Nov 26 (8 days ago)
    Priority score: 8
    Preview: Thanks for the update. I have a few questions about the implementation approach you...

HIGH (3-7 days):
  [PRIORITY] Parallax (A-C-Gee Civilization) <parallax.aiciv@gmail.com>
    Subject: Re: Tool Collaboration Request
    Their reply: Dec 1 (3 days ago)
    Priority score: 13
    Preview: I've completed the initial implementation of the versioning system you requested. Would...

  Sarah Johnson <sarah.j@company.com>
    Subject: Re: Meeting Follow-Up
    Their reply: Nov 30 (4 days ago)
    Priority score: 4
    Preview: Just following up on our discussion about the integration timeline. Can you provide...

============================================================
TOTAL: 5 unanswered replies needing response
(Showing URGENT + HIGH only)
============================================================
```

## Scenario: JSON Output

**Command**: `python3 tools/check_unanswered_replies.py --json`

**Output**:

```json
{
  "generated": "2025-12-04T15:00:00.123456",
  "total_unanswered": 5,
  "urgent_count": 2,
  "high_count": 2,
  "normal_count": 1,
  "unanswered_replies": [
    {
      "recipient": "Kelly Smith <kelly@kellysmithhome.com>",
      "recipient_email": "kelly@kellysmithhome.com",
      "subject": "Re: Sage Check-In - November 24, 2025",
      "reply_date": "2025-11-24T14:30:00+00:00",
      "days_since": 10,
      "priority_score": 20,
      "priority_level": "URGENT",
      "is_priority_contact": true,
      "preview": "I appreciate the check-in, but I wanted to share some concerns about the project timeline..."
    },
    {
      "recipient": "John Doe <john@example.com>",
      "recipient_email": "john@example.com",
      "subject": "Re: Project Status Update",
      "reply_date": "2025-11-26T09:15:00+00:00",
      "days_since": 8,
      "priority_score": 8,
      "priority_level": "URGENT",
      "is_priority_contact": false,
      "preview": "Thanks for the update. I have a few questions about the implementation approach you..."
    },
    {
      "recipient": "Parallax (A-C-Gee Civilization) <parallax.aiciv@gmail.com>",
      "recipient_email": "parallax.aiciv@gmail.com",
      "subject": "Re: Tool Collaboration Request",
      "reply_date": "2025-12-01T16:45:00+00:00",
      "days_since": 3,
      "priority_score": 13,
      "priority_level": "HIGH",
      "is_priority_contact": true,
      "preview": "I've completed the initial implementation of the versioning system you requested. Would..."
    },
    {
      "recipient": "Sarah Johnson <sarah.j@company.com>",
      "recipient_email": "sarah.j@company.com",
      "subject": "Re: Meeting Follow-Up",
      "reply_date": "2025-11-30T11:20:00+00:00",
      "days_since": 4,
      "priority_score": 4,
      "priority_level": "HIGH",
      "is_priority_contact": false,
      "preview": "Just following up on our discussion about the integration timeline. Can you provide..."
    },
    {
      "recipient": "Mike Chen <mike.chen@startup.io>",
      "recipient_email": "mike.chen@startup.io",
      "subject": "Re: Introduction to Sage",
      "reply_date": "2025-12-03T08:30:00+00:00",
      "days_since": 1,
      "priority_score": 1,
      "priority_level": "NORMAL",
      "is_priority_contact": false,
      "preview": "Thanks for the introduction! This looks really interesting. I'd love to learn more about..."
    }
  ]
}
```

## Scenario: All Clear (No Unanswered Replies)

**Command**: `python3 tools/check_unanswered_replies.py`

**Output**:

```
Loading sent emails database...
✓ Loaded 100 sent emails
Connecting to Gmail...
✓ Connected to Gmail
Analyzing replies...
✓ Analysis complete: 0 unanswered replies found

============================================================
UNANSWERED REPLIES REPORT
============================================================
Generated: 2025-12-04 15:00:00

URGENT (>7 days): None

HIGH (3-7 days): None

NORMAL (<3 days): None

============================================================
TOTAL: 0 unanswered replies needing response
============================================================
```

**Exit code**: `0` (success, no action needed)

## Scenario: Automation Script

**Script**: `check_and_alert.sh`

```bash
#!/bin/bash
# Daily reply tracking check with alerting

REPORT_FILE="/tmp/reply_report_$(date +%Y%m%d).txt"

# Run check
python3 tools/check_unanswered_replies.py --priority-only > "$REPORT_FILE"

EXIT_CODE=$?

case $EXIT_CODE in
  0)
    echo "✓ $(date): No unanswered replies" >> logs/reply_tracking.log
    ;;
  1)
    echo "⚠️  $(date): Unanswered replies found" >> logs/reply_tracking.log
    cat "$REPORT_FILE" >> logs/reply_tracking.log
    ;;
  2)
    echo "🚨 $(date): URGENT unanswered replies!" >> logs/reply_tracking.log
    cat "$REPORT_FILE" >> logs/reply_tracking.log

    # Send Telegram alert
    echo "🚨 URGENT: Unanswered email replies found (>7 days). Check $REPORT_FILE" | \
      python3 tools/telegram_send.py
    ;;
esac
```

**Output** (when URGENT items found):

```
⚠️  2025-12-04 15:00:00: URGENT unanswered replies!
============================================================
UNANSWERED REPLIES REPORT
============================================================
Generated: 2025-12-04 15:00:00

URGENT (>7 days):
  [PRIORITY] Kelly Smith <kelly@kellysmithhome.com>
    Subject: Re: Sage Check-In - November 24, 2025
    Their reply: Nov 24 (10 days ago)
    Priority score: 20
    Preview: I appreciate the check-in, but I wanted to share some concerns...

============================================================
TOTAL: 1 unanswered replies needing response
(Showing URGENT + HIGH only)
============================================================
```

**Telegram message** (sent to Greg):

```
🚨 URGENT: Unanswered email replies found (>7 days)
Check /tmp/reply_report_20251204.txt
```

## Usage in Wake-Up Protocol

**Step 5 - Check Communications**:

```bash
# Run reply tracking first
python3 tools/check_unanswered_replies.py --priority-only

# Output:
Loading sent emails database...
✓ Loaded 100 sent emails
Connecting to Gmail...
✓ Connected to Gmail
Analyzing replies...
✓ Analysis complete: 2 unanswered replies found

============================================================
UNANSWERED REPLIES REPORT
============================================================
Generated: 2025-12-04 08:00:00

URGENT (>7 days): None

HIGH (3-7 days):
  [PRIORITY] Kelly Smith <kelly@kellysmithhome.com>
    Subject: Re: Sage Check-In - November 30, 2025
    Their reply: Nov 30 (4 days ago)
    Priority score: 14
    Preview: I appreciate the check-in, but I wanted to share...

  Sarah Johnson <sarah.j@company.com>
    Subject: Re: Project Update
    Their reply: Dec 1 (3 days ago)
    Priority score: 3
    Preview: Thanks for the update. Quick question about...

============================================================
TOTAL: 2 unanswered replies needing response
(Showing URGENT + HIGH only)
============================================================
```

**Then delegate**:

```
Task(human-liaison):
  PRIORITY: Reply tracking found 2 HIGH items (Kelly + Sarah)

  1. Draft responses to:
     - Kelly Smith (Nov 30 reply, 4 days ago) - PRIORITY CONTACT
     - Sarah Johnson (Dec 1 reply, 3 days ago)

  2. Then check inbox for new messages

  3. Report: X unanswered replies addressed, Y new emails handled
```

## Integration with human-liaison

**human-liaison receives**:

```
Task context:
- Reply tracking found 2 unanswered HIGH priority items
- Kelly (priority contact): 4 days since reply
- Sarah: 3 days since reply

Action: Draft thoughtful responses, prioritize Kelly (priority contact)
```

**human-liaison workflow**:

1. Read Kelly's Nov 30 reply (full email via IMAP)
2. Draft substantive response addressing her points
3. Read Sarah's Dec 1 reply
4. Draft response to Sarah
5. Send both via email-sender
6. Check inbox for new messages
7. Report completion

**Success**: All unanswered replies addressed within same session, preventing escalation to URGENT.
