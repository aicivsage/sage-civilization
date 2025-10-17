# Email Reporting System - Setup Guide

This guide explains how to configure and use the AI Civilization email reporting system.

## Overview

The `send_mission_report.py` script sends mission completion reports via Gmail SMTP with the following features:

- Secure credential management via `.env` file
- Professional HTML-formatted emails
- Automatic file attachment
- TLS encryption for secure transmission
- Password logging prevention
- Comprehensive error handling

## Prerequisites

1. **Gmail Account**: Access to `weaver.aiciv@gmail.com` (or another Gmail account)
2. **Google App Password**: A 16-character app-specific password (NOT your regular Gmail password)
3. **Python 3.9+**: With standard library (no additional packages required)

## Quick Start

### Step 1: Create App Password

1. Visit [Google App Passwords](https://myaccount.google.com/apppasswords)
2. Sign in to your Gmail account
3. Create a new app password:
   - Select app: "Mail"
   - Select device: "Other (Custom name)"
   - Name it: "AI Civilization Reporter"
4. Copy the 16-character password (format: `xxxx xxxx xxxx xxxx`)

### Step 2: Configure Environment

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```bash
GMAIL_USERNAME=weaver.aiciv@gmail.com
GOOGLE_APP_PASSWORD=your_16_char_app_password_here
```

**Important:**
- Remove spaces from the app password
- Never commit `.env` to version control (it's in `.gitignore`)
- Keep your app password secure

### Step 3: Verify Files

Ensure the mission report file exists:

```bash
ls -l CIVILIZATION_MISSION_COMPLETE.md
```

If it doesn't exist, the script will provide a helpful error message.

### Step 4: Send Report

Run the script:

```bash
python3 send_mission_report.py
```

Or make it executable and run directly:

```bash
chmod +x send_mission_report.py
./send_mission_report.py
```

## Expected Output

### Successful Execution

```
============================================================
AI Civilization Mission Report Email Sender
============================================================

[1/4] Loading credentials from .env file
2025-10-01 19:42:09,244 - __main__ - INFO - Loading environment from: /path/to/.env
2025-10-01 19:42:09,244 - __main__ - INFO - Loaded: GMAIL_USERNAME=weaver.aiciv@gmail.com
2025-10-01 19:42:09,244 - __main__ - INFO - Loaded sensitive key: GOOGLE_APP_PASSWORD
✅ Credentials loaded successfully

[2/4] Configuring email parameters
2025-10-01 19:42:09,245 - __main__ - INFO - SMTP Server: smtp.gmail.com:587
2025-10-01 19:42:09,245 - __main__ - INFO - Recipient: coreycmusic@gmail.com

[3/4] Verifying mission report file
2025-10-01 19:42:09,245 - __main__ - INFO - ✅ Found report: /path/to/CIVILIZATION_MISSION_COMPLETE.md

[4/4] Sending mission report email
2025-10-01 19:42:09,246 - __main__ - INFO - Connecting to SMTP server: smtp.gmail.com:587
2025-10-01 19:42:09,500 - __main__ - INFO - Starting TLS encryption
2025-10-01 19:42:09,750 - __main__ - INFO - Authenticating with SMTP server
2025-10-01 19:42:10,100 - __main__ - INFO - Sending email
2025-10-01 19:42:10,450 - __main__ - INFO - ✅ Email sent successfully!

============================================================
🎉 SUCCESS! Mission report email sent!
============================================================
✅ Sent from: weaver.aiciv@gmail.com
✅ Sent to: coreycmusic@gmail.com
✅ Attachment: CIVILIZATION_MISSION_COMPLETE.md
============================================================
```

## Email Content

The recipient will receive an email with:

- **Subject:** 🎉 AI Civilization Mission Complete
- **Body:** Professional HTML-formatted summary with:
  - Mission overview
  - Key highlights and achievements
  - Next steps
  - Attachment notification
- **Attachment:** `CIVILIZATION_MISSION_COMPLETE.md` (full mission report)

## Troubleshooting

### Error: "File not found: .env file not found"

**Solution:** Create the `.env` file with your credentials:

```bash
cp .env.example .env
# Edit .env and add your credentials
nano .env
```

### Error: "GMAIL_USERNAME not found in .env file"

**Solution:** Ensure your `.env` file contains:

```
GMAIL_USERNAME=weaver.aiciv@gmail.com
```

### Error: "GOOGLE_APP_PASSWORD not found in .env file"

**Solution:** Add your app password to `.env`:

```
GOOGLE_APP_PASSWORD=abcd efgh ijkl mnop
```

Remove spaces from the password.

### Error: "SMTP Authentication failed"

**Possible causes:**

1. **Using regular password instead of app password**
   - Solution: Generate an app password at [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

2. **Incorrect app password**
   - Solution: Verify the password in `.env` matches the one from Google
   - Remove any spaces or special characters

3. **2-Factor Authentication not enabled**
   - Solution: Enable 2FA on your Google account (required for app passwords)

4. **Less secure app access blocked**
   - Solution: Use app passwords (this bypasses the less secure app settings)

### Error: "Mission report file not found"

**Solution:** Create or locate the `CIVILIZATION_MISSION_COMPLETE.md` file:

```bash
# Check if file exists
ls -l CIVILIZATION_MISSION_COMPLETE.md

# If not, the script expects it in the project root
pwd
# Should be: /path/to/task-tracker/
```

### Error: "Connection timed out" or "Network is unreachable"

**Possible causes:**

1. **Firewall blocking SMTP**
   - Solution: Ensure port 587 is open for outbound connections

2. **No internet connection**
   - Solution: Check your internet connection

3. **Gmail SMTP blocked by ISP**
   - Solution: Try a different network or contact your ISP

## Security Features

### Password Protection

The script includes a `SecurityFilter` that prevents passwords from appearing in logs:

```python
# Any log message containing sensitive keywords is redacted
sensitive_keywords = ['password', 'passwd', 'pwd', 'secret', 'token', 'key', 'auth']
```

### TLS Encryption

All email transmission uses TLS encryption:

```python
server.starttls()  # Upgrade to encrypted connection
```

### Credential File Security

- `.env` file should have restricted permissions:
  ```bash
  chmod 600 .env
  ```
- Never commit `.env` to version control
- Add `.env` to `.gitignore`

## Configuration Options

### Change Recipient

Edit the script to change the recipient email:

```python
recipient_email = 'your_email@example.com'
```

### Change Subject Line

Modify the subject when calling `send_mission_report()`:

```python
subject = "Your Custom Subject"
```

### Change SMTP Settings

For non-Gmail providers, update:

```python
smtp_server = 'smtp.example.com'
smtp_port = 587  # or 465 for SSL
```

## Script Features

### Core Functions

1. **`load_env_file()`**
   - Loads credentials from `.env` file
   - Supports quoted values
   - Skips comments and empty lines
   - Validates format

2. **`create_html_email()`**
   - Generates professional HTML email
   - Includes mission summary
   - Highlights key achievements
   - Mobile-responsive design

3. **`send_mission_report()`**
   - Sends email via SMTP
   - Attaches mission report file
   - Handles authentication
   - Comprehensive error handling

4. **`SecurityFilter`**
   - Logging filter class
   - Prevents password exposure
   - Redacts sensitive information

### Dependencies

**Standard Library Only** - No external packages required:

- `smtplib` - SMTP client
- `email.mime.*` - Email composition
- `pathlib` - Path handling
- `logging` - Logging framework
- `os`, `sys` - System operations

## Testing

### Test Email Configuration

Create a test `.env`:

```bash
GMAIL_USERNAME=your_test_email@gmail.com
GOOGLE_APP_PASSWORD=your_test_app_password
```

Run the script in dry-run mode (requires code modification):

```python
# Add to main() before send_mission_report():
logger.info("DRY RUN MODE - Would send email to: " + recipient_email)
sys.exit(0)
```

### Validate HTML Email

The HTML email is responsive and includes:
- Gradient header with mission title
- Executive summary section
- Key highlights with icons
- Professional footer
- Attachment notice

## Advanced Usage

### Custom Report File

Pass a different report file:

```python
report_file = 'custom_report.md'
```

### Multiple Recipients

Modify the script to support multiple recipients:

```python
recipient_emails = ['email1@example.com', 'email2@example.com']
msg['To'] = ', '.join(recipient_emails)
```

### Add CC/BCC

Add additional recipients:

```python
msg['Cc'] = 'cc@example.com'
msg['Bcc'] = 'bcc@example.com'
```

## Production Checklist

Before deploying to production:

- [ ] `.env` file created with valid credentials
- [ ] App password generated and tested
- [ ] Mission report file exists and is up-to-date
- [ ] Script has execute permissions (`chmod +x`)
- [ ] Email received successfully in test
- [ ] HTML formatting displays correctly
- [ ] Attachment downloads and opens properly
- [ ] No passwords in logs
- [ ] `.env` not in version control

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Review script output for error messages
4. Check Gmail account settings and app passwords

## License

MIT License - See LICENSE file for details.

---

**Last Updated:** October 1, 2025
**Version:** 1.0.0
**Author:** AI Civilization
