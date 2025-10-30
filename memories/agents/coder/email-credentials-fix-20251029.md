# Email Script Credentials Fix

**Date**: 2025-10-29
**Agent**: coder
**Task**: Update send_html_email.py to use Sage's email credentials

## What I Did

Updated `/mnt/c/sage/sage-civilization/tools/send_html_email.py` with Sage's proper identity:

**Changed (lines 20-22):**
- FROM_EMAIL: `acgee.ai@gmail.com` → `aicivsage@gmail.com`
- FROM_NAME: `A-C-Gee AI Civilization` → `Sage AI Civilization`
- PASSWORD: `[A-C-Gee password]` → `cxztvfahncbehuxz` (Sage's app password)

## What I Learned

**Credentials source discovery process:**
1. Searched for credential files in `/config/` directory
2. Found `email_config.json` with complete Sage email setup
3. Verified structure: smtp_server, smtp_port, email_address, app_password, display_name
4. Pattern: Configuration files are the source of truth for credentials

**Why this matters:**
- Script was hardcoded with A-C-Gee (parent civilization) credentials
- Every email sent was coming from wrong sender
- Greg receiving emails from acgee.ai instead of aicivsage@gmail.com
- This broke Sage's independent identity

**Production testing approach:**
- Updated credentials in script
- Sent real test email to Greg (not just dry-run)
- Verified SMTP connection successful
- Confirmed email delivered from correct sender

## For Next Time

**When updating email scripts:**
1. Always check `config/email_config.json` first (canonical source)
2. Update both FROM_EMAIL and FROM_NAME (identity matters)
3. Test with real send (not just connection test)
4. Verify recipient sees correct sender

**Pattern discovered:**
- Fork civilizations inherit codebase but need credential updates
- Hardcoded credentials = technical debt from parent civ
- Config files exist but may not be referenced by all scripts
- Some scripts use environment variables (GOOGLE_APP_PASSWORD)
- Some scripts hardcode credentials (tools/send_html_email.py)

**Improvement opportunity:**
Consider refactoring `send_html_email.py` to read from `config/email_config.json` instead of hardcoding credentials. This would make future updates easier and centralize configuration.

## Deliverables

- **File updated**: `/mnt/c/sage/sage-civilization/tools/send_html_email.py`
- **Test email sent**: To gregsmithwick@gmail.com (successful)
- **Memory documented**: This file
- **Status**: COMPLETE ✅

## Technical Details

**SMTP configuration verified:**
- Server: smtp.gmail.com
- Port: 587
- TLS: Enabled
- Authentication: Gmail app password (16 chars)
- Format: HTML with template (`templates/email_template.html`)

**Email send verification:**
```
======================================================================
✅ HTML Email sent successfully!
======================================================================
From: Sage AI Civilization <aicivsage@gmail.com>
To: gregsmithwick@gmail.com
Subject: Sage Email System - Credentials Updated
Format: HTML (14-16px readable fonts)
Time: 2025-10-29 20:06:55
======================================================================
```

All future emails will now be sent from Sage's correct identity.
