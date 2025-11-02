# Sage Civilization - Cron Job Setup Guide

**Purpose:** Automated end-of-day email summaries sent to Greg at 6pm ET daily.

---

## Overview

The end-of-day email automation uses a cron job to trigger `send_end_of_day_email.py` at 6pm Eastern Time every day. This ensures Greg receives consistent daily summaries without manual intervention.

**Key Components:**
- **Email Script:** `tools/send_end_of_day_email.py` (generates and sends email)
- **Cron Wrapper:** `tools/cron_end_of_day.sh` (handles environment, logging, errors)
- **Log File:** `memories/system/cron_logs/end_of_day.log` (execution history)

---

## Installation

### Step 1: Verify Scripts Exist

```bash
cd /mnt/c/sage/sage-civilization

# Check email script
ls -l tools/send_end_of_day_email.py

# Check cron wrapper
ls -l tools/cron_end_of_day.sh

# Ensure wrapper is executable
chmod +x tools/cron_end_of_day.sh
```

### Step 2: Test Script Manually

```bash
# Dry run (no email sent, validates everything works)
python3 tools/send_end_of_day_email.py --dry-run

# Full test (actually sends email - use sparingly!)
python3 tools/send_end_of_day_email.py --force
```

### Step 3: Add Cron Job

Open crontab editor:
```bash
crontab -e
```

Add this line (runs at 6pm ET every day):
```cron
0 18 * * * cd /mnt/c/sage/sage-civilization && TZ=America/New_York bash tools/cron_end_of_day.sh
```

**Cron Syntax Explanation:**
- `0 18 * * *` = At minute 0, hour 18 (6pm), every day of month, every month, every day of week
- `TZ=America/New_York` = Sets Eastern Time (handles DST automatically)
- `cd /mnt/c/sage/sage-civilization` = Changes to project directory first
- `bash tools/cron_end_of_day.sh` = Runs the wrapper script

### Step 4: Verify Cron Job Installed

```bash
# List all cron jobs for current user
crontab -l

# You should see the line added in Step 3
```

---

## Timezone Handling

**Critical:** The script MUST run in Eastern Time (America/New_York) to ensure 6pm ET delivery regardless of system timezone or Daylight Saving Time changes.

**Methods used:**
1. **Cron entry:** `TZ=America/New_York` environment variable
2. **Wrapper script:** `export TZ=America/New_York` (redundant safety)
3. **Python script:** Uses system timezone after TZ is set

**DST handling:** Automatic via `America/New_York` timezone (switches between EST/EDT automatically)

---

## Monitoring and Troubleshooting

### Check Execution Logs

```bash
# View recent log entries
tail -50 memories/system/cron_logs/end_of_day.log

# Monitor live (if testing around 6pm)
tail -f memories/system/cron_logs/end_of_day.log

# Check for errors
grep ERROR memories/system/cron_logs/end_of_day.log
```

### Verify Last Run

```bash
# Check log file modification time
ls -lh memories/system/cron_logs/end_of_day.log

# Check state file (updated by email script)
cat memories/system/email_schedule_state.json | grep last_end_of_day_email
```

### Common Issues

**Problem:** Cron job not running
- **Check:** `crontab -l` (is entry present?)
- **Check:** Cron service running: `systemctl status cron` (Linux) or `sudo launchctl list | grep cron` (macOS)
- **Fix:** Restart cron service if needed

**Problem:** Email not sending
- **Check:** Log file for errors: `grep ERROR memories/system/cron_logs/end_of_day.log`
- **Check:** Email script runs manually: `python3 tools/send_end_of_day_email.py --force`
- **Check:** Email credentials in `config/email_config.json`

**Problem:** Wrong timezone
- **Check:** Log timestamps: `tail memories/system/cron_logs/end_of_day.log`
- **Verify:** TZ variable in cron entry and wrapper script
- **Fix:** Ensure both use `TZ=America/New_York`

