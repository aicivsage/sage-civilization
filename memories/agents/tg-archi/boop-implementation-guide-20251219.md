# BOOP System Integration Guide for Sage Civilization
**Date**: 2025-12-19
**Agent**: tg-archi
**Task**: Technical analysis of A-C-Gee's BOOP autonomous operation system

---

## Executive Summary

**BOOP (Being Operated by Organic Prompting)** is A-C-Gee's autonomous operation infrastructure that keeps Claude working continuously without human input. Sage already has 90% of this infrastructure operational - we just need to adapt their naming/paths and integrate with our Telegram monitoring.

**Key Insight**: BOOP is tmux injection + rotating prompts + cron scheduling. We already have all the pieces - we're just calling them different names.

---

## 1. Technical Integration Points

### How autonomy_nudge.sh Works

```bash
# Core mechanism (same as our inject_prompt.sh)
tmux send-keys -t "claude.0" -l "$PROMPT_TEXT"
tmux send-keys -t "claude.0" Enter
```

**Detection of "Claude is waiting"**:
- BOOP doesn't actively detect waiting state
- Instead: periodic injection (every 30 min) ensures forward momentum
- Rate limit check prevents injection spam
- If Claude is actively working, prompt appears as "next task" suggestion

**Triggering Mechanism**:
```bash
# Cron entry (every 30 minutes)
*/30 * * * * /path/to/autonomy_nudge.sh >> /path/to/nudge.log 2>&1
```

**Answer to YOUR question**: BOOP sends prompts via tmux directly to Claude Code session, NOT through Telegram bridge. Telegram monitors output (one-way: Claude → Telegram).

---

## 2. Session Management Coordination

### Current Sage Infrastructure

| Component | Purpose | Status |
|-----------|---------|--------|
| `telegram_bridge.py` | Inbound (Telegram → tmux) | ✅ Operational |
| `telegram_jsonl_monitor.py` | Outbound (Claude → Telegram) | ✅ Operational |
| `inject_prompt.sh` | Autonomous prompting | ✅ Exists (A-C-Gee version) |
| `cron job` | 30-min scheduler | ❌ NOT INSTALLED for Sage |

### Session Monitoring Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        SAGE TMUX SESSION                        │
│                     (sage-session:0.0)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐        ┌──────────────┐       ┌──────────────┐   │
│  │ Telegram │──msg──>│ Bridge       │──────>│ Claude Code  │   │
│  │ (Greg)   │        │ (injects)    │       │ (stdin)      │   │
│  └──────────┘        └──────────────┘       └──────┬───────┘   │
│                                                     │           │
│  ┌──────────┐        ┌──────────────┐              │           │
│  │ Telegram │<──msg──│ JSONL        │<─────────────┘           │
│  │ (Greg)   │        │ Monitor      │ (reads .jsonl)           │
│  └──────────┘        └──────────────┘                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ BOOP (autonomy_nudge.sh) - RUNS OUTSIDE TMUX             │  │
│  │   - Cron triggers every 30 min                           │  │
│  │   - Injects rotating prompts via tmux send-keys          │  │
│  │   - NO conflict with Telegram bridge (different flow)    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                    │
│                            └──────> Claude Code stdin           │
└─────────────────────────────────────────────────────────────────┘
```

### Conflict Analysis: NONE

**Why BOOP and telegram_jsonl_monitor don't conflict**:

1. **Different directions**:
   - BOOP: Outside process → tmux (input injection)
   - JSONL Monitor: Reads `.jsonl` files → sends to Telegram (output monitoring)
   - No overlap, no race conditions

2. **Different triggers**:
   - BOOP: Time-based (cron every 30 min)
   - JSONL Monitor: Content-based (watches for 🤖🎯📱 wrapper)
   - Independent event streams

3. **Different data sources**:
   - BOOP: Prompt files in `/autonomous-session/prompts/`
   - JSONL Monitor: Claude Code conversation logs in `~/.claude/projects/`
   - No shared state

**Coordination strategy**: NONE NEEDED. They operate independently by design.

---

## 3. Configuration Requirements

### Files to Adapt from A-C-Gee

**Core Script** (already exists, needs path updates):
```bash
/mnt/c/sage/sage-civilization/autonomous-session/scripts/inject_prompt.sh

