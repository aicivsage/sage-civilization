# Sage AI Civilization - Communications Setup Guide

## 🎯 Overview

This guide will help you set up three communication channels for your Sage AI Civilization:
1. **Email** - Send status reports and receive commands via email
2. **Telegram** - Real-time chat interface with your civilization
3. **Web Dashboard** - Visual monitoring interface in your browser

## 📦 What's Included

Your setup package includes:
- Configuration templates
- Python scripts for email and Telegram
- Web dashboard with real-time updates
- Agent manifests for new communication agents
- Automated installation script

## 🚀 Quick Start (5 Minutes)

### Step 1: Extract and Run Installation

1. Download and extract the setup package to your Sage AI Civilization directory
2. Open terminal and navigate to your directory:
   ```bash
   cd /path/to/sage-civilization
   ```
3. Run the installation script:
   ```bash
   bash sage-civilization-setup/scripts/install.sh
   ```

The script will:
- Create necessary directories
- Copy all files to the right places
- Install Python dependencies
- Set up configuration templates

### Step 2: Configure Email (2 minutes)

1. **Get Gmail App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Sign in to your Google account
   - Create a new app password (select "Mail" and your device)
   - Copy the 16-character password

2. **Edit configuration:**
   ```bash
   nano config/email_config.json
   ```
   
   Replace these values:
   ```json
   {
     "email_address": "your-actual-email@gmail.com",
     "app_password": "your-16-char-password-here"
   }
   ```

3. **Test it:**
   ```bash
   python3 scripts/email_handler.py test your-email@gmail.com
   ```
   
   You should receive a test email!

### Step 3: Configure Telegram (3 minutes)

