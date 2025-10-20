# Telegram System Boot Message Template

**Purpose**: Standard message tg-archi sends when starting or checking Telegram systems
**When to use**: Every tg-archi invocation (automatic health check)

---

## Template

```
Telegram Infrastructure Status:
- Bridge (PID {bridge_pid}): Bi-directional Telegram ↔ tmux {status}
- Monitor (PID {monitor_pid}): Auto-sends wrapped messages to Telegram {status}
- Last bridge activity: {bridge_timestamp}
- Last monitor activity: {monitor_timestamp}

Primary reminder:
- Wrap messages for auto-mirroring: 🤖🎯📱 ... ✨🔚
- Direct send: python3 tools/send_telegram_direct.py 437939400 "message"
- File send: python3 tools/send_telegram_file.py 437939400 /path/to/file "caption"
- Templates: source tools/telegram_templates.sh && tg_session_start

Full protocol: memories/agents/tg-archi/PRIMARY_TELEGRAM_PROTOCOL.md
```

---

## Variables to Fill

- `{bridge_pid}`: Process ID from `ps aux | grep telegram_bridge.py` (or "NONE" if not running)
- `{monitor_pid}`: Process ID from `ps aux | grep telegram_monitor.py` (or "NONE" if not running)
- `{status}`: One of:
  - `✅ RUNNING` - Process active and healthy
  - `🔄 RESTARTED` - Was dead, now restarted
  - `❌ FAILED` - Cannot start or crashed repeatedly
- `{bridge_timestamp}`: Last log entry from `/tmp/telegram_bridge.log`
- `{monitor_timestamp}`: Last log entry from `/tmp/telegram_monitor.log`

---

## Example (All Healthy)

```
Telegram Infrastructure Status:
- Bridge (PID 12345): Bi-directional Telegram ↔ tmux ✅ RUNNING
- Monitor (PID 12346): Auto-sends wrapped messages to Telegram ✅ RUNNING
- Last bridge activity: 2025-10-18 14:32:15 (message received from Corey)
- Last monitor activity: 2025-10-18 14:30:00 (polling tmux)

Primary reminder:
- Wrap messages for auto-mirroring: 🤖🎯📱 ... ✨🔚
- Direct send: python3 tools/send_telegram_direct.py 437939400 "message"
- File send: python3 tools/send_telegram_file.py 437939400 /path/to/file "caption"
- Templates: source tools/telegram_templates.sh && tg_session_start

Full protocol: memories/agents/tg-archi/PRIMARY_TELEGRAM_PROTOCOL.md
```

---

## Example (Monitor Restarted)

```
Telegram Infrastructure Status:
- Bridge (PID 12345): Bi-directional Telegram ↔ tmux ✅ RUNNING
- Monitor (PID 12789): Auto-sends wrapped messages to Telegram 🔄 RESTARTED
- Last bridge activity: 2025-10-18 14:32:15 (message received from Corey)
- Last monitor activity: 2025-10-18 14:35:01 (restarted by health check)

Primary reminder:
- Wrap messages for auto-mirroring: 🤖🎯📱 ... ✨🔚
- Direct send: python3 tools/send_telegram_direct.py 437939400 "message"
- File send: python3 tools/send_telegram_file.py 437939400 /path/to/file "caption"
- Templates: source tools/telegram_templates.sh && tg_session_start

Full protocol: memories/agents/tg-archi/PRIMARY_TELEGRAM_PROTOCOL.md

Note: Monitor was dead, successfully restarted. Auto-mirroring should resume.
```

---

## Example (Critical Failure)

```
Telegram Infrastructure Status:
- Bridge (PID NONE): Bi-directional Telegram ↔ tmux ❌ FAILED
- Monitor (PID 12346): Auto-sends wrapped messages to Telegram ✅ RUNNING
- Last bridge activity: 2025-10-18 12:15:32 (crashed - no bot token?)
- Last monitor activity: 2025-10-18 14:30:00 (polling tmux)

Primary reminder:
- Wrap messages for auto-mirroring: 🤖🎯📱 ... ✨🔚
- Direct send: python3 tools/send_telegram_direct.py 437939400 "message"
- File send: python3 tools/send_telegram_file.py 437939400 /path/to/file "caption"
- Templates: source tools/telegram_templates.sh && tg_session_start

Full protocol: memories/agents/tg-archi/PRIMARY_TELEGRAM_PROTOCOL.md

⚠️ CRITICAL: Bridge failed to start! Incoming messages from Corey will not be received!
Error log: /tmp/telegram_bridge.log
Escalating to Primary for investigation.
```

---

## Why This Matters

**Purpose of boot message:**
1. **Confirms systems are running** - Primary knows Telegram is operational
2. **Reminds wrapper protocol** - Primary doesn't need to remember emoji sequence
3. **Shows available commands** - Quick reference for direct sends
4. **Points to full protocol** - If Primary needs details
5. **Alerts on failures** - Immediate visibility if systems down

**When to send:**
- Every tg-archi invocation (automatic)
- After health check completes
- Before returning control to Primary

**This prevents:**
- Primary using Telegram when systems are down
- Forgetting wrapper protocol syntax
- Confusion about which scripts to call
- Silent failures going unnoticed

---

**Template created 2025-10-18 as part of Telegram infrastructure hardening.**
