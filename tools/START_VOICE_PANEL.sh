#!/bin/bash
# Quick launcher for Voice Control Panel

echo "🎤 Starting SAGE Voice Control Panel..."
echo ""

cd "$(dirname "$0")/.."
source venv/bin/activate
python3 tools/voice_control_panel.py
