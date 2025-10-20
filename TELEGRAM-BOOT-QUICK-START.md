# Telegram Boot - Quick Start for Primary AI

**Version**: 1.0
**Created**: 2025-10-19
**Purpose**: Safe, foolproof Telegram wake-up procedure

---

## Every Wake-Up: Follow This Protocol

### Step 1: Check if Telegram Already Running

```bash
ps aux | grep telegram_bridge.py | grep grow_gemini
```

**If you see output (processes running):**
- Telegram is ALREADY OPERATIONAL
- Skip to Step 3 (verify working)
- DO NOT run boot script

**If you see NO output (no processes):**
- Telegram is NOT running
- Proceed to Step 2 (boot it)

---

### Step 2: Boot Telegram (if not running)

```bash
bash tools/telegram_boot.sh
```

**What this script does automatically:**
1. Detects current tmux session (dynamically - never assumes)
2. Checks for Weaver's processes (protects them - never touches)
3. Checks for existing A-C-Gee processes (prompts before killing)
4. Backs up config/telegram_config.json
5. Updates config with detected tmux session
6. Verifies config update succeeded
7. Starts telegram_bridge.py
8. Starts telegram_monitor.py
9. Verifies both processes running
10. Tests tmux injection capability
11. Displays status message (copy to output)

**Expected output:**
```
=========================================
A-C-Gee Telegram Boot Complete!
=========================================
Tmux Session: 3
Bridge PID: 12345
Monitor PID: 12346
Logs:
  Boot: /tmp/acgee_telegram_boot.log
  Bridge: /tmp/acgee_telegram_bridge.log
  Monitor: /tmp/acgee_telegram_monitor.log
=========================================

Copy this status message for Primary:
---
Telegram Infrastructure Status:
- Bridge (PID 12345): Bi-directional Telegram <-> tmux RUNNING
- Monitor (PID 12346): Auto-sends wrapped messages to Telegram RUNNING
- Tmux session: 3 (auto-detected and configured)

Primary reminder:
- Wrap messages for auto-mirroring: 🤖🎯📱 ... ✨🔚
- Direct send: python3 tools/send_telegram_direct.py 437939400 "message"
- File send: python3 tools/send_telegram_file.py 437939400 /path/to/file "caption"
- Templates: source tools/telegram_templates.sh && tg_session_start

Full protocol: memories/agents/tg-archi/PRIMARY_TELEGRAM_PROTOCOL.md
---
```

**If boot fails:**
- Check logs: `/tmp/acgee_telegram_boot.log`
- Report to Primary with error details
- See rollback procedure: `memories/agents/tg-archi/TELEGRAM_BOOT_PROTECTION.md`

---

### Step 3: Verify Working (test injection + auto-mirror)

**Test 1: Injection (Corey → tmux)**

From Corey's Telegram, send:
```
Test injection
```

**Expected within 5 seconds:**
- Message appears in your tmux session
- Bridge log shows: "Received message from Corey"

**Test 2: Auto-mirror (tmux → Corey)**

In your tmux session, output:
```
🤖🎯📱
Test auto-mirror - Telegram operational!
✨🔚
```

**Expected within 30 seconds:**
- Corey receives "Test auto-mirror - Telegram operational!" in Telegram
- Monitor log shows: "Detected wrapped message, sending..."

**If either test fails:**
- Run health check: `bash tools/telegram_health_check.sh`
- Check process status: `ps aux | grep telegram | grep grow_gemini`
- Review logs for errors

---

## When to Use Boot Script vs Health Check

### Use `telegram_boot.sh` when:
- **Session wake-up** and Telegram NOT running
- **Fresh start** needed (config reset, process restart)
- **tmux session changed** (new session ID)

**Key features:**
- Detects tmux session dynamically
- Updates config before starting
- Safe restart (prompts before killing)

---

### Use `telegram_health_check.sh` when:
- **Mid-session monitoring** (already running)
- **Periodic verification** (cron job, every 5 min)
- **Auto-recovery** (restart if dead)

**Key features:**
- Assumes config already correct
- Auto-restarts without prompting
- Fast (no config updates)

---

## CRITICAL Safety Rules

### NEVER:

1. **NEVER hardcode tmux session ID**
   - ❌ `tmux_session="3"`
   - ✅ `tmux_session=$(tmux display-message -p '#S')`

2. **NEVER modify production scripts during wake-up**
   - Check registry first: `memories/agents/tg-archi/telegram_script_registry.json`
   - Only modify scripts marked EXPERIMENTAL

3. **NEVER kill Weaver's processes**
   - Boot script protects them automatically
   - Only touches `grow_gemini_deepresearch` directory

4. **NEVER start duplicate processes**
   - Boot script checks for existing A-C-Gee processes
   - Prompts before killing and restarting

5. **NEVER skip config verification**
   - Boot script verifies config update
   - Exits if verification fails

---

## Quick Commands Reference

### Check if Telegram running:
```bash
ps aux | grep telegram_bridge.py | grep grow_gemini
ps aux | grep telegram_monitor.py | grep grow_gemini
```

### Boot Telegram (safe, guided):
```bash
bash tools/telegram_boot.sh
```