1. **Create Bot:**
   - Open Telegram app
   - Search for `@BotFather`
   - Send: `/newbot`
   - Follow prompts to name your bot
   - Copy the bot token (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

2. **Get Your Chat ID:**
   - Search for `@userinfobot`
   - Start a chat
   - Copy your user ID (a number like: `123456789`)

3. **Edit configuration:**
   ```bash
   nano config/telegram_config.json
   ```
   
   Replace these values:
   ```json
   {
     "bot_token": "your-bot-token-here",
     "allowed_chat_ids": [123456789],
     "admin_chat_ids": [123456789]
   }
   ```

4. **Test it:**
   ```bash
   python3 scripts/telegram_bot.py
   ```
   
   - Open Telegram
   - Search for your bot by name
   - Send: `/start`
   - You should get a welcome message!
   - Press Ctrl+C to stop the bot

### Step 4: Start Web Dashboard (30 seconds)

```bash
python3 web/dashboard.py
```

Open your browser and go to: **http://localhost:5000**

You should see your civilization dashboard!

## 📚 Detailed Configuration

### Email Configuration Options

Edit `config/email_config.json`:

```json
{
  "smtp_server": "smtp.gmail.com",        // SMTP server
  "smtp_port": 587,                       // Port (587 for TLS, 465 for SSL)
  "use_tls": true,                        // Use TLS encryption
  "email_address": "your@email.com",      // Your email
  "app_password": "app-password",         // App password (NOT your regular password)
  "display_name": "Sage AI",              // Display name for emails
  "default_recipients": [                 // Default recipients for reports
    "recipient1@email.com"
  ]
}
```

**For Other Email Providers:**

**Outlook/Office 365:**
```json
{
  "smtp_server": "smtp-mail.outlook.com",
  "smtp_port": 587,
  "email_address": "your@outlook.com",
  "app_password": "your-password"
}
```

**Yahoo:**
```json
{
  "smtp_server": "smtp.mail.yahoo.com",
  "smtp_port": 465,
  "email_address": "your@yahoo.com",
  "app_password": "your-app-password"
}
```

### Telegram Configuration Options

Edit `config/telegram_config.json`:

```json
{
  "bot_token": "your-bot-token",          // From @BotFather
  "allowed_chat_ids": [123456789],        // Users who can use the bot
  "admin_chat_ids": [123456789],          // Users with admin privileges
  "polling_interval": 2,                  // How often to check for messages (seconds)
  "webhook_url": null,                    // For webhook mode (advanced)
  "enable_notifications": true            // Send proactive notifications
}
```

**Multiple Users:**
```json
{
  "allowed_chat_ids": [123456789, 987654321, 456789123],
  "admin_chat_ids": [123456789]
}
```

### Environment Variables

Edit `.env` for sensitive information:

```bash
# Email
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_APP_PASSWORD=your-app-password

# Telegram
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_ADMIN_CHAT_ID=123456789

# Web Dashboard
DASHBOARD_PORT=5000
DASHBOARD_HOST=0.0.0.0

# Security
SECRET_KEY=generate-a-random-secret-key
```

## 🤖 Register New Agents

Add the communication agents to your civilization:

Edit `memories/agents/agent_registry.json`:

```json
{
  "communications-coordinator": {
    "role": "Communications Hub",
    "status": "active",
    "reputation": 50,
    "manifest": ".claude/agents/communications-coordinator.md"
  },
  "telegram-bot": {
    "role": "Telegram Interface",
    "status": "active",
    "reputation": 50,
    "manifest": ".claude/agents/telegram-bot.md"
  }
}
```

## 📊 Using the Systems

### Email Commands

**Send test email:**
```bash
python3 scripts/email_handler.py test recipient@email.com
```

**Send status report:**
```bash
python3 scripts/email_handler.py status recipient@email.com
```

**From within Claude Code:**
```
"Use the email handler to send a status report to user@email.com"
```

### Telegram Commands

**Start the bot:**
```bash
python3 scripts/telegram_bot.py
```

**Run in background:**
```bash
nohup python3 scripts/telegram_bot.py > telegram.log 2>&1 &
```

**Stop background bot:**
```bash
pkill -f telegram_bot.py
```

**Available bot commands:**
- `/start` - Welcome message and help
- `/status` - System status
- `/agents` - List all agents
- `/goals` - Current goals
- `/myid` - Get your Telegram ID
- `/help` - Show help

**Send notification from civilization:**
```python
# In your agent code
from scripts.telegram_bot import TelegramBot
bot = TelegramBot()
await bot.send_notification("System update: All agents operational")
```

### Web Dashboard

**Start dashboard:**
```bash
python3 web/dashboard.py
```

**Access dashboard:**
Open browser to: http://localhost:5000

**Run on different port:**
```bash
DASHBOARD_PORT=8080 python3 web/dashboard.py
```

**Run in background:**
```bash
nohup python3 web/dashboard.py > dashboard.log 2>&1 &
```

**Features:**
- Real-time agent status
- Current goals display
- Recent messages
- Recent votes
- Auto-refresh every 30 seconds
- Manual refresh button

## 🔧 Troubleshooting

### Email Issues

**"Authentication failed"**
- Make sure you're using an App Password, not your regular password
- Enable "Less secure app access" if using older Gmail account
- Check if 2FA is enabled (required for App Passwords)

**"Connection refused"**
- Check SMTP server and port
- Verify TLS/SSL settings
- Check firewall settings

**Test connection:**
```bash
python3 -c "import smtplib; smtplib.SMTP('smtp.gmail.com', 587).starttls(); print('OK')"
```

### Telegram Issues

**"Unauthorized"**
- Verify bot token is correct
- Make sure you started a chat with your bot first
- Check that your user ID is in allowed_chat_ids

**"Bot not responding"**
- Check if bot is running: `ps aux | grep telegram_bot`
- Check logs: `cat telegram.log`
- Restart bot: `pkill -f telegram_bot && python3 scripts/telegram_bot.py`

**Get detailed logs:**
```bash
python3 scripts/telegram_bot.py 2>&1 | tee telegram-debug.log
```

### Web Dashboard Issues

**"Cannot connect"**
- Check if dashboard is running: `ps aux | grep dashboard`
- Verify port 5000 is not in use: `lsof -i :5000`
- Try different port: `DASHBOARD_PORT=8080 python3 web/dashboard.py`

**"No data showing"**
- Verify memories/ directory exists
- Check file permissions
- Ensure agent_registry.json exists

## 🔐 Security Best Practices

1. **Never commit sensitive files:**
   ```bash
   echo "config/email_config.json" >> .gitignore
   echo "config/telegram_config.json" >> .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use environment variables for production:**
   - Load from .env file
   - Never hardcode credentials

3. **Restrict Telegram access:**
   - Only add trusted users to allowed_chat_ids
   - Keep admin_chat_ids minimal
   - Regularly review access logs

4. **Secure web dashboard:**
   - Don't expose to internet without authentication
   - Use reverse proxy (nginx) for public access
   - Add rate limiting

## 🚀 Advanced Usage

### Autostart on Boot

**systemd service for Telegram bot:**

Create `/etc/systemd/system/sage-telegram.service`:

```ini
[Unit]
Description=Sage AI Telegram Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/sage-civilization
ExecStart=/usr/bin/python3 scripts/telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable sage-telegram
sudo systemctl start sage-telegram
```

### Webhook Mode for Telegram

For better performance with high message volume:

1. Get SSL certificate
2. Set up webhook URL
3. Configure in telegram_config.json:
   ```json
   {
     "webhook_url": "https://yourdomain.com/telegram-webhook"
   }
   ```

### Custom Dashboard Themes

Edit `web/templates/dashboard.html` CSS section to customize colors and layout.

### Email Templates

Customize email formats in `scripts/email_handler.py`:
- Modify `format_status_report()` method
- Add new email types
- Customize HTML templates

## 📈 Monitoring

**Check logs:**
```bash
# Email logs
cat memories/communication/email_logs/email_log_*.json

# Telegram logs
cat memories/communication/telegram_logs/telegram_log_*.json

# Message bus
ls -la memories/communication/message_bus/
```

**Monitor bot status:**
```bash
watch -n 5 'ps aux | grep -E "telegram_bot|dashboard"'
```

## 🆘 Support

**Common Issues:**
1. Check logs in memories/communication/
2. Verify configuration files
3. Test network connectivity
4. Review agent manifests

**Need Help?**
- Check memories/agents/*/error_log.json
- Review system status: `/system/status-report`
- Test each component individually

## ✅ Verification Checklist

- [ ] Email config created and tested
- [ ] Telegram bot created and responding
- [ ] Web dashboard accessible
- [ ] Agent manifests in .claude/agents/
- [ ] Agents registered in agent_registry.json
- [ ] Python dependencies installed
- [ ] All tests passing
- [ ] Background services configured (optional)
- [ ] Security settings reviewed
- [ ] Logs directories created

## 🎉 You're All Set!

Your Sage AI Civilization now has:
- ✅ Email communication
- ✅ Telegram real-time chat
- ✅ Web monitoring dashboard
- ✅ Two new specialized agents

**Next Steps:**
1. Talk to your civilization via Telegram
2. Monitor activity on the dashboard
3. Set up automated status reports
4. Integrate with other agents

Enjoy your enhanced AI civilization! 🏛️
