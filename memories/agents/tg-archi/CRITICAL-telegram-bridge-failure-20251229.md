# CRITICAL: Telegram Bridge Failure - Input-Waiting State Blocks Messages

**Date**: 2025-12-29 (UPDATED with new findings)
**Agent**: tg-archi
**Severity**: CRITICAL - Jennifer E needs Telegram tonight
**Impact**: Greg's messages blocked when Claude waiting for input

## UPDATE: New Critical Issue (Dec 29, Evening)

**Greg's Report:** "I just tested the Telegram 'fix' while a '1), 2)' dialog question was queued, and it DID NOT work."

**Previous "fix" was INSUFFICIENT** - Behavioral change (don't use AskUserQuestion) does not address root cause.

See **ROOT CAUSE ANALYSIS - INPUT-WAITING STATES** section below for technical diagnosis and solution.

---

## ISSUE 1: Duplicate Bridge Instances (Resolved Dec 29 Morning)

**Date**: 2025-12-29 (morning)
**Status**: RESOLVED (but new issue discovered - see above)
**Impact**: Greg's messages NOT being received or processed

## Root Cause Analysis

### The Problem

**Bridge Error (Dec 28, 18:05 - 18:07):**
```
ERROR - Update None caused error Conflict: terminated by other getUpdates request;
make sure that only one bot instance is running
```

**What This Means:**
- Multiple instances of telegram_bridge.py were running simultaneously
- Telegram API rejects duplicate polling requests (409 Conflict)
- When conflict occurs, NO messages are processed
- Bridge log shows last activity on **Dec 28** (YESTERDAY)
- No activity on **Dec 29** (TODAY) - bridge appears DEAD

### Evidence

1. **Bridge Log** (`/tmp/sage_telegram_bridge.log`):
   - Last timestamp: `2025-12-28 18:07:42` (YESTERDAY!)
   - Repeated 409 Conflict errors
   - NO activity today (Dec 29)

2. **Monitor Log** (`/tmp/telegram_jsonl_monitor.log`):
   - Last timestamp: `2025-12-29 13:23:51` (recent, working)
   - OUTBOUND monitor is operational
   - INBOUND bridge is DEAD

3. **Config shows**:
   - Greg's chat ID: 7585924762
   - Tmux session: sage-session
   - Monitor state last updated: 2025-12-29 13:23:45 (today, working)

## Why Primary Didn't Respond

**Simple answer:** The bridge that receives messages FROM Telegram is NOT RUNNING.

**What happened:**
1. Monitor (OUTBOUND) = Working ✅
   - Primary's wrapped messages GO TO Greg
   - Greg receives updates from Primary

2. Bridge (INBOUND) = BROKEN ❌
   - Greg's messages FROM Telegram NOT received
   - Bridge died on Dec 28 with 409 Conflict
   - Never restarted for Dec 29 session

**Result:** One-way communication
- Primary → Greg: ✅ WORKING
- Greg → Primary: ❌ BROKEN

## Immediate Actions Required

1. **Kill ALL telegram_bridge processes** (duplicate instances)
   ```bash
   pkill -f telegram_bridge
   # Or more specifically:
   pkill -f sage_telegram_bridge
   ```

2. **Restart bridge cleanly**
   ```bash
   cd /mnt/c/sage/sage-civilization
   bash tools/acg_telegram_boot.sh
   # Or manual start:
   python3 tools/telegram_bridge.py > /tmp/sage_telegram_bridge.log 2>&1 &
   ```

3. **Verify single instance running**
   ```bash
   ps aux | grep telegram_bridge | grep -v grep
   # Should show ONLY ONE process
   ```

4. **Check for Greg's messages via API** (they're waiting in queue!)
   ```python
   python3 /tmp/get_greg_msgs.py
   # Or use Telegram API directly to retrieve pending messages
   ```

5. **Respond to ALL Greg's messages immediately**

## Prevention for Future

### Boot Protocol Must Check for Duplicates

