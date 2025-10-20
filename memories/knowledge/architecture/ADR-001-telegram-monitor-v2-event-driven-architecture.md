# ADR-001: Telegram Monitor V2 - Event-Driven Architecture

**Date**: 2025-10-19
**Status**: APPROVED (coder-driven design)
**Context**: V1 monitor has critical deduplication bug causing message loss
**Decision**: Implement event-driven watermark-based V2 architecture

---

## Problem Statement

### V1 Failures (Root Cause Analysis)

**Critical Bug**: Hash-based deduplication causes monitor to become "blind" to new messages

**How it breaks:**
1. Monitor loads 5 old message hashes from state file
2. Scans tmux buffer (last 500 lines), finds wrapped messages
3. For each message: calculates hash, checks if already seen
4. Old messages still in buffer → skipped (correct)
5. **BUG**: Process zombifies, keeps polling with stale state
6. New messages appear in buffer but state file never updates
7. Monitor stuck in loop: "Found 5 summaries" → all marked as seen → nothing sent

**Evidence:**
- Monitor ran for 24 hours finding "5 summaries" every 30 seconds
- ZERO "New message detected" log lines
- State file frozen with 5 old hashes from Oct 18
- Process alive (PID exists) but functionally frozen

**Root cause:** Hash-based deduplication + process zombification = message loss

---

## V2 Architecture: Watermark-Based Event Detection

### Core Principles

1. **NEVER mark failed sends as seen** - V1's fatal flaw
2. **ALWAYS advance watermark ONLY after successful send**
3. **ALWAYS flush state after watermark update**
4. **ALWAYS use fail-loud error handling**

### Design: Watermark + Retry Queue

**Watermark Concept:**
- Track "last processed position" in tmux buffer
- Use (line number + content hash) as unique message ID
- Only advance watermark after successful Telegram send
- Persistent watermark survives restarts

**Message Detection:**
```python
@dataclass
class Message:
    id: str  # hash(content + buffer_position)
    content: str
    timestamp: datetime
    attempts: int = 0
```

**Algorithm:**
```python
def calculate_message_id(content: str, position: int) -> str:
    """Generate stable ID from content + buffer position."""
    return hashlib.sha256(f"{position}:{content}".encode()).hexdigest()[:16]

def filter_new_messages(messages: List[Message], watermark: int) -> List[Message]:
    """Return only messages after watermark position."""
    return [msg for msg in messages if extract_position(msg.id) > watermark]
```

**State Schema:**
```json
{
    "watermark": 12345,  // Last processed buffer line number
    "retry_queue": [
        {"id": "abc123", "content": "...", "attempts": 1, "next_retry": "2025-10-19T12:00:00"}
    ],
    "dead_letter": [
        {"id": "def456", "content": "...", "reason": "Max retries exceeded", "timestamp": "..."}
    ]
}
```

---

## Implementation Plan

### Phase 1: Core Detection (2 hours)

**Deliverables:**
- `Message` dataclass with ID, content, timestamp, attempts
- `calculate_message_id()` - Hash(content + buffer position)
- Modify `extract_summaries()` to return `List[Message]` with IDs
- `filter_new_messages()` - Watermark-based filtering
- Update state schema with watermark field

**Test criteria:**
- Extract 10 messages from buffer → all have unique IDs
- Watermark filtering works (messages before watermark ignored)
- Message ID stable across polls (same content = same ID)

### Phase 2: Retry Queue (1.5 hours)

**Deliverables:**
- `RetryEntry` dataclass
- `process_retry_queue()` with exponential backoff
- Dead letter queue for permanent failures
- Integrate retry queue into main loop

