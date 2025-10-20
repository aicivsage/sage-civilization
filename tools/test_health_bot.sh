#!/bin/bash
# Test A-C-Gee Health Coach Bot
# Tests connection and sends initial message to Corey

PROJECT_ROOT="/home/corey/projects/AI-CIV/grow_gemini_deepresearch"
cd "$PROJECT_ROOT" || exit 1

BOT_TOKEN="8472258805:AAFdYmIlJozyqIVjNC8PHEDAK_-XZ1vO3T4"
COREY_CHAT_ID="437939400"

echo "=== A-C-Gee Health Coach Bot Test ==="
echo ""

# Test 1: Check pyTelegramBotAPI installation
echo "1. Checking pyTelegramBotAPI installation..."
if python3 -c "import telebot" 2>/dev/null; then
    VERSION=$(python3 -c "import telebot; print(telebot.__version__)")
    echo "   ✅ pyTelegramBotAPI installed (version $VERSION)"
else
    echo "   ❌ pyTelegramBotAPI not installed. Installing..."
    pip3 install pyTelegramBotAPI
    if [ $? -eq 0 ]; then
        echo "   ✅ pyTelegramBotAPI installed successfully"
    else
        echo "   ❌ Installation failed"
        exit 1
    fi
fi
echo ""

# Test 2: Test bot connection
echo "2. Testing bot connection..."
python3 tools/health_bot_handler.py --test --token "$BOT_TOKEN"
if [ $? -eq 0 ]; then
    echo "   ✅ Bot connection successful"
else
    echo "   ❌ Bot connection failed"
    exit 1
fi
echo ""

# Test 3: Send test message
echo "3. Sending test message to Corey..."
python3 -c "
import telebot
bot = telebot.TeleBot('$BOT_TOKEN')
message = '''🏥 *A-C-Gee Health Coach Bot is online!*

I'm ready to help you track:
• Weight (Sundays: +/-\$100 per lb)
• Blood pressure (+\$10 per check)
• Steps (+\$20 if ≥6k, -\$20 if <6k)

*Try these commands:*
• /help - Full instructions
• /status - Current data & balance
• /streak - Current streaks

Or just message me naturally:
• \"weight 195\"
• \"BP 120/80\"
• \"steps 7000\"

Let's build healthy habits! 💪
'''
try:
    result = bot.send_message($COREY_CHAT_ID, message, parse_mode='Markdown')
    print('   ✅ Test message sent successfully!')
    print(f'   Message ID: {result.message_id}')
except Exception as e:
    print(f'   ❌ Failed to send message: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "=== All Tests Passed! ==="
    echo ""
    echo "Health bot is configured and ready."
    echo ""
    echo "To start the bot permanently:"
    echo "  export HEALTH_BOT_TOKEN=\"$BOT_TOKEN\""
    echo "  nohup python3 tools/health_bot_handler.py > /tmp/health_bot.log 2>&1 &"
    echo ""
    echo "Or for testing:"
    echo "  python3 tools/health_bot_handler.py --token \"$BOT_TOKEN\""
else
    echo ""
    echo "=== Test Failed ==="
    exit 1
fi
