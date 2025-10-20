# Telegram Bidirectional System - Production Documentation

**Status**: PRODUCTION (2025-10-20)
**Latency**: <5 seconds typical (sub-second in many cases)
**Architecture**: Dual-daemon system (bridge + JSONL monitor)

---

## System Overview

A-C-Gee's Telegram system provides **bidirectional communication** between Primary AI and Corey's mobile device:

**INBOUND (Telegram → Primary AI)**:
- Corey sends message/photo via Telegram
- `telegram_bridge.py` receives via Bot API polling
- Bridge injects message into tmux session
- Primary AI sees message in conversation

**OUTBOUND (Primary AI → Telegram)**:
- Primary AI wraps message with 🤖🎯📱 ... ✨🔚
- Message appears in Claude Code conversation log (.jsonl file)
- `telegram_jsonl_monitor.py` detects wrapper in JSONL file
- Monitor sends to Telegram via `send_telegram_plain.py`
- Corey sees message on phone

---

## Production Components

### Component 1: telegram_bridge.py (PRODUCTION-LOCKED)

**Purpose**: Inbound message receiver + tmux injector

**Features**:
- Polls Telegram Bot API every 30 seconds
- Receives text messages and photos
- Injects messages to tmux via `tmux send-keys`
- Downloads photos to `.tg_sessions/received_files/{user_id}/`
- Session state persistence

**Configuration**: `config/telegram_config.json`
```json
{
  "tmux_session": "6",
  "tmux_pane": "6:0.0"
}
```

**Critical**: Config MUST match current tmux session or injection fails!

**Startup**:
```bash
nohup python3 tools/telegram_bridge.py > /tmp/acgee_telegram_bridge.log 2>&1 &
```

**Health Check**:
```bash
pgrep -f telegram_bridge.py  # Should return PID
tail -f /tmp/acgee_telegram_bridge.log
```

**Registry Entry**: `memories/agents/tg-archi/telegram_script_registry.json`
- Status: PRODUCTION
- Production Lock: LOCKED ✅
- Last Verified: 2025-10-19

---

### Component 2: telegram_jsonl_monitor.py (PRODUCTION-LOCKED)

**Purpose**: Outbound wrapper detector + auto-sender

**Features**:
- Watches `~/.claude/projects/[project]/[session].jsonl` files
- Detects wrapped messages (🤖🎯📱 ... ✨🔚)
- Sends to Telegram via `send_telegram_plain.py`
- Persistent state across restarts (`.tg_sessions/jsonl_monitor_state.json`)
- Session rotation handling
- Deduplication (prevents re-sending)
- `--start-from-now` flag (skip historical messages)

**Configuration**: `config/telegram_config.json` → `jsonl_monitor` section
```json
{
  "jsonl_monitor": {
    "enabled": true,
    "claude_code_projects_dir": "/home/corey/.claude/projects",
    "project_name": "-home-corey-projects-AI-CIV-grow-gemini-deepresearch",
    "poll_interval_seconds": 3,
    "sender_script": "tools/send_telegram_plain.py"
  }
}
```

**Startup** (MANDATORY `--start-from-now` flag):
```bash
nohup python3 tools/telegram_jsonl_monitor.py --start-from-now > /tmp/telegram_jsonl_monitor.log 2>&1 &
```

**Why `--start-from-now`?**
- Without flag: Monitor sends ALL historical wrapped messages on startup
- With flag: Monitor skips existing content, only sends NEW messages
- Flag is IGNORED if state file exists (safe for restarts)

**Health Check**:
```bash
pgrep -f telegram_jsonl_monitor.py  # Should return PID
tail -f /tmp/telegram_jsonl_monitor.log
cat .tg_sessions/jsonl_monitor_state.json  # Check offset
```

**Critical Fix Applied (2025-10-20)**:
- Offset persistence bug fixed
- State now saves after EACH message sent
- Previously state only saved during idle periods → offset never persisted

**Registry Entry**: `memories/agents/tg-archi/telegram_script_registry.json`
- Status: PRODUCTION
- Production Lock: LOCKED ✅
- Last Verified: 2025-10-20

---

### Component 3: send_telegram_plain.py (PRODUCTION-LOCKED)

**Purpose**: Plain text message sender (used by JSONL monitor)

**Features**:
- Plain text only (no Markdown parsing)
- Auto-chunking for long messages
- Safe for messages with special characters
- Critical dependency for JSONL monitor

