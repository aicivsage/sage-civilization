#!/usr/bin/env python3
"""
Web-based Chat Interface for Sage AI Civilization
Provides real-time chat capabilities through a web interface
"""

import json
import asyncio
import uuid
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import hashlib
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
socketio = SocketIO(app, cors_allowed_origins="*")

# Chat storage paths
CHAT_DIR = Path('memories/communication/chat')
CHAT_HISTORY_DIR = CHAT_DIR / 'history'
CHAT_USERS_FILE = CHAT_DIR / 'users.json'
CHAT_ROOMS_FILE = CHAT_DIR / 'rooms.json'
MESSAGE_BUS_DIR = Path('memories/communication/message_bus/web_chat')

# Queue paths for health monitoring
QUEUE_DIR = CHAT_DIR / 'queue'
PENDING_DIR = QUEUE_DIR / 'pending'
PROCESSED_DIR = QUEUE_DIR / 'processed'

# Initialize directories
CHAT_DIR.mkdir(parents=True, exist_ok=True)
CHAT_HISTORY_DIR.mkdir(exist_ok=True)
MESSAGE_BUS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# Health Monitoring Utilities
# ============================================================================

def check_process_running(process_name: str) -> Dict[str, any]:
    """
    Check if a process is running using pgrep

    Args:
        process_name: Name of the process to check (e.g., 'chat_queue_monitor')

    Returns:
        dict with 'running' (bool) and 'pid' (int or None)
    """
    try:
        # Use pgrep to find process by name
        result = subprocess.run(
            ['pgrep', '-f', process_name],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0 and result.stdout.strip():
            # Process found - get first PID
            pids = [int(p) for p in result.stdout.strip().split('\n') if p]
            return {
                'running': True,
                'pid': pids[0] if pids else None,
                'count': len(pids)
            }
        else:
            return {
                'running': False,
                'pid': None,
                'count': 0
            }
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, ValueError) as e:
        # Error checking process - assume not running
        return {
            'running': False,
            'pid': None,
            'count': 0,
            'error': str(e)
        }

def get_queue_status() -> Dict[str, any]:
    """
    Get current queue status by scanning pending directory

    Returns:
        dict with 'pending_count', 'oldest_message_age_seconds', 'oldest_message_id'
    """
    try:
        if not PENDING_DIR.exists():
            return {
                'pending_count': 0,
                'oldest_message_age_seconds': 0,
                'oldest_message_id': None
            }

        # Get all pending message files
        pending_files = list(PENDING_DIR.glob('*.json'))
        pending_count = len(pending_files)

        if pending_count == 0:
            return {
                'pending_count': 0,
                'oldest_message_age_seconds': 0,
                'oldest_message_id': None
            }

        # Find oldest message
        oldest_file = None
        oldest_mtime = None

        for file in pending_files:
            mtime = file.stat().st_mtime
            if oldest_mtime is None or mtime < oldest_mtime:
                oldest_mtime = mtime
                oldest_file = file

        # Calculate age in seconds
        if oldest_mtime:
            oldest_age = datetime.now().timestamp() - oldest_mtime
        else:
            oldest_age = 0

        return {
            'pending_count': pending_count,
            'oldest_message_age_seconds': oldest_age,
            'oldest_message_id': oldest_file.stem if oldest_file else None
        }

    except (OSError, IOError) as e:
        return {
            'pending_count': 0,
            'oldest_message_age_seconds': 0,
            'oldest_message_id': None,
            'error': str(e)
        }

def get_activity_stats() -> Dict[str, any]:
    """
    Get activity statistics from processed messages in last hour

    Returns:
        dict with 'processed_last_hour', 'total_processed'
    """
    try:
        if not PROCESSED_DIR.exists():
            return {
                'processed_last_hour': 0,
                'total_processed': 0
            }

        # Get all processed message files
        processed_files = list(PROCESSED_DIR.glob('*.json'))
        total_processed = len(processed_files)

        # Count files modified in last hour
        one_hour_ago = datetime.now().timestamp() - 3600
        processed_last_hour = 0

        for file in processed_files:
            if file.stat().st_mtime > one_hour_ago:
                processed_last_hour += 1

        return {
            'processed_last_hour': processed_last_hour,
            'total_processed': total_processed
        }

    except (OSError, IOError) as e:
        return {
            'processed_last_hour': 0,
            'total_processed': 0,
            'error': str(e)
        }

