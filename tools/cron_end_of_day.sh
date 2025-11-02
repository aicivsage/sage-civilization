#!/bin/bash

# Sage Civilization - End of Day Email Cron Wrapper
# Runs at 6pm ET daily via cron
# Sends automated summary email to Greg

# Exit on error
set -e

# Set timezone to Eastern Time (handles DST automatically)
export TZ=America/New_York

# Project root (assuming script is in tools/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Log directory
LOG_DIR="$PROJECT_ROOT/memories/system/cron_logs"
LOG_FILE="$LOG_DIR/end_of_day.log"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Function to log with timestamp
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] $1" >> "$LOG_FILE"
}

# Start logging
log_message "=== End of Day Email Cron Job Started ==="

# Change to project directory (required for relative paths in Python script)
cd "$PROJECT_ROOT"

# Verify Python script exists
if [ ! -f "tools/send_end_of_day_email.py" ]; then
    log_message "ERROR: send_end_of_day_email.py not found"
    exit 1
fi

# Run the email script
log_message "Executing send_end_of_day_email.py..."
if python3 tools/send_end_of_day_email.py >> "$LOG_FILE" 2>&1; then
    log_message "SUCCESS: End of day email sent successfully"
    EXIT_CODE=0
else
    EXIT_CODE=$?
    log_message "ERROR: Email script failed with exit code $EXIT_CODE"
fi

log_message "=== End of Day Email Cron Job Complete ==="
log_message ""

exit $EXIT_CODE
