# Email Automation Scripts - Sage Civilization

**Location**: `/mnt/c/sage/sage-civilization/tools/`

**Purpose**: Automated email schedule system for communicating with Greg on a predictable daily rhythm.

---

## Scripts Overview

### 1. `send_day_start_email.py` - Morning Session Start

**Purpose**: Send morning email when Primary AI starts first session of the day.

**What it does**:
- Checks if already sent today (prevents duplicates)
- Reads most recent handoff from HANDOFF_REGISTRY.json
- Checks for overnight developments (emails sent in last 12 hours)
- Fills template with:
  - Today's priorities (from handoff incomplete_items)
  - Overnight activity (recent emails)
  - Context from yesterday (handoff deliverables)
- Sends to gregsmithwick@gmail.com
- Updates state file to prevent duplicate sends

**Usage**:
```bash
# Normal use (prevents duplicate if already sent today)
python3 tools/send_day_start_email.py

# Force send even if already sent today
python3 tools/send_day_start_email.py --force

# Dry-run (preview without sending)
python3 tools/send_day_start_email.py --dry-run
```

**When to call**: First thing in morning session (after wake-up protocol)

---

### 2. `send_end_of_day_email.py` - Evening Summary

**Purpose**: Send end-of-day summary with accomplishments and tomorrow's priorities.

**What it does**:
- Gathers today's activity:
  - Git commits since midnight (`git log --since="today 00:00"`)
  - Emails sent today (from sent_emails.json)
  - Handoffs created today (from HANDOFF_REGISTRY.json)
- Fills template with:
  - Accomplishments (deliverables, commits, communications)
  - In-progress work (from handoff status)
  - Blocked items (from incomplete_items with blocker keywords)
  - Tomorrow's priorities (from most recent handoff)
  - Session statistics (hours, commits, emails)
- Sends to gregsmithwick@gmail.com
- Updates state file (increments end_of_day_count)

**Usage**:
```bash
# Normal use
python3 tools/send_end_of_day_email.py

# Dry-run (preview without sending)
python3 tools/send_end_of_day_email.py --dry-run
```

**When to call**:
- 6pm ET daily (via cron/scheduler)
- End of last session if before 6pm
- Manual for session summaries

---

### 3. `send_major_accomplishment_email.py` - Immediate Achievement Alert

**Purpose**: Send immediate email when significant accomplishments occur.

**What it does**:
- Takes command-line arguments for achievement details
- Formats bullet points and paragraphs into HTML
- Fills template with:
  - Achievement title
  - Detailed description (supports markdown-style bullets)
  - Why it matters (significance)
  - What's next (implications/next steps)
- Sends immediately (no duplicate checking - each achievement unique)
- Logs accomplishment to state file

**Usage**:
```bash
# Single-line details
python3 tools/send_major_accomplishment_email.py \
  --achievement "Blog published" \
  --details "Published 'Caring as Action' to Telegraph with 25K words" \
  --why-it-matters "First public-facing content from Sage civilization" \
  --whats-next "Send to priority contacts, await feedback"

# Multi-line details with bullets
python3 tools/send_major_accomplishment_email.py \
  --achievement "Replit integration complete" \
  --details "- Blog platform operational
- Comment system working
- Memory profiles active" \
  --why-it-matters "Enables public discourse and relationship building" \
  --whats-next "Publish next blog post on natural topics"

# Dry-run
python3 tools/send_major_accomplishment_email.py \
  --achievement "Test" \
  --details "Test details" \
  --why-it-matters "Testing" \
  --whats-next "Verify" \
  --dry-run
```

**When to call**: Immediately when major accomplishments occur

---

## State File

**Location**: `/mnt/c/sage/sage-civilization/memories/system/email_schedule_state.json`

**Format**:
```json
{
  "last_day_start_email": "2025-11-01",
  "day_start_count": 5,
  "end_of_day_count": 5,
  "major_accomplishments": [
    {
      "achievement": "Blog published",
      "timestamp": "2025-10-31T14:30:00.000000",
      "date": "2025-10-31"
    }
  ]
}
```

**Purpose**:
- Prevent duplicate day-start emails (checks `last_day_start_email`)
- Track email counts for metrics
- Log major accomplishments (last 50 kept)

---

## Templates

**Location**: `/mnt/c/sage/sage-civilization/templates/`

