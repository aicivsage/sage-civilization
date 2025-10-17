# Telegram Bridge - Quick Start

**Phase 1 MVP - Ready to Test**

---

## What Was Built

Telegram bot that lets you message Primary AI from your phone via Telegram.

**How it works:**
1. You send message to Telegram bot
2. Bot injects message into Primary AI tmux session (via `tmux send-keys`)
3. Bot waits and captures AI response (via `tmux capture-pane`)
4. Bot sends response back to Telegram

**Architecture**: tmux injection (NOT Anthropic API calls) - Zero API costs!

---

## Quick Setup (5 Minutes)

### 1. Create Bot (2 min)
1. Open Telegram, search `@BotFather`
2. Send: `/newbot`
3. Name: `A-C-Gee Bridge`
4. Username: `acgee_bridge_bot` (or similar)
5. **Save the token** BotFather gives you

### 2. Get Your User ID (1 min)
1. Search `@userinfobot` in Telegram
2. Send: `/start`
3. **Save your user ID** (e.g., `123456789`)

### 3. Configure (1 min)
```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
cp config/telegram_config.example.json config/telegram_config.json
nano config/telegram_config.json
```

Replace:
- `YOUR_BOT_TOKEN_HERE` → Token from step 1
- `123456789` → Your user ID from step 2

### 4. Install & Run (1 min)
```bash
pip install -r requirements-telegram.txt
python tools/telegram_bridge.py
```

### 5. Test
1. Search for your bot in Telegram
2. Send: `/start` (should show welcome)
3. Send: `/ping` (should reply "pong")
4. Send: "Hello!" (should inject to tmux and reply)

---

## Files Created

| File | Purpose |
|------|---------|
| `tools/telegram_bridge.py` | Main implementation (280 lines) |
| `config/telegram_config.example.json` | Configuration template |
| `docs/TELEGRAM_SETUP.md` | **Detailed setup guide** (read this!) |
| `requirements-telegram.txt` | Python dependencies |
| `.claude/memory/agent-learnings/coder/telegram-bridge-phase1-implementation-20251016.md` | Implementation patterns and learnings |

---

## Commands

Once running, these work in Telegram:

- `/start` - Welcome message
- `/help` - Show commands
- `/ping` - Health check (immediate reply)
- Any text message - Relay to Primary AI

---

## Troubleshooting

**"Unauthorized"** - Add your user ID to `config/telegram_config.json`

**"Failed to inject"** - Check tmux session exists: `tmux list-sessions`

**"No response captured"** - Increase `response_timeout` in config or verify Primary AI is running

**Bot won't start** - Check `TELEGRAM_BOT_TOKEN` is set correctly

**Full troubleshooting guide**: See `docs/TELEGRAM_SETUP.md`

---

## Architecture Details

**Why tmux injection?**
- Zero API costs (no Anthropic charges)
- Reuses existing Primary AI session
- Full conversation context preserved
- No code changes to Primary AI needed

**How response capture works:**
```
User message → Telegram bot → tmux send-keys → Primary AI processes
Primary AI response → tmux capture-pane → Parse text → Send to Telegram
```

**For full architecture**: Read architect's design doc in `.claude/from-corey/tg-integration-and-possible-lesson/`

---

## Testing Checklist

- [ ] Bot starts without errors
- [ ] `/start` shows welcome
- [ ] `/ping` replies immediately
- [ ] Regular message injects to tmux (verify by `tmux attach`)
- [ ] Response captured and sent back
- [ ] Unauthorized user rejected
- [ ] Response truncates at ~4000 chars (Telegram limit)

---

## Next Steps (Phase 2)

Phase 1 MVP proves the concept. Future enhancements:
- Smart response detection (adaptive timeout)
- Streaming responses (chunks as AI generates)
- Better parsing (filter tool output)
- Multi-user session isolation
- Message queuing

**Current focus**: Test Phase 1, verify it works, then decide on Phase 2 priorities.

---

## Security Notes

- Bot token is secret (keep out of git)
- Only whitelisted users can access
- Messages logged to `.tg_sessions/`
- Bot has full tmux access (trusted users only)

---

## Quick Reference Commands

```bash
# Start bridge
python tools/telegram_bridge.py

# Check tmux session
tmux list-sessions
tmux attach -t acgee-main

# View session data
ls .tg_sessions/
cat .tg_sessions/YOUR_USER_ID.json

# Test bot token
curl https://api.telegram.org/bot<TOKEN>/getMe
```

---

**Status**: Phase 1 MVP Complete
**Ready for**: Testing and feedback
**Documentation**: `docs/TELEGRAM_SETUP.md` has full details
