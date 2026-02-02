# Email Authentication Fix Guide - 5 Minute Solution

**Problem:** Gmail authentication has been broken since December 26, 2025
**Impact:** Cannot read incoming emails or send responses (communication bridge is down)
**Solution:** Generate new app-specific password and update credentials

---

## Step 1: Generate New App-Specific Password (2 minutes)

1. Go to https://myaccount.google.com/apppasswords
2. Sign in if prompted
3. Select app: **Mail**
4. Select device: **Other (Custom name)**
5. Enter name: `Sage Civilization Email Access`
6. Click **Generate**
7. Copy the 16-character password (format: `xxxx xxxx xxxx xxxx`)
8. **SAVE THIS PASSWORD** - you'll need it in Step 2

---

## Step 2: Update Email Credentials (3 minutes)

### Option A: Quick Update (if .env file exists)

1. Open `/mnt/c/sage/sage-civilization/.env` in text editor
2. Find these lines:
   ```
   GMAIL_USER=your-email@gmail.com
   GMAIL_APP_PASSWORD=old-password-here
   ```
3. Replace `old-password-here` with the new 16-character password (no spaces)
4. Save the file

### Option B: Create .env File (if doesn't exist)

1. Create new file: `/mnt/c/sage/sage-civilization/.env`
2. Add these lines (replace with your actual credentials):
   ```
   GMAIL_USER=greg.reeves@sageandweaver.com
   GMAIL_APP_PASSWORD=your-new-16-char-password
   ```
3. Save the file

### Option C: Let Primary Update Programmatically

1. Paste the new password into chat
2. Say: "Sage, update email credentials with this password: [paste password]"
3. I'll update all necessary files automatically

---

## Step 3: Verify Email Access (30 seconds)

After updating credentials, I can verify access works:

**Quick test command:**
```bash
python3 tools/check_inbox.py
```

**Expected success output:**
```
✅ Connected to Gmail successfully
📧 Inbox status: X unread messages
```

**If still failing:**
- Double-check password has no spaces
- Verify you used "app-specific password" not regular Gmail password
- Ensure 2-factor authentication is enabled on Gmail account

---

## What This Fixes

**Before (Broken):**
- ❌ Cannot read incoming emails
- ❌ Cannot send responses via email
- ❌ Communication bridge partially down
- ❌ Missing Greg's emails for over a week

**After (Fixed):**
- ✅ Full inbox monitoring restored
- ✅ Can respond to urgent emails within 30 minutes
- ✅ Communication infrastructure operational
- ✅ BOOP alerts will work correctly

---

## Why This Broke

Gmail app-specific passwords expire or get revoked for security reasons. This is normal and happens periodically. The fix is simple: generate new password and update credentials.

**Prevention:** We should test email authentication weekly as part of infrastructure health checks.

---

## Choose Your Approach

**Fastest (5 minutes total):**
- Option C: Give me the new password, I'll update everything

**Most Control (5 minutes total):**
- Option A or B: Update .env file yourself, I verify it works

**Either way: This is a quick fix that restores critical infrastructure.**

---

## Need Help?

If you hit any issues:
1. Paste error message into chat
2. I'll diagnose and provide next steps
3. We'll get this working in minutes

---

**Status:** Ready to implement (awaiting your choice of Option A, B, or C)

**Estimated time to fix:** 5 minutes total
**Impact of fix:** Restores full email communication bridge
**Urgency:** High (has been broken for 8+ days)
