# Telegram Production Status Summary

**Date**: 2025-10-20
**Status**: PRODUCTION-READY ✅
**System**: Bidirectional Telegram Integration
**Latency**: <5 seconds typical

---

## Production Components

| Component | Status | Lock | Purpose | Verified |
|-----------|--------|------|---------|----------|
| `telegram_bridge.py` | PRODUCTION | LOCKED ✅ | Inbound receiver (Telegram → tmux) | 2025-10-19 |
| `telegram_jsonl_monitor.py` | PRODUCTION | LOCKED ✅ | Outbound monitor (wrapped → Telegram) | 2025-10-20 |
| `send_telegram_plain.py` | PRODUCTION | LOCKED ✅ | Plain text sender (JSONL monitor dependency) | 2025-10-20 |
| `send_telegram_direct.py` | PRODUCTION | LOCKED ✅ | Markdown sender (Primary direct use) | 2025-10-19 |
| `fix_telegram_session.sh` | PRODUCTION | LOCKED ✅ | Session config updater + bridge restart | 2025-10-20 |
| `telegram_boot.sh` | PRODUCTION | LOCKED ✅ | Full system startup (both daemons) | 2025-10-20 |

---

## System Architecture

```
INBOUND (Telegram → Primary):
  Telegram message
    ↓ (Bot API polling, 30s interval)
  telegram_bridge.py
    ↓ (tmux send-keys injection)
  Primary AI sees message in tmux

OUTBOUND (Primary → Telegram):
  Primary wraps message (🤖🎯📱 ... ✨🔚)
    ↓ (Claude Code writes to .jsonl)
  telegram_jsonl_monitor.py detects wrapper
    ↓ (calls send_telegram_plain.py)
  Corey sees message on Telegram
```

---

## Quick Commands

### Start Everything
```bash
bash tools/telegram_boot.sh
```

### Check Status
```bash
./tools/session_wakeup.sh
```

### Restart Bridge (if tmux session changed)
```bash
bash tools/fix_telegram_session.sh
```

### Restart Monitor
```bash
pkill -f telegram_jsonl_monitor.py
nohup python3 tools/telegram_jsonl_monitor.py --start-from-now > /tmp/telegram_jsonl_monitor.log 2>&1 &
```

### Verify Processes Running
```bash
pgrep -f telegram_bridge.py       # Should return PID
pgrep -f telegram_jsonl_monitor.py # Should return PID
```

### Check Logs
```bash
tail -f /tmp/acgee_telegram_bridge.log   # Inbound
tail -f /tmp/telegram_jsonl_monitor.log  # Outbound
```

---

## Production Protection Rules

**BEFORE modifying ANY Telegram script:**

1. **Read script registry**:
   ```bash
   cat memories/agents/tg-archi/telegram_script_registry.json
   ```

2. **Check production status**:
   - If `"production_lock": "LOCKED ✅"` → DO NOT modify without testing
   - Check `"called_by"` to see dependencies
   - Check `"never_modify_unless"` for conditions

3. **Test in experimental fork**:
   - Never modify production scripts directly
   - Create experimental version
   - Test end-to-end
   - Verify no regressions

4. **Update registry after changes**:
   - Document what changed
   - Update `last_verified_working` date
   - Add notes about changes

**Lesson Learned (2025-10-18)**:
> We broke our working system by modifying production scripts without checking the registry. ALWAYS check `telegram_script_registry.json` before modifying ANY Telegram script.

---

## Critical Dependencies

```
telegram_jsonl_monitor.py
  ├── CRITICAL: send_telegram_plain.py (DO NOT replace/deprecate)
  ├── CRITICAL: config/telegram_config.json (jsonl_monitor section)
  └── State: .tg_sessions/jsonl_monitor_state.json

telegram_bridge.py
  ├── CRITICAL: config/telegram_config.json (tmux_session, tmux_pane)
  └── State: .tg_sessions/437939400.json

send_telegram_plain.py
  ├── CRITICAL: config/telegram_config.json (bot_token)
  └── Called by: telegram_jsonl_monitor.py (PRODUCTION)
```

**Breaking ANY dependency = system failure!**

---

## Testing Checklist

### Test Inbound (Telegram → Primary)
- [ ] Send message from Telegram: "test inbound"
- [ ] Verify appears in tmux within 30s
- [ ] Check bridge log: `tail -f /tmp/acgee_telegram_bridge.log`

### Test Outbound (Primary → Telegram)
- [ ] Primary sends wrapped message:
  ```
  🤖🎯📱
  Test outbound
  ✨🔚
  ```
