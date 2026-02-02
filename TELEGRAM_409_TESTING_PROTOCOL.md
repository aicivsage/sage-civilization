# Telegram Bridge 409 Fix - Testing Protocol

**Date**: 2025-12-29
**Agent**: architect → tester
**Architecture**: See `TELEGRAM_409_CONFLICT_FIX_ARCHITECTURE.md`
**Implementation**: See `TELEGRAM_409_IMPLEMENTATION_SPEC.md`

---

## Test Execution Order

1. Test 1: Single Instance Guarantee (5 min)
2. Test 2: Stale PID Cleanup (3 min)
3. Test 3: 409 Detection in Logs (5 min)
4. Test 4: Health Check Auto-Recovery (5 min)
5. Test 5: 48-Hour Stability (48 hours - separate execution)

**Total active testing time**: ~20 minutes
**Total calendar time**: 48+ hours (includes soak test)

---

## Test 1: Single Instance Guarantee

### Purpose
Verify boot script refuses to start duplicate bridge instance.

### Prerequisites
- Implementation complete (all 4 files modified)
- No bridge currently running

### Test Steps

1. **Initial cleanup**:
```bash
cd /mnt/c/sage/sage-civilization
pkill -f telegram_bridge.py
rm -f .tg_sessions/telegram_bridge.pid
```

2. **First boot (should succeed)**:
```bash
bash tools/acg_telegram_boot.sh
```

3. **Wait for startup**:
```bash
sleep 5
```

4. **Verify single instance**:
```bash
ps auxww | grep telegram_bridge.py | grep -v grep
# Should show EXACTLY ONE process
```

5. **Check PID file**:
```bash
cat .tg_sessions/telegram_bridge.pid
# Should contain a valid PID number
```

6. **Second boot attempt (should FAIL)**:
```bash
bash tools/acg_telegram_boot.sh
echo "Exit code: $?"
# Should be non-zero (failure)
```

7. **Verify error message**:
```bash
# Output should contain:
# "ERROR: Bridge is already running (PID: XXXXX)"
```

8. **Verify still single instance**:
```bash
ps auxww | grep telegram_bridge.py | grep -v grep | wc -l
# Should still be 1
```

### Expected Results

- First boot: SUCCESS (exit code 0)
- Bridge running: 1 process
- PID file created: ✓
- Second boot: FAILED (exit code != 0)
- Error message: "Bridge is already running"
- Process count: Still 1

### Pass Criteria

✓ Second boot refused with error
✓ Single instance maintained
✓ PID file valid
✓ No 409 errors in logs

### Evidence to Collect

```bash
# 1. Process count
ps auxww | grep telegram_bridge.py | grep -v grep | wc -l

# 2. PID file contents
cat .tg_sessions/telegram_bridge.pid

# 3. Boot script output (second attempt)
# Copy error message from terminal

# 4. Log check (no 409 errors)
grep "409 Conflict" /tmp/sage_telegram_bridge.log
# Should return nothing or "no match"
```

### Cleanup After Test

```bash
# Leave bridge running for Test 2
# (Test 2 will test with running instance)
```

---

## Test 2: Stale PID Cleanup

### Purpose
Verify boot script auto-removes stale PID files and starts successfully.

### Prerequisites
- Test 1 complete (bridge currently running)

### Test Steps

1. **Kill bridge process directly (simulate crash)**:
```bash
pkill -9 -f telegram_bridge.py
sleep 2
```

2. **Verify process dead**:
```bash
ps auxww | grep telegram_bridge.py | grep -v grep
# Should show NO processes
```

3. **Verify PID file still exists (stale)**:
```bash
cat .tg_sessions/telegram_bridge.pid
# Should still contain PID from dead process
```

4. **Boot bridge (should detect stale PID and clean up)**:
```bash
bash tools/acg_telegram_boot.sh 2>&1 | tee /tmp/test2_output.txt
```

5. **Check boot script output for stale PID detection**:
```bash
grep "stale PID file" /tmp/test2_output.txt
# Should find message about removing stale PID
```

6. **Verify bridge started successfully**:
```bash
ps auxww | grep telegram_bridge.py | grep -v grep
# Should show ONE process (new instance)
```

7. **Verify new PID file**:
```bash
cat .tg_sessions/telegram_bridge.pid
# Should contain NEW PID (different from old one)
```

8. **Verify new PID matches running process**:
```bash
BRIDGE_PID=$(cat .tg_sessions/telegram_bridge.pid)
ps -p $BRIDGE_PID
# Should show running bridge process
```

### Expected Results

- Process killed: ✓
- Stale PID file detected: ✓
- Stale PID removed: ✓
- Bridge starts successfully: ✓
- New PID file created: ✓
- New PID matches running process: ✓

