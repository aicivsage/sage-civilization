# Tmux → Telegram Mirror - Visual Quick Reference

**Status**: Design Complete, Ready for Implementation
**Date**: 2025-10-19

---

## The Problem

```
┌─────────────────────────────────────┐
│   PRIMARY AI (in tmux)              │
│                                     │
│   > Checking systems...             │
│   > Email inbox clear               │
│   > Health bot operational          │
│                                     │
└─────────────────────────────────────┘
                 │
                 │ Corey only sees this
                 │ if he's at his computer
                 ▼
┌─────────────────────────────────────┐
│   COREY'S PHONE                     │
│                                     │
│   (nothing - he's away)             │
│                                     │
└─────────────────────────────────────┘
```

**Corey's request**: "i want your output here to be mirrored in our tg channel perfectly"

---

## The Solution

```
┌─────────────────────────────────────────────────────────────┐
│                    PRIMARY AI (tmux pane 0:0.0)             │
│                                                             │
│   Human: What's the status?                                │
│   Assistant: Checking systems...                           │
│              Email inbox: 3 new messages                   │
│              Health systems: All operational               │
│                                                             │
└──────────────┬──────────────────────────────────────────────┘
               │
               │ tmux buffer (last 500 lines)
               │
               ▼
┌──────────────────────────────────────────────────────────────┐
│              telegram_tmux_mirror.py (NEW DAEMON)            │
│                                                              │
│  Every 5 seconds:                                           │
│  1. Capture tmux buffer                                     │
│  2. Check last_buffer_position (was: 1247)                  │
│  3. Extract new lines (1248-1252)                           │
│  4. Batch for 2 seconds                                     │
│  5. Send to Telegram                                        │
│  6. Update position (now: 1252)                             │
│                                                              │
└──────────────┬───────────────────────────────────────────────┘
               │
               │ via send_telegram_direct.py
               │
               ▼
┌──────────────────────────────────────────────────────────────┐
│                  COREY'S PHONE (Telegram)                    │
│                                                              │
│   [A-C-Gee Bot] 14:32                                       │
│   Checking systems...                                       │
│   Email inbox: 3 new messages                               │
│   Health systems: All operational                            │
│                                                              │
│   (Perfect mirror - even when Corey is away!)               │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Three Telegram Daemons (All Running Together)

```
┌────────────────────────────────────────────────────────────┐
│                 TELEGRAM ECOSYSTEM                          │
│                                                            │
│  ┌──────────────────────────────────────────────────┐    │
│  │  telegram_bridge.py (RECEIVE)                    │    │
│  │  • Telegram → tmux                               │    │
│  │  • Long-polling (24/7)                           │    │
│  │  • Handles TEXT + PHOTOS                         │    │
│  └──────────────────────────────────────────────────┘    │
│                                                            │
│  ┌──────────────────────────────────────────────────┐    │
│  │  telegram_monitor.py (WRAPPED SUMMARIES)         │    │
│  │  • Detects: 🤖🎯📱 ... ✨🔚                       │    │
│  │  • Polls every 5 MINUTES                         │    │
│  │  • For: Session summaries, milestones            │    │
│  └──────────────────────────────────────────────────┘    │
│                                                            │
│  ┌──────────────────────────────────────────────────┐    │
│  │  telegram_tmux_mirror.py (FULL MIRROR) ★ NEW    │    │
│  │  • Sends: ALL outputs                            │    │
│  │  • Polls every 5 SECONDS                         │    │
│  │  • For: Real-time conversation mirroring         │    │
│  └──────────────────────────────────────────────────┘    │
│                                                            │
│  All managed by: telegram_health_check.sh                 │
│  • Auto-restart if dead                                   │
│  • Run every tg-archi invocation                          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## How Position Tracking Works (No Duplicates!)

```
Poll 1 (time: 0s)
┌────────────────────────────────┐
│ Tmux Buffer                    │
│ Line 1245: Health bot working  │
│ Line 1246: Tests passing       │
│ Line 1247: Ready               │  ← last_buffer_position = 1247
└────────────────────────────────┘
         ↓
    (nothing new, don't send)


Poll 2 (time: 5s) - NEW OUTPUT
┌────────────────────────────────┐
│ Tmux Buffer                    │
│ Line 1245: Health bot working  │
│ Line 1246: Tests passing       │
│ Line 1247: Ready               │  ← old position
│ Line 1248: Checking email...   │  ← NEW
│ Line 1249: 3 messages found    │  ← NEW
│ Line 1250: Drafting response   │  ← NEW
└────────────────────────────────┘
         ↓
    Extract lines 1248-1250
         ↓
    Send to Telegram:
    "Checking email...
     3 messages found
     Drafting response"
         ↓
    Update: last_buffer_position = 1250


Poll 3 (time: 10s) - NO NEW OUTPUT
┌────────────────────────────────┐
│ Tmux Buffer                    │
│ Line 1248: Checking email...   │
│ Line 1249: 3 messages found    │
│ Line 1250: Drafting response   │  ← last_buffer_position = 1250
└────────────────────────────────┘
         ↓
    (nothing new, don't send)
         ↓
    Position stays 1250
```

**Result**: Each line sent EXACTLY ONCE, no duplicates!

---

## Smart Batching (No Flooding!)

```
Without Batching (BAD):
14:32:01 - "Line 1"      ← API call 1
14:32:01 - "Line 2"      ← API call 2
14:32:01 - "Line 3"      ← API call 3
14:32:02 - "Line 4"      ← API call 4
14:32:02 - "Line 5"      ← API call 5

Result: 5 Telegram messages, annoying flood!


With Batching (GOOD):
14:32:01 - Accumulating...
14:32:01 - Accumulating...
14:32:01 - Accumulating...
14:32:02 - Accumulating...
14:32:02 - Output stopped, wait 2s...
14:32:04 - Send batch!    ← API call 1

Message:
"Line 1
 Line 2
 Line 3
 Line 4
 Line 5"

Result: 1 Telegram message, coherent thought!
```

