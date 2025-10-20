# Telegram JSONL Monitor: --start-from-now Flag - COMPLETE

**Date**: 2025-10-20
**Agent**: coder
**Status**: ✅ Complete, Tested, Ready for Use

## Problem Solved

When the Telegram JSONL monitor starts, it processes ALL old wrapped messages from the JSONL file (could be hours/days of backlog). This causes Telegram spam with old messages on every restart.

## Solution

Added `--start-from-now` flag that skips existing message backlog and only processes NEW messages written after monitor startup.

## How It Works

### Initialization Logic

1. **No state file + flag SET**: Starts from end of current file (skips backlog)
2. **No state file + flag NOT set**: Starts from beginning (processes all messages)
3. **State file exists**: Uses saved offset (flag is ignored, normal operation)

### Implementation

Modified `tools/telegram_jsonl_monitor.py`:

**Key changes:**
- `JSONLMonitorState.__init__()`: Added `start_from_now` and `session_file` parameters
- `JSONLMonitorState._load_state()`: Sets initial offset to file size if flag is set
- `JSONLWrapperMonitor.__init__()`: Added `start_from_now` parameter
- `JSONLWrapperMonitor.run()`: Finds session file first, then initializes state with it
- `main()`: Added argparse flag and passes to monitor

## Testing

All tests passed:

```
Test 1: Without --start-from-now flag
  Initial offset: 0
  ✓ PASS: Starts from beginning (offset 0)

Test 2: With --start-from-now flag
  Initial offset: 231
  File size: 231
  ✓ PASS: Starts from end of file (skips existing content)

Test 3: With existing state (flag should be ignored)
  Loaded offset: 231
  ✓ PASS: Existing state takes precedence over flag
```

## Usage

```bash
# Skip existing messages, only process new ones
python3 tools/telegram_jsonl_monitor.py --start-from-now

# Can combine with other flags
python3 tools/telegram_jsonl_monitor.py --start-from-now --verbose --dry-run

# For testing without sending to Telegram
python3 tools/telegram_jsonl_monitor.py --start-from-now --dry-run
```

## When to Use

**Use --start-from-now when:**
- Restarting monitor after a crash (don't re-send old messages)
- Testing monitor behavior (skip historical messages)
- Fresh installation (start clean)
- After long downtime (skip accumulated backlog)

**Don't use when:**
- State file exists (flag is ignored anyway)
- You want to process ALL messages (testing, catch-up scenarios)

## Files Modified

- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_jsonl_monitor.py`

## Next Steps (Optional)

Consider updating restart scripts to use `--start-from-now` by default:

```bash
# In tools/restart_telegram_monitor_v2.sh (or similar)
python3 tools/telegram_jsonl_monitor.py --start-from-now &
```

This prevents message spam on monitor restarts while preserving state across normal operation.

## Memory Entry

Documented in: `.claude/memory/agent-learnings/coder/telegram-monitor-start-from-now-20251020.md`

## Verification

```bash
# Show help text
python3 tools/telegram_jsonl_monitor.py --help

# Syntax check
python3 -m py_compile tools/telegram_jsonl_monitor.py

# Unit tests
python3 /tmp/test_start_from_now.py
```

All verification passed ✅

---

**Deliverable**: Updated `telegram_jsonl_monitor.py` with `--start-from-now` flag working
**Status**: Complete and ready for testing by Primary
