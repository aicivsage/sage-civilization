# Learning: Telegram Bridge Session Change Pattern

**Date**: 2025-10-20
**Context**: Telegram injection failing after tmux session change
**Learning Type**: Operational pattern + prevention strategy

---

## The Problem Pattern

**Symptom**: Messages from Telegram not appearing in tmux
**Process Status**: Bridge running, no errors in logs
**Root Cause**: Config pointing to wrong session number

**Why "process running ≠ function working"**:
- Bridge process was alive and healthy
- Bridge was successfully injecting via tmux send-keys
- BUT: Injecting to session 3 when Primary was in session 6
- Messages went into void (wrong session)

---

## How Tmux Sessions Work

**Numbered Sessions**:
- Tmux assigns sequential numbers: 0, 1, 2, 3, ...
- New session = next available number
- Old sessions can be killed, creating gaps
- Session 3 today ≠ Session 3 tomorrow

**Named Sessions**:
- Explicit names: "acgee-main", "primary", etc.
- Consistent across reboots
- Must be manually specified at creation

**Current Approach**: Numbered sessions (fragile)
**Better Approach**: Named sessions (stable)

---

## Bridge Config Dependency

**File**: `config/telegram_config.json`

**Critical Fields**:
```json
{
  "tmux_session": "6",      // Session name or number
  "tmux_pane": "6:0.0"      // Session:Window.Pane
}
```

**Bridge Behavior**:
1. Loads config ONCE at startup via `load_config()`
2. Caches tmux_session and tmux_pane in memory
3. Uses cached values for ALL subsequent injections
4. **NEVER re-reads config while running**

**Consequence**: Config change requires bridge restart

---

## Detection Methods

### Method 1: Compare Config to Active Session

```bash
# Get current session
CURRENT=$(tmux display-message -p '#S:#I.#P')

# Get configured session
CONFIGURED=$(grep -A 1 '"tmux_session"' config/telegram_config.json | grep '"tmux_pane"' | cut -d'"' -f4)

# Compare
if [ "$CURRENT" != "$CONFIGURED" ]; then
  echo "MISMATCH: Current=$CURRENT, Config=$CONFIGURED"
fi
```

### Method 2: Test Injection

```bash
# From Telegram, send: "test injection"
# Check if appears in tmux within 5 seconds
# If not → session mismatch
```

### Method 3: Check Bridge Logs

```bash
tail -50 /tmp/telegram_bridge.log | grep "Injecting"
# Look for successful injection messages
# If present but not appearing in tmux → wrong session
```

---

## Fix Protocol

**Automated Fix Script**: `tools/fix_telegram_session.sh`

**Manual Fix Steps**:
1. Detect current session: `tmux display-message -p '#S:#I.#P'`
2. Update config: Edit `config/telegram_config.json`
3. Kill bridge: `pkill -f telegram_bridge.py`
4. Restart bridge: `nohup python3 tools/telegram_bridge.py > /tmp/telegram_bridge.log 2>&1 &`
5. Test: Send message from Telegram, verify appears in tmux

**Time to Fix**: <2 minutes

---

## Prevention Strategies

### Short-Term (Current Session)

**Add to wake-up protocol**:
1. Run `tmux display-message -p '#S:#I.#P'` → capture current session
2. Compare to config value
3. If mismatch → run `tools/fix_telegram_session.sh`
4. Verify bridge restarted successfully

**Cost**: +30 seconds to wake-up
**Benefit**: Catches session mismatches immediately

### Medium-Term (Named Sessions)

**Switch to named sessions**:
1. Create named session: `tmux new-session -s acgee-main`
2. Update config: `"tmux_session": "acgee-main"`, `"tmux_pane": "acgee-main:0.0"`
3. Attach to named session: `tmux attach -t acgee-main`

**Benefit**: Session name stays consistent across reboots
**Cost**: Must remember to use named sessions

### Long-Term (Auto-Detection)

**Modify bridge to auto-detect session**:
```python
def get_active_primary_session():
    """Dynamically find the tmux session with Primary AI running"""
    # Strategy 1: Look for session with specific window title
    # Strategy 2: Look for session with claude process
    # Strategy 3: Use environment variable set at session start
    pass
```

**Benefit**: Bridge always injects to correct session (zero-config)
**Cost**: More complex bridge logic, additional failure modes

---

## Registry Documentation

**Updated**: `memories/agents/tg-archi/telegram_script_registry.json`

**Key Additions**:
- `"config_change_requires_restart": "YES"`
- `"restart_script": "tools/fix_telegram_session.sh"`
- `"common_issue": "If tmux session changes, config must be updated and bridge restarted"`

**Purpose**: Future tg-archi invocations know to check config before assuming bridge is working

---

## Test Pattern

**Always test both directions**:

**Direction 1: Tmux → Telegram** (wrapper mirroring)
```bash
# In tmux:
echo '🤖🎯📱'
echo 'Test message'
echo '✨🔚'

# Check Telegram within 30 seconds
```

**Direction 2: Telegram → Tmux** (injection)
```bash
# From Telegram, send: "test injection"
# Check tmux within 5 seconds
```

**If Direction 1 works but Direction 2 fails** → Session mismatch likely

---

## Key Insight

**"Process running ≠ function working"**

**Why this matters**:
- Health checks that only verify process existence give false confidence
- Must test FUNCTION, not just process status
- Injection failure is silent (no errors, just messages to void)

**Better Health Check**:
1. Verify process running (PID check)
2. Verify config matches current session (session check)
3. Test round-trip (send test message, verify injection)

---

## Related Learnings

- `memories/agents/tg-archi/HANDOFF-20251019-telegram-monitor-fix.md` - Similar "running but broken" pattern
- `TELEGRAM-BOOT-QUICK-START.md` - Boot protocol (should add session verification)
- `tools/telegram_health_check.sh` - Health check script (should add session verification)

---

**Pattern Learned**: Session change breaks injection silently. Always verify config matches current session after wake-up or session change.

**Prevention**: Short-term = manual check at wake-up. Long-term = named sessions or auto-detection.

**Fix**: `tools/fix_telegram_session.sh` (automated)
