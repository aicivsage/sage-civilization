---
name: email-report
description: Send email report to user
usage: /email-report [type]
examples:
  - /email-report summary
  - /email-report health
  - /email-report mission-complete
---

# Email Report Command

## Purpose
Manually trigger an email notification to the user with a report of current civilization status.

## Parameters
- `type` (optional): Type of report to send
  - `summary`: Daily summary of activities
  - `health`: Health check report from auditor
  - `mission-complete`: Mission completion report
  - `test`: Test email to verify configuration
  - Default: `summary` if not specified

## Implementation

```bash
# Invoke the automated email system
python3 auto_email_report.py

# Or send a specific report type
python3 send_mission_report.py  # For mission complete reports
```

## Example Output

```
Sending email report...
✅ Email sent successfully to coreycmusic@gmail.com
Subject: 🤖 AI Civilization: Daily Summary
```

## Requirements
- Gmail credentials in `.env`:
  - `GMAIL_USERNAME`
  - `GOOGLE_APP_PASSWORD`
- Recipient email configured (default: coreycmusic@gmail.com)

## Related
- `/health-check`: Generate health report first
- `.claude/agents/email-monitor.md`: Automated email agent
- `auto_email_report.py`: Automation script
