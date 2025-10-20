# Telegram Monitor Double-Wrapping Bug - Fixed 2025-10-19

## The Bug

**Symptom**: Monitor logged "Sent message summary" but Corey never received messages.

**Root Cause**: Monitor was adding wrapper emojis TWICE:

```python
# BROKEN CODE:
message = f"🤖🎯📱\n\n{summary['content']}\n\n✨🔚"
# Creates: 🤖🎯📱\n\n🤖🎯📱\n[content]\n✨🔚\n\n✨🔚
```

## Why It Failed Silently

1. Double-wrapped message causes Markdown parse failure
2. `send_telegram_direct.py` falls back to plain text
3. Fallback returns exit code 0 (no exception)
4. Monitor sees successful exit, logs "Sent"
5. But message never actually delivered to Telegram

## The Fix

**Remove double-wrapping:**
```python
# FIXED CODE:
message = summary['content']  # Already wrapped by Primary
```

**Added debugging:**
```python
# Log subprocess output
if result.stdout:
    logger.info(f"Send script output: {result.stdout.strip()}")
if result.stderr:
    logger.warning(f"Send script stderr: {result.stderr.strip()}")
```

## Key Learning

**Primary wraps BEFORE tmux output:**
- Primary writes: `🤖🎯📱\n[content]\n✨🔚` to tmux
- Monitor extracts: `summary['content']` (already wrapped)
- Monitor should send: `summary['content']` AS-IS

**Monitor should NOT add wrappers** - they're already there!

## Testing

After fix, test with:
```
🤖🎯📱
TEST: Monitor fix at $(date +%H:%M:%S)
✨🔚
```

Should arrive on Telegram within 30 seconds.

## Prevention

1. ALWAYS log subprocess stdout/stderr
2. Test end-to-end delivery after monitor changes
3. Keep registry "last_verified_working" current
4. Document wrapping protocol in PRIMARY_TELEGRAM_PROTOCOL.md

## Files Changed

- `tools/telegram_monitor.py` (line 263-289)
- `memories/agents/tg-archi/telegram_script_registry.json` (updated notes)

## Related Issues

This is the SECOND time we've broken the monitor:
- **2025-10-18**: Changed to `send_telegram_plain.py` (wrong sender)
- **2025-10-19**: Double-wrapping bug (wrong message format)

**Pattern**: Monitor is fragile, needs integration tests.