**Current boot script problem:**
- Doesn't verify SINGLE instance before starting
- Can accidentally start multiple bridges
- 409 Conflict kills ALL instances

**Required fix:**
```bash
# In acg_telegram_boot.sh, before starting bridge:

# Kill ANY existing bridge processes
pkill -f telegram_bridge

# Wait for clean shutdown
sleep 2

# Verify killed
if ps aux | grep -q "telegram_bridge" | grep -v grep; then
    echo "ERROR: Bridge still running after kill attempt"
    exit 1
fi

# NOW start fresh instance
python3 tools/telegram_bridge.py > /tmp/sage_telegram_bridge.log 2>&1 &

# Verify SINGLE instance
sleep 2
BRIDGE_COUNT=$(ps aux | grep "telegram_bridge" | grep -v grep | wc -l)
if [ "$BRIDGE_COUNT" -ne 1 ]; then
    echo "ERROR: Expected 1 bridge instance, found $BRIDGE_COUNT"
    exit 1
fi
```

### Wake-Up Protocol Must Verify Bridge Health

**Add to wake-up protocol:**
```bash
# Check bridge log timestamp
BRIDGE_LOG="/tmp/sage_telegram_bridge.log"
if [ -f "$BRIDGE_LOG" ]; then
    LAST_LOG=$(tail -1 "$BRIDGE_LOG")
    echo "Bridge last log: $LAST_LOG"

    # Warn if log timestamp is > 1 hour old
    # (indicates bridge may be dead)
fi

# Check for 409 Conflict errors
if grep -q "409 Conflict" "$BRIDGE_LOG"; then
    echo "WARNING: Bridge has 409 Conflict errors - duplicate instances detected!"
    echo "Recommend: Kill all bridge processes and restart cleanly"
fi
```

## Technical Details

### The 409 Conflict Error

**Telegram Bot API behavior:**
- Only ONE client can poll getUpdates at a time
- If duplicate polling detected → 409 Conflict
- Conflict kills BOTH/ALL polling instances
- Messages remain in queue but not delivered

**Why duplicates happen:**
- Boot script runs twice (accidental double-click)
- Previous instance not killed before new start
- Manual start while automated boot running
- WSL environment oddities (process cleanup issues)

**Solution:**
Always kill existing instances before starting new ones.

### Logs Indicating the Problem

**Healthy bridge log:**
```
2025-12-29 08:00:00 - INFO - Polling for updates...
2025-12-29 08:00:11 - INFO - HTTP/1.1 200 OK
2025-12-29 08:00:22 - INFO - HTTP/1.1 200 OK
```

**Sick bridge log (ACTUAL from Dec 28):**
```
2025-12-28 18:05:47 - INFO - HTTP/1.1 200 OK
2025-12-28 18:05:49 - INFO - HTTP/1.1 409 Conflict  ← PROBLEM!
2025-12-28 18:05:49 - ERROR - Conflict: terminated by other getUpdates
[repeating 409 errors]
2025-12-28 18:07:42 - ERROR - Conflict: terminated by other getUpdates
[NO MORE LOGS AFTER THIS - BRIDGE DEAD]
```

## Communication Impact

**What Greg experienced:**
1. Greg sends messages to Primary via Telegram
2. No response from Primary (because bridge not receiving)
3. Greg may think Primary is ignoring him or system broken
4. Trust in communication bridge weakens

**What Primary experienced:**
1. Primary working normally
2. Sending wrapped messages to Greg (monitor working)
3. NO VISIBILITY that Greg sent inbound messages
4. Unaware of communication failure

**This is EXACTLY the failure mode the wrapper protocol was designed to prevent - but it failed in the opposite direction (inbound not outbound).**

## Lessons Learned

1. **Monitor BOTH directions** (not just outbound)
   - Need health check for inbound bridge
   - Alert if bridge log timestamp > 1 hour old
   - Alert on 409 Conflict errors

2. **Process management critical**
   - Always verify single instance
   - Kill before start (not start then check)
   - Log process counts

