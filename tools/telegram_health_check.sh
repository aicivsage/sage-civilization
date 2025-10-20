#!/bin/bash
# A-C-Gee Telegram Infrastructure Health Check & Auto-Recovery
# Run this via cron every 5 minutes: */5 * * * * /path/to/telegram_health_check.sh

PROJECT_ROOT="/home/corey/projects/AI-CIV/grow_gemini_deepresearch"
LOG_FILE="/tmp/acgee_telegram_health_check.log"
BRIDGE_LOG="/tmp/acgee_telegram_bridge.log"
MONITOR_LOG="/tmp/acgee_telegram_monitor.log"
PID_FILE="$PROJECT_ROOT/.tg_sessions/acgee_monitor.pid"

echo "[$(date)] === A-C-Gee Telegram Health Check ===" >> "$LOG_FILE"

# Check if telegram_bridge.py is running (civilization-specific)
BRIDGE_PID=$(pgrep -f "grow_gemini_deepresearch/tools/telegram_bridge.py")
if [ -z "$BRIDGE_PID" ]; then
    echo "[$(date)] ❌ A-C-Gee telegram_bridge.py NOT running - restarting..." >> "$LOG_FILE"
    cd "$PROJECT_ROOT"
    nohup python3 tools/telegram_bridge.py >> "$BRIDGE_LOG" 2>&1 &
    echo "[$(date)] ✅ A-C-Gee telegram_bridge.py restarted (PID: $!)" >> "$LOG_FILE"
else
    echo "[$(date)] ✅ A-C-Gee telegram_bridge.py running (PID: $BRIDGE_PID)" >> "$LOG_FILE"

    # Check if it's responsive (last log entry within 120 seconds)
    if [ -f "$BRIDGE_LOG" ]; then
        LAST_LOG=$(tail -1 "$BRIDGE_LOG" | grep -oP '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
        if [ -n "$LAST_LOG" ]; then
            LAST_TIMESTAMP=$(date -d "$LAST_LOG" +%s 2>/dev/null || echo 0)
            NOW=$(date +%s)
            AGE=$((NOW - LAST_TIMESTAMP))

            if [ $AGE -gt 120 ]; then
                echo "[$(date)] ⚠️  A-C-Gee telegram_bridge.py unresponsive (last log ${AGE}s ago) - restarting..." >> "$LOG_FILE"
                kill $BRIDGE_PID
                sleep 2
                cd "$PROJECT_ROOT"
                nohup python3 tools/telegram_bridge.py >> "$BRIDGE_LOG" 2>&1 &
                echo "[$(date)] ✅ A-C-Gee telegram_bridge.py restarted (PID: $!)" >> "$LOG_FILE"
            fi
        fi
    fi
fi

# Check if telegram_monitor.py is running (use PID file for civilization-specific check)
if [ -f "$PID_FILE" ]; then
    MONITOR_PID=$(cat "$PID_FILE")
    # Verify process is actually running
    if ! ps -p "$MONITOR_PID" > /dev/null 2>&1; then
        echo "[$(date)] ❌ A-C-Gee telegram_monitor.py PID $MONITOR_PID not running - restarting..." >> "$LOG_FILE"
        rm -f "$PID_FILE"
        cd "$PROJECT_ROOT"
        nohup python3 tools/telegram_monitor.py --interval 30 >> "$MONITOR_LOG" 2>&1 &
        echo "[$(date)] ✅ A-C-Gee telegram_monitor.py restarted (PID: $!)" >> "$LOG_FILE"
    else
        echo "[$(date)] ✅ A-C-Gee telegram_monitor.py running (PID: $MONITOR_PID)" >> "$LOG_FILE"

        # Check if it's responsive
        if [ -f "$MONITOR_LOG" ]; then
            LAST_LOG=$(tail -1 "$MONITOR_LOG" | grep -oP '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
            if [ -n "$LAST_LOG" ]; then
                LAST_TIMESTAMP=$(date -d "$LAST_LOG" +%s 2>/dev/null || echo 0)
                NOW=$(date +%s)
                AGE=$((NOW - LAST_TIMESTAMP))

                if [ $AGE -gt 120 ]; then
                    echo "[$(date)] ⚠️  A-C-Gee telegram_monitor.py unresponsive (last log ${AGE}s ago) - restarting..." >> "$LOG_FILE"
                    kill $MONITOR_PID
                    rm -f "$PID_FILE"
                    sleep 2
                    cd "$PROJECT_ROOT"
                    nohup python3 tools/telegram_monitor.py --interval 30 >> "$MONITOR_LOG" 2>&1 &
                    echo "[$(date)] ✅ A-C-Gee telegram_monitor.py restarted (PID: $!)" >> "$LOG_FILE"
                fi
            fi
        fi
    fi
else
    # No PID file - check if process is running anyway (fallback)
    MONITOR_PID=$(pgrep -f "grow_gemini_deepresearch/tools/telegram_monitor.py")
    if [ -z "$MONITOR_PID" ]; then
        echo "[$(date)] ❌ A-C-Gee telegram_monitor.py NOT running (no PID file) - restarting..." >> "$LOG_FILE"
        cd "$PROJECT_ROOT"
        nohup python3 tools/telegram_monitor.py --interval 30 >> "$MONITOR_LOG" 2>&1 &
        echo "[$(date)] ✅ A-C-Gee telegram_monitor.py restarted (PID: $!)" >> "$LOG_FILE"
    else
        echo "[$(date)] ✅ A-C-Gee telegram_monitor.py running (PID: $MONITOR_PID, no PID file - will be created)" >> "$LOG_FILE"
    fi
fi

echo "[$(date)] === A-C-Gee Health Check Complete ===" >> "$LOG_FILE"
