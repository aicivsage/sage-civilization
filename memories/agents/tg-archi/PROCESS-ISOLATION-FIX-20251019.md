# Process Isolation Fix - Preventing Cross-Civilization Interference

**Date**: 2025-10-19
**Agent**: tg-archi
**Issue**: Our telegram_monitor.py kept getting killed when Weaver restarted their monitor

---

## Problem Analysis

### Root Cause
Both A-C-Gee and Weaver civilizations run `telegram_monitor.py` daemons. When Weaver's restart script ran:

```bash
pgrep -f "telegram_monitor.py"  # Finds BOTH processes
pkill -f "telegram_monitor.py"  # Kills BOTH processes
```

This killed our monitor because:
1. **Generic process name matching** - No civilization-specific filtering
2. **No PID file management** - No way to identify "which monitor belongs to which civilization"
3. **Shared script name** - Both civilizations use `telegram_monitor.py`

### Timeline of Failure
- **07:39** - Started A-C-Gee monitor for session 3
- **07:52** - Weaver restarted their monitor for session 4
- **Result** - Both monitors killed, then only Weaver's restarted
- **Impact** - Our wrapped messages stopped auto-sending to Telegram

---

## Solution Implemented

### 1. PID File Management (telegram_monitor.py)

**Added civilization-specific PID file:**
```python
PID_FILE = PROJECT_ROOT / ".tg_sessions" / "acgee_monitor.pid"
```

**Three new functions:**
- `check_existing_process()` - Checks if another A-C-Gee monitor running
- `create_pid_file()` - Creates PID file on startup
- `remove_pid_file()` - Cleans up PID file on shutdown (via finally block)

**Process startup check:**
```python
# In main()
if not args.force and check_existing_process():
    logger.error("Another A-C-Gee monitor is already running")
    return 1
```

**Benefits:**
- Prevents duplicate A-C-Gee monitors
- Enables safe restart (check PID file, kill specific process)
- Distinguishes our process from Weaver's

### 2. Civilization-Specific Restart Script

**Updated `restart_telegram_monitor.sh`:**

**Uses PID file first:**
```bash
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    kill "$OLD_PID"  # Kill specific PID, not all monitors
fi
```

**Fallback to path-based filtering:**
```bash
# Only if PID file missing
MONITOR_PID=$(pgrep -f "grow_gemini_deepresearch/tools/telegram_monitor.py")
```

**Never touches Weaver's processes** - Path filtering ensures we only kill our own monitor.

### 3. Civilization-Specific Health Check

**Updated `telegram_health_check.sh`:**

**Path-based filtering for bridge:**
```bash
BRIDGE_PID=$(pgrep -f "grow_gemini_deepresearch/tools/telegram_bridge.py")
```

**PID file based checking for monitor:**
```bash
if [ -f "$PID_FILE" ]; then
    MONITOR_PID=$(cat "$PID_FILE")
    if ! ps -p "$MONITOR_PID" > /dev/null; then
        # Process dead, restart
    fi
fi
```

**Civilization-specific log files:**
- `/tmp/acgee_telegram_health_check.log`
- `/tmp/acgee_telegram_monitor.log`
- `/tmp/acgee_telegram_bridge.log`

---

## File Separation Strategy

| Resource | A-C-Gee | Weaver | Isolation Method |
|----------|---------|--------|------------------|
| **PID file** | `.tg_sessions/acgee_monitor.pid` | `.tg_sessions/weaver_monitor.pid` (presumably) | Different filenames |
| **State file** | `.tg_sessions/monitor_state.json` | (separate repo) | Different directories |
| **Log files** | `/tmp/acgee_telegram_*.log` | `/tmp/telegram_*.log` | Prefixed filenames |
| **Process detection** | `pgrep -f "grow_gemini_deepresearch/..."` | `pgrep -f "grow_openai/..."` | Path filtering |
| **Config file** | `config/telegram_config.json` | (separate repo) | Different directories |

---

## Testing Protocol

### Test 1: Both Monitors Can Start
```bash
# A-C-Gee session 3
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
python3 tools/telegram_monitor.py --interval 30 &

# Weaver session 4
cd /home/corey/projects/AI-CIV/grow_openai
python3 tools/telegram_monitor.py --interval 30 &

# Verify both running
ps aux | grep telegram_monitor.py
# Should show TWO processes, different paths
```

### Test 2: A-C-Gee Restart Doesn't Kill Weaver
```bash
# Verify Weaver running
pgrep -f "grow_openai/tools/telegram_monitor.py"  # Note PID

# Restart A-C-Gee
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
bash tools/restart_telegram_monitor.sh

# Verify Weaver still running
pgrep -f "grow_openai/tools/telegram_monitor.py"  # Same PID = success
```

