#!/bin/bash

# Sage AI Civilization Chat System Launcher
# Starts the web-based chat interface

echo "🏛️ Starting Sage Chat System..."

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    # Use system Python 3
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
fi

# Install required packages if not already installed
echo "Checking dependencies..."
$PIP_CMD install Flask flask-socketio python-socketio eventlet --quiet --break-system-packages 2>/dev/null || true

# Start the chat server
echo "Starting chat server on http://localhost:5001"
echo "Press Ctrl+C to stop the server"
$PYTHON_CMD web/chat.py