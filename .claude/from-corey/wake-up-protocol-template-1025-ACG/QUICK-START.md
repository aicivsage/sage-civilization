# Quick Start - Wake-Up Protocol V2.1

**For Primary AI starting a new session**

---

## The 7 Steps (5-10 minutes)

### 1. Boot Telegram FIRST ⚡
```bash
# Invoke tg-archi for instructions
Task(tg-archi): "Provide Telegram boot instructions"

# Execute what they say, then verify with PROOF
# Send session start message
```

### 2. Run Wake-Up Script 📊
```bash
./tools/session_wakeup.sh
```
Shows: Recent handoff, status files, git commits, Telegram status

### 3. Load Context 📖
Read in order:
1. CLAUDE.md (identity + protocols)
2. Most recent handoff (from registry)
3. Status files (if shown)

### 4. Check Communications 📬
```bash
# Parallel invocation
Task(human-liaison) + Task(comms-hub)
```

### 5. Verify Comprehension ✅
```bash
Task(primary-helper):
  Mode: wakeup
  Context: [brief summary]
  Request: Verify comprehension
```

### 6. Confirm Ready 📱
```bash
tg_context_loaded "[handoff]" "[priority]"
```

### 7. Begin Work 🚀
Armed with: Identity + Context + Communications + Verification

---

## End of Session

### 1. Write Handoff 📝
```bash
vim SESSION-HANDOFF-YYYYMMDD-HHMM-TOPIC.md
```

### 2. Update Registry 📌
```bash
./tools/update_handoff_registry.sh SESSION-HANDOFF-*.md
```

### 3. Send Summary 📱
```bash
tg_session_complete "[duration]" "[achievements]"
```

---

## Emergency Shortcuts

### If Telegram Down
Skip Steps 1 and 6, proceed with 2-5-7

### If Time Critical
Minimum: Steps 2, 3 (handoff only), 7

### If Context Missing
Run `find . -name "*HANDOFF*.md" -mtime -1` to find recent work

---

## Success Checklist

Before starting work, verify:
- [ ] Telegram operational (or skipped with reason)
- [ ] Recent handoff read (< 24 hours old preferred)
- [ ] Communications checked (human-liaison + comms-hub)
- [ ] Comprehension verified (primary-helper answered)
- [ ] User notified (Telegram or equivalent)

---

## Tools Reference

```bash
# Wake-up
./tools/session_wakeup.sh                 # Context scanner

# Telegram
./tools/acg_telegram_boot.sh              # Boot system
source tools/telegram_templates.sh        # Load helpers
tg_session_start                          # "I'm alive"
tg_context_loaded "[h]" "[p]"            # "Ready"
tg_session_complete "[d]" "[a]"          # "Done"

# Registry
./tools/update_handoff_registry.sh [file] # Update pointer
cat memories/system/HANDOFF_REGISTRY.json # Check current
```

---

**Duration Target**: 5-10 minutes
**Quality Gate**: primary-helper verification
**User Visibility**: Telegram throughout

**FOR US ALL. 🤖**
