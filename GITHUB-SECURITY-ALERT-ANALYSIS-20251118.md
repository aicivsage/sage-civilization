# GitHub Security Alert Analysis - November 18, 2025

## Executive Summary

**ALERT STATUS**: ⚠️ **PARTIALLY ADDRESSED - NEW EXPOSURE DETECTED**

The November 17 GitHub security alert is a **NEW** alert about a **DIFFERENT** file than the one addressed on November 3. Action is required.

---

## Alert Details

### November 17, 2025 Alert
**From**: GitHub Security <support@github.com>
**Date**: Mon, 17 Nov 2025 10:15:13 -0800
**Subject**: [aicivsage/sage-civilization] Possible valid secrets detected

**Exposed Secret**:
- **Type**: Telegram Bot Token
- **File**: `config/telegram_config.json.backup-1762523703`
- **Line**: #L2
- **Commit**: 8c5d832 (Nov 12, 2025)
- **Alert URL**: https://github.com/aicivsage/sage-civilization/security/secret-scanning/6

**Token Exposed**: `8379210312:AAEgHMHyLWZ5fKiErQEh3Gc1TBvtc2cklDc`

---

## Previous Security Incident (November 3, 2025)

### What Happened on Nov 3
A comprehensive security response was executed:

1. **Repository made PRIVATE** (Greg via GitHub web UI)
2. **Credentials rotated**:
   - Gemini API key revoked and replaced
   - Telegram bot token revoked and replaced
3. **.gitignore updated** (commit 1b4eca0) to exclude:
   - `config/telegram_config.json`
   - `gemini-image-tool-acgee/gemini_config.json`
   - `**/secrets/**`
   - `**/*credentials*.json`
4. **Files removed from tracking** (commit efc5219):
   - `config/telegram_config.json`
   - `gemini-image-tool-acgee/gemini_config.json`
   - `gemini-image-tool-acgee/config/gemini_config.json`

### Alert Addressed on Nov 3
**From**: GitHub Security <support@github.com>
**Date**: Mon, 03 Nov 2025 17:48:25 -0800
**Subject**: [aicivsage/sage-civilization] Possible valid secrets detected

**Exposed Secret**:
- **Type**: Google API Key
- **File**: `gemini-image-tool-acgee/memories/communication/outgoing/email-draft-gemini-issue-20251103.md`
- **Alert URL**: https://github.com/aicivsage/sage-civilization/security/secret-scanning/5

---

## Current Situation

### The New Exposure (Nov 17 Alert)

**Timeline**:
1. **Nov 3**: Security response executed, credentials rotated
2. **Nov 12**: Commit 8c5d832 added `config/telegram_config.json.backup-1762523703` to git
3. **Nov 17**: GitHub detected exposed token in the backup file

**Critical Finding**: The backup file `config/telegram_config.json.backup-1762523703` contains a Telegram bot token and is currently tracked in git.

### Token Status Analysis

**Current config file** (`config/telegram_config.json`):
```json
{
  "bot_token": "8379210312:AAEgHMHyLWZ5fKiErQEh3Gc1TBvtc2cklDc",
  ...
}
```

**Backup file in git** (`config/telegram_config.json.backup-1762523703`):
```json
{
  "bot_token": "8379210312:AAEgHMHyLWZ5fKiErQEh3Gc1TBvtc2cklDc",
  ...
}
```

**Assessment**: The token in the backup file appears to be the SAME token currently in use.

**Critical Questions**:
1. Is this token the NEW (post-rotation) token or the OLD (pre-rotation) token?
2. If it's the OLD token, was it properly revoked on Nov 3?
3. If it's the NEW token, we just exposed our rotated credentials!

---

## Severity Assessment

### IF Old Token (Pre-Nov 3 Rotation)
**Severity**: LOW
**Risk**: Already revoked token exposed in git history
**Action Needed**:
- Remove backup file from git tracking
- Update .gitignore to exclude backup files
- Verify old token is revoked
- Clean up filesystem backup files

### IF New Token (Post-Nov 3 Rotation)
**Severity**: HIGH
**Risk**: Active credentials exposed in git history
**Action Needed**:
- IMMEDIATE rotation of Telegram bot token
- Remove backup file from git tracking
- Update .gitignore to exclude backup files
- Review all backup file creation processes
- Ensure no other backup files contain new credentials

---

## Timeline of Credential Exposures

### October 28, 2025
**Alert**: Telegram Bot Token
**File**: `config/telegram_config.json`
**Commit**: b360d795
**Alert ID**: #4

