# Telegram Monitor V2 - Deployment Runbook

**Date**: 2025-10-19
**Status**: READY FOR DEPLOYMENT
**Implementation**: coder (autonomous)

---

## Overview

Telegram Monitor V2 replaces V1's hash-based deduplication with watermark-based architecture.

**Key improvements:**
- Zero message loss (watermark + retry queue)
- Zero duplicates (watermark prevents re-processing)
- Graceful restart (watermark persists)
- Fast polling (10-30s intervals)
- Fail-loud error handling

**Architecture**: See `memories/knowledge/architecture/ADR-001-telegram-monitor-v2-event-driven-architecture.md`

---

## Pre-Deployment Checklist

- [ ] V1 monitor status verified
- [ ] Recent V1 logs reviewed (check for pending messages)
- [ ] V1 state backed up
- [ ] Tests passing (28 tests, 2 skipped manual tests)
- [ ] Scripts executable (restart_telegram_monitor_v2.sh, migrate_monitor_state.py)

**Verify V1 status:**
```bash
ps aux | grep telegram_monitor.py | grep -v v2
tail -50 /tmp/acgee_telegram_monitor.log
cat .tg_sessions/monitor_state.json
```

---

## Deployment Steps

### Step 1: Stop V1 Monitor

**Option A: Using stop script (if exists)**
```bash
bash tools/stop_telegram_monitor.sh
```

**Option B: Manual stop**
```bash
# Get PID
cat .tg_sessions/acgee_monitor.pid

# Kill process
kill <PID>

# Verify stopped
ps aux | grep telegram_monitor.py | grep -v v2
```

**Verification:**
- No V1 monitor process running
- PID file removed (or stale)

---

### Step 2: Migrate State

**Run migration script:**
```bash
python3 tools/migrate_monitor_state.py
```

**Expected output:**
```
🔄 Migrating Telegram Monitor V1 → V2 state

✅ V1 state backed up: .tg_sessions/monitor_state_v1_backup.json
✅ V2 state created: .tg_sessions/monitor_state_v2.json

Migration complete!

⚠️  IMPORTANT:
   V2 will re-send all wrapped messages currently in tmux buffer
   This is expected on first migration poll
   Subsequent polls will use watermark to avoid duplicates
```

**Verification:**
- V1 state backed up: `ls -lh .tg_sessions/monitor_state_v1_backup.json`
- V2 state exists: `cat .tg_sessions/monitor_state_v2.json`
- V2 state has watermark=0: `jq '.watermark' .tg_sessions/monitor_state_v2.json`

---

### Step 3: Start V2 Monitor

**Run restart script:**
```bash
bash tools/restart_telegram_monitor_v2.sh 30
```
(30 = polling interval in seconds, adjust as needed)

**Expected output:**
```
🔄 Restarting Telegram Monitor V2
   Project: /home/corey/projects/AI-CIV/grow_gemini_deepresearch
   Interval: 30s

No existing V2 monitor found
Clearing old log...

Starting V2 monitor...
   ✅ Started (PID: <PID>)

Monitor V2 running!

Check status:
   ps aux | grep telegram_monitor_v2.py

View logs:
   tail -f /tmp/acgee_telegram_monitor_v2.log

Recent log output:
2025-10-19 12:00:00,000 - telegram_monitor_v2 - INFO - Created PID file: .tg_sessions/acgee_monitor_v2.pid (PID: <PID>)
2025-10-19 12:00:00,001 - telegram_monitor_v2 - INFO - Loaded user config: user_id=437939400
2025-10-19 12:00:00,002 - telegram_monitor_v2 - INFO - No state file found - starting fresh
2025-10-19 12:00:00,003 - telegram_monitor_v2 - INFO - 🚀 Monitor V2 started: interval=30s, session=0
2025-10-19 12:00:00,004 - telegram_monitor_v2 - INFO -    Watermark: 0
2025-10-19 12:00:00,005 - telegram_monitor_v2 - INFO -    Retry queue: 0 messages
2025-10-19 12:00:00,006 - telegram_monitor_v2 - INFO -    Dead letter: 0 messages
```

**Verification:**
- Process running: `ps aux | grep telegram_monitor_v2.py`
- PID file exists: `cat .tg_sessions/acgee_monitor_v2.pid`
- Log shows startup: `tail -20 /tmp/acgee_telegram_monitor_v2.log`

