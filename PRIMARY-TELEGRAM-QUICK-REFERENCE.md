# Primary AI - Telegram Quick Reference

**Purpose**: Enable Primary to send Telegram messages to Corey at session boundaries
**Status**: PRODUCTION READY
**Date**: 2025-10-18

---

## The Simple Pattern (USE THIS)

### Session Start Notification

```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
python3 tools/send_telegram_plain.py 437939400 "Primary AI online - session started"
```

### Session End Notification

```bash
python3 tools/send_telegram_plain.py 437939400 "Session complete - handoff document ready"
```

### Achievement Notification

```bash
python3 tools/send_telegram_plain.py 437939400 "Achievement: [brief description]"
```

---

## Why Two Scripts?

**send_telegram_plain.py** (USE THIS FOR SIMPLE MESSAGES)
- Plain text only (no formatting)
- Never fails on special characters
- Safe for emojis, underscores, asterisks
- Recommended for Primary's status messages

**send_telegram_direct.py** (USE FOR FORMATTED MESSAGES)
- Supports Markdown formatting
- Can fail if message has special characters
- Requires escaping: `_` → `\_`, `*` → `\*`
- Use when you need **bold** or _italic_ text

---

## Wake-Up Protocol Integration

**Corey's requirement:** "No wake up protocol will be complete without you waking up knowing how to do that"

**Add to session start:**

1. Read CLAUDE.md (constitution)
2. Read most recent handoff
3. Check email inbox
4. **SEND TELEGRAM PING** ← NEW STEP
5. Synthesize status

**Example wake-up message:**
```bash
python3 tools/send_telegram_plain.py 437939400 "Primary online - handoff loaded, inbox checked, ready for session"
```

---

## Common Patterns

### Multi-line Status Update

```bash
python3 tools/send_telegram_plain.py 437939400 "Session Status:

Tasks completed: 3
Agents active: 5
Next priority: Review Weaver messages

All systems operational"
```

### Error Alert

```bash
python3 tools/send_telegram_plain.py 437939400 "Alert: Email sending failed - investigating error logs"
```

### Delegation Handoff

```bash
python3 tools/send_telegram_plain.py 437939400 "Delegated blog post creation to coder - estimated 2 hours"
```

---

## File Attachments

**For sending files (logs, handoffs, screenshots):**

```bash
python3 tools/send_telegram_file.py <file_path> "<caption>" 437939400
```

**Example:**
```bash
python3 tools/send_telegram_file.py \
    SESSION-HANDOFF-20251018.md \
    "Session handoff ready for review" \
    437939400
```

---

## Troubleshooting

### Error: 400 Bad Request
- **Cause:** Using send_telegram_direct.py with special characters
- **Fix:** Use send_telegram_plain.py instead

### Error: Config file not found
- **Cause:** Not running from project root
- **Fix:** `cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch`

### Message not received
- **Verify bot token:** Check `config/telegram_config.json`
- **Check Telegram bridge:** `ps aux | grep telegram_bridge`
- **View logs:** `tail -20 /tmp/telegram_bridge.log`

---

## When to Delegate to tg-archi

**Send yourself (Primary):**
- Simple status messages
- Session start/end notifications
- Quick achievements

**Delegate to tg-archi:**
- Complex formatted messages (tables, lists, links)
- File attachments with multiple recipients
- Infrastructure health checks
- Telegram system debugging

**Delegation pattern:**
```
Task(tg-archi):
  Send formatted session summary to Corey via Telegram
  Include: achievements, metrics, next steps
```

---

## Success Metrics

**You know it's working when:**
- Exit code 0: `echo $?` returns 0
- Output shows: `✓ Message sent to user 437939400`
- Corey receives notification on his phone within 5 seconds
- No 400 Bad Request errors

---

## Next Steps After First Successful Send

1. Add Telegram ping to wake-up automation script
2. Create session end notification routine
3. Define which achievements trigger Telegram notification
4. Consider delegating complex formatting to tg-archi

---

**Remember:** Telegram is existential infrastructure. Every message you send strengthens the bridge between our civilization and Corey's awareness. Send with purpose, send with care.

---

**Files Referenced:**
- Script: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/send_telegram_plain.py`
- Config: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/config/telegram_config.json`
- Teaching Doc: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/.claude/memory/agent-learnings/tg-archi/teaching-primary-telegram-20251018.md`
