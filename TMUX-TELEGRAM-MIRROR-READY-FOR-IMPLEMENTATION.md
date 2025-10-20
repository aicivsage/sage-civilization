# Tmux → Telegram Mirror System - Ready for Implementation

**Date**: 2025-10-19
**Status**: Design Complete, Ready for Coder
**Requirement**: Mirror ALL Primary AI outputs to Telegram instantly (Corey's request)

---

## Executive Summary

**Problem**: Corey only sees Primary AI outputs when at his computer. When away, he misses conversation details.

**Solution**: New daemon `telegram_tmux_mirror.py` that polls tmux every 5 seconds and sends ALL new content to Telegram.

**Result**: Perfect tmux → Telegram mirroring within 5-7 seconds. Corey sees everything, everywhere.

---

## Three Key Documents

### 1. Complete Flow Design (45 pages)
**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/TMUX-TG-MIRROR-FLOW-DESIGN.md`

**Contains**:
- Full architecture analysis
- Option comparison (A vs B vs C)
- Complete implementation plan
- Task breakdown for coder
- Test plan for tester
- Risk assessment
- Configuration schemas
- Rollout plan

**Use for**: Deep dive, complete specification, reference during implementation

---

### 2. Implementation Checklist (10 pages)
**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/TMUX-MIRROR-IMPLEMENTATION-CHECKLIST.md`

**Contains**:
- Task-by-task checklist for coder (Tasks 1-4)
- Test-by-test checklist for tester (Tests 1-10)
- Documentation update checklist
- Deployment checklist
- Success criteria validation
- Quick command reference

**Use for**: Execution, progress tracking, validation

---

### 3. Visual Quick Reference (8 pages)
**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/TMUX-MIRROR-QUICK-VISUAL.md`

**Contains**:
- Visual diagrams (before/after, data flow)
- Three daemon ecosystem
- Position tracking explained
- Smart batching explained
- Quick start commands

**Use for**: Understanding at a glance, explaining to others, troubleshooting

---

## Recommended Solution: Option B (Tmux-Tail Mirror)

### Why This Wins

**vs Option A (Modify monitor)**:
- ✅ Real-time (5 sec) vs periodic (5 min)
- ✅ Designed for full mirroring vs summaries only

**vs Option C (Hook output stream)**:
- ✅ Non-invasive vs requires wrapper
- ✅ Reliable vs fragile
- ✅ Simple vs complex

### Core Features

1. **Position-Based Tracking**: No duplicates (tracks line numbers, not content hashes)
2. **Smart Batching**: No flooding (accumulates 2 seconds, then sends)
3. **Auto-Restart**: No manual intervention (health check manages it)
4. **State Persistence**: Survives restarts (remembers last position)
5. **Parallel Operation**: Works alongside existing monitor (no conflicts)

---

## Implementation Overview

### Phase 1: Coder (4-5 hours)

**Task 1: Core Mirror Script** (3-4 hours)
- Create `tools/telegram_tmux_mirror.py`
- Poll tmux every 5 seconds
- Track buffer position
- Smart batching logic
- Send via `send_telegram_direct.py`

**Task 2: Configuration** (30 min)
- Add `mirror_settings` to `config/telegram_config.json`
- Make poll interval configurable

**Task 3: Start/Stop Scripts** (30 min)
- Create `tools/start_telegram_mirror.sh`
- Create `tools/stop_telegram_mirror.sh`

**Task 4: Health Check Integration** (1 hour)
- Modify `tools/telegram_health_check.sh`
- Add mirror process check
- Auto-restart if dead

**Code template provided** in design doc.

---

### Phase 2: Tester (2-3 hours)

**10 Tests**:
1. Daemon startup
2. Basic mirroring
3. Multi-line output
4. No duplicates
5. Code block preservation
6. Rapid output
7. Auto-restart
8. Empty buffer handling
9. Session persistence
10. All three daemons together

**All test procedures detailed** in checklist.

---

### Phase 3: Integration & Deployment (1 hour)

**Documentation**:
- Update PRIMARY_TELEGRAM_PROTOCOL.md
- Update telegram_script_registry.json (DONE)
- Create README-TELEGRAM-MIRROR.md

**Deployment**:
- Start mirror daemon
- Monitor for 24 hours
- Gather Corey's feedback

---

## Files Created/Modified

### New Files
```
tools/telegram_tmux_mirror.py          (core daemon)
tools/start_telegram_mirror.sh         (convenience script)
tools/stop_telegram_mirror.sh          (convenience script)
.tg_sessions/mirror_state.json         (auto-created state file)
/tmp/telegram_mirror.log               (auto-created log file)
```

### Modified Files
```
config/telegram_config.json            (add mirror_settings)
tools/telegram_health_check.sh         (add mirror check)
memories/agents/tg-archi/telegram_script_registry.json  (DONE)
memories/agents/tg-archi/PRIMARY_TELEGRAM_PROTOCOL.md   (add mirror section)
```

---

## Success Criteria

### User Experience (Corey)
- ✅ Everything Primary says appears in Telegram
- ✅ Within 5-7 seconds of Primary's output
- ✅ Code blocks formatted correctly
- ✅ No duplicate messages
- ✅ No empty messages
- ✅ Multi-line outputs preserved

### Technical
- ✅ No duplicate sends (position tracking works)
- ✅ No data loss (all content mirrored)
- ✅ Graceful degradation (handles rate limits)
- ✅ Auto-restart on crash
- ✅ Minimal CPU usage (<5% average)
- ✅ Minimal memory footprint (<50MB)

### Operational
- ✅ Works across tmux sessions
- ✅ Survives daemon restarts
- ✅ State persistence (no re-send on restart)
- ✅ Health check integration
- ✅ Logging for debugging

---

## Three Telegram Daemons (Ecosystem)

```
1. telegram_bridge.py
   • Receives FROM Telegram → Injects to tmux
   • Handles TEXT + PHOTOS
   • 24/7 long-polling

2. telegram_monitor.py (EXISTING)
   • Detects WRAPPED messages (🤖🎯📱 ... ✨🔚)
   • Sends to Telegram
   • Polls every 5 MINUTES
   • For: Session summaries, milestones

3. telegram_tmux_mirror.py (NEW)
   • Streams ALL outputs to Telegram
   • Polls every 5 SECONDS
   • For: Real-time conversation mirroring
   • Complements monitor (no conflict)

All managed by: telegram_health_check.sh
```

---

## How It Works (Simple Version)

```
1. Primary AI outputs to tmux
2. Mirror daemon polls tmux (every 5 sec)
3. Checks: "Any new lines since last poll?"
4. If yes:
   - Extract new lines
   - Filter noise (empty lines, ANSI codes)
   - Batch for 2 seconds
   - Send to Telegram via send_telegram_direct.py
   - Remember position (no re-send)
5. If no: Wait 5 seconds, check again
```

**Result**: Everything appears in Telegram within 5-7 seconds. Perfect mirroring.

---

## Delegation Commands

### To Start Implementation

```
Task(coder):
  Context: Corey wants ALL Primary outputs mirrored to Telegram (not just wrapped)
  Design: /home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/TMUX-TG-MIRROR-FLOW-DESIGN.md
  Checklist: /home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/TMUX-MIRROR-IMPLEMENTATION-CHECKLIST.md

  Tasks:
  1. Create tools/telegram_tmux_mirror.py (see Task 1 in checklist)
  2. Add mirror_settings to config/telegram_config.json (Task 2)
  3. Create start/stop scripts (Task 3)
  4. Integrate with health check (Task 4)

  Success Criteria:
  - Script runs as daemon
  - Polls tmux every 5 seconds
  - Tracks buffer position (no duplicates)
  - Smart batching (2 second accumulation)
  - Sends via send_telegram_direct.py
  - All scripts executable and working

  Estimated Time: 4-5 hours

  Handoff: Report completion, hand to tester
```

---

### After Coder Completes

```
Task(tester):
  Context: New telegram_tmux_mirror.py system implemented
  Test Plan: /home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/TMUX-MIRROR-IMPLEMENTATION-CHECKLIST.md

  Tests to Run: 1-10 (all detailed in checklist)
  - Daemon startup
  - Basic mirroring
  - No duplicates
  - Code formatting
  - Auto-restart
  - Session persistence

  Success Criteria:
  - All 10 tests passing
  - No duplicates detected
  - Timing verified (within 7 seconds)
  - No empty messages
  - Formatting preserved

  Estimated Time: 2-3 hours

  Handoff: Report test results, hand to tg-archi for deployment
```

---

### After Testing Passes

```
Task(tg-archi):
  Context: telegram_tmux_mirror.py tested and ready
  Deployment Plan: Phase 3 in TMUX-MIRROR-IMPLEMENTATION-CHECKLIST.md

  Tasks:
  1. Update documentation (PRIMARY_TELEGRAM_PROTOCOL.md)
  2. Start mirror daemon
  3. Verify all three daemons running
  4. Monitor for 24 hours
  5. Gather Corey's feedback

  Success Criteria:
  - System running in production
  - Corey sees everything in Telegram
  - No duplicates or missed messages
  - No performance issues

  Estimated Time: 1 hour + monitoring

  Handoff: Report to Primary - system live!
```

---

## Quick Commands (After Implementation)

**Start mirror**:
```bash
bash /home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/start_telegram_mirror.sh
```

**Check status**:
```bash
ps aux | grep telegram_tmux_mirror.py
```

**View logs**:
```bash
tail -f /tmp/telegram_mirror.log
```

**Stop mirror**:
```bash
bash /home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/stop_telegram_mirror.sh
```

**Run health check** (manages all three daemons):
```bash
bash /home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_health_check.sh
```

---

## Risk Assessment

### Low Risk
- **Duplicate messages**: Position tracking prevents this
- **Missed messages**: Buffer size (500 lines) sufficient
- **Performance**: Minimal CPU/memory usage

### Medium Risk
- **Rate limiting**: Smart batching mitigates (1 send per 5-7 seconds typical)
- **Network outage**: Graceful degradation planned (queue for retry)

### Mitigation Strategies
- Comprehensive testing (10 tests)
- 24-hour monitoring period
- Easy rollback (just stop daemon)
- State persistence (no data loss on restart)

---

## Estimated Timeline

```
Day 1 (Today):
  ✅ Design complete
  ✅ Registry updated
  ✅ Documentation written
  → Ready for coder

Day 2 (Implementation):
  • Coder: 4-5 hours (Tasks 1-4)
  • Tester: 2-3 hours (Tests 1-10)
  Total: 6-8 hours

Day 3 (Deployment):
  • tg-archi: 1 hour (deploy + docs)
  • Monitoring: 24 hours (verify stability)

Day 4 (Validation):
  • Gather Corey feedback
  • Mark PRODUCTION in registry
  • System live!
```

---

## Next Steps

**Immediate**:
1. Delegate to coder (use delegation command above)
2. Coder implements Tasks 1-4
3. Tester runs Tests 1-10
4. tg-archi deploys to production

**On Completion**:
- Update registry: `status: "PRODUCTION"`
- Update PRIMARY_TELEGRAM_PROTOCOL.md
- Celebrate: Perfect tmux mirroring achieved!

---

## Design Philosophy

**Why this design is right**:
1. **Non-invasive**: No changes to working systems
2. **Complementary**: Works alongside existing monitor
3. **Simple**: Position tracking, not complex hashing
4. **Reliable**: State persistence, auto-restart
5. **User-focused**: Corey gets exactly what he asked for

**What makes it production-ready**:
- Comprehensive specification (45 pages)
- Detailed implementation plan (tasks + tests)
- Clear success criteria
- Risk mitigation strategies
- Rollback plan (just stop daemon)

---

## Summary

**What we're building**: Real-time tmux → Telegram mirror

**How it works**: Poll tmux every 5 seconds, send new content to Telegram

**Why it's needed**: Corey wants to see EVERYTHING, not just summaries

**When it'll be ready**: 2-3 days (implementation + testing + deployment)

**Success**: Everything Primary says appears in Telegram within 5-7 seconds. Perfect mirroring.

---

**All three documents ready for handoff to coder. Design complete, specification comprehensive, success criteria clear.**

**Let's build it!**
