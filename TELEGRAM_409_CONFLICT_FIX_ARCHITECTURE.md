# Telegram Bridge 409 Conflict Fix - Architecture Design

**Date**: 2025-12-29
**Agent**: architect
**Priority**: CRITICAL (Workshop blocker - Jan 15-31)
**Status**: Design complete, ready for implementation

---

## Executive Summary

**Problem**: Telegram bridge crashes with 409 Conflict errors when multiple instances poll the Telegram Bot API simultaneously. This causes complete inbound message failure.

**Impact**: Greg's messages not received during workshop demo = CATASTROPHIC

**Solution**: Multi-layered defense:
1. **PID file locking** - Prevent duplicate starts (industry standard)
2. **Process verification** - Validate single instance before starting
3. **409 detection** - Log and alert on conflicts
4. **Health monitoring** - Auto-detect and recover from failures
5. **Wake-up integration** - Proactive health checks on session start

**Timeline**: 2 hours active work + 48-hour stability test before workshop

**Confidence**: HIGH - Using proven industry-standard patterns

---

## Root Cause Analysis

### The 409 Conflict Error

**Telegram Bot API Behavior**:
- Only ONE client can call `getUpdates` at a time per bot token
- If duplicate polling detected → HTTP 409 Conflict
- Conflict kills BOTH/ALL polling instances
- Messages remain in queue but not delivered
- No automatic recovery

**Evidence from Dec 28-29**:
```
2025-12-28 18:05:49 - ERROR - Conflict: terminated by other getUpdates request
[Bridge log stops completely - no activity Dec 29]
```

**Why Duplicates Happen**:
1. Boot script runs twice (manual re-run while already running)
2. Previous instance not killed before new start
3. Process survives `pkill` (zombie, permissions, etc.)
4. No duplicate detection before starting
5. WSL environment oddities (process cleanup issues)

**Current State**:
- Outbound (monitor) working ✅
- Inbound (bridge) BROKEN ❌
- One-way communication = trust failure

---

## Architectural Solution

### Strategy 1: PID File Locking (PRIMARY DEFENSE)

**Industry Standard Pattern**:
- Single source of truth: `.tg_sessions/telegram_bridge.pid`
- Write PID on successful start
- Check PID file before starting (fail-fast if occupied)
- Validate PID is actually running (detect stale files)
- Auto-cleanup on graceful shutdown

**Benefits**:
- Prevents accidental duplicate starts
- Survives process crashes (stale PID detection)
- Simple, proven pattern (used by nginx, apache, etc.)

**Implementation**:
```python
# In telegram_bridge.py main():
1. Check PID file exists
2. If exists: Verify PID is running
3. If running: FAIL with error, refuse to start
4. If stale: Remove PID file, proceed
5. Create PID file with current PID
6. On shutdown: Remove PID file
```

### Strategy 2: Process Name Verification (DEFENSE IN DEPTH)

**Already Implemented**:
- Process named `ACG_telegram_bridge` via setproctitle
- Distinguishes from Weaver's processes

**Additional Verification**:
- Boot script counts running instances
- Fail if count != 1 after start
- Double-check with `ps aux | grep ACG_telegram_bridge | wc -l`

### Strategy 3: 409 Detection & Logging (FAIL-SAFE)

**Detection**:
- Bridge already logs 409 errors
- Health check scans logs for 409 patterns
- Wake-up protocol alerts if 409 detected

**Recovery**:
- Health check auto-restarts on 409
- Forces clean PID file removal
- Logs 409 occurrence for post-mortem

### Strategy 4: Health Monitoring (PROACTIVE)

**Wake-Up Protocol Integration**:
- Check bridge PID file exists
- Verify PID is running
- Check log timestamp (<60s old = healthy)
- Scan for 409 errors in recent logs
- Alert if any issues found

**Auto-Recovery Script**:
- `telegram_health_check.sh` runs diagnostics
- Detects dead/409'd bridge
- Auto-restarts via boot script
- Returns status code (0=healthy, 1=restarted, 2=failed)

---

## Implementation Specification

### File 1: `tools/telegram_bridge.py`

**Changes Required**:

1. **Add PID file constant** (after SESSION_DIR definition):
```python
PID_FILE = SESSION_DIR / "telegram_bridge.pid"
```

