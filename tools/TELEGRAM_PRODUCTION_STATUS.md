# Telegram Production Status Registry

**Last Updated:** 2025-10-19 (V3 deployed)
**Purpose:** Document which Telegram systems are production-locked and which are broken

---

## PRODUCTION-LOCKED SYSTEMS ✅

These files are WORKING and STABLE. **DO NOT MODIFY** without explicit approval and testing.

### 1. telegram_monitor_v3.py

**Status:** PRODUCTION-LOCKED ✅
**Path:** `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_monitor_v3.py`
**Purpose:** Auto-detects and sends wrapped messages from tmux to Telegram
**Last Verified:** 2025-10-19 (deployed and tested)

**What it does:**
- Polls tmux buffer every 30 seconds for wrapped messages
- Hash-based deduplication (content + timestamp)
- Auto-sends to Corey's Telegram within 30 seconds
- Position-independent (survives buffer wrap/scroll)
- Two-phase commit (zero duplicate loops)
- Graceful error handling (invalid timestamps, etc.)

**How to use:**
```bash
# Start monitor
bash tools/restart_telegram_monitor_v3.sh 30

# Check if running
ps aux | grep telegram_monitor_v3.py

# View logs
tail -f /tmp/acgee_telegram_monitor_v3.log

# Send wrapped message (auto-detected and forwarded)
source tools/telegram_templates.sh
send_tg_wrapped "Your message here"
```

**Wrapper format (REQUIRED timestamp):**
```
🤖🎯📱[TIMESTAMP:2025-10-19T16:42:00Z]
Your message content here
✨🔚
```

**How to verify it works:**
```bash
# Send test wrapped message
source tools/telegram_templates.sh
send_tg_wrapped "Test message - $(date)"

# Wait 30 seconds
sleep 35

# Check logs for "Sent message"
tail -20 /tmp/acgee_telegram_monitor_v3.log | grep "Sent message"

# Check Telegram - message should arrive
```

**Dependencies:**
- config/telegram_config.json (bot token, corey_user_id, tmux_session)
- tools/send_telegram_direct.py (message sender)
- tools/telegram_templates.sh (helper function send_tg_wrapped)

**State:**
- .tg_sessions/monitor_state_v3.json (sent hashes)
- .tg_sessions/acgee_monitor_v3.pid (process ID)

---

### 2. telegram_bridge.py

**Status:** PRODUCTION-LOCKED ✅
**Path:** `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_bridge.py`
**Purpose:** Receives Corey's Telegram messages and injects to tmux
**Last Verified:** 2025-10-19

**What it does:**
- Listens for messages from Corey's Telegram
- Injects messages to tmux pane (instant bidirectional communication)
- Runs as daemon in background

**How to use:**
```bash
# Start bridge (daemon mode)
nohup python3 tools/telegram_bridge.py > /tmp/telegram_bridge.log 2>&1 &

# Check if running
ps aux | grep telegram_bridge

# View logs
tail -f /tmp/telegram_bridge.log
```

**How to verify it works:**
- Send message from Corey's Telegram
- Message appears in tmux instantly
- Logs show "Injected to tmux"

**Dependencies:**
- config/telegram_config.json (bot token)
- .tg_sessions/437939400.json (session state)

---

### 2. send_telegram_direct.py

**Status:** PRODUCTION-LOCKED ✅  
**Path:** `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/send_telegram_direct.py`  
**Purpose:** Primary's canonical message sender with Markdown support  
**Last Verified:** 2025-10-19

**What it does:**
- Sends messages directly to Telegram via Bot API
- Supports Markdown formatting
- Auto-chunks long messages
- Used by telegram_bridge.py

**How to use:**
```bash
# Send plain message
python3 tools/send_telegram_direct.py 437939400 "Hello from Primary!"

# Send with Markdown
python3 tools/send_telegram_direct.py 437939400 "**Bold** and *italic* text"

# Send multi-line
python3 tools/send_telegram_direct.py 437939400 "Line 1
Line 2
Line 3"
```

**How to verify it works:**
```bash
# Send test message
python3 tools/send_telegram_direct.py 437939400 "Test message - $(date)"

# Check Telegram - message should arrive immediately
```

**Dependencies:**
- config/telegram_config.json (bot token)

---

## DEPRECATED SYSTEMS ⚠️

These files are DEPRECATED and should NOT be used. They have been replaced by V3.

### 1. telegram_monitor.py (V1)