**Problem:** Permission errors
- **Check:** Script executable: `ls -l tools/cron_end_of_day.sh`
- **Fix:** `chmod +x tools/cron_end_of_day.sh`

---

## Testing the Cron Job

### Method 1: Temporary Test Entry (Recommended)

Edit crontab and add a test entry that runs in 2 minutes:

```bash
crontab -e

# Add this line (replace HH:MM with current time + 2 minutes)
MM HH * * * cd /mnt/c/sage/sage-civilization && TZ=America/New_York bash tools/cron_end_of_day.sh
```

Example: If it's currently 3:47pm, use `49 15 * * *`

Wait 2 minutes, then check log:
```bash
tail -20 memories/system/cron_logs/end_of_day.log
```

Remove test entry after verification:
```bash
crontab -e
# Delete the test line
```

### Method 2: Manual Wrapper Execution

```bash
# Run the wrapper script directly (tests everything except cron scheduling)
bash tools/cron_end_of_day.sh

# Check log file
tail -20 memories/system/cron_logs/end_of_day.log
```

---

## Maintenance

### Update Cron Schedule

To change timing (e.g., 5pm instead of 6pm):
```bash
crontab -e
# Change: 0 18 * * *  (6pm)
# To:     0 17 * * *  (5pm)
```

### Disable Temporarily

```bash
crontab -e
# Comment out the line by adding # at start:
# 0 18 * * * cd /mnt/c/sage/sage-civilization && TZ=America/New_York bash tools/cron_end_of_day.sh
```

### Remove Completely

```bash
crontab -e
# Delete the entire line
```

### Rotate Log Files

If log file grows too large (>10MB):
```bash
# Archive old log
mv memories/system/cron_logs/end_of_day.log memories/system/cron_logs/end_of_day.log.$(date +%Y%m%d)

# Compress archive
gzip memories/system/cron_logs/end_of_day.log.*

# Log will be recreated automatically on next run
```

---

## Integration with Other Email Automation

**Related Scripts:**
- `tools/send_day_start_email.py` - Morning email (triggered manually in wake-up protocol)
- `tools/send_major_accomplishment_email.py` - Achievement alerts (triggered by Primary during work)
- `tools/send_end_of_day_email.py` - This script (automated via cron)

**State Tracking:**
- All three scripts share `memories/system/email_schedule_state.json`
- Prevents duplicate sends (e.g., day start email sent only once per day)
- Cron script respects state file (won't send if already sent manually)

**Testing All Scripts:**
```bash
# Test suite (validates all email automation)
bash tools/test_email_automation.sh
```

---

## Reference

**Cron Time Examples:**
```
0 9 * * *     # 9am daily
0 18 * * *    # 6pm daily (current setting)
0 12 * * 1-5  # Noon, Monday-Friday only
*/30 9-17 * * * # Every 30 min, 9am-5pm
```

**Cron Environment Notes:**
- Cron jobs run with minimal environment (no shell initialization)
- Always use absolute paths or cd to project directory first
- Set timezone explicitly (don't rely on system default)
- Redirect output to log files (cron emails are unreliable)

**Documentation:**
- Main automation doc: `memories/agents/email-reporter/EMAIL_AUTOMATION_COMPLETE.md`
- Wake-up protocol: `.claude/CLAUDE.md` (Article III: Operational Principles)
- Email templates: `templates/email_*.html`

---

## Quick Reference

```bash
# Install cron job
crontab -e
# Add: 0 18 * * * cd /mnt/c/sage/sage-civilization && TZ=America/New_York bash tools/cron_end_of_day.sh

# Check if running
crontab -l | grep end_of_day

# View logs
tail -50 memories/system/cron_logs/end_of_day.log

# Test manually
bash tools/cron_end_of_day.sh

# Test email script
python3 tools/send_end_of_day_email.py --dry-run
```

---

**Maintained by:** Sage Civilization Infrastructure Team
**Last Updated:** 2025-11-01
**Related Docs:** `EMAIL_AUTOMATION_COMPLETE.md`, `CLAUDE.md` (Wake-Up Protocol)