**Batching logic**:
- Accumulate for 2 seconds after last output
- If output resumes, keep accumulating
- If 2 seconds of silence, send batch
- Preserves conversation flow

---

## Data Flow Diagram

```
┌──────────┐
│  Human   │ Types message in tmux
└─────┬────┘
      │
      ▼
┌─────────────────┐
│  Claude Code    │ Generates response
│  (Primary AI)   │
└─────┬───────────┘
      │
      ▼ (output to tmux)
┌─────────────────────────────────────┐
│  Tmux Pane 0:0.0                    │
│  Buffer: Lines 1-1500               │
│  Last 500 lines capturable          │
└─────┬───────────────────────────────┘
      │
      │ (every 5 seconds)
      ▼
┌──────────────────────────────────┐
│  telegram_tmux_mirror.py         │
│                                  │
│  1. tmux capture-pane -p -S -500 │
│  2. Compare to last_position     │
│  3. Extract new lines            │
│  4. Filter (empty, ANSI)         │
│  5. Batch (2 sec delay)          │
│  6. Send                         │
│  7. Update position              │
└─────┬────────────────────────────┘
      │
      ▼ (calls)
┌──────────────────────────────────┐
│  send_telegram_direct.py         │
│  • Markdown formatting           │
│  • Auto-chunking (4096 limit)    │
│  • Telegram Bot API              │
└─────┬────────────────────────────┘
      │
      ▼ (HTTPS POST)
┌──────────────────────────────────┐
│  Telegram Bot API                │
│  api.telegram.org/bot.../        │
└─────┬────────────────────────────┘
      │
      ▼ (push notification)
┌──────────────────────────────────┐
│  Corey's Phone                   │
│  [A-C-Gee Bot]                   │
│  Primary's latest output         │
└──────────────────────────────────┘
```

---

## State File Schema

**File**: `.tg_sessions/mirror_state.json`

```json
{
  "last_buffer_position": 1252,
  "last_poll_timestamp": "2025-10-19T14:32:15Z",
  "total_messages_sent": 42,
  "session_started": "2025-10-19T10:00:00Z"
}
```

**Why this works**:
- `last_buffer_position`: Line number in tmux buffer
- Never re-send lines <= this position
- Persists across daemon restarts
- Simple, reliable, no complex hashing

---

## Configuration Schema

**File**: `config/telegram_config.json`

```json
{
  "bot_token": "...",
  "authorized_users": {...},
  "mirror_settings": {
    "enabled": true,
    "poll_interval_seconds": 5,
    "batch_delay_seconds": 2,
    "max_message_length": 4000,
    "filter_empty_lines": true,
    "filter_ansi_codes": true
  }
}
```

**Tunable for different use cases**:
- Fast response: `poll_interval_seconds: 3`
- Reduce API calls: `batch_delay_seconds: 5`
- Disable temporarily: `enabled: false`

---

## Before vs After

### Before (Current State)
```
Corey at computer:
✅ Sees everything in tmux

Corey away from computer:
❌ Sees ONLY wrapped summaries (every 5 min)
❌ Misses conversation details
❌ Has to wait for next summary
```

### After (With Mirror)
```
Corey at computer:
✅ Sees everything in tmux (same as before)

Corey away from computer:
✅ Sees EVERYTHING in Telegram (real-time)
✅ Full conversation mirrored
✅ Within 5-7 seconds of output
✅ Perfect parity with tmux
```

---

## Why This Design Wins

**Option A: Modify monitor**
❌ 5-minute polling (not real-time)
❌ Designed for summaries, not full mirroring

**Option B: Tmux-tail mirror (THIS)**
✅ 5-second polling (real-time)
✅ Position-based (no duplicates)
✅ Smart batching (no flooding)
✅ Non-invasive (no changes to existing scripts)
✅ Parallel to monitor (both can run)

**Option C: Hook output stream**
❌ Too invasive
❌ Fragile
❌ Breaks on updates

---

## Success Criteria

**For Corey**:
- [ ] Everything Primary says appears in Telegram
- [ ] Within 5-7 seconds
- [ ] Code blocks formatted
- [ ] No duplicates
- [ ] No empty spam

**For Engineers**:
- [ ] Position tracking works (no duplicates)
- [ ] Smart batching works (no flooding)
- [ ] Auto-restart on crash
- [ ] Low resource usage (<5% CPU, <50MB RAM)
- [ ] State persists across restarts

---

## Implementation Time Estimates

```
Coder (Tasks 1-4):          4-5 hours
  • Core script:            3-4 hours
  • Config support:         30 min
  • Start/stop scripts:     30 min
  • Health check:           1 hour

Tester (Tests 1-10):        2-3 hours
  • Basic tests (1-6):      1.5 hours
  • Advanced tests (7-10):  1 hour

tg-archi (Deploy):          1 hour
  • Documentation:          30 min
  • Deployment:             15 min
  • Monitoring:             15 min

TOTAL:                      8 hours to production
```

---

## Quick Start Commands

**After implementation, to use**:

```bash
# Start mirror
bash tools/start_telegram_mirror.sh

# Check status
ps aux | grep telegram_tmux_mirror.py

# View live logs
tail -f /tmp/telegram_mirror.log

# Check state
cat .tg_sessions/mirror_state.json

# Stop mirror
bash tools/stop_telegram_mirror.sh
```

---

**Complete design ready for implementation. Next step: Delegate to coder!**
