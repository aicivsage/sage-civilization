#!/bin/bash
# Sage Civilization Startup Script
# Starts all essential processes for chat system and AI communication

echo "🌱 Starting Sage AI Civilization..."
echo "=================================="
echo ""

# Change to sage-civilization directory
cd "$(dirname "$0")/.." || exit 1

# Check if required directories exist
echo "📁 Checking directories..."
mkdir -p memories/communication/chat/queue/{pending,responses,processed}
mkdir -p memories/communication/chat/history
mkdir -p logs
echo "✓ Directories ready"
echo ""

# 1. Start Chat Web Server
echo "🌐 Starting chat web server..."
if pgrep -f "web/chat.py" > /dev/null; then
    echo "⚠️  Chat server already running"
else
    nohup python3 web/chat.py > logs/chat_server.log 2>&1 &
    CHAT_PID=$!
    sleep 2
    if pgrep -f "web/chat.py" > /dev/null; then
        echo "✓ Chat server started (PID: $CHAT_PID)"
        echo "  URL: http://localhost:5001"
    else
        echo "❌ Chat server failed to start"
        echo "   Check logs/chat_server.log"
    fi
fi
echo ""

# 2. Start Chat Queue Monitor
echo "📬 Starting chat queue monitor..."
if pgrep -f "chat_queue_monitor.py" > /dev/null; then
    echo "⚠️  Queue monitor already running"
else
    nohup python3 -u scripts/chat_queue_monitor.py > logs/chat_monitor.log 2>&1 &
    MONITOR_PID=$!
    echo $MONITOR_PID > logs/chat_monitor.pid
    sleep 2
    if pgrep -f "chat_queue_monitor.py" > /dev/null; then
        echo "✓ Queue monitor started (PID: $MONITOR_PID)"
    else
        echo "❌ Queue monitor failed to start"
        echo "   Check logs/chat_monitor.log"
    fi
fi
echo ""

# 3. Start Auto Queue Responder
echo "🔔 Starting auto queue responder..."
if pgrep -f "auto_queue_responder.py" > /dev/null; then
    echo "⚠️  Auto-responder already running"
else
    nohup python3 -u scripts/auto_queue_responder.py > logs/auto_responder.log 2>&1 &
    RESPONDER_PID=$!
    echo $RESPONDER_PID > logs/auto_responder.pid
    sleep 2
    if pgrep -f "auto_queue_responder.py" > /dev/null; then
        echo "✓ Auto-responder started (PID: $RESPONDER_PID)"
        echo "  Checks queue every 30 seconds"
    else
        echo "❌ Auto-responder failed to start"
        echo "   Check logs/auto_responder.log"
    fi
fi
echo ""

# Status Summary
echo "=================================="
echo "✅ Sage AI Civilization is running!"
echo "=================================="
echo ""
echo "📊 System Status:"
echo "  Chat UI:        http://localhost:5001"
echo "  Queue Monitor:  Running (checks for messages)"
echo "  Auto-Responder: Running (alerts every 30s)"
echo ""
echo "💬 How to use:"
echo "  1. Open http://localhost:5001 in your browser"
echo "  2. Send messages in the chat"
echo "  3. Primary AI will be alerted and respond"
echo ""
echo "📝 Logs:"
echo "  Chat server:    logs/chat_server.log"
echo "  Queue monitor:  logs/chat_monitor.log"
echo "  Auto-responder: logs/auto_responder.log"
echo ""
echo "🛑 To stop all processes: ./scripts/stop_sage.sh"
echo ""
