#!/bin/bash
# BOOP Status Dashboard for Sage
# Shows current BOOP system health and status

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMUX_SESSION="sage-session"
PROMPTS_DIR="/mnt/c/sage/sage-civilization/autonomous-session/prompts"
STATE_FILE="$SCRIPT_DIR/injection_state.txt"
LOG_FILE="$SCRIPT_DIR/injection_log.txt"
PAUSE_FILE="$SCRIPT_DIR/PAUSE"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║           BOOP Status Dashboard - Sage Civilization            ║"
echo "╠════════════════════════════════════════════════════════════════╣"
echo ""

# System Status
echo "System Status:"
echo "─────────────────────────────────────────────────────────────────"

# Check tmux session
if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    echo "  tmux session ($TMUX_SESSION):     RUNNING ✅"
else
    echo "  tmux session ($TMUX_SESSION):     NOT FOUND ❌"
fi

# Check cron job
if crontab -l 2>/dev/null | grep -q "inject_prompt.sh"; then
    CRON_LINE=$(crontab -l 2>/dev/null | grep "inject_prompt.sh")
    echo "  Cron job:                          INSTALLED ✅"
    echo "    Schedule: $(echo "$CRON_LINE" | awk '{print $1, $2, $3, $4, $5}')"
else
    echo "  Cron job:                          NOT INSTALLED ⏸️"
fi

# Check pause status
if [ -f "$PAUSE_FILE" ]; then
    echo "  PAUSE flag:                        ACTIVE ⏸️ (BOOP paused)"
else
    echo "  PAUSE flag:                        OFF ✅ (BOOP running)"
fi

echo ""

# Current State
echo "Current Injection State:"
echo "─────────────────────────────────────────────────────────────────"

if [ -f "$STATE_FILE" ]; then
    CURRENT=$(cat "$STATE_FILE")
    echo "  Current state counter:             $CURRENT"
else
    echo "  Current state counter:             NOT INITIALIZED ⚠️"
    CURRENT="?"
fi

# Available prompts
PROMPT_FILES=($(ls -1 "$PROMPTS_DIR"/*.txt 2>/dev/null | sort))
TOTAL_PROMPTS=${#PROMPT_FILES[@]}

echo "  Total prompts available:           $TOTAL_PROMPTS"

if [ "$CURRENT" != "?" ]; then
    PROMPT_INDEX=$((($CURRENT - 1) % $TOTAL_PROMPTS))
    CURRENT_PROMPT=$(basename "${PROMPT_FILES[$PROMPT_INDEX]}" .txt)
    NEXT_INDEX=$(( ($CURRENT % $TOTAL_PROMPTS) ))
    NEXT_PROMPT=$(basename "${PROMPT_FILES[$NEXT_INDEX]}" .txt)

    echo "  Current prompt:                    #$CURRENT: $CURRENT_PROMPT"
    echo "  Next prompt:                       #$((CURRENT+1)): $NEXT_PROMPT"
fi

echo ""

# Recent Activity
echo "Recent Activity:"
echo "─────────────────────────────────────────────────────────────────"

if [ -f "$LOG_FILE" ]; then
    echo "  Last 5 injections:"
    tail -5 "$LOG_FILE" | sed 's/^/    /'
    echo ""
    echo "  Total injections logged:           $(grep -c "INJECTED:" "$LOG_FILE") successful"
    echo "  Total skips (rate limit):          $(grep -c "SKIPPED:" "$LOG_FILE")"
    echo "  Total errors:                      $(grep -c "ERROR:" "$LOG_FILE")"
else
    echo "  No injection log found yet"
fi

echo ""

# Available Prompts
echo "Available Prompts:"
echo "─────────────────────────────────────────────────────────────────"

for i in "${!PROMPT_FILES[@]}"; do
    name=$(basename "${PROMPT_FILES[$i]}" .txt)
    if [ $((i+1)) -eq "$CURRENT" ] 2>/dev/null; then
        marker=" ← CURRENT"
    else
        marker=""
    fi
    printf "  %2d. %-35s%s\n" $((i+1)) "$name" "$marker"
done

echo ""

# Quick Commands
echo "Quick Commands:"
echo "─────────────────────────────────────────────────────────────────"
echo "  View full injection log:           tail -f $LOG_FILE"
echo "  Manual test injection:             bash $SCRIPT_DIR/test_boop_injection.sh"
echo "  Install cron job:                  bash $SCRIPT_DIR/install_cron.sh"
echo "  Pause BOOP:                        touch $PAUSE_FILE"
echo "  Resume BOOP:                       rm $PAUSE_FILE"
echo "  Check tmux session:                tmux attach -t $TMUX_SESSION"
echo ""

echo "╚════════════════════════════════════════════════════════════════╝"
