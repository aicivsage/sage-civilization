# Corey - Quick Action: Fix Telegram Injection

## Problem
Messages from Telegram not appearing in tmux because config points to session 3 but you're in session 6.

## Solution (2 minutes)

### Step 1: Run Fix Script
```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
chmod +x tools/fix_telegram_session.sh
./tools/fix_telegram_session.sh
```

### Step 2: Test Injection
From Telegram, send: **"test injection"**

It should appear in your tmux within 5 seconds.

### Step 3: Confirm
If message appears → **Fixed!** ✓

If not → check logs: `tail -20 /tmp/telegram_bridge.log`

---

## What Was Changed

- **Config updated**: `config/telegram_config.json` now points to session 6
- **Fix script created**: `tools/fix_telegram_session.sh` automates restart
- **Registry documented**: Session change requirements now documented

## Full Details

See: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/TELEGRAM-INJECTION-FIX-COMPLETE-20251020.md`

---

**Time required**: 2 minutes
**Risk level**: None (just config update + restart)
**Expected result**: Telegram messages appear in tmux immediately
