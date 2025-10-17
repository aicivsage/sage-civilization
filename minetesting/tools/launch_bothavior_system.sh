#!/bin/bash
# Launch BOTHAVIOR Complete System
# Orchestrator + Diana's Mind + Status Monitor

echo "🚀 Launching BOTHAVIOR System"
echo "=============================="
echo ""

# Check if orchestrator is already running
if lsof -Pi :8787 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Port 8787 already in use - orchestrator may already be running"
    echo "   Kill it with: kill \$(lsof -t -i:8787)"
    exit 1
fi

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create logs directory
mkdir -p logs

# Start orchestrator in background
echo "1️⃣ Starting HTTP Orchestrator..."
python3 "$SCRIPT_DIR/bothavior_orchestrator.py" > logs/orchestrator.log 2>&1 &
ORCH_PID=$!
echo "   PID: $ORCH_PID"

# Wait for orchestrator to start
sleep 2

# Check if orchestrator is running
if ! kill -0 $ORCH_PID 2>/dev/null; then
    echo "❌ Orchestrator failed to start"
    cat logs/orchestrator.log
    exit 1
fi

echo "   ✅ Orchestrator running on http://127.0.0.1:8787"

# Start Diana's mind in background
echo "2️⃣ Starting Diana's Mind..."
python3 "$SCRIPT_DIR/diana_mind.py" > logs/diana.log 2>&1 &
DIANA_PID=$!
echo "   PID: $DIANA_PID"
echo "   ✅ Diana's decision loop running"

echo ""
echo "=============================="
echo "✅ BOTHAVIOR System Online!"
echo "=============================="
echo ""
echo "Components:"
echo "  • Orchestrator: http://127.0.0.1:8787 (PID: $ORCH_PID)"
echo "  • Diana's Mind: Decision loop (PID: $DIANA_PID)"
echo ""
echo "Logs:"
echo "  • Orchestrator: logs/orchestrator.log"
echo "  • Diana: logs/diana.log"
echo ""
echo "Status: curl http://127.0.0.1:8787/status"
echo "Events: curl http://127.0.0.1:8787/events"
echo ""
echo "Stop: kill $ORCH_PID $DIANA_PID"
echo "Or: ./tools/stop_bothavior_system.sh"
echo ""
echo "Next Steps:"
echo "  1. Start Minetest"
echo "  2. Enable HTTP in minetest.conf (see minetest-config-http.txt)"
echo "  3. Load world with bothavior_simple mod"
echo "  4. Spawn Diana: /ai_spawn Diana"
echo "  5. Watch the magic! ✨"
echo ""

# Save PIDs for stopping later
echo "$ORCH_PID" > /tmp/bothavior_orch.pid
echo "$DIANA_PID" > /tmp/bothavior_diana.pid

# Tail logs (Ctrl+C to stop viewing, system keeps running)
echo "Tailing logs (Ctrl+C to stop viewing)..."
tail -f logs/orchestrator.log logs/diana.log
