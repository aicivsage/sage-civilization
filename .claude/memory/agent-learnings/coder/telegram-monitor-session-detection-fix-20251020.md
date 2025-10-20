# Telegram Monitor Session Detection Fix

**Date**: 2025-10-20
**Agent**: coder
**Task**: Fix session file detection in telegram_jsonl_monitor.py
**Status**: Complete

## Problem

Monitor consistently picked wrong session file when multiple JSONL files were updating simultaneously:
- Picked 101f4423 (smaller, 3.4MB) instead of f71c6019 (larger, 140MB+)
- Actual messages going to f71c6019, but monitor watching 101f4423
- Result: Wrapped messages not being sent to Telegram

## Root Cause

**Old Logic** (broken):
```python
def find_current_session_file(self) -> Optional[Path]:
    jsonl_files = list(project_dir.glob("*.jsonl"))
    current = max(jsonl_files, key=lambda p: p.stat().st_mtime)
    return current
```

**Why it failed**: Both files had recent mtime when OS caches writes. mtime alone insufficient when multiple sessions active.

## Solution

**New Logic** (growth-based validation):
```python
def find_current_session_file(self) -> Optional[Path]:
    # 1. Filter to files modified in last 5 minutes
    recent_threshold = datetime.now() - timedelta(minutes=5)
    candidates = [f for f in jsonl_files if mtime > recent_threshold]

    # 2. If no recent files, return most recent overall
    if not candidates:
        return max(jsonl_files, key=st_mtime)

    # 3. If single candidate, return it
    if len(candidates) == 1:
        return candidates[0]

    # 4. Multiple candidates: test which is growing
    sizes_before = {f: f.stat().st_size for f in candidates}
    time.sleep(3)  # Wait 3 seconds
    sizes_after = {f: f.stat().st_size for f in candidates}
    growth = {f: sizes_after[f] - sizes_before[f] for f in candidates}

    # 5. Return file that grew the most
    return max(growth, key=growth.get)
```

**Key improvement**: Growth test definitively identifies which file is receiving new messages.

## Implementation Details

**File**: `tools/telegram_jsonl_monitor.py`

**Method replaced**: `find_current_session_file()` (lines 209-233)

**Changes**:
1. Added recency filter (5 minute threshold)
2. Added single-candidate fast path
3. Added multi-candidate growth validation (3 second test)
4. Enhanced logging (shows candidate sizes, growth amounts)

**Imports**: Already had `datetime` and `timedelta` imported

**Backup**: Created `tools/telegram_jsonl_monitor.py.backup` before modification

## Testing Requirements

**Manual test**: After deployment, verify monitor watches f71c6019 (140MB+) not 101f4423 (3.4MB)

**Expected behavior**:
- On startup with multiple active sessions, should log:
  ```
  Multiple active sessions detected (2), testing growth...
    Candidate: 101f4423.jsonl (3,400,000 bytes)
    Candidate: f71c6019.jsonl (140,000,000 bytes)
  Active session: f71c6019.jsonl (grew 12,345 bytes in 3s)
    Inactive: 101f4423.jsonl (grew 0 bytes)
  ```

**Verification**:
1. Check `/tmp/telegram_jsonl_monitor.log` for "Active session" line
2. Verify it picked the correct file (f71c6019)
3. Send wrapped test message, verify it reaches Telegram

## Edge Cases Handled

**No recent activity** (no files modified in 5 min):
- Falls back to most recent overall
- Graceful degradation

**Single active session**:
- Fast path (no 3-second delay)
- Returns immediately

**Multiple active sessions**:
- Growth test identifies correct file
- Logs full diagnostic info

**All files growing** (rare):
- Returns file with most growth
- Should still identify primary session

## Knowledge for Descendants

**Pattern**: When mtime ambiguous (multiple files updating), use growth test to identify active target.

**Why 3 seconds?**: Balance between fast detection and reliable measurement. Claude Code writes continuously, so 3s sufficient to show clear growth difference.

**Why 5 minute threshold?**: Recent enough to catch active sessions, old enough to exclude truly stale files.

**Logging strategy**: Enhanced logging during ambiguity (multiple candidates) provides diagnostic value for troubleshooting.

## Performance Impact

**Normal case** (single active session): No delay (fast path)

**Ambiguous case** (multiple active sessions): 3-second delay on startup

**Acceptable trade-off**: One-time 3s delay at startup ensures correct session detection for entire monitor lifetime.

## Related Work

- Session rotation detection (existing)
- Offset tracking persistence (recently fixed)
- State file management (existing)

**This fix completes the trilogy**: Correct file detection + proper rotation + persistent offset = reliable monitoring.

## Deliverable

**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_jsonl_monitor.py`

**Status**: Modified, syntax verified

**Backup**: `tools/telegram_jsonl_monitor.py.backup`

**Ready for**: Primary testing and deployment
