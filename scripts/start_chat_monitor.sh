#!/bin/bash
# Start the Sage Chat Monitor as a background service

cd "$(dirname "$0")/.."

echo "Starting Sage Chat Monitor..."
nohup python3 -u scripts/chat_monitor.py > logs/chat_monitor.log 2>&1 &
echo $! > logs/chat_monitor.pid

echo "Chat Monitor started with PID: $(cat logs/chat_monitor.pid)"
echo "Log file: logs/chat_monitor.log"
echo ""
echo "To stop: kill \$(cat logs/chat_monitor.pid)"
echo "To view logs: tail -f logs/chat_monitor.log"
