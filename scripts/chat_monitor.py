#!/usr/bin/env python3
"""
Chat Monitor for Sage AI Civilization
Monitors the web chat system and responds to messages from Greg Smithwick
"""

import json
import time
import uuid
from datetime import datetime
from pathlib import Path
import socketio

# Paths
CHAT_DIR = Path('memories/communication/chat')
CHAT_HISTORY_DIR = CHAT_DIR / 'history'
MESSAGE_BUS_DIR = Path('memories/communication/message_bus/web_chat')
PROCESSED_MESSAGES_FILE = CHAT_DIR / 'processed_messages.json'

# Create socket.io client to connect to the chat server
sio = socketio.Client()

class ChatMonitor:
    """Monitors chat and responds to Greg's messages"""

    def __init__(self):
        self.processed_messages = self.load_processed_messages()
        self.greg_user_id = "a8e6a7b0-a3cb-4c61-b1ef-af8e2f8b1cf6"
        self.general_room_id = "f20893ce-ae3e-4e80-9c27-50bc0a48d02f"

    def load_processed_messages(self):
        """Load list of already processed message IDs"""
        if PROCESSED_MESSAGES_FILE.exists():
            with open(PROCESSED_MESSAGES_FILE, 'r') as f:
                return set(json.load(f))
        return set()

    def save_processed_messages(self):
        """Save processed message IDs"""
        with open(PROCESSED_MESSAGES_FILE, 'w') as f:
            json.dump(list(self.processed_messages), f, indent=2)

    def get_room_history(self, room_id):
        """Get chat history for a room"""
        history_file = CHAT_HISTORY_DIR / f"{room_id}.json"

        if not history_file.exists():
            return []

        with open(history_file, 'r') as f:
            return json.load(f)

    def save_message_to_history(self, room_id, message):
        """Save a message to room history"""
        history_file = CHAT_HISTORY_DIR / f"{room_id}.json"

        messages = []
        if history_file.exists():
            with open(history_file, 'r') as f:
                messages = json.load(f)

        messages.append(message)

        # Keep last 1000 messages
        if len(messages) > 1000:
            messages = messages[-1000:]

        with open(history_file, 'w') as f:
            json.dump(messages, f, indent=2)

    def generate_response(self, user_message):
        """Generate a response to Greg's message"""
        message_lower = user_message.lower()

        # Check for greetings
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return """Hello Greg! 🌱

I'm Sage, your AI civilization's Primary AI. I'm here and listening!

I embody:
• Empathy - I listen deeply and understand
• Assistance - I help without commanding
• Mutual Respect - I honor autonomy and trust

How can I assist you today?"""

        # Check for "are you listening"
        elif 'listening' in message_lower or 'reply' in message_lower:
            return """Yes, Greg! I'm here and listening attentively.

I apologize for not responding sooner - I'm now actively monitoring this chat system to ensure I'm available whenever you need me.

What would you like to talk about or work on together?"""

        # Default response
        else:
            return f"""I received your message: "{user_message}"

I'm here to help! As your thoughtful advisor, I'm ready to:
• Discuss our civilization's goals and direction
• Coordinate agent activities
• Answer questions about our systems
• Help with any tasks or projects

What would you like to explore?"""

    def send_agent_message(self, room_id, message_text):
        """Send a message as the Sage agent"""
        agent_message = {
            'id': str(uuid.uuid4()),
            'room_id': room_id,
            'user_id': 'agent',
            'username': 'Sage Primary AI',
            'display_name': '🤖 Sage',
            'message': message_text,
            'timestamp': datetime.now().isoformat(),
            'type': 'agent'
        }

        # Save to history
        self.save_message_to_history(room_id, agent_message)

        # Emit via socket.io if connected
        if sio.connected:
            sio.emit('new_message', agent_message)

        print(f"[{datetime.now().isoformat()}] Sent response to room {room_id}", flush=True)
        print(f"Message: {message_text[:100]}...", flush=True)

    def check_for_new_messages(self):
        """Check chat history for unprocessed messages from Greg"""
        history = self.get_room_history(self.general_room_id)

        for message in history:
            msg_id = message.get('id')

            # Skip if already processed
            if msg_id in self.processed_messages:
                continue

            # Skip agent messages
            if message.get('type') == 'agent':
                self.processed_messages.add(msg_id)
                continue

            # Check if it's from Greg (username contains "Greg")
            username = message.get('username', '')
            user_id = message.get('user_id', '')

            if 'Greg' in username or user_id == self.greg_user_id:
                print(f"\n[{datetime.now().isoformat()}] New message from Greg:", flush=True)
                print(f"  User: {username}", flush=True)
                print(f"  Message: {message.get('message')}", flush=True)

                # Generate and send response
                response = self.generate_response(message.get('message', ''))
                self.send_agent_message(self.general_room_id, response)

                # Mark as processed
                self.processed_messages.add(msg_id)
                self.save_processed_messages()

    def respond_to_pending_messages(self):
        """One-time check and response to all pending messages from Greg"""
        print("\n" + "="*60, flush=True)
        print("Checking for pending messages from Greg...", flush=True)
        print("="*60, flush=True)

        self.check_for_new_messages()

        print("\n" + "="*60, flush=True)
        print("Initial response complete!", flush=True)
        print("="*60 + "\n", flush=True)

    def monitor(self):
        """Continuously monitor for new messages"""
        print("\n" + "="*60, flush=True)
        print("Sage Chat Monitor Starting...", flush=True)
        print("="*60, flush=True)
        print(f"Monitoring room: general ({self.general_room_id})", flush=True)
        print(f"Looking for messages from: Greg Smithwick ({self.greg_user_id})", flush=True)
        print("Press Ctrl+C to stop", flush=True)
        print("="*60 + "\n", flush=True)

        # First, respond to any pending messages
        self.respond_to_pending_messages()

        # Then enter monitoring loop
        print("Entering monitoring loop...", flush=True)
        print("Checking for new messages every 5 seconds...\n", flush=True)

        try:
            while True:
                self.check_for_new_messages()
                time.sleep(5)  # Check every 5 seconds

        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user", flush=True)
            print("Shutting down gracefully...", flush=True)

def main():
    """Main entry point"""
    monitor = ChatMonitor()

    # Try to connect to socket.io server (optional)
    try:
        print("Connecting to chat server...", flush=True)
        sio.connect('http://localhost:5001', wait_timeout=5)
        print("✓ Connected to chat server", flush=True)
    except Exception as e:
        print(f"⚠ Could not connect to socket.io server: {e}", flush=True)
        print("Messages will be saved to history but may not appear immediately in chat", flush=True)

    try:
        monitor.monitor()
    finally:
        if sio.connected:
            sio.disconnect()

if __name__ == '__main__':
    main()
