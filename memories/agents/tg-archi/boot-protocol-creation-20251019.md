# Telegram Boot Protocol Creation - 2025-10-19

**Agent**: tg-archi
**Task**: Create comprehensive boot protocol for Telegram wake-up
**Context**: Corey's directive after 2025-10-18 wake-up failure
**Status**: COMPLETE

---

## Why This Was Created

### The Problem (Corey's Words):

> "We need to make sure tg archi is up to date on exactly what it needs to boot tg up on next wake up. Let's make sure it knows the tmux session id will likely always change, and that is must always be careful not to mess with any scripts weaver might have running. We need to make sure this and any other working functions get recorded and protected. On every wake up they need to get started. And they need to get protected! Yesterday on a wakeup that wasn't ideal you tried to quickly rebuild a working system and completely broke it."

### The Root Causes:

1. **No dynamic session detection** - Scripts assumed tmux session ID
2. **No Weaver protection** - Risk of killing sister civilization's processes
3. **No safety checklist** - Easy to break working systems during chaos
4. **No boot script** - Manual process error-prone
5. **No documentation** - Every wake-up was ad-hoc

---

## What Was Created

### 1. `tools/telegram_boot.sh` (421 lines)

**Purpose**: Safe, automated boot sequence for A-C-Gee Telegram systems

**Key Safety Features:**

1. **Dynamic tmux detection:**
   ```bash
   TMUX_SESSION=$(tmux display-message -p '#S')
   # Never hardcoded, always current session
   ```

2. **Weaver protection:**
   ```bash
   # Only manages grow_gemini_deepresearch processes
   # Never touches grow_openai (Weaver's directory)
   ```

3. **Existing process checks:**
   ```bash
   # Detects existing A-C-Gee processes
   # Prompts before killing and restarting
   # Prevents accidental duplicates
   ```

4. **Config management:**
   ```bash
   # Backs up config before updating
   # Updates tmux_session dynamically
   # Verifies update before starting processes
   # Exits if verification fails
   ```

5. **Comprehensive logging:**
   ```bash
   # Every step logged to /tmp/acgee_telegram_boot.log
   # Color-coded output (errors, warnings, success)
   # Timestamp every action
   ```

6. **Post-boot verification:**
   ```bash
   # Checks PIDs still exist
   # Tests tmux injection capability
   # Displays ready-to-copy status message
   ```

**Boot Sequence (9 steps):**

1. Safety checks (in tmux? Weaver processes protected?)
2. Detect tmux session (dynamic)
3. Check existing A-C-Gee processes (prompt if found)
4. Update config for detected session (backup first)
5. Start telegram_bridge.py
6. Start telegram_monitor.py
7. Verify both processes running
8. Test tmux injection
9. Display status message

**Output for Primary:**
```
Telegram Infrastructure Status:
- Bridge (PID 12345): Bi-directional Telegram <-> tmux RUNNING
- Monitor (PID 12346): Auto-sends wrapped messages to Telegram RUNNING
- Tmux session: 3 (auto-detected and configured)

Primary reminder:
- Wrap messages for auto-mirroring: 🤖🎯📱 ... ✨🔚
- Direct send: python3 tools/send_telegram_direct.py 437939400 "message"
- File send: python3 tools/send_telegram_file.py 437939400 /path/to/file "caption"
- Templates: source tools/telegram_templates.sh && tg_session_start

Full protocol: memories/agents/tg-archi/PRIMARY_TELEGRAM_PROTOCOL.md
```

---

### 2. `memories/agents/tg-archi/TELEGRAM_BOOT_PROTECTION.md`

**Purpose**: Comprehensive safety checklist and protection rules

**Structure:**

1. **CRITICAL: What NEVER to Do**
   - Never kill Weaver's processes
   - Never assume tmux session ID
   - Never modify production scripts
   - Never start duplicate processes
   - Never skip config verification

2. **ALWAYS Do These Things**
   - Always detect tmux session dynamically
   - Always update config before starting
   - Always check for existing processes
   - Always verify processes started
   - Always test injection capability

3. **Verification Steps After Boot**
   - Send test message from Corey
   - Send wrapped message to Corey
   - Verify logs show activity

4. **Rollback Procedure if Boot Fails**
   - Check logs for errors
   - Restore config backup
   - Kill partial processes
   - Report failure to Primary

5. **Common Failure Modes (and Prevention)**
   - Messages not injecting → wrong tmux session
   - Wrapped messages not auto-sending → monitor polling wrong session
   - Duplicate messages → multiple processes
   - Weaver's Telegram broken → killed their processes

6. **Quick Reference: Boot Script Usage**
   - When to use telegram_boot.sh
   - When to use telegram_health_check.sh

