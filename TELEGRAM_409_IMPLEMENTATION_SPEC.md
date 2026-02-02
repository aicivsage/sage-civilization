# Telegram Bridge 409 Fix - Implementation Spec for Coder

**Date**: 2025-12-29
**Agent**: architect → coder
**Architecture**: See `TELEGRAM_409_CONFLICT_FIX_ARCHITECTURE.md`
**Estimated Time**: 45 minutes

---

## Quick Context

**Problem**: Multiple bridge instances cause 409 Conflict, kill all instances
**Solution**: PID file locking prevents duplicate starts
**Files to modify**: 4 files (details below)

---

## File 1: `tools/telegram_bridge.py`

### Step 1: Add PID file constant

**Location**: After line 62 (SESSION_DIR definition)

**Add**:
```python
PID_FILE = SESSION_DIR / "telegram_bridge.pid"
```

### Step 2: Add check_pid_file() function

**Location**: Before main() function (around line 439)

**Add**:
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

### Step 3: Add create_pid_file() function

**Location**: After check_pid_file()

**Add**:
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

### Step 4: Add remove_pid_file() function

**Location**: After create_pid_file()

**Add**:
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

### Step 5: Modify main() function

**Location**: Line 439-491

**Changes**:

1. **After setproctitle block** (line 448), add:
```python
    # CHECK PID FILE FIRST (CRITICAL - prevents 409 conflicts)
    if check_pid_file():
        logger.error("Exiting due to duplicate instance detection")
        return 1
```

2. **After bridge initialization** (line 463), add:
```python
    # CREATE PID FILE (CRITICAL - marks this instance as running)
    create_pid_file()
```

3. **In finally block** (after line 485), add:
```python
    finally:
        # CLEANUP PID FILE (CRITICAL - allows restart)
        remove_pid_file()
```

**Complete modified main()** should look like:
```python
def main():
    global bridge

    # Set process name to distinguish from Weaver's processes
    try:
        import setproctitle
        setproctitle.setproctitle("ACG_telegram_bridge")
    except ImportError:
        pass  # setproctitle not available, skip naming

    # CHECK PID FILE FIRST (NEW - prevents 409 conflicts)
    if check_pid_file():
        logger.error("Exiting due to duplicate instance detection")
        return 1

    logger.info("Starting A-C-Gee Telegram Bridge (Phase 1 MVP)")

    # Load configuration
    try:
        config = load_config()
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        logger.error("See docs/TELEGRAM_SETUP.md for setup instructions")
        return 1

    # Initialize bridge
    bridge = TelegramBridge(config)
    logger.info(f"Bridge initialized for tmux session: {bridge.tmux_pane}")

    # CREATE PID FILE (NEW - marks this instance as running)
    create_pid_file()

    # Create application
    application = Application.builder().token(config["bot_token"]).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    # Start bot
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
        # CLEANUP PID FILE (NEW - allows restart)
        remove_pid_file()

    return 0
```

**Note**: `os` module already imported at top of file (line 37)

---

## File 2: `tools/acg_telegram_boot.sh`

### Change 1: Add PID file check

**Location**: After Step 2 (line 84), before Step 3

**Insert**:
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

### Change 2: Add post-start verification

**Location**: After Step 3 (bridge start, line 98), before Step 4

**Insert**:
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

---

## File 3: `tools/session_wakeup.sh`

### Change: Add health check section

**Location**: Near end of file, before final output

**Insert**:
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

---

## File 4: `tools/telegram_health_check.sh` (NEW FILE)

### Create new file

**Create**: `tools/telegram_health_check.sh`

**Content**:
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

### Make executable

**After creating file, run**:
```bash
chmod +x tools/telegram_health_check.sh
```

---

## Implementation Checklist

- [ ] File 1: Add PID_FILE constant
- [ ] File 1: Add check_pid_file() function
- [ ] File 1: Add create_pid_file() function
- [ ] File 1: Add remove_pid_file() function
- [ ] File 1: Modify main() - add PID check at start
- [ ] File 1: Modify main() - add PID create after init
- [ ] File 1: Modify main() - add PID cleanup in finally
- [ ] File 2: Add Step 2.5 (PID file check)
- [ ] File 2: Add Step 3.5 (post-start verification)
- [ ] File 3: Add health check section
- [ ] File 4: Create telegram_health_check.sh
- [ ] File 4: Make executable (chmod +x)

---

## Testing After Implementation

**Invoke tester with**:
```
Task(tester):
  Run Tests 1-4 from TELEGRAM_409_CONFLICT_FIX_ARCHITECTURE.md
  Verify:
    - Test 1: Single instance guarantee (second boot fails)
    - Test 2: Stale PID cleanup (auto-removes dead PID)
    - Test 3: 409 detection in logs (errors logged)
    - Test 4: Health check auto-recovery (dead bridge restarts)
  Report pass/fail for each test with evidence
```

**Test 5** (48-hour stability) runs separately before workshop.

---

## Common Issues & Solutions

**Issue**: PID file permissions error
**Solution**: .tg_sessions/ already exists and is writable, should not occur

**Issue**: os.kill() not available on Windows WSL
**Solution**: WSL has full Linux syscalls, os.kill(pid, 0) works

**Issue**: Process survives check_pid_file()
**Solution**: os.kill(pid, 0) is definitive - if returns, process exists

**Issue**: Boot script can't write PID file variable
**Solution**: Variable is local to script, no conflicts

---

## Handoff to Tester

**After implementation complete**:

1. Commit changes with message: "Fix: Add PID locking to prevent 409 Conflict errors"
2. Invoke tester for Tests 1-4
3. If all pass → Schedule Test 5 (48-hour soak)
4. If failures → Debug and re-test

**Critical**: Test 5 must complete before Jan 15 workshop deadline

---

**Implementation spec complete. Ready for coding.**
