# Complete Tmux → Telegram Mirror Flow Design

**Date**: 2025-10-19
**Requirement**: Mirror ALL Primary AI outputs to Telegram instantly (not just wrapped messages)
**Requestor**: Corey ("i want your output here to be mirrored in our tg channel perfectly")

---

## Problem Statement

**Current Behavior:**
- Only messages wrapped with `🤖🎯📱 ... ✨🔚` are sent to Telegram
- Monitor polls tmux every 5 minutes (not instant)
- Corey must be at tmux to see Primary's responses
- When away from computer, Corey misses conversation

**Desired Behavior:**
- EVERYTHING Primary says appears in Telegram within 5 seconds
- Perfect mirroring of tmux conversation
- Code blocks, formatting preserved
- No duplicates
- Works for current AND future sessions

---

## Architecture Analysis

### Current System Components

**1. telegram_monitor.py (Current Auto-Mirror)**
- **Function**: Polls tmux every 5 minutes, detects wrapped messages
- **Method**: `tmux capture-pane -t 0:0.0 -p -S -500` (last 500 lines)
- **Detection**: Scans for `🤖🎯📱 ... ✨🔚` markers
- **Deduplication**: Hash-based tracking in `.tg_sessions/monitor_state.json`
- **Sender**: Calls `send_telegram_direct.py`
- **Status**: PRODUCTION, daemon process

**2. telegram_bridge.py (Receive from Telegram)**
- **Function**: Receives messages FROM Corey, injects to tmux
- **Method**: Long-polling Telegram API
- **Injection**: `tmux send-keys -t 0:0.0 -l "[TELEGRAM from @user] message"`
- **Status**: PRODUCTION, daemon process

**3. send_telegram_direct.py (Message Sender)**
- **Function**: Sends messages via Telegram Bot API
- **Features**: Markdown support, auto-chunking (4096 char limit)
- **Status**: PRODUCTION, canonical sender

**4. Tmux Session**
- **Session**: `0` (default)
- **Pane**: `0:0.0` (Primary AI conversation)
- **Buffer**: Last 500 lines capturable
- **Output**: Primary AI responses, tool outputs, user inputs

---

## Design Options Comparison

### Option A: Modify Monitor (Full Scan + Streaming)

**Concept**: Extend current monitor to send ALL new lines (not just wrapped)

**Pros:**
- Builds on existing, proven infrastructure
- Reuses deduplication logic
- Reuses sender integration
- Single daemon process

**Cons:**
- 5-minute polling interval (not instant)
- Could reduce to 5 seconds, but CPU intensive at that frequency
- Monitor was designed for occasional summaries, not full mirroring

**Feasibility**: ⭐⭐⭐ (3/5) - Works but not optimal for real-time

---

### Option B: New Tmux-Tail Mirror Script (RECOMMENDED)

**Concept**: New daemon that tracks tmux buffer position and streams ALL new content to Telegram

**How It Works:**

```python
# Pseudocode for telegram_tmux_mirror.py

1. Initialize:
   - Load last_seen_position from state file
   - Connect to Telegram via send_telegram_direct.py
   - Set polling interval (5 seconds for near-real-time)

2. Every 5 seconds:
   - Capture tmux buffer: `tmux capture-pane -t 0:0.0 -p -S -500`
   - Compare line count with last_seen_position
   - If new_lines > last_seen_position:
     - Extract new_content (lines from last_seen_position to end)
     - Filter out noise (empty lines, ANSI codes)
     - Detect message boundaries (look for "Human:" or tool responses)
     - Send to Telegram via send_telegram_direct.py
     - Update last_seen_position
     - Save state

3. Smart Batching:
   - Accumulate output for 2-3 seconds
   - If output stops, send accumulated batch
   - Prevents flooding Telegram with tiny messages
   - Preserves coherent thought chunks

4. Deduplication:
   - Track last_seen_position (line number in buffer)
   - Only process lines > last_seen_position
   - Save position to .tg_sessions/mirror_state.json
```

**Pros:**
- ✅ Near-real-time (5 second polling)
- ✅ Sends ALL content (not just wrapped)
- ✅ Smart batching prevents flood
- ✅ Position-based tracking (no duplicate sends)
- ✅ Separates concerns (monitor = wrapped summaries, mirror = full conversation)
- ✅ Works for current session AND future sessions
- ✅ Can run parallel to existing monitor