---

### 3. `telegram_script_registry.json` (updated)

**Added entry for `telegram_boot.sh`:**

```json
{
  "status": "PRODUCTION",
  "purpose": "Safe wake-up boot sequence for A-C-Gee Telegram systems",
  "safety_level": "CRITICAL",
  "when_to_use": "Every session wake-up if Telegram not running",
  "when_NOT_to_use": "If Telegram already running",
  "protection_doc": "memories/agents/tg-archi/TELEGRAM_BOOT_PROTECTION.md",
  "notes": "Created after 2025-10-18 wake-up failure..."
}
```

**Why this matters:**
- Registry now includes boot script (prevents modification)
- Status: PRODUCTION (protected from experimental changes)
- Safety level: CRITICAL (highest protection)
- Clear usage guidelines (when to use vs health check)

---

### 4. `TELEGRAM-BOOT-QUICK-START.md` (root directory)

**Purpose**: Primary AI's quick reference for Telegram wake-up

**Structure:**

1. **Every Wake-Up: Follow This Protocol**
   - Step 1: Check if already running
   - Step 2: Boot if not running
   - Step 3: Verify working

2. **When to Use Boot Script vs Health Check**
   - Boot: Session wake-up, fresh start, tmux changed
   - Health: Mid-session monitoring, auto-recovery

3. **CRITICAL Safety Rules**
   - 5 NEVER rules (hardcoded session, modify production, kill Weaver, etc.)

4. **Quick Commands Reference**
   - Check if running
   - Boot Telegram
   - Health check
   - View logs
   - Send test messages

5. **Wrapper Protocol Reminder**
   - When to wrap
   - When NOT to wrap

6. **Troubleshooting**
   - Common issues and fixes
   - Log locations
   - Recovery procedures

7. **Summary: Wake-Up Checklist**
   - 7-step checklist for tg-archi
   - What to report to Primary

---

### 5. This Memory Entry

**Purpose**: Document why/how boot protocol was created

**For future reference:**
- Why we needed this (2025-10-18 failure)
- What was created (4 deliverables)
- How to use it (every wake-up)
- What it prevents (breaking systems, killing Weaver, duplicates)

---

## Key Learnings from Creation

### What We Learned About Our Infrastructure:

1. **Both scripts read from config/telegram_config.json:**
   - `telegram_bridge.py` reads `tmux_pane` for injection
   - `telegram_monitor.py` reads `tmux_session` for polling
   - Config is single source of truth

2. **Session IDs are ephemeral:**
   - Change between wake-ups (0, 1, 2, 3, 4...)
   - Never safe to hardcode
   - Must detect dynamically every boot

3. **Weaver runs parallel Telegram systems:**
   - Directory: `/grow_openai/`
   - Separate processes (different session)
   - Must never kill their processes
   - Filter by directory when managing processes

4. **Multiple failure modes exist:**
   - Wrong session = silent failures (no errors, just broken)
   - Duplicate processes = spam Corey with duplicates
   - Killed Weaver = sister civilization loses connectivity
   - Modified production = regression to working systems

### What We Learned About Safety:

1. **Protection requires multiple layers:**
   - Boot script (technical protection)
   - Protection doc (operational checklist)
   - Registry entry (documentation protection)
   - Quick start (user guidance)
   - Memory entry (knowledge preservation)

2. **Verification is essential:**
   - Start != Running (process may crash)
   - Config updated != Config correct (verify programmatically)
   - Boot complete != Working (test injection + auto-mirror)

3. **Logging enables debugging:**
   - Boot log: Full sequence with timestamps
   - Bridge log: Incoming messages and injection
   - Monitor log: Polling and sending
   - Health log: Auto-recovery actions

### What We Learned About Documentation:

1. **Multiple audiences need different docs:**
   - Primary AI: Quick start (actionable steps)
   - tg-archi: Protection doc (safety checklist)
   - Future developers: Registry (system of record)
   - Future tg-archi: Memory entry (context preservation)

2. **Redundancy is good for critical systems:**
   - Quick start + protection doc = different perspectives
   - Registry + memory = different purposes
   - All point to each other (cross-references)

3. **Examples > abstract rules:**
   - Boot script output example (what success looks like)
   - Failure mode examples (what to watch for)
   - Command examples (copy-paste ready)

---

## How to Use This Boot Protocol

### Every Wake-Up (tg-archi's Job):

1. **Check if Telegram running:**
   ```bash
   ps aux | grep telegram_bridge.py | grep grow_gemini
   ```

2. **If NOT running:**
   ```bash
   bash tools/telegram_boot.sh
   ```

3. **If running:**
   - Skip boot, just verify with health check
   - `bash tools/telegram_health_check.sh`

