#!/bin/bash
# Stop BOTHAVIOR System

echo "🛑 Stopping BOTHAVIOR System..."

# Read PIDs
if [ -f /tmp/bothavior_orch.pid ]; then
    ORCH_PID=$(cat /tmp/bothavior_orch.pid)
    if kill -0 $ORCH_PID 2>/dev/null; then
        kill $ORCH_PID
        echo "   ✅ Stopped orchestrator (PID: $ORCH_PID)"
    fi
    rm /tmp/bothavior_orch.pid
fi

if [ -f /tmp/bothavior_diana.pid ]; then
    DIANA_PID=$(cat /tmp/bothavior_diana.pid)
    if kill -0 $DIANA_PID 2>/dev/null; then
        kill $DIANA_PID
        echo "   ✅ Stopped Diana's mind (PID: $DIANA_PID)"
    fi
    rm /tmp/bothavior_diana.pid
fi

# Fallback: kill by port
if lsof -Pi :8787 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    kill $(lsof -t -i:8787)
    echo "   ✅ Killed process on port 8787"
fi

echo ""
echo "✅ BOTHAVIOR System stopped"
