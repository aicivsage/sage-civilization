#!/bin/bash
# Hourly Email Auto-Send Script
# Injects human-liaison AUTO-SEND task into active Claude Code tmux session
# Constitutional authority: CLAUDE.md Article IV (blanket email approval)

# Configuration
TMUX_SESSION="claude"
TMUX_PANE="claude.0"
STATE_FILE="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts/email_autosend_state.json"
LOG_FILE="/home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts/hourly_email_check_log.txt"

# Timestamp function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "======================================"
log "HOURLY EMAIL AUTO-SEND CHECK"
log "======================================"

# Check if tmux session exists
if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    log "ERROR: tmux session '$TMUX_SESSION' not found"
    log "Auto-send requires active Claude Code session"
    exit 1
fi

# Check for rate limit (basic check)
RECENT_OUTPUT=$(tmux capture-pane -t "$TMUX_PANE" -p | tail -5)
if echo "$RECENT_OUTPUT" | grep -qi "rate limit"; then
    log "SKIPPED: Rate limit detected, waiting for next cycle"
    exit 0
fi

# Initialize state file if needed
if [ ! -f "$STATE_FILE" ]; then
    echo '{"last_check": null, "total_sends": 0, "processed_emails": []}' > "$STATE_FILE"
fi

# Build AUTO-SEND task prompt
read -r -d '' TASK_PROMPT << 'EOF'
Task(human-liaison):

**AUTONOMOUS MODE - AUTO-SEND ENABLED**
Constitutional authority: CLAUDE.md Article IV (blanket email approval)

Your task:

1. Check inbox for new messages (HIGH/MEDIUM priority: Corey, Greg, Chris, Weaver)
2. For each priority email:
   - Draft HTML response (templates/email_template.html)
   - SEND IMMEDIATELY via tools/send_html_email.py (NO approval needed)
   - Log to memories/agents/email-reporter/sent_emails.json

3. Duplicate prevention:
   - Check sent_emails.json before sending
   - Skip same thread within 24h

4. Return JSON summary:
{
  "emails_checked": N,
  "priority_emails_found": N,
  "emails_sent": N,
  "send_log": ["recipient: subject", ...]
}

Success criteria: All priority emails responded within 1 hour, zero drafts lingering unsent.
EOF

log "Injecting human-liaison AUTO-SEND task into Claude session..."

# Inject the task prompt
tmux send-keys -t "$TMUX_PANE" -l "$TASK_PROMPT"
tmux send-keys -t "$TMUX_PANE" Enter

log "Task injected successfully"
log "human-liaison will check inbox and auto-send responses"
log "======================================"

# Output for manual testing
echo "✅ Auto-send task injected into Claude Code session"
echo "Monitor tmux session: tmux attach -t $TMUX_SESSION"
