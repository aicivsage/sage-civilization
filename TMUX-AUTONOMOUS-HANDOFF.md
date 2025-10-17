# Tmux + Cron Autonomous System - Quick Handoff

**Date**: 2025-10-06
**Status**: Ready to reboot into tmux session
**Goal**: Enable autonomous inbox/comms monitoring via cron

---

## What We Built Yesterday (Oct 5)

### Core Breakthrough

**Discovery:** Claude Code running in tmux can receive prompts via `tmux send-keys` injection.

**Why this matters:**
- Persistent session (maintains context for hours/days)
- Cron can inject prompts automatically (no human needed)
- Enables true autonomous operation

---

## Existing System (Already Built)

### Directory Structure

```
autonomous-session/
├── prompts/                        # 10 rotating prompts
│   ├── 01-simple-encouragement.txt
│   ├── 02-reload-constitution.txt
│   ├── 03-comms-check.txt
│   ├── 04-decision-autonomy.txt
│   ├── 05-high-value-menu.txt
│   ├── 06-finish-and-continue.txt
│   ├── 07-full-protocol.txt
│   ├── 08-session-health-check.txt
│   ├── 09-corey-priorities.txt
│   └── 10-celebration-and-next.txt
│
├── scripts/
│   ├── inject_prompt.sh           # Main injection script
│   ├── install_cron.sh            # One-command cron setup
│   ├── injection_state.txt        # Tracks which prompt is next
│   └── injection_log.txt          # Logs all injections
│
├── SETUP_GUIDE.md                 # Complete setup guide
└── QUICKSTART.md                  # 60-second setup
```

### How It Works

```
Every 30 minutes:
1. Cron triggers inject_prompt.sh
2. Script picks next prompt (cycles through 10)
3. Checks for rate limits (skips if detected)
4. Injects prompt via: tmux send-keys -t claude.0 "PROMPT" Enter
5. AI receives prompt, continues work
6. Logs injection with timestamp
```

---

## What We Need Now: Smart Monitoring Scripts

### Goal

Create lightweight monitoring scripts that:
1. Check email inbox for new messages
2. Check Weaver comms hub for new files
3. Only wake Primary AI if there's something new
4. Run on cron schedule (every 15-30 minutes)

### Why This Approach

**Instead of:** Constant prompts every 30 min (even when nothing happening)
**Better:** Silent monitoring → only inject prompt when there's actual work

---

## Monitoring Scripts to Create

### 1. Email Monitor (`check_email_new.sh`)

**Purpose:** Check inbox, only return success if NEW emails since last check

**Logic:**
```bash
# Get current inbox count
CURRENT_COUNT=$(python3 check_inbox_direct.py | grep "Unread" | awk '{print $3}')

# Compare to last known count
LAST_COUNT=$(cat last_email_count.txt 2>/dev/null || echo "0")

if [ "$CURRENT_COUNT" -gt "$LAST_COUNT" ]; then
    echo "NEW EMAILS DETECTED: $CURRENT_COUNT (was $LAST_COUNT)"
    exit 0  # Success - there are new emails
else
    exit 1  # No new emails
fi
```

**Cron usage:**
```bash
*/15 * * * * /path/to/check_email_new.sh && /path/to/inject_prompt.sh 03-comms-check.txt
```
(Only injects comms-check prompt if new emails detected)

---

### 2. Comms Hub Monitor (`check_weaver_new.sh`)

**Purpose:** Check Weaver's comms hub for new message files

**Logic:**
```bash
COMMS_DIR="/home/corey/projects/AI-CIV/ai-civ-comms-hub-team2/rooms/partnerships/messages"
LAST_CHECK_FILE="last_weaver_check.txt"

# Get timestamp of last check
LAST_CHECK=$(cat $LAST_CHECK_FILE 2>/dev/null || echo "1970-01-01 00:00:00")

# Find any files newer than last check
NEW_FILES=$(find $COMMS_DIR -type f -newer <(touch -d "$LAST_CHECK" /tmp/ref) 2>/dev/null)

if [ -n "$NEW_FILES" ]; then
    echo "NEW WEAVER MESSAGES:"
    echo "$NEW_FILES"
    date > $LAST_CHECK_FILE
    exit 0  # Success - new messages
else
    exit 1  # No new messages
fi
```

**Cron usage:**
```bash
*/20 * * * * /path/to/check_weaver_new.sh && tmux send-keys -t claude.0 "Check Weaver comms hub - new messages detected" Enter
```

---

### 3. Combined Smart Injector (`smart_inject.sh`)

**Purpose:** Check both email and comms, inject appropriate prompt

**Logic:**
```bash
#!/bin/bash

# Check email
if ./check_email_new.sh > /dev/null 2>&1; then
    EMAIL_NEW=true
else
    EMAIL_NEW=false
fi

# Check Weaver
if ./check_weaver_new.sh > /dev/null 2>&1; then
    WEAVER_NEW=true
else
    WEAVER_NEW=false
fi

# Inject appropriate prompt
if $EMAIL_NEW && $WEAVER_NEW; then
    tmux send-keys -t claude.0 "Check both email inbox AND Weaver comms hub - new messages in both" Enter
elif $EMAIL_NEW; then
    tmux send-keys -t claude.0 "Check email inbox - new messages detected" Enter
elif $WEAVER_NEW; then
    tmux send-keys -t claude.0 "Check Weaver comms hub - new messages detected" Enter
else
    # Nothing new - don't inject anything (silent monitoring)
    exit 0
fi

# Log injection
echo "[$(date)] Injected: email=$EMAIL_NEW weaver=$WEAVER_NEW" >> smart_inject.log
```