- [ ] Verify arrives on Telegram within 5s
- [ ] Check monitor log: `tail -f /tmp/telegram_jsonl_monitor.log`

### Verify State Persistence
- [ ] Check monitor state: `cat .tg_sessions/jsonl_monitor_state.json`
- [ ] Verify `last_processed_offset` > 0
- [ ] Verify `sent_message_hashes` contains entries (after sending messages)

---

## Troubleshooting Quick Reference

| Issue | Diagnostic | Fix |
|-------|-----------|-----|
| Outbound not working | `pgrep -f telegram_jsonl_monitor.py` | `bash tools/telegram_boot.sh` |
| Inbound not working | `grep tmux_pane config/telegram_config.json` | `bash tools/fix_telegram_session.sh` |
| Re-sending old messages | Check if `--start-from-now` was used | Reset state, restart with flag |
| Monitor stuck | Check `last_updated` in state file | Restart monitor |
| Bridge injection fails | Compare tmux session to config | Run `fix_telegram_session.sh` |

---

## Configuration

**File**: `config/telegram_config.json`

**Critical sections**:
```json
{
  "tmux_session": "6",          // MUST match current tmux session
  "tmux_pane": "6:0.0",         // MUST match current pane
  "jsonl_monitor": {
    "enabled": true,
    "sender_script": "tools/send_telegram_plain.py"  // DO NOT change
  }
}
```

**Update config** (when tmux session changes):
```bash
bash tools/fix_telegram_session.sh
```

---

## Wake-Up Integration

**From CLAUDE.md Session Start Principles:**

**Step 1: Telegram session start (WRAPPED)**
```bash
source tools/telegram_templates.sh
tg_session_start
```

**Step 2: Run wake-up script**
```bash
./tools/session_wakeup.sh
```

**If Telegram processes NOT running**:
```bash
bash tools/telegram_boot.sh
```

**Step 6: Telegram context loaded (WRAPPED)**
```bash
tg_context_loaded "[handoff]" "[priority]"
```

---

## Performance Characteristics

**Latency**:
- Inbound: ~30s (polling interval)
- Outbound: <5s typical (3s poll + processing)

**Resource Usage**:
- Bridge: ~10MB RAM
- Monitor: ~15MB RAM
- Combined: <30MB RAM

**Reliability Features**:
- Deduplication (prevents re-sends)
- State persistence (survives restarts)
- Session rotation handling
- Graceful shutdown (SIGTERM, SIGINT)
- Automatic retry (3 attempts with exponential backoff)

---

## Documentation Index

| Document | Purpose |
|----------|---------|
| `TELEGRAM-BIDIRECTIONAL-SYSTEM-PRODUCTION.md` | Full production documentation |
| `memories/agents/tg-archi/telegram_script_registry.json` | Canonical script registry |
| `memories/agents/tg-archi/PRIMARY_TELEGRAM_PROTOCOL.md` | Primary usage protocol |
| `.claude/CLAUDE.md` | Wake-up protocol integration |
| `tools/telegram_templates.sh` | Quick command templates |

---

## Rollback Procedure

If changes break the system:

```bash
# 1. Restore working version
git checkout HEAD~1 tools/[broken_script].py

# 2. Restart system
bash tools/telegram_boot.sh

# 3. Verify working
# Test inbound + outbound

# 4. Document failure in registry
vim memories/agents/tg-archi/telegram_script_registry.json
```

---

## Success Metrics

**Current Performance** (as of 2025-10-20):
- ✅ Inbound working: Telegram → tmux injection
- ✅ Outbound working: Wrapped messages → Telegram
- ✅ Latency: <5s typical (sub-second many cases)
- ✅ Reliability: State persistence, deduplication, retry logic
- ✅ Production-locked: All critical scripts protected
- ✅ Boot integration: `telegram_boot.sh` starts both daemons
- ✅ Wake-up integration: `session_wakeup.sh` shows status

**Known Issues**: NONE

**Future Enhancements**:
- Health monitoring endpoint
- Metrics collection
- Alerting on failures
- Rich formatting (buttons, keyboards)

---

**Document Status**: PRODUCTION SUMMARY
**Last Updated**: 2025-10-20
**Maintainer**: tg-archi agent

---

## REMEMBER

> "ALWAYS check `telegram_script_registry.json` BEFORE modifying ANY Telegram script."

**This prevents breaking working production systems.**

---

**End of Summary**
