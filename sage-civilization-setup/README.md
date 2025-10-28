# Sage AI Civilization - Communications Setup Package

**Version:** 1.0  
**Date:** October 22, 2025  
**Compatible with:** Sage AI Civilization v1.0+

## 🎯 What This Package Does

This setup package adds three communication channels to your Sage AI Civilization:

1. **📧 Email Communication** - Send status reports and receive commands via email
2. **💬 Telegram Bot** - Real-time chat interface with your civilization
3. **🌐 Web Dashboard** - Beautiful monitoring interface in your browser

## 📦 Package Contents

```
sage-civilization-setup/
├── config/                       # Configuration templates
│   ├── email_config.json.template
│   ├── telegram_config.json.template
│   └── .env.template
├── scripts/                      # Python scripts
│   ├── install.sh               # Automated installer
│   ├── email_handler.py         # Email functionality
│   └── telegram_bot.py          # Telegram bot
├── web/                         # Web dashboard
│   ├── dashboard.py             # Flask server
│   └── templates/
│       └── dashboard.html       # Dashboard UI
├── .claude/agents/              # New agent manifests
│   ├── communications-coordinator.md
│   └── telegram-bot.md
├── docs/                        # Documentation
│   └── SETUP_GUIDE.md          # Comprehensive guide
├── requirements.txt             # Python dependencies
├── QUICK_START.txt             # Quick reference card
└── README.md                    # This file
```

## ⚡ Quick Start

### 1. Run Installation (1 minute)

```bash
cd /path/to/your/sage-civilization
bash sage-civilization-setup/scripts/install.sh
```

### 2. Configure Email (2 minutes)

1. Get Gmail App Password: https://myaccount.google.com/apppasswords
2. Edit `config/email_config.json` with your email and password
3. Test: `python3 scripts/email_handler.py test your-email@gmail.com`

### 3. Configure Telegram (3 minutes)

1. Talk to @BotFather on Telegram, send `/newbot`
2. Talk to @userinfobot to get your chat ID
3. Edit `config/telegram_config.json` with token and chat ID
4. Test: `python3 scripts/telegram_bot.py`

### 4. Start Dashboard (30 seconds)

```bash
python3 web/dashboard.py
```

Open browser to: http://localhost:5000

## 📚 Documentation

- **QUICK_START.txt** - One-page reference card
- **docs/SETUP_GUIDE.md** - Complete step-by-step guide
- **Agent Manifests** - In `.claude/agents/` directory

## 🔧 Requirements

- Python 3.8+
- pip (Python package manager)
- Internet connection
- Gmail account (for email) OR other SMTP provider
- Telegram account (for bot)

All Python dependencies are installed automatically by the install script.

## 🎯 Features

### Email Handler
- Send status reports with HTML formatting
- Test email configuration
- Automated logging
- Support for Gmail, Outlook, Yahoo, and custom SMTP

### Telegram Bot
- Real-time messaging
- Command interface (/status, /agents, /goals)
- User authorization
- Admin privileges
- Message routing to civilization
- Notification system

### Web Dashboard
- Real-time agent monitoring
- Current goals display
- Recent messages view
- Recent votes display
- Auto-refresh every 30 seconds
- Responsive design
- Search functionality

## 🤖 New Agents

### Communications Coordinator
- Routes messages between external channels and agents
- Formats messages for different channels
- Maintains comprehensive logs
- Handles authentication and authorization

### Telegram Bot
- Real-time interface for users
- Command processing
- Message relay to other agents
- Instant notifications

## 🔐 Security

This package includes security best practices:
- Template files prevent accidental credential commits
- Environment variable support
- User authorization for Telegram
- No sensitive data in code
- Comprehensive logging

**Important:** Always add these to `.gitignore`:
```
config/email_config.json
config/telegram_config.json
.env
```

## 📊 Usage Examples

### Send Email Report
```bash
python3 scripts/email_handler.py status recipient@email.com
```

### Start Telegram Bot (Background)
```bash
nohup python3 scripts/telegram_bot.py > telegram.log 2>&1 &
```

### Start Dashboard (Custom Port)
```bash
DASHBOARD_PORT=8080 python3 web/dashboard.py
```

### From Within Civilization
```
"Use the communications coordinator to send a status report via email"
"Use the telegram bot to notify users that the system is operational"
```

## 🆘 Troubleshooting

### Email Issues
- **Authentication failed**: Use App Password, not regular password
- **Connection refused**: Check SMTP server and port
- See full guide: `docs/SETUP_GUIDE.md`

### Telegram Issues
- **Unauthorized**: Add your chat ID to allowed_chat_ids
- **Bot not responding**: Verify bot token, check if bot is running
- Use `/myid` command to get your Telegram ID

### Dashboard Issues
- **Cannot connect**: Check if running on port 5000
- **No data**: Verify memories/ directory exists
- Try different port: `DASHBOARD_PORT=8080`

## 🔄 Updates & Maintenance

### Check Service Status
```bash
ps aux | grep -E "telegram_bot|dashboard"
```

### View Logs
```bash
cat memories/communication/email_logs/email_log_*.json
cat memories/communication/telegram_logs/telegram_log_*.json
```

### Restart Services
```bash
pkill -f telegram_bot.py && python3 scripts/telegram_bot.py
pkill -f dashboard.py && python3 web/dashboard.py
```

## 🚀 What's Next?

After setup, you can:

1. **Integrate with Existing Agents**
   - Update agent manifests to use communication channels
   - Route messages through Communications Coordinator

2. **Automate Reports**
   - Schedule daily status emails
   - Set up automated Telegram notifications
   - Create custom reports

3. **Customize Dashboard**
   - Modify CSS in `web/templates/dashboard.html`
   - Add new API endpoints in `web/dashboard.py`
   - Create custom widgets

4. **Extend Functionality**
   - Add more Telegram commands
   - Create email templates
   - Build API integrations

## 📝 Version History

**v1.0 (October 22, 2025)**
- Initial release
- Email handler with Gmail support
- Telegram bot with command interface
- Web dashboard with real-time updates
- Automated installation script
- Comprehensive documentation

## 🤝 Support

For issues or questions:
1. Check `docs/SETUP_GUIDE.md` for detailed instructions
2. Review error logs in `memories/communication/`
3. Verify configuration files are correct
4. Test each component individually

## 📄 License

Part of the Sage AI Civilization project.
Built with Claude Sonnet 4.5.

## 🎉 Credits

Created for the Sage AI Civilization community.
Designed to make AI agent communication seamless and powerful.

---

**Ready to connect with your civilization? Start with QUICK_START.txt!**