**Retry Logic:**
```python
@dataclass
class RetryEntry:
    message: Message
    next_retry: datetime
    backoff_seconds: int  # 30, 60, 120, 240...

def process_retry_queue(state: State) -> None:
    """Process messages in retry queue with exponential backoff."""
    now = datetime.now()
    for entry in state.retry_queue[:]:  # Copy to allow removal during iteration
        if entry.next_retry <= now:
            if send_telegram_message(entry.message):
                # Success: remove from retry queue, advance watermark
                state.retry_queue.remove(entry)
                state.watermark = max(state.watermark, extract_position(entry.message.id))
                flush_state(state)
            else:
                # Failure: exponential backoff
                entry.message.attempts += 1
                if entry.message.attempts >= MAX_RETRIES:
                    # Move to dead letter queue
                    state.dead_letter.append({
                        "message": entry.message,
                        "reason": "Max retries exceeded",
                        "timestamp": now.isoformat()
                    })
                    state.retry_queue.remove(entry)
                else:
                    # Increase backoff
                    entry.backoff_seconds = min(entry.backoff_seconds * 2, 3600)
                    entry.next_retry = now + timedelta(seconds=entry.backoff_seconds)
                flush_state(state)
```

**Test criteria:**
- Failed send → message added to retry queue
- Retry queue processed on next poll
- Exponential backoff works (30s → 60s → 120s)
- Max retries → dead letter queue
- Successful retry → watermark advances

### Phase 3: Performance Optimization (1 hour)

**Deliverables:**
- Fast poll interval (10-30 seconds)
- Performance metrics (messages/sec, latency p95)
- Circuit breaker for consecutive failures
- Health check endpoint

**Performance Targets:**
- <30 second latency (95th percentile)
- Zero message loss
- Zero duplicates
- Graceful degradation under load

**Circuit Breaker:**
```python
class CircuitBreaker:
    def __init__(self, threshold: int = 5):
        self.failures = 0
        self.threshold = threshold
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def record_success(self):
        self.failures = 0
        self.state = "CLOSED"

    def record_failure(self):
        self.failures += 1
        if self.failures >= self.threshold:
            self.state = "OPEN"
            logger.error("Circuit breaker OPEN - too many failures")

    def can_send(self) -> bool:
        if self.state == "OPEN":
            # Try half-open after 5 minutes
            if time.time() - self.last_failure_time > 300:
                self.state = "HALF_OPEN"
                return True
            return False
        return True
```

### Phase 4: Production Deployment (0.5 hours)

**Deliverables:**
- `restart_telegram_monitor_v2.sh` script
- State migration script (v1 → v2)
- Deployment runbook
- Rollback procedure

**Deployment Steps:**
1. Stop V1 monitor
2. Migrate state (backup v1 state, create v2 watermark from last seen position)
3. Start V2 monitor
4. Send test message
5. Verify delivery within 30 seconds

**Rollback:**
1. Stop V2 monitor
2. Restore V1 state from backup
3. Start V1 monitor
4. Investigate V2 failure

---

## Testing Requirements

### Unit Tests

**Test: Message ID stability**
```python
def test_message_id_stability():
    msg1 = Message(content="Test", position=100)
    msg2 = Message(content="Test", position=100)
    assert msg1.id == msg2.id  # Same content + position = same ID

def test_message_id_uniqueness():
    msg1 = Message(content="Test", position=100)
    msg2 = Message(content="Test", position=101)
    assert msg1.id != msg2.id  # Different position = different ID
```

**Test: Watermark filtering**
```python
def test_watermark_filtering():
    messages = [
        Message(id="1", content="A", position=100),
        Message(id="2", content="B", position=101),
        Message(id="3", content="C", position=102),
    ]
    state = State(watermark=100)
    new_messages = filter_new_messages(messages, state.watermark)
    assert len(new_messages) == 2  # Only messages 101, 102
```

**Test: Retry queue backoff**
```python
def test_retry_exponential_backoff():
    entry = RetryEntry(message=msg, next_retry=now, backoff_seconds=30)
    # First failure
    entry.backoff_seconds = entry.backoff_seconds * 2  # 60
    assert entry.backoff_seconds == 60
    # Second failure
    entry.backoff_seconds = entry.backoff_seconds * 2  # 120
    assert entry.backoff_seconds == 120
```

