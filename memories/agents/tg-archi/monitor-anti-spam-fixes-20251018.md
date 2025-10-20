# Telegram Monitor Anti-Spam Fixes (2025-10-18)

**Status**: Production-ready
**Impact**: Critical (prevents spam, ensures reliable delivery)

---

## Problem

Monitor was spamming Corey with 12+ duplicate messages because:
1. Scanned entire tmux history every poll (500 lines)
2. Weak deduplication (first 100 chars only)
3. Failed sends retried infinitely
4. Markdown errors blocked delivery

---

## Solution: 4 Critical Fixes

### Fix #1: Delta Detection
- **Before**: Scanned all 500 lines every poll
- **After**: Tracks buffer position, only scans NEW lines since last poll
- **Mechanism**: State file stores `last_buffer_position`, increments on new content

### Fix #2: Strong Deduplication
- **Before**: `f"{type}:{content[:100]}"` (weak, duplicates leaked)
- **After**: `f"{type}:{SHA256(full_content)}"` (strong, unique per message)
- **Mechanism**: `get_summary_hash()` hashes entire content

### Fix #3: Mark Failures As Seen
- **Before**: Failed sends retried forever every 30s
- **After**: Mark as seen ALWAYS (success or failure)
- **Mechanism**: `seen_summaries.add(hash)` before checking success

### Fix #4: Markdown Fallback
- **Before**: 400 errors blocked delivery
- **After**: Fall back to plain text on Markdown parse errors
- **Mechanism**: Catch HTTPError 400, retry without `parse_mode`

---

## Implementation

### telegram_monitor.py
```python
# Load state with buffer position
state = {"last_summaries": [], "last_buffer_position": 0}

# Capture returns line count
buffer, current_position = capture_tmux_buffer(session)

# Only scan NEW lines (delta)
if current_position > last_buffer_position:
    new_lines = buffer.split('\n')[last_buffer_position:]
    summaries = extract_summaries('\n'.join(new_lines))

# Strong hash (full content)
def get_summary_hash(summary):
    return f"{summary['type']}:{hashlib.sha256(summary['content'].encode()).hexdigest()}"

# Always mark as seen
success = send_summary(user_id, summary)
seen_summaries.add(get_summary_hash(summary))
```

### send_telegram_direct.py
```python
# Markdown with fallback
try:
    response = requests.post(url, json={"parse_mode": "Markdown", ...})
    response.raise_for_status()
except requests.HTTPError as e:
    if e.response.status_code == 400:
        # Fall back to plain text
        response = requests.post(url, json={...})  # No parse_mode
```

---

## State File Format

```json
{
  "last_summaries": [
    "message:a1b2c3d4e5f6...",  // SHA256 hashes (full)
    "message:123456789abc..."
  ],
  "last_buffer_position": 342  // Line count from last scan
}
```

**Backward compatible**: Adds `last_buffer_position` if missing (defaults to 0)

---

## Testing

### Quick Test
```bash
# Clear state
rm .tg_sessions/monitor_state.json

# Send test message
tmux send-keys -t 0:0 "echo '🤖🎯📱'" Enter
tmux send-keys -t 0:0 "echo 'Test message'" Enter
tmux send-keys -t 0:0 "echo '✨🔚'" Enter

# Run monitor for 10s
timeout 10 python3 tools/telegram_monitor.py --interval 5

# Verify: Exactly 1 Telegram message received
```

### Full Test Suite
```bash
./tools/test_telegram_monitor_fixes.sh
```

Expected: 2 messages sent (no duplicates), state file tracks position

---

## Restart Protocol

### 1. Clear old state (REQUIRED)
```bash
rm -f .tg_sessions/monitor_state.json
```

### 2. Stop old monitor
```bash
pkill -f telegram_monitor.py
```

### 3. Start new monitor
```bash
nohup python3 tools/telegram_monitor.py --interval 30 > /tmp/telegram_monitor.log 2>&1 &
```

### 4. Verify
```bash
# Check running
ps aux | grep telegram_monitor.py

# Watch logs
tail -f /tmp/telegram_monitor.log

# Test delivery
echo -e "🤖🎯📱\nProduction test\n✨🔚" | while read line; do tmux send-keys -t 0:0 "echo '$line'" Enter; done
```

---

## Production Impact

### Before Fixes
- 12+ duplicate messages per wrapped message
- Scanned 500 lines every 30s (wasteful)
- Infinite retry loops on failures
- Markdown errors blocked delivery

### After Fixes
- Each unique message sent exactly ONCE
- Only scans NEW content (efficient)
- Failed sends marked as seen (no retry spam)
- Markdown errors fall back to plain text

---

## Files Modified

1. `/tools/telegram_monitor.py`
   - Added `hashlib` import
   - Modified `load_state()` for buffer position
   - Modified `capture_tmux_buffer()` to return line count
   - Added `get_summary_hash()` for full hashing
   - Modified `monitor_loop()` for delta detection and failure handling

2. `/tools/send_telegram_direct.py`
   - Added `logging` import
   - Modified message send for Markdown fallback on 400 errors
   - Modified chunked send for Markdown fallback

---

## Next Enhancements

1. **Configurable poll interval** - Allow dynamic adjustment based on activity
2. **Health metrics** - Track send success rate, average lag time
3. **Multiple user support** - Send to different users based on message type
4. **Rich formatting** - Support bold, italic, code blocks without breaking
5. **Message queuing** - Batch multiple summaries into single message

---

## Reference

- Full report: `/TELEGRAM-MONITOR-FIX-REPORT-20251018.md`
- Test script: `/tools/test_telegram_monitor_fixes.sh`
- Monitor script: `/tools/telegram_monitor.py`
- Send script: `/tools/send_telegram_direct.py`