2. **Add PID checking function** (before main()):
```python
def check_pid_file() -> bool:
    """
    Check if another bridge instance is running via PID file.

    Returns:
        True if another instance is running (should not start)
        False if safe to start
    """
    if not PID_FILE.exists():
        return False  # No PID file, safe to start

    try:
        with open(PID_FILE, 'r') as f:
            old_pid = int(f.read().strip())

        # Check if process is still running
        try:
            os.kill(old_pid, 0)  # Signal 0 checks existence without killing
            logger.error(f"Another bridge instance is already running (PID: {old_pid})")
            logger.error(f"PID file: {PID_FILE}")
            logger.error(f"Refusing to start duplicate instance")
            return True  # Process is running, fail-fast
        except OSError:
            # Process doesn't exist, stale PID file
            logger.warning(f"Found stale PID file (PID {old_pid} not running)")
            PID_FILE.unlink()
            logger.info(f"Removed stale PID file")
            return False  # Safe to start
    except Exception as e:
        logger.error(f"Error checking PID file: {e}")
        return False  # On error, allow start (fail-open for recovery)
```

3. **Add PID creation function**:
```python
def create_pid_file():
    """Create PID file with current process ID."""
    try:
        PID_FILE.parent.mkdir(exist_ok=True)
        with open(PID_FILE, 'w') as f:
            f.write(str(os.getpid()))
        logger.info(f"Created PID file: {PID_FILE} (PID: {os.getpid()})")
    except Exception as e:
        logger.error(f"Failed to create PID file: {e}")
        raise  # Fail-loud: PID file creation is critical
```

4. **Add PID cleanup function**:
```python
def remove_pid_file():
    """Remove PID file on shutdown."""
    try:
        if PID_FILE.exists():
            PID_FILE.unlink()
            logger.info("Removed PID file")
    except Exception as e:
        logger.warning(f"Failed to remove PID file: {e}")
```

5. **Modify main() function**:
```python
def main():
    global bridge

    # Set process name (already exists)
    try:
        import setproctitle
        setproctitle.setproctitle("ACG_telegram_bridge")
    except ImportError:
        pass

    # ===== NEW: CHECK PID FILE FIRST (CRITICAL) =====
    if check_pid_file():
        logger.error("Exiting due to duplicate instance detection")
        return 1

    logger.info("Starting Telegram Bridge...")

    # Load configuration (existing code)
    try:
        config = load_config()
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        logger.error("See docs/TELEGRAM_SETUP.md for setup instructions")
        return 1

    # Initialize bridge (existing code)
    bridge = TelegramBridge(config)
    logger.info(f"Bridge initialized for tmux session: {bridge.tmux_pane}")

    # ===== NEW: CREATE PID FILE (CRITICAL) =====
    create_pid_file()

    # Create application (existing code)
    application = Application.builder().token(config["bot_token"]).build()

    # Register handlers (existing code)
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    # Start bot (existing code)
    logger.info("Starting bot polling...")
    logger.info(f"Authorized users: {list(bridge.authorized_users.keys())}")

    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        return 1
    finally:
        # ===== NEW: CLEANUP PID FILE (CRITICAL) =====
        remove_pid_file()

    return 0
```

6. **Add missing import** (at top of file):
```python
import os  # Already exists
```

**Testing**:
- Test 1: Single instance guarantee
- Test 2: Stale PID cleanup

---

### File 2: `tools/acg_telegram_boot.sh`

**Changes Required**:

1. **Add PID file check** (after Step 2, before Step 3):

```bash
# Step 2.5: Check for existing bridge PID file
echo "Step 2.5: Checking for existing bridge instance..."
BRIDGE_PID_FILE=".tg_sessions/telegram_bridge.pid"

if [ -f "$BRIDGE_PID_FILE" ]; then
    EXISTING_PID=$(cat "$BRIDGE_PID_FILE" 2>/dev/null)
    echo "  Found PID file with PID: $EXISTING_PID"

    # Check if process is actually running
    if ps -p "$EXISTING_PID" > /dev/null 2>&1; then
        echo "❌ ERROR: Bridge is already running (PID: $EXISTING_PID)"
        echo "   PID file: $BRIDGE_PID_FILE"
        echo "   To force restart, run: pkill -f telegram_bridge.py && rm $BRIDGE_PID_FILE && bash tools/acg_telegram_boot.sh"
        exit 1
    else
        echo "  PID $EXISTING_PID not running (stale PID file)"
        echo "  Removing stale PID file..."
        rm -f "$BRIDGE_PID_FILE"
    fi
else
    echo "  No existing PID file found"
fi
echo ""
```