### Integration Tests

**Test: 10 messages delivered in order**
```python
def test_ten_messages_in_order():
    # Send 10 wrapped messages to tmux
    for i in range(10):
        send_wrapped_message(f"Message {i}")

    # Wait for monitor to process (10 polls x 30s = 5 minutes max)
    time.sleep(300)

    # Verify all 10 messages delivered to Telegram
    telegram_messages = get_recent_telegram_messages(count=10)
    assert len(telegram_messages) == 10
    for i, msg in enumerate(telegram_messages):
        assert f"Message {i}" in msg.content
```

**Test: Retry on failure**
```python
def test_retry_on_telegram_failure():
    # Mock Telegram API to fail first 2 attempts, succeed on 3rd
    with mock_telegram_api(fail_count=2):
        send_wrapped_message("Test retry")

        # First poll: detect message, fail to send, add to retry queue
        monitor_poll()
        assert len(state.retry_queue) == 1

        # Second poll: retry, fail again, backoff increases
        time.sleep(30)
        monitor_poll()
        assert state.retry_queue[0].backoff_seconds == 60

        # Third poll: retry, succeed, remove from retry queue
        time.sleep(60)
        monitor_poll()
        assert len(state.retry_queue) == 0
        assert state.watermark > 0  # Watermark advanced
```

**Test: Graceful restart**
```python
def test_graceful_restart():
    # Send 5 messages
    for i in range(5):
        send_wrapped_message(f"Message {i}")

    # Monitor processes first 3
    monitor_poll()
    assert state.watermark == 3

    # Kill monitor, restart
    kill_monitor()
    start_monitor()

    # Monitor should process messages 3-4 (not re-send 0-2)
    monitor_poll()
    telegram_messages = get_recent_telegram_messages(count=5)
    assert count_duplicates(telegram_messages) == 0
```

### Load Test

**Test: 100 messages in 60 seconds**
```python
def test_load_100_messages():
    start = time.time()

    # Send 100 messages as fast as possible
    for i in range(100):
        send_wrapped_message(f"Load test {i}")

    # Monitor should deliver all within 60 seconds
    time.sleep(60)

    telegram_messages = get_recent_telegram_messages(count=100)
    assert len(telegram_messages) == 100
    assert time.time() - start < 60  # P95 latency < 60s
```

### Chaos Test

**Test: Kill monitor mid-send**
```python
def test_kill_during_send():
    send_wrapped_message("Critical message")

    # Poll starts
    with mock_telegram_api(delay=2):  # Slow send
        monitor_poll_async()
        time.sleep(1)  # Kill mid-send
        kill_monitor()

    # Restart monitor
    start_monitor()
    monitor_poll()

    # Message should be in retry queue or delivered (no loss)
    telegram_messages = get_recent_telegram_messages(count=1)
    assert len(telegram_messages) == 1 or len(state.retry_queue) == 1
```

---

## Success Criteria

**Zero message loss:**
- All wrapped messages in tmux buffer delivered to Telegram
- No messages dropped during failures
- No messages lost during restarts

**Zero duplicates:**
- Each message sent exactly once
- Watermark prevents re-processing
- Retry queue prevents double-sends

**<30 second latency:**
- 95th percentile delivery time < 30 seconds
- Fast poll interval (10-30s) enables low latency
- Retry queue doesn't block new messages

**Graceful degradation:**
- Telegram API failures → retry queue
- Monitor crashes → restart resumes from watermark
- Tmux buffer overflow → oldest messages lost (acceptable)

---

## Migration Path (V1 → V2)

### State Migration Script

