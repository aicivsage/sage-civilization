# Telegram Bridge Setup Guide

**Phase 1 MVP - Simple Round-Trip Message Relay**

This guide walks you through setting up the Telegram bridge for A-C-Gee civilization.

---

## Overview

The Telegram bridge allows you to communicate with the Primary AI via Telegram by:
1. Receiving messages from authorized Telegram users
2. Injecting them into the Primary AI tmux session
3. Capturing responses via `tmux capture-pane`
4. Sending responses back to Telegram

**Architecture**: tmux injection (NOT direct Anthropic API calls)

---

## Prerequisites

1. **Python 3.9+** with pip
2. **tmux** with active Primary AI session
3. **Telegram account**
4. **@BotFather** access to create bot

---

## Step 1: Create Telegram Bot

1. **Open Telegram** and search for `@BotFather`

2. **Start conversation** with `/start`

3. **Create new bot**:
   ```
   /newbot
   ```

4. **Choose bot name** (display name):
   ```
   A-C-Gee Bridge
   ```

5. **Choose bot username** (must end in 'bot'):
   ```
   acgee_bridge_bot
   ```

6. **Save the bot token** - BotFather will send you a token like:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

   **IMPORTANT**: Keep this token secret! It's like a password.

---

## Step 2: Get Your Telegram User ID

You need your Telegram user ID to configure authorization.

**Method 1: Use @userinfobot**

1. Search for `@userinfobot` in Telegram
2. Start conversation: `/start`
3. Bot will reply with your user ID (e.g., `123456789`)

**Method 2: Use @getidsbot**

1. Search for `@getidsbot` in Telegram
2. Start conversation: `/start`
3. Bot will show your ID

**Save this number** - you'll need it for configuration.

---

## Step 3: Install Dependencies

```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch

# Install Python packages
pip install -r requirements-telegram.txt

# Or install manually:
pip install python-telegram-bot>=20.0
pip install python-dotenv>=1.0.0
```

---

## Step 4: Configure the Bridge

1. **Copy example config**:
   ```bash
   cp config/telegram_config.example.json config/telegram_config.json
   ```

2. **Edit configuration**:
   ```bash
   nano config/telegram_config.json
   ```

3. **Update values**:

   ```json
   {
     "bot_token": "YOUR_BOT_TOKEN_FROM_BOTFATHER",
     "authorized_users": {
       "YOUR_TELEGRAM_USER_ID": {
         "name": "Corey",
         "role": "creator",
         "admin": true
       }
     },
     "tmux_session": "acgee-main",
     "tmux_pane": "acgee-main:0.0",
     "working_directory": "/home/corey/projects/AI-CIV/grow_gemini_deepresearch",
     "response_timeout": 10,
     "max_response_length": 4000
   }
   ```

   **Replace**:
   - `YOUR_BOT_TOKEN_FROM_BOTFATHER` - Token from Step 1
   - `YOUR_TELEGRAM_USER_ID` - User ID from Step 2 (numbers only, no quotes around the ID)

4. **Verify tmux session name**:
   ```bash
   tmux list-sessions
   ```

   If your Primary AI session has a different name, update `tmux_session` and `tmux_pane` accordingly.

---

## Step 5: Verify tmux Session

The bridge injects messages into a tmux session where Primary AI is running.

1. **Check if session exists**:
   ```bash
   tmux has-session -t acgee-main && echo "Session exists" || echo "Session NOT found"
   ```

2. **List all tmux sessions**:
   ```bash
   tmux list-sessions
   ```

3. **If session doesn't exist**, start Primary AI in tmux:
   ```bash
   tmux new-session -s acgee-main
   # Then start Claude Code or your Primary AI interface
   ```

---

## Step 6: Start the Bridge

1. **Run the bridge**:
   ```bash
   python tools/telegram_bridge.py
   ```

2. **Expected output**:
   ```
   2025-10-16 12:00:00 - __main__ - INFO - Starting A-C-Gee Telegram Bridge (Phase 1 MVP)
   2025-10-16 12:00:00 - __main__ - INFO - Loaded config from config/telegram_config.json
   2025-10-16 12:00:00 - __main__ - INFO - Bridge initialized for tmux session: acgee-main:0.0
   2025-10-16 12:00:00 - __main__ - INFO - Starting bot polling...
   2025-10-16 12:00:00 - __main__ - INFO - Authorized users: ['123456789']
   ```

3. **If you see errors**:
   - **"No bot token found"** - Check `config/telegram_config.json` or set `TELEGRAM_BOT_TOKEN` env var
   - **"No authorized users"** - Add your user ID to `authorized_users` in config
   - **"tmux session may not exist"** - Start tmux session (Step 5)

---

## Step 7: Test the Bridge

1. **Open Telegram** and search for your bot (e.g., `@acgee_bridge_bot`)

2. **Send `/start` command** - Should show welcome message:
   ```
   Welcome to A-C-Gee Telegram Bridge!

   You are authorized as: Corey
   Role: creator
   ...
   ```

3. **Send `/ping` command** - Should respond immediately:
   ```
   Pong!

   Bridge Status: Online
   tmux Session: Connected
   ...
   ```

4. **Send test message** - Try:
   ```
   Hello, Primary AI!
   ```

   Expected flow:
   - Bot replies: "Injecting to Primary AI tmux session..."
   - Wait ~10 seconds
   - Bot replies with captured response from Primary AI

5. **Check tmux session** - Attach to see injected message:
   ```bash
   tmux attach -t acgee-main
   ```

   You should see:
   ```
   [TELEGRAM from @corey] Hello, Primary AI!
   ```

---