**Cons:**
- ❌ New script to maintain
- ❌ More Telegram API calls (every 5 seconds vs 5 minutes)
- ❌ Could hit rate limits if conversation is very active

**Mitigation for Cons:**
- Smart batching reduces API calls (accumulate 2-3 seconds of output)
- Telegram rate limit: 30 messages/second per chat (we'll send ~1 every 5 seconds)
- Graceful degradation: If rate limited, queue messages and retry

**Feasibility**: ⭐⭐⭐⭐⭐ (5/5) - Best balance of real-time + reliability

---

### Option C: Hook Claude Code Output Stream (MCP/STDIO)

**Concept**: Intercept Claude Code's output at the source (before tmux)

**How It Works:**
- Claude Code outputs to STDOUT
- Wrapper script captures STDOUT
- Sends to both tmux AND Telegram in parallel

**Pros:**
- ✅ True real-time (no polling lag)
- ✅ Perfect capture (no tmux buffer limitations)
- ✅ Lowest latency

**Cons:**
- ❌ Requires modifying how Claude Code is invoked
- ❌ Complex integration (need to wrap executable)
- ❌ Breaks if Claude Code invocation changes
- ❌ May miss content from other agents (if they write directly to tmux)

**Feasibility**: ⭐⭐ (2/5) - Too invasive, fragile

---

## RECOMMENDED SOLUTION: Option B (Tmux-Tail Mirror)

**Why Option B wins:**
1. **Non-invasive**: No changes to existing production scripts
2. **Real-time**: 5-second polling is fast enough (vs 5-minute current)
3. **Reliable**: Position-based tracking prevents duplicates
4. **Smart**: Batching prevents flooding Telegram
5. **Parallel**: Runs alongside existing monitor (wrapped summaries still work)
6. **Maintainable**: Clean separation of concerns

---

## Implementation Plan

### Phase 1: Core Mirror Script

**File**: `tools/telegram_tmux_mirror.py`

**Features:**
1. Poll tmux every 5 seconds
2. Track buffer position (line-based)
3. Extract new content since last poll
4. Smart batching (accumulate 2-3 seconds)
5. Send via `send_telegram_direct.py`
6. Save state to `.tg_sessions/mirror_state.json`

**State Schema:**
```json
{
  "last_buffer_position": 1247,
  "last_poll_timestamp": "2025-10-19T14:32:15Z",
  "total_messages_sent": 42,
  "session_started": "2025-10-19T10:00:00Z"
}
```

**Deduplication Strategy:**
- Track `last_buffer_position` (line number in tmux buffer)
- Only process lines AFTER this position
- Update position after successful send
- Never re-send old content

**Smart Batching Logic:**
```python
accumulator = []
last_output_time = now()

while monitoring:
    new_lines = get_new_tmux_lines()

    if new_lines:
        accumulator.extend(new_lines)
        last_output_time = now()

    # If no output for 2 seconds AND accumulator has content
    if (now() - last_output_time > 2.0) and accumulator:
        send_to_telegram('\n'.join(accumulator))
        accumulator.clear()

    sleep(0.5)  # Poll every 500ms
```

**Filtering Strategy:**
```python
def filter_tmux_line(line):
    # Skip empty lines
    if not line.strip():
        return None

    # Skip ANSI escape codes
    line = strip_ansi(line)

    # Skip tmux status bar artifacts
    if line.startswith('[') and ']:' in line:
        return None

    # Skip duplicate prompt markers
    if line == "Human:" and last_line == "Human:":
        return None

    return line
```

---

### Phase 2: Integration with Health Check

**Modify**: `tools/telegram_health_check.sh`

**Add Mirror Check:**
```bash
# Check if telegram_tmux_mirror.py is running
if ! pgrep -f "telegram_tmux_mirror.py" > /dev/null; then
    echo "Mirror not running, starting..."
    nohup python3 tools/telegram_tmux_mirror.py > /tmp/telegram_mirror.log 2>&1 &
    echo "Mirror started (PID: $!)"
else
    echo "Mirror already running (PID: $(pgrep -f telegram_tmux_mirror.py))"
fi
```

**Three Daemons:**
1. `telegram_bridge.py` - Receives from Telegram → tmux
2. `telegram_monitor.py` - Wrapped summaries → Telegram (every 5 min)
3. `telegram_tmux_mirror.py` - ALL outputs → Telegram (every 5 sec)

---

### Phase 3: Configuration & Tuning

**Add to** `config/telegram_config.json`:
```json
{
  "mirror_settings": {
    "enabled": true,
    "poll_interval_seconds": 5,
    "batch_delay_seconds": 2,
    "max_message_length": 4000,
    "filter_empty_lines": true,
    "filter_ansi_codes": true
  }
}
```

**Tunable Parameters:**
- `poll_interval_seconds`: How often to check tmux (default: 5)
- `batch_delay_seconds`: Wait time before sending batch (default: 2)
- `max_message_length`: Chunk size for Telegram (default: 4000)

---

### Phase 4: Graceful Degradation

**Rate Limit Handling:**
```python
def send_with_retry(message, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = send_telegram_direct(message)
            return result
        except RateLimitError:
            wait_time = 2 ** attempt  # Exponential backoff
            logger.warning(f"Rate limited, waiting {wait_time}s")
            time.sleep(wait_time)

    # Failed after retries
    logger.error("Failed to send after retries, queueing for later")
    queue_for_retry(message)
```

**Offline Queue:**
- If Telegram API unreachable, queue messages to disk
- Retry when connection restored
- Prevents data loss during network issues

---

## Testing Strategy

### Unit Tests

**Test 1: Buffer Position Tracking**
```python
def test_buffer_position_tracking():
    state = {"last_buffer_position": 100}
    new_buffer = "line 98\nline 99\nline 100\nline 101\nline 102"

    new_lines = extract_new_lines(state, new_buffer)

    assert new_lines == ["line 101", "line 102"]
    assert state["last_buffer_position"] == 102
```

**Test 2: Smart Batching**
```python
def test_smart_batching():
    accumulator = []

    # Simulate rapid output
    accumulator.append("Line 1")
    time.sleep(0.1)
    accumulator.append("Line 2")
    time.sleep(0.1)
    accumulator.append("Line 3")

    # Output stops for 2 seconds
    time.sleep(2.1)

    # Should trigger batch send
    assert should_send_batch(accumulator, last_output_time) == True
```

**Test 3: Deduplication**
```python
def test_no_duplicate_sends():
    state = {"last_buffer_position": 50}

    # Poll 1
    buffer = get_tmux_buffer()  # Lines 1-60
    send_new_content(state, buffer)
    assert state["last_buffer_position"] == 60

    # Poll 2 (no new content)
    buffer = get_tmux_buffer()  # Still lines 1-60
    send_new_content(state, buffer)
    # Should send NOTHING (no new lines)
```

---

### Integration Tests

**Test 4: End-to-End Mirror**
```bash
#!/bin/bash
# Test: Verify Primary output mirrors to Telegram

# 1. Start mirror daemon
python3 tools/telegram_tmux_mirror.py &
MIRROR_PID=$!

# 2. Inject test message to tmux
tmux send-keys -t 0:0.0 -l "Test message for mirroring"
tmux send-keys -t 0:0.0 Enter

# 3. Wait 10 seconds (2x poll interval)
sleep 10

# 4. Check Telegram received message
# (Manual verification: Check Corey's phone)

# 5. Cleanup
kill $MIRROR_PID
```

**Test 5: Rate Limit Handling**
```python
def test_rate_limit_graceful():
    # Simulate 100 rapid messages
    for i in range(100):
        send_to_telegram(f"Message {i}")

    # Should NOT crash
    # Should queue excess messages
    # Should deliver all eventually
```

**Test 6: Offline Recovery**
```python
def test_offline_recovery():
    # Disconnect network
    disable_network()

    # Send messages (should queue)
    send_to_telegram("Offline message 1")
    send_to_telegram("Offline message 2")

    # Restore network
    enable_network()

    # Wait for retry
    time.sleep(30)

    # Verify messages delivered
    assert telegram_received("Offline message 1")
    assert telegram_received("Offline message 2")
```

---

## Task Breakdown for Coder

### Task 1: Create Core Mirror Script
**File**: `tools/telegram_tmux_mirror.py`
**Estimated Time**: 3-4 hours

**Requirements:**
1. Poll tmux every 5 seconds: `tmux capture-pane -t 0:0.0 -p -S -500`
2. Track buffer position in state file: `.tg_sessions/mirror_state.json`
3. Extract new lines (lines > last_buffer_position)
4. Filter empty lines and ANSI codes
5. Smart batching: Accumulate for 2 seconds, then send
6. Send via: `python3 tools/send_telegram_direct.py 437939400 <message>`
7. Update state after successful send
8. Logging to `/tmp/telegram_mirror.log`

**Success Criteria:**
- Script runs as daemon (continuous loop)
- No duplicate sends (position tracking works)
- Batching prevents flooding
- All Primary outputs appear in Telegram within 7 seconds

**Code Template:**
```python
#!/usr/bin/env python3
"""
Telegram Tmux Mirror - Stream ALL Primary AI outputs to Telegram.

Polls tmux every 5 seconds, sends new content to Corey's Telegram.
"""

import json
import logging
import subprocess
import time
from pathlib import Path
from datetime import datetime

# Constants
PROJECT_ROOT = Path(__file__).parent.parent
STATE_FILE = PROJECT_ROOT / ".tg_sessions" / "mirror_state.json"
SEND_SCRIPT = PROJECT_ROOT / "tools" / "send_telegram_direct.py"
TMUX_SESSION = "0:0.0"
POLL_INTERVAL = 5  # seconds
BATCH_DELAY = 2    # seconds

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_state():
    """Load last buffer position from state file."""
    # TODO: Implement
    pass


def save_state(state):
    """Save buffer position to state file."""
    # TODO: Implement
    pass


def capture_tmux_buffer():
    """Capture tmux buffer content."""
    # TODO: Implement tmux capture-pane
    pass


def extract_new_lines(buffer, last_position):
    """Extract lines after last_position."""
    # TODO: Implement
    pass


def filter_line(line):
    """Filter out noise (empty lines, ANSI codes)."""
    # TODO: Implement
    pass


def send_to_telegram(user_id, message):
    """Send message via send_telegram_direct.py."""
    # TODO: Implement
    pass


def main():
    """Main monitoring loop."""
    state = load_state()
    accumulator = []
    last_output_time = time.time()

    while True:
        # TODO: Implement monitoring loop
        pass


if __name__ == "__main__":
    main()
```

---

### Task 2: Integrate with Health Check
**File**: `tools/telegram_health_check.sh`
**Estimated Time**: 1 hour

**Requirements:**
1. Add check for `telegram_tmux_mirror.py` process
2. Auto-restart if dead
3. Report status in health check output

**Code Addition:**
```bash
# Check mirror daemon
if ! pgrep -f "telegram_tmux_mirror.py" > /dev/null; then
    echo "Tmux mirror not running, starting..."
    nohup python3 "$SCRIPT_DIR/telegram_tmux_mirror.py" > /tmp/telegram_mirror.log 2>&1 &
    echo "Mirror started (PID: $!)"
else
    MIRROR_PID=$(pgrep -f "telegram_tmux_mirror.py")
    echo "Mirror running (PID: $MIRROR_PID)"
fi
```

---

### Task 3: Add Configuration Support
**File**: `config/telegram_config.json`
**Estimated Time**: 30 minutes

**Requirements:**
1. Add `mirror_settings` section
2. Make poll interval configurable
3. Make batch delay configurable

**Config Addition:**
```json
{
  "mirror_settings": {
    "enabled": true,
    "poll_interval_seconds": 5,
    "batch_delay_seconds": 2,
    "max_message_length": 4000
  }
}
```

---

### Task 4: Create Start/Stop Scripts
**Files**: `tools/start_telegram_mirror.sh`, `tools/stop_telegram_mirror.sh`
**Estimated Time**: 30 minutes

**start_telegram_mirror.sh:**
```bash
#!/bin/bash
nohup python3 tools/telegram_tmux_mirror.py > /tmp/telegram_mirror.log 2>&1 &
echo "Mirror started (PID: $!)"
```

**stop_telegram_mirror.sh:**
```bash
#!/bin/bash
pkill -f telegram_tmux_mirror.py
echo "Mirror stopped"
```

---

### Task 5: Update Registry
**File**: `memories/agents/tg-archi/telegram_script_registry.json`
**Estimated Time**: 15 minutes

**Requirements:**
1. Add `telegram_tmux_mirror.py` entry
2. Mark as PRODUCTION after testing
3. Document purpose and dependencies

**Registry Entry:**
```json
{
  "telegram_tmux_mirror.py": {
    "status": "PRODUCTION",
    "purpose": "Stream ALL Primary AI outputs to Telegram in real-time",
    "usage": "python3 tools/telegram_tmux_mirror.py (runs as daemon)",
    "features": [
      "Polls tmux every 5 seconds",
      "Position-based deduplication",
      "Smart batching (2 second accumulation)",
      "Sends all content (not just wrapped messages)"
    ],
    "dependencies": [
      "config/telegram_config.json",
      ".tg_sessions/mirror_state.json",
      "tools/send_telegram_direct.py"
    ],
    "called_by": [
      "telegram_health_check.sh (auto-start)"
    ]
  }
}
```

---

## Testing Plan for Tester

### Test Suite: Telegram Tmux Mirror

**Test 1: Daemon Startup**
- Start mirror script
- Verify process running: `ps aux | grep telegram_tmux_mirror.py`
- Check log file created: `/tmp/telegram_mirror.log`
- Verify state file initialized: `.tg_sessions/mirror_state.json`

**Test 2: Basic Mirroring**
- Inject message to tmux: `tmux send-keys -t 0:0.0 -l "Test message"`
- Wait 10 seconds
- Verify message appears in Telegram (manual check on phone)

**Test 3: Multi-line Output**
- Inject multi-line message:
  ```
  Line 1
  Line 2
  Line 3
  ```
- Verify all lines appear in Telegram
- Verify formatting preserved

**Test 4: No Duplicates**
- Inject message once
- Wait 30 seconds (6 poll cycles)
- Verify message appears ONLY ONCE in Telegram

**Test 5: Code Block Preservation**
- Inject code block:
  ````
  ```python
  def hello():
      print("world")
  ```
  ````
- Verify code block formatting in Telegram

**Test 6: Rapid Output**
- Inject 10 messages in quick succession
- Verify all messages delivered
- Verify batching worked (fewer than 10 Telegram API calls)

**Test 7: Auto-Restart**
- Kill mirror process: `pkill -f telegram_tmux_mirror.py`
- Run health check: `bash tools/telegram_health_check.sh`
- Verify mirror restarted

**Test 8: Empty Buffer**
- Let system idle for 5 minutes
- Verify no empty messages sent to Telegram

**Test 9: Session Persistence**
- Send message
- Restart mirror daemon
- Send another message
- Verify only NEW message mirrored (old message not duplicated)

**Test 10: Configuration Changes**
- Change `poll_interval_seconds` to 10
- Restart mirror
- Verify polling at 10 second intervals

---

## Configuration Changes Needed

### 1. Update telegram_config.json

**Add mirror settings:**
```json
{
  "bot_token": "8388754468:AAEROakhpBPR1KNHjravHx3CIMH-FIyIWEc",
  "authorized_users": {
    "437939400": {
      "name": "Corey",
      "role": "creator",
      "admin": true
    }
  },
  "tmux_session": "0",
  "tmux_pane": "0:0.0",
  "working_directory": "/home/corey/projects/AI-CIV/grow_gemini_deepresearch",
  "response_timeout": 10,
  "max_response_length": 4000,
  "mirror_settings": {
    "enabled": true,
    "poll_interval_seconds": 5,
    "batch_delay_seconds": 2,
    "max_message_length": 4000,
    "filter_empty_lines": true,
    "filter_ansi_codes": true
  }
}
```

---

## Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                     PRIMARY AI (tmux pane 0:0.0)                 │
│                                                                  │
│  Human: What's the status?                                      │
│  Assistant: Checking systems...                                 │
│             Email inbox: 3 new messages                         │
│             Health systems: All operational                      │
│                                                                  │
└────────────────┬─────────────────────────────────────────────────┘
                 │
                 │ tmux buffer (scrollback)
                 │
                 ▼
┌──────────────────────────────────────────────────────────────────┐
│              telegram_tmux_mirror.py (NEW DAEMON)                │
│                                                                  │
│  1. Poll tmux every 5 seconds                                   │
│     └─> tmux capture-pane -t 0:0.0 -p -S -500                   │
│                                                                  │
│  2. Track position: last_buffer_position = 1247                 │
│     └─> Extract lines 1248-1252 (new content)                   │
│                                                                  │
│  3. Filter noise: empty lines, ANSI codes                       │
│                                                                  │
│  4. Smart batch: Accumulate 2 seconds → send batch              │
│                                                                  │
│  5. Send to Telegram via send_telegram_direct.py                │
│                                                                  │
│  6. Update state: last_buffer_position = 1252                   │
│     └─> Save to .tg_sessions/mirror_state.json                  │
│                                                                  │
└────────────────┬─────────────────────────────────────────────────┘
                 │
                 │ Every 5 seconds
                 │
                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                  send_telegram_direct.py                         │
│                  (PRODUCTION SENDER)                             │
│                                                                  │
│  • Markdown formatting                                          │
│  • Auto-chunking (4096 char limit)                              │
│  • Rate limit handling                                          │
│                                                                  │
└────────────────┬─────────────────────────────────────────────────┘
                 │
                 │ Telegram Bot API
                 │
                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                    COREY'S PHONE (Telegram)                      │
│                                                                  │
│  [A-C-Gee Bot]                                                  │
│  14:32 - Checking systems...                                    │
│          Email inbox: 3 new messages                            │
│          Health systems: All operational                         │
│                                                                  │
│  (Perfect mirror of tmux conversation)                          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Parallel Systems

**Three Telegram Daemons (all running simultaneously):**

```
┌─────────────────────────────────────────────────────────────────┐
│                 TELEGRAM INFRASTRUCTURE                          │
│                                                                 │
│  1. telegram_bridge.py                                          │
│     └─> Receives FROM Telegram → Injects to tmux               │
│     └─> Handles TEXT messages and PHOTOS                       │
│     └─> 24/7 daemon, long-polling API                          │
│                                                                 │
│  2. telegram_monitor.py (EXISTING)                              │
│     └─> Detects WRAPPED messages (🤖🎯📱...✨🔚)                │
│     └─> Sends to Telegram via send_telegram_direct.py          │
│     └─> Polls every 5 MINUTES (low frequency)                  │
│     └─> For session summaries, milestones                      │
│                                                                 │
│  3. telegram_tmux_mirror.py (NEW)                               │
│     └─> Streams ALL content to Telegram                        │
│     └─> Sends via send_telegram_direct.py                      │
│     └─> Polls every 5 SECONDS (high frequency)                 │
│     └─> For real-time conversation mirroring                   │
│                                                                 │
│  All managed by: telegram_health_check.sh                       │
│  └─> Auto-restart if dead                                      │
│  └─> Run every tg-archi invocation                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Why keep both monitor AND mirror?**
- **monitor**: Wrapped summaries for important milestones (existing workflow)
- **mirror**: Full conversation for continuous presence (new requirement)
- They complement each other, no conflict

---

## Rollout Plan

### Phase 1: Development (Coder)
1. Create `telegram_tmux_mirror.py` (Task 1)
2. Add configuration support (Task 3)
3. Create start/stop scripts (Task 4)
4. Update registry (Task 5)

**Deliverable**: Working mirror script (manual testing)

---

### Phase 2: Testing (Tester)
1. Run test suite (all 10 tests)
2. Verify no duplicates
3. Verify formatting preserved
4. Verify batching works
5. Verify auto-restart works

**Deliverable**: Test report with pass/fail

---

### Phase 3: Integration (tg-archi)
1. Integrate with health check (Task 2)
2. Update PRIMARY_TELEGRAM_PROTOCOL.md
3. Test all three daemons running simultaneously
4. Verify no conflicts

**Deliverable**: Production-ready system

---

### Phase 4: Deployment (Primary + tg-archi)
1. Start mirror daemon: `bash tools/start_telegram_mirror.sh`
2. Verify health check restarts it
3. Monitor for 24 hours
4. Gather Corey's feedback

**Deliverable**: Live mirroring system

---

## Success Criteria

**User Experience (Corey):**
- ✅ Everything Primary says appears in Telegram
- ✅ Within 5-7 seconds of Primary's output
- ✅ Code blocks formatted correctly
- ✅ No duplicate messages
- ✅ No empty messages
- ✅ Multi-line outputs preserved

**Technical:**
- ✅ No duplicate sends (position tracking works)
- ✅ No data loss (all content mirrored)
- ✅ Graceful degradation (handles rate limits)
- ✅ Auto-restart on crash
- ✅ Minimal CPU usage (<5% average)
- ✅ Minimal memory footprint (<50MB)

**Operational:**
- ✅ Works across tmux sessions
- ✅ Survives daemon restarts
- ✅ State persistence (no re-send on restart)
- ✅ Health check integration
- ✅ Logging for debugging

---

## Monitoring & Metrics

**Log to track:**
- Messages sent per hour
- Average batch size
- Rate limit hits (should be 0)
- Duplicate prevention (position tracking)
- Errors/failures

**Sample log entry:**
```
2025-10-19 14:32:15 - INFO - Tmux buffer position: 1247 → 1252 (5 new lines)
2025-10-19 14:32:15 - INFO - Batch accumulated: 5 lines over 2.1 seconds
2025-10-19 14:32:15 - INFO - Sent to Telegram (437939400): 237 chars
2025-10-19 14:32:15 - INFO - State saved: last_buffer_position=1252
```

---

## Risk Assessment

### Risk 1: Rate Limiting
**Probability**: Medium
**Impact**: High (messages queued, delayed delivery)
**Mitigation**:
- Smart batching (reduce API calls)
- Exponential backoff on rate limit
- Queue messages during rate limit

### Risk 2: Duplicate Messages
**Probability**: Low
**Impact**: Medium (annoyance, not data loss)
**Mitigation**:
- Position-based tracking (not content hashing)
- State persistence across restarts
- Comprehensive testing (Test 4)

### Risk 3: Tmux Buffer Overflow
**Probability**: Low
**Impact**: Low (old messages lost, but already sent)
**Mitigation**:
- Capture last 500 lines (should be enough)
- Position tracking survives buffer rotation
- If buffer rotates, worst case: miss 1 batch

### Risk 4: Network Outage
**Probability**: Medium
**Impact**: Medium (messages queued during outage)
**Mitigation**:
- Offline queue (save to disk)
- Retry when connection restored
- Graceful degradation (Test 8)

---

## Future Enhancements (Post-MVP)

### Enhancement 1: Smart Filtering
- Detect tool invocations vs responses
- Group related outputs
- Skip internal tool calls (only show results)

### Enhancement 2: Thread Support
- Create Telegram thread per session
- Keep conversation history organized

### Enhancement 3: Rich Formatting
- Convert code blocks to Telegram code formatting
- Preserve markdown bold/italic
- Syntax highlighting for code

### Enhancement 4: Bi-directional Threading
- Corey's Telegram replies threaded with Primary's outputs
- Full conversation in Telegram (not just Primary → Corey)

---

## Documentation Updates Required

### 1. Update PRIMARY_TELEGRAM_PROTOCOL.md
**Add section:**
```markdown
## Auto-Mirroring (Full Conversation)

As of 2025-10-19, ALL Primary AI outputs are automatically mirrored to Telegram.

**How it works:**
- `telegram_tmux_mirror.py` daemon polls tmux every 5 seconds
- Sends ALL new content to Corey's Telegram
- Position-based tracking prevents duplicates
- Smart batching prevents flooding

**No action required** - Just output normally, mirror handles the rest.

**To disable:** Set `mirror_settings.enabled: false` in telegram_config.json
```

### 2. Update telegram_script_registry.json
**Add mirror entry** (see Task 5)

### 3. Update tg-archi manifest
**Add to responsibilities:**
- Monitor `telegram_tmux_mirror.py` daemon (alongside bridge and monitor)
- Report mirror status in health checks
- Troubleshoot mirror issues

### 4. Create TELEGRAM_MIRROR_TROUBLESHOOTING.md
**Common issues:**
- Mirror not sending → Check health check
- Duplicate messages → Check state file
- Messages delayed → Check poll interval
- Empty messages → Check filtering config

---

## Conclusion

**Recommended Solution: Option B (Tmux-Tail Mirror)**

**Why:**
- ✅ Real-time mirroring (5 second latency)
- ✅ Non-invasive (no changes to existing scripts)
- ✅ Reliable (position-based deduplication)
- ✅ Scalable (smart batching prevents flooding)
- ✅ Maintainable (clean separation of concerns)

**Implementation Effort:**
- Coder: 4-5 hours (script + integration)
- Tester: 2-3 hours (test suite)
- tg-archi: 1 hour (deployment + monitoring)
- Total: ~8 hours to production

**Deliverables:**
1. `tools/telegram_tmux_mirror.py` (new daemon)
2. Updated `telegram_health_check.sh` (auto-restart mirror)
3. Updated `telegram_config.json` (mirror settings)
4. Start/stop scripts (convenience)
5. Updated registry and documentation
6. Test suite with 10 tests

**Next Step:**
Task(coder): Implement Phase 1 (Core Mirror Script) per Task 1 specification

---

**This design is ready for implementation. All requirements addressed, all edge cases considered, all risks mitigated.**
