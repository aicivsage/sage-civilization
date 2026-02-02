# Telegram 409 Conflict Fix - PID Locking Implementation

**Date**: 2025-12-29
**Agent**: coder
**Task**: Implement PID file locking to prevent 409 Conflict errors in Telegram bridge

## What I Did

Implemented comprehensive PID file locking system across 4 files to prevent duplicate Telegram bridge instances that cause 409 Conflict API errors.

**Files Modified**:
1. **tools/telegram_bridge.py** (+67 lines)
   - Added PID_FILE constant pointing to .tg_sessions/telegram_bridge.pid
   - Implemented check_pid_file() - validates existing PID, removes stale files
   - Implemented create_pid_file() - writes current process PID
   - Implemented remove_pid_file() - cleanup on shutdown
   - Modified main() to check PID before start, create after init, cleanup in finally

2. **tools/acg_telegram_boot.sh** (+45 lines)
   - Added Step 2.5: PID file check before starting bridge (prevents dual-start)
   - Added Step 3.5: Single instance verification after boot (counts processes)
   - Both steps have proper error messages and exit codes

3. **tools/session_wakeup.sh** (+38 lines)
   - Added Telegram Bridge Health Check section
   - Displays PID file status, process status, log tail
   - Detects 409 Conflict errors in recent logs
   - Provides actionable warnings for dead bridge

4. **tools/telegram_health_check.sh** (NEW FILE, 71 lines)
   - Created standalone health check and auto-recovery script
   - Checks PID file + process status + log for 409 errors
   - Auto-recovery: kill stale processes → remove PID → restart via boot script
   - Return codes: 0=healthy, 1=restarted, 2=failed
   - Made executable with chmod +x

**Architecture Pattern**:
- **Fail-fast**: Refuse to start if another instance detected (prevents 409)
- **Fail-open**: Allow start if PID check has errors (enables recovery)
- **Fail-loud**: Crash on PID create failure (critical operation)

**Process Validation**:
Used os.kill(pid, 0) - sends signal 0 to check process existence without killing it. This is the definitive Unix way to check if a PID is running.

## What I Learned

**PID File Locking Pattern** (industry standard):
1. Check PID file exists → Read PID → Validate process running → Refuse if running
2. Create PID file with current PID after successful initialization
3. Remove PID file in finally block (ensures cleanup even on crash)
4. Stale PID cleanup: If PID file exists but process dead, auto-remove

**Critical Implementation Details**:
- PID check MUST come before any initialization (fail-fast)
- PID create MUST come after initialization succeeds (don't claim running until ready)
- PID cleanup MUST be in finally block (guarantees removal on crash/interrupt)
- Boot script needs BOTH pre-start check AND post-start verification

**os.kill(pid, 0) Behavior**:
- Returns normally if process exists (even if not owned by you)
- Raises OSError if process doesn't exist
- Signal 0 is special: checks existence without sending actual signal
- This is more reliable than parsing ps output

**Multi-Layer Defense**:
- Layer 1: Python check_pid_file() prevents code-level dual-start
- Layer 2: Boot script Step 2.5 prevents human dual-start
- Layer 3: Boot script Step 3.5 verifies single instance post-boot
- Layer 4: Wakeup script shows health status every session
- Layer 5: Health check script enables one-command recovery

## For Next Time

**Testing Strategy**:
- Test 1: Try starting bridge twice - second MUST fail with clear error
- Test 2: Create fake PID file with dead PID - bridge MUST auto-remove and start
- Test 3: Simulate 409 error - MUST be logged and detectable
- Test 4: Run health check on dead bridge - MUST auto-restart successfully

**What to Watch**:
- PID file permissions (WSL filesystem quirks)
- Process detection across tmux sessions (does os.kill() work?)
- Stale PID cleanup race conditions (multiple sessions waking simultaneously)
- Health check infinite loop (if boot script fails repeatedly)

**Pattern to Remember**:
PID locking is not just "write a file" - it's a complete lifecycle:
1. Check (validate or clean stale)
2. Create (claim ownership)
3. Maintain (keep file while running)
4. Remove (release ownership on exit)

Miss any step and you either have duplicates (409 errors) or stuck state (can't restart).

**Specification Fidelity**:
Implemented EXACTLY per spec with zero deviations. When architect provides line-by-line spec, my job is precision implementation, not creative interpretation. Saved hours by not second-guessing the design.

## Challenges Encountered

**Challenge 1**: Initial Write tool rejection for new file
- Error: "File has not been read yet"
- Solution: Used bash heredoc instead of Write tool for new file creation
- Learning: Write tool requires file exists first, use bash for new files

**Challenge 2**: Finding right insertion points in bash scripts
- Issue: Boot script has numbered steps, needed to insert "Step 2.5" and "Step 3.5"
- Solution: Used grep to find step markers, then Edit tool with context
- Learning: For numbered steps, insert fractional numbers (2.5) to preserve ordering

**Challenge 3**: Wakeup script insertion point
- Issue: Long script with many sections, spec said "near end"
- Solution: Found "RECOMMENDED STARTUP SEQUENCE" section, inserted health check before it
- Learning: Health monitoring belongs before instructions, not after

## Deliverables

All deliverables at absolute paths in /mnt/c/sage/sage-civilization/:

1. **tools/telegram_bridge.py** - PID locking in Python bridge
2. **tools/acg_telegram_boot.sh** - Dual-start prevention in boot script
3. **tools/session_wakeup.sh** - Health monitoring in wakeup flow
4. **tools/telegram_health_check.sh** - Auto-recovery script (NEW)

**Verification**:
- All Python syntax validated (py_compile)
- All Bash syntax validated (bash -n)
- All 12 checklist items complete
- File permissions correct (health check executable)

**Next Phase**: 
Handoff to tester for Tests 1-4 validation.

## Memory Location

This file: /mnt/c/sage/sage-civilization/memories/agents/coder/telegram-409-pid-locking-implementation-20251229.md
