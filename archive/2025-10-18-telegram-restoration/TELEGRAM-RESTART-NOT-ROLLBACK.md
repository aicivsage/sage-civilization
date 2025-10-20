# TELEGRAM: Restart Monitor (Don't Rollback)

**TL;DR**: The fixes are CORRECT and PRESENT in code. The monitor just needs to be restarted.

---

## The Situation

**What you thought**: "We broke the working Telegram system with today's fixes"

**What actually happened**: "The fixes are good, but the old monitor process is still running the old code in memory"

---

## DO NOT ROLLBACK

**The code on disk is CORRECT:**
✅ Delta detection (only scan new lines)
✅ Strong deduplication (full SHA256 hash)
✅ Mark failures as seen (no infinite retry)
✅ Markdown fallback (plain text on 400 errors)

**The monitor process needs restart to load the new code.**

---

## ACTION: Restart Monitor (3 commands)

```bash
# 1. Clear state
rm -f /home/corey/projects/AI-CIV/grow_gemini_deepresearch/.tg_sessions/monitor_state.json

# 2. Kill old process
pkill -f telegram_monitor.py

# 3. Start with new code
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
nohup python3 tools/telegram_monitor.py --interval 30 > /tmp/telegram_monitor.log 2>&1 &
```

---

## TEST: Verify It Works

```bash
# Send test wrapped message
tmux send-keys -t 0:0 "echo '🤖🎯📱'" Enter
tmux send-keys -t 0:0 "echo 'Monitor restart test'" Enter
tmux send-keys -t 0:0 "echo '✨🔚'" Enter

# Wait 30 seconds
# Check Telegram: Should get EXACTLY 1 message (no spam)
```

---

## IF THIS WORKS: Commit the Fixes

```bash
git add tools/telegram_monitor.py tools/send_telegram_direct.py
git add TELEGRAM*.md VERIFICATION*.md
git commit -m "🔧 Fix Telegram monitor spam (delta detection + strong hashing)"
```

---

## IF THIS FAILS: Then Consider Rollback

```bash
# Stop monitor
pkill -f telegram_monitor.py

# Revert code
git checkout HEAD -- tools/telegram_monitor.py tools/send_telegram_direct.py

# Clear state
rm .tg_sessions/monitor_state.json

# Restart old version
nohup python3 tools/telegram_monitor.py --interval 30 > /tmp/telegram_monitor.log 2>&1 &
```

---

## Full Analysis

See: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/GIT-SPECIALIST-TELEGRAM-ROLLBACK-ANALYSIS.md`

---

**Bottom line**: Try restart first. The fixes are good. Rollback only if restart proves the fixes wrong.
