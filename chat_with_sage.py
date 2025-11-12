#!/usr/bin/env python3
"""Simple terminal chat interface for Sage"""

import json
import time
from pathlib import Path
from datetime import datetime

QUEUE_DIR = Path("memories/communication/chat/queue")
PENDING_DIR = QUEUE_DIR / "pending"
RESPONSES_DIR = QUEUE_DIR / "responses"

def send_message(username, message_text):
    """Send a message to Sage"""
    msg_id = int(time.time())
    
    message_data = {
        "message": {
            "username": username,
            "timestamp": datetime.now().isoformat(),
            "message": message_text
        },
        "context": [],
        "room_id": "general"
    }
    
    msg_file = PENDING_DIR / f"msg_{msg_id}.json"
    with open(msg_file, 'w') as f:
        json.dump(message_data, f, indent=2)
    
    return msg_id

def wait_for_response(msg_id, timeout=30):
    """Wait for Sage's response"""
    resp_file = RESPONSES_DIR / f"resp_{msg_id}.json"
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        if resp_file.exists():
            with open(resp_file, 'r') as f:
                data = json.load(f)
                return data.get('response_text', '')
        time.sleep(1)
    
    return None

def main():
    print("=" * 60)
    print("🌿 Sage Terminal Chat")
    print("=" * 60)
    print("Type your messages below. Type 'exit' to quit.\n")
    
    username = "Corey"
    
    while True:
        # Get user input
        user_input = input(f"\n{username}: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("\n👋 Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Send message
        print("📤 Sending message...")
        msg_id = send_message(username, user_input)
        
        # Wait for response
        print("⏳ Waiting for Sage's response...")
        response = wait_for_response(msg_id)
        
        if response:
            print(f"\n🌿 Sage: {response}")
        else:
            print("\n⚠️  Timeout waiting for response (check if responder is running)")

if __name__ == "__main__":
    main()
