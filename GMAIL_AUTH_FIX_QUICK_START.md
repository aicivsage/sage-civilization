# Gmail Authentication Fix - Quick Start

**Status**: Email communication BROKEN - Needs immediate fix
**Account**: aicivsage@gmail.com
**Problem**: Invalid app-specific passwords

---

## TL;DR - Fix in 3 Steps

### Step 1: Generate New App-Specific Password
1. Go to: https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer" (or your device)
3. Google generates a 16-character password
4. **Copy this password** (you'll need it in Step 2)

### Step 2: Update Credentials in Code
Update these 3 files with the new password:

**File 1**: `.env`
```
EMAIL_APP_PASSWORD=YOUR_NEW_16_CHAR_PASSWORD_HERE
```

**File 2**: `tools/send_html_email.py` (line 15)
```python
PASSWORD = 'YOUR_NEW_16_CHAR_PASSWORD_HERE'
```

**File 3**: `tools/read_recent_emails.py` (line 11)
```python
PASSWORD = 'YOUR_NEW_16_CHAR_PASSWORD_HERE'
```

### Step 3: Test the Connection
```bash
# Test email sending
python3 tools/send_html_email.py \
  --to gregsmithwick@gmail.com \
  --subject "Gmail Auth Fixed" \
  --content "Email system is working!"

# Test email reading
python3 tools/read_recent_emails.py --count 5
```

---

## Why This Happened

Google deprecated less-secure app passwords in 2025. The system now requires:
- 2-Factor Authentication enabled ✓ (already is)
- App-Specific Password (not account password) ✗ (missing/expired)
- Regular passwords NO LONGER WORK for IMAP/SMTP

The old passwords are:
- `cxztvfahncbehuxz` (hardcoded in source) ❌ INVALID
- `Bulawayo1973` (in .env file) ❌ INVALID

---

## What's Broken Right Now

Without valid credentials:
- Greg won't receive session summaries
- System can't send him status updates
- No urgent alerts or notifications
- No response to his emails
- Zero communication with Greg

**This is CRITICAL - Email is the primary communication channel.**

---

## Estimated Time

- **Step 1** (Generate password): 2 minutes
- **Step 2** (Update 3 files): 5 minutes
- **Step 3** (Test): 5 minutes
- **TOTAL**: 12 minutes

---

## Detailed Diagnostic Info

For full technical details, see:
- `/mnt/c/sage/sage-civilization/GMAIL_AUTHENTICATION_DIAGNOSTIC.md`

For test scripts and debugging:
- `/tmp/test_gmail_smtp.py`
- `/tmp/test_gmail_connection.py`

---

## Security Note

⚠️ **After fixing**: Move away from hardcoded passwords
- Never commit real passwords to git
- Use environment variables (`.env` is better than hardcoding)
- Use OAuth2 tokens for production (best practice)
- Rotate credentials regularly

---

## Support

If you get stuck:
1. Check that 2FA is enabled: https://myaccount.google.com/security
2. Verify app password was generated correctly
3. Make sure you copied the full 16-character password
4. Try the test scripts above to debug
5. Check Gmail's security page: https://support.google.com/mail/?p=BadCredentials

Contact: Corey (coreycmusic@gmail.com) or Greg (gregsmithwick@gmail.com)