**Status:** DEPRECATED ⚠️
**Path:** `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_monitor.py`
**Issue:** Hash-based deduplication had edge cases
**Last Status Check:** 2025-10-19
**Replaced by:** telegram_monitor_v3.py

**Why deprecated:**
- Hash collisions possible (no timestamp in hash)
- No retention cleanup (unbounded state growth)
- No graceful error handling

**Use instead:** telegram_monitor_v3.py

---

### 2. telegram_monitor_v2.py

**Status:** DEPRECATED ⚠️
**Path:** `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_monitor_v2.py`
**Issue:** Watermark-based tracking fails on buffer scroll
**Last Status Check:** 2025-10-19
**Replaced by:** telegram_monitor_v3.py

**Why deprecated:**
- Position-based watermark breaks on buffer wrap/scroll/shrink
- Complex retry queue and circuit breaker (650 LOC)
- Buffer shrink detection didn't trigger reliably

**Use instead:** telegram_monitor_v3.py

---

### 3. telegram_monitor_v2.py deployment files

**Status:** DEPRECATED ⚠️
**Files:**
- tools/restart_telegram_monitor_v2.sh
- tools/migrate_monitor_state.py
- .tg_sessions/monitor_state_v2.json (if exists)
- TELEGRAM-MONITOR-V2-DEPLOYMENT-RUNBOOK.md

**Replaced by:**
- tools/restart_telegram_monitor_v3.sh
- .tg_sessions/monitor_state_v3.json
- TELEGRAM-MONITOR-V3-COMPLETE.md

**DO NOT:**
- Start V1 or V2 monitors
- Reference V1/V2 in production workflows
- Modify V1/V2 (use V3 for all improvements)

---

## Quick Reference for Weaver / External Collaborators

**Want to send message to Corey's Telegram instantly?**
```bash
python3 /home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/send_telegram_direct.py 437939400 "Your message here"
```

**Want to auto-send wrapped messages (Primary AI)?**
```bash
# 1. Ensure V3 monitor is running
bash /home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/restart_telegram_monitor_v3.sh 30

# 2. Use helper function (easiest)
source /home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_templates.sh
send_tg_wrapped "Your message here"

# 3. OR manually inject wrapped message with timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "🤖🎯📱[TIMESTAMP:$TIMESTAMP]
Your message here
✨🔚"

# V3 monitor detects and sends within 30 seconds
```

**Want to receive Corey's Telegram messages in tmux?**
```bash
# Start bridge (if not running)
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
nohup python3 tools/telegram_bridge.py > /tmp/telegram_bridge.log 2>&1 &

# Corey's messages appear instantly in tmux
```

**Want to check Telegram config?**
```bash
cat /home/corey/projects/AI-CIV/grow_gemini_deepresearch/config/telegram_config.json
```

---

## Test Commands

**Test direct sender:**
```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
python3 tools/send_telegram_direct.py 437939400 "Test from send_telegram_direct.py - $(date)"
```

**Test bridge detection:**
```bash
# 1. Start bridge if not running
nohup python3 tools/telegram_bridge.py > /tmp/telegram_bridge.log 2>&1 &

# 2. In Primary AI tmux session, output wrapped message:
echo "🤖🎯📱
Bridge test message - $(date)
✨🔚"

# 3. Check Telegram within 30 seconds
# 4. Check bridge logs:
tail -20 /tmp/telegram_bridge.log
```

---

## File Modification Protocol

**Before modifying ANY production-locked file:**

1. **Get explicit approval** from Corey or Primary AI
2. **Create backup:**
   ```bash
   cp tools/telegram_bridge.py tools/telegram_bridge.py.backup-$(date +%Y%m%d-%H%M%S)
   ```
3. **Test thoroughly** in isolated environment
4. **Verify with test commands** (see above)
5. **Update this registry** with new status
6. **Update tg-archi registry:** `memories/agents/tg-archi/telegram_script_registry.json`

**If modification breaks production:**
1. **Immediately restore backup:**
   ```bash
   cp tools/telegram_bridge.py.backup tools/telegram_bridge.py
   ```
2. **Alert Corey and Primary AI**
3. **Document what went wrong**
4. **Submit fix proposal before retrying**

---

## Registry Maintenance

**Update this registry when:**
- Production status changes (working → broken or vice versa)
- New Telegram script created
- Script deprecated or replaced
- Critical dependencies change

**Registry owner:** tg-archi agent  
**Review frequency:** Monthly or on significant changes  
**Cross-reference:** `memories/agents/tg-archi/telegram_script_registry.json`

---

**END OF REGISTRY**
