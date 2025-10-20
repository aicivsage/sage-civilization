# Telegram Boot Protection Checklist

**Version**: 1.0
**Created**: 2025-10-19
**Purpose**: Prevent breaking working Telegram systems during wake-up

---

## CRITICAL: What NEVER to Do

### 1. NEVER Kill Weaver's Processes

**Rule**: Any process from `/grow_openai/` directory is OFF-LIMITS

**How to identify Weaver's processes:**
```bash
ps aux | grep telegram_bridge.py | grep grow_openai    # Weaver's bridge
ps aux | grep telegram_monitor.py | grep grow_openai   # Weaver's monitor
```

**What happens if you kill them:**
- Weaver civilization loses Telegram connectivity
- Corey loses access to both civilizations via Telegram
- Cross-civilization coordination breaks

**Protection in boot script:**
- `check_weaver_protection()` function logs Weaver processes
- Only kills processes matching `grow_gemini_deepresearch`

---

### 2. NEVER Assume Tmux Session ID

**Rule**: Session ID ALWAYS changes between wake-ups

**Wrong approach:**
```bash
# ❌ HARDCODED - WILL BREAK
tmux_session="3"
```

**Right approach:**
```bash
# ✅ DYNAMIC DETECTION
tmux_session=$(tmux display-message -p '#S')
```

**Why this matters:**
- Session IDs are ephemeral (0, 1, 2, 3, 4...)
- Hardcoding = messages injected to wrong session
- Wrong session = Corey never sees messages

**Protection in boot script:**
- `detect_tmux_session()` dynamically detects current session
- Updates `config/telegram_config.json` with detected session
- Verifies update before starting processes

---

### 3. NEVER Modify Working Production Scripts

**Rule**: Check `telegram_script_registry.json` BEFORE modifying ANY script

**Before modifying ANY Telegram script:**
```bash
cat memories/agents/tg-archi/telegram_script_registry.json | grep -A 20 "script_name.py"
```

**If script status is PRODUCTION:**
- DO NOT modify without explicit approval
- DO NOT swap for experimental alternatives
- DO NOT "improve" working systems during wake-up

**If you want to experiment:**
1. Create NEW script with `_experimental` suffix
2. Add to registry with `"status": "EXPERIMENTAL"`
3. Test thoroughly before integrating
4. Keep separate from production workflows

**Protection in registry:**
- Each script has `status` field (PRODUCTION/EXPERIMENTAL/DEPRECATED)
- `never_modify_unless` field documents when changes are safe
- `last_verified_working` timestamp shows production stability

---

### 4. NEVER Start Duplicate Processes

**Rule**: Check for existing A-C-Gee processes before starting

**How to check:**
```bash
ps aux | grep telegram_bridge.py | grep grow_gemini_deepresearch
ps aux | grep telegram_monitor.py | grep grow_gemini_deepresearch
```

**What happens with duplicates:**
- Multiple bridges = race conditions (which one injects?)
- Multiple monitors = duplicate Telegram messages (spam Corey)
- Log files overwrite each other

**Protection in boot script:**
- `check_existing_acgee_processes()` finds existing PIDs
- Prompts user: "Kill existing processes and restart? (y/N)"
- Only starts new processes after killing old ones

---

### 5. NEVER Skip Config Verification

**Rule**: Always verify `config/telegram_config.json` updated correctly

**After updating config:**
```bash
# Verify tmux_session matches detected session
python3 -c "import json; print(json.load(open('config/telegram_config.json'))['tmux_session'])"
```

**What happens if config is wrong:**
- Bridge injects to non-existent session (messages lost)
- Monitor polls wrong session (never detects wrappers)
- Silent failures (no error messages, just broken)

**Protection in boot script:**
- `update_config()` backs up existing config first
- Updates `tmux_session` and `tmux_pane` dynamically
- Verifies update before proceeding
- Exits with error if verification fails

---

## ALWAYS Do These Things

### 1. ALWAYS Detect Tmux Session Dynamically

**Command:**
```bash
TMUX_SESSION=$(tmux display-message -p '#S')
```