### Pass Criteria

✓ Stale PID auto-cleaned
✓ Bridge starts successfully after cleanup
✓ New PID file valid
✓ Single instance running

### Evidence to Collect

```bash
# 1. Boot script output showing stale detection
cat /tmp/test2_output.txt | grep -A2 -B2 "stale"

# 2. New PID file
cat .tg_sessions/telegram_bridge.pid

# 3. Process verification
BRIDGE_PID=$(cat .tg_sessions/telegram_bridge.pid)
ps -p $BRIDGE_PID
```

### Cleanup After Test

```bash
# Leave bridge running for Test 3
```

---

## Test 3: 409 Detection in Logs

### Purpose
Verify 409 Conflict errors are logged and detectable by health checks.

### Prerequisites
- Test 2 complete (bridge running cleanly)

### Test Steps

1. **Record current log size**:
```bash
wc -l /tmp/sage_telegram_bridge.log
```

2. **Manually start duplicate bridge (bypass PID check)**:
```bash
# Remove PID file to bypass check, then start duplicate
rm .tg_sessions/telegram_bridge.pid
python3 tools/telegram_bridge.py > /tmp/sage_telegram_bridge_duplicate.log 2>&1 &
DUPLICATE_PID=$!
echo "Started duplicate with PID: $DUPLICATE_PID"
```

3. **Wait for 409 conflict**:
```bash
sleep 30
```

4. **Check for 409 errors in main log**:
```bash
grep -n "409 Conflict" /tmp/sage_telegram_bridge.log
# Should show 409 error entries
```

5. **Check for 409 errors in duplicate log**:
```bash
grep -n "409 Conflict" /tmp/sage_telegram_bridge_duplicate.log
# Should also show 409 errors
```

6. **Verify both instances likely dead**:
```bash
ps auxww | grep telegram_bridge.py | grep -v grep
# May show 0 or zombie processes
```

7. **Run wake-up health check**:
```bash
bash tools/session_wakeup.sh 2>&1 | grep -A5 "Telegram Bridge Health"
# Should detect 409 in logs and warn
```

### Expected Results

- 409 Conflict errors logged: ✓
- Both bridge instances affected: ✓
- Health check detects 409 pattern: ✓
- Warning message shown: ✓

### Pass Criteria

✓ 409 errors present in logs
✓ Health check detects 409 pattern
✓ Wake-up script warns about 409

### Evidence to Collect

```bash
# 1. 409 errors from logs
grep "409 Conflict" /tmp/sage_telegram_bridge.log | head -5

# 2. Health check output
bash tools/session_wakeup.sh 2>&1 | grep -A10 "Telegram Bridge Health"

# 3. Process state
ps auxww | grep telegram_bridge.py | grep -v grep
```

### Cleanup After Test

```bash
# Kill all bridge processes
pkill -9 -f telegram_bridge.py

# Remove PID file
rm -f .tg_sessions/telegram_bridge.pid

# Clean up duplicate log
rm -f /tmp/sage_telegram_bridge_duplicate.log
```

---

## Test 4: Health Check Auto-Recovery

### Purpose
Verify health check script detects dead bridge and auto-restarts.

### Prerequisites
- Test 3 complete (all bridges killed, clean slate)

### Test Steps

1. **Boot bridge cleanly**:
```bash
bash tools/acg_telegram_boot.sh
sleep 5
```

2. **Verify bridge running**:
```bash
BRIDGE_PID=$(cat .tg_sessions/telegram_bridge.pid)
ps -p $BRIDGE_PID
# Should show running process
```

3. **Simulate crash (kill without cleanup)**:
```bash
pkill -9 -f telegram_bridge.py
sleep 2
```

4. **Remove PID file (simulate crash before cleanup)**:
```bash
rm -f .tg_sessions/telegram_bridge.pid
```

5. **Verify bridge dead**:
```bash
ps auxww | grep telegram_bridge.py | grep -v grep
# Should show NO processes
```

6. **Run health check (should auto-recover)**:
```bash
bash tools/telegram_health_check.sh
echo "Health check exit code: $?"
# Should return 1 (indicating restart occurred)
```

7. **Verify bridge restarted**:
```bash
ps auxww | grep telegram_bridge.py | grep -v grep
# Should show ONE process
```

8. **Verify new PID file**:
```bash
cat .tg_sessions/telegram_bridge.pid
# Should exist with new PID
```

9. **Verify bridge functional**:
```bash
tail -10 /tmp/sage_telegram_bridge.log
# Should show recent startup messages
```

### Expected Results