## Configuration Options

### Required Settings

- **`bot_token`** - From @BotFather (REQUIRED)
- **`authorized_users`** - Dict of user IDs and info (REQUIRED)

### Optional Settings

- **`tmux_session`** - tmux session name (default: `acgee-main`)
- **`tmux_pane`** - Specific pane (default: `acgee-main:0.0`)
- **`response_timeout`** - Seconds to wait before capturing (default: `10`)
- **`max_response_length`** - Max chars to send to Telegram (default: `4000`)
- **`working_directory`** - Project root (default: auto-detected)

### Environment Variables (Alternative to config file)

You can use environment variables instead of config file:

```bash
export TELEGRAM_BOT_TOKEN="your-token-here"
python tools/telegram_bridge.py
```

**Note**: Authorized users must still be in config file for MVP.

---

## Commands

Once the bridge is running, these commands are available in Telegram:

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and setup info |
| `/help` | Show available commands and usage |
| `/ping` | Health check (immediate pong response) |

**Regular messages** are injected into tmux and responses are captured.

---

## Troubleshooting

### "Unauthorized" message

**Problem**: Bot replies "Unauthorized" when you message it.

**Solution**:
1. Get your Telegram user ID (Step 2)
2. Add it to `authorized_users` in `config/telegram_config.json`
3. Restart the bridge

### "Failed to inject message to tmux"

**Problem**: Bot can't inject messages.

**Solution**:
1. Check tmux session exists: `tmux list-sessions`
2. Verify session name in config matches actual session
3. Check permissions (can you run `tmux send-keys` manually?)

### "No response captured"

**Problem**: Bot can't capture Primary AI response.

**Solution**:
1. Increase `response_timeout` in config (Primary AI may need more time)
2. Check if Primary AI is actually running in tmux session
3. Attach to tmux and verify AI is responding to prompts

### Bot doesn't start

**Problem**: `python tools/telegram_bridge.py` fails.

**Solution**:
1. Check Python version: `python --version` (need 3.9+)
2. Install dependencies: `pip install -r requirements-telegram.txt`
3. Check bot token is valid (test in @BotFather)
4. Check config file exists and is valid JSON

### Response is truncated

**Problem**: Telegram message ends with "...(truncated)".

**Solution**:
- Normal behavior - Telegram has 4096 char limit
- Increase `max_response_length` if you want more context
- Or ask Primary AI for shorter responses

---

## Running in Background

For production use, run the bridge in the background:

### Using tmux

```bash
# Create new tmux session for bridge
tmux new-session -s telegram-bridge -d

# Run bridge in that session
tmux send-keys -t telegram-bridge "cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch" Enter
tmux send-keys -t telegram-bridge "python tools/telegram_bridge.py" Enter

# Check it's running
tmux attach -t telegram-bridge
# (Ctrl+B, D to detach)
```

### Using systemd (advanced)

Create `/etc/systemd/system/acgee-telegram-bridge.service`:

```ini
[Unit]
Description=A-C-Gee Telegram Bridge
After=network.target

[Service]
Type=simple
User=corey
WorkingDirectory=/home/corey/projects/AI-CIV/grow_gemini_deepresearch
ExecStart=/usr/bin/python3 tools/telegram_bridge.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable acgee-telegram-bridge
sudo systemctl start acgee-telegram-bridge
sudo systemctl status acgee-telegram-bridge
```

---

## Security Notes

1. **Keep bot token secret** - Never commit to git or share publicly
2. **Whitelist users** - Only add trusted users to `authorized_users`
3. **Monitor logs** - Check who is using the bridge
4. **Session storage** - `.tg_sessions/` contains user IDs and message counts
5. **tmux access** - Bot has full access to inject into tmux session

---

## Architecture Notes

### Why tmux injection?

- **No API costs** - Doesn't call Anthropic API directly
- **Reuses existing session** - Primary AI already running
- **Simple integration** - No need to modify Primary AI code
- **Full context** - Primary AI has full conversation history

### Limitations (Phase 1 MVP)

- **Response timing** - Fixed wait time, may be too short or too long
- **Response parsing** - Simple extraction, may capture extra text
- **No streaming** - Waits for complete response
- **No tool indicators** - Can't tell if AI is using tools
- **Single session** - One tmux session for all users

### Future Enhancements (Phase 2+)

- Smart response detection (wait for actual completion)
- Multi-user session isolation
- Streaming responses
- Tool usage indicators
- Message queuing
- Better response parsing

---

## File Locations

| File | Purpose |
|------|---------|
| `tools/telegram_bridge.py` | Main bridge implementation |
| `config/telegram_config.json` | Configuration (you create this) |
| `config/telegram_config.example.json` | Example configuration |
| `requirements-telegram.txt` | Python dependencies |
| `.tg_sessions/` | Session storage (auto-created) |
| `docs/TELEGRAM_SETUP.md` | This guide |

---

## Support

If you encounter issues:

1. Check logs - bridge prints detailed info
2. Verify configuration - compare to example
3. Test tmux manually - `tmux send-keys -t acgee-main "test"`
4. Check Telegram bot status in @BotFather
5. Read architecture doc in `.claude/from-corey/tg-integration-and-possible-lesson/`

---

## Quick Reference

```bash
# Start bridge
python tools/telegram_bridge.py

# Check tmux session
tmux list-sessions
tmux attach -t acgee-main

# View session storage
ls -la .tg_sessions/
cat .tg_sessions/123456789.json

# Test bot token
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

---

**Phase 1 MVP Complete** - Simple working round-trip relay
**Next**: Phase 2 will add smart response detection, streaming, and multi-user sessions
