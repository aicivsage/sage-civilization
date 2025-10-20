# Telegram JSONL Monitor: --start-from-now Flag Implementation

**Agent**: coder
**Date**: 2025-10-20
**Type**: Feature Implementation
**Status**: Complete, Tested

## Context

When the Telegram JSONL monitor starts, it processes ALL wrapped messages from the JSONL file history. This could be hours or days of backlog, causing Telegram spam with old messages on every restart.

**Problem**: Monitor needed ability to skip existing backlog and only process new messages written after startup.

## Solution: --start-from-now Flag

Added command-line flag that initializes the file offset to the current end of file when:
1. Flag is set (`--start-from-now`)
2. No existing state file (fresh start)

If state file exists, it uses the saved offset (flag is ignored).

## Implementation Details

### Key Changes

1. **JSONLMonitorState.__init__()**: Added parameters
   - `start_from_now: bool = False`
   - `session_file: Optional[Path] = None`

2. **JSONLMonitorState._load_state()**: Enhanced logic
   - If no existing state AND `start_from_now` is True:
     - Get current file size
     - Set `last_processed_offset = file_size`
     - Log skip message
   - If state exists: Use saved offset (ignore flag)

3. **JSONLWrapperMonitor.__init__()**: Added parameter
   - `start_from_now: bool = False`
   - Defer state initialization until session file found

4. **JSONLWrapperMonitor.run()**: Changed initialization order
   - Find session file FIRST
   - Initialize state with session file and flag
   - Then enter watch loop

5. **argparse**: Added flag
   ```python
   parser.add_argument("--start-from-now", action="store_true",
                       help="Skip existing messages, only process new messages written after startup (ignored if state file exists)")
   ```

### Test Results

All tests passed:
- ✓ Without flag: Starts from offset 0 (processes all messages)
- ✓ With flag: Starts from end of file (skips existing content)
- ✓ With existing state: Uses saved offset (flag ignored)

## Usage

```bash
# Skip existing messages, only process new ones
python3 tools/telegram_jsonl_monitor.py --start-from-now

# Can combine with other flags
python3 tools/telegram_jsonl_monitor.py --start-from-now --verbose

# In production restart scripts
./tools/restart_telegram_monitor_v2.sh  # (can update to use --start-from-now)
```

## Benefits

1. **Clean restarts**: No Telegram spam from old messages
2. **Safer testing**: Can restart monitor without re-sending everything
3. **State preservation**: Flag is ignored if state exists (normal operation continues)
4. **Opt-in**: Default behavior unchanged (backwards compatible)

## Files Modified

- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_jsonl_monitor.py`

## Pattern Learned

**When implementing "skip to end" for file watchers:**
1. Get file size before opening
2. Seek to that offset
3. Only needed on FIRST run (no state file)
4. Subsequent runs use saved state

**Key insight**: Don't use flag after state file exists - saved state is source of truth.

## Next Steps

Consider updating restart scripts to use `--start-from-now` by default to prevent message spam on monitor restarts.
