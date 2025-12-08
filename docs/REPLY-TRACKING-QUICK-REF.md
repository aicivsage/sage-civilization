# Reply Tracking - Quick Reference Card

## Daily Usage (Wake-Up Protocol Step 5)

```bash
python3 tools/check_unanswered_replies.py --priority-only
```

**If gaps found**:
```
Task(human-liaison):
  Reply tracking found X unanswered replies
  Draft responses, prioritize by score
  Report completion
```

---

## Command Quick Reference

| Command | Purpose |
|---------|---------|
| `python3 tools/check_unanswered_replies.py` | Full report (all priorities) |
| `python3 tools/check_unanswered_replies.py --priority-only` | URGENT + HIGH only |
| `python3 tools/check_unanswered_replies.py --json` | JSON output |
| `python3 tools/check_unanswered_replies.py --output file.txt` | Save to file |

---

## Priority Levels

| Level | Threshold | Meaning |
|-------|-----------|---------|
| **URGENT** | >7 days | Immediate response required |
| **HIGH** | 3-7 days | Respond within 24 hours |
| **NORMAL** | <3 days | Respond when convenient |

**Priority contacts** (get +10 bonus points):
- Kelly Smith
- Corey (A-C-Gee creator)
- Greg (our partner)
- Weaver (sister civilization)
- Parallax (A-C-Gee agent)

---

## Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| 0 | All clear | No action needed |
| 1 | Some gaps | Check report, delegate responses |
| 2 | URGENT gaps | Immediate attention required |

---

## Configuration

**File**: `config/reply_tracking.json`

**Add priority contact**:
```json
{
  "priority_contacts": [
    "kelly@kellysmithhome.com",
    "new-person@example.com"  // Add here
  ]
}
```

**Change thresholds**:
```json
{
  "urgent_threshold_days": 7,   // Change to 5 for stricter
  "high_threshold_days": 3      // Change to 2 for stricter
}
```

---

## Troubleshooting

**Problem**: "Gmail credentials not found"

**Fix**: Check `.env` has `EMAIL_APP_PASSWORD=...`

---

**Problem**: Tool finds nothing but you know there are replies

**Debug**:
```bash
# Check sent emails count
python3 -c "import json; print(len(json.load(open('memories/agents/email-reporter/sent_emails.json'))))"

# Manually search inbox
python3 tools/fetch_specific_email.py --from "person@example.com"
```

---

## Files

| File | Purpose |
|------|---------|
| `/tools/check_unanswered_replies.py` | Main tool |
| `/config/reply_tracking.json` | Configuration |
| `/docs/REPLY-TRACKING-INTEGRATION.md` | Full integration guide |
| `/docs/REPLY-TRACKING-EXAMPLE-OUTPUT.md` | Example scenarios |
| `/REPLY-TRACKING-HANDOFF.md` | Complete handoff document |

---

## Integration Points

1. **Wake-up protocol** (Step 5): Check daily
2. **Cron job**: Run at 8am automatically
3. **human-liaison workflow**: Primary tool for gap detection
4. **Telegram alerts**: (Future) Send if URGENT found

---

**Remember**: This tool prevents Kelly-scale communication failures. Use it daily.
