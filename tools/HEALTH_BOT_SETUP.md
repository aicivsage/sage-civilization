# Health Bot Setup Guide

**Purpose:** Create a dedicated Telegram bot for manual health data entry and AI coach interactions

**Date:** 2025-10-18

---

## Step 1: Create Bot via BotFather

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. When prompted for name, use: `A-C-Gee Health Coach`
4. When prompted for username, use: `acgee_health_coach_bot` (or similar if taken)
5. BotFather will reply with your **bot token** - copy it immediately

**Expected response:**
```
Done! Congratulations on your new bot. You will find it at t.me/acgee_health_coach_bot

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890

For a description of the Bot API, see this page: https://core.telegram.org/bots/api
```

6. Copy the token (format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890`)

---

## Step 2: Configure Bot Token

**Save token to environment:**

```bash
# Add to ~/.bashrc or ~/.zshrc
export HEALTH_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"

# Reload shell
source ~/.bashrc
```

**Or save to project .env file:**

```bash
# Create/edit .env in project root
echo "HEALTH_BOT_TOKEN=YOUR_BOT_TOKEN_HERE" >> /home/corey/projects/AI-CIV/grow_gemini_deepresearch/.env
```

---

## Step 3: Set Bot Commands (Optional)

Via BotFather, you can set commands that users see when typing `/`:

1. Send `/setcommands` to BotFather
2. Select your new bot
3. Send this command list:

```
weight - Log weight (e.g., /weight 195)
bp - Log blood pressure (e.g., /bp 120/80)
steps - Log steps (e.g., /steps 7000)
status - View current score and balance
streak - View current streaks
help - How to use this bot
```

---

## Step 4: Test Bot Connection

Once token is configured, test the bot responds:

```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
python3 tools/health_bot_handler.py --test
```

Expected output:
```
✅ Health bot connection successful!
Bot username: @acgee_health_coach_bot
Bot name: A-C-Gee Health Coach
```

---

## Step 5: Start Bot Service

**Option A: Run in terminal (foreground):**
```bash
python3 tools/health_bot_handler.py
```

**Option B: Run as background process:**
```bash
nohup python3 tools/health_bot_handler.py > logs/health_bot.log 2>&1 &
```

**Option C: Add to cron (restart on reboot):**
```bash
@reboot cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch && python3 tools/health_bot_handler.py > logs/health_bot.log 2>&1 &
```

---

## How to Use the Bot

**Natural language reporting:**
- "weight 195"
- "steps 7200"
- "BP 120/80"
- "blood pressure 118/76"

**Slash commands:**
- `/weight 195`
- `/bp 120/80`
- `/steps 7200`
- `/status` - Current score/balance
- `/streak` - Current streaks
- `/help` - Usage guide

**Bot will respond with:**
- Confirmation of data logged
- Score impact (+/- dollars)
- Running balance
- Achievement celebrations (if milestone hit)
- Daily check-in at 8 AM (automated)

---

## Data Flow

```
Corey sends message
    ↓
health_bot_handler.py parses format
    ↓
Validates data (weight >0, BP format correct, steps ≥0)
    ↓
Inserts into health_gamification/data/health.db
    ↓
Invokes health-coach agent for response
    ↓
Bot sends confirmation + score update
```

---

## Files Created

- `tools/health_bot_handler.py` - Main bot service (polling, parsing, database)
- `.claude/agents/health-coach.md` - AI coach agent manifest
- `health_gamification/data/health.db` - SQLite database (auto-created)

---

## Troubleshooting

**Bot doesn't respond:**
1. Check token is correct: `echo $HEALTH_BOT_TOKEN`
2. Verify bot process running: `ps aux | grep health_bot`
3. Check logs: `tail -f logs/health_bot.log`

**Database errors:**
1. Check database exists: `ls -lh health_gamification/data/health.db`
2. Verify schema: `sqlite3 health_gamification/data/health.db ".schema"`

**Can't find bot:**
1. Make sure bot username is exactly what BotFather assigned
2. Search in Telegram: `@acgee_health_coach_bot`

---

## Next Steps

Once bot is running and responding:

1. Send first data entry to test end-to-end flow
2. Check database has entry: `sqlite3 health_gamification/data/health.db "SELECT * FROM health_metrics;"`
3. Verify coach agent invoked and responded
4. Set up 8 AM daily check-in cron job

---

**Questions?** Check `tools/health_bot_handler.py` for implementation details.
