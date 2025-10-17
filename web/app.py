#!/usr/bin/env python3
"""
AI-CIV Collective Web Dashboard
Real-time agent visualization with WebSocket updates
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import threading
import time

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app, cors_allowed_origins="*")

# Path to Observatory state
STATE_FILE = Path(__file__).parent.parent / ".claude/observatory/dashboard-state.json"


def load_state():
    """Load current Observatory state"""
    if not STATE_FILE.exists():
        return {
            "version": "1.0.0",
            "currentDeployment": None,
            "history": [],
            "stats": {
                "totalDeployments": 0,
                "totalAgentsDeployed": 0,
                "totalFindings": 0
            }
        }

    with open(STATE_FILE, 'r') as f:
        return json.load(f)


def format_timestamp(iso_timestamp):
    """Format ISO timestamp to human-readable"""
    if not iso_timestamp:
        return "N/A"

    try:
        dt = datetime.fromisoformat(iso_timestamp)
        now = datetime.now()
        delta = now - dt

        if delta.total_seconds() < 60:
            return f"{int(delta.total_seconds())}s ago"
        elif delta.total_seconds() < 3600:
            return f"{int(delta.total_seconds() / 60)}m ago"
        elif delta.total_seconds() < 86400:
            return f"{int(delta.total_seconds() / 3600)}h ago"
        else:
            return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return iso_timestamp


def broadcast_state():
    """Background thread to broadcast state updates"""
    last_state = None

    while True:
        try:
            state = load_state()

            # Only broadcast if state changed
            if state != last_state:
                # Format timestamps for display
                if state.get('currentDeployment'):
                    dep = state['currentDeployment']
                    dep['startTime_formatted'] = format_timestamp(dep.get('startTime'))

                    for agent in dep.get('agents', []):
                        agent['startTime_formatted'] = format_timestamp(agent.get('startTime'))
                        agent['completedAt_formatted'] = format_timestamp(agent.get('completedAt'))

                for dep in state.get('history', [])[:10]:  # Only send recent 10
                    dep['completedAt_formatted'] = format_timestamp(dep.get('completedAt'))

                socketio.emit('state_update', state, namespace='/')
                last_state = state

            time.sleep(1)  # Check every second

        except Exception as e:
            print(f"Error broadcasting state: {e}")
            time.sleep(1)


@app.route('/')
def index():
    """Serve main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/state')
def get_state():
    """API endpoint for current state"""
    return jsonify(load_state())


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('state_update', load_state())


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')


if __name__ == '__main__':
    # Start background state broadcaster
    broadcaster = threading.Thread(target=broadcast_state, daemon=True)
    broadcaster.start()

    print("🎭 AI-CIV Collective Web Dashboard starting...")
    print("📡 Real-time updates enabled via WebSocket")
    print("🌐 Open http://localhost:5000 in your browser")
    print()

    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
