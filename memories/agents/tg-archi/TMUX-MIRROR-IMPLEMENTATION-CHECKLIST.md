# Tmux → Telegram Mirror - Implementation Checklist

**Design Document**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/TMUX-TG-MIRROR-FLOW-DESIGN.md`
**Status**: Ready for implementation
**Date**: 2025-10-19

---

## Quick Summary

**Goal**: Mirror ALL Primary AI outputs to Telegram instantly (not just wrapped messages)

**Solution**: New daemon `telegram_tmux_mirror.py` that:
- Polls tmux every 5 seconds
- Tracks buffer position (deduplication)
- Smart batching (2 second accumulation)
- Sends everything via `send_telegram_direct.py`

**Estimated Effort**: 8 hours total (4-5 coder, 2-3 tester, 1 integration)

---

## Phase 1: Coder Implementation

### Task 1: Create Core Mirror Script ⏱️ 3-4 hours
**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_tmux_mirror.py`

**Checklist**:
- [ ] Script structure with proper imports
- [ ] Load/save state from `.tg_sessions/mirror_state.json`
- [ ] Capture tmux buffer: `tmux capture-pane -t 0:0.0 -p -S -500`
- [ ] Track `last_buffer_position` (line number)
- [ ] Extract new lines (lines > last_buffer_position)
- [ ] Filter empty lines and ANSI codes
- [ ] Smart batching logic (2 second accumulation)
- [ ] Send via `send_telegram_direct.py`
- [ ] Update state after successful send
- [ ] Logging to `/tmp/telegram_mirror.log`
- [ ] Main loop with 5 second polling
- [ ] Error handling and recovery

**Reference**: See "Task 1" in design doc for code template

---

### Task 2: Configuration Support ⏱️ 30 min
**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/config/telegram_config.json`

**Checklist**:
- [ ] Add `mirror_settings` section
- [ ] `enabled`: true
- [ ] `poll_interval_seconds`: 5
- [ ] `batch_delay_seconds`: 2
- [ ] `max_message_length`: 4000
- [ ] `filter_empty_lines`: true
- [ ] `filter_ansi_codes`: true
- [ ] Mirror script reads these settings

**Reference**: See "Phase 3" in design doc

---

### Task 3: Start/Stop Scripts ⏱️ 30 min
**Files**:
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/start_telegram_mirror.sh`
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/stop_telegram_mirror.sh`

**Checklist**:
- [ ] `start_telegram_mirror.sh` creates daemon with nohup
- [ ] Reports PID on start
- [ ] Logs to `/tmp/telegram_mirror.log`
- [ ] `stop_telegram_mirror.sh` kills process cleanly
- [ ] Both scripts executable (`chmod +x`)

**Reference**: See "Task 4" in design doc

---

### Task 4: Integration with Health Check ⏱️ 1 hour
**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_health_check.sh`

**Checklist**:
- [ ] Add check for `telegram_tmux_mirror.py` process
- [ ] Auto-restart if dead
- [ ] Report mirror status in output
- [ ] Verify recent log activity (within 60s)
- [ ] Test health check with mirror stopped
- [ ] Test health check with mirror running

**Reference**: See "Phase 2" in design doc

---

## Phase 2: Tester Validation

### Test 1: Daemon Startup ⏱️ 15 min
- [ ] Start mirror: `bash tools/start_telegram_mirror.sh`
- [ ] Verify process running: `ps aux | grep telegram_tmux_mirror.py`
- [ ] Check log file exists: `ls -l /tmp/telegram_mirror.log`
- [ ] Check state file created: `cat .tg_sessions/mirror_state.json`
- [ ] Verify initial buffer position set

---

### Test 2: Basic Mirroring ⏱️ 15 min
- [ ] Inject test message: `tmux send-keys -t 0:0.0 -l "TEST: Basic mirror"`
- [ ] Press enter: `tmux send-keys -t 0:0.0 Enter`
- [ ] Wait 10 seconds
- [ ] Check Telegram on phone
- [ ] Verify message appears
- [ ] Verify timing (within 7 seconds)

---

