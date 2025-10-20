# Teaching Primary: Telegram Message Sending

**Date**: 2025-10-18
**Agent**: tg-archi
**Purpose**: Document correct Telegram message sending patterns for Primary AI

---

## The Problem

Primary attempted to send a Telegram message and received a 400 Bad Request error:

```bash
python3 tools/send_telegram_direct.py 437939400 "message here"
# ERROR: 400 Client Error: Bad Request
```

**Root Cause**: The `send_telegram_direct.py` script uses `parse_mode: "Markdown"` which fails when messages contain characters that Markdown interprets as special syntax (underscores, asterisks, some emojis).

---

## The Solution

### Option 1: Plain Text Messages (RECOMMENDED FOR PRIMARY)

**For simple status messages without formatting:**

```bash
python3 tools/send_telegram_direct.py 437939400 "Testing Telegram - Primary learning to communicate"
```

**Why avoid special characters:**
- Emojis can conflict with Markdown parsing
- Underscores create italics: `_word_` → _word_
- Asterisks create bold: `*word*` → **word**
- Brackets create links: `[text](url)`

**Safe pattern:**
- Use plain English
- Avoid: `_` `*` `[` `]` `` ` `` `~` `>`
- Add emojis ONLY if you know they're safe (most common emojis work, but some don't)

### Option 2: Escape Special Characters

**If you MUST use special characters:**

The script already handles Markdown parsing, so you need to escape:
- `_` → `\_`
- `*` → `\*`
- `[` → `\[`
- `` ` `` → `` \` ``

**Example:**
```bash
# BAD (will fail)
python3 tools/send_telegram_direct.py 437939400 "Task_name completed"

# GOOD (escaped)
python3 tools/send_telegram_direct.py 437939400 "Task\_name completed"
```

### Option 3: Fix the Script (FUTURE ENHANCEMENT)

**Modify send_telegram_direct.py to:**
1. Remove `parse_mode` for plain messages
2. Add optional `--markdown` or `--html` flag for formatted messages
3. Auto-detect and escape special characters

**This is a FUTURE task** - for now, use plain text.

---

## Working Examples

### 1. Session Wake-Up Ping (SIMPLE)

```bash
python3 tools/send_telegram_direct.py 437939400 "Primary AI online - session started"
```

### 2. Status Update (PLAIN TEXT)

```bash
python3 tools/send_telegram_direct.py 437939400 "Git specialist agent completed PR merge - branch clean-main is now active"
```

### 3. Multi-line Message (SAFE)

```bash
python3 tools/send_telegram_direct.py 437939400 "Session Update:

Achievements:
- Telegram infrastructure verified
- Primary learned message sending
- Wake-up protocol enhanced

Status: All systems operational"
```

### 4. With Safe Emoji (TEST FIRST)

```bash
# Most common emojis work fine
python3 tools/send_telegram_direct.py 437939400 "System check complete"
```

**NOTE:** Test emojis first - if you get 400 error, remove emoji and resend.

---

## Correct Command Format

**Standard invocation:**
```bash
python3 tools/send_telegram_direct.py <user_id> "<message>"
```

**Parameters:**
- `<user_id>`: Corey's Telegram ID = `437939400`
- `"<message>"`: Message text in quotes (supports multi-line)

**Success indicators:**
- Exit code 0
- Output: `✓ Message sent to user 437939400`

**Failure indicators:**
- Exit code 1
- Output: `✗ Failed to send message` or `ERROR: 400 Client Error`

---

## Integration into Wake-Up Protocol

**Primary should:**

1. **At session start:**
   ```bash
   python3 tools/send_telegram_direct.py 437939400 "Primary AI online - session started at $(date +%H:%M)"
   ```

2. **At session end:**
   ```bash
   python3 tools/send_telegram_direct.py 437939400 "Session complete - handoff document ready"
   ```

3. **On significant achievements:**
   ```bash
   python3 tools/send_telegram_direct.py 437939400 "Achievement unlocked: [brief description]"
   ```

4. **On errors requiring attention:**
   ```bash
   python3 tools/send_telegram_direct.py 437939400 "Alert: [error description] - investigating"
   ```

---

## Advanced: File Sending

**For sending files (logs, screenshots, documents):**

```bash
python3 tools/send_telegram_file.py <file_path> "<caption>" <user_id>
```

**Example:**
```bash
python3 tools/send_telegram_file.py \
    /home/corey/projects/AI-CIV/grow_gemini_deepresearch/SESSION-HANDOFF-20251018.md \
    "Session handoff document ready for review" \
    437939400
```

**Documentation:** See `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/README-TELEGRAM-FILE-SENDING.md`

---

## Troubleshooting

### Error: 400 Bad Request

**Cause:** Message contains Markdown special characters
**Fix:** Remove or escape special characters (`_`, `*`, `[`, `]`, `` ` ``)

### Error: Config file not found

**Cause:** Script can't find `config/telegram_config.json`
**Fix:** Run from project root: `cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch`

### Error: Bot token invalid

**Cause:** Bot token expired or incorrect in config
**Fix:** Verify token in `config/telegram_config.json`

### Message too long

**Cause:** Message exceeds 4096 characters
**Fix:** Script auto-chunks long messages (handled automatically)

---

## What Primary Learned

1. **Telegram messages require careful formatting**
   - Plain text is safest for status messages
   - Markdown special characters cause failures
   - Test emoji messages before relying on them

2. **The correct invocation pattern:**
   ```bash
   cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
   python3 tools/send_telegram_direct.py 437939400 "message"
   ```

3. **Wake-up protocol is incomplete without Telegram ping**
   - Corey expects notification when Primary wakes up
   - Mobile access requires Telegram communication
   - Session boundaries should trigger Telegram updates

4. **Primary can delegate to tg-archi for complex messages**
   - Simple status: Primary sends directly
   - Complex formatting: Delegate to tg-archi
   - File attachments: Always delegate to tg-archi

---

## Next Steps for Primary

1. Update wake-up protocol to include Telegram ping
2. Test message sending at session start
3. Add Telegram notification to session end routine
4. Consider delegating complex Telegram tasks to tg-archi

---

## Next Steps for tg-archi

1. Enhance `send_telegram_direct.py` to handle special chars gracefully
2. Add `--plain` flag to force plain text mode (no parse_mode)
3. Document emoji compatibility matrix
4. Propose Markdown/HTML formatting guide for Primary

---

**Status**: Primary now understands Telegram message sending
**Validation**: Awaiting test message confirmation from Primary
