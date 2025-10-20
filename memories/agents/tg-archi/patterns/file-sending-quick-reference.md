# Quick Reference: Telegram File Sending

**Purpose**: Fast lookup for sending files via Telegram
**Script**: `tools/send_telegram_file.py`
**Status**: Ready for testing

---

## Basic Usage

```bash
# Send file (default user: Corey 437939400)
python3 tools/send_telegram_file.py path/to/file.pdf

# With caption
python3 tools/send_telegram_file.py handoff.md "Session handoff - Oct 17"

# With custom user ID
python3 tools/send_telegram_file.py report.txt "Report" 123456789
```

---

## Common Use Cases

### Session Handoff Document
```bash
python3 tools/send_telegram_file.py \
  HANDOFF-SESSION-20251017.md \
  "Session complete! Full handoff attached." \
  437939400
```

### Error Logs
```bash
python3 tools/send_telegram_file.py \
  /tmp/error.log \
  "Error log - needs review"
```

### Memory Archive
```bash
python3 tools/send_telegram_file.py \
  memories/agents/tg-archi/performance_log.json \
  "Weekly performance backup"
```

---

## Limits & Constraints

- **Max file size**: 50 MB (bot uploads)
- **Max caption**: 1024 chars (auto-truncates with "...")
- **Timeout**: 30 seconds
- **Supported formats**: All file types

---

## Error Handling

**File not found:**
```
ERROR: File not found: nonexistent.txt
Exit code: 1
```

**File too large:**
```
ERROR: File too large (51.00 MB). Max: 50 MB
Exit code: 1
```

**Network error:**
```
ERROR: Network error: Connection timeout
Exit code: 1
```

---

## Integration with Text Messages

**Use files for:**
- Documents >2000 chars
- Logs >500 lines
- Session handoffs
- Configuration backups

**Use text messages for:**
- Session summaries
- Quick notifications
- Emoji-wrapped updates (Telegram monitor)

---

**Last Updated**: 2025-10-17
