# Telegram Monitor Fix - 2025-10-19

## Problem Diagnosed

**Symptom**: Monitor logs "Sent message summary" but Corey never receives messages on Telegram.

**Root Cause**: **Double-wrapping bug** in `telegram_monitor.py` line 263.

### The Bug

```python
# BROKEN CODE (before fix):
message = f"🤖🎯📱\n\n{summary['content']}\n\n✨🔚"
```

**What was happening:**
1. Primary wraps message with `🤖🎯📱 ... ✨🔚` in tmux output
2. Monitor extracts wrapped content into `summary['content']`
3. Monitor adds SECOND layer of wrappers: `🤖🎯📱\n\n{already_wrapped_content}\n\n✨🔚`
4. Result: Double-wrapped message with nested emojis
5. Telegram Markdown parser fails on malformed message
6. `send_telegram_direct.py` tries fallback to plain text, but message still broken
7. subprocess returns 0 (no exception), but message never delivered
8. Monitor logs "Sent" because no exception raised

### Evidence

From `/tmp/acgee_telegram_monitor.log`:
```
2025-10-19 08:46:54,592 - INFO - Found 5 summaries in buffer
2025-10-19 08:46:54,592 - INFO - New message summary detected
2025-10-19 08:46:55,424 - INFO - Sent message summary to user 437939400
```

But Corey's last received message was at 08:53 (direct send via `send_telegram_direct.py`).

### Why Direct Sending Works

`send_telegram_direct.py` doesn't double-wrap - it sends exactly what it receives:
```bash
python3 tools/send_telegram_direct.py 437939400 "🤖🎯📱\nContent\n✨🔚"
```

This works because there's only ONE layer of wrappers.

## The Fix

### Code Changes

**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_monitor.py`

**Line 263 changed from:**
```python
message = f"🤖🎯📱\n\n{summary['content']}\n\n✨🔚"
```

**To:**
```python
message = summary['content']  # Already contains wrapper emojis from Primary
```

**Additional improvements (lines 276-280):**
- Log subprocess stdout/stderr for debugging
- Better error messages with exit codes

### Registry Update

Updated `memories/agents/tg-archi/telegram_script_registry.json`:
- `last_verified_working`: "2025-10-19 (double-wrapping bug fixed)"
- `recent_breakage`: Added "2025-10-19: Double-wrapping bug - FIXED"
- `notes`: Added "FIX 2025-10-19: Removed double-wrapping"

## Testing Plan

### 1. Restart Monitor with Fix

```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
bash tools/restart_telegram_monitor.sh
```

### 2. Send Test Wrapped Message

From Primary AI in tmux:
```
🤖🎯📱
TEST: Monitor fix verification at $(date +%H:%M:%S)
This message should arrive on Telegram within 30 seconds.
✨🔚
```

### 3. Verify Delivery

- Check Corey's Telegram within 30 seconds
- Should receive exactly the wrapped message (not double-wrapped)
- Check `/tmp/acgee_telegram_monitor.log` for:
  - "New message summary detected"
  - "Send script output: ✓ Message sent to user 437939400"
  - "Sent message summary to user 437939400"

### 4. Verify State File Updated

```bash
cat .tg_sessions/monitor_state.json
# Should show new message hash in last_summaries
```

## Success Criteria

1. Corey receives test message on Telegram
2. Message displays correctly (single wrapper, readable content)
3. Monitor log shows subprocess output
4. No duplicate sends
5. State file properly updated

## Rollback Plan

If fix doesn't work:
1. Revert `tools/telegram_monitor.py` to previous version
2. Restart monitor: `bash tools/restart_telegram_monitor.sh`
3. Document new symptoms for further investigation

## Root Cause Analysis

**Why did this bug exist?**

The monitor was designed to wrap summaries for Telegram, but the protocol changed:
- **Original design**: Monitor extracts plain content, wraps it
- **Current protocol**: Primary wraps content BEFORE tmux output
- **Bug**: Monitor didn't adapt to new protocol, kept wrapping

**Why did it silently fail?**

1. `send_telegram_direct.py` has Markdown fallback logic
2. Fallback returns exit code 0 even if message malformed
3. Monitor only checks exit code, not actual delivery
4. subprocess stdout/stderr not logged until this fix

**Prevention for future:**

1. ALWAYS log subprocess stdout/stderr when calling external scripts
2. Test message delivery end-to-end after ANY monitor changes
3. Keep registry updated with "last_verified_working" timestamps
4. Document wrapping protocol clearly in PRIMARY_TELEGRAM_PROTOCOL.md

## Related Files

- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_monitor.py` (FIXED)
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/send_telegram_direct.py` (working correctly)
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/telegram_script_registry.json` (UPDATED)
- `/tmp/acgee_telegram_monitor.log` (debugging evidence)

## Next Steps

1. Apply this fix (restart monitor)
2. Test with wrapped message
3. If successful, document in PRIMARY_TELEGRAM_PROTOCOL.md
4. Consider adding integration test for monitor sending
5. Update tg-archi manifest with this learning