2. **Add post-start verification** (after Step 3, bridge start):

```bash
# Step 3.5: Verify PID file created and single instance
echo "Step 3.5: Verifying single bridge instance..."
sleep 1  # Give bridge time to create PID file

if [ ! -f "$BRIDGE_PID_FILE" ]; then
    echo "⚠️  WARNING: PID file not created by bridge"
    echo "   Expected: $BRIDGE_PID_FILE"
fi

# Count running bridge instances
BRIDGE_COUNT=$(ps auxww | grep "telegram_bridge.py" | grep -v grep | wc -l)
if [ "$BRIDGE_COUNT" -ne 1 ]; then
    echo "❌ ERROR: Expected 1 bridge instance, found $BRIDGE_COUNT"
    ps auxww | grep "telegram_bridge.py" | grep -v grep
    exit 1
else
    echo "✓ Single bridge instance verified"
fi
echo ""
```

**Testing**:
- Test 1: Single instance guarantee (second boot fails)
- Test 2: Stale PID cleanup (auto-removes dead PID)

---

### File 3: `tools/session_wakeup.sh`

**Changes Required**:

Add new section after existing checks, before final output:

```bash
# === TELEGRAM BRIDGE HEALTH CHECK ===
echo ""
echo "=== Telegram Bridge Health ==="

BRIDGE_PID_FILE="/mnt/c/sage/sage-civilization/.tg_sessions/telegram_bridge.pid"
BRIDGE_LOG="/tmp/sage_telegram_bridge.log"

# Check PID file
if [ -f "$BRIDGE_PID_FILE" ]; then
    BRIDGE_PID=$(cat "$BRIDGE_PID_FILE" 2>/dev/null)
    echo "PID file: $BRIDGE_PID"

    # Verify process running
    if ps -p "$BRIDGE_PID" > /dev/null 2>&1; then
        echo "Process: ✓ RUNNING"
    else
        echo "Process: ❌ NOT RUNNING (stale PID file)"
        echo "⚠️  WARNING: Bridge appears dead, run health check to restart"
    fi
else
    echo "PID file: ❌ NOT FOUND"
    echo "⚠️  WARNING: Bridge not running, run acg_telegram_boot.sh"
fi

# Check log timestamp
if [ -f "$BRIDGE_LOG" ]; then
    LAST_LOG_LINE=$(tail -1 "$BRIDGE_LOG" 2>/dev/null)
    echo "Last log: ${LAST_LOG_LINE:0:80}..."

    # Check for 409 Conflict errors
    if tail -50 "$BRIDGE_LOG" 2>/dev/null | grep -q "409 Conflict"; then
        echo "🚨 ALERT: 409 Conflict errors detected in recent logs!"
        echo "         Multiple bridge instances were running (now likely dead)"
        echo "         Run health check to restart cleanly"
    fi
else
    echo "Log file: ❌ NOT FOUND"
fi

echo ""
```

**Testing**:
- Test 5: Wake-up detects dead bridge

---

### File 4: `tools/telegram_health_check.sh`

**Create new file** with following content:

