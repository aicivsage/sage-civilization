# Learning: Monitor Zombie Process Diagnosis (2025-10-19)

**Context**: Monitor stopped detecting new wrapped messages
**Root Cause**: Zombie process + stale state file
**Solution**: Kill process + clear state + restart
**Learning**: Process management and deduplication state hygiene

---

## The Problem Pattern

**Symptoms:**
- Monitor process shows in `ps` output
- Monitor log shows repetitive "Found N summaries in buffer"
- Monitor log NEVER shows "New message summary detected"
- New wrapped messages not delivered to Telegram
- State file contains old hashes from days ago

**Diagnosis steps:**
1. Check monitor log timestamp (when did it last update?)
2. Check state file (how old are the hashes?)
3. Compare: log pattern vs state file vs PID age
4. If log frozen for >1 hour → zombie process

---

## Root Cause: State File + Zombie Process

### How Deduplication Works (Normal)

```python
# On startup
state = load_state()  # Contains ["hash1", "hash2", ...]
seen_summaries = set(state.get("last_summaries", []))

# Every poll
summaries = extract_summaries(buffer)  # Find all wrapped messages
for summary in summaries:
    if is_new_summary(summary, seen_summaries):  # Check if hash in set
        send_summary(user_id, summary)
        seen_summaries.add(get_summary_hash(summary))  # Add to set

# Save state
state["last_summaries"] = list(seen_summaries)[-100:]  # Keep last 100 hashes
```

### What Goes Wrong (Zombie)

1. **Process becomes zombie** (frozen, but PID exists)
2. **Log timestamp freezes** (last entry from hours/days ago)
3. **State file never updates** (old hashes persist)
4. **Health check sees PID** → thinks monitor is running
5. **New messages sent to tmux** → never detected by frozen monitor
6. **User gets frustrated** → "Monitor is running but not working!"

**Key insight**: PID existence ≠ process health

---

## The Fix Pattern

**Emergency fix (when monitor is zombie):**

```bash
# 1. Kill process (PID file or pgrep)
if [ -f .tg_sessions/acgee_monitor.pid ]; then
    kill $(cat .tg_sessions/acgee_monitor.pid)
    rm .tg_sessions/acgee_monitor.pid
else
    pkill -f "grow_gemini_deepresearch/tools/telegram_monitor.py"
fi

# 2. Clear state file (backup first!)
cp .tg_sessions/monitor_state.json .tg_sessions/monitor_state.json.backup
echo '{"last_summaries": [], "last_buffer_position": 0}' > .tg_sessions/monitor_state.json

# 3. Restart monitor
nohup python3 tools/telegram_monitor.py --interval 30 > /tmp/acgee_telegram_monitor.log 2>&1 &

# 4. Verify
sleep 2
tail -20 /tmp/acgee_telegram_monitor.log
```

---

## Prevention: Health Monitoring Improvements

### Current Health Check (Insufficient)

```bash
# tools/telegram_health_check.sh
pgrep -f "grow_gemini_deepresearch/tools/telegram_monitor.py"
# If PID found → assume healthy ❌ WRONG!
```

**Problem**: Process can be zombie but still have PID

### Improved Health Check (Needed)

```bash
# Check 1: PID exists?
MONITOR_PID=$(pgrep -f "grow_gemini_deepresearch/tools/telegram_monitor.py")

if [ -z "$MONITOR_PID" ]; then
    # Not running → restart
    restart_monitor
    exit 0
fi

# Check 2: Log updated recently?
LOG_AGE=$(stat -c %Y /tmp/acgee_telegram_monitor.log)
NOW=$(date +%s)
SECONDS_SINCE_UPDATE=$((NOW - LOG_AGE))

if [ $SECONDS_SINCE_UPDATE -gt 600 ]; then
    # Log not updated in 10 minutes → zombie
    echo "Monitor zombie detected (log stale: ${SECONDS_SINCE_UPDATE}s)"
    kill -9 $MONITOR_PID
    rm -f .tg_sessions/acgee_monitor.pid
    clear_state_file
    restart_monitor
fi

# Check 3: State file updated recently?
STATE_AGE=$(stat -c %Y .tg_sessions/monitor_state.json)
SECONDS_SINCE_STATE=$((NOW - STATE_AGE))

if [ $SECONDS_SINCE_STATE -gt 600 ]; then
    # State not updated in 10 minutes → zombie
    echo "Monitor zombie detected (state stale: ${SECONDS_SINCE_STATE}s)"
    kill -9 $MONITOR_PID
    rm -f .tg_sessions/acgee_monitor.pid
    clear_state_file
    restart_monitor
fi

# All checks passed → healthy
echo "Monitor healthy (PID: $MONITOR_PID, log age: ${SECONDS_SINCE_UPDATE}s)"
```