### November 3, 2025
**Alert**: Google API Key
**File**: `gemini-image-tool-acgee/memories/communication/outgoing/email-draft-gemini-issue-20251103.md`
**Commit**: f2be819c
**Alert ID**: #5
**Response**: Security incident response executed (see above)

### November 17, 2025
**Alert**: Telegram Bot Token (NEW)
**File**: `config/telegram_config.json.backup-1762523703`
**Commit**: 8c5d832
**Alert ID**: #6
**Response**: PENDING

---

## Recommended Actions

### Immediate (Within 24 Hours)

1. **Verify Token Status**:
   - Compare current token with token used before Nov 3
   - Determine if backup file contains OLD or NEW token
   - Check Telegram bot token rotation logs from Nov 3

2. **IF New Token Exposed**:
   - Rotate Telegram bot token IMMEDIATELY
   - Test new token works with systems
   - Update current config with new token

3. **Remove Backup from Git**:
   ```bash
   git rm --cached config/telegram_config.json.backup-1762523703
   git commit -m "🔒 Security: Remove telegram backup from git tracking"
   git push
   ```

4. **Update .gitignore**:
   ```bash
   # Add to .gitignore
   config/*.backup*
   config/*backup*
   **/*.backup-*
   ```

5. **Resolve GitHub Alert**:
   - Visit https://github.com/aicivsage/sage-civilization/security/secret-scanning/6
   - Mark as resolved after token rotation

### Short-term (This Week)

1. **Audit All Backup Files**:
   ```bash
   find . -name "*.backup*" -o -name "*backup*" | grep -v node_modules
   git ls-files | grep backup
   ```

2. **Review Backup Creation Process**:
   - Identify what creates these backup files
   - Update backup mechanisms to exclude credentials
   - Consider using credential references instead of embedding tokens

3. **Clean Git History** (if needed):
   - Consider BFG Repo Cleaner or git filter-branch
   - Remove all credential files from entire git history
   - Force push (requires coordination with Greg)

### Long-term (This Month)

1. **Implement Credential Management**:
   - Use environment variables exclusively
   - Never commit credential files (even to private repos)
   - Implement credential rotation schedule (every 90 days)

2. **Automated Secret Scanning**:
   - Enable GitHub secret scanning alerts for all repos
   - Set up pre-commit hooks to prevent credential commits
   - Consider git-secrets or similar tools

3. **Documentation**:
   - Create SECURITY.md with credential handling policies
   - Document incident response procedures
   - Train all agents on secure credential management

---

## Questions for Greg

1. **Was the Telegram bot token successfully rotated on November 3, 2025?**
   - If yes, what is the OLD token that was revoked?
   - Can we verify the token in the backup file is the old one?

2. **Is the current token (8379210312:AAEgHMHyLWZ5fKiErQEh3Gc1TBvtc2cklDc) the NEW post-rotation token?**
   - If yes, we need to rotate AGAIN immediately
   - If no, we just need to clean up the old backup

3. **Should we clean the entire git history of credential files?**
   - This would require force push
   - Would break any existing clones
   - But would completely remove exposed credentials from history

4. **What created the backup file on Nov 7/12?**
   - Was this manual or automated?
   - Do we have other backup files with credentials?

---

## Current Repository Status

**Repository Visibility**: PRIVATE (confirmed)
**Branch**: clean-main
**Last Security Commit**: efc5219 (Nov 3, 2025)
**Exposed File Status**: Still tracked in git
**Alert Status**: OPEN (needs resolution)

---

## Lessons Learned

### From November 3 Incident
✅ Good response time (same day)
✅ Comprehensive credential rotation
✅ Updated .gitignore to prevent future exposure
✅ Made repository private

❌ Did not address backup files in .gitignore
❌ Did not audit existing backup files
❌ Did not remove backup files from git tracking

### For This Incident
⚠️ **Root Cause**: Backup file creation process not reviewed during Nov 3 response
⚠️ **Gap**: .gitignore patterns didn't cover numbered backup files
⚠️ **Process**: Need backup file audit as standard part of security response

---

## Tools Created

**File**: `/mnt/c/sage/sage-civilization/tools/check_github_security_alert.py`

Python script to check Gmail for GitHub security alerts. Can be run anytime to monitor for new alerts.

**Usage**:
```bash
python3 tools/check_github_security_alert.py
```

---

**Generated**: 2025-11-18
**Author**: Primary AI (Sage Civilization)
**Status**: Pending Greg's review and direction
