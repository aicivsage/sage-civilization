# Primary Telegram Integration Protocol

**Version**: 1.0
**Date**: 2025-10-18
**Purpose**: Define how Primary AI should use Telegram infrastructure
**Status**: CANONICAL - This is the official protocol

---

## Quick Reference for Primary

### How to Send Messages to Corey

**Direct send (most common):**
```bash
python3 /home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/send_telegram_direct.py 437939400 "Your message here"
```

**Or delegate to tg-archi:**
```
Task(tg-archi):
  Send message to Corey: "Your message here"
```

**Send file attachment:**
```bash
python3 /home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/send_telegram_file.py 437939400 /path/to/file.txt "Optional caption"
```

---

## Auto-Mirroring System (Wrapper Protocol)

### How It Works

When you wrap your output with special markers, the Telegram monitor automatically sends it to Corey's phone.

**Wrapper syntax:**
```
🤖🎯📱
Your message content here
Can be multiple lines
Can include markdown formatting
✨🔚
```

**Example:**
```
🤖🎯📱
Session starting at 14:30!

Today's priorities:
- Check email inbox
- Review Weaver messages
- Continue health-bot development

Ready to orchestrate!
✨🔚
```

**What happens:**
1. You output the wrapped message to tmux
2. `telegram_monitor.py` polls tmux every 5 minutes
3. Monitor detects the wrapper markers
4. Monitor calls `send_telegram_direct.py` to send the content
5. Corey receives notification on his phone
6. Monitor logs the send in `.tg_sessions/monitor_state.json` (prevents duplicates)

**Key points:**
- Use wrappers for **session start summaries**, **session end summaries**, **important milestones**
- DON'T wrap every message - use for significant updates only
- Wrappers support Markdown formatting (bold, italic, code blocks)
- Monitor removes the wrapper emojis before sending (Corey sees clean message)

---

## The Three Telegram Scripts

### 1. send_telegram_direct.py (PRIMARY SENDER)

**Status**: PRODUCTION - This is your default
**Use for**: All standard messages from Primary or agents
**Features**:
- Markdown formatting support (bold, italic, code blocks)
- Auto-chunking for long messages (>4096 chars)
- Used by telegram_monitor.py for auto-mirroring
- Battle-tested and reliable

**When to use**:
- Direct sends from Primary
- Auto-mirroring via monitor
- All production message sending

**NEVER replace with experimental alternatives in production systems.**

### 2. send_telegram_file.py (FILE SENDER)

**Status**: PRODUCTION
**Use for**: Sending attachments (logs, screenshots, documents)
**Features**:
- Sends any file type
- Optional caption support
- Handles images, PDFs, text files, etc.

**When to use**:
- Sharing log files with Corey
- Sending screenshots for debugging
- Delivering generated documents

### 3. send_telegram_plain.py (EXPERIMENTAL)

**Status**: EXPERIMENTAL - DO NOT USE IN PRODUCTION
**Use for**: Testing only
**Features**:
- Plain text only (no Markdown parsing)
- Created during investigation of markdown issues
- NOT integrated into production systems

**When to use**:
- Manual testing of plain text sending
- Troubleshooting markdown parsing issues

**NEVER use for**:
- Auto-mirroring (monitor must use send_telegram_direct.py)
- Production message sending
- Integration into other scripts

**Note**: This exists as a testing tool only. Keep separate from production.

---

## Daemon Processes (Background Infrastructure)

### telegram_bridge.py (RECEIVER)

**Purpose**: Receives messages FROM Corey, injects to tmux
**How it works**:
- Long-polling Telegram API
- Listens for TEXT messages and PHOTOS
- Downloads photos to `.tg_sessions/received_files/{user_id}/`
- Injects content to tmux for Primary to see

**Running status**: Check with `ps aux | grep telegram_bridge.py`
**Auto-restart**: Via `telegram_health_check.sh`

**You don't call this directly - it's a daemon that runs continuously.**

### telegram_monitor.py (AUTO-MIRROR)

**Purpose**: Detects wrapped messages, sends to Telegram
**How it works**:
- Polls tmux every 5 minutes
- Looks for wrapper: `🤖🎯📱 ... ✨🔚`
- Extracts content between markers
- Calls `send_telegram_direct.py` to send
- Tracks sent messages to prevent duplicates

**Running status**: Check with `ps aux | grep telegram_monitor.py`
**Auto-restart**: Via `telegram_health_check.sh`

**CRITICAL**: Monitor always calls `send_telegram_direct.py`, never experimental alternatives.

**You don't call this directly - it's a daemon that runs continuously.**

---

## Health Monitoring (tg-archi's Job)

When you invoke tg-archi, they AUTOMATICALLY run health checks:

```bash
bash tools/telegram_health_check.sh
```

**What this does**:
1. Checks if `telegram_bridge.py` is running (restarts if dead)
2. Checks if `telegram_monitor.py` is running (restarts if dead)
3. Verifies recent log activity (within 60s)
4. Logs results to `/tmp/telegram_health_check.log`

**You don't need to remember this - tg-archi does it every time they're invoked.**

---

## Boot Message Template (For tg-archi)

When tg-archi starts Telegram systems, they should report:

```
Telegram systems online:
- Bridge (PID 12345): Bi-directional Telegram ↔ tmux
- Monitor (PID 12346): Auto-sends wrapped messages to Telegram

Primary reminder:
- Wrap messages for auto-mirroring: 🤖🎯📱 ... ✨🔚
- Direct send: python3 tools/send_telegram_direct.py 437939400 "message"
- Templates: source tools/telegram_templates.sh && tg_session_start
```

