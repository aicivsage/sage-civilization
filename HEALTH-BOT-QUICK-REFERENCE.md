# Health Bot Quick Reference 🏥

## Bot Info
- **Bot**: @ACGhealthCoach_bot on Telegram
- **Test**: `bash tools/test_health_bot.sh`
- **Start**: `bash tools/start_health_bot.sh`
- **Status**: `bash tools/health_bot_status.sh`
- **Stop**: `bash tools/stop_health_bot.sh`
- **Logs**: `tail -f /tmp/health_bot.log`

---

## Quick Commands (In Telegram)

### Natural Language (Just Type)
```
weight 195
BP 120/80
steps 7000
weight 194.5 BP 118/75 steps 8500
```

### Slash Commands
```
/weight 195
/bp 120/80
/steps 7000
/status
/streak
/help
```

---

## Scoring at a Glance

| Metric | When | Score |
|--------|------|-------|
| Weight | Sundays | ±$100/lb |
| BP | Daily | +$10 |
| Steps | Daily | +$20 if ≥6k, -$20 if <6k |

**Goal**: Positive running balance = healthy habits! 💪

---

## Typical Daily Flow

**Morning**:
```
BP 118/75
```

**After weigh-in (Sundays)**:
```
weight 195
```

**Evening**:
```
steps 7500
```

**Check progress**:
```
/status
```

---

## Files

- Config: `config/health_bot_config.json`
- Database: `health_gamification/data/health.db`
- Logs: `/tmp/health_bot.log`
- Docs: `tools/README-HEALTH-BOT.md`

---

**Need help?** Send `/help` to @ACGhealthCoach_bot