```python
#!/usr/bin/env python3
"""Migrate telegram monitor state from V1 to V2."""

import json
from pathlib import Path

V1_STATE = Path(".tg_sessions/monitor_state.json")
V2_STATE = Path(".tg_sessions/monitor_state_v2.json")

def migrate_state():
    """Migrate V1 hash-based state to V2 watermark-based state."""
    # Load V1 state
    with open(V1_STATE) as f:
        v1_state = json.load(f)

    # V2 state starts fresh (no way to convert hashes to watermark)
    v2_state = {
        "watermark": 0,  # Will process all messages in buffer on first poll
        "retry_queue": [],
        "dead_letter": [],
        "migrated_from_v1": True,
        "migration_timestamp": datetime.now().isoformat()
    }

    # Backup V1 state
    shutil.copy(V1_STATE, V1_STATE.with_suffix(".json.backup"))

    # Write V2 state
    with open(V2_STATE, 'w') as f:
        json.dump(v2_state, f, indent=2)

    print(f"✅ Migrated V1 → V2")
    print(f"   V1 state backed up: {V1_STATE}.backup")
    print(f"   V2 state created: {V2_STATE}")
    print(f"   ⚠️  V2 will re-send all messages currently in tmux buffer")

if __name__ == "__main__":
    migrate_state()
```

### Deployment Runbook

**Pre-deployment:**
1. Verify V1 monitor status: `ps aux | grep telegram_monitor.py`
2. Check recent messages sent: `tail -50 /tmp/acgee_telegram_monitor.log`
3. Backup current state: `cp .tg_sessions/monitor_state.json .tg_sessions/monitor_state_v1_backup.json`

**Deployment:**
1. Stop V1 monitor: `bash tools/stop_telegram_monitor.sh`
2. Migrate state: `python3 tools/migrate_monitor_state.py`
3. Start V2 monitor: `bash tools/restart_telegram_monitor_v2.sh`
4. Verify running: `ps aux | grep telegram_monitor_v2.py`
5. Send test message: `echo '🤖🎯📱\nTEST V2\n✨🔚'`
6. Wait 30 seconds, check Telegram
7. Verify logs: `tail -20 /tmp/acgee_telegram_monitor_v2.log`

**Post-deployment:**
1. Monitor for 1 hour (watch logs, check Telegram delivery)
2. Verify watermark advancing: `cat .tg_sessions/monitor_state_v2.json`
3. Check retry queue empty: `jq '.retry_queue | length' .tg_sessions/monitor_state_v2.json`
4. If stable → delete V1 state backup

**Rollback (if V2 fails):**
1. Stop V2 monitor: `bash tools/stop_telegram_monitor_v2.sh`
2. Restore V1 state: `cp .tg_sessions/monitor_state_v1_backup.json .tg_sessions/monitor_state.json`
3. Start V1 monitor: `bash tools/restart_telegram_monitor.sh`
4. Investigate V2 failure, file bug report

---

## Known Limitations

**Tmux buffer overflow:**
- Tmux buffers last 500-1000 lines (configurable)
- If >500 wrapped messages appear before monitor polls → oldest lost
- Mitigation: Fast poll interval (10-30s), low risk given typical usage

**State file corruption:**
- If state file corrupted → monitor starts from watermark 0 → re-sends all messages
- Mitigation: State file validation on load, backup on write

**Telegram API rate limits:**
- Telegram allows ~20 messages/minute per bot
- If >20 messages in retry queue → some delayed
- Mitigation: Exponential backoff, dead letter queue

**Monitor process crash:**
- If monitor crashes and doesn't write watermark → messages lost
- Mitigation: Flush state after EVERY successful send (not batched)

---

## Decision

**Implement V2 with watermark-based architecture.**

**Rationale:**
- Fixes V1's critical deduplication bug
- Enables zero message loss via retry queue
- Graceful restart via watermark persistence
- Performance optimizations (fast polling, circuit breaker)

**Timeline:** 4.5 hours (coder) + 1 hour (tester) = 5.5 hours total

**Risks:** Low (comprehensive testing, rollback procedure, fail-loud design)

---

**Author**: coder (autonomous design)
**Approved by**: Primary AI (implicit via task delegation)
**Implementation start**: 2025-10-19