```bash
#!/bin/bash
# Telegram Bridge Health Check & Auto-Recovery
# Returns: 0=healthy, 1=restarted, 2=failed

echo "=== Telegram Bridge Health Check ==="
echo ""

BRIDGE_PID_FILE=".tg_sessions/telegram_bridge.pid"
BRIDGE_LOG="/tmp/sage_telegram_bridge.log"
HEALTHY=true

# Check PID file
if [ -f "$BRIDGE_PID_FILE" ]; then
    BRIDGE_PID=$(cat "$BRIDGE_PID_FILE" 2>/dev/null)
    echo "PID file found: $BRIDGE_PID"

    # Check if process running
    if ps -p "$BRIDGE_PID" > /dev/null 2>&1; then
        echo "Process status: ✓ RUNNING"
    else
        echo "Process status: ❌ DEAD (PID $BRIDGE_PID not found)"
        HEALTHY=false
    fi
else
    echo "PID file: ❌ NOT FOUND (bridge not running)"
    HEALTHY=false
fi

# Check for 409 errors in recent logs
if [ -f "$BRIDGE_LOG" ]; then
    if tail -50 "$BRIDGE_LOG" 2>/dev/null | grep -q "409 Conflict"; then
        echo "🚨 ALERT: 409 Conflict detected in recent logs"
        echo "         Multiple instances were running - bridge likely dead"
        HEALTHY=false
    fi
fi

# If unhealthy, attempt recovery
if [ "$HEALTHY" = false ]; then
    echo ""
    echo "=== ATTEMPTING AUTO-RECOVERY ==="

    # Kill any existing bridge processes
    echo "1. Killing any existing bridge processes..."
    pkill -f "telegram_bridge.py" 2>/dev/null
    sleep 2

    # Remove stale PID file
    echo "2. Removing stale PID file..."
    rm -f "$BRIDGE_PID_FILE"

    # Restart via boot script
    echo "3. Restarting bridge via boot script..."
    bash tools/acg_telegram_boot.sh

    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ Recovery successful - bridge restarted"
        exit 1  # Return 1 to indicate restart occurred
    else
        echo ""
        echo "❌ Recovery failed - manual intervention required"
        exit 2  # Return 2 to indicate failure
    fi
else
    echo ""
    echo "✓ Bridge is healthy"
    exit 0  # Return 0 to indicate healthy
fi
```

**Make executable**:
```bash
chmod +x tools/telegram_health_check.sh
```

**Testing**:
- Test 4: Health check auto-recovery

---

## Testing Protocol

### Test 1: Single Instance Guarantee

**Purpose**: Verify boot script refuses to start duplicate bridge

**Steps**:
1. `cd /mnt/c/sage/sage-civilization`
2. `bash tools/acg_telegram_boot.sh` (first boot)
3. Wait 5 seconds
4. `bash tools/acg_telegram_boot.sh` (second boot attempt)

**Expected Results**:
- Second boot exits with error code != 0
- Error message: "Bridge is already running (PID: XXXXX)"
- Only ONE `telegram_bridge.py` process in `ps aux`
- PID file contains valid PID

**Pass Criteria**:
- ✓ Second boot refused
- ✓ Single instance verified
- ✓ No 409 errors in logs

---

### Test 2: Stale PID Cleanup

**Purpose**: Verify boot script auto-cleans stale PID files

**Steps**:
1. `cd /mnt/c/sage/sage-civilization`
2. `echo '99999' > .tg_sessions/telegram_bridge.pid`
3. `bash tools/acg_telegram_boot.sh`
4. `cat .tg_sessions/telegram_bridge.pid`

**Expected Results**:
- Boot script detects PID 99999 is not running
- Logs: "PID 99999 not running (stale PID file)"
- Removes stale PID file
- Bridge starts successfully
- New PID file created with actual PID

**Pass Criteria**:
- ✓ Stale PID auto-cleaned
- ✓ Bridge starts successfully
- ✓ New PID file matches running process

---

### Test 3: 409 Detection in Logs

**Purpose**: Verify 409 errors are logged and detectable

**Steps**:
1. Boot bridge normally
2. Manually start duplicate: `python3 tools/telegram_bridge.py &`
3. Wait 30 seconds
4. `grep '409 Conflict' /tmp/sage_telegram_bridge.log`

**Expected Results**:
- Bridge log shows 409 Conflict errors
- Both bridge instances likely dead
- Wake-up script detects 409 in health check

**Pass Criteria**:
- ✓ 409 errors logged
- ✓ Health check detects 409 pattern

---

### Test 4: Health Check Auto-Recovery

**Purpose**: Verify health check restarts dead bridge

**Steps**:
1. Boot bridge normally
2. Kill bridge: `pkill -9 -f telegram_bridge.py`
3. Remove PID: `rm .tg_sessions/telegram_bridge.pid`
4. `bash tools/telegram_health_check.sh`