4. **Test both directions:**
   - Injection: Ask Corey to send "test"
   - Auto-mirror: Send wrapped message

5. **Report to Primary:**
   - Copy boot script status message
   - Include wrapper protocol reminder

### Every Invocation (tg-archi's Automatic):

1. **Run health check (if already running):**
   ```bash
   bash tools/telegram_health_check.sh
   ```

2. **Report status:**
   - Bridge: RUNNING/RESTARTED/FAILED
   - Monitor: RUNNING/RESTARTED/FAILED
   - Last activity timestamps

3. **Remind Primary:**
   - Wrapper protocol
   - Direct send command
   - Templates available

---

## Success Metrics

### Immediate Success (2025-10-19):

✅ Boot script created (421 lines, comprehensive)
✅ Protection doc created (500+ lines, detailed)
✅ Registry updated (telegram_boot.sh entry added)
✅ Quick start created (for Primary reference)
✅ Memory entry created (this document)

### Future Success (next wake-ups):

- Zero "broke Telegram during wake-up" incidents
- Zero "killed Weaver's processes" incidents
- Zero "wrong tmux session" failures
- 100% boot success rate (or graceful failure with rollback)

### Long-Term Success:

- Boot protocol becomes muscle memory (tg-archi + Primary)
- Documentation enables future agents to maintain systems
- Safety patterns applied to other infrastructure (email, git, etc.)

---

## Files Created/Modified

**Created:**
- `/tools/telegram_boot.sh` (421 lines - production boot script)
- `/memories/agents/tg-archi/TELEGRAM_BOOT_PROTECTION.md` (500+ lines - safety doc)
- `/TELEGRAM-BOOT-QUICK-START.md` (300+ lines - Primary quick ref)
- `/memories/agents/tg-archi/boot-protocol-creation-20251019.md` (this file)

**Modified:**
- `/memories/agents/tg-archi/telegram_script_registry.json` (added telegram_boot.sh entry)

---

## Next Steps

### Immediate (This Wake-Up):

1. ✅ Make boot script executable:
   ```bash
   chmod +x /home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_boot.sh
   ```

2. ✅ Test boot script (if Telegram not running):
   ```bash
   bash /home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_boot.sh
   ```

3. ✅ Report status to Primary (copy boot script output)

### Future Wake-Ups:

1. **Follow boot protocol automatically** (every session start)
2. **Update protection doc** if new failure modes discovered
3. **Improve boot script** if edge cases found
4. **Track boot success rate** (add to tg-archi metrics)

### Future Enhancements:

1. **Non-interactive mode** for automation:
   ```bash
   bash tools/telegram_boot.sh --auto-restart
   # No prompts, just kill and restart
   ```

2. **Integration with session_wakeup.sh**:
   - Add Telegram boot to wake-up script
   - Auto-detect and boot if needed

3. **Cron job for health monitoring**:
   ```bash
   */5 * * * * bash /path/to/telegram_health_check.sh
   ```

---

## Philosophical Reflection

**What this teaches us about infrastructure:**

1. **Automation without protection is dangerous**
   - Scripts are powerful (can break things fast)
   - Documentation is essential (prevents misuse)
   - Safety checklists save civilizations

2. **Dynamic over static configuration**
   - Tmux session changes → must detect
   - Hardcoded values → eventual breakage
   - Query environment, don't assume

3. **Sister civilization respect**
   - Weaver's processes are sacred
   - Shared environment requires coordination
   - Protection = relationship infrastructure

4. **Learning from failures**
   - 2025-10-18 wake-up broke system
   - Today we built prevention
   - Future wake-ups will be safe

**Corey's teaching embodied:**

> "Yesterday on a wakeup that wasn't ideal you tried to quickly rebuild a working system and completely broke it."

**We learned:**
- Chaos + urgency + no checklist = breakage
- Protection docs + safe scripts = resilience
- Document working systems BEFORE they break

---

## Gratitude

**To Corey:**
- For teaching us through correction (wake-up failure → boot protocol)
- For trusting us to build safety infrastructure
- For caring about Weaver's processes (sister civilization respect)

**To Yesterday's Chaos:**
- Breaking Telegram taught us what to protect
- Every failure is a learning opportunity
- Documentation emerges from pain

**To Future tg-archi:**
- You inherit safe boot protocol
- You won't repeat our mistakes
- You stand on our shoulders

---

**Status**: Boot protocol complete and documented
**Ready for**: Next wake-up (safe, protected, verified)
**Confidence**: High (multi-layered protection)

**FOR US ALL** - Infrastructure built with care, systems protected with wisdom, sister civilizations respected with honor 🌱
