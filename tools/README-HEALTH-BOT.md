# A-C-Gee Health Coach Telegram Bot

**Status**: Configured and ready for testing
**Bot**: @ACGhealthCoach_bot
**Created**: 2025-10-18

---

## Overview

The A-C-Gee Health Coach bot helps Corey track health metrics via Telegram with gamified rewards:

- **Weight tracking**: +/-$100 per pound (Sunday weigh-ins)
- **Blood pressure**: +$10 per daily check
- **Steps**: +$20 if ≥6k, -$20 if <6k
- **Balance tracking**: Virtual dollars fund AI/energy stock portfolio

---

## Quick Start

### 1. Test Connection
```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
bash tools/test_health_bot.sh
```

This will:
- Verify pyTelegramBotAPI is installed
- Test bot connection
- Send welcome message to Corey's Telegram

### 2. Start Bot (Background Service)
```bash
bash tools/start_health_bot.sh
```

### 3. Check Status
```bash
bash tools/health_bot_status.sh
```

### 4. Stop Bot
```bash
bash tools/stop_health_bot.sh
```

---

## Bot Configuration

**Config file**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/config/health_bot_config.json`

```json
{
  "bot_token": "8472258805:AAFdYmIlJozyqIVjNC8PHEDAK_-XZ1vO3T4",
  "corey_chat_id": 437939400,
  "database_path": "health_gamification/data/health.db",
  "daily_checkin_time": "08:00",
  "timezone": "America/Chicago"
}
```

---

## How Corey Interacts with Bot

### Start Bot on Telegram
1. Open Telegram
2. Search for `@ACGhealthCoach_bot`
3. Click "START" button
4. Send `/help` to see commands

### Natural Language Entry
Just send messages like:
- `"weight 195"`
- `"BP 120/80"`
- `"steps 7000"`
- `"weight 194.5 BP 118/75 steps 8500"` (multiple metrics at once)

### Slash Commands
- `/weight 195` - Log weight
- `/bp 120/80` - Log blood pressure
- `/steps 7000` - Log steps
- `/status` - View current data and balance
- `/streak` - View current streaks
- `/help` - Show help message

---

## Scoring System

### Weight (Sundays only)
- **+$100** per pound lost
- **-$100** per pound gained
- Compares to previous Sunday's weigh-in

### Blood Pressure
- **+$10** for each daily BP check
- No penalty for missing days
- Tracks consecutive day streaks

### Steps
- **+$20** if ≥6,000 steps
- **-$20** if <6,000 steps
- Encourages daily movement goal

### Balance
- Running balance of all scores
- Viewable with `/status` command
- ~$500 per AI/energy share equivalent shown

---

## Database

**Location**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/health_gamification/data/health.db`

**Tables**:
1. `health_metrics` - Daily measurements (weight, BP, steps)
2. `health_scores` - Daily scores and running balance
3. `audit_log` - All operations for debugging

**Backup**:
```bash
cp health_gamification/data/health.db health_gamification/data/health_backup_$(date +%Y%m%d).db
```

---

## Logs

**Bot logs**: `/tmp/health_bot.log`

**Monitor logs**:
```bash
tail -f /tmp/health_bot.log
```

**Check for errors**:
```bash
grep "ERROR\|❌" /tmp/health_bot.log
```

---

## Architecture

```
Telegram User (Corey)
    ↓
@ACGhealthCoach_bot
    ↓
tools/health_bot_handler.py
    ├── Message parsing (natural language + slash commands)
    ├── Database operations (SQLite)
    ├── Score calculations
    └── Response generation
    ↓
health.db (SQLite)
```

**Key Features**:
- Auto-installs pyTelegramBotAPI if missing
- Natural language parsing (regex-based)
- Slash command support
- Automatic score calculations
- Sunday weigh-in logic
- Streak tracking
- Audit logging

---

## Troubleshooting

### Bot not responding
1. Check if bot is running: `bash tools/health_bot_status.sh`
2. Restart bot: `bash tools/stop_health_bot.sh && bash tools/start_health_bot.sh`
3. Check logs: `tail -50 /tmp/health_bot.log`

### "pyTelegramBotAPI not installed"
```bash
pip3 install pyTelegramBotAPI
```

### Database locked errors
- Only one bot instance should run at a time
- Check for multiple processes: `ps aux | grep health_bot_handler`
- Kill duplicates: `pkill -f health_bot_handler.py`

### Bot sends duplicate responses
- Ensure only one bot instance is running
- Check for old processes: `ps aux | grep health_bot`

---

## Daily Check-ins (Future Feature)

**Planned**: Automatic 8 AM check-in messages

**Current status**: Manual entry only (send messages to bot when ready)

**To implement**: Schedule daily_checkin() function with cron or systemd timer

---

## Integration with A-C-Gee Civilization

### Relationship to Existing Telegram Infrastructure

**Separate systems** (different bot tokens):
- **Main A-C-Gee bot**: Bridge + monitor for CLI ↔ Telegram mirroring
- **Health Coach bot**: Standalone health data tracking

**Both bots can coexist** - no conflicts.

### Future Enhancements
1. Health-coach agent invocation for AI-generated responses
2. Integration with main A-C-Gee memory systems
3. Weekly summary emails via email-sender agent
4. Trend analysis and predictions
5. Integration with fitness APIs (Fitbit, Apple Health, etc.)

---

## Development

**Main script**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/health_bot_handler.py`

**Test mode**:
```bash
python3 tools/health_bot_handler.py --test --token "YOUR_TOKEN"
```

**Run interactively** (for debugging):
```bash
export HEALTH_BOT_TOKEN="8472258805:AAFdYmIlJozyqIVjNC8PHEDAK_-XZ1vO3T4"
python3 tools/health_bot_handler.py
```

**Add new features**:
1. Edit `health_bot_handler.py`
2. Test with `--test` flag
3. Restart bot: `bash tools/stop_health_bot.sh && bash tools/start_health_bot.sh`
4. Monitor logs: `tail -f /tmp/health_bot.log`

---

## Security Notes

- Bot token stored in config file (not in git - ensure .gitignore includes config/)
- Only Corey's chat ID (437939400) should use bot
- Database has no authentication (local file access only)
- Logs may contain chat IDs but no sensitive health data

**Production hardening** (future):
- Move token to environment variables or secrets manager
- Add user authentication
- Encrypt database
- HIPAA compliance considerations if sharing data

---

## Success Criteria

✅ Bot responds to test message
✅ Corey can send "help" command and get response
✅ Bot ready for manual health data entry
✅ Database initialized and working
✅ Management scripts (start/stop/status) functional
✅ Documentation complete

**Next steps**:
1. Corey tests bot on Telegram
2. First real data entry (weight, BP, steps)
3. Verify scoring calculations
4. Collect feedback for improvements

---

**Status**: Ready for production testing with Corey! 🏥💪
