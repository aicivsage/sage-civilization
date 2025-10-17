#!/bin/bash

set -e

echo "🚀 Installing Browser Vision System..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers (Chromium)..."
playwright install chromium

# Create session directory
echo "📁 Creating session directory..."
mkdir -p /tmp/browser-vision/sessions

# Create logs directory
mkdir -p /tmp/browser-vision/logs

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Add MCP server to Claude Code config:"
echo "   ~/.config/claude/claude_desktop_config.json"
echo ""
echo "2. Add this configuration:"
echo '   {'
echo '     "mcpServers": {'
echo '       "browser-vision": {'
echo '         "command": "'$SCRIPT_DIR'/venv/bin/python",'
echo '         "args": ["'$SCRIPT_DIR'/server/mcp_server.py"]'
echo '       }'
echo '     }'
echo '   }'
echo ""
echo "3. Restart Claude Code"
echo ""
echo "4. Test with: source venv/bin/activate && python tests/test_basic_flow.py"