def calculate_alert_level(queue_status: dict, process_status: dict) -> Tuple[str, List[str]]:
    """
    Calculate overall alert level and list of alerts

    Args:
        queue_status: Dict from get_queue_status()
        process_status: Dict with 'queue_monitor' and 'auto_responder' status

    Returns:
        Tuple of (alert_level, alerts_list)
        alert_level: 'green', 'yellow', or 'red'
        alerts_list: List of alert messages
    """
    alerts = []

    # Check queue health
    pending = queue_status.get('pending_count', 0)
    oldest_age = queue_status.get('oldest_message_age_seconds', 0)

    # Check process health
    queue_monitor_running = process_status.get('queue_monitor', {}).get('running', False)
    auto_responder_running = process_status.get('auto_responder', {}).get('running', False)
    processes_down = sum([
        not queue_monitor_running,
        not auto_responder_running
    ])

    # RED alerts (critical issues)
    if oldest_age > 300:  # 5 minutes
        alerts.append(f"CRITICAL: Message pending for {int(oldest_age/60)} minutes")

    if pending >= 10:
        alerts.append(f"CRITICAL: {pending} messages in queue")

    if processes_down >= 2:
        alerts.append("CRITICAL: Both queue processes are down")

    # YELLOW alerts (warnings)
    if 120 < oldest_age <= 300:  # 2-5 minutes
        alerts.append(f"WARNING: Message pending for {int(oldest_age/60)} minutes")

    if 5 <= pending < 10:
        alerts.append(f"WARNING: {pending} messages in queue")

    if processes_down == 1:
        if not queue_monitor_running:
            alerts.append("WARNING: Queue monitor is down")
        if not auto_responder_running:
            alerts.append("WARNING: Auto-responder is down")

    # Determine overall level
    if any('CRITICAL' in alert for alert in alerts):
        return 'red', alerts
    elif any('WARNING' in alert for alert in alerts):
        return 'yellow', alerts
    else:
        # All green
        if not alerts:
            alerts.append("All systems operational")
        return 'green', alerts

