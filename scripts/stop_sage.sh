#!/bin/bash
# Stop all Sage processes gracefully

echo "🛑 Stopping Sage AI Civilization..."
echo "=================================="
echo ""

cd "$(dirname "$0")/.." || exit 1

# Stop Auto Queue Responder
echo "Stopping auto queue responder..."
if [ -f logs/auto_responder.pid ]; then
    kill $(cat logs/auto_responder.pid) 2>/dev/null && echo "✓ Auto-responder stopped"
    rm logs/auto_responder.pid
else
    pkill -f "auto_queue_responder.py" && echo "✓ Auto-responder stopped"
fi

# Stop Chat Queue Monitor
echo "Stopping chat queue monitor..."
if [ -f logs/chat_monitor.pid ]; then
    kill $(cat logs/chat_monitor.pid) 2>/dev/null && echo "✓ Queue monitor stopped"
    rm logs/chat_monitor.pid
else
    pkill -f "chat_queue_monitor.py" && echo "✓ Queue monitor stopped"
fi

# Stop Chat Server
echo "Stopping chat web server..."
pkill -f "web/chat.py" && echo "✓ Chat server stopped"

echo ""
echo "✅ All Sage processes stopped"
echo ""
