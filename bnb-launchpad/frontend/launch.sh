#!/bin/bash

echo "🚀 BNB Token Launchpad Frontend"
echo "================================"
echo ""
echo "Starting local HTTP server..."
echo ""
echo "📍 Open in your browser:"
echo "   http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Try Python 3 first
if command -v python3 &> /dev/null; then
    python3 -m http.server 8000
# Try Python 2
elif command -v python &> /dev/null; then
    python -m SimpleHTTPServer 8000
# Try Node.js
elif command -v npx &> /dev/null; then
    npx http-server -p 8000
else
    echo "❌ Error: No HTTP server found"
    echo ""
    echo "Install one of:"
    echo "  - Python 3: apt install python3"
    echo "  - Node.js: apt install nodejs npm"
    echo ""
    echo "Or simply open index.html in your browser"
fi