class ChatManager:
    """Manages chat rooms, users, and message routing"""
    
    def __init__(self):
        self.users: Dict[str, dict] = self.load_users()
        self.rooms: Dict[str, dict] = self.load_rooms()
        self.active_sessions: Dict[str, str] = {}  # session_id -> user_id
        
        # Create default room if none exist
        if not self.rooms:
            self.create_room('general', 'General discussion room', 'system')
            self.create_room('agents', 'Agent communication channel', 'system')
    
    def load_users(self) -> dict:
        """Load registered users"""
        if CHAT_USERS_FILE.exists():
            with open(CHAT_USERS_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    def save_users(self):
        """Save users to file"""
        with open(CHAT_USERS_FILE, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def load_rooms(self) -> dict:
        """Load chat rooms"""
        if CHAT_ROOMS_FILE.exists():
            with open(CHAT_ROOMS_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    def save_rooms(self):
        """Save rooms to file"""
        with open(CHAT_ROOMS_FILE, 'w') as f:
            json.dump(self.rooms, f, indent=2)
    
    def create_user(self, username: str, display_name: str = None) -> str:
        """Create a new user"""
        user_id = str(uuid.uuid4())
        self.users[user_id] = {
            'id': user_id,
            'username': username,
            'display_name': display_name or username,
            'created_at': datetime.now().isoformat(),
            'last_seen': datetime.now().isoformat(),
            'role': 'user'
        }
        self.save_users()
        return user_id
    
    def create_room(self, name: str, description: str, created_by: str) -> str:
        """Create a new chat room"""
        room_id = str(uuid.uuid4())
        self.rooms[room_id] = {
            'id': room_id,
            'name': name,
            'description': description,
            'created_by': created_by,
            'created_at': datetime.now().isoformat(),
            'members': [],
            'type': 'public'
        }
        self.save_rooms()
        return room_id
    
    def join_room_user(self, room_id: str, user_id: str):
        """Add user to room"""
        if room_id in self.rooms and user_id not in self.rooms[room_id]['members']:
            self.rooms[room_id]['members'].append(user_id)
            self.save_rooms()
    
    def leave_room_user(self, room_id: str, user_id: str):
        """Remove user from room"""
        if room_id in self.rooms and user_id in self.rooms[room_id]['members']:
            self.rooms[room_id]['members'].remove(user_id)
            self.save_rooms()
    
    def save_message(self, room_id: str, message: dict):
        """Save message to history"""
        history_file = CHAT_HISTORY_DIR / f"{room_id}.json"
        
        messages = []
        if history_file.exists():
            with open(history_file, 'r') as f:
                messages = json.load(f)
        
        messages.append(message)
        
        # Keep last 1000 messages per room
        if len(messages) > 1000:
            messages = messages[-1000:]
        
        with open(history_file, 'w') as f:
            json.dump(messages, f, indent=2)
    
    def get_room_history(self, room_id: str, limit: int = 50) -> List[dict]:
        """Get recent messages from a room"""
        history_file = CHAT_HISTORY_DIR / f"{room_id}.json"
        
        if not history_file.exists():
            return []
        
        with open(history_file, 'r') as f:
            messages = json.load(f)
        
        return messages[-limit:] if len(messages) > limit else messages
    
    def write_to_message_bus(self, user_id: str, message: str, room_id: str):
        """Write message to message bus for agent processing"""
        msg_data = {
            'timestamp': datetime.now().isoformat(),
            'source': 'web_chat',
            'user_id': user_id,
            'room_id': room_id,
            'message': message,
            'status': 'pending'
        }
        
        msg_file = MESSAGE_BUS_DIR / f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        with open(msg_file, 'w') as f:
            json.dump(msg_data, f, indent=2)

# Initialize chat manager
chat_manager = ChatManager()

@app.route('/')
def index():
    """Render chat interface"""
    return render_template('chat.html')

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    username = data.get('username')
    display_name = data.get('display_name')

    if not username:
        return jsonify({'error': 'Username required'}), 400

    # Check if username exists
    for user in chat_manager.users.values():
        if user['username'] == username:
            return jsonify({'error': 'Username already taken'}), 400

    user_id = chat_manager.create_user(username, display_name)
    session['user_id'] = user_id

    return jsonify({
        'user_id': user_id,
        'username': username,
        'display_name': display_name or username
    })

@app.route('/api/login', methods=['POST'])
def login():
    """Login an existing user"""
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({'error': 'Username required'}), 400

    # Find user by username
    for user_id, user in chat_manager.users.items():
        if user['username'] == username:
            session['user_id'] = user_id
            # Update last seen
            chat_manager.users[user_id]['last_seen'] = datetime.now().isoformat()
            chat_manager.save_users()

            return jsonify({
                'user_id': user_id,
                'username': user['username'],
                'display_name': user['display_name']
            })

    return jsonify({'error': 'User not found'}), 404

@app.route('/api/rooms')
def get_rooms():
    """Get list of available rooms"""
    rooms = []
    for room in chat_manager.rooms.values():
        rooms.append({
            'id': room['id'],
            'name': room['name'],
            'description': room['description'],
            'member_count': len(room['members'])
        })
    return jsonify(rooms)

@app.route('/api/rooms/<room_id>/history')
def get_room_history(room_id):
    """Get message history for a room"""
    limit = request.args.get('limit', 50, type=int)
    messages = chat_manager.get_room_history(room_id, limit)
    return jsonify(messages)

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'message': 'Connected to Sage Chat'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    session_id = request.sid
    if session_id in chat_manager.active_sessions:
        user_id = chat_manager.active_sessions[session_id]
        del chat_manager.active_sessions[session_id]
        
        # Update last seen
        if user_id in chat_manager.users:
            chat_manager.users[user_id]['last_seen'] = datetime.now().isoformat()
            chat_manager.save_users()

@socketio.on('authenticate')
def handle_authenticate(data):
    """Authenticate user"""
    user_id = data.get('user_id')
    
    if user_id not in chat_manager.users:
        emit('error', {'message': 'Invalid user ID'})
        return
    
    session_id = request.sid
    chat_manager.active_sessions[session_id] = user_id
    
    user = chat_manager.users[user_id]
    emit('authenticated', {
        'user': {
            'id': user['id'],
            'username': user['username'],
            'display_name': user['display_name']
        }
    })

@socketio.on('join_room')
def handle_join_room(data):
    """Handle user joining a room"""
    room_id = data.get('room_id')
    session_id = request.sid
    
    if session_id not in chat_manager.active_sessions:
        emit('error', {'message': 'Not authenticated'})
        return
    
    user_id = chat_manager.active_sessions[session_id]
    
    if room_id not in chat_manager.rooms:
        emit('error', {'message': 'Room not found'})
        return
    
    join_room(room_id)
    chat_manager.join_room_user(room_id, user_id)
    
    user = chat_manager.users[user_id]
    room = chat_manager.rooms[room_id]
    
    # Notify room members
    emit('user_joined', {
        'room_id': room_id,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'display_name': user['display_name']
        }
    }, room=room_id)
    
    # Send room info to user
    emit('room_joined', {
        'room': {
            'id': room['id'],
            'name': room['name'],
            'description': room['description']
        }
    })

@socketio.on('leave_room')
def handle_leave_room(data):
    """Handle user leaving a room"""
    room_id = data.get('room_id')
    session_id = request.sid
    
    if session_id not in chat_manager.active_sessions:
        return
    
    user_id = chat_manager.active_sessions[session_id]
    
    leave_room(room_id)
    chat_manager.leave_room_user(room_id, user_id)
    
    user = chat_manager.users[user_id]
    
    # Notify room members
    emit('user_left', {
        'room_id': room_id,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'display_name': user['display_name']
        }
    }, room=room_id)

@socketio.on('send_message')
def handle_send_message(data):
    """Handle sending a message"""
    room_id = data.get('room_id')
    message_text = data.get('message')
    session_id = request.sid
    
    if session_id not in chat_manager.active_sessions:
        emit('error', {'message': 'Not authenticated'})
        return
    
    user_id = chat_manager.active_sessions[session_id]
    user = chat_manager.users[user_id]
    
    if room_id not in chat_manager.rooms:
        emit('error', {'message': 'Room not found'})
        return
    
    # Create message object
    message = {
        'id': str(uuid.uuid4()),
        'room_id': room_id,
        'user_id': user_id,
        'username': user['username'],
        'display_name': user['display_name'],
        'message': message_text,
        'timestamp': datetime.now().isoformat(),
        'type': 'user'
    }
    
    # Save to history
    chat_manager.save_message(room_id, message)
    
    # Write to message bus for agent processing
    chat_manager.write_to_message_bus(user_id, message_text, room_id)
    
    # Broadcast to room
    emit('new_message', message, room=room_id)

@socketio.on('typing')
def handle_typing(data):
    """Handle typing indicator"""
    room_id = data.get('room_id')
    session_id = request.sid
    
    if session_id not in chat_manager.active_sessions:
        return
    
    user_id = chat_manager.active_sessions[session_id]
    user = chat_manager.users[user_id]
    
    emit('user_typing', {
        'room_id': room_id,
        'user': {
            'id': user['id'],
            'display_name': user['display_name']
        }
    }, room=room_id, include_self=False)

@socketio.on('stop_typing')
def handle_stop_typing(data):
    """Handle stop typing"""
    room_id = data.get('room_id')
    session_id = request.sid
    
    if session_id not in chat_manager.active_sessions:
        return
    
    user_id = chat_manager.active_sessions[session_id]
    
    emit('user_stopped_typing', {
        'room_id': room_id,
        'user_id': user_id
    }, room=room_id, include_self=False)

@app.route('/api/agent_message', methods=['POST'])
def agent_message():
    """Receive and broadcast agent messages"""
    data = request.json
    room_id = data.get('room_id')
    message_text = data.get('message')
    agent_name = data.get('agent_name', 'Sage Primary AI')

    if not room_id or not message_text:
        return jsonify({'error': 'Missing room_id or message'}), 400

    msg = {
        'id': str(uuid.uuid4()),
        'room_id': room_id,
        'user_id': 'agent',
        'username': agent_name,
        'display_name': f"🤖 {agent_name.split()[0]}",
        'message': message_text,
        'timestamp': datetime.now().isoformat(),
        'type': 'agent'
    }

    chat_manager.save_message(room_id, msg)
    socketio.emit('new_message', msg, room=room_id)

    return jsonify({'status': 'success', 'message_id': msg['id']})

def broadcast_agent_message(room_id: str, agent_name: str, message: str):
    """Broadcast a message from an agent to a room"""
    msg = {
        'id': str(uuid.uuid4()),
        'room_id': room_id,
        'user_id': 'agent',
        'username': agent_name,
        'display_name': f"🤖 {agent_name}",
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'type': 'agent'
    }

    chat_manager.save_message(room_id, msg)
    socketio.emit('new_message', msg, room=room_id)

# ============================================================================
# Health Monitoring API Endpoints
# ============================================================================

@app.route('/api/chat/health')
def chat_health():
    """
    Comprehensive health check endpoint for chat queue system
    Returns real-time status of queue and processes
    """
    try:
        # Check process status
        queue_monitor_status = check_process_running('chat_queue_monitor.py')
        auto_responder_status = check_process_running('auto_queue_responder.py')

        process_status = {
            'queue_monitor': queue_monitor_status,
            'auto_responder': auto_responder_status
        }

        # Check queue status
        queue_status = get_queue_status()

        # Get activity stats
        activity_stats = get_activity_stats()

        # Calculate alert level
        alert_level, alerts = calculate_alert_level(queue_status, process_status)

        # Build response
        response = {
            'status': 'healthy' if alert_level == 'green' else 'degraded' if alert_level == 'yellow' else 'critical',
            'alert_level': alert_level,
            'timestamp': datetime.now().isoformat(),
            'queue': {
                'pending_count': queue_status.get('pending_count', 0),
                'oldest_message_age_seconds': queue_status.get('oldest_message_age_seconds', 0),
                'oldest_message_id': queue_status.get('oldest_message_id')
            },
            'processes': {
                'queue_monitor': {
                    'running': queue_monitor_status.get('running', False),
                    'pid': queue_monitor_status.get('pid'),
                    'count': queue_monitor_status.get('count', 0)
                },
                'auto_responder': {
                    'running': auto_responder_status.get('running', False),
                    'pid': auto_responder_status.get('pid'),
                    'count': auto_responder_status.get('count', 0)
                }
            },
            'activity': {
                'processed_last_hour': activity_stats.get('processed_last_hour', 0),
                'total_processed': activity_stats.get('total_processed', 0)
            },
            'alerts': alerts
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({
            'status': 'error',
            'alert_level': 'red',
            'timestamp': datetime.now().isoformat(),
            'error': str(e),
            'alerts': [f'ERROR: Health check failed - {str(e)}']
        }), 500

@app.route('/api/chat/status')
def chat_status():
    """
    Detailed statistics endpoint for chat system
    Provides comprehensive metrics and diagnostics
    """
    try:
        # Get basic health data
        queue_monitor_status = check_process_running('chat_queue_monitor.py')
        auto_responder_status = check_process_running('auto_queue_responder.py')
        queue_status = get_queue_status()
        activity_stats = get_activity_stats()

        # Calculate uptime (if processes are running)
        uptime_info = {}
        if queue_monitor_status.get('running'):
            try:
                # Get process start time via ps
                result = subprocess.run(
                    ['ps', '-o', 'etime=', '-p', str(queue_monitor_status['pid'])],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    uptime_info['queue_monitor_uptime'] = result.stdout.strip()
            except:
                pass

        if auto_responder_status.get('running'):
            try:
                result = subprocess.run(
                    ['ps', '-o', 'etime=', '-p', str(auto_responder_status['pid'])],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    uptime_info['auto_responder_uptime'] = result.stdout.strip()
            except:
                pass

        # Build detailed response
        response = {
            'timestamp': datetime.now().isoformat(),
            'queue': {
                'pending': queue_status.get('pending_count', 0),
                'oldest_age_seconds': queue_status.get('oldest_message_age_seconds', 0),
                'oldest_message_id': queue_status.get('oldest_message_id')
            },
            'processes': {
                'queue_monitor': {
                    'status': 'running' if queue_monitor_status.get('running') else 'stopped',
                    'pid': queue_monitor_status.get('pid'),
                    'process_count': queue_monitor_status.get('count', 0),
                    'uptime': uptime_info.get('queue_monitor_uptime', 'N/A')
                },
                'auto_responder': {
                    'status': 'running' if auto_responder_status.get('running') else 'stopped',
                    'pid': auto_responder_status.get('pid'),
                    'process_count': auto_responder_status.get('count', 0),
                    'uptime': uptime_info.get('auto_responder_uptime', 'N/A')
                }
            },
            'activity': {
                'processed_last_hour': activity_stats.get('processed_last_hour', 0),
                'total_processed': activity_stats.get('total_processed', 0)
            },
            'directories': {
                'pending_exists': PENDING_DIR.exists(),
                'processed_exists': PROCESSED_DIR.exists(),
                'queue_exists': QUEUE_DIR.exists()
            }
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/health')
def health_check():
    """
    Simple health check endpoint
    Returns 200 if system is operational, includes chat service status
    """
    try:
        # Check if critical processes are running
        queue_monitor = check_process_running('chat_queue_monitor.py')
        auto_responder = check_process_running('auto_queue_responder.py')

        # Get queue status
        queue_status = get_queue_status()

        # Determine overall health
        is_healthy = (
            queue_monitor.get('running', False) or
            auto_responder.get('running', False)
        ) and queue_status.get('pending_count', 0) < 20

        status_code = 200 if is_healthy else 503

        response = {
            'status': 'healthy' if is_healthy else 'degraded',
            'timestamp': datetime.now().isoformat(),
            'services': {
                'web_chat': 'running',
                'queue_monitor': 'running' if queue_monitor.get('running') else 'stopped',
                'auto_responder': 'running' if auto_responder.get('running') else 'stopped'
            },
            'queue_pending': queue_status.get('pending_count', 0)
        }

        return jsonify(response), status_code

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/chat')
def chat_health_dashboard():
    """
    Render the chat health monitoring dashboard
    """
    return render_template('chat_health.html')

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)