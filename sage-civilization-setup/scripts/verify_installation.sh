#!/bin/bash
# Sage AI Civilization - Installation Verification Script
# This script checks if everything is set up correctly

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Sage AI Civilization - Installation Verification         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASS=0
FAIL=0
WARN=0

check_pass() {
    echo -e "${GREEN}✓ $1${NC}"
    ((PASS++))
}

check_fail() {
    echo -e "${RED}✗ $1${NC}"
    ((FAIL++))
}

check_warn() {
    echo -e "${YELLOW}⚠ $1${NC}"
    ((WARN++))
}

echo "Checking directory structure..."
[ -d "config" ] && check_pass "config/ directory exists" || check_fail "config/ directory missing"
[ -d "scripts" ] && check_pass "scripts/ directory exists" || check_fail "scripts/ directory missing"
[ -d "web" ] && check_pass "web/ directory exists" || check_fail "web/ directory missing"
[ -d ".claude/agents" ] && check_pass ".claude/agents/ directory exists" || check_fail ".claude/agents/ directory missing"
[ -d "memories/communication" ] && check_pass "memories/communication/ directory exists" || check_fail "memories/communication/ directory missing"

echo ""
echo "Checking configuration files..."
if [ -f "config/email_config.json" ]; then
    if grep -q "YOUR_EMAIL" "config/email_config.json" 2>/dev/null; then
        check_warn "Email config exists but not configured"
    else
        check_pass "Email config exists and appears configured"
    fi
else
    check_fail "Email config missing"
fi

if [ -f "config/telegram_config.json" ]; then
    if grep -q "YOUR_BOT_TOKEN" "config/telegram_config.json" 2>/dev/null; then
        check_warn "Telegram config exists but not configured"
    else
        check_pass "Telegram config exists and appears configured"
    fi
else
    check_fail "Telegram config missing"
fi

echo ""
echo "Checking scripts..."
[ -f "scripts/email_handler.py" ] && check_pass "Email handler script exists" || check_fail "Email handler missing"
[ -f "scripts/telegram_bot.py" ] && check_pass "Telegram bot script exists" || check_fail "Telegram bot missing"
[ -x "scripts/email_handler.py" ] && check_pass "Email handler is executable" || check_warn "Email handler not executable (run: chmod +x scripts/email_handler.py)"
[ -x "scripts/telegram_bot.py" ] && check_pass "Telegram bot is executable" || check_warn "Telegram bot not executable (run: chmod +x scripts/telegram_bot.py)"

echo ""
echo "Checking web dashboard..."
[ -f "web/dashboard.py" ] && check_pass "Dashboard script exists" || check_fail "Dashboard missing"
[ -f "web/templates/dashboard.html" ] && check_pass "Dashboard template exists" || check_fail "Dashboard template missing"

echo ""
echo "Checking agent manifests..."
[ -f ".claude/agents/communications-coordinator.md" ] && check_pass "Communications coordinator manifest exists" || check_fail "Communications coordinator manifest missing"
[ -f ".claude/agents/telegram-bot.md" ] && check_pass "Telegram bot manifest exists" || check_fail "Telegram bot manifest missing"

echo ""
echo "Checking Python dependencies..."
python3 -c "import telegram" 2>/dev/null && check_pass "python-telegram-bot installed" || check_fail "python-telegram-bot missing (run: pip install python-telegram-bot --break-system-packages)"
python3 -c "import flask" 2>/dev/null && check_pass "Flask installed" || check_fail "Flask missing (run: pip install flask --break-system-packages)"
python3 -c "import flask_cors" 2>/dev/null && check_pass "Flask-CORS installed" || check_fail "Flask-CORS missing (run: pip install flask-cors --break-system-packages)"
python3 -c "from dotenv import load_dotenv" 2>/dev/null && check_pass "python-dotenv installed" || check_fail "python-dotenv missing (run: pip install python-dotenv --break-system-packages)"

echo ""
echo "Checking agent registry..."
if [ -f "memories/agents/agent_registry.json" ]; then
    check_pass "Agent registry exists"
    if grep -q "communications-coordinator" "memories/agents/agent_registry.json" 2>/dev/null; then
        check_pass "Communications coordinator in registry"
    else
        check_warn "Communications coordinator not in registry (see docs/agent_registry_additions.json)"
    fi
    if grep -q "telegram-bot" "memories/agents/agent_registry.json" 2>/dev/null; then
        check_pass "Telegram bot in registry"
    else
        check_warn "Telegram bot not in registry (see docs/agent_registry_additions.json)"
    fi
else
    check_fail "Agent registry missing"
fi

echo ""
echo "════════════════════════════════════════════════════════════"
echo "SUMMARY:"
echo -e "${GREEN}✓ Passed: $PASS${NC}"
echo -e "${YELLOW}⚠ Warnings: $WARN${NC}"
echo -e "${RED}✗ Failed: $FAIL${NC}"
echo "════════════════════════════════════════════════════════════"

if [ $FAIL -eq 0 ]; then
    echo ""
    echo "🎉 Installation verification complete!"
    if [ $WARN -gt 0 ]; then
        echo "⚠️  You have $WARN warnings to address."
        echo "📖 Check the messages above and docs/SETUP_GUIDE.md"
    else
        echo "✅ Everything looks good!"
    fi
    echo ""
    echo "Next steps:"
    echo "1. Configure your credentials in config files"
    echo "2. Test email: python3 scripts/email_handler.py test your@email.com"
    echo "3. Test Telegram: python3 scripts/telegram_bot.py"
    echo "4. Start dashboard: python3 web/dashboard.py"
else
    echo ""
    echo "❌ Installation verification found issues."
    echo "📖 Please review the failures above and:"
    echo "   - Check docs/SETUP_GUIDE.md"
    echo "   - Re-run install.sh if files are missing"
    echo "   - Install missing Python packages"
fi
echo ""