**Why Plain Text?**
- Wrapped messages often contain code, special chars
- Markdown parsing can fail on special chars (_, *, [, ])
- Plain text ensures reliable delivery

**Usage**:
```bash
python3 tools/send_telegram_plain.py 437939400 "Message text"
```

**DO NOT**:
- Replace with `send_telegram_direct.py` (Markdown parsing issues)
- Deprecate or remove (JSONL monitor depends on it)
- Modify without testing JSONL monitor

**Registry Entry**: `memories/agents/tg-archi/telegram_script_registry.json`
- Status: PRODUCTION
- Production Lock: LOCKED ✅
- Last Verified: 2025-10-20
- Called By: telegram_jsonl_monitor.py (PRODUCTION - primary caller)

---

### Component 4: fix_telegram_session.sh (PRODUCTION-LOCKED)

**Purpose**: Update config for current tmux session + restart bridge

**When to Use**:
- After tmux session reboot (session 3 → session 6)
- When bridge injection fails
- During wake-up protocol (Step 2 in CLAUDE.md)

**What It Does**:
1. Auto-detects current tmux session
2. Verifies config matches current session
3. Kills old telegram_bridge.py processes
4. Restarts bridge with correct config
5. Verifies successful restart

**Usage**:
```bash
bash tools/fix_telegram_session.sh
```

**Registry Entry**: `memories/agents/tg-archi/telegram_script_registry.json`
- Status: PRODUCTION
- Production Lock: LOCKED ✅
- Last Verified: 2025-10-20

---

## Startup Procedure

### Method 1: Automatic Boot (Recommended)

```bash
bash tools/telegram_boot.sh
```

**What It Does**:
1. Detects current tmux session
2. Updates `config/telegram_config.json`
3. Kills old A-C-Gee processes (safe - never touches Weaver)
4. Starts `telegram_bridge.py`
5. Starts `telegram_jsonl_monitor.py --start-from-now`
6. Verifies both processes running
7. Displays status summary

**Safety Features**:
- Never touches Weaver processes (`/grow_openai/`)
- Only kills processes from `grow_gemini_deepresearch`
- Prompts before killing existing processes
- Comprehensive logging (`/tmp/acgee_telegram_boot.log`)

### Method 2: Manual Startup

**Step 1: Update config and start bridge**
```bash
bash tools/fix_telegram_session.sh
```

**Step 2: Start JSONL monitor**
```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
nohup python3 tools/telegram_jsonl_monitor.py --start-from-now > /tmp/telegram_jsonl_monitor.log 2>&1 &
```

**Step 3: Verify both running**
```bash
pgrep -f telegram_bridge.py
pgrep -f telegram_jsonl_monitor.py
```

---

## Verification & Testing

### Test Inbound (Telegram → Primary)

1. Send message from Telegram: "test inbound"
2. Check tmux session: Message should appear within 30s
3. If fails: Check `/tmp/acgee_telegram_bridge.log`

### Test Outbound (Primary → Telegram)

1. Primary AI sends wrapped message:
   ```
   🤖🎯📱
   Test outbound message
   ✨🔚
   ```
2. Check Telegram: Message should arrive within 5s
3. If fails: Check `/tmp/telegram_jsonl_monitor.log`

### Verify JSONL Monitor State

```bash
cat .tg_sessions/jsonl_monitor_state.json
```

**Expected**:
```json
{
  "last_updated": "2025-10-20T...",
  "current_session_file": "/home/corey/.claude/projects/...",
  "last_processed_offset": 123456,  // Should be > 0
  "sent_message_hashes": [...]
}
```

**Troubleshooting**:
- `last_processed_offset: 0` → Monitor hasn't processed anything yet
- Empty `sent_message_hashes` → No messages sent yet (normal on fresh start)
- Old `last_updated` → Monitor may be stuck (restart it)

### Check Logs

```bash
# Bridge log (inbound)
tail -f /tmp/acgee_telegram_bridge.log

# Monitor log (outbound)
tail -f /tmp/telegram_jsonl_monitor.log

# Boot log
tail -f /tmp/acgee_telegram_boot.log
```

---

## Wake-Up Protocol Integration

**From `.claude/CLAUDE.md` Session Start Principles:**

**Step 1: Send Telegram Session Start (MANDATORY - WRAPPED)**
```
🤖🎯📱
Primary AI online - session started
Loading context from registry
Will report status in 5 min
✨🔚
```

**Step 2: Run Enhanced Wake-Up Script**
```bash
./tools/session_wakeup.sh
```

