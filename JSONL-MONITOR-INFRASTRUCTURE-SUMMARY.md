# JSONL Wrapper Monitor - Infrastructure Design Summary

**Date**: 2025-10-20
**Author**: tg-archi (Telegram Infrastructure Specialist)
**Status**: Ready for Architect Review

---

## What We're Building

A **REPLACEMENT** for tmux-polling wrapper detection with a JSONL file watcher that:
- Watches Claude Code conversation logs (JSONL format)
- Detects wrapped messages (`🤖🎯📱` ... `✨🔚`)
- Sends to Telegram via `send_telegram_plain.py`
- Sub-second latency (vs 30s with tmux polling)

---

## Architecture Overview

```
Current State (tmux-based):
  Primary → tmux → telegram_bridge.py polls tmux → send_telegram_direct.py → Telegram
  (30s latency, screen scraping, inefficient)

New State (JSONL-based):
  Primary → Claude Code JSONL → telegram_jsonl_monitor.py watches file → send_telegram_plain.py → Telegram
  (<5s latency, structured data, efficient)
```

---

## Key Design Decisions

### 1. Process Management
- **New daemon**: `telegram_jsonl_monitor.py` (independent process)
- **Keep existing**: `telegram_bridge.py` (Telegram → tmux receiver, still needed)
- **Startup**: Via `telegram_boot.sh` (boots both daemons)
- **Health monitoring**: Integrated into `telegram_health_check.sh`

### 2. Configuration
- **Extend existing**: `config/telegram_config.json` (add `jsonl_monitor` section)
- **Session detection**: Auto-find most recent JSONL file in Claude Code log dir
- **Hot-reload**: Most settings reload without restart (poll interval, markers, etc.)
- **State tracking**: `.tg_sessions/jsonl_monitor_state.json` (deduplication, offset)

### 3. Script Registry
- **Add entry**: `telegram_jsonl_monitor.py` (PRODUCTION after verification)
- **Update entry**: `telegram_bridge.py` (note wrapper detection removed)
- **Production lock**: Uses `send_telegram_plain.py` (not `send_telegram_direct.py`)
- **Why plain?**: Avoid Markdown parsing issues with extracted JSONL content

### 4. Error Handling
- **Telegram API failures**: Retry with exponential backoff (3 attempts)
- **JSONL rotation**: Auto-detect new session files, seamless switch
- **Logging**: Main log + error-only log, daily rotation
- **Graceful degradation**: Never crash monitor, log failures, continue running

### 5. Testing
- **Dry-run mode**: Test detection without sending
- **Parallel phase**: Run old + new monitor simultaneously (7 days)
- **Verification**: Compare outputs, ensure 100% coverage
- **Test script**: `test_telegram_jsonl_monitor.sh` (unit tests)

---

## Migration Plan

### Phase 1: Implementation (Days 1-3)
- Coder builds `telegram_jsonl_monitor.py`
- Add config, test script, registry entry
- Run dry-run tests

### Phase 2: Parallel Testing (Days 4-7)
- Deploy JSONL monitor alongside tmux monitor
- Both send to Telegram (accept duplicates during testing)
- Compare logs, verify 100% coverage

### Phase 3: Cutover (Day 8)
- Stop tmux monitor wrapper detection
- JSONL monitor becomes sole wrapper sender
- Monitor for 24 hours

### Phase 4: Cleanup (Days 9-15)
- Remove old wrapper detection code
- Update `telegram_bridge.py` to receiver-only
- Production-lock JSONL monitor
- Update docs

---

## Integration Points

### Boot Script (`telegram_boot.sh`)
```bash
# Start receiver (Telegram → tmux)
nohup python3 tools/telegram_bridge.py > /tmp/telegram_bridge.log 2>&1 &

# Start sender (JSONL → Telegram)
nohup python3 tools/telegram_jsonl_monitor.py > /tmp/telegram_jsonl_monitor.log 2>&1 &
```

### Health Check (`telegram_health_check.sh`)
```bash
# Check both processes running
pgrep -f telegram_bridge.py
pgrep -f telegram_jsonl_monitor.py

# Auto-restart if dead
```

### Wake-Up Script (`session_wakeup.sh`)
```bash
# Report JSONL monitor status
if pgrep -f telegram_jsonl_monitor.py > /dev/null; then
    echo "✓ JSONL monitor (sender): Running"
else
    echo "✗ JSONL monitor (sender): DEAD"
fi
```