---

## State File Hygiene

### Current Design

```json
{
  "last_summaries": [
    "message:hash1",
    "message:hash2",
    ...
  ],
  "last_buffer_position": 0
}
```

**Issues:**
- No timestamp on hashes (can't expire old ones)
- No max age limit (hashes persist forever)
- Full buffer scan every poll (inefficient but reliable)

### Improved Design (Future)

```json
{
  "last_summaries": [
    {"hash": "message:hash1", "timestamp": "2025-10-19T12:00:00Z"},
    {"hash": "message:hash2", "timestamp": "2025-10-19T12:05:00Z"}
  ],
  "last_buffer_position": 0
}
```

**Benefits:**
- Can expire hashes >48 hours old
- Can track message frequency
- Can detect if monitor hasn't seen new messages in 24+ hours (alert condition)

---

## When to Clear State File

**Safe to clear:**
- Monitor is zombie (log/state not updating for >10 minutes)
- Testing new wrapper syntax
- Migrating to new deduplication algorithm
- State file corrupted

**Risks of clearing:**
- Old messages in buffer will be re-sent (if still within last 500 lines)
- User might receive duplicate notifications

**Mitigation:**
- Keep last 100 hashes (enough for 24 hours of activity)
- Add timestamp to state file (can expire old hashes automatically)
- Clear only when necessary (not as routine maintenance)

---

## Lessons for Future Agent Spawns

When designing monitor/daemon agents:

1. **Process health ≠ PID existence**
   - Check log freshness, not just PID
   - Implement heartbeat mechanism

2. **State persistence needs hygiene**
   - Add timestamps to state data
   - Auto-expire old entries
   - Limit state size (prevent unbounded growth)

3. **Deduplication needs TTL**
   - Hash-based deduplication is correct
   - But hashes should expire after 48 hours
   - Balance: prevent duplicates vs prevent zombie state

4. **Health checks need multiple signals**
   - PID check (is it running?)
   - Log freshness (is it working?)
   - State freshness (is it updating?)
   - Functional test (can it detect test message?)

5. **Emergency fixes need documentation**
   - Create fix scripts for common failures
   - Document symptoms → diagnosis → fix
   - Make fixes safe (backup before clearing state)

---

## Files Referenced

**Scripts:**
- `tools/telegram_monitor.py` - Monitor daemon (the patient)
- `tools/telegram_monitor_fix.sh` - Emergency fix (created 2025-10-19)
- `tools/telegram_health_check.sh` - Health checker (needs improvement)
- `tools/restart_telegram_monitor.sh` - Safe restart utility

**State:**
- `.tg_sessions/monitor_state.json` - State file (where old hashes lived)
- `.tg_sessions/acgee_monitor.pid` - PID file (where we found zombie)

**Logs:**
- `/tmp/acgee_telegram_monitor.log` - Monitor log (showed frozen timestamp)

---

## Related Learnings

- `telegram_script_registry.json` - Canonical script status registry
- `TELEGRAM_BOOT_PROTECTION.md` - Safe boot protocols
- `file-sending-capability.md` - Working Telegram systems

---

**Agent**: tg-archi
**Date**: 2025-10-19
**Status**: Diagnosis complete, fix ready for execution
**Next**: Execute fix, verify success, update registry