**Files**:
- `email_day_start.html` - Morning session start template
- `email_end_of_day.html` - Evening summary template
- `email_major_accomplishment.html` - Achievement alert template

**Placeholders** (replaced by scripts):
- `{date}` - Formatted date (e.g., "Friday, November 1, 2025")
- `{priorities}` - HTML list of today's priorities
- `{overnight_developments}` - HTML of overnight activity
- `{context_summary}` - HTML of yesterday's context
- `{accomplishments}` - HTML of today's accomplishments
- `{in_progress}` - HTML of in-progress work
- `{blocked}` - HTML of blocked items
- `{tomorrow_priorities}` - HTML of tomorrow's priorities
- `{stats}` - HTML of session statistics
- `{achievement}` - Achievement title
- `{details}` - HTML of achievement details
- `{why_it_matters}` - HTML of significance
- `{whats_next}` - HTML of next steps

---

## Dependencies

**Python**: 3.x (built-in libraries only)
- `sys`, `json`, `argparse`, `pathlib`, `datetime`, `subprocess`

**External scripts**:
- `tools/send_html_email.py` - Email sending utility (must exist)

**Data sources**:
- `memories/system/HANDOFF_REGISTRY.json` - Session handoffs
- `memories/agents/email-reporter/sent_emails.json` - Email log
- Git repository (for commit history)

---

## Error Handling

**Graceful degradation**:
- Missing handoff registry → Uses defaults
- Missing sent emails log → Empty list
- Git errors → Empty commit list
- Missing template → Error with clear message
- Email send failure → Returns exit code 1

**Exit codes**:
- `0` = Success (email sent or dry-run completed)
- `1` = Error (template missing, email failed, etc.)

---

## Integration Points

### Wake-Up Protocol
Add to Step 2 (after Telegram boot):
```bash
python3 tools/send_day_start_email.py
```

### Session End
Add to session end protocol:
```bash
python3 tools/send_end_of_day_email.py
```

### Cron Schedule (Future)
```cron
# Day start (8am ET = 12:00 UTC)
0 12 * * * cd /mnt/c/sage/sage-civilization && python3 tools/send_day_start_email.py

# End of day (6pm ET = 22:00 UTC)
0 22 * * * cd /mnt/c/sage/sage-civilization && python3 tools/send_end_of_day_email.py
```

### Primary AI Usage
```python
# Morning session start
Task(email-sender):
  Run: python3 tools/send_day_start_email.py

# Major accomplishment
Task(email-sender):
  Run: python3 tools/send_major_accomplishment_email.py \
    --achievement "[title]" \
    --details "[details]" \
    --why-it-matters "[significance]" \
    --whats-next "[next steps]"

# End of session
Task(email-sender):
  Run: python3 tools/send_end_of_day_email.py
```

---

## Testing

**Dry-run all scripts**:
```bash
# Test day start
python3 tools/send_day_start_email.py --dry-run

# Test end of day
python3 tools/send_end_of_day_email.py --dry-run

# Test major accomplishment
python3 tools/send_major_accomplishment_email.py \
  --achievement "Test" \
  --details "Testing script" \
  --why-it-matters "Quality assurance" \
  --whats-next "Deploy" \
  --dry-run
```

**Verify state file**:
```bash
cat memories/system/email_schedule_state.json
```

**Check sent emails log**:
```bash
cat memories/agents/email-reporter/sent_emails.json
```

---

## Design Philosophy

**Predictable rhythm**: Greg knows when to expect emails (morning, evening, major events)

**Rich context**: Each email includes actionable information, not just "I'm working"

**No spam**: Day-start prevents duplicates, end-of-day once daily, accomplishments only when significant

**Graceful degradation**: Missing data sources don't crash - scripts adapt

**Observable state**: State file provides audit trail and metrics

**Template-based**: Easy to update email styling without touching Python

---

## Maintenance

**Update templates**: Edit HTML in `templates/` directory

**Add new placeholders**:
1. Add `{new_placeholder}` to template
2. Add `html_body.replace('{new_placeholder}', value)` to script

**Change email recipient**: Update `TO_EMAIL` constant in each script

**Add new data sources**: Extend `get_*()` functions in scripts

**Debugging**: Use `--dry-run` flag to preview without sending

---

**Created**: 2025-11-01 by coder agent
**Status**: Production-ready, tested with dry-run
**Version**: 1.0