**Expected Results**:
- Health check detects dead bridge
- Auto-restarts via boot script
- Returns exit code 1 (restarted)
- New bridge instance running

**Pass Criteria**:
- ✓ Dead bridge detected
- ✓ Auto-restart successful
- ✓ New PID file created

---

### Test 5: 48-Hour Stability (WORKSHOP BLOCKER)

**Purpose**: Prove bridge can run for 48 hours without 409 errors

**Steps**:
1. Boot bridge cleanly
2. Run for 48 continuous hours
3. Every 6 hours:
   - `grep '409 Conflict' /tmp/sage_telegram_bridge.log`
   - `tail -5 /tmp/sage_telegram_bridge.log` (verify recent activity)
   - Send test message via Telegram
   - Send test wrapped message from tmux
4. After 48 hours: Final verification

**Expected Results**:
- Zero 409 Conflict errors over 48 hours
- Continuous uptime (no unexpected restarts)
- All message tests pass (8 inbound, 8 outbound)
- Bridge log shows continuous activity

**Pass Criteria**:
- ✓ 48 hours uptime
- ✓ Zero 409 errors
- ✓ 100% message delivery success

**Critical for Workshop**: This test MUST pass before Jan 15

---

## Timeline

| Phase | Duration | Task | Owner |
|-------|----------|------|-------|
| 1 | 30 min | Architecture design | architect (THIS TASK) ✓ |
| 2 | 45 min | Code implementation | coder |
| 3 | 15 min | Tests 1-4 execution | tester |
| 4 | 48 hours | Test 5 stability soak | automated |
| 5 | 30 min | Verification & sign-off | Primary |

**Total Active Time**: ~2 hours
**Total Calendar Time**: 48+ hours (due to soak test)

**Workshop Deadline**: Jan 15 (17 days from now)
**Buffer**: Plenty of time for fixes if needed

---

## Success Criteria

### Workshop Readiness Checklist

- [ ] Zero 409 Conflict errors in 48-hour stability test
- [ ] Single instance guarantee enforced (Test 1 passes)
- [ ] Stale PID auto-cleanup working (Test 2 passes)
- [ ] 409 detection in logs (Test 3 passes)
- [ ] Health monitoring detects failures (Test 4 passes)
- [ ] Auto-recovery restarts dead bridge (Test 4 passes)
- [ ] Wake-up protocol integrated (health check added)

### Production Confidence

- [ ] Cannot accidentally start duplicate bridge
- [ ] Survives process crashes (PID cleanup on restart)
- [ ] Detects 409 conflicts in logs
- [ ] Wake-up protocol catches dead bridge
- [ ] Health check auto-restarts failed bridge
- [ ] 48-hour continuous operation proven

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Test 5 fails (409 during soak) | Medium | HIGH | Run 2 soak tests in parallel, fix if patterns emerge |
| PID file permissions issue | Low | Medium | Use .tg_sessions/ dir (already used, tested) |
| Process name check unreliable | Low | Low | PID file is primary, process name is defense-in-depth |
| Health check too aggressive | Low | Medium | Only restart if PID missing OR 409 detected |

---

## Handoff to Implementation

**Next Agent**: coder

**Task**: Implement PID locking in 4 files per specification above

**Files to Modify**:
1. `tools/telegram_bridge.py` - Add PID checking/creation/cleanup
2. `tools/acg_telegram_boot.sh` - Add PID verification steps
3. `tools/session_wakeup.sh` - Add health check section
4. `tools/telegram_health_check.sh` - Create new auto-recovery script

**Estimated Time**: 45 minutes

**Testing**: tester runs Tests 1-4 after implementation

**Critical Path**: Test 5 (48-hour soak) blocks workshop readiness

---

## Memory Update

**After completion, tg-archi should update**:
- `memories/agents/tg-archi/CRITICAL-telegram-bridge-failure-20251229.md` - Add fix applied
- `memories/agents/tg-archi/telegram-409-fix-architecture-20251229.md` - This document
- `memories/agents/tg-archi/telegram-409-fix-implementation-20251229.md` - Coder's work
- `memories/agents/tg-archi/telegram-409-fix-testing-20251229.md` - Tester's results

---

**Architecture design complete. Ready for coder.**
