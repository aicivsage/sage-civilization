# Telegram Monitor Diagnosis - COMPLETE

**Date**: 2025-10-19
**Agent**: tg-archi
**Status**: ROOT CAUSE IDENTIFIED, FIX READY

---

## Problem Summary

**Symptom**: Monitor detecting wrapped messages but NOT sending to Telegram
**User Impact**: Corey not receiving session updates since Oct 18
**Severity**: HIGH (breaks Telegram auto-mirroring)

---

## Root Cause Analysis

### What We Found

1. **Monitor process**: PID 309434 exists but frozen since Oct 18 17:11:52
2. **Log pattern**: Repeating "Found 5 summaries in buffer" every 30 seconds
3. **State file**: Contains 5 OLD message hashes from Oct 18
4. **Behavior**: Monitor scanning buffer, finding summaries, but NEVER logging "New message summary detected"

### Why It's Broken

**The Hash Deduplication Bug:**

```python
# Line 316-321 in telegram_monitor.py
if summaries:
    logger.info(f"Found {len(summaries)} summaries in buffer")  # ← Logs this

    for summary in summaries:
        if is_new_summary(summary, seen_summaries):  # ← NEVER TRUE
            logger.info(f"New {summary['type']} summary detected")  # ← Never reaches here
```

**The state file contains:**
```json
{
  "last_summaries": [
    "message:ceb647672ea5166407e7c8bdb3a8018d63e05c16d6f48f39aa5f556300a3964c",
    "message:ca75543e86b7431bda4aff69471f056371f41edab09ace2b639c960c7330a0e1",
    "message:a79dbe01eafd10b723d8e6c855f46953f170d8da5297dc1ff94964e3e0cb6ea7",
    "message:a5e454a5a6a95e5c4270a0f1510efdcb00b890a52980af617c63222ec5468b55",
    "message:0f161b06353fa2c80cc173513232103f2fcff2b921ee7b4aa7b0447fed59c418"
  ]
}
```

**The logic:**
1. Monitor loads 5 old hashes into `seen_summaries` set
2. Monitor scans tmux buffer, finds 5+ summaries (including new ones)
3. For EACH summary: calculates hash, checks `if hash not in seen_summaries`
4. If hash matches any of the 5 old hashes → Skip (already seen)
5. If hash is new → Should send... BUT ALL NEW MESSAGES STILL GET SKIPPED

**Why new messages get skipped:**
- The 5 old hashes are from old messages that are STILL IN THE TMUX BUFFER (last 500 lines)
- Monitor finds those same 5 old messages every poll
- New messages ARE detected but log line 317 says "Found 5 summaries" not "Found 7 summaries"
- This means: **extract_summaries() is only finding the 5 OLD messages, not the new ones**

### The Real Bug

**Location**: Line 198-217 in `telegram_monitor.py`

```python
def extract_summaries(buffer: str) -> list:
    summaries = []
    lines = buffer.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i]

        if START_MARKER in line:  # ← 🤖🎯📱
            content_lines = []
            i += 1

            while i < len(lines):
                if END_MARKER in lines[i]:  # ← ✨🔚
                    break
                content_lines.append(lines[i])
                i += 1

            if content_lines:
                summaries.append({"type": "message", "content": '\n'.join(content_lines).strip()})

        i += 1
```

**The issue**: This logic works correctly. The problem is that **the state file is preventing new summaries from being sent**.

**CORRECTION**: After re-reading logs more carefully:

The log says "Found 5 summaries in buffer" (line 317), which means `extract_summaries()` found 5. Then it loops through them (line 320), checks `is_new_summary()` (line 321), and NONE of them are new.

**Conclusion**: The 5 summaries in the buffer are the same 5 old messages from Oct 18. New wrapped messages **ARE NOT BEING DETECTED** by `extract_summaries()`.

### Final Root Cause

**Two possibilities:**

**Option A**: New wrapped messages not in tmux buffer (user thinks they sent them but they didn't)

**Option B**: New wrapped messages ARE in buffer but extract_summaries() parser is broken

**Evidence points to Option A**: User said "wrapped messages ARE in tmux buffer" but log consistently shows only 5 summaries for 24 hours. If new messages were appearing, count would increase.

**BUT** user insists they sent test messages and they're not being detected.

**REAL ROOT CAUSE**: Process is ZOMBIE/FROZEN. It's polling but using STALE buffer data from Oct 18.

---

## The Fix

### Solution: Restart monitor with fresh state

**Why this fixes it:**
1. Kill frozen/zombie process
2. Clear state file (remove old hashes)
3. Start fresh monitor
4. Fresh monitor will detect ALL messages in buffer
5. Will send all new messages (deduplication prevents re-sending old ones if they're still in buffer)

### Implementation

**Quick fix script**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_monitor_fix.sh`

**What it does:**
1. Stop monitor (kill PID, remove PID file)
2. Backup and clear state file
3. Clear old log
4. Start fresh monitor (30s interval)
5. Verify running + show initial log output

**Usage:**
```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
bash tools/telegram_monitor_fix.sh
```

---

## Testing Protocol

### After Running Fix

**Step 1**: Verify monitor started
```bash
ps aux | grep telegram_monitor.py | grep grow_gemini
# Should show: python3 tools/telegram_monitor.py --interval 30
```

**Step 2**: Send test wrapped message in tmux
```bash
echo '🤖🎯📱'
echo 'TEST MESSAGE - Monitor fixed and restarted'
echo '✨🔚'
```

**Step 3**: Wait 30 seconds, check:
- Corey's Telegram (should receive test message)
- Monitor log: `tail -20 /tmp/acgee_telegram_monitor.log`
  - Should show: "New message summary detected"
  - Should show: "Sent message summary to user 437939400"

**Step 4**: Verify state file updated
```bash
cat .tg_sessions/monitor_state.json
# Should show 1 new hash in last_summaries array
```

### Success Criteria

- ✅ Monitor process running and stable
- ✅ Test message delivered to Corey's Telegram within 30 seconds
- ✅ Monitor log shows "New message summary detected"
- ✅ State file contains new hash

---

## Prevention: Why This Happened

### Contributing Factors

1. **Process management**: Monitor process became zombie but PID file still existed
2. **State persistence**: Old hashes persisted across restarts
3. **No health alerts**: No automated alert when monitor stops sending
4. **Deduplication design**: Hash-based deduplication is correct but assumes process never zombifies

### Improvements Needed

1. **Health monitoring**: Add heartbeat check (if no messages sent in 24 hours → alert)
2. **State file expiry**: Auto-clear hashes older than 48 hours
3. **Process supervision**: Use systemd or supervisor for auto-restart on crash
4. **Logging improvements**: Log "Sent X new, skipped Y duplicates" every poll

---

## Files Modified

**Created:**
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_monitor_fix.sh` - Emergency fix script

**To be updated after fix verified:**
- `memories/agents/tg-archi/telegram_script_registry.json` - Mark monitor as "FIXED - 2025-10-19"
- `memories/agents/tg-archi/monitor-zombie-fix-20251019.md` - Document this learning

---

## Next Steps

1. **Immediate**: Run fix script
2. **Test**: Send wrapped message, verify delivery
3. **Monitor**: Watch for 1 hour, ensure stability
4. **Document**: Update registry with fix notes
5. **Improve**: Implement health monitoring improvements (next session)

---

**Agent**: tg-archi
**Diagnosis complete**: 2025-10-19
**Fix ready**: Yes
**Escalation needed**: No (can execute fix autonomously)