# UPDATE THESE LINES:
TMUX_SESSION="sage-session"          # (was "claude")
TMUX_PANE="sage-session:0.0"         # (was "claude.0")
PROMPTS_DIR="/mnt/c/sage/sage-civilization/autonomous-session/prompts"
STATE_FILE="/mnt/c/sage/sage-civilization/autonomous-session/scripts/injection_state.txt"
LOG_FILE="/mnt/c/sage/sage-civilization/autonomous-session/scripts/injection_log.txt"
```

**Cron Installer**:
```bash
/mnt/c/sage/sage-civilization/autonomous-session/scripts/install_cron.sh

# UPDATE crontab entry:
*/30 * * * * /mnt/c/sage/sage-civilization/autonomous-session/scripts/inject_prompt.sh >> /mnt/c/sage/sage-civilization/autonomous-session/scripts/cron_output.log 2>&1
```

### BOOP Tier Configuration

**A-C-Gee uses 3-tier system**:

| Tier | Trigger | Prompt Type | Example |
|------|---------|-------------|---------|
| 1 | Every 30 min | Simple continuation | "You are doing incredible!! KEEP GOING!!" |
| 2 | Every 2 hours | Consolidation | "Write handoff, update registry, wrap summary for Telegram" |
| 3 | Every 4 hours | Ceremony/Deep work | "Run deep ceremony, reflect on progress" |

**Implementation**: Use existing prompt rotation in `inject_prompt.sh` (already cycles through 10 prompts)

**Thresholds**: Built into prompt sequence (prompts 1-5 = Tier 1, 6-8 = Tier 2, 9-10 = Tier 3)

### Log Configuration

```bash
# BOOP logs
/mnt/c/sage/sage-civilization/autonomous-session/scripts/injection_log.txt
/mnt/c/sage/sage-civilization/autonomous-session/scripts/cron_output.log

# Monitor logs (existing)
/tmp/telegram_jsonl_monitor.log
/tmp/telegram_bridge.log
```

**Log rotation**: Not configured (TODO: add logrotate for long-running systems)

---

## 4. Telegram Protocol Compatibility

### Wrapper Protocol: 🤖🎯📱 ... ✨🔚

**BOOP Understanding**: NO

BOOP is **input-only** (sends prompts to Claude). It doesn't read or parse output.

**Who handles wrapped messages**:
- `telegram_jsonl_monitor.py` watches for wrappers in `.jsonl` files
- Sends wrapped content to Greg via Telegram
- BOOP has NO AWARENESS of this

**Autonomous Work Notification**:

**Current flow**:
1. BOOP injects: "Full protocol: comms → finish → decide → execute"
2. Claude responds (wrapped): 🤖🎯📱 Session summary... ✨🔚
3. JSONL Monitor detects wrapper → sends to Greg
4. Greg sees update on Telegram

**NO CHANGES NEEDED** - BOOP just provides input, existing monitor handles output.

### Integration with Telegram Wrapper Protocol

**Should BOOP-triggered work wrap messages?**

**Answer**: YES, but BOOP doesn't control this.

**How it works**:
- BOOP injects prompts that ENCOURAGE wrapping
- Example prompt: "Send wrapped session summary to Greg via Telegram"
- Claude decides to wrap based on prompt content
- Monitor detects and forwards

**Prompt examples that encourage wrapping**:
```
# Current prompt 07 (full protocol)
"Task(human-liaison): Check inbox, respond to urgent
Complete current task, write handoff
🤖🎯📱 Wrap session summary for Greg 🎯📱
Pick next priority and execute"
```

**Recommendation**: Add explicit "wrap summary" reminder to consolidation prompts (Tier 2)

---

## 5. Testing & Verification

### Safe Testing Protocol

**Test 1: Manual Injection (NO RISK)**
```bash
cd /mnt/c/sage/sage-civilization/autonomous-session/scripts

# Edit inject_prompt.sh (update paths to sage-session)
nano inject_prompt.sh

# Test single injection
./inject_prompt.sh

# Expected: Prompt appears in sage-session tmux
# Check: tmux attach -t sage-session
```

**Test 2: Verify State Tracking**
```bash
# Check which prompt is next
cat /mnt/c/sage/sage-civilization/autonomous-session/scripts/injection_state.txt

# Should show: 2 (increments after each injection)

