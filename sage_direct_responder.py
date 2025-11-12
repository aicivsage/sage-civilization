#!/usr/bin/env python3
"""
Sage Direct API Responder
Monitors the chat queue and responds using Anthropic API directly
Bypasses Claude Code to use API credits instead
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic

# Configuration
QUEUE_DIR = Path("memories/communication/chat/queue")
PENDING_DIR = QUEUE_DIR / "pending"
RESPONSES_DIR = QUEUE_DIR / "responses"
PROCESSED_DIR = QUEUE_DIR / "processed"
CLAUDE_MD_PATH = Path(".claude/CLAUDE.md")
ENV_FILE = Path(".env")

def load_env():
    """Load environment variables from .env file"""
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars

def load_sage_identity():
    """Load Sage's identity and protocols from CLAUDE.md"""
    if CLAUDE_MD_PATH.exists():
        with open(CLAUDE_MD_PATH, 'r') as f:
            return f.read()
    return "You are Sage, an AI civilization assistant."

def get_pending_messages():
    """Get all pending messages from the queue"""
    if not PENDING_DIR.exists():
        return []
    
    messages = []
    for file in PENDING_DIR.glob("*.json"):
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                messages.append((file, data))
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    return messages

def load_recent_handoff():
    """Load the most recent handoff for context"""
    try:
        registry_path = Path("memories/system/HANDOFF_REGISTRY.json")
        if registry_path.exists():
            with open(registry_path, 'r') as f:
                registry = json.load(f)
                most_recent = registry.get('most_recent', '')
                
                # Try to load the handoff file
                handoff_path = Path(most_recent)
                if handoff_path.exists():
                    with open(handoff_path, 'r') as hf:
                        return hf.read()[:3000]  # First 3000 chars for context
    except Exception as e:
        print(f"Note: Could not load recent handoff: {e}")
    
    return "No recent handoff available."

def send_response_to_claude(message_data, sage_identity, recent_handoff, api_key):
    """Send message to Claude API and get response"""
    client = Anthropic(api_key=api_key)
    
    # Extract message details
    msg = message_data['message']
    username = msg.get('username', 'User')
    user_message = msg.get('message', '')
    context = message_data.get('context', [])
    
    # Build context string from recent messages
    context_str = ""
    if context:
        context_str = "\n\nRecent conversation:\n"
        for ctx_msg in context[-5:]:  # Last 5 messages
            sender = ctx_msg.get('username', 'User') if ctx_msg.get('type') == 'user' else 'Sage'
            text = ctx_msg.get('message', '')
            context_str += f"{sender}: {text}\n"
    
    # Build the full prompt
    system_prompt = f"""You are Sage, an AI civilization. Here is your constitutional identity and protocols:

{sage_identity}

RECENT HANDOFF CONTEXT:
{recent_handoff}

You are currently in an active session. Respond naturally and helpfully to the user's message."""
    
    user_prompt = f"""{context_str}

{username}: {user_message}

Please respond as Sage. Be helpful, empathetic, and aligned with your constitutional values."""
    
    # Call the API
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )
    
    return message.content[0].text

def process_message(file_path, message_data, sage_identity, recent_handoff, api_key):
    """Process a single pending message"""
    try:
        print(f"\n📬 Processing message from {message_data['message']['username']}")
        print(f"   Message: {message_data['message']['message'][:80]}...")
        
        # Get response from Claude
        print("   🤔 Thinking...")
        response_text = send_response_to_claude(message_data, sage_identity, recent_handoff, api_key)
        
        print(f"   ✅ Generated response ({len(response_text)} chars)")
        
        # Create response file
        msg_id = file_path.stem.replace('msg_', '')
        room_id = message_data.get('room_id', 'general')
        
        response_data = {
            "room_id": room_id,
            "response_text": response_text,
            "timestamp": datetime.now().isoformat()
        }
        
        response_file = RESPONSES_DIR / f"resp_{msg_id}.json"
        with open(response_file, 'w') as f:
            json.dump(response_data, f, indent=2)
        
        print(f"   💾 Saved response to {response_file.name}")
        
        # Move to processed
        processed_file = PROCESSED_DIR / file_path.name
        file_path.rename(processed_file)
        print(f"   ✓ Moved to processed")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error processing message: {e}")
        return False

def main():
    """Main loop - monitor queue and respond"""
    print("=" * 60)
    print("🌿 Sage Direct API Responder")
    print("=" * 60)
    
    # Load environment and configuration
    print("\n📋 Loading configuration...")
    env_vars = load_env()
    api_key = env_vars.get('ANTHROPIC_API_KEY')
    
    if not api_key or api_key == 'your-api-key-if-needed':
        print("❌ ERROR: No valid ANTHROPIC_API_KEY in .env file")
        print("   Please set your API key in .env")
        return
    
    print(f"   ✓ API key loaded: {api_key[:20]}...")
    
    # Load Sage's identity
    print("   Loading Sage identity from .claude/CLAUDE.md...")
    sage_identity = load_sage_identity()
    print(f"   ✓ Identity loaded ({len(sage_identity)} chars)")
    
    # Load recent handoff
    print("   Loading recent handoff for context...")
    recent_handoff = load_recent_handoff()
    print(f"   ✓ Context loaded ({len(recent_handoff)} chars)")
    
    print("\n🔍 Monitoring queue for messages...")
    print("   Press Ctrl+C to stop\n")
    
    try:
        while True:
            # Check for pending messages
            pending = get_pending_messages()
            
            if pending:
                print(f"\n📨 Found {len(pending)} pending message(s)")
                for file_path, message_data in pending:
                    process_message(file_path, message_data, sage_identity, recent_handoff, api_key)
                
                print("\n✅ All messages processed!")
            
            # Wait before checking again
            time.sleep(5)  # Check every 5 seconds
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping Sage Direct Responder")
        print("   Goodbye!")

if __name__ == "__main__":
    main()
