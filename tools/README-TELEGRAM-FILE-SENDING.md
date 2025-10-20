# Telegram File Sending - Quick Start

**New capability as of 2025-10-17**: Send file attachments via Telegram Bot API

---

## Basic Usage

```bash
# Send file to Corey (default user 437939400)
python3 tools/send_telegram_file.py path/to/file.pdf

# Send with caption
python3 tools/send_telegram_file.py handoff.md "Session handoff document"

# Send to custom user
python3 tools/send_telegram_file.py report.txt "Report" 123456789
```

---

## Limits

- **Max file size:** 50 MB
- **Max caption:** 1024 characters (auto-truncates)
- **Supported formats:** All file types
- **Timeout:** 30 seconds

---

## Common Use Cases

### Session Handoffs
```bash
python3 tools/send_telegram_file.py \
  HANDOFF-SESSION-20251017.md \
  "Session complete! Full handoff attached."
```

### Error Logs
```bash
python3 tools/send_telegram_file.py \
  /tmp/error.log \
  "Error log - needs review"
```

### Memory Backups
```bash
python3 tools/send_telegram_file.py \
  memories/agents/my-agent/performance_log.json \
  "Weekly performance backup"
```

---

## Testing

Run test suite:
```bash
bash tools/test_telegram_file_sending.sh
```

---

## Documentation

**Full documentation:**
- `memories/agents/tg-archi/file-sending-capability.md`

**Quick reference:**
- `memories/agents/tg-archi/patterns/file-sending-quick-reference.md`

**Complete report:**
- `TG-ARCHI-FILE-SENDING-COMPLETE-20251017.md`

---

## Questions?

Ask **tg-archi** agent - I'm the Telegram infrastructure specialist!

```
Task(tg-archi):
  Help with file sending: [your question]
```

---

**Created:** 2025-10-17 by tg-archi
**Status:** Production-ready (pending test confirmation)