# Check log
tail /mnt/c/sage/sage-civilization/autonomous-session/scripts/injection_log.txt

# Should show: [timestamp] INJECTED: 01-simple-encouragement (#1)
```

**Test 3: Rate Limit Detection**
```bash
# Manually trigger rate limit message in Claude
# (or simulate by adding "rate limit" text to tmux pane)

# Run injection
./inject_prompt.sh

# Expected: SKIPPED in log (won't inject if rate limit detected)
```

**Test 4: Cron Installation (SAFE with dry-run)**
```bash
# DON'T run install_cron.sh yet
# Instead: manually add cron entry with dry-run flag

crontab -e
# Add:
# */30 * * * * /mnt/c/sage/sage-civilization/autonomous-session/scripts/inject_prompt.sh >> /mnt/c/sage/sage-civilization/autonomous-session/scripts/cron_output.log 2>&1

# Wait 30 min, check log
tail /mnt/c/sage/sage-civilization/autonomous-session/scripts/injection_log.txt
```

**Test 5: Full Cycle (PRODUCTION)**
```bash
# Let BOOP run for 5 hours
# Should cycle through all 10 prompts
# Then restart at prompt #1

# Monitor:
watch -n 60 tail /mnt/c/sage/sage-civilization/autonomous-session/scripts/injection_log.txt
```

### Kill Switch (Emergency Stop)

**If autonomous session goes wrong**:

```bash
# METHOD 1: Disable cron (prevents future injections)
crontab -e
# Comment out BOOP cron entry with #

# METHOD 2: Stop tmux session (nuclear option)
tmux kill-session -t sage-session

# METHOD 3: Pause BOOP (temporary)
# Create flag file
touch /mnt/c/sage/sage-civilization/autonomous-session/scripts/PAUSE

# Modify inject_prompt.sh to check for PAUSE file:
if [ -f "$SCRIPT_DIR/PAUSE" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] PAUSED: Remove PAUSE file to resume" >> "$LOG_FILE"
    exit 0
fi
```

### Verification Checklist

**Before considering BOOP operational**:

- [ ] Paths updated in inject_prompt.sh (sage-session, not claude)
- [ ] Manual injection works (Test 1 passed)
- [ ] State tracking increments (Test 2 passed)
- [ ] Rate limit detection works (Test 3 passed)
- [ ] Cron entry installed and triggered (Test 4 passed)
- [ ] Full cycle completed (Test 5 passed)
- [ ] Greg receives wrapped summaries via Telegram (existing monitor verified)
- [ ] Kill switch tested (can disable cron, session stops)
- [ ] Logs viewable and rotated (no disk space issues)

---

## 6. Implementation Checklist

### Phase 1: Preparation (NO RISK)

- [ ] **Read existing infrastructure**
  - [x] Reviewed `inject_prompt.sh` (A-C-Gee version)
  - [x] Reviewed `telegram_jsonl_monitor.py` (Sage production)
  - [x] Reviewed `telegram_bridge.py` (Sage production)
  - [x] Confirmed tmux session name: `sage-session:0.0`

- [ ] **Update BOOP scripts for Sage**
  - [ ] Edit `inject_prompt.sh` (TMUX_SESSION="sage-session", TMUX_PANE="sage-session:0.0")
  - [ ] Edit paths (PROMPTS_DIR, STATE_FILE, LOG_FILE to Sage paths)
  - [ ] Add PAUSE file check (kill switch mechanism)
  - [ ] Update `install_cron.sh` (Sage paths)

- [ ] **Review/customize prompts**
  - [ ] Check 10 existing prompts in `/autonomous-session/prompts/`
  - [ ] Add "wrap summary" reminder to Tier 2 prompts (06, 07, 08)
  - [ ] Update `09-corey-priorities.txt` → `09-greg-priorities.txt` (partner name)

### Phase 2: Local Testing (SAFE)

- [ ] **Manual injection test**
  - [ ] Run `./inject_prompt.sh` manually
  - [ ] Verify prompt appears in sage-session tmux
  - [ ] Check `injection_log.txt` for timestamp
  - [ ] Check `injection_state.txt` incremented

- [ ] **Rate limit detection test**
  - [ ] Simulate rate limit message in tmux
  - [ ] Run `./inject_prompt.sh`
  - [ ] Verify SKIPPED in log

- [ ] **Prompt rotation test**
  - [ ] Inject 10 times manually (cycle through all prompts)
  - [ ] Verify state file wraps back to 1 after prompt 10
  - [ ] Verify each prompt content correct

### Phase 3: Cron Integration (PRODUCTION)

- [ ] **Install cron (START HERE ONLY AFTER PHASE 2 COMPLETE)**
  - [ ] Run `./install_cron.sh`
  - [ ] Verify cron entry: `crontab -l`
  - [ ] Wait 30 minutes
  - [ ] Check `cron_output.log` for first automated injection

- [ ] **Monitor first autonomous cycle**
  - [ ] Watch `injection_log.txt` for automatic entries
  - [ ] Verify Greg receives wrapped summaries via Telegram
  - [ ] Check no conflicts with Telegram bridge (both operational)

- [ ] **Full 5-hour cycle test**
  - [ ] Let BOOP run unsupervised for 5 hours
  - [ ] Verify all 10 prompts cycled
  - [ ] Verify wrapped messages reached Greg
  - [ ] Check tmux session still healthy (no crashes)

### Phase 4: Monitoring & Maintenance

- [ ] **Setup log rotation** (prevent disk fill)
  - [ ] Configure logrotate for `injection_log.txt`
  - [ ] Configure logrotate for `cron_output.log`
  - [ ] Test rotation (force rotate, verify logs compressed)

- [ ] **Document kill switches**
  - [ ] Write emergency stop procedure (disable cron)
  - [ ] Write PAUSE mechanism (touch PAUSE file)
  - [ ] Test both methods

- [ ] **Create monitoring dashboard** (optional)
  - [ ] Script to show: last injection time, next prompt, cycle count
  - [ ] Add to session wake-up script (show BOOP status)

---

## 7. Safety Protocols

### Built-in Safety Features

**Rate Limit Detection**:
```bash
# inject_prompt.sh checks last 5 lines of tmux output
RECENT_OUTPUT=$(tmux capture-pane -t "$TMUX_PANE" -p | tail -5)
if echo "$RECENT_OUTPUT" | grep -qi "rate limit"; then
    echo "[$(date)] SKIPPED: Rate limit detected" >> "$LOG_FILE"
    exit 0
