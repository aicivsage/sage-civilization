# JSONL Wrapper Monitor - Telegram Infrastructure Design

**Version**: 1.0
**Date**: 2025-10-20
**Author**: tg-archi
**Status**: DESIGN PROPOSAL (pending architect review)

---

## Executive Summary

This document defines the Telegram infrastructure integration for a new JSONL-based wrapper monitor to replace the existing tmux-polling `telegram_bridge.py` wrapper detection system.

**Key Decision**: This is a REPLACEMENT system, not an addition. The JSONL monitor will supersede tmux-polling for wrapper detection while maintaining all existing functionality.

---

## 1. Process Management

### 1.1 Process Architecture

**New Process:**
- **Name**: `telegram_jsonl_monitor.py`
- **Purpose**: Watch Claude Code JSONL conversation logs, detect wrapped messages, send to Telegram
- **Parent**: None (independent daemon)
- **Siblings**: `telegram_bridge.py` (Telegram → tmux receiver, still needed)

**Process Relationship:**
```
telegram_bridge.py      (KEEP - receives from Telegram, injects to tmux)
    ↓
  tmux session
    ↓
telegram_jsonl_monitor.py  (NEW - watches JSONL, sends to Telegram)
    ↓
send_telegram_plain.py     (PRODUCTION sender)
```

### 1.2 Lifecycle Management

**Startup:**
```bash
# Method 1: Manual start (testing)
nohup python3 tools/telegram_jsonl_monitor.py > /tmp/telegram_jsonl_monitor.log 2>&1 &
echo $! > .tg_sessions/jsonl_monitor.pid

# Method 2: Boot script (production)
bash tools/telegram_boot.sh
# This script starts BOTH:
#   - telegram_bridge.py (receiver)
#   - telegram_jsonl_monitor.py (JSONL watcher)
```

**Shutdown:**
```bash
# Method 1: Manual stop
kill $(cat .tg_sessions/jsonl_monitor.pid)
rm .tg_sessions/jsonl_monitor.pid

# Method 2: Boot script (production)
bash tools/telegram_shutdown.sh
# Stops both bridge and JSONL monitor
```

**Health Check Integration:**
Update `tools/telegram_health_check.sh` to monitor BOTH processes:
```bash
# Check bridge (receiver)
ps aux | grep telegram_bridge.py

# Check JSONL monitor (NEW)
ps aux | grep telegram_jsonl_monitor.py

# Auto-restart if either is dead
```

**Migration Strategy:**
1. **Phase 1** (testing): Run old tmux monitor AND new JSONL monitor in parallel
2. **Phase 2** (verification): Compare outputs, verify JSONL catches everything
3. **Phase 3** (cutover): Stop old monitor, keep JSONL monitor
4. **Phase 4** (cleanup): Remove old monitor code after 7 days

### 1.3 Runtime Mode