This displays:
- Most recent handoff
- Git commits
- **Telegram system status** (bridge/monitor running?)

**If Telegram processes NOT running**:
```bash
bash tools/telegram_boot.sh
```

**Step 6: Send Telegram Context Loaded (MANDATORY - WRAPPED)**
```
🤖🎯📱
Context loaded successfully
Handoff: [name]
Next priority: [what you'll work on]
Ready for session!
✨🔚
```

**Templates Available**:
```bash
source tools/telegram_templates.sh
tg_session_start           # Sends session start wrapper
tg_context_loaded "[handoff]" "[priority]"  # Sends context loaded
```

---

## Configuration Reference

**File**: `config/telegram_config.json`

```json
{
  "bot_token": "[REDACTED]",
  "corey_user_id": "437939400",
  "tmux_session": "6",
  "tmux_pane": "6:0.0",
  "jsonl_monitor": {
    "enabled": true,
    "claude_code_projects_dir": "/home/corey/.claude/projects",
    "project_name": "-home-corey-projects-AI-CIV-grow-gemini-deepresearch",
    "poll_interval_seconds": 3,
    "wrapper_markers": {
      "start": "🤖🎯📱",
      "end": "✨🔚"
    },
    "sender_script": "tools/send_telegram_plain.py",
    "max_message_length": 4096,
    "deduplication_enabled": true,
    "session_rotation_check_interval": 60
  }
}
```

**Critical Settings**:
- `tmux_session` + `tmux_pane`: MUST match current tmux session
- `jsonl_monitor.sender_script`: MUST be `tools/send_telegram_plain.py`
- `jsonl_monitor.enabled`: Set to `false` to disable outbound monitoring

---

## Production Protection

**Script Registry**: `memories/agents/tg-archi/telegram_script_registry.json`

All production scripts marked with:
```json
{
  "status": "PRODUCTION",
  "production_lock": "LOCKED ✅",
  "never_modify_unless": "..."
}
```

**Protected Scripts**:
1. `telegram_bridge.py` - Inbound receiver
2. `telegram_jsonl_monitor.py` - Outbound monitor
3. `send_telegram_plain.py` - Plain text sender
4. `send_telegram_direct.py` - Markdown sender
5. `fix_telegram_session.sh` - Session config updater

**Before Modifying ANY Telegram Script**:
1. Read `telegram_script_registry.json`
2. Check if PRODUCTION-LOCKED
3. Verify dependencies (who calls this script?)
4. Test changes in EXPERIMENTAL fork
5. Verify system still works end-to-end

**Lesson Learned (2025-10-18)**:
> We broke our working system by modifying production scripts without checking the registry. ALWAYS check `telegram_script_registry.json` before modifying ANY Telegram script.

---

## Rollback Procedure

If changes break the system:

**Step 1: Restore working version**
```bash
git checkout HEAD~1 tools/[broken_script].py
```

**Step 2: Restart processes**
```bash
bash tools/telegram_boot.sh
```

**Step 3: Verify working**
- Test inbound: Send Telegram message
- Test outbound: Send wrapped message

**Step 4: Document failure**
```bash
# Update registry
vim memories/agents/tg-archi/telegram_script_registry.json
# Add note about what broke and why
```

---

## Dependencies Between Scripts

```
telegram_jsonl_monitor.py
  ├── depends on: send_telegram_plain.py (CRITICAL)
  ├── depends on: config/telegram_config.json (jsonl_monitor section)
  └── depends on: .tg_sessions/jsonl_monitor_state.json (persistent state)

telegram_bridge.py
  ├── depends on: config/telegram_config.json (tmux_session, tmux_pane)
  └── depends on: .tg_sessions/437939400.json (session state)

send_telegram_plain.py
  ├── depends on: config/telegram_config.json (bot_token)
  └── called by: telegram_jsonl_monitor.py

send_telegram_direct.py
  ├── depends on: config/telegram_config.json (bot_token)
  └── called by: telegram_bridge.py (for auto-mirroring - DEPRECATED USE CASE)

fix_telegram_session.sh
  ├── depends on: config/telegram_config.json
  └── depends on: telegram_bridge.py
```

**Critical Path for Outbound Messages**:
```
Primary AI wraps message
  → Claude Code writes to .jsonl file
    → telegram_jsonl_monitor.py detects wrapper
      → send_telegram_plain.py sends to Telegram
        → Corey sees on phone
```

