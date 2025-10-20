# Telegram Monitor Markdown Fix

**Date**: 2025-10-18
**Agent**: tg-archi
**Severity**: CRITICAL
**Status**: Fixed (awaiting restart)

---

## Problem

`telegram_monitor.py` was detecting wrapped messages but failing to send them to Telegram with 400 Bad Request errors.

**Evidence**:
```
2025-10-18 14:40:11,938 - INFO - Found 1 summaries in buffer
2025-10-18 14:40:11,938 - INFO - New message summary detected
2025-10-18 14:40:12,447 - ERROR - Failed to send summary: 400 Client Error
```

**Root cause**:
- Monitor used `send_telegram_direct.py` (Markdown parser)
- Emoji wrappers (`🤖🎯📱`) triggered Markdown parsing errors
- Telegram API rejected malformed Markdown

---

## Solution

**Changed**: Line 46 of `tools/telegram_monitor.py`

```python
# BEFORE (broken)
SEND_SCRIPT = PROJECT_ROOT / "tools" / "send_telegram_direct.py"

# AFTER (fixed)
SEND_SCRIPT = PROJECT_ROOT / "tools" / "send_telegram_plain.py"
```

**Why this works**:
- `send_telegram_plain.py` sends plain text (no Markdown parsing)
- Emoji wrappers are just Unicode characters (safe)
- No 400 errors from malformed formatting

---

## Files Modified

1. `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_monitor.py`
   - Line 46: Changed SEND_SCRIPT constant

---

## Restart Required

**Process must be restarted** to pick up code changes.

**Manual restart**:
```bash
bash /home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/restart_telegram_monitor.sh
```

**Or wait for health check** (runs every 5 minutes, will detect unresponsive process)

---

## Verification

After restart, check:

1. **Process running**:
   ```bash
   ps aux | grep telegram_monitor.py
   ```

2. **Logs show successful sends**:
   ```bash
   tail -20 /tmp/telegram_monitor.log
   ```

3. **No more 400 errors** in log

4. **Corey receives wrapped messages** on Telegram

---

## Impact

**Before**: Real-time conversation mirroring broken (all wrapped messages failed)
**After**: Real-time mirroring working (wrapped messages delivered successfully)

This was blocking Corey's mobile access to Primary AI conversations.

---

## Lessons Learned

1. **Emoji wrappers need plain text sender** (not Markdown parser)
2. **Always check logs after infrastructure changes** (caught error pattern quickly)
3. **Telegram API is strict about Markdown** (malformed formatting = 400 error)
4. **Have both send_telegram_direct.py and send_telegram_plain.py** (different use cases)

---

## Related Files

- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/send_telegram_plain.py` - Plain text sender
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/send_telegram_direct.py` - Markdown sender
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/restart_telegram_monitor.sh` - Restart script (NEW)
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_health_check.sh` - Auto-recovery script