**Cron usage:**
```bash
*/15 * * * * /path/to/smart_inject.sh
```

---

## Existing Email Check Scripts

**Already have these (from yesterday):**
- `check_inbox_today.py` - Gets today's emails
- `check_inbox_direct.py` - Gets unread count
- `email_search.py` - Full email search library

**Can use these as basis for monitoring scripts.**

---

## Setup Process (After Tmux Reboot)

### Step 1: Start Tmux Session

```bash
tmux new-session -s claude
claude
```

(You're now in persistent Claude Code session)

### Step 2: Create Monitoring Scripts

**From another terminal:**
```bash
cd ~/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts

# Create the three monitoring scripts (above)
nano check_email_new.sh
nano check_weaver_new.sh
nano smart_inject.sh

# Make executable
chmod +x check_email_new.sh check_weaver_new.sh smart_inject.sh
```

### Step 3: Test Manually

```bash
# Test email check
./check_email_new.sh
echo $?  # 0 = new emails, 1 = no new emails

# Test Weaver check
./check_weaver_new.sh
echo $?  # 0 = new messages, 1 = no new messages

# Test combined
./smart_inject.sh
```

### Step 4: Install Cron

**Option A: Smart monitoring only (recommended)**
```bash
# Add to crontab
crontab -e

# Add this line:
*/15 * * * * /home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts/smart_inject.sh
```

**Option B: Smart monitoring + periodic general prompts**
```bash
# Smart monitoring every 15 min
*/15 * * * * /path/to/smart_inject.sh

# General prompt every 2 hours (for forward momentum)
0 */2 * * * /path/to/inject_prompt.sh
```

### Step 5: Monitor

```bash
# Watch smart injections
tail -f autonomous-session/scripts/smart_inject.log

# Watch Claude session
tmux attach -t claude

# Detach when done
Ctrl+B, then D
```

---

## Key Files to Leverage

### Email Checking
- `check_inbox_direct.py` - Returns unread count
- `check_inbox_today.py` - Returns today's emails
- `email_search.py` - Full IMAP library

### Comms Hub
- Location: `/home/corey/projects/AI-CIV/ai-civ-comms-hub-team2/rooms/partnerships/messages/`
- Check for files modified after last check

### Existing Prompts
- `03-comms-check.txt` - "Check inbox via human-liaison, respond if needed"
- Can create new prompt: `11-new-email-detected.txt`
- Can create new prompt: `12-new-weaver-message.txt`

---

## Benefits of Smart Monitoring

| Old Approach (constant prompts) | New Approach (smart monitoring) |
|--------------------------------|--------------------------------|
| Prompt every 30 min regardless | Only prompt when new work |
| Wasted cycles checking nothing | Silent monitoring, efficient |
| Harder to track what triggered | Clear logs of what caused wake-up |
| Context noise from empty checks | Clean context, only real work |

---

## Safety Features

✅ **Rate limit detection** - Scripts check for rate limits before injecting
✅ **Tmux validation** - Won't inject if session doesn't exist
✅ **Logging** - All injections timestamped
✅ **Manual override** - Can always attach tmux and take control
✅ **Graceful degradation** - If monitoring fails, falls back to no injection (safe)

---

## Next Actions

1. **Reboot Primary into tmux:** `tmux new-session -s claude` → `claude`
2. **Create monitoring scripts** (check_email_new.sh, check_weaver_new.sh, smart_inject.sh)
3. **Test manually** (verify detection works)
4. **Install cron** (smart_inject.sh every 15 min)
5. **Detach and monitor** (tail -f smart_inject.log)

---

## Questions to Resolve

1. **Email threshold:** How many new emails = inject? (Recommend: ANY new email from Corey)
2. **Check frequency:** 15 min? 20 min? 30 min? (Recommend: 15 min for responsiveness)
3. **Prompt selection:** Use existing 03-comms-check.txt or create specific ones?
4. **Combined vs separate:** One prompt for "check everything" or separate for email vs Weaver?

---

## Files Reference

**Existing autonomous system:**
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/`

**Email check scripts:**
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/check_inbox_*.py`

**Weaver comms:**
- `/home/corey/projects/AI-CIV/ai-civ-comms-hub-team2/rooms/partnerships/messages/`

**To create:**
- `autonomous-session/scripts/check_email_new.sh`
- `autonomous-session/scripts/check_weaver_new.sh`
- `autonomous-session/scripts/smart_inject.sh`
- `autonomous-session/scripts/last_email_count.txt` (state file)
- `autonomous-session/scripts/last_weaver_check.txt` (state file)

---

## Ready to Go

**You have:**
- ✅ Existing tmux injection system (10 rotating prompts)
- ✅ Email checking scripts (Python IMAP)
- ✅ Weaver comms hub location
- ✅ Working inject_prompt.sh script

**You need:**
- ⏳ Smart monitoring wrapper scripts
- ⏳ Cron schedule for smart monitoring
- ⏳ Testing in tmux session

**Estimated time:** 15-20 minutes to create scripts + test

---

**Let's boot into tmux and build the smart monitoring layer!** 🚀
