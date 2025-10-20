# Telegram Injection Fix Complete - 2025-10-20

## Problem Identified

**Symptom**: Messages sent from Telegram not appearing in tmux
**Root Cause**: Config pointing to wrong session (session 3 vs actual session 6)
**Process Running ≠ Function Working**: Bridge processes were running but injecting to wrong session

## What Was Fixed

### 1. Config Update
**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/config/telegram_config.json`

**Changed**:
```json
"tmux_session": "3",    → "tmux_session": "6",
"tmux_pane": "3:0.0",   → "tmux_pane": "6:0.0",
```

**Why**: Primary is currently in session 6, but config was still pointing to session 3 (probably from previous session)

### 2. Registry Documentation Update
**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/telegram_script_registry.json`

**Added to telegram_bridge.py entry**:
- `"config_change_requires_restart": "YES"`
- `"restart_script": "tools/fix_telegram_session.sh"`
- `"common_issue": "If tmux session changes, config must be updated and bridge restarted"`
- Updated features to include bidirectional functionality (TO and FROM Telegram)

**Why**: Prevents future confusion about whether bridge needs restart after config changes

### 3. Automated Fix Script Created
**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/fix_telegram_session.sh`

**What it does**:
1. Detects current tmux session automatically
2. Verifies config matches current session
3. Kills old telegram_bridge.py processes
4. Restarts bridge with correct config
5. Verifies bridge started successfully
6. Shows recent logs for troubleshooting

**Usage**:
```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
chmod +x tools/fix_telegram_session.sh
./tools/fix_telegram_session.sh
```

## Next Steps for Corey

### To Apply the Fix:

1. **Run the fix script**:
   ```bash
   cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
   chmod +x tools/fix_telegram_session.sh
   ./tools/fix_telegram_session.sh
   ```

2. **Verify fix worked**:
   - Send a test message from Telegram (e.g., "test injection")
   - Check if it appears in tmux session 6
   - If yes → injection fixed! ✓

3. **Monitor bridge logs** (if issues):
   ```bash
   tail -f /tmp/telegram_bridge.log
   ```

### Expected Output from Fix Script:

```
=== Telegram Bridge Session Fix ===

Step 1: Detecting current tmux session...
Current session: 6:0.0

Step 2: Verifying config update...
Configured pane: 6:0.0

Step 3: Stopping old telegram_bridge.py processes...
Killed old processes

Step 4: Starting telegram_bridge.py with correct session...
Bridge started with PID: [some number]

Step 5: Verify it started
✓ Bridge process running (PID: [some number])

Step 6: Recent bridge logs:
[logs showing bridge initialization]

=== Fix Complete ===

Next steps:
1. Send test message from Telegram: 'test injection'
2. Check if it appears in tmux session 6
3. If working, injection is fixed!
```

## Root Cause Analysis

**Why This Happened**:
- Tmux sessions are numbered sequentially (0, 1, 2, 3, ...)
- Each time you create a new tmux session, it gets the next number
- Config was hardcoded to session 3 from a previous session
- When you started a new session (session 6), bridge kept trying to inject to session 3
- **Process was running but injecting to wrong place**

**Lesson Learned**: "Process running ≠ function working" (from this morning's handoff)

## Prevention Strategy

### For Future Sessions:

**Option 1: Manual Check at Session Start** (current approach)
- Add to wake-up protocol: Verify telegram config matches current session
- If mismatch detected, run `tools/fix_telegram_session.sh`

**Option 2: Auto-Detection in Bridge** (future enhancement)
- Modify telegram_bridge.py to detect current session dynamically
- Remove hardcoded session from config
- Bridge auto-finds active Primary session

**Option 3: Named Sessions** (most robust)
- Use named tmux sessions instead of numbers (e.g., "acgee-main")
- Named sessions stay consistent across reboots
- Config points to name, not number

**Recommendation**: Implement Option 3 (named sessions) for long-term stability

## Files Modified

1. **config/telegram_config.json** - Updated session/pane to 6:0.0
2. **memories/agents/tg-archi/telegram_script_registry.json** - Added restart requirements
3. **tools/fix_telegram_session.sh** - NEW automated fix script

## Files to Review (Context)

- `tools/telegram_bridge.py` - Bridge implementation (loads config once at startup)
- `TELEGRAM-BOOT-QUICK-START.md` - Boot protocol (should add session verification step)
- `PRIMARY-TELEGRAM-QUICK-REFERENCE.md` - Quick reference (should mention session requirement)

## Success Criteria

**Fixed when**:
- ✓ Config updated to session 6
- ✓ Fix script created and documented
- ✓ Registry updated with restart requirements
- ⏳ Bridge restarted with correct config (requires Corey to run script)
- ⏳ Test message from Telegram appears in tmux (requires Corey to test)

**Test Command**:
1. From Telegram, send: "test injection"
2. In tmux session 6, message should appear immediately
3. If working → injection fixed! ✓

---

**tg-archi signature**: Config fixed, script created, registry updated. Ready for Corey to restart bridge and test.
