#!/bin/bash
# AI-CIV Dashboard Auto-Installer
# Installs and launches the real-time agent visualization dashboard

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Emojis
ROCKET="🚀"
CHECK="✅"
WARN="⚠️"
INFO="ℹ️"
SPARKLE="✨"
WRENCH="🔧"

echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║        AI-CIV Dashboard Auto-Installer ${ROCKET}               ║"
echo "║                                                          ║"
echo "║        Real-time Agent Visualization Dashboard          ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Detect installation directory
INSTALL_DIR="${1:-$(pwd)}"
cd "$INSTALL_DIR"

echo -e "${BLUE}${INFO} Installation directory: ${INSTALL_DIR}${NC}"
echo ""

# Step 1: Check Python
echo -e "${CYAN}[1/7] ${WRENCH} Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo -e "${GREEN}${CHECK} Python ${PYTHON_VERSION} found${NC}"
else
    echo -e "${RED}${WARN} Python 3 not found!${NC}"
    echo "Please install Python 3.8 or higher:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "  MacOS: brew install python3"
    echo "  Windows: Download from python.org"
    exit 1
fi
echo ""

# Step 2: Check/Create virtual environment
echo -e "${CYAN}[2/7] ${WRENCH} Setting up virtual environment...${NC}"
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo -e "${GREEN}${CHECK} Virtual environment created${NC}"
else
    echo -e "${GREEN}${CHECK} Virtual environment already exists${NC}"
fi
echo ""

# Step 3: Activate virtual environment and install dependencies
echo -e "${CYAN}[3/7] ${WRENCH} Installing Python dependencies...${NC}"
source .venv/bin/activate

# Check if packages are already installed
FLASK_INSTALLED=$(pip list 2>/dev/null | grep -c "Flask " || true)
if [ "$FLASK_INSTALLED" -eq 0 ]; then
    echo "Installing Flask, Flask-SocketIO, python-dotenv..."
    pip install Flask==3.1.2 Flask-SocketIO==5.5.1 python-dotenv==1.1.1 --quiet
    echo -e "${GREEN}${CHECK} Dependencies installed${NC}"
else
    echo -e "${GREEN}${CHECK} Dependencies already installed${NC}"
fi
echo ""

# Step 4: Create directory structure
echo -e "${CYAN}[4/7] ${WRENCH} Creating directory structure...${NC}"

mkdir -p web/templates
mkdir -p .claude/observatory
mkdir -p tools

echo -e "${GREEN}${CHECK} Directories created${NC}"
echo ""

# Step 5: Check for required files
echo -e "${CYAN}[5/7] ${WRENCH} Checking required files...${NC}"

MISSING_FILES=()

# Check for core files
if [ ! -f "web/app.py" ]; then
    MISSING_FILES+=("web/app.py")
fi

if [ ! -f "web/templates/dashboard.html" ]; then
    MISSING_FILES+=("web/templates/dashboard.html")
fi

if [ ! -f ".claude/observatory/observatory.py" ]; then
    MISSING_FILES+=(".claude/observatory/observatory.py")
fi

if [ ! -f "tools/conductor_tools.py" ]; then
    MISSING_FILES+=("tools/conductor_tools.py")
fi

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo -e "${YELLOW}${WARN} Missing files detected:${NC}"
    for file in "${MISSING_FILES[@]}"; do
        echo "  - $file"
    done
    echo ""
    echo "Please copy the following files from the AI-CIV repository:"
    echo "  git clone https://github.com/ai-CIV-2025/ai-civ-collective.git"
    echo "  cd ai-civ-collective"
    echo "  cp -r web/ .claude/ tools/ $INSTALL_DIR/"
    echo ""
    echo "Or download the installation package from:"
    echo "  https://github.com/ai-CIV-2025/ai-civ-collective/releases"
    echo ""
    exit 1
else
    echo -e "${GREEN}${CHECK} All required files present${NC}"
fi
echo ""

# Step 6: Create/check state file
echo -e "${CYAN}[6/7] ${WRENCH} Initializing dashboard state...${NC}"

STATE_FILE=".claude/observatory/dashboard-state.json"
if [ ! -f "$STATE_FILE" ]; then
    echo "Creating initial state file..."
    cat > "$STATE_FILE" << 'EOF'
{
  "version": "1.0.0",
  "currentDeployment": null,
  "history": [],
  "stats": {
    "totalDeployments": 0,
    "totalAgentsDeployed": 0,
    "totalFindings": 0
  },
  "lastUpdated": null
}
EOF
    echo -e "${GREEN}${CHECK} State file initialized${NC}"
else
    echo -e "${GREEN}${CHECK} State file already exists${NC}"
fi
echo ""

# Step 7: Create/check start script
echo -e "${CYAN}[7/7] ${WRENCH} Creating launch script...${NC}"

if [ ! -f "start-dashboard" ]; then
    cat > start-dashboard << 'EOF'
#!/bin/bash
# Launch AI-CIV Web Dashboard

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🎭 Starting AI-CIV Collective Web Dashboard..."
echo "📡 Real-time updates enabled"
echo "🌐 Open http://localhost:5000 in your browser"
echo ""
echo "Press Ctrl+C to stop"
echo ""

exec .venv/bin/python web/app.py
EOF
    chmod +x start-dashboard
    echo -e "${GREEN}${CHECK} Launch script created${NC}"
else
    echo -e "${GREEN}${CHECK} Launch script already exists${NC}"
fi
echo ""

# Installation complete
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║          ${SPARKLE} Installation Complete! ${SPARKLE}                      ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

echo -e "${BLUE}${ROCKET} Quick Start:${NC}"
echo ""
echo "  1. Launch the dashboard:"
echo -e "     ${CYAN}./start-dashboard${NC}"
echo ""
echo "  2. Open your browser:"
echo -e "     ${CYAN}http://localhost:5000${NC}"
echo ""
echo "  3. Start a mission (in another terminal):"
echo -e "${CYAN}"
cat << 'EOF'
     python3 << 'PYTHON'
from tools.conductor_tools import Mission

mission = Mission("Test mission")
mission.add_agent("agent-1")
mission.start()
mission.update_agent("agent-1", "working", 50, "Testing...")
mission.complete_agent("agent-1", ["Success!"])
mission.complete("Mission complete!")
PYTHON
EOF
echo -e "${NC}"
echo ""

echo -e "${BLUE}${INFO} Configuration:${NC}"
echo "  - State file: .claude/observatory/dashboard-state.json"
echo "  - Port: 5000 (change with: export FLASK_PORT=8080)"
echo "  - Host: 0.0.0.0 (all interfaces)"
echo ""

echo -e "${BLUE}${INFO} Documentation:${NC}"
echo "  - Full guide: tools/DASHBOARD-INSTALL.md"
echo "  - Customization: Edit web/templates/dashboard.html"
echo "  - API docs: .claude/observatory/README.md"
echo ""

# Offer to launch
echo -e "${YELLOW}${ROCKET} Launch dashboard now? (y/n)${NC} "
read -r -n 1 LAUNCH
echo ""

if [[ $LAUNCH =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}${ROCKET} Launching dashboard...${NC}"
    echo ""
    ./start-dashboard
else
    echo -e "${BLUE}${INFO} To launch later, run: ${CYAN}./start-dashboard${NC}"
    echo ""
    echo -e "${GREEN}Happy agent orchestrating! ${SPARKLE}${NC}"
fi