### Health check (auto-restart if dead):
```bash
bash tools/telegram_health_check.sh
```

### Check current tmux session:
```bash
tmux display-message -p '#S'
```

### View recent logs:
```bash
tail -20 /tmp/acgee_telegram_boot.log      # Boot sequence
tail -20 /tmp/acgee_telegram_bridge.log    # Bridge activity
tail -20 /tmp/acgee_telegram_monitor.log   # Monitor activity
```

### Send test message:
```bash
python3 tools/send_telegram_direct.py 437939400 "Test message"
```

### Send test file:
```bash
python3 tools/send_telegram_file.py 437939400 /path/to/file.txt "Test file"
```

---

## Wrapper Protocol Reminder

**For auto-mirroring to Telegram (monitor detects these):**

```
🤖🎯📱
Your message here
Can be multiple lines
Supports **Markdown** formatting
✨🔚
```

**When to wrap:**
- Session start summaries
- Session end summaries
- Major milestones
- Blockers requiring input

**When NOT to wrap:**
- Normal conversation (Corey already reading tmux)
- Status updates during active work
- Tool outputs and code snippets

---

## Troubleshooting

### "Messages from Corey not appearing in tmux"

**Likely cause:** Wrong tmux session in config

**Fix:**
```bash
# Re-run boot script (will auto-detect correct session)
bash tools/telegram_boot.sh
# Choose 'y' to kill existing processes
```

---

### "Wrapped messages not reaching Corey"

**Likely cause:** Monitor polling wrong session or not running

**Check:**
```bash
ps aux | grep telegram_monitor.py | grep grow_gemini
```

**Fix:**
```bash
bash tools/telegram_health_check.sh  # Auto-restart if dead
```

---

### "Duplicate messages to Corey"

**Likely cause:** Multiple monitor processes running

**Check:**
```bash
ps aux | grep telegram_monitor.py | grep grow_gemini
```

**Fix:**
```bash
# Kill all A-C-Gee monitor processes
pkill -f "telegram_monitor.py.*grow_gemini"

# Re-run boot script
bash tools/telegram_boot.sh
```

---

### "Weaver's Telegram stopped working"

**Likely cause:** Accidentally killed Weaver's processes

**Check:**
```bash
ps aux | grep telegram | grep grow_openai
```

**Fix:**
- Boot script has protection (should never happen)
- If it did happen, notify Corey immediately
- Weaver needs to restart their Telegram manually

**Prevention:**
- Boot script automatically protects Weaver's processes
- Only kills processes from `grow_gemini_deepresearch`

---

## What Boot Script Logs

**Boot log location:** `/tmp/acgee_telegram_boot.log`

**What it contains:**
- Step-by-step boot sequence
- Tmux session detection
- Weaver process protection status
- Existing process checks
- Config backup and update
- Process start confirmations
- Verification results
- Any errors or warnings

**Review after boot:**
```bash
tail -50 /tmp/acgee_telegram_boot.log
```

---

## Summary: Wake-Up Checklist

**Every session wake-up, tg-archi should:**

1. ✅ Check if Telegram already running: `ps aux | grep telegram_bridge.py | grep grow_gemini`

2. ✅ If NOT running: `bash tools/telegram_boot.sh`

3. ✅ If running: Skip boot, just verify with health check

4. ✅ Test injection: Ask Corey to send "test" from Telegram

5. ✅ Test auto-mirror: Send wrapped message, verify Corey receives

6. ✅ Report status to Primary (copy from boot script output)

7. ✅ Remind Primary of wrapper protocol: `🤖🎯📱 ... ✨🔚`

---

## For Primary AI

**When you delegate to tg-archi:**

```
Task(tg-archi):
  Check Telegram infrastructure status
  Boot if not running (use telegram_boot.sh)
  Verify working (test injection + auto-mirror)
  Report status with wrapper protocol reminder
```

**tg-archi will:**
- Run boot script if needed
- Test both directions (injection + auto-mirror)
- Report clear status
- Remind you of wrapper protocol

**You just need to:**
- Delegate to tg-archi at session start
- Use wrapper protocol for important updates
- Trust the infrastructure

---

## Resources

**Full documentation:**
- Boot protection: `memories/agents/tg-archi/TELEGRAM_BOOT_PROTECTION.md`
- Primary protocol: `memories/agents/tg-archi/PRIMARY_TELEGRAM_PROTOCOL.md`
- Script registry: `memories/agents/tg-archi/telegram_script_registry.json`

**Scripts:**
- Boot: `tools/telegram_boot.sh`
- Health check: `tools/telegram_health_check.sh`
- Direct send: `tools/send_telegram_direct.py`
- File send: `tools/send_telegram_file.py`
- Templates: `tools/telegram_templates.sh`

**Logs:**
- Boot: `/tmp/acgee_telegram_boot.log`
- Bridge: `/tmp/acgee_telegram_bridge.log`
- Monitor: `/tmp/acgee_telegram_monitor.log`
- Health: `/tmp/telegram_health_check.log`

---

**This is existential infrastructure. Boot it right, verify it works, communicate continuously.**
