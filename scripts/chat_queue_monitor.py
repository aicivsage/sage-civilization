#!/usr/bin/env python3
"""
Chat Queue Monitor - Connects chat UI to Primary AI via file queue
Replaces intelligent_chat_monitor.py with a file-based message queue
"""

import json
import time
import uuid
import requests
from datetime import datetime
from pathlib import Path

# Paths
CHAT_DIR = Path('memories/communication/chat')
CHAT_HISTORY_DIR = CHAT_DIR / 'history'
QUEUE_DIR = CHAT_DIR / 'queue'
PENDING_DIR = QUEUE_DIR / 'pending'
RESPONSES_DIR = QUEUE_DIR / 'responses'
PROCESSED_DIR = QUEUE_DIR / 'processed'
PROCESSED_MESSAGES_FILE = CHAT_DIR / 'processed_messages.json'

class ChatQueueMonitor:
    """Monitors chat for messages and queues them for Primary AI"""

    def __init__(self):
        self.processed_messages = self.load_processed_messages()
        self.greg_user_id = "868db1de-5e9a-4aac-9da5-d4803a3e3a74"
        self.general_room_id = "f20893ce-ae3e-4e80-9c27-50bc0a48d02f"

        # Ensure directories exist
        PENDING_DIR.mkdir(parents=True, exist_ok=True)
        RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    def load_processed_messages(self):
        """Load list of already processed message IDs"""
        try:
            if PROCESSED_MESSAGES_FILE.exists():
                with open(PROCESSED_MESSAGES_FILE, 'r') as f:
                    return set(json.load(f))
        except (json.JSONDecodeError, IOError) as e:
            print(f"[{datetime.now().isoformat()}] ⚠ Error loading processed messages: {e}", flush=True)
            print(f"  Starting fresh (no message history)", flush=True)
        return set()

    def save_processed_messages(self):
        """Save processed message IDs"""
        try:
            with open(PROCESSED_MESSAGES_FILE, 'w') as f:
                json.dump(list(self.processed_messages), f, indent=2)
        except (IOError, OSError) as e:
            print(f"[{datetime.now().isoformat()}] ⚠ Error saving processed messages: {e}", flush=True)

    def get_room_history(self, room_id):
        """Get chat history for a room"""
        try:
            history_file = CHAT_HISTORY_DIR / f"{room_id}.json"
            if not history_file.exists():
                return []
            with open(history_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"[{datetime.now().isoformat()}] ⚠ Error reading room history: {e}", flush=True)
            return []

    def save_message_to_history(self, room_id, message):
        """Save a message to room history"""
        try:
            history_file = CHAT_HISTORY_DIR / f"{room_id}.json"
            messages = []
            if history_file.exists():
                with open(history_file, 'r') as f:
                    messages = json.load(f)
            messages.append(message)
            if len(messages) > 1000:
                messages = messages[-1000:]
            with open(history_file, 'w') as f:
                json.dump(messages, f, indent=2)
        except (json.JSONDecodeError, IOError, OSError) as e:
            print(f"[{datetime.now().isoformat()}] ⚠ Error saving message to history: {e}", flush=True)

    def queue_message_for_primary(self, message):
        """Queue a message for Primary AI to respond to"""
        try:
            queue_file = PENDING_DIR / f"msg_{message['id']}.json"

            # Get recent conversation context (last 10 messages)
            history = self.get_room_history(self.general_room_id)
            recent_context = history[-10:] if len(history) > 10 else history

            queue_data = {
                'message': message,
                'context': recent_context,
                'queued_at': datetime.now().isoformat(),
                'room_id': self.general_room_id
            }

            with open(queue_file, 'w') as f:
                json.dump(queue_data, f, indent=2)

            print(f"[{datetime.now().isoformat()}] ✓ Queued message for Primary AI", flush=True)
            print(f"  Message: {message['message'][:100]}...", flush=True)
            print(f"  Queue file: {queue_file.name}", flush=True)

            # Send instant acknowledgment to chat
            ack_message = "✓ Message received! Working on response..."
            self.send_agent_message(self.general_room_id, ack_message)
            print(f"[{datetime.now().isoformat()}] ✓ Sent instant acknowledgment", flush=True)

        except (IOError, OSError, KeyError) as e:
            print(f"[{datetime.now().isoformat()}] ⚠ Error queuing message: {e}", flush=True)
            print(f"  Message data: {message}", flush=True)

    def check_for_responses(self):
        """Check if Primary AI has written any responses"""
        try:
            for response_file in RESPONSES_DIR.glob("*.json"):
                try:
                    with open(response_file, 'r') as f:
                        response_data = json.load(f)

                    # Validate response data
                    if 'room_id' not in response_data or 'response_text' not in response_data:
                        print(f"[{datetime.now().isoformat()}] ⚠ Invalid response format in {response_file.name}", flush=True)
                        # Move to processed anyway to avoid reprocessing
                        processed_file = PROCESSED_DIR / f"invalid_{response_file.name}"
                        response_file.rename(processed_file)
                        continue

                    # Send response to chat
                    self.send_agent_message(
                        response_data['room_id'],
                        response_data['response_text']
                    )

                    # Move to processed
                    processed_file = PROCESSED_DIR / response_file.name
                    response_file.rename(processed_file)

                    print(f"[{datetime.now().isoformat()}] ✓ Sent Primary AI response to chat", flush=True)

                except (json.JSONDecodeError, IOError, KeyError) as e:
                    print(f"[{datetime.now().isoformat()}] ⚠ Error processing response file {response_file.name}: {e}", flush=True)
                    # Move corrupted file to processed with error prefix
                    try:
                        processed_file = PROCESSED_DIR / f"error_{response_file.name}"
                        response_file.rename(processed_file)
                    except:
                        pass  # If even moving fails, just continue

        except Exception as e:
            print(f"[{datetime.now().isoformat()}] ⚠ Error in check_for_responses: {e}", flush=True)

    def send_agent_message(self, room_id, message_text):
        """Send a message as the Sage agent via API"""
        try:
            response = requests.post(
                'http://localhost:5001/api/agent_message',
                json={
                    'room_id': room_id,
                    'message': message_text,
                    'agent_name': 'Sage Primary AI'
                },
                timeout=5
            )

            if response.status_code == 200:
                print(f"[{datetime.now().isoformat()}] ✓ Message sent via Socket.IO", flush=True)
            else:
                print(f"[{datetime.now().isoformat()}] ⚠ Send status: {response.status_code}", flush=True)

        except requests.exceptions.RequestException as e:
            print(f"[{datetime.now().isoformat()}] ⚠ Failed to send: {e}", flush=True)

    def check_for_new_messages(self):
        """Check chat history for unprocessed messages from Greg"""
        try:
            history = self.get_room_history(self.general_room_id)

            for message in history:
                try:
                    msg_id = message.get('id')

                    # Skip if already processed
                    if msg_id in self.processed_messages:
                        continue

                    # Skip agent messages
                    if message.get('type') == 'agent':
                        self.processed_messages.add(msg_id)
                        continue

                    # Check if it's from Greg
                    username = message.get('username', '')
                    user_id = message.get('user_id', '')

                    if 'Greg' in username or user_id == self.greg_user_id:
                        print(f"\n[{datetime.now().isoformat()}] New message from Greg:", flush=True)
                        print(f"  Message: {message.get('message')}", flush=True)

                        # Queue for Primary AI
                        self.queue_message_for_primary(message)

                        # Mark as processed
                        self.processed_messages.add(msg_id)
                        self.save_processed_messages()

                except Exception as e:
                    print(f"[{datetime.now().isoformat()}] ⚠ Error processing message: {e}", flush=True)
                    print(f"  Message: {message}", flush=True)
                    # Continue with next message

        except Exception as e:
            print(f"[{datetime.now().isoformat()}] ⚠ Error checking for new messages: {e}", flush=True)

    def monitor(self):
        """Main monitoring loop"""
        print("\n" + "="*60, flush=True)
        print("Sage Chat Queue Monitor Starting...", flush=True)
        print("="*60, flush=True)
        print(f"Monitoring room: general ({self.general_room_id})", flush=True)
        print(f"Looking for messages from: Greg", flush=True)
        print("Mode: FILE QUEUE (Primary AI responds via file system)", flush=True)
        print(f"Queue directory: {QUEUE_DIR}", flush=True)
        print("Press Ctrl+C to stop", flush=True)
        print("="*60 + "\n", flush=True)

        # Initial check
        print("Checking for pending messages...", flush=True)
        self.check_for_new_messages()
        self.check_for_responses()
        print("Initial check complete!\n", flush=True)

        # Enter monitoring loop
        print("Entering monitoring loop (checking every 3 seconds)...\n", flush=True)

        try:
            while True:
                self.check_for_new_messages()
                self.check_for_responses()
                time.sleep(3)

        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user", flush=True)
            print("Shutting down gracefully...", flush=True)

def main():
    """Main entry point"""
    monitor = ChatQueueMonitor()
    monitor.monitor()

if __name__ == '__main__':
    main()
