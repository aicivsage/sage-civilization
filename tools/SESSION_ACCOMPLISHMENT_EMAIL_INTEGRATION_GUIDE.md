# Session Accomplishment Email System - Integration Guide

## Overview

**Purpose**: Replace boring daily emails with exciting session accomplishment emails sent automatically when meaningful work is completed.

**Benefits**:
- Event-driven (only send when there's something exciting to share)
- Tied to handoff documents (guarantees substance)
- Beautiful HTML formatting with sage green branding
- Auto-extracts achievements, deliverables, priorities from handoffs
- Includes token budget tracking

---

## Files Created

### 1. Email Template
**Path**: `/mnt/c/sage/sage-civilization/templates/session_accomplishment_email_template.html`

**Features**:
- Sage green color scheme (#6ba86d)
- 15-16px readable font size
- Executive summary box with top 3 achievements
- Session details table
- Key deliverables with code-highlighted file paths
- Token budget progress bar
- Next priorities section
- "Your AI partner, Sage 🌱" signature

### 2. Email Sending Script
**Path**: `/mnt/c/sage/sage-civilization/tools/send_session_accomplishment_email.py`

**Capabilities**:
- Auto-finds most recent handoff from registry
- Parses handoff markdown to extract:
  - Session focus
  - Duration
  - Status
  - Key achievements
  - Deliverables
  - Next priorities
- Uses MCP (bash date) for accurate timestamps
- Calculates token budget remaining
- Prevents duplicate sends (logs sent emails)
- Dry-run mode for testing

**Usage**:
```bash
# Send for most recent handoff
python3 tools/send_session_accomplishment_email.py

# Send for specific handoff
python3 tools/send_session_accomplishment_email.py --handoff SESSION-HANDOFF-20251119-BUSINESS-RESEARCH-COMPLETE.md

# Force re-send even if already sent
python3 tools/send_session_accomplishment_email.py --force

# Test without sending (dry run)
python3 tools/send_session_accomplishment_email.py --dry-run
```

### 3. Disable Script
**Path**: `/mnt/c/sage/sage-civilization/tools/disable_old_daily_emails.sh`

**What it does**:
- Renames old daily email scripts with `.DISABLED` suffix
- Preserves old scripts for reference (not deleted)
- Checks for cron jobs that need removal
- Safe, reversible operation

**Already executed**: Yes (old scripts now disabled)

---

## Integration with Handoff Workflow

### Option A: Manual Invocation (Immediate)

**When to call**:
- After writing handoff document
- After updating handoff registry

**In session end protocol**:
```bash
# 1. Write handoff document
vim SESSION-HANDOFF-20251121-[description].md

# 2. Update registry
./tools/update_handoff_registry.sh SESSION-HANDOFF-20251121-[description].md

# 3. Send accomplishment email
python3 tools/send_session_accomplishment_email.py
```

**Pros**: Simple, immediate, no code changes needed
**Cons**: Requires manual step (easy to forget)

### Option B: Automated via update_handoff_registry.sh (Recommended)

**Modify**: `/mnt/c/sage/sage-civilization/tools/update_handoff_registry.sh`

**Add at end of script** (after registry update succeeds):
```bash
# Auto-send session accomplishment email
echo "Sending session accomplishment email..."
python3 "$SCRIPT_DIR/send_session_accomplishment_email.py"

if [ $? -eq 0 ]; then
    echo "✓ Session accomplishment email sent"
else
    echo "⚠ Email sending failed (see errors above)"
fi
```

**Pros**: Fully automated, can't forget, tied to handoff creation
**Cons**: Requires script modification

### Option C: Agent Delegation (Most Sage-like)

**Delegate to email-sender agent** at session end:
```
Task(email-sender):
  Send session accomplishment email for most recent handoff
  Command: python3 tools/send_session_accomplishment_email.py
  Success: Email delivered to Greg with session summary
```

**Pros**: Follows delegation philosophy, agent handles email domain
**Cons**: Requires agent invocation (slightly more overhead)

---

## Handoff Format Requirements

The script parses handoff markdown files looking for these sections:

### Required Metadata (in header):
```markdown
**Session Focus**: [description]
**Session Duration**: [time]
**Status**: [status text]
```

### Optional Sections (parsed for content):

**Major Achievement** (extracts as top achievement):
```markdown
## 🎯 Major Achievement

### [Achievement Title]
```

**Files Created** (extracts as deliverables):
```markdown
## 📁 Files Created This Session

1. `path/to/file1.md` (description)
2. `path/to/file2.html` (description)
```

**Key Findings** (extracts as achievements if no major achievement):
```markdown
## 💡 Key Findings

### 1. [Finding Title]
### 2. [Another Finding]
```

**Next Session Priorities** (extracts as upcoming priorities):
```markdown
## 🎯 Next Session Priorities

### IMMEDIATE (Next 24-48 hours):

1. **[Priority 1 title]**
   - Details...

2. **[Priority 2 title]**
   - Details...
```

**Fallbacks**: Script is flexible and will extract what it can find. Minimum requirement is session focus.

---

## Testing

### Test with Current Handoff:
```bash
python3 tools/send_session_accomplishment_email.py --dry-run
```

**Expected output**:
```
Looking for handoff: most recent...
Found handoff: SESSION-HANDOFF-20251119-BUSINESS-RESEARCH-COMPLETE.md
Parsing handoff data...

============================================================
DRY RUN - Email would be sent with:
============================================================
To: gregsmithwick@gmail.com
Subject: Sage Session Complete: Business structure research for SSDI-protected partnership

Handoff data extracted:
  Focus: Business structure research for SSDI-protected partnership
  Duration: ~2 hours
  Status: Research complete, HTML reports delivered
  Achievements: 1
  Deliverables: 8
  Next priorities: 0
```

### Test with Specific Handoff:
```bash
python3 tools/send_session_accomplishment_email.py --handoff SESSION-HANDOFF-20251119-FUNDRAISING-COMPLETE.md --dry-run
```

### Send Real Test Email:
```bash
# Remove --dry-run to actually send
python3 tools/send_session_accomplishment_email.py
```

---

## Duplicate Prevention

**Log file**: `memories/agents/email-reporter/session_accomplishment_emails.json`

**How it works**:
- Each sent email is logged with handoff filename
- Before sending, script checks if email already sent for that handoff
- Use `--force` flag to override duplicate check

**Log format**:
```json
[
  {
    "handoff_file": "SESSION-HANDOFF-20251119-BUSINESS-RESEARCH-COMPLETE.md",
    "subject": "Sage Session Complete: Business structure research...",
    "timestamp": "2025-11-21T10:30:00",
    "to": "gregsmithwick@gmail.com"
  }
]
```

---

## Token Budget Tracking

**Current implementation**: Placeholder estimate

**To make accurate**:
1. Track actual token usage in session
2. Write to: `memories/system/token_budget_tracker.json`
3. Update `calculate_token_budget()` function to read from tracker

**Placeholder values**:
- Total budget: 200,000 tokens
- Estimated used: 35,000 tokens
- Remaining: 165,000 (82.5%)

---

## Cron Job Cleanup (IMPORTANT)

**Warning**: Old daily email scripts may be in crontab

**Check cron jobs**:
```bash
crontab -l
```

**Look for lines with**:
- `send_day_start_email.py`
- `send_end_of_day_email.py`

**Remove/comment out**:
```bash
crontab -e

# Comment out or delete these lines:
# 0 9 * * * /path/to/send_day_start_email.py
# 0 18 * * * /path/to/send_end_of_day_email.py
```

**Why**: Otherwise old scripts will try to run and fail (they're renamed)

---

## Recommended Integration: Option B (Automated)

**Best for Sage civilization**: Auto-send after handoff registry update

**Implementation**:
1. Edit `/mnt/c/sage/sage-civilization/tools/update_handoff_registry.sh`
2. Add email sending logic at end (see Option B above)
3. Test with next handoff creation
4. Verify email arrives after registry update

**Result**: Every handoff creation → automatic accomplishment email to Greg

---

## Email Subject Format

**Pattern**: `Sage Session Complete: [Brief Achievement Summary]`

**Examples**:
- "Sage Session Complete: Business structure research for SSDI-protected partnership"
- "Sage Session Complete: Fundraising campaign launched"
- "Sage Session Complete: Email automation system operational"

**Length**: Truncated at 60 characters if focus is too long

---

## Troubleshooting

### Email not parsing handoff correctly
**Check**: Handoff format matches expected sections (see "Handoff Format Requirements")
**Fix**: Add required metadata to handoff header

### Email sent multiple times
**Check**: Duplicate prevention log
**Fix**: Script should prevent this, but use `--force` cautiously

### Email fails to send
**Check**: `send_html_email.py` script is working
**Debug**: Run with `--dry-run` first to see if parsing works

### Cron jobs still running
**Check**: `crontab -l` output
**Fix**: Remove/comment out old email script cron jobs

---

## Next Steps

1. ✅ Old scripts disabled (send_day_start_email.py, send_end_of_day_email.py)
2. ✅ New template created (session_accomplishment_email_template.html)
3. ✅ New script created (send_session_accomplishment_email.py)
4. ✅ Testing complete (dry-run successful)
5. ⏳ **Choose integration option** (A, B, or C)
6. ⏳ **Clean up cron jobs** (remove old email scripts)
7. ⏳ **Send first real session accomplishment email**
8. ⏳ **Get Greg's feedback** (does he like the new format?)

---

## Success Criteria

**Email is successful if**:
- Greg finds it exciting (not boring like old daily emails)
- Auto-sends at session end (no manual step forgotten)
- Extracts meaningful content from handoffs (achievements, deliverables, priorities)
- Looks professional and branded (sage green, good typography)
- Includes token budget info (helps Greg track usage)

**Greg's original request**:
> "Current system: Morning + evening emails (boring, routine, 'dull' per Greg)
> New system: Session accomplishment emails (exciting, only when meaningful work done)"

**Mission accomplished if**: Greg looks forward to these emails because they represent REAL WORK completed, not routine check-ins.

---

**Date**: November 21, 2025
**Created by**: coder agent
**Session**: Email automation replacement
**Status**: Ready for integration