---

## Configuration Schema

**Add to** `config/telegram_config.json`:

```json
{
  "jsonl_monitor": {
    "enabled": true,
    "claude_code_log_dir": "/home/corey/.config/Claude/Code/User/globalStorage/saoudrizwan.claude-dev/tasks",
    "watch_method": "tail",
    "poll_interval_seconds": 1,
    "state_file": ".tg_sessions/jsonl_monitor_state.json",
    "wrapper_markers": {
      "start": "🤖🎯📱",
      "end": "✨🔚"
    },
    "sender_script": "tools/send_telegram_plain.py",
    "max_message_length": 4096,
    "deduplication_enabled": true,
    "log_file": "/tmp/telegram_jsonl_monitor.log",
    "error_log_file": "/tmp/telegram_jsonl_monitor_error.log"
  }
}
```

---

## Success Metrics

**Performance:**
- Latency: <5 seconds (wrapper → Telegram delivery)
- CPU usage: <1% average
- Memory: <50MB

**Quality:**
- Zero duplicate sends (deduplication working)
- Zero missed messages (100% coverage)
- Zero false positives (only wrapped messages sent)

**Operational:**
- Health check passes 100% (auto-restart works)
- Config hot-reload working
- Session rotation seamless

---

## Open Questions for Architect

1. **File watching**: Use Python `inotify` library or `tail -f` subprocess?
2. **State tracking**: Track message hashes or JSONL line offsets?
3. **Rate limiting**: Implement max messages per minute?
4. **Multi-session**: Support multiple simultaneous Claude Code sessions?

---

## Open Questions for Primary

1. **Wrapper config**: Keep markers configurable or hardcode?
2. **Markdown support**: Add Markdown formatting to plain sender?
3. **Emergency fallback**: Implement emergency "send to Corey" command?

---

## Open Questions for Corey

1. **Parallel testing**: Accept duplicate sends during 7-day parallel phase?
2. **Error notification**: Email Corey when monitor encounters critical errors?
3. **Permanent logging**: Log wrapper messages to file (not just Telegram)?

---

## Files Created

**Design Documentation:**
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/JSONL-WRAPPER-MONITOR-INFRASTRUCTURE-DESIGN.md` (full design, 600+ lines)
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/JSONL-MONITOR-INFRASTRUCTURE-SUMMARY.md` (this file)

**Next Steps:**
1. Architect reviews design (parallel task)
2. tg-archi + architect align on decisions
3. Coder implements `telegram_jsonl_monitor.py`
4. tg-archi deploys and tests

---

## Key Insights from tg-archi Perspective

### Why This Matters (Infrastructure)

1. **Latency reduction**: 30s → <5s = better UX for Corey
2. **Reliability improvement**: JSONL parsing > screen scraping
3. **Efficiency gain**: Event-driven > polling
4. **Maintainability**: Structured data easier to debug

### Risks Mitigated

1. **Vendor lock-in**: JSONL format dependency (acceptable, Claude Code stable)
2. **Session rotation**: Auto-detection handles seamlessly
3. **Telegram API failures**: Retry logic + graceful degradation
4. **Configuration errors**: Hot-reload + defaults prevent crashes

### Production Safeguards

1. **Script registry**: Clear PRODUCTION vs EXPERIMENTAL status
2. **Sender lock**: Config specifies sender, not hardcoded
3. **Health monitoring**: Auto-restart if process dies
4. **Parallel testing**: 7 days to verify before cutover
5. **Rollback plan**: Keep old monitor available during Phase 2

---

## Infrastructure Perspective Summary

**From tg-archi's view, this design:**

✅ **Integrates cleanly** with existing Telegram infrastructure
✅ **Protects production** via registry, config, and phased rollout
✅ **Enables testing** via dry-run mode and parallel operation
✅ **Handles errors** gracefully without crashing monitor
✅ **Simplifies operations** via health checks and auto-restart
✅ **Reduces maintenance** via hot-reload and structured logging

**Ready for architect review and coder implementation.**

---

**Author**: tg-archi (Telegram Infrastructure Specialist)
**Contact**: Invoke via `Task(tg-archi)` for questions
**Next Review**: After architect provides feedback

**Full Design**: `memories/agents/tg-archi/JSONL-WRAPPER-MONITOR-INFRASTRUCTURE-DESIGN.md`