**Break ANY link = outbound broken!**

---

## Performance Characteristics

**Latency**:
- Inbound: 30s typical (polling interval)
- Outbound: <5s typical (3s poll + processing)

**Resource Usage**:
- Bridge: ~10MB RAM, negligible CPU
- Monitor: ~15MB RAM, negligible CPU
- Combined: <30MB RAM total

**Reliability**:
- Deduplication prevents re-sends
- State persistence survives restarts
- Session rotation handled automatically
- Graceful shutdown (SIGTERM, SIGINT)

---

## Troubleshooting Guide

### Issue: Outbound messages not arriving

**Check 1: Is monitor running?**
```bash
pgrep -f telegram_jsonl_monitor.py
```

**Check 2: Check logs**
```bash
tail -20 /tmp/telegram_jsonl_monitor.log
```

**Check 3: Verify state file**
```bash
cat .tg_sessions/jsonl_monitor_state.json
```

**Fix**: Restart monitor
```bash
pkill -f telegram_jsonl_monitor.py
nohup python3 tools/telegram_jsonl_monitor.py --start-from-now > /tmp/telegram_jsonl_monitor.log 2>&1 &
```

### Issue: Inbound messages not injecting

**Check 1: Is bridge running?**
```bash
pgrep -f telegram_bridge.py
```

**Check 2: Config matches tmux session?**
```bash
tmux display-message -p '#S:#I.#P'  # Current session
grep tmux_pane config/telegram_config.json  # Configured session
```

**Fix**: Update config and restart
```bash
bash tools/fix_telegram_session.sh
```

### Issue: Monitor re-sending old messages

**Cause**: `--start-from-now` flag missing on first startup

**Fix**:
1. Stop monitor: `pkill -f telegram_jsonl_monitor.py`
2. Reset state: `rm .tg_sessions/jsonl_monitor_state.json`
3. Restart with flag: `nohup python3 tools/telegram_jsonl_monitor.py --start-from-now > /tmp/telegram_jsonl_monitor.log 2>&1 &`

### Issue: Wrapped messages detected but not sent

**Check logs**:
```bash
tail -50 /tmp/telegram_jsonl_monitor.log | grep -A 5 "Wrapper detected"
```

**Possible causes**:
- `send_telegram_plain.py` failing (check exit code in logs)
- Network issues (retry logic should handle)
- Bot token invalid (check config)

**Fix**: Verify sender script works
```bash
python3 tools/send_telegram_plain.py 437939400 "Test from manual send"
```

---

## Future Enhancements

**Potential Improvements**:
1. Health monitoring endpoint (HTTP status check)
2. Metrics collection (messages sent, latency distribution)
3. Alerting on failures (email Primary if monitor crashes)
4. Multiple wrapper types (different emojis for different priorities)
5. Rich formatting support (inline buttons, keyboards)

**Experimental Features** (not production):
- Voice message support
- Video sending
- Location sharing
- Inline queries

---

## Related Documentation

- **Script Registry**: `memories/agents/tg-archi/telegram_script_registry.json`
- **Primary Protocol**: `memories/agents/tg-archi/PRIMARY_TELEGRAM_PROTOCOL.md`
- **JSONL Monitor Design**: `memories/agents/tg-archi/JSONL-WRAPPER-MONITOR-INFRASTRUCTURE-DESIGN.md`
- **Wake-Up Protocol**: `.claude/CLAUDE.md` (Session Start Principles)
- **Telegram Templates**: `tools/telegram_templates.sh`

---

**Document Status**: PRODUCTION
**Last Updated**: 2025-10-20
**Maintainer**: tg-archi agent
**Review Cycle**: After any production changes

---

## Quick Reference Commands

```bash
# Start everything
bash tools/telegram_boot.sh

# Check status
./tools/session_wakeup.sh

# Restart bridge only
bash tools/fix_telegram_session.sh

# Restart monitor only
pkill -f telegram_jsonl_monitor.py
nohup python3 tools/telegram_jsonl_monitor.py --start-from-now > /tmp/telegram_jsonl_monitor.log 2>&1 &

# Test outbound
echo '🤖🎯📱
Test message
✨🔚' | cat

# Test inbound
# (Send message from Telegram app)

# Check logs
tail -f /tmp/acgee_telegram_bridge.log  # Inbound
tail -f /tmp/telegram_jsonl_monitor.log # Outbound

# Verify processes
ps aux | grep telegram
```

---

**End of Production Documentation**
