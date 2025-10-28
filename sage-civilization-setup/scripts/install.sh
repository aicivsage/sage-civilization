#!/bin/bash
# Sage AI Civilization Communications Setup Script
# This script will install and configure email, Telegram, and web communications

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Sage AI Civilization - Communications Setup              ║"
echo "║  This will set up email, Telegram, and web dashboard      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if running in Sage AI Civilization directory
if [ ! -d ".claude" ]; then
    print_error "This doesn't appear to be a Sage AI Civilization directory"
    print_info "Please run this script from your sage-civilization directory"
    exit 1
fi

print_success "Found Sage AI Civilization directory"

# Create necessary directories
echo ""
echo "Creating directory structure..."
mkdir -p config
mkdir -p web/templates
mkdir -p web/static
mkdir -p scripts
mkdir -p memories/communication/{email_logs,telegram_logs,message_bus}
mkdir -p .claude/agents
print_success "Directories created"

# Copy configuration files
echo ""
echo "Setting up configuration files..."

if [ -f "config/email_config.json" ]; then
    print_info "Email config already exists, skipping..."
else
    cp sage-civilization-setup/config/email_config.json.template config/email_config.json
    print_success "Email config template created"
fi

if [ -f "config/telegram_config.json" ]; then
    print_info "Telegram config already exists, skipping..."
else
    cp sage-civilization-setup/config/telegram_config.json.template config/telegram_config.json
    print_success "Telegram config template created"
fi

if [ -f ".env" ]; then
    print_info ".env already exists, skipping..."
else
    cp sage-civilization-setup/config/.env.template .env
    print_success ".env template created"
fi

# Copy scripts
echo ""
echo "Installing communication scripts..."
cp sage-civilization-setup/scripts/email_handler.py scripts/
cp sage-civilization-setup/scripts/telegram_bot.py scripts/
chmod +x scripts/*.py
print_success "Scripts installed"

# Copy web dashboard
echo ""
echo "Installing web dashboard..."
cp sage-civilization-setup/web/dashboard.py web/
cp sage-civilization-setup/web/templates/dashboard.html web/templates/
print_success "Web dashboard installed"

# Copy agent manifests
echo ""
echo "Installing new agent manifests..."
cp sage-civilization-setup/.claude/agents/communications-coordinator.md .claude/agents/
cp sage-civilization-setup/.claude/agents/telegram-bot.md .claude/agents/
print_success "Agent manifests installed"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
print_info "This may take a minute..."

pip install --break-system-packages python-telegram-bot flask flask-cors python-dotenv 2>&1 | grep -v "WARNING" || true
print_success "Python dependencies installed"

# Test installations
echo ""
echo "Testing installations..."

python3 -c "import telegram" 2>/dev/null && print_success "Telegram library OK" || print_error "Telegram library failed"
python3 -c "import flask" 2>/dev/null && print_success "Flask library OK" || print_error "Flask library failed"
python3 -c "from dotenv import load_dotenv" 2>/dev/null && print_success "Python-dotenv OK" || print_error "Python-dotenv failed"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Installation Complete!                                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "1. Configure Email:"
echo "   - Edit config/email_config.json"
echo "   - Get Gmail App Password: https://myaccount.google.com/apppasswords"
echo "   - Add your email and password"
echo ""
echo "2. Configure Telegram:"
echo "   - Talk to @BotFather on Telegram to create a bot"
echo "   - Get your bot token"
echo "   - Talk to @userinfobot to get your chat ID"
echo "   - Edit config/telegram_config.json with token and chat ID"
echo ""
echo "3. Test Email:"
echo "   python3 scripts/email_handler.py test your-email@example.com"
echo ""
echo "4. Start Telegram Bot:"
echo "   python3 scripts/telegram_bot.py"
echo "   (Run in background: nohup python3 scripts/telegram_bot.py &)"
echo ""
echo "5. Start Web Dashboard:"
echo "   python3 web/dashboard.py"
echo "   Then visit: http://localhost:5000"
echo ""
echo "6. Update Agent Registry:"
echo "   Add the new agents to memories/agents/agent_registry.json:"
echo "   - communications-coordinator"
echo "   - telegram-bot"
echo ""
print_info "For detailed instructions, see: docs/SETUP_GUIDE.md"
echo ""