---

### Step 4: Send Test Message

**In tmux session 0:**
```bash
echo '🤖🎯📱'
echo 'TEST: V2 Monitor Deployment'
echo 'Timestamp: 2025-10-19 12:00'
echo '✨🔚'
```

**Wait 30 seconds** (or your poll interval)

**Expected behavior:**
1. V2 monitor detects message in next poll
2. Sends to Telegram within poll interval
3. Watermark advances
4. Log shows successful send

**Verification:**
- Check Corey's Telegram: Test message delivered
- Check logs: `tail -30 /tmp/acgee_telegram_monitor_v2.log`
  - Should show: "Found X total messages in buffer"
  - Should show: "🆕 1 new messages detected"
  - Should show: "✅ Sent message <ID> to user 437939400"
  - Should show: "✅ Watermark advanced to <POSITION>"
- Check state: `jq '.watermark' .tg_sessions/monitor_state_v2.json`
  - Should be > 0 (watermark advanced)

---

### Step 5: Monitor for 1 Hour

**Watch logs in real-time:**
```bash
tail -f /tmp/acgee_telegram_monitor_v2.log
```

**Send additional test messages** (spaced 5-10 minutes apart):
```bash
echo '🤖🎯📱'
echo 'V2 Stability Test - Message 2'
echo '✨🔚'
```

**Monitor metrics:**
- All messages delivered to Telegram
- No duplicates sent
- Watermark advances monotonically
- No error messages in logs
- State file updates correctly

**Check state periodically:**
```bash
# Every 15 minutes
cat .tg_sessions/monitor_state_v2.json

# Expected values:
# - watermark: increasing (never decreasing)
# - retry_queue: empty (no failures)
# - dead_letter: empty (no permanent failures)
```

---

### Step 6: Verify Success

**After 1 hour of stable operation:**

- [ ] All test messages delivered
- [ ] No duplicates detected
- [ ] Watermark advancing correctly
- [ ] No errors in logs
- [ ] State file healthy (retry_queue and dead_letter empty)
- [ ] Process stable (PID unchanged)

**If all checks pass:**
```bash
# Delete V1 state backup (no longer needed)
rm .tg_sessions/monitor_state_v1_backup.json

# Optional: Archive V1 monitor script
mv tools/telegram_monitor.py tools/telegram_monitor_v1.py.archive
```

**Document success:**
- Update tg-archi script registry: Mark V2 as PRODUCTION
- Create memory entry documenting deployment
- Update TELEGRAM-BOOT-QUICK-START.md to reference V2

---

## Rollback Procedure

**If V2 fails or shows critical issues:**

### Step 1: Stop V2
```bash
# Get V2 PID
cat .tg_sessions/acgee_monitor_v2.pid

# Kill V2
kill <PID>

# Remove PID file
rm .tg_sessions/acgee_monitor_v2.pid
```

### Step 2: Restore V1 State
```bash
# Restore V1 state from backup
cp .tg_sessions/monitor_state_v1_backup.json .tg_sessions/monitor_state.json
```

### Step 3: Start V1
```bash
# Using restart script
bash tools/restart_telegram_monitor.sh

# OR manual start
nohup python3 tools/telegram_monitor.py --interval 300 >> /tmp/acgee_telegram_monitor.log 2>&1 &
```

### Step 4: Verify V1 Running
```bash
ps aux | grep telegram_monitor.py | grep -v v2
tail -20 /tmp/acgee_telegram_monitor.log
```

### Step 5: Investigate V2 Failure
```bash
# Review V2 logs
cat /tmp/acgee_telegram_monitor_v2.log

# Check V2 state at failure
cat .tg_sessions/monitor_state_v2.json

# File bug report
# Document failure mode
# Escalate to Primary for architect review
```

---

## Troubleshooting

### Issue: V2 Not Starting

**Symptoms:**
- Restart script reports failure
- No PID file created
- Log shows error

**Diagnosis:**
```bash
# Check log for error
cat /tmp/acgee_telegram_monitor_v2.log

# Common issues:
# 1. Config file missing/invalid
cat config/telegram_config.json

# 2. State file corrupted
cat .tg_sessions/monitor_state_v2.json | python3 -m json.tool

# 3. Tmux not accessible
tmux capture-pane -t 0 -p | head -10
```

