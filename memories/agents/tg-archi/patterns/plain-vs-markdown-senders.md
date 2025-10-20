# When to Use Plain vs Markdown Telegram Senders

**Quick Reference**: Which send script for which use case?

---

## The Two Senders

### 1. `send_telegram_plain.py` - Plain Text Only

**Use for**:
- Emoji-wrapped messages (`🤖🎯📱` ... `✨🔚`)
- Messages with special characters (*, _, `, [, ])
- Code snippets with potential Markdown conflicts
- Debugging output
- Any content where formatting might break

**How it works**:
- Sends text as-is (no parsing)
- All special characters are literal
- No formatting applied

**Example**:
```bash
python3 tools/send_telegram_plain.py 437939400 "🤖🎯📱\nThis is wrapped\n✨🔚"
# ✓ Sends successfully
```

---

### 2. `send_telegram_direct.py` - Markdown Parsing

**Use for**:
- Formatted messages (bold, italic, links)
- Human-readable reports
- Session summaries with structure
- Documentation snippets

**How it works**:
- Parses text as Markdown
- Converts to Telegram formatting
- Can reject malformed Markdown (400 error)

**Example**:
```bash
python3 tools/send_telegram_direct.py 437939400 "*Bold* and _italic_ text"
# ✓ Sends with formatting
```

**Danger**:
```bash
python3 tools/send_telegram_direct.py 437939400 "🤖🎯📱\nWrapped\n✨🔚"
# ✗ 400 Bad Request (emoji breaks Markdown parser)
```

---

## Which Scripts Use Which Sender?

### Plain Text Users (send_telegram_plain.py)

1. **telegram_monitor.py** (CRITICAL FIX 2025-10-18)
   - Sends emoji-wrapped messages
   - Cannot use Markdown parser

2. **Primary AI wake-up notifications** (recommended)
   - Simple alerts
   - Emoji status indicators

### Markdown Users (send_telegram_direct.py)

1. **Session summaries** (when manually sent)
   - Formatted reports
   - Human-readable structure

2. **Email drafts** (when sharing via Telegram)
   - Links, headers, formatting

---

## The Rule

**If message contains emoji wrappers or special characters → use `send_telegram_plain.py`**

**If message needs formatting → use `send_telegram_direct.py`**

**When in doubt → use `send_telegram_plain.py` (safer)**

---

## Historical Context

**Before 2025-10-18**:
- telegram_monitor.py used send_telegram_direct.py
- All wrapped messages failed with 400 errors
- Real-time mirroring broken

**After 2025-10-18**:
- telegram_monitor.py uses send_telegram_plain.py
- Wrapped messages deliver successfully
- Real-time mirroring working

**Lesson**: Infrastructure must match content format.

---

## Testing

**Test plain text sender**:
```bash
python3 tools/send_telegram_plain.py 437939400 "🤖 Test *special* chars [brackets] _underscores_"
# Should send all characters literally
```

**Test Markdown sender**:
```bash
python3 tools/send_telegram_direct.py 437939400 "*Bold* and _italic_ and [link](https://example.com)"
# Should send with formatting applied
```

---

## Related Files

- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/send_telegram_plain.py`
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/send_telegram_direct.py`
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_monitor.py`