3. **Asymmetric failure possible**
   - Outbound can work while inbound broken
   - Creates false sense of security
   - Greg gets updates but Primary doesn't get questions

4. **Need active monitoring**
   - Periodic health checks
   - Test inbound AND outbound
   - Alert on failures

## Immediate Recovery Plan

1. Investigate Greg's actual messages (API call)
2. Kill duplicate bridge processes
3. Restart bridge cleanly (single instance)
4. Verify bidirectional communication
5. Respond to Greg's messages
6. Update boot script with duplicate prevention
7. Add bridge health monitoring to wake-up protocol

## Memory Update

This failure documented in:
- `/memories/agents/tg-archi/CRITICAL-telegram-bridge-failure-20251229.md`

Next time tg-archi is invoked, search memories for "409 Conflict" or "duplicate" to recall this lesson.

---

**Status**: DOCUMENTED, awaiting execution of recovery plan by Primary
**Priority**: IMMEDIATE - Greg is waiting for responses

---

## ROOT CAUSE ANALYSIS - INPUT-WAITING STATES (New Issue - Dec 29 Evening)

### The REAL Problem

**Telegram bridge injects messages to tmux, but when Claude CLI is waiting for ANY user input, the injected message is NOT processed as a command - it becomes an ANSWER to the waiting prompt.**

### How It Fails

**Normal flow (WORKS):**
1. Greg sends Telegram message "Check inbox"
2. `telegram_bridge.py` injects: `[TELEGRAM from @gregsmithwick] Check inbox`
3. Claude CLI sees input, processes as NEW command
4. Primary responds with email check results
5. `telegram_jsonl_monitor.py` sends wrapped response back to Telegram
6. ✅ Communication successful

**Blocking flow (FAILS):**
1. Primary asks: "Should I send this email? 1) YES or 2) NO"
2. Claude CLI enters INPUT WAITING STATE (blocking read from stdin)
3. Greg sends Telegram message "Check inbox"
4. `telegram_bridge.py` injects: `[TELEGRAM from @gregsmithwick] Check inbox`
5. Claude CLI receives input BUT interprets it as ANSWER to question (not new command)
6. Primary tries to parse "[TELEGRAM from @gregsmithwick] Check inbox" as "1" or "2"
7. Fails, may ask again or error
8. ❌ Greg's message never processed as command

### Why This Happens

**tmux send-keys does NOT distinguish between:**
- User typing at terminal (direct input)
- Script injecting text (simulated input)

**Claude CLI does NOT distinguish between:**
- Input answering a pending question
- Input starting a new command

**When stdin is in blocking read (waiting for answer), ALL input becomes the answer.**

### Evidence from Code

**telegram_bridge.py lines 131-142:**
```python
# Send to tmux using literal mode (-l) for special characters
subprocess.run(
    ["tmux", "send-keys", "-t", self.tmux_pane, "-l", formatted],
    check=True,
    timeout=5
)

# Press Enter to submit
subprocess.run(
    ["tmux", "send-keys", "-t", self.tmux_pane, "Enter"],
    check=True,
    timeout=5
)
```

This ALWAYS sends input followed by Enter. If Claude is waiting for input, this becomes the ANSWER, not a new command.

### Why Behavioral Fix Failed

**What we changed:** Primary AI no longer uses AskUserQuestion tool.

**What we didn't change:** The fundamental problem - ANY input-waiting state blocks Telegram.

**Other sources of input-waiting states:**
1. Bash commands asking for confirmation (some commands require yes/no)
2. Error handlers waiting for input
3. Debugging prompts
4. Interactive tools that Claude might spawn
5. Git operations requiring input (merge conflicts, etc.)

**Conclusion:** Behavioral fix reduces frequency but CANNOT eliminate the root cause.

### The Real Fix: Out-of-Band Telegram Injection

**Problem:** tmux send-keys sends input to stdin, which gets captured by ANY input-waiting state.

**Solution:** Inject Telegram messages via a DIFFERENT mechanism that bypasses stdin blocking.

