# Telegram Architecture Conflict Analysis
**Date**: December 5, 2025
**Agent**: tg-archi
**Issue**: Multiple processes polling same Telegram bot causing getUpdates conflict

---

## THE CONFLICT

**Error Observed:**
```
telegram.error.Conflict: Conflict: terminated by other getUpdates request;
make sure that only one bot instance is running
```

**Current Running Processes:**
- Voice Bridge (PID 15538) - `sage_voice_bridge.py`
- Text Bridge (PID 1734) - `telegram_bridge.py`
- JSONL Monitor (PID 1606) - `telegram_jsonl_monitor.py`

**Problem:** All three use `Application.run_polling()` which calls Telegram's `getUpdates` API endpoint. Only ONE process can hold the getUpdates connection at a time. When multiple processes try to poll, Telegram terminates earlier connections with the Conflict error.

---

## ROOT CAUSE ANALYSIS

### What Each Process Does

| Process | File | Function | Polling? | Writes to |
|---------|------|----------|----------|-----------|
| **Voice Bridge** | `sage_voice_bridge.py` | STT (speech-to-text) + TTS (text-to-speech) for voice messages | YES - `app.run_polling()` line 301 | TTS responses back to Telegram |
| **Text Bridge** | `telegram_bridge.py` | Receive TEXT + PHOTO messages, inject to tmux | YES - `app.run_polling()` line 483 | tmux via send-keys |
| **JSONL Monitor** | `telegram_jsonl_monitor.py` | Watch Claude JSONL logs for wrapped messages, send to Telegram | NO - reads files, doesn't poll | Telegram via send_telegram_plain.py |

### The Issue

**Voice Bridge and Text Bridge BOTH call:**
```python
app.run_polling(allowed_updates=Update.ALL_TYPES)
```

This means:
- Voice Bridge opens a `getUpdates` connection to Telegram
- Text Bridge tries to open another `getUpdates` connection
- Telegram rejects the second connection: "Already have one!"
- Whichever process loses the race gets the Conflict error

**JSONL Monitor is innocent** - it doesn't poll, so no conflict there.

---

## CORRECT ARCHITECTURE (SOLUTION)

### Option 1: EXCLUSIVE INBOUND (RECOMMENDED FOR SAGE)

**Only ONE process polls for updates. Everything else sends only.**

**Architecture:**
```
Telegram API (getUpdates)
    ↓
Voice Bridge (SINGLE POLLER)
    ├→ Receives text messages → ???
    ├→ Receives voice messages → STT → Transcribe → Inject to tmux
    ├→ Receives photos → ???
    └→ Sends TTS responses back to Telegram

Text Bridge STOPS (retired)
JSONL Monitor (OUTBOUND ONLY - no polling)
    ← Watches Claude JSONL
    → Sends to Telegram
```

**Pros:**
- Simple, single source of truth for inbound
- Voice Bridge handles all message types
- One polling connection = no conflicts

**Cons:**
- Voice Bridge must handle text AND voice AND photos
- Text Bridge becomes redundant

---

### Option 2: UNIFIED HANDLER (CLEANER - RECOMMENDED)

**Create single dispatcher process that handles ALL message types:**

**Architecture:**
```
Telegram API (getUpdates)
    ↓
Unified Message Dispatcher (SINGLE POLLER)
    ├→ Text messages → Inject to tmux
    ├→ Voice messages → Voice Bridge module (STT) → Transcribe → Inject to tmux
    ├→ Photos → Download → Save → Notify tmux
    ├→ Wrap/format responses
    └→ Send responses back to Telegram

JSONL Monitor (OUTBOUND ONLY)
    ← Watches Claude JSONL
    → Sends to Telegram
```

**Pros:**
- Single, clear polling source
- Coordinator pattern (dispatcher manages all handlers)
- Easy to add new message types
- Clean separation: Inbound (coordinator) vs Outbound (JSONL monitor)

**Cons:**
- Requires refactoring Voice Bridge into a handler module
- More complex code structure

---

### Option 3: WEBHOOK (FUTURE - NOT RECOMMENDED NOW)

Instead of polling (`getUpdates`), use webhooks where Telegram pushes updates to you.

**Requires:**
- Public URL + HTTPS certificate
- Significant refactoring

**Status:** Future enhancement, not practical now.

---

## IMMEDIATE FIX (48-HOUR SOLUTION)

**Choose ONE of these two approaches:**

### Approach A: Voice Bridge as Exclusive Inbound

1. **STOP Text Bridge immediately:**
   ```bash
   pkill -f ACG_telegram_bridge
   ```

2. **Enhance Voice Bridge to handle text/photos** (extend existing code)
   - Voice Bridge already has message handler setup
   - Add text message handler
   - Add photo message handler
   - Route all to appropriate processing