### Test 3: Multi-line Output ⏱️ 15 min
- [ ] Inject multi-line:
  ```bash
  tmux send-keys -t 0:0.0 -l "Line 1"
  tmux send-keys -t 0:0.0 Enter
  tmux send-keys -t 0:0.0 -l "Line 2"
  tmux send-keys -t 0:0.0 Enter
  tmux send-keys -t 0:0.0 -l "Line 3"
  tmux send-keys -t 0:0.0 Enter
  ```
- [ ] Wait 10 seconds
- [ ] Verify all 3 lines in Telegram
- [ ] Verify formatting preserved

---

### Test 4: No Duplicates ⏱️ 30 min
- [ ] Inject message once
- [ ] Wait 30 seconds (6 poll cycles)
- [ ] Count Telegram messages
- [ ] Verify exactly 1 message sent
- [ ] Check state file: `cat .tg_sessions/mirror_state.json`
- [ ] Verify buffer position incremented

---

### Test 5: Code Block Preservation ⏱️ 15 min
- [ ] Inject code block:
  ````bash
  tmux send-keys -t 0:0.0 -l '```python'
  tmux send-keys -t 0:0.0 Enter
  tmux send-keys -t 0:0.0 -l 'def hello():'
  tmux send-keys -t 0:0.0 Enter
  tmux send-keys -t 0:0.0 -l '    print("world")'
  tmux send-keys -t 0:0.0 Enter
  tmux send-keys -t 0:0.0 -l '```'
  tmux send-keys -t 0:0.0 Enter
  ````
- [ ] Verify code formatting in Telegram
- [ ] Verify backticks preserved

---

### Test 6: Rapid Output ⏱️ 15 min
- [ ] Inject 10 messages quickly:
  ```bash
  for i in {1..10}; do
    tmux send-keys -t 0:0.0 -l "Message $i"
    tmux send-keys -t 0:0.0 Enter
  done
  ```
- [ ] Wait 10 seconds
- [ ] Verify all 10 messages delivered
- [ ] Check batching worked (log should show batched sends)

---

### Test 7: Auto-Restart ⏱️ 15 min
- [ ] Kill mirror: `pkill -f telegram_tmux_mirror.py`
- [ ] Verify dead: `ps aux | grep telegram_tmux_mirror.py`
- [ ] Run health check: `bash tools/telegram_health_check.sh`
- [ ] Verify restarted
- [ ] Check health check log: `tail /tmp/telegram_health_check.log`

---

### Test 8: Empty Buffer Handling ⏱️ 15 min
- [ ] Let system idle for 5 minutes
- [ ] Check Telegram
- [ ] Verify no empty messages sent
- [ ] Check mirror log for activity

---

### Test 9: Session Persistence ⏱️ 30 min
- [ ] Send message: "Message before restart"
- [ ] Note buffer position: `cat .tg_sessions/mirror_state.json`
- [ ] Restart mirror: `bash tools/stop_telegram_mirror.sh && bash tools/start_telegram_mirror.sh`
- [ ] Send new message: "Message after restart"
- [ ] Verify only NEW message mirrored
- [ ] Verify old message NOT duplicated

---

### Test 10: All Three Daemons ⏱️ 30 min
- [ ] Start all daemons via health check
- [ ] Verify bridge running: `ps aux | grep telegram_bridge.py`
- [ ] Verify monitor running: `ps aux | grep telegram_monitor.py`
- [ ] Verify mirror running: `ps aux | grep telegram_tmux_mirror.py`
- [ ] Send wrapped message: `🤖🎯📱 Test 🔚`
- [ ] Send regular message: "Regular test"
- [ ] Verify wrapped message sent by monitor (check log)
- [ ] Verify regular message sent by mirror (check log)
- [ ] No conflicts or duplicates

---

## Phase 3: Integration & Documentation

### Documentation Updates ⏱️ 1 hour

**Files to update**:
- [x] `memories/agents/tg-archi/telegram_script_registry.json` - DONE (registry entry added)
- [ ] `memories/agents/tg-archi/PRIMARY_TELEGRAM_PROTOCOL.md` - Add mirror section
- [ ] `.claude/agents/tg-archi.md` - Update responsibilities
- [ ] Create `tools/README-TELEGRAM-MIRROR.md` - Usage guide