- Bridge killed: ✓
- PID file removed: ✓
- Health check detects dead bridge: ✓
- Auto-restart triggered: ✓
- Exit code 1 (restarted): ✓
- New bridge running: ✓

### Pass Criteria

✓ Dead bridge detected
✓ Auto-restart successful
✓ Exit code = 1 (restarted)
✓ New instance operational

### Evidence to Collect

```bash
# 1. Health check output
# (copy from terminal during step 6)

# 2. New PID
cat .tg_sessions/telegram_bridge.pid

# 3. Bridge log recent activity
tail -20 /tmp/sage_telegram_bridge.log

# 4. Process verification
ps auxww | grep telegram_bridge.py | grep -v grep
```

### Cleanup After Test

```bash
# Leave bridge running (healthy state for production)
```

---

## Test 5: 48-Hour Stability (Workshop Blocker)

### Purpose
Prove bridge can run for 48 continuous hours without 409 Conflict errors.

### Prerequisites
- Tests 1-4 passed
- Bridge running cleanly from Test 4

### Critical Importance

**This test MUST pass before Jan 15 workshop**:
- Workshop: Jan 15-31
- Today: Dec 29
- Days until workshop: 17 days
- Buffer: Plenty of time for re-test if needed

**If this test fails**: Workshop demo could fail catastrophically (Greg's messages not received)

### Test Steps

#### Initial Setup (Hour 0)

1. **Verify clean start**:
```bash
# Restart bridge cleanly
pkill -f telegram_bridge.py
rm -f .tg_sessions/telegram_bridge.pid
bash tools/acg_telegram_boot.sh

# Record start time
date -u +"%Y-%m-%d %H:%M:%S UTC" > /tmp/bridge_stability_test_start.txt
echo "Started at: $(cat /tmp/bridge_stability_test_start.txt)"
```

2. **Baseline measurement**:
```bash
# Record PID
BRIDGE_PID=$(cat .tg_sessions/telegram_bridge.pid)
echo "Bridge PID: $BRIDGE_PID" | tee /tmp/bridge_stability_test.log

# Log file size
wc -l /tmp/sage_telegram_bridge.log >> /tmp/bridge_stability_test.log

# Initial 409 check (should be zero)
grep "409 Conflict" /tmp/sage_telegram_bridge.log | wc -l >> /tmp/bridge_stability_test.log
```

#### Checks Every 6 Hours (8 checkpoints)

**Schedule**: Hour 6, 12, 18, 24, 30, 36, 42, 48

For each checkpoint:

1. **Process verification**:
```bash
echo "=== Checkpoint $(date) ===" >> /tmp/bridge_stability_test.log

# Check PID still running
BRIDGE_PID=$(cat .tg_sessions/telegram_bridge.pid 2>/dev/null)
if ps -p $BRIDGE_PID > /dev/null 2>&1; then
    echo "✓ Bridge still running (PID: $BRIDGE_PID)" >> /tmp/bridge_stability_test.log
else
    echo "❌ FAIL: Bridge dead (PID: $BRIDGE_PID)" >> /tmp/bridge_stability_test.log
    exit 1
fi
```

2. **409 error check**:
```bash
# Check for ANY 409 errors since test start
CONFLICT_COUNT=$(grep "409 Conflict" /tmp/sage_telegram_bridge.log | wc -l)
echo "409 Conflict count: $CONFLICT_COUNT" >> /tmp/bridge_stability_test.log

if [ "$CONFLICT_COUNT" -gt 0 ]; then
    echo "❌ FAIL: Found $CONFLICT_COUNT 409 Conflict errors" >> /tmp/bridge_stability_test.log
    grep "409 Conflict" /tmp/sage_telegram_bridge.log >> /tmp/bridge_stability_test.log
    exit 1
fi
```

3. **Log activity check**:
```bash
# Verify recent log activity (within last 5 minutes)
LAST_LOG=$(tail -1 /tmp/sage_telegram_bridge.log)
echo "Last log: $LAST_LOG" >> /tmp/bridge_stability_test.log
```

4. **Functional test (inbound)**:
```bash
# Send test message via Telegram to Greg's account
# Greg should manually send a test message like "Test checkpoint N"
# Bridge should inject it to tmux

# Verify injection occurred (check tmux buffer)
tmux capture-pane -t sage-session -p | grep "TELEGRAM from" >> /tmp/bridge_stability_test.log
```

5. **Functional test (outbound)**:
```bash
# Send wrapped message from tmux to Telegram
# Greg should verify receipt on Telegram
echo "Wrapped test sent at checkpoint" >> /tmp/bridge_stability_test.log
```

#### Final Verification (Hour 48)

1. **Completion timestamp**:
```bash
date -u +"%Y-%m-%d %H:%M:%S UTC" > /tmp/bridge_stability_test_end.txt
echo "Ended at: $(cat /tmp/bridge_stability_test_end.txt)"
```

2. **Final metrics**:
```bash
echo "=== FINAL RESULTS ===" >> /tmp/bridge_stability_test.log

# Total runtime
START=$(cat /tmp/bridge_stability_test_start.txt)
END=$(cat /tmp/bridge_stability_test_end.txt)
echo "Start: $START" >> /tmp/bridge_stability_test.log
echo "End: $END" >> /tmp/bridge_stability_test.log

# 409 error count (MUST be zero)
FINAL_409_COUNT=$(grep "409 Conflict" /tmp/sage_telegram_bridge.log | wc -l)
echo "Total 409 Conflicts: $FINAL_409_COUNT" >> /tmp/bridge_stability_test.log

# Process status
BRIDGE_PID=$(cat .tg_sessions/telegram_bridge.pid 2>/dev/null)
if ps -p $BRIDGE_PID > /dev/null 2>&1; then
    echo "✓ Bridge still running after 48 hours" >> /tmp/bridge_stability_test.log
else
    echo "❌ Bridge died during test" >> /tmp/bridge_stability_test.log
fi

# Functional tests passed
echo "Functional tests: 8/8 inbound, 8/8 outbound" >> /tmp/bridge_stability_test.log
```

### Expected Results

- 48 hours continuous uptime: ✓
- Zero 409 Conflict errors: ✓
- All 16 functional tests pass (8 inbound, 8 outbound): ✓
- Log shows continuous activity: ✓
- No unexpected restarts: ✓

### Pass Criteria

✓ 48 hours uptime confirmed
✓ Zero 409 errors in logs
✓ 16/16 functional tests passed
✓ Same PID for entire duration
✓ No crashes or restarts

### Fail Conditions

❌ ANY 409 Conflict errors → IMMEDIATE FAIL
❌ Bridge crashes → FAIL
❌ >1 restart during test → FAIL
❌ <16/16 functional tests → FAIL

### If Test Fails

1. **Document failure**:
```bash
# Copy full log
cp /tmp/sage_telegram_bridge.log /tmp/bridge_stability_test_FAILED_$(date +%s).log

# Copy test log
cp /tmp/bridge_stability_test.log /tmp/bridge_stability_test_results_FAILED.log

# Note failure time
echo "Failed at: $(date)" >> /tmp/bridge_stability_test_results_FAILED.log
```

2. **Analyze root cause**:
- What time did failure occur?
- What was happening at that time?
- Were there duplicate starts attempted?
- What do logs show?

3. **Fix and re-test**:
- Address root cause
- Restart 48-hour test
- MUST complete before Jan 15

### Evidence to Collect

```bash
# Final test log
cat /tmp/bridge_stability_test.log

# 409 error count (should be 0)
grep "409 Conflict" /tmp/sage_telegram_bridge.log | wc -l

# Process uptime
BRIDGE_PID=$(cat .tg_sessions/telegram_bridge.pid)
ps -p $BRIDGE_PID -o pid,etime,cmd

# Bridge log excerpt
tail -50 /tmp/sage_telegram_bridge.log
```

---

## Test Summary Report Template

After completing Tests 1-4, tester should create:

### Test Summary

**Date**: [Date]
**Tester**: tester
**Implementation**: [Commit hash]

**Results**:

| Test | Status | Duration | Notes |
|------|--------|----------|-------|
| Test 1: Single Instance | PASS/FAIL | X min | [Any issues] |
| Test 2: Stale PID Cleanup | PASS/FAIL | X min | [Any issues] |
| Test 3: 409 Detection | PASS/FAIL | X min | [Any issues] |
| Test 4: Health Auto-Recovery | PASS/FAIL | X min | [Any issues] |
| Test 5: 48-Hour Stability | PENDING | 48 hrs | [Scheduled start date] |

**Overall**: PASS/FAIL (4/4 required for Test 5 scheduling)

**Recommendations**:
- [Any issues found]
- [Suggestions for improvement]
- [Test 5 scheduling]

**Evidence**:
- [Attach test outputs]
- [Screenshots if relevant]
- [Log excerpts]

---

## Critical Path

**Test 5 is on critical path for workshop**:
- Must complete before Jan 15
- Requires 48 continuous hours
- Cannot overlap with other major work
- Suggest starting Test 5 on Jan 1-2 (gives buffer for re-test if needed)

**If Test 5 fails**:
- Fix root cause immediately
- Re-run Test 5
- Must have passing Test 5 by Jan 10 (5 days before workshop)

---

**Testing protocol complete. Ready for tester execution.**