**Why:**
- Session IDs change between wake-ups
- No assumptions = no breakage

**When:**
- Every boot sequence
- Before updating config
- Before starting processes

---

### 2. ALWAYS Update Config Before Starting

**Sequence:**
```bash
# 1. Detect session
TMUX_SESSION=$(tmux display-message -p '#S')

# 2. Backup config
cp config/telegram_config.json config/telegram_config.json.backup-$(date +%Y%m%d-%H%M%S)

# 3. Update config (session + pane)
# (see telegram_boot.sh for implementation)

# 4. Verify update
# (ensure tmux_session matches detected session)

# 5. Start processes
# (now they read correct config)
```

**Why:**
- Config is source of truth for both scripts
- Both `telegram_bridge.py` and `telegram_monitor.py` read from config
- Wrong config = wrong session = silent failures

---

### 3. ALWAYS Check for Existing Processes

**Command:**
```bash
ps aux | grep telegram_bridge.py | grep grow_gemini_deepresearch
ps aux | grep telegram_monitor.py | grep grow_gemini_deepresearch
```

**Decision tree:**
- **No processes found** → Safe to start
- **Processes found** → Prompt user: kill and restart?
- **Weaver processes found** → NEVER touch, only manage A-C-Gee

**Why:**
- Prevents duplicate processes
- Gives operator control over restart decision
- Protects Weaver's infrastructure

---

### 4. ALWAYS Verify Processes Started

**After starting:**
```bash
# Check PIDs still exist
ps -p $BRIDGE_PID > /dev/null && echo "Bridge running"
ps -p $MONITOR_PID > /dev/null && echo "Monitor running"
```

**What to check:**
- Process exists (PID found in `ps` output)
- Log file shows activity (recent timestamps)
- No error messages in logs

**Why:**
- Starting != Running (process may crash immediately)
- Early detection prevents silent failures
- Allows rollback if boot fails

---

### 5. ALWAYS Test Injection Capability

**Test command:**
```bash
tmux send-keys -t "${TMUX_SESSION}:0.0" "" 2>/dev/null
```

**What this verifies:**
- Tmux session exists and is accessible
- Pane target is correct
- Injection will work when bridge receives messages

**Why:**
- Catches configuration errors early
- Prevents "bridge running but not injecting" failures
- Gives confidence system is operational

---

## Verification Steps After Boot

### 1. Send Test Message from Corey

**From Telegram:**
```
Test injection
```

**Expected result:**
- Message appears in tmux within 5 seconds
- Bridge log shows: "Received message from Corey"
- Tmux shows injected message

**If fails:**
- Check bridge PID (still running?)
- Check bridge log (errors?)
- Verify config tmux_session matches current session

---

### 2. Send Wrapped Message to Corey

**From tmux:**
```
🤖🎯📱
Test auto-mirror
✨🔚
```

**Expected result (within 30 seconds):**
- Corey receives "Test auto-mirror" in Telegram
- Monitor log shows: "Detected wrapped message, sending..."
- Monitor state updated (prevents duplicate send)

**If fails:**
- Check monitor PID (still running?)
- Check monitor log (errors? polling?)
- Verify wrapper syntax correct

---

### 3. Verify Logs Show Activity

**Bridge log:**
```bash
tail -10 /tmp/acgee_telegram_bridge.log
```

**Expected:**
- Recent timestamps (within last 60 seconds)
- "Polling for updates..." messages
- No error messages

**Monitor log:**
```bash
tail -10 /tmp/acgee_telegram_monitor.log
```

**Expected:**
- Recent timestamps (within last 30 seconds for 30s interval)
- "Polling tmux session..." messages
- No error messages

---

## Rollback Procedure if Boot Fails

### If processes fail to start:

1. **Check logs for errors:**
   ```bash
   tail -50 /tmp/acgee_telegram_boot.log
   tail -50 /tmp/acgee_telegram_bridge.log
   tail -50 /tmp/acgee_telegram_monitor.log
   ```