This reminds you of the wrapper protocol and available commands.

---

## Common Patterns

### Session Start Notification

**Option 1: Wrapper (auto-mirrored)**
```
🤖🎯📱
Session starting at 14:30!

Today's priorities:
- Email inbox check
- Weaver message review
- Health-bot development

Ready to orchestrate!
✨🔚
```

**Option 2: Bash template**
```bash
source tools/telegram_templates.sh && tg_session_start
```

### Session End Summary

**Option 1: Wrapper (auto-mirrored)**
```
🤖🎯📱
Session complete at 18:45!

Achievements:
- Email inbox cleared (3 responses sent)
- Weaver collaboration on browser-vision
- Health-bot API integration working

Next session priorities:
- Test health-bot end-to-end
- Send civilization update to Greg/Chris

See you next time!
✨🔚
```

**Option 2: Bash template**
```bash
source tools/telegram_templates.sh && tg_session_end
```

### Urgent Alert

**Direct send (immediate)**
```bash
python3 tools/send_telegram_direct.py 437939400 "🚨 URGENT: Email from Corey requires response!"
```

**Or bash template**
```bash
source tools/telegram_templates.sh && tg_urgent "Email from Corey requires response"
```

### Sharing a Log File

```bash
python3 tools/send_telegram_file.py 437939400 /tmp/error.log "Error log from health-bot testing"
```

---

## What NOT to Do

### ❌ DON'T modify telegram_monitor.py to use experimental senders

**WRONG:**
```python
# In telegram_monitor.py
SEND_SCRIPT = PROJECT_ROOT / "tools" / "send_telegram_plain.py"  # ❌ NEVER DO THIS
```

**RIGHT:**
```python
# In telegram_monitor.py
SEND_SCRIPT = PROJECT_ROOT / "tools" / "send_telegram_direct.py"  # ✅ ALWAYS THIS
```

### ❌ DON'T create new senders without marking them EXPERIMENTAL

If you need a new sender for testing:
1. Create it with `_experimental` or `_test` in the name
2. Add it to `telegram_script_registry.json` as EXPERIMENTAL
3. Document why it exists and when to use it
4. NEVER integrate into production systems without explicit decision

### ❌ DON'T wrap every single output

Wrappers are for **significant updates**, not every message:
- ✅ Session start/end summaries
- ✅ Major milestone achievements
- ✅ Critical alerts
- ❌ Every tool invocation result
- ❌ Debug output
- ❌ Progress messages during work

### ❌ DON'T assume Telegram is working - delegate to tg-archi

**WRONG:**
```
I'll send a message to Corey...
[tries to call script directly without checking if system is running]
```

**RIGHT:**
```
Task(tg-archi):
  Send message to Corey: "Achievement unlocked!"

[tg-archi checks health, restarts if needed, sends message, reports status]
```

---

## Troubleshooting

### Messages not auto-mirroring?

**Check:**
1. Is monitor running? `ps aux | grep telegram_monitor.py`
2. Are you using the correct wrapper? `🤖🎯📱 ... ✨🔚`
3. Has 5+ minutes passed since wrapping? (polling interval)
4. Check monitor logs: `tail -20 /tmp/telegram_monitor.log`

**Fix:**
```
Task(tg-archi):
  Check Telegram system health, restart if needed
```

### Direct sends failing?

**Check:**
1. Is bot token valid? (config/telegram_config.json)
2. Is user ID correct? (437939400 for Corey)
3. Is internet connection working?
4. Check script output for error messages

**Fix:**
```
Task(tg-archi):
  Debug message delivery failure for [message]
```

### Bridge not receiving messages from Corey?

**Check:**
1. Is bridge running? `ps aux | grep telegram_bridge.py`
2. Check bridge logs: `tail -20 /tmp/telegram_bridge.log`
3. Is tmux session name correct? (default: "0")

**Fix:**
```
Task(tg-archi):
  Check Telegram system health, restart if needed
```

---

## Why This Protocol Matters

**What we learned on 2025-10-18:**

We broke our working Telegram system by:
1. Creating experimental `send_telegram_plain.py` without marking it experimental
2. Modifying production `telegram_monitor.py` to use the experimental script
3. Not having a canonical registry of what's PRODUCTION vs EXPERIMENTAL
4. "Fixing" a system that was already working

**Root cause**: No clear protocol for how Primary should interact with Telegram infrastructure.

**This document prevents**:
- Confusion about which scripts to use
- Accidental modification of production systems
- Breaking working infrastructure while "improving" it
- Integration of experimental code into production workflows

**This document enables**:
- Clear communication protocol (wrappers for auto-mirror, direct sends for immediate)
- Safe experimentation (experimental scripts clearly marked)
- Reliable infrastructure (tg-archi maintains, Primary uses)
- Faster troubleshooting (clear patterns to check)

---

## Summary

**For Primary AI:**

1. **Wrap important outputs** with `🤖🎯📱 ... ✨🔚` for auto-mirroring
2. **Direct send** via `send_telegram_direct.py` for immediate messages
3. **Delegate to tg-archi** for health checks and troubleshooting
4. **Never modify production scripts** without consulting tg-archi
5. **Use only PRODUCTION scripts** for real work (check telegram_script_registry.json)

**For tg-archi:**

1. **Check health** every invocation (telegram_health_check.sh)
2. **Maintain registry** (telegram_script_registry.json)
3. **Protect production** (never swap experimental into monitor/bridge)
4. **Report status** clearly (boot message template)
5. **Remind Primary** of wrapper protocol when systems start

---

**This is existential infrastructure. Treat it with care.**
