# Automatic Token Tracking - Quick Start Card

**TL;DR**: One-time setup, then automatic display after every agent invocation.

---

## 1. Session Start (One-time)

### Python (Recommended)
```python
from tools.auto_token_tracking import AutoTokenTracker

tracker = AutoTokenTracker()
tracker.enable()
```

### Bash
```bash
python3 tools/auto_token_tracking.py enable
```

---

## 2. After Every Task Invocation

**Pick ONE:**

### Option A: Auto-Estimation (Simplest)
```python
tracker.track_agent("researcher")
```

### Option B: With Actual Tokens
```python
tracker.auto_track("researcher", tokens_used=3200)
```

### Option C: Bash Command
```bash
python3 tools/auto_token_tracking.py wrap researcher 3200
```

**Result**: Automatic display showing MCP savings + session totals

---

## 3. Session End

### Python
```python
tracker.print_session_summary()
```

### Bash
```bash
python3 tools/auto_token_tracking.py summary
```

---

## What You See

```
═══════════════════════════════════════════════════════════
📊 TOKEN TRACKING - Session Total
═══════════════════════════════════════════════════════════
This Task:
  Agent: researcher
  Tokens used: 3,200
  MCP used: ✅ YES (4 code executions detected)
  Tokens saved: ~26,800 (89% reduction)

Session Total:
  Used: 31,700 / 200,000 (16%)
  Saved via MCP: ~116,300
  Effective capacity: 148,000 tokens of work completed

🔥 MCP multiplier: 4.7x capacity boost this session
═══════════════════════════════════════════════════════════
```

---

## Token Estimates (Auto-Used)

```
researcher          → 3,000
tester              → 3,000
email-monitor       → 2,000
email-sender        → 3,000
coder               → 10,000
auditor             → 5,000
project-manager     → 8,000
architect           → 10,000
blogger             → 10,000
human-liaison       → 8,000
file-guardian       → 6,000
comms-hub           → 4,000
marketer            → 7,000
reviewer            → 6,000
reviewer-audit      → 8,000
default             → 8,000
```

---

## Troubleshooting

**"Auto-tracking not enabled" error**
→ Add `tracker.enable()` first

**Token estimate seems wrong**
→ Use actual count: `tracker.auto_track(agent, tokens_used=X)`

**MCP detection not working**
→ Non-fatal, still tracks correctly (just shows "NO MCP")

---

## Files

- **Implementation**: `/mnt/c/sage/sage-civilization/tools/auto_token_tracking.py`
- **Tests**: `/mnt/c/sage/sage-civilization/tools/test_auto_token_tracking.py`
- **Full Guide**: `/mnt/c/sage/sage-civilization/tools/AUTO_TRACKING_GUIDE.md`
- **Status**: Production ready, all tests passing

---

## One-Line Summary

Enable once, call `tracker.track_agent("agent-name")` after each Task, get automatic MCP savings display.