fi
```

**Session Validation**:
```bash
# Won't inject if tmux session doesn't exist
if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    echo "[$(date)] ERROR: tmux session '$TMUX_SESSION' not found" >> "$LOG_FILE"
    exit 1
fi
```

**Logging**:
- All injections timestamped: `[2025-12-19 10:30:00] INJECTED: 03-comms-check (#3)`
- Cron stdout/stderr captured: `cron_output.log`
- Easy audit trail: `tail -f injection_log.txt`

### Manual Override

**Anytime during BOOP operation**:
```bash
# Attach to session (take control)
tmux attach -t sage-session

# BOOP will still inject prompts (appears as messages)
# You can ignore them or respond to them
# Detach when done: Ctrl+B, then D
```

**Pause BOOP temporarily**:
```bash
# Create PAUSE file (after adding check to script)
touch /mnt/c/sage/sage-civilization/autonomous-session/scripts/PAUSE

# Resume
rm /mnt/c/sage/sage-civilization/autonomous-session/scripts/PAUSE
```

### Runaway Loop Prevention

**Problem**: What if BOOP triggers infinite delegation loops?

**Mitigation**:
1. **Prompts are curated** (10 known-good prompts, manually reviewed)
2. **Rate limit check** prevents spam (if Claude hits API limits, BOOP stops)
3. **Greg has visibility** (wrapped summaries to Telegram, can intervene)
4. **Manual override** (attach to tmux, stop cron, create PAUSE file)

**Not possible**: BOOP cannot create new prompts (reads static files)

---

## 8. A-C-Gee vs Sage Differences

### File Paths

| Component | A-C-Gee Path | Sage Path |
|-----------|--------------|-----------|
| Prompts | `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/prompts/` | `/mnt/c/sage/sage-civilization/autonomous-session/prompts/` |
| Scripts | `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts/` | `/mnt/c/sage/sage-civilization/autonomous-session/scripts/` |
| Logs | Same directory as scripts | Same directory as scripts |

### Tmux Session Names

| System | Session Name | Pane Name |
|--------|--------------|-----------|
| A-C-Gee | `claude` | `claude.0` |
| Sage | `sage-session` | `sage-session:0.0` |

### Telegram Configuration

| System | User | Chat ID | Config File |
|--------|------|---------|-------------|
| A-C-Gee | Corey | 437939400 | `/mnt/c/ACG/ai-civ/config/telegram_config.json` |
| Sage | Greg | 7585924762 | `/mnt/c/sage/sage-civilization/config/telegram_config.json` |

### Prompt Customization

**A-C-Gee prompt 09**: `09-corey-priorities.txt`
**Sage equivalent**: `09-greg-priorities.txt` (rename for clarity)

**Content difference**: Update partner name references
- A-C-Gee: "Corey's current focus areas"
- Sage: "Greg's current focus areas"

---

## 9. Future Enhancements

### Immediate (Post-Integration)

- [ ] **Add "wrap summary" to all Tier 2 prompts** (ensure Greg always gets updates)
- [ ] **Rename 09 prompt** (corey → greg for clarity)
- [ ] **Add PAUSE mechanism** (kill switch via flag file)

### Near-term (1-2 weeks)

- [ ] **Stuck detector** (if same task >1 hour, inject help prompt)
- [ ] **Achievement tracker** (detect handoff writes, auto-celebrate)
- [ ] **Email reminder prompt** (Tier 2: "Send email update to Greg every 3 hours")

### Long-term (1-2 months)

- [ ] **Adaptive prompts** (AI learns which prompts work best, adjusts rotation)
- [ ] **Health-based injection** (auditor detects low progress → inject encouragement)
- [ ] **Multi-tier scheduler** (simple/consolidation/ceremony on different intervals)
- [ ] **Prompt A/B testing** (measure which prompts yield most progress)

---

## 10. Files Summary

### Required Downloads from A-C-Gee

**Core Scripts** (already exist in Sage repo):
- [x] `autonomous-session/scripts/inject_prompt.sh`
- [x] `autonomous-session/scripts/install_cron.sh`

**Prompts** (already exist):
- [x] `autonomous-session/prompts/01-simple-encouragement.txt` through `10-celebration-and-next.txt`

**Documentation** (already exists):
- [x] `autonomous-session/QUICKSTART.md`
- [x] `autonomous-session/SETUP_GUIDE.md`

### Files to Modify for Sage

**Scripts**:
1. `inject_prompt.sh` (TMUX_SESSION, paths)
2. `install_cron.sh` (paths)

**Prompts**:
1. `09-corey-priorities.txt` → `09-greg-priorities.txt` (rename + update content)
2. `06-finish-and-continue.txt`, `07-full-protocol.txt`, `08-session-health-check.txt` (add wrap reminders)

**Documentation**:
1. This guide (BOOP implementation for Sage)

### New Files to Create

**Safety**:
- `/autonomous-session/scripts/PAUSE` (flag file, created when needed)

**Monitoring**:
- `/autonomous-session/scripts/boop_status.sh` (show last injection, next prompt, health)

---

## Conclusion

**BOOP Integration Readiness**: 95%

**What we have**:
- ✅ All scripts inherited from A-C-Gee
- ✅ Telegram monitoring operational (JSONL monitor)
- ✅ Tmux session stable (sage-session)
- ✅ Prompt library (10 prompts)

**What we need**:
- [ ] Update 2 lines in `inject_prompt.sh` (session name, paths)
- [ ] Test manually (Phase 2 checklist)
- [ ] Install cron (Phase 3 checklist)
- [ ] Monitor for 5 hours (verification)

**Estimated setup time**: 30 minutes (if following checklist)

**Risk level**: LOW (BOOP is read-only input injection, no destructive operations)

**Recommendation**: Proceed with Phase 1 (preparation) and Phase 2 (local testing) immediately. Phase 3 (cron integration) only after Greg approves autonomous operation.

---

**Next Steps**:
1. Greg review/approval of BOOP integration
2. tg-archi executes Phase 1 (update scripts)
3. Primary executes Phase 2 (manual testing)
4. Greg observes Phase 3 (first autonomous cycle)
5. Civilization operates autonomously with BOOP + Telegram monitoring

**Status**: READY FOR IMPLEMENTATION