**Fix:**
- If config missing: Create from template
- If state corrupted: Delete and recreate with migrate script
- If tmux issue: Verify tmux session exists

---

### Issue: Messages Not Detected

**Symptoms:**
- Wrapped messages in tmux buffer
- Log shows "Found 0 total messages"
- No Telegram delivery

**Diagnosis:**
```bash
# Check tmux buffer manually
tmux capture-pane -t 0 -p -S -500 | grep -A5 "🤖🎯📱"

# Verify markers correct
# START: 🤖🎯📱
# END: ✨🔚
```

**Fix:**
- Verify markers match exactly (emoji copy-paste errors common)
- Check tmux session number (default: "0")
- Restart monitor with --tmux-session flag if needed

---

### Issue: Messages Sent Multiple Times

**Symptoms:**
- Same message delivered to Telegram multiple times
- Watermark not advancing

**Diagnosis:**
```bash
# Check watermark value
jq '.watermark' .tg_sessions/monitor_state_v2.json

# Check retry queue
jq '.retry_queue | length' .tg_sessions/monitor_state_v2.json

# Check logs for watermark updates
grep "Watermark advanced" /tmp/acgee_telegram_monitor_v2.log
```

**Fix:**
- If watermark=0 and not advancing: State flush failing (disk space?)
- If retry_queue growing: Telegram API failures (circuit breaker should trigger)
- If logs show "Failed to flush state": Check disk space and permissions

---

### Issue: Messages Lost

**Symptoms:**
- Wrapped message in buffer
- Monitor detects message (log shows "New message detected")
- No Telegram delivery
- Message not in retry queue

**Diagnosis:**
```bash
# Check circuit breaker state
grep "Circuit breaker" /tmp/acgee_telegram_monitor_v2.log | tail -5

# Check retry queue
cat .tg_sessions/monitor_state_v2.json | jq '.retry_queue'

# Check dead letter queue
cat .tg_sessions/monitor_state_v2.json | jq '.dead_letter'
```

**Fix:**
- If circuit breaker OPEN: Telegram API down (wait for recovery)
- If message in dead_letter: Max retries exceeded (manual investigation needed)
- If message nowhere: Critical bug (escalate immediately, rollback to V1)

---

## Performance Metrics

**Track these metrics after deployment:**

**Latency:**
- P50 (median): Should be ~15-20 seconds (half poll interval)
- P95: Should be <30 seconds (poll interval)
- P99: Should be <60 seconds (retry backoff)

**Reliability:**
- Message loss rate: 0%
- Duplicate rate: 0%
- Delivery success rate: >99%

**Availability:**
- Uptime: >99.9%
- Process crashes: 0
- State corruption events: 0

**Health:**
- Retry queue size: <5 messages (sustained)
- Dead letter queue size: <10 messages (lifetime)
- Circuit breaker opens: <1/day

---

## Next Steps After Deployment

1. **Monitor for 24 hours** - Ensure stability before archiving V1
2. **Load testing** - Send burst of 10 messages, verify all delivered
3. **Chaos testing** - Kill monitor mid-send, verify recovery
4. **Documentation** - Update all references to V1 → V2
5. **Health monitoring** - Add automated alerts for failures
6. **Performance tuning** - Adjust poll interval based on usage patterns

---

## Files Deployed

**Core implementation:**
- `/tools/telegram_monitor_v2.py` - Main monitor script
- `/tools/restart_telegram_monitor_v2.sh` - Deployment script
- `/tools/migrate_monitor_state.py` - State migration
- `/tests/test_telegram_monitor_v2.py` - Test suite

**State files:**
- `/.tg_sessions/monitor_state_v2.json` - Persistent state
- `/.tg_sessions/acgee_monitor_v2.pid` - Process ID

**Logs:**
- `/tmp/acgee_telegram_monitor_v2.log` - Monitor logs

**Documentation:**
- `/memories/knowledge/architecture/ADR-001-telegram-monitor-v2-event-driven-architecture.md` - Architecture
- `/TELEGRAM-MONITOR-V2-DEPLOYMENT-RUNBOOK.md` - This document

---

**Deployment Owner**: coder
**Test Coverage**: 28 tests (100% passing, 2 manual tests skipped)
**Estimated Risk**: LOW (comprehensive testing, rollback procedure, fail-loud design)
**Recommended Deployment Window**: Any time (non-critical system, easy rollback)