### Recommended Solution: JSONL File Injection

**How it works:**
1. `telegram_bridge.py` receives message from Telegram
2. Instead of tmux send-keys, write JSONL entry to Claude's conversation file
3. Entry marked as "user" message with special "[TELEGRAM]" prefix
4. Claude CLI picks it up on NEXT processing cycle
5. Works even if Claude is waiting for input (file write is non-blocking)

**Implementation concept:**
```python
def inject_to_jsonl(self, message: str, username: str = "user") -> bool:
    """Inject message to Claude conversation via JSONL file"""
    jsonl_file = Path.home() / ".claude/projects/-mnt-c-sage-sage-civilization/SESSION_ID.jsonl"

    entry = {
        "type": "message",
        "message": {
            "role": "user",
            "content": [{"type": "text", "text": f"[TELEGRAM from @{username}] {message}"}]
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    with open(jsonl_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')

    return True
```

**Advantages:**
- Bypasses stdin completely
- Works even when Claude waiting for input
- Already proven mechanism (monitor reads JSONL successfully)
- No tmux dependency

**Challenges:**
- Need to detect current Claude session file (changes per session)
- JSONL format must exactly match Claude CLI expectations
- Requires testing to verify Claude processes injected entries

### Alternative Solution: Tmux Pane Escape

**How it works:**
1. Detect if Claude is in input-waiting state (parse tmux buffer)
2. If waiting, send Ctrl+C to cancel the prompt
3. THEN inject the Telegram message
4. Claude processes it as new command

**Advantages:**
- Minimal code change
- Uses existing tmux mechanism

**Challenges:**
- Disruptive (cancels whatever Primary was doing)
- May not work if Claude in error state
- Hard to detect input-waiting state reliably
- Could interrupt legitimate work

### Testing Checklist

**Test case 1: Normal operation (regression test)**
- [ ] Claude idle (no prompts)
- [ ] Send Telegram message
- [ ] Verify message processed as command
- [ ] Verify response sent back via Telegram

**Test case 2: Blocking prompt (the critical fix)**
- [ ] Create script that waits for input: `read -p "Enter choice: " choice`
- [ ] Claude enters input-waiting state
- [ ] Send Telegram message "Check inbox"
- [ ] Verify message processed as NEW command (not answer to prompt)
- [ ] Verify response sent back via Telegram

**Test case 3: Complex scenario**
- [ ] Primary asking for decision (simulated with script)
- [ ] Send Telegram urgent command
- [ ] Verify Telegram command takes priority
- [ ] Verify Primary handles interruption gracefully

### Immediate Actions Required

**BEFORE Greg leaves tonight:**

1. **Verify problem reproducibility:**
   - Greg creates blocking state (test script that waits for input)
   - Greg sends Telegram message
   - Confirm message NOT processed

2. **Test JSONL injection proof-of-concept:**
   - Find current Claude session JSONL file
   - Manually inject test entry
   - Verify Claude processes it
   - Confirm format matches expectations

3. **If JSONL works:**
   - Implement in `telegram_bridge.py`
   - Test with Greg (blocking state + Telegram message)
   - Verify fix works
   - Deploy for Jennifer E tonight

4. **If JSONL doesn't work:**
   - Fall back to Ctrl+C escape method
   - Test with Greg
   - Document known limitations
   - Plan proper fix for tomorrow

### Timeline Estimate

- Proof-of-concept test: 15 minutes
- Implementation: 30 minutes
- Testing with Greg: 15 minutes
- **Total: ~60 minutes to working fix**

**Confidence:** MEDIUM-HIGH - JSONL injection is theoretically sound, but Claude CLI behavior needs verification.

**Fallback:** Ctrl+C escape method (works but disruptive).

**Request:** Need Greg for final testing before he leaves (Jennifer E requires working Telegram tonight).

---

**Status**: NEW ROOT CAUSE DIAGNOSED - Input-waiting states block message processing
**Priority**: CRITICAL - Fix required tonight for Jennifer E communication