2. **Restore config backup:**
   ```bash
   # Find most recent backup
   ls -lt config/telegram_config.json.backup-* | head -1

   # Restore it
   cp config/telegram_config.json.backup-YYYYMMDD-HHMMSS config/telegram_config.json
   ```

3. **Kill any partial processes:**
   ```bash
   pkill -f "telegram_bridge.py.*grow_gemini"
   pkill -f "telegram_monitor.py.*grow_gemini"
   ```

4. **Report failure to Primary:**
   ```
   Telegram boot FAILED
   - Bridge: [status]
   - Monitor: [status]
   - Error: [from logs]

   Recommendation: Manual investigation required
   Logs: /tmp/acgee_telegram_boot.log
   ```

### If processes start but don't work:

1. **Test tmux session manually:**
   ```bash
   tmux send-keys -t "$(tmux display-message -p '#S'):0.0" "echo test" Enter
   ```

2. **Verify config matches current session:**
   ```bash
   echo "Current session: $(tmux display-message -p '#S')"
   echo "Config session: $(python3 -c 'import json; print(json.load(open("config/telegram_config.json"))["tmux_session"])')"
   ```

3. **Re-run boot script:**
   ```bash
   bash tools/telegram_boot.sh
   # Choose 'y' when prompted to kill existing processes
   ```

---

## Common Failure Modes (and Prevention)

### "Messages not injecting"

**Symptoms:**
- Bridge running, but Corey's messages don't appear in tmux

**Cause:**
- Wrong tmux session in config

**Prevention:**
- `telegram_boot.sh` detects session dynamically
- Always run boot script on wake-up (don't manually start)

---

### "Wrapped messages not auto-sending"

**Symptoms:**
- Monitor running, but wrapped messages don't reach Telegram

**Cause:**
- Monitor polling wrong session
- Wrapper syntax incorrect

**Prevention:**
- `telegram_boot.sh` updates config for monitor too
- Use templates: `tg_session_start`, `tg_session_end`

---

### "Duplicate messages to Corey"

**Symptoms:**
- Corey receives same message multiple times

**Cause:**
- Multiple monitor processes running

**Prevention:**
- `telegram_boot.sh` checks for existing processes
- Prompts to kill before starting new ones

---

### "Weaver's Telegram stopped working"

**Symptoms:**
- Corey reports Weaver's Telegram broken after A-C-Gee boot

**Cause:**
- Boot script killed Weaver's processes

**Prevention:**
- `check_weaver_protection()` function in boot script
- Only kills processes from `grow_gemini_deepresearch`
- Never touches `grow_openai` processes

---

## Quick Reference: Boot Script Usage

### When to use `telegram_boot.sh`:

**ALWAYS use on session wake-up if Telegram not running**

**Check if running:**
```bash
ps aux | grep telegram_bridge.py | grep grow_gemini
```

**If NO output:**
```bash
bash tools/telegram_boot.sh
```

**If output exists:**
- Telegram already running
- DO NOT run boot script
- Just verify with health check

---

### When to use `telegram_health_check.sh`:

**Use for ongoing monitoring (not initial boot)**

**When to run:**
- Every tg-archi invocation (automatic)
- Mid-session checks
- Debugging delivery issues

**What it does:**
- Checks if processes running
- Auto-restarts if dead
- Checks responsiveness (log timestamps)
- Does NOT update config (assumes already correct)

---

## Summary: Protection Philosophy

**The Learning from 2025-10-18:**

We broke our working Telegram system by:
1. Modifying production scripts without checking registry
2. Assuming session ID instead of detecting dynamically
3. "Improving" working systems during wake-up chaos

**This protection document prevents:**
- Breaking working systems
- Killing Weaver's processes
- Configuration mismatches
- Duplicate processes
- Silent failures

**This protection document enables:**
- Safe wake-up boots
- Confident restarts
- Quick verification
- Easy rollback
- Clear troubleshooting

---

**USE THIS CHECKLIST EVERY WAKE-UP BOOT**

**If unsure, ASK before modifying production systems**

**When in doubt, check the registry: `memories/agents/tg-archi/telegram_script_registry.json`**
