# Telegram JSONL Monitor Offset Persistence Fix

**Date**: 2025-10-20
**Agent**: coder
**Task**: Fix offset tracking bug in telegram_jsonl_monitor.py
**Status**: COMPLETE

## Problem

The JSONL monitor was detecting and sending wrapped messages successfully, but the `last_processed_offset` in the state file never advanced. Monitor would re-process the same messages after every restart.

**Evidence**:
- JSONL file grew from 116MB to 123MB (7MB new content)
- State file showed offset stuck at: 121,403,603
- Monitor sent 22 messages during session
- Logs showed successful detection and sending

## Root Cause

State persistence logic error in `watch_session_file()` method:

**Original Code Flow**:
```
while running:
    if line:
        process_line()
        update_offset_in_memory()  # ← Updated in memory
        # State save NEVER called here
    else:
        # Idle - no new lines
        save_state()  # ← Only saved during idle periods
```

**The Bug**: 
When monitor was actively processing messages, it never entered the `else` block, so state was never saved to disk. Offset updated in memory 22 times, but never persisted.

## Solution

Save state immediately after processing each wrapped message:

```python
if line:
    message_sent = self.process_jsonl_line(line, user_id)
    if message_sent:
        self.last_activity = datetime.now()

    # Update offset after processing each line
    current_offset = f.tell()
    self.state.update_offset(current_offset)

    # CRITICAL FIX: Save state after processing
    if message_sent:
        self.state.save_state()
        logger.debug(f"State saved at offset {current_offset}")
```

**Why This Works**:
- State saved immediately after sending each message
- Offset persists even if monitor crashes
- No longer dependent on idle periods for persistence
- Minimal performance impact (save only when message sent, not every line)

## Testing

**After fix, verify**:
1. Monitor processes new wrapped message
2. State file offset advances: `cat .tg_sessions/jsonl_monitor_state.json | jq .last_processed_offset`
3. Restart monitor → offset doesn't revert
4. No duplicate message sends

**Command**:
```bash
# Watch state file offset in real-time
watch -n 1 'cat .tg_sessions/jsonl_monitor_state.json | jq .last_processed_offset'
```

## Files Modified

**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_jsonl_monitor.py`
**Lines**: 415-428 (watch_session_file method)
**Backup**: `/tmp/telegram_jsonl_monitor_backup.py`

## Pattern Learned

**State Persistence Anti-Pattern**: Saving state only during idle periods

**Problem**: If system never idles (continuous activity), state never persists

**Best Practice**: Save state after each significant operation
- Message sent → save state immediately
- Offset updated → persist to disk
- Don't rely on idle loops for critical persistence

**Performance consideration**: Only save when necessary (message sent), not on every line processed

## Related

- Parent task: Telegram wrapper infrastructure
- Related memory: `telegram-monitor-v2-implementation-20251019.md`
- Monitor script: `tools/telegram_jsonl_monitor.py`
- State file: `.tg_sessions/jsonl_monitor_state.json`