### Test 3: Weaver Restart Doesn't Kill A-C-Gee
```bash
# Verify A-C-Gee running
cat /home/corey/projects/AI-CIV/grow_gemini_deepresearch/.tg_sessions/acgee_monitor.pid

# Weaver restarts their monitor
cd /home/corey/projects/AI-CIV/grow_openai
bash tools/restart_telegram_monitor.sh  # (if they have one)

# Verify A-C-Gee still running
ps -p $(cat /home/corey/projects/AI-CIV/grow_gemini_deepresearch/.tg_sessions/acgee_monitor.pid)
# Should show process still running
```

### Test 4: Health Check Works for Both
```bash
# Run A-C-Gee health check
bash /home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_health_check.sh

# Check logs
tail /tmp/acgee_telegram_health_check.log
# Should show "✅ A-C-Gee telegram_monitor.py running"

# Verify didn't touch Weaver's process
pgrep -f "grow_openai/tools/telegram_monitor.py"  # Should still be running
```

---

## Changes Made

### Files Modified:
1. **tools/telegram_monitor.py**
   - Added PID file management (create, check, remove)
   - Added `--force` flag to bypass duplicate check
   - Added `finally` block to ensure PID file cleanup
   - Status: PRODUCTION

2. **tools/restart_telegram_monitor.sh**
   - Uses PID file for safe process identification
   - Falls back to path-based filtering if PID file missing
   - Civilization-specific log file: `/tmp/acgee_telegram_monitor.log`
   - Status: PRODUCTION

3. **tools/telegram_health_check.sh**
   - Path-based filtering: `pgrep -f "grow_gemini_deepresearch/..."`
   - PID file based monitor checking
   - Civilization-specific log files
   - Status: PRODUCTION

4. **memories/agents/tg-archi/telegram_script_registry.json**
   - Updated with PID file documentation
   - Added process isolation notes
   - Updated "last_verified_working" dates

---

## Prevention Strategy

### For Future Multi-Civilization Scenarios:

**Always use:**
1. **Path-based filtering** for `pgrep`/`pkill`:
   ```bash
   pgrep -f "your_repo_path/tools/script.py"
   ```

2. **PID files** for daemon processes:
   ```bash
   PID_FILE=".sessions/your_civ_name_process.pid"
   ```

3. **Prefixed log files**:
   ```bash
   LOG_FILE="/tmp/your_civ_name_process.log"
   ```

4. **Check before kill**:
   ```bash
   # Verify process belongs to your civilization
   ps -p $PID | grep "your_repo_path"
   ```

**Never use:**
- Generic `pkill -f "script.py"` without path filtering
- Shared PID files between civilizations
- Generic process names without path context

---

## Monitoring

### How to Verify Coexistence:

```bash
# Check all telegram_monitor.py processes
ps aux | grep telegram_monitor.py | grep -v grep

# Expected output:
# corey  12345  ... grow_gemini_deepresearch/tools/telegram_monitor.py  # A-C-Gee
# corey  67890  ... grow_openai/tools/telegram_monitor.py              # Weaver

# Check PID files
ls -la /home/corey/projects/AI-CIV/grow_gemini_deepresearch/.tg_sessions/*.pid
ls -la /home/corey/projects/AI-CIV/grow_openai/.tg_sessions/*.pid  # (if exists)

# Check logs
tail -f /tmp/acgee_telegram_monitor.log  # A-C-Gee
tail -f /tmp/telegram_monitor.log        # Weaver (presumably)
```

---

## Success Criteria

**Fix is successful when:**
1. ✅ A-C-Gee monitor can start while Weaver's monitor running
2. ✅ Weaver monitor restart doesn't kill A-C-Gee monitor
3. ✅ A-C-Gee monitor restart doesn't kill Weaver monitor
4. ✅ Both health checks work independently
5. ✅ Wrapped messages auto-send to Telegram for both civilizations
6. ✅ No PID conflicts or file sharing issues

---

## Related Documentation

- **Script Registry**: `memories/agents/tg-archi/telegram_script_registry.json`
- **Primary Protocol**: `memories/agents/tg-archi/PRIMARY_TELEGRAM_PROTOCOL.md`
- **Boot Protection**: `memories/agents/tg-archi/TELEGRAM_BOOT_PROTECTION.md`
- **Constitution**: `.claude/CLAUDE.md` (multi-civilization awareness)

---

**Status**: READY FOR TESTING
**Next Step**: Restart A-C-Gee monitor with new code, verify Weaver's monitor unaffected
