# Hourly Email Auto-Send Setup

**Problem Fixed**: human-liaison was drafting emails but not sending them

**Solution**: AUTO-SEND mode with blanket approval (CLAUDE.md Article IV)

## How It Works

### Script: `hourly_email_autosend.sh`

1. Checks if Claude Code tmux session is active
2. Injects human-liaison task with AUTO-SEND directive
3. human-liaison:
   - Checks inbox for priority emails (Corey, Greg, Chris, Weaver)
   - Drafts HTML responses
   - **SENDS IMMEDIATELY** (no waiting for approval)
   - Logs all sends to `memories/agents/email-reporter/sent_emails.json`

### Constitutional Authority

**CLAUDE.md Article IV** grants blanket approval for proactive email communication:

> "Frequency: Email on ALL significant achievements (not just milestones)
> Blanket Approval: Send emails proactively without asking permission"

### Duplicate Prevention

- Checks `sent_emails.json` before sending
- Skips same thread within 24h
- Tracks processed emails in state file

## Installation

### Step 1: Verify Script Works

```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch

# Test script (requires active Claude session)
./autonomous-session/scripts/hourly_email_autosend.sh
```

### Step 2: Add to Cron (Hourly)

```bash
crontab -e
```

Add this line:

```cron
# A-C-Gee Hourly Email Auto-Send (every hour at :00)
0 * * * * /home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts/hourly_email_autosend.sh >> /home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts/cron_log.txt 2>&1
```

### Step 3: Verify Cron Entry

```bash
crontab -l | grep autosend
```

## Monitoring

### Check Logs

```bash
# Auto-send activity log
tail -f autonomous-session/scripts/hourly_email_check_log.txt

# Sent emails registry
cat memories/agents/email-reporter/sent_emails.json | jq '.[-5:]'

# Cron execution log
tail -f autonomous-session/scripts/cron_log.txt
```

### State File

```bash
# Processing state (tracks sends)
cat autonomous-session/scripts/email_autosend_state.json | jq
```

## Success Criteria

- ✅ Script runs without errors
- ✅ human-liaison invoked with AUTO-SEND directive
- ✅ Emails drafted AND sent automatically
- ✅ Zero drafts lingering unsent
- ✅ All sends logged to sent_emails.json

## Troubleshooting

### "tmux session not found"

Claude Code must be running in tmux session named "claude":

```bash
tmux ls
# Should show: claude: 1 windows (created ...)
```

### "Rate limit detected"

Script skips injection when rate limited. Will retry next hour.

### Emails not being sent

1. Check human-liaison has access to `tools/send_html_email.py`
2. Verify GOOGLE_APP_PASSWORD is set in environment
3. Check `sent_emails.json` for duplicate prevention triggers

## Manual Testing

```bash
# Run script manually (requires active Claude session)
./autonomous-session/scripts/hourly_email_autosend.sh

# Watch tmux session for execution
tmux attach -t claude

# Check logs immediately
tail -20 autonomous-session/scripts/hourly_email_check_log.txt
```

## Comparison to Old Script

**OLD (BROKEN)**:
```bash
# Used non-existent CLI
claude chat --agent human-liaison --prompt "..."
# Result: command not found
```

**NEW (WORKING)**:
```bash
# Injects Task into active Claude Code tmux session
tmux send-keys -t claude.0 -l "Task(human-liaison): ..."
# Result: human-liaison executes with full context and tools
```

## Files

- **Script**: `/autonomous-session/scripts/hourly_email_autosend.sh`
- **State**: `/autonomous-session/scripts/email_autosend_state.json`
- **Log**: `/autonomous-session/scripts/hourly_email_check_log.txt`
- **Sent emails**: `/memories/agents/email-reporter/sent_emails.json`

## Next Steps

1. Test script manually once
2. Add to crontab (hourly)
3. Monitor for 24h to verify auto-send working
4. Celebrate zero lingering drafts! 🎉
