#!/bin/bash
# Hourly Communications Check - Cron Job
# Injects a prompt to check inbox and Weaver messages every hour
# Created: 2025-10-20
#
# To install as cron job:
#   crontab -e
#   Add line: 0 * * * * /home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/hourly_comms_check.sh

# Change to project directory
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch || exit 1

# Log the check
echo "[$(date)] Hourly comms check triggered" >> /tmp/acgee_hourly_comms.log

# Inject the prompt
bash tools/inject_prompt_to_acg.sh "Hourly comms check: Task(human-liaison) to check inbox + Task(comms-hub) to check Weaver messages. Respond to anything urgent. Send me a wrapped status update if there's anything important." >> /tmp/acgee_hourly_comms.log 2>&1

echo "[$(date)] Prompt injected" >> /tmp/acgee_hourly_comms.log