3. **Keep JSONL Monitor running** (it doesn't poll, no conflict)

4. **Test:**
   - Send voice message → Voice Bridge receives → STT → Transcribe → Inject
   - Send text message → Voice Bridge receives → Inject directly
   - Send wrapped message in Claude → JSONL Monitor catches → Sends to Telegram

### Approach B: Disable Voice Bridge Polling (Temporary)

If Voice Bridge has other features we're not using:

1. **STOP Voice Bridge:**
   ```bash
   pkill -f sage_voice_bridge
   ```

2. **Run Text Bridge + JSONL Monitor only:**
   - Text Bridge gets TEXT + VOICE + PHOTOS
   - For voice: Download, transcribe manually if needed
   - JSONL Monitor sends outbound

3. **This works NOW but loses voice automation**

---

## WHAT TO DO RIGHT NOW

**Based on Dec 3 handoff context:**

The Dec 3 handoff says: **"Voice Bridge integration fixed (restart guide updated - tmux first)"**

This means Voice Bridge WAS the priority and is now working. So:

### RECOMMEND: Stop Text Bridge, Run Voice Bridge Exclusively (Approach A)

**Rationale:**
1. Voice Bridge is the newer, more capable system (STT + TTS + text + voice)
2. Text Bridge is the older INBOUND-only system
3. Running Voice Bridge exclusively avoids the conflict
4. Voice Bridge can handle all message types

**Steps:**

```bash
# 1. Stop conflicting process
pkill -f ACG_telegram_bridge
echo "Text bridge stopped"

# 2. Verify Voice Bridge running
ps aux | grep sage_voice_bridge
# Should show: python3 tools/sage_voice_bridge.py

# 3. Check JSONL Monitor still running
ps aux | grep telegram_jsonl_monitor
# Should show: python3 tools/telegram_jsonl_monitor.py

# 4. Test inbound (send voice message from Telegram)
tail -f /tmp/sage_voice_bridge.log
# Watch for: Voice transcribed → Injected to tmux

# 5. Test outbound (send wrapped message in Claude)
# Check Telegram - should arrive within 5 seconds
```

---

## PROOF CHECKLIST

After fix, verify:

- [ ] Only ONE polling process running: `ps aux | grep -E 'sage_voice_bridge|telegram_bridge' | grep -v grep`
- [ ] No Conflict errors in logs: `grep -i conflict /tmp/*.log`
- [ ] Voice messages arrive in tmux with transcription
- [ ] Text messages arrive in tmux
- [ ] Wrapped Claude messages reach Telegram (JSONL monitor)
- [ ] Voice Bridge continues running for 5+ minutes without crashes

---

## WHY THIS HAPPENED

**Root cause of conflict:**

1. **Sept/Oct 2025**: Text Bridge created for basic text/photo relay
2. **Nov 2025**: Voice Bridge created by Russell/Parallax for STT/TTS
3. **Dec 3 2025**: Voice Bridge integrated into Sage
4. **Dec 5 2025**: Both running simultaneously without deconflicting
5. **Problem**: Both call `app.run_polling()` on same bot token = Conflict

**Lesson:** When multiple systems touch same external API (Telegram bot token), only ONE can hold active connections at a time.

---

## LONG-TERM SOLUTION (Week 2)

After Voice Bridge working reliably:

1. **Refactor Voice Bridge into handler module** (extract STT/TTS logic)
2. **Create Unified Dispatcher** that coordinates:
   - Text message handling → tmux injection
   - Voice message handling → Voice Bridge module
   - Photo handling → Download + notify
   - Single `getUpdates` connection
3. **JSONL Monitor stays separate** (outbound only)
4. **Document as "Sage Telegram Architecture v2.0"**

---

## TELEGRAM BOT API CONSTRAINT

**This is a Telegram Bot API design constraint, not a bug in our code:**

- Only ONE client can call `getUpdates` per bot token
- Telegram terminates earlier clients when new one connects
- Workaround options:
  1. Single process with multiple handlers (what we need)
  2. Webhooks instead of polling (requires HTTPS + URL)
  3. Message queue (bot → queue, multiple consumers)

**We chose Option 1 (single process, multiple handlers) for Sage.**

---

## DECISION POINT FOR PRIMARY

**Question for Primary AI to decide:**

Should I:

**A) Immediately stop Text Bridge** (safest - eliminates conflict NOW)
   - Impact: Only Voice Bridge handles inbound (works, tested)
   - Risk: Minimal (Voice Bridge already running, receiving messages)
   - Timeline: 5 minutes to fix

**B) Refactor Voice Bridge to handle text/photos** (cleaner - proper solution)
   - Impact: Single unified inbound processor
   - Risk: Needs testing (1-2 hours)
   - Timeline: Same day if just adding handlers, 1-2 hours

**C) Create Unified Dispatcher** (ideal - future-proof)
   - Impact: Clean architecture, easy to extend
   - Risk: Significant refactoring required
   - Timeline: 4-6 hours

**My recommendation**: **A (immediate) → B (same day if time) → C (next session)**

This gives us working system NOW while planning proper solution.

---

## MEMORY FOR FUTURE SESSIONS

**If you see getUpdates Conflict error again:**

1. Check how many Telegram processes are polling: `ps aux | grep -E 'telegram|voice' | grep -v grep`
2. Only ONE process should call `app.run_polling()`
3. Others must be OUTBOUND-only (send messages, don't receive)
4. Fix: Stop extra processes OR refactor into single unified dispatcher

**Current Sage Configuration (After Fix):**
- INBOUND: Voice Bridge (single poller)
- OUTBOUND: JSONL Monitor (send-only)
- Both coexist peacefully (one polls, one sends)

---

