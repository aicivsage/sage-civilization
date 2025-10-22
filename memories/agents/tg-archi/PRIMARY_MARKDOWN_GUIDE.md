# Primary AI - Telegram Markdown Quick Reference

**Date**: 2025-10-20
**Status**: PRODUCTION - Markdown enabled
**For**: Primary AI usage in wrapped messages

---

## How to Use Markdown in Wrapped Messages

Wrapped messages now support Telegram Markdown formatting automatically!

### Basic Syntax

```
🤖🎯📱

*Bold text* - Use single asterisks
_Italic text_ - Use underscores
\`inline code\` - Use backticks
[Link text](https://example.com) - Standard markdown links

✨🔚
```

---

## Formatting Reference

| You Want | Telegram Markdown | Example |
|----------|------------------|---------|
| **Bold** | `*text*` | `*Status:* Complete` |
| _Italic_ | `_text_` | `_Priority:_ High` |
| `Code` | `` `text` `` | `` `bash command` `` |
| Link | `[text](URL)` | `[Documentation](https://example.com)` |

---

## Common Patterns for Session Summaries

### Session Start
```
🤖🎯📱

*Primary AI online* - session started
_Status:_ All systems operational

Next priority: Load context from registry

✨🔚
```

### Session Complete
```
🤖🎯📱

*Session Complete*

_Duration:_ 2 hours
_Agent:_ Primary AI

*Achievements:*
- Telegram markdown formatting implemented
- Testing complete
- Documentation updated

*Next priority:* Production deployment

*Handoff:* SESSION-HANDOFF-20251020.md

✨🔚
```

### Progress Update
```
🤖🎯📱

*Progress Update*

Working on: Health gamification phase 1

_Status:_ Implementation in progress
_Blocker:_ None

*Next steps:*
- Complete user model
- Deploy to staging
- Test with real data

✨🔚
```

### Error Alert
```
🤖🎯📱

*Alert: Error Detected*

_Component:_ Email monitor
_Severity:_ Medium

*Issue:* Inbox check failed

*Action taken:* Retry scheduled
*Escalation:_ Will notify if persists

✨🔚
```

---

## Important Notes

### What Works
- Single asterisk for bold: `*text*`
- Underscores for italic: `_text_`
- Backticks for code: `` `text` ``
- Standard markdown links: `[text](URL)`

### What DOESN'T Work
- Double asterisks: `**text**` (use `*text*` instead)
- Headers: `# Heading` (not supported)
- Code blocks with triple backticks: ``` (not well supported)
- Nested formatting (keep it simple)

### Safety Features
- If markdown parsing fails, message auto-sends as plain text
- You'll never lose a message due to formatting errors
- Logs show warnings if fallback occurs
- No need to escape special chars in most cases

---

## Best Practices

### DO
- Use bold for headings: `*Session Complete*`
- Use italic for metadata: `_Duration:_ 2 hours`
- Use code for technical terms: `` `bash command` ``
- Use links for references: `[Handoff doc](file://...)`
- Keep formatting simple and clear

### DON'T
- Overuse formatting (makes message noisy)
- Mix too many formats on one line
- Use unmatched special characters
- Rely on complex markdown features

### Example: Well-Formatted Message
```
🤖🎯📱

*Telegram Markdown Feature Complete*

_Status:_ Ready for production
_Agent:_ tg-archi

*Changes:*
- send_telegram_plain.py enhanced
- telegram_jsonl_monitor.py updated
- Documentation complete

*Testing:*
Run: \`bash tools/test_telegram_markdown.sh\`

*Next:* Restart monitor and verify

[Full details](memories/agents/tg-archi/markdown-formatting-enhancement.md)

✨🔚
```

---

## Testing

### Quick Test
```bash
python3 tools/send_telegram_plain.py 437939400 "*Bold test*" --markdown
```

### Full Test Suite
```bash
bash tools/test_telegram_markdown.sh
```

### Verify in Production
1. Send a wrapped message with markdown
2. Check Telegram on phone
3. Verify formatting displays correctly
4. Check logs: `tail /tmp/telegram_jsonl_monitor.log`

---

## Troubleshooting

### Message Shows Raw Markdown
**Problem:** You see `*text*` instead of bold text

**Solutions:**
1. Verify JSONL monitor is running with new code
2. Check monitor process: `ps aux | grep ACG_telegram_jsonl_monitor`
3. Restart monitor: `pkill -f ACG_telegram_jsonl_monitor && python3 tools/telegram_jsonl_monitor.py --start-from-now --session-file [SESSION].jsonl &`

### Message Not Arriving
**Problem:** Wrapped message doesn't reach Telegram

**Solutions:**
1. Check monitor logs: `tail -50 /tmp/telegram_jsonl_monitor.log`
2. Look for errors or warnings
3. Verify wrapper syntax: `🤖🎯📱 ... ✨🔚`
4. Check JSONL monitor is watching correct session file

### Formatting Looks Wrong
**Problem:** Text displays incorrectly formatted

**Solutions:**
1. Check Telegram markdown syntax (single `*`, not double `**`)
2. Verify backticks escaped: `` \`text\` ``
3. Check logs for fallback warnings
4. Test with simpler formatting first

---

## Remember

**Every wrapped message automatically gets Markdown formatting now!**

No extra steps needed - just use the formatting syntax in your wrapped messages and they'll display beautifully on Corey's phone.

**The formatting happens automatically when JSONL monitor detects and sends your wrapped message.**

---

**Happy formatting! 🎨**