**Daemon Characteristics:**
- Long-running process (no auto-exit)
- Minimal CPU usage (event-driven, not polling)
- Minimal memory footprint (don't load entire JSONL, use tail + inotify)
- Graceful shutdown on SIGTERM (flush state, close files)

**Comparison to Existing:**
| Feature | telegram_bridge.py (tmux poll) | telegram_jsonl_monitor.py (NEW) |
|---------|-------------------------------|--------------------------------|
| Watch method | tmux capture-pane (30s poll) | inotify/tail -f (event-driven) |
| CPU usage | Constant (polling) | Minimal (event-driven) |
| Latency | Up to 30s | Sub-second |
| JSONL awareness | No | Yes |
| Configuration reload | Restart required | Hot-reload possible |

---

## 2. Configuration

### 2.1 Configuration Schema

**Extend existing** `config/telegram_config.json`:

```json
{
  "bot_token": "8388754468:AAEROakhpBPR1KNHjravHx3CIMH-FIyIWEc",
  "authorized_users": {
    "437939400": {
      "name": "Corey",
      "role": "creator",
      "admin": true
    }
  },
  "tmux_session": "6",
  "tmux_pane": "6:0.0",
  "working_directory": "/home/corey/projects/AI-CIV/grow_gemini_deepresearch",
  "response_timeout": 10,
  "error_notification": true,
  "corey_user_id": "437939400",

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
    "deduplication_enabled": true
  }
}
```

**Configuration Fields:**

- `enabled`: Master switch (allows disabling without stopping process)
- `claude_code_log_dir`: Where Claude Code stores JSONL conversation logs
- `watch_method`: "tail" (Linux tail -f) or "inotify" (filesystem events)
- `poll_interval_seconds`: Fallback polling if tail/inotify unavailable
- `state_file`: Tracks sent messages (deduplication)
- `wrapper_markers`: Start/end emojis (configurable for future changes)
- `sender_script`: Which script to call for sending (PRODUCTION LOCK)
- `max_message_length`: Telegram API limit
- `deduplication_enabled`: Prevent sending same message twice

### 2.2 Session Detection

**Problem**: Which JSONL file to watch? Claude Code creates new files per session.

**Solution**: Auto-detect most recent JSONL file in watch directory:

```python
def find_current_session_file(log_dir: Path) -> Path:
    """
    Find the most recently modified JSONL file in Claude Code log directory.

    Returns:
        Path to current session JSONL file
    """
    jsonl_files = list(log_dir.glob("*.jsonl"))
    if not jsonl_files:
        raise FileNotFoundError(f"No JSONL files found in {log_dir}")

    # Return most recently modified
    return max(jsonl_files, key=lambda p: p.stat().st_mtime)
```

**Session Rotation Handling:**
- Monitor detects when current file stops growing
- After 60 seconds of inactivity, re-scan for new file
- Seamlessly switch to new session file
- Log transition: "Switched from session X to session Y"

### 2.3 Configuration Reload

**Hot-reload capability:**
- Monitor checks `telegram_config.json` mtime every 60 seconds
- If config changed, reload settings (except bot_token - requires restart)
- Allows changing wrapper markers, poll interval without restart

**Restart-required changes:**
- `bot_token` (security: don't hold token in memory during reload)
- `claude_code_log_dir` (filesystem watch setup)
- `watch_method` (requires different initialization)

---

## 3. Script Registry

### 3.1 Registry Entry

**Add to** `memories/agents/tg-archi/telegram_script_registry.json`:

```json
{
  "telegram_jsonl_monitor.py": {
    "status": "PRODUCTION",
    "production_lock": "LOCKED ✅",
    "last_verified_working": "2025-10-20",
    "purpose": "Watches Claude Code JSONL conversation logs for wrapped messages, sends to Telegram",
    "usage": "nohup python3 tools/telegram_jsonl_monitor.py > /tmp/telegram_jsonl_monitor.log 2>&1 &",
    "features": [
      "Event-driven JSONL watching (sub-second latency)",
      "Auto-detects current session file",
      "Handles session rotation seamlessly",
      "Deduplication via state file",
      "Hot-reload configuration",
      "Graceful shutdown"
    ],
    "dependencies": [
      "config/telegram_config.json (jsonl_monitor section)",
      ".tg_sessions/jsonl_monitor_state.json (runtime state)",
      "tools/send_telegram_plain.py (CRITICAL DEPENDENCY - production sender)"
    ],
    "replaces": "telegram_bridge.py wrapper detection (keep bridge for receiving)",
    "called_by": [
      "tools/telegram_boot.sh (automatic startup)",
      "tools/telegram_health_check.sh (health monitoring)"
    ],
    "config_change_requires_restart": "Partial - most settings hot-reload, see docs",
    "common_issue": "If Claude Code log directory changes, update config and restart",
    "git_commit_hash_when_working": "TBD (after implementation)",
    "never_modify_unless": "Adding features or fixing bugs with explicit approval and testing",
    "notes": "This is the PRODUCTION wrapper monitor. Uses JSONL, not tmux polling. PRODUCTION-LOCKED after verification phase.",
    "test_command": "Send wrapped message in Claude Code, verify Telegram delivery within 5 seconds"
  }
}
```

### 3.2 Dependencies

**Production Sender Lock:**
```json
"sender_script": "tools/send_telegram_plain.py"
```

**Why `send_telegram_plain.py` not `send_telegram_direct.py`?**
- `send_telegram_plain.py`: Plain text (no Markdown parsing) - safer for arbitrary content
- `send_telegram_direct.py`: Markdown parsing - can break on special characters

**Decision**: Use `send_telegram_plain.py` for JSONL monitor to avoid Markdown parsing issues with extracted content.

**Registry Protection:**
- Monitor script READS sender path from config
- NEVER hardcode sender path in monitor script
- Registry documents this dependency clearly
- Any changes to sender require registry update + testing

### 3.3 Deprecation of Old Monitor

**Update registry for** `telegram_bridge.py`:

```json
{
  "telegram_bridge.py": {
    "status": "PRODUCTION",
    "production_lock": "PARTIAL - wrapper detection removed, receiver kept",
    "purpose": "Receives messages FROM Telegram, injects to tmux (wrapper detection moved to telegram_jsonl_monitor.py)",
    "features": [
      "Receives text and photos from Telegram",
      "Injects received content to tmux",
      "Session state persistence",
      "Daemon mode operation"
    ],
    "notes": "Wrapper detection feature removed in favor of telegram_jsonl_monitor.py. Keep this for receiving messages from Corey."
  }
}
```

---

## 4. Error Handling

### 4.1 Telegram API Failures

**Scenario**: `send_telegram_plain.py` returns non-zero exit code

**Strategy**:
```python
def send_with_retry(user_id: int, message: str, max_retries: int = 3) -> bool:
    """
    Send message with exponential backoff retry.

    Returns:
        True if sent successfully, False after all retries exhausted
    """
    for attempt in range(max_retries):
        result = subprocess.run(
            ["python3", SENDER_SCRIPT, str(user_id), message],
            capture_output=True,
            timeout=30
        )

        if result.returncode == 0:
            logger.info(f"Message sent successfully (attempt {attempt + 1})")
            return True

        # Exponential backoff: 2s, 4s, 8s
        backoff_seconds = 2 ** attempt
        logger.warning(f"Send failed (attempt {attempt + 1}/{max_retries}), retry in {backoff_seconds}s")
        time.sleep(backoff_seconds)

    logger.error(f"Message send failed after {max_retries} attempts")
    return False
```

**Fallback**: If ALL retries fail, log to error file but DON'T crash monitor:
```python
# Log failed message for manual retry
with open(ERROR_LOG, 'a') as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "message": message[:200],  # Truncate for logging
        "error": "Telegram API unavailable after 3 retries"
    }, f)
    f.write('\n')
```

### 4.2 JSONL File Rotation

**Scenario**: Claude Code starts new session, creates new JSONL file

**Detection**:
```python
def detect_session_rotation(current_file: Path, last_activity: datetime) -> Optional[Path]:
    """
    Detect if current session has rotated to a new file.

    Returns:
        New session file if rotated, None if still active
    """
    # If no activity for 60 seconds, check for new files
    if datetime.now() - last_activity > timedelta(seconds=60):
        new_file = find_current_session_file(LOG_DIR)

        if new_file != current_file:
            logger.info(f"Session rotation detected: {current_file.name} → {new_file.name}")
            return new_file

    return None
```

**Handling**:
1. Close watch on old file
2. Open watch on new file
3. Reset state tracking (offset, last message ID)
4. Continue monitoring

### 4.3 Logging Strategy

**Log Levels:**
- **DEBUG**: JSONL line processing, state updates, config checks
- **INFO**: Wrapper detected, message sent, session rotation, health checks
- **WARNING**: Send retry, config reload issues, file access warnings
- **ERROR**: Send failure after retries, JSONL parse errors, critical failures

**Log Files:**
```
/tmp/telegram_jsonl_monitor.log          (main log, rotated daily)
/tmp/telegram_jsonl_monitor_error.log    (error-only log, never rotates)
```

**Log Rotation:**
- Main log rotates at 10MB or daily (whichever first)
- Keep last 7 days of logs
- Error log never rotates (manual review required)

**Log Format:**
```
2025-10-20 14:35:22,123 - INFO - telegram_jsonl_monitor - Wrapper detected: "Session starting at..."
2025-10-20 14:35:23,456 - INFO - telegram_jsonl_monitor - Message sent to 437939400 (length: 145)
2025-10-20 14:35:45,789 - WARNING - telegram_jsonl_monitor - Send failed (attempt 1/3), retry in 2s
2025-10-20 14:40:00,000 - INFO - telegram_jsonl_monitor - Session rotation detected: session_1.jsonl → session_2.jsonl
```

### 4.4 Graceful Degradation

**If critical components fail:**

| Component | Failure Mode | Graceful Degradation |
|-----------|--------------|---------------------|
| Telegram API | HTTP errors, timeouts | Retry with backoff, log failures, continue monitoring |
| JSONL file access | Permission denied, file missing | Retry file discovery every 60s, log error |
| Config file | Parse error, missing fields | Use defaults, log warning, continue with last valid config |
| State file | Corrupt, unreadable | Reset state (may cause duplicate sends), log warning |
| Sender script | Missing, not executable | Log critical error, notify via tmux injection, halt sending |

**Never crash the monitor unless**:
- Config file completely missing (can't determine basic settings)
- Sender script missing (can't fulfill core function)
- Log directory doesn't exist and can't be created

---

## 5. Testing

### 5.1 Test Environments

**Development Testing (safe):**
```json
{
  "jsonl_monitor": {
    "enabled": true,
    "test_mode": true,
    "test_user_id": "437939400",
    "dry_run": false
  }
}
```

**Dry-Run Testing (no actual sends):**
```json
{
  "jsonl_monitor": {
    "enabled": true,
    "test_mode": true,
    "dry_run": true
  }
}
```

In dry-run mode:
- Monitor logs what it WOULD send
- Does NOT call sender script
- Useful for verifying detection logic without spamming Corey

### 5.2 Test Script

**Create** `tools/test_telegram_jsonl_monitor.sh`:

```bash
#!/bin/bash
# Test JSONL wrapper monitor end-to-end

set -e

PROJECT_ROOT="/home/corey/projects/AI-CIV/grow_gemini_deepresearch"
cd "$PROJECT_ROOT"

echo "=== Telegram JSONL Monitor Test Suite ==="
echo

# Test 1: Dry-run detection
echo "Test 1: Dry-run wrapper detection"
echo "🤖🎯📱" >> test_session.jsonl
echo "Test message 1" >> test_session.jsonl
echo "✨🔚" >> test_session.jsonl

# Check logs for detection
sleep 2
if grep -q "Test message 1" /tmp/telegram_jsonl_monitor.log; then
    echo "✓ Test 1 passed: Wrapper detected in dry-run"
else
    echo "✗ Test 1 failed: Wrapper not detected"
    exit 1
fi

# Test 2: Deduplication
echo "Test 2: Deduplication"
echo "🤖🎯📱" >> test_session.jsonl
echo "Test message 1" >> test_session.jsonl  # Same message
echo "✨🔚" >> test_session.jsonl

sleep 2
SEND_COUNT=$(grep -c "Message sent to 437939400" /tmp/telegram_jsonl_monitor.log)
if [ "$SEND_COUNT" -eq 1 ]; then
    echo "✓ Test 2 passed: Duplicate prevented"
else
    echo "✗ Test 2 failed: Duplicate sent (count: $SEND_COUNT)"
    exit 1
fi

# Test 3: Session rotation
echo "Test 3: Session rotation detection"
mv test_session.jsonl test_session_old.jsonl
echo "🤖🎯📱" >> test_session_new.jsonl
echo "Test message 2" >> test_session_new.jsonl
echo "✨🔚" >> test_session_new.jsonl

sleep 3
if grep -q "Session rotation detected" /tmp/telegram_jsonl_monitor.log; then
    echo "✓ Test 3 passed: Session rotation detected"
else
    echo "✗ Test 3 failed: Session rotation not detected"
    exit 1
fi

# Test 4: Real send (ONLY if not in dry-run)
if [ "$1" != "--dry-run" ]; then
    echo "Test 4: Real Telegram send"
    echo "🤖🎯📱" >> test_session_new.jsonl
    echo "JSONL Monitor Test - please acknowledge!" >> test_session_new.jsonl
    echo "✨🔚" >> test_session_new.jsonl

    echo "⚠ Check Telegram for test message, then press Enter..."
    read
    echo "✓ Test 4 completed (manual verification required)"
fi

echo
echo "=== All tests passed! ==="
```

### 5.3 Verification Checklist

**Pre-deployment verification:**

- [ ] Wrapper detection works (test with known wrapped message)
- [ ] Deduplication works (send same message twice, only one Telegram delivery)
- [ ] Session rotation works (create new JSONL, verify switch)
- [ ] Config hot-reload works (change poll interval, verify update without restart)
- [ ] Error handling works (kill sender script, verify graceful degradation)
- [ ] Health check integration works (kill monitor, verify auto-restart)
- [ ] Log rotation works (generate 10MB+ logs, verify rotation)
- [ ] Graceful shutdown works (send SIGTERM, verify state flush)

**Post-deployment verification:**

- [ ] Monitor running? `ps aux | grep telegram_jsonl_monitor.py`
- [ ] Logs healthy? `tail -20 /tmp/telegram_jsonl_monitor.log`
- [ ] State file updating? `cat .tg_sessions/jsonl_monitor_state.json`
- [ ] Real message delivery? (send wrapped message, check Telegram)
- [ ] No duplicate sends? (check state file for unique message IDs)
- [ ] Health check passing? `bash tools/telegram_health_check.sh`

### 5.4 Parallel Testing Phase

**Goal**: Verify JSONL monitor catches everything tmux monitor catches

**Setup:**
1. Run old tmux monitor (telegram_bridge.py wrapper detection)
2. Run new JSONL monitor (telegram_jsonl_monitor.py)
3. Both send to Telegram
4. Compare deliveries (should be identical)

**Test Plan:**
- Day 1-3: Parallel operation, collect metrics
- Day 4-7: Compare logs, verify no missed messages
- Day 8: If identical, promote JSONL to production
- Day 9-15: JSONL only, monitor for issues
- Day 16+: Remove old tmux monitor code

**Metrics to Compare:**
- Total wrapped messages detected
- Total Telegram deliveries
- Latency (wrapper → Telegram delivery time)
- Failure rate (send errors)
- Duplicate sends (should be zero for both)

---

## 6. Integration Points

### 6.1 Boot Script Integration

**Update** `tools/telegram_boot.sh`:

```bash
#!/bin/bash
# Boot all Telegram systems

set -e

PROJECT_ROOT="/home/corey/projects/AI-CIV/grow_gemini_deepresearch"
cd "$PROJECT_ROOT"

echo "=== Booting Telegram Systems ==="

# Start bridge (receiver: Telegram → tmux)
echo "Starting telegram_bridge.py..."
nohup python3 tools/telegram_bridge.py > /tmp/telegram_bridge.log 2>&1 &
echo $! > .tg_sessions/telegram_bridge.pid
echo "✓ Bridge started (PID: $(cat .tg_sessions/telegram_bridge.pid))"

# Start JSONL monitor (sender: tmux → Telegram)
echo "Starting telegram_jsonl_monitor.py..."
nohup python3 tools/telegram_jsonl_monitor.py > /tmp/telegram_jsonl_monitor.log 2>&1 &
echo $! > .tg_sessions/jsonl_monitor.pid
echo "✓ JSONL monitor started (PID: $(cat .tg_sessions/jsonl_monitor.pid))"

echo
echo "=== Telegram Systems Online ==="
echo "Bridge (receiver): $(cat .tg_sessions/telegram_bridge.pid)"
echo "JSONL monitor (sender): $(cat .tg_sessions/jsonl_monitor.pid)"
echo
echo "Logs:"
echo "  - Bridge: /tmp/telegram_bridge.log"
echo "  - JSONL monitor: /tmp/telegram_jsonl_monitor.log"
```

### 6.2 Health Check Integration

**Update** `tools/telegram_health_check.sh`:

```bash
# Check JSONL monitor
if ! pgrep -f telegram_jsonl_monitor.py > /dev/null; then
    echo "⚠ JSONL monitor dead, restarting..."
    nohup python3 tools/telegram_jsonl_monitor.py > /tmp/telegram_jsonl_monitor.log 2>&1 &
    echo $! > .tg_sessions/jsonl_monitor.pid
    echo "✓ JSONL monitor restarted"
fi

# Check log freshness
LAST_LOG=$(tail -1 /tmp/telegram_jsonl_monitor.log | awk '{print $1, $2}')
LOG_AGE=$(( $(date +%s) - $(date -d "$LAST_LOG" +%s 2>/dev/null || echo 0) ))

if [ "$LOG_AGE" -gt 120 ]; then
    echo "⚠ JSONL monitor log stale (${LOG_AGE}s), may be frozen"
fi
```

### 6.3 Primary AI Wake-Up Integration

**Update** `tools/session_wakeup.sh` to report JSONL monitor status:

```bash
# Telegram Infrastructure Status
echo "=== Telegram Infrastructure ==="

if pgrep -f telegram_bridge.py > /dev/null; then
    echo "✓ Bridge (receiver): Running"
else
    echo "✗ Bridge (receiver): DEAD"
fi

if pgrep -f telegram_jsonl_monitor.py > /dev/null; then
    echo "✓ JSONL monitor (sender): Running"
else
    echo "✗ JSONL monitor (sender): DEAD"
fi

# Check last activity
BRIDGE_AGE=$(tail -1 /tmp/telegram_bridge.log | awk '{print $1, $2}')
JSONL_AGE=$(tail -1 /tmp/telegram_jsonl_monitor.log | awk '{print $1, $2}')

echo "Last bridge activity: $BRIDGE_AGE"
echo "Last JSONL activity: $JSONL_AGE"
```

---

## 7. Migration Plan

### Phase 1: Implementation (Days 1-3)

**Tasks:**
1. Implement `telegram_jsonl_monitor.py` (coder)
2. Add config section to `telegram_config.json`
3. Create test script `test_telegram_jsonl_monitor.sh`
4. Update registry with new entry
5. Run unit tests (dry-run mode)

**Success Criteria:**
- Monitor detects wrappers in test JSONL files
- Deduplication works
- Logs are clean (no errors)

### Phase 2: Parallel Testing (Days 4-7)

**Tasks:**
1. Deploy JSONL monitor alongside existing tmux monitor
2. Both systems send to Telegram (acceptable duplicate sends during testing)
3. Compare logs daily
4. Fix any discrepancies

**Success Criteria:**
- JSONL monitor catches 100% of messages tmux monitor catches
- Latency is equal or better (target: <5s)
- No missed messages
- No false positives

### Phase 3: Cutover (Day 8)

**Tasks:**
1. Stop old tmux monitor wrapper detection
2. Keep JSONL monitor as sole wrapper sender
3. Monitor for issues (24 hours)
4. Update documentation

**Rollback Plan:**
- If issues detected, restart tmux monitor
- Debug JSONL monitor in dry-run mode
- Return to Phase 2 for more testing

**Success Criteria:**
- No missed messages during cutover
- Corey receives all expected Telegram notifications
- System stable for 24 hours

### Phase 4: Cleanup (Days 9-15)

**Tasks:**
1. Remove tmux monitor wrapper detection code
2. Update `telegram_bridge.py` to be receiver-only
3. Archive old monitor code to `archive/`
4. Update all documentation
5. Production-lock JSONL monitor in registry

**Success Criteria:**
- Old code removed from production path
- Documentation reflects new architecture
- Registry accurate
- tg-archi knows new system

---

## 8. Architectural Decisions

### 8.1 Why JSONL Instead of Tmux?

**Advantages:**
- **Latency**: Event-driven (sub-second) vs polling (30s)
- **Reliability**: Structured data (JSONL) vs screen scraping (tmux)
- **Efficiency**: Watch file changes vs poll screen buffer
- **Scalability**: JSONL doesn't grow with conversation length

**Disadvantages:**
- **Dependency**: Requires Claude Code JSONL format (vendor lock-in)
- **Complexity**: Session rotation handling, file watching

**Decision**: JSONL is superior for latency and reliability. Vendor dependency is acceptable risk.

### 8.2 Why Plain Text Sender?

**Question**: Why `send_telegram_plain.py` instead of `send_telegram_direct.py`?

**Answer**:
- Wrapped content is already formatted by Primary
- Markdown parsing can break on special characters in JSONL
- Plain text is safer for arbitrary content extraction
- Corey still sees formatted messages (Primary controls formatting)

**Decision**: Use `send_telegram_plain.py` for JSONL monitor to avoid Markdown parsing issues.

### 8.3 Why Keep Bridge?

**Question**: Can we combine JSONL monitor and bridge into one process?

**Answer**:
- Bridge receives from Telegram (long-polling API)
- JSONL monitor watches file system (inotify/tail)
- Two different I/O paradigms, better as separate processes
- Easier to debug, test, and restart independently

**Decision**: Keep as two separate daemons.

---

## 9. Success Metrics

### 9.1 Performance

**Target Metrics:**
- Latency: Wrapper written → Telegram delivery < 5 seconds (vs 30s with tmux)
- Reliability: 99.9% delivery rate (no missed messages)
- Efficiency: CPU usage < 1% average, memory < 50MB

### 9.2 Quality

**Target Metrics:**
- Zero duplicate sends (deduplication working)
- Zero false positives (only actual wrapped messages sent)
- Zero crashes (graceful error handling)
- Log clarity (issues debuggable from logs)

### 9.3 Operational

**Target Metrics:**
- Health check passes 100% of time (auto-restart works)
- Configuration hot-reload working (no restart for minor changes)
- Session rotation seamless (no missed messages during rotation)
- Documentation complete (tg-archi can maintain without coder)

---

## 10. Open Questions

**For Architect:**
1. Should we use Python `inotify` library or `tail -f` subprocess?
2. Should state file track message hashes or JSONL line offsets?
3. Should we implement rate limiting (max X messages per minute)?
4. Should we support multiple simultaneous Claude Code sessions?

**For Primary:**
1. Should we keep wrapper markers configurable or hardcode them?
2. Should we add support for Markdown formatting in plain sender?
3. Should we implement emergency "send to Corey" command if all else fails?

**For Corey:**
1. Is duplicate sending during parallel testing acceptable?
2. Should we notify via email when JSONL monitor encounters critical errors?
3. Do we need wrapper messages logged to a permanent file (not just Telegram)?

---

## 11. Handoff

**This infrastructure design is ready for:**

1. **Architect Review**: System design, architectural decisions
2. **Coder Implementation**: Build `telegram_jsonl_monitor.py`
3. **Tester Verification**: Run test suite, verify functionality
4. **tg-archi Integration**: Deploy, monitor, maintain

**Next Steps:**
1. Architect reviews and approves design
2. Coder implements monitor script
3. tg-archi creates test environment
4. Run Phase 1 testing (dry-run)
5. Deploy Phase 2 (parallel testing)

**Questions?** Escalate to tg-archi or Primary.

---

**Document Status**: DESIGN PROPOSAL
**Author**: tg-archi (Telegram Infrastructure Specialist)
**Date**: 2025-10-20
**Next Review**: After architect feedback

---

## Appendix A: Configuration Example

**Complete** `config/telegram_config.json` with JSONL monitor:

```json
{
  "bot_token": "8388754468:AAEROakhpBPR1KNHjravHx3CIMH-FIyIWEc",
  "authorized_users": {
    "437939400": {
      "name": "Corey",
      "role": "creator",
      "admin": true
    }
  },
  "tmux_session": "6",
  "tmux_pane": "6:0.0",
  "working_directory": "/home/corey/projects/AI-CIV/grow_gemini_deepresearch",
  "response_timeout": 10,
  "error_notification": true,
  "corey_user_id": "437939400",

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
    "error_log_file": "/tmp/telegram_jsonl_monitor_error.log",
    "test_mode": false,
    "dry_run": false
  }
}
```

## Appendix B: State File Format

**`.tg_sessions/jsonl_monitor_state.json`:**

```json
{
  "last_updated": "2025-10-20T14:35:45.123456",
  "current_session_file": "/home/corey/.config/Claude/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/session_abc123.jsonl",
  "last_processed_offset": 15234,
  "sent_messages": {
    "hash_1": {
      "content": "Session starting at 14:30...",
      "sent_at": "2025-10-20T14:30:15.000000",
      "telegram_message_id": 12345
    },
    "hash_2": {
      "content": "Session complete at 16:45...",
      "sent_at": "2025-10-20T16:45:30.000000",
      "telegram_message_id": 12346
    }
  },
  "session_history": [
    {
      "file": "session_abc123.jsonl",
      "started_at": "2025-10-20T14:30:00.000000",
      "ended_at": "2025-10-20T16:45:30.000000",
      "messages_sent": 2
    }
  ]
}
```

## Appendix C: File Watching Implementation Notes

**Option 1: Python `tail -f` subprocess (simpler):**
```python
import subprocess

proc = subprocess.Popen(
    ["tail", "-f", "-n", "0", str(jsonl_file)],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

for line in proc.stdout:
    process_jsonl_line(line)
```

**Option 2: Python `inotify` library (more efficient):**
```python
import inotify.adapters

i = inotify.adapters.Inotify()
i.add_watch(str(jsonl_file.parent))

for event in i.event_gen(yield_nones=False):
    (_, type_names, path, filename) = event
    if filename == jsonl_file.name and 'IN_MODIFY' in type_names:
        # Read new lines from file
        with open(jsonl_file) as f:
            f.seek(last_offset)
            for line in f:
                process_jsonl_line(line)
            last_offset = f.tell()
```

**Recommendation**: Start with Option 1 (`tail -f`) for simplicity. Migrate to Option 2 if performance becomes issue.

---

**End of Infrastructure Design Document**