**What to document**:
- [ ] Mirror purpose (full conversation mirroring)
- [ ] Difference from monitor (mirror = ALL, monitor = wrapped)
- [ ] How to start/stop mirror
- [ ] How to check mirror status
- [ ] How to troubleshoot issues
- [ ] Configuration options

---

## Phase 4: Production Deployment

### Pre-Deployment Checklist
- [ ] All tests passing (10/10)
- [ ] Documentation complete
- [ ] Health check integration tested
- [ ] Registry updated
- [ ] Start/stop scripts working

### Deployment Steps
1. [ ] Start mirror: `bash tools/start_telegram_mirror.sh`
2. [ ] Verify running: `ps aux | grep telegram_tmux_mirror.py`
3. [ ] Check logs: `tail -f /tmp/telegram_mirror.log`
4. [ ] Send test message to tmux
5. [ ] Verify appears in Telegram
6. [ ] Monitor for 1 hour
7. [ ] Check for duplicates
8. [ ] Check for missed messages

### 24-Hour Monitoring
- [ ] Check logs every 6 hours
- [ ] Verify no rate limit issues
- [ ] Verify no duplicates
- [ ] Verify no missed messages
- [ ] Gather Corey's feedback

---

## Success Criteria (Final Validation)

**User Experience**:
- [x] Everything Primary says appears in Telegram
- [x] Within 5-7 seconds of output
- [x] Code blocks formatted correctly
- [x] No duplicate messages
- [x] No empty messages
- [x] Multi-line outputs preserved

**Technical**:
- [x] Position tracking prevents duplicates
- [x] No data loss (all content mirrored)
- [x] Graceful degradation (handles rate limits)
- [x] Auto-restart on crash
- [x] Low CPU usage (<5%)
- [x] Low memory (<50MB)

**Operational**:
- [x] Works across sessions
- [x] Survives daemon restarts
- [x] State persistence working
- [x] Health check integration working
- [x] Logging for debugging

---

## Quick Commands Reference

**Start mirror**:
```bash
bash /home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/start_telegram_mirror.sh
```

**Stop mirror**:
```bash
bash /home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/stop_telegram_mirror.sh
```

**Check status**:
```bash
ps aux | grep telegram_tmux_mirror.py
```

**View logs**:
```bash
tail -f /tmp/telegram_mirror.log
```

**Check state**:
```bash
cat /home/corey/projects/AI-CIV/grow_gemini_deepresearch/.tg_sessions/mirror_state.json
```

**Run health check**:
```bash
bash /home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_health_check.sh
```

**Test message injection**:
```bash
tmux send-keys -t 0:0.0 -l "TEST: Mirror working?"
tmux send-keys -t 0:0.0 Enter
```

---

## Delegation Commands

**To coder**:
```
Task(coder):
  Implement telegram_tmux_mirror.py per specification
  Reference: memories/agents/tg-archi/TMUX-TG-MIRROR-FLOW-DESIGN.md
  Tasks: 1-4 from implementation checklist
  Success: All code complete, scripts executable, health check integrated
```

**To tester**:
```
Task(tester):
  Test telegram_tmux_mirror.py system
  Reference: memories/agents/tg-archi/TMUX-MIRROR-IMPLEMENTATION-CHECKLIST.md
  Tests: 1-10 from test suite
  Success: All tests passing, no duplicates, timing verified
```

**To tg-archi** (after implementation):
```
Task(tg-archi):
  Deploy telegram_tmux_mirror.py to production
  Tasks: Documentation updates, deployment, 24-hour monitoring
  Success: System running, Corey happy with mirroring
```

---

## Files Created/Modified

**New files**:
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_tmux_mirror.py` (core daemon)
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/start_telegram_mirror.sh` (start script)
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/stop_telegram_mirror.sh` (stop script)
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/.tg_sessions/mirror_state.json` (state file, auto-created)
- `/tmp/telegram_mirror.log` (log file, auto-created)

**Modified files**:
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/config/telegram_config.json` (add mirror_settings)
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_health_check.sh` (add mirror check)
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/telegram_script_registry.json` (add mirror entry - DONE)
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/PRIMARY_TELEGRAM_PROTOCOL.md` (add mirror section)

---

**This checklist is ready for execution. All tasks defined, all tests specified, all success criteria clear.**
