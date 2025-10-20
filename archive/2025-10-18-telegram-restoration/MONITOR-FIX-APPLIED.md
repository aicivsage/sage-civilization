# Telegram Monitor Buffer Shrinking Fix Applied

## Fix Applied: 2025-10-18

**File Modified**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_monitor.py`

**Lines Changed**: 265-283

---

## The Problem

Monitor failed to detect new content when tmux buffer shrank due to scrolling:

- Monitor initialized at position 543
- Tmux buffer scrolled, now 542 lines
- Monitor checked: `if current_position (542) > last_buffer_position (543)` → FALSE
- Result: Never scanned, never detected new messages

---

## The Fix

Changed detection logic at line 265 from:

```python
# OLD (BROKEN):
if buffer and current_position > last_buffer_position:
```

To:

```python
# NEW (FIXED):
if buffer and current_position != last_buffer_position:
    # Handle buffer shrinking (tmux scrolling)
    if current_position < last_buffer_position:
        logger.info(f"Buffer shrunk ({last_buffer_position} → {current_position}), resetting position")
        last_buffer_position = max(0, current_position - 50)  # Go back 50 lines to catch recent content

    # Only scan NEW lines since last poll (delta detection)
    if current_position > last_buffer_position:
        # ... existing scanning logic ...
    else:
        # Buffer shrunk, no new content beyond reset point
        summaries = []
```

**Behavior Now**:
- If buffer grows: Scan new lines (original behavior)
- If buffer shrinks: Reset position back 50 lines to catch recent content
- Delta detection still works (only scan lines since last poll)

---

## Manual Steps Required

**Execute these commands to restart monitor with fix:**

```bash
# 1. Kill current monitor process
pkill -f telegram_monitor.py

# 2. Clear state to start fresh
rm -f /home/corey/projects/AI-CIV/grow_gemini_deepresearch/.tg_sessions/monitor_state.json

# 3. Restart monitor
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
nohup python3 tools/telegram_monitor.py --interval 60 > /tmp/telegram_monitor.log 2>&1 &

# 4. Check monitor is running
ps aux | grep telegram_monitor.py

# 5. Tail logs to verify
tail -f /tmp/telegram_monitor.log
```

---

## Test After Restart

1. **Wrap message in tmux**:
   ```
   🤖🎯📱
   TEST MESSAGE: Monitor should detect this even after buffer shrinking
   ✨🔚
   ```

2. **Wait 60 seconds** (monitor polls every minute)

3. **Check Telegram** - Should receive wrapped test message

4. **Verify logs**:
   ```bash
   tail -20 /tmp/telegram_monitor.log
   ```

Expected log output:
- "Buffer shrunk (X → Y), resetting position" (if buffer shrank)
- "Scanning N new lines (position X → Y)"
- "Found 1 summaries in new content"
- "Sent message summary to user 437939400"

---

## Fix Status

- [x] Code fixed in telegram_monitor.py
- [ ] Monitor killed (manual step required)
- [ ] State cleared (manual step required)
- [ ] Monitor restarted (manual step required)
- [ ] Test message wrapped (manual step required)
- [ ] Delivery confirmed (manual step required)

---

**Next Action**: Execute manual steps above to complete fix deployment and test.

**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_monitor.py` (lines 265-283)
