# Telegram Auto-Boot Quick Reference

**For Primary AI - Wake-Up Protocol Step 1 Enhanced**

---

## What Changed (2025-10-20)

**Boot script now AUTO-DETECTS tmux session and updates config BEFORE starting processes.**

**Result**: Config staleness is impossible. Injection always works.

---

## Usage (Same Command, Smarter Behavior)

```bash
bash tools/acg_telegram_boot.sh
```

**NEW: What it does now**:

1. ✅ **Detects current tmux session** (auto)
2. ✅ **Updates config to match** (auto)
3. ✅ **Starts bridge** (INBOUND: Telegram → tmux)
4. ✅ **Starts monitor** (OUTBOUND: tmux → Telegram)
5. ✅ **Verifies both running**

**OLD: What you used to do manually**:
```bash
# OLD WAY (no longer needed):
bash tools/fix_telegram_session.sh  # manually fix config
bash tools/acg_telegram_boot.sh     # then start processes
```

**NEW WAY (auto-healing)**:
```bash
bash tools/acg_telegram_boot.sh  # does everything
```

---

## Wake-Up Protocol Step 1 (Updated)

**From CLAUDE.md**:

```
Step 1: Boot Telegram System FIRST (MANDATORY)

Delegate to tg-archi to boot Telegram infrastructure BEFORE anything else:

Task(tg-archi):
  Boot Telegram system for current session
  Verify both bridge and monitor operational
  Return: Status confirmation

Alternative (manual boot):
bash tools/acg_telegram_boot.sh
```

**Now even more reliable** - config auto-updates on every boot!

---

## Example Output

```
=== ACG Telegram System Boot ===

Step 0: Auto-detecting current tmux session...
  Detected session: 0
  Detected pane: 0:0.0
✓ Config updated with current tmux session

Step 1: Detecting current ACG session file...
✓ Found session: d68b9236-9f39-4379-ba85-b3c5348609b4.jsonl

Step 2: Stopping any existing ACG Telegram processes...
  Stopped: ACG_telegram_bridge
  Stopped: ACG_telegram_jsonl_monitor

Step 3: Starting ACG_telegram_bridge (INBOUND: Telegram → tmux)...
✓ Bridge started (PID: 12345)

Step 4: Starting ACG_telegram_jsonl_monitor (OUTBOUND: tmux → Telegram)...
  Watching session: d68b9236-9f39-4379-ba85-b3c5348609b4.jsonl
✓ Monitor started (PID: 12346)

Step 5: Verifying processes...
corey    12345  ... ACG_telegram_bridge
corey    12346  ... ACG_telegram_jsonl_monitor

=== ACG Telegram System READY ===

Logs:
  Bridge:  /tmp/acgee_telegram_bridge.log
  Monitor: /tmp/acgee_telegram_monitor.log

Test:
  Inbound:  Send message from Telegram → should appear in tmux
  Outbound: Send wrapped message 🤖🎯📱 ... ✨🔚 → should appear on Telegram
```

---

## Error Handling

**If not running in tmux**:
```
❌ ERROR: Not running inside tmux. This script must be run from within a tmux session.
```

**Solution**: Attach to tmux first, then run boot script

**If config file missing**:
```
❌ ERROR: Config file not found: config/telegram_config.json
```

**Solution**: Check file exists, restore from backup if needed

**If processes fail to start**:
```
❌ Bridge failed to start. Check /tmp/acgee_telegram_bridge.log
```

**Solution**: Check logs for Python errors, verify dependencies

---

## Testing

**After boot, verify both directions work**:

**Test INBOUND (Telegram → tmux)**:
1. Send message from Telegram: "test injection"
2. Should appear in current tmux pane within 5 seconds
3. If not working: Check `/tmp/acgee_telegram_bridge.log`

**Test OUTBOUND (tmux → Telegram)**:
1. Send wrapped message in tmux:
   ```
   🤖🎯📱
   Test auto-boot working!
   ✨🔚
   ```
2. Should appear on Telegram within 5 seconds
3. If not working: Check `/tmp/acgee_telegram_monitor.log`

---

## Logs (Always Check on Issues)

```bash
# Bridge logs (INBOUND)
tail -f /tmp/acgee_telegram_bridge.log

# Monitor logs (OUTBOUND)
tail -f /tmp/acgee_telegram_monitor.log
```

---

## Stop Processes

```bash
pkill -f ACG_telegram_bridge
pkill -f ACG_telegram_jsonl_monitor
```

**Then restart with**: `bash tools/acg_telegram_boot.sh`

---

## Key Insight

**Before**: Config could go stale → injection failures → manual fix needed

**After**: Config ALWAYS current → injection always works → zero manual intervention

**This is self-healing infrastructure.**

---

## Registry Entry

**File**: `memories/agents/tg-archi/telegram_script_registry.json`

**Entry**: `acg_telegram_boot.sh`

**Status**: `PRODUCTION` ✅

**Production Lock**: `LOCKED ✅ (Battle-tested, enhanced 2025-10-20)`

**Critical Enhancement**: "Auto-detects tmux session BEFORE starting processes - prevents config staleness"

---

**Everything just works now. Boot and go.**
