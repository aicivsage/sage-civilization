#!/usr/bin/env python3
"""
Chat-Agent Bridge
Monitors web chat messages and routes them to appropriate agents
Sends agent responses back to the chat interface
"""

import json
import time
import threading
from pathlib import Path
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Check if we can import from task_tracker, otherwise create a simple version
try:
    from task_tracker.agent_messaging.message_bus import MessageBus, JSONFileStorage
    from task_tracker.agent_messaging.message import Message
except ImportError:
    # Simple fallback implementation
    print("Note: Using simplified message bus implementation")
    
    class Message:
        def __init__(self, sender, recipient, content, metadata=None):
            self.sender = sender
            self.recipient = recipient
            self.content = content
            self.metadata = metadata or {}
            self.topic = None
            self.id = str(datetime.now().timestamp())
            
        def set_topic(self, topic):
            self.topic = topic
    
    class MessageBus:
        def __init__(self, storage=None):
            self.agents = set()
            self.subscriptions = {}
            
        def register_agent(self, agent):
            self.agents.add(agent)
            
        def subscribe(self, agent, topic):
            if topic not in self.subscriptions:
                self.subscriptions[topic] = set()
            self.subscriptions[topic].add(agent)
            
        def send(self, message):
            print(f"Message sent: {message.content}")
    
    class JSONFileStorage:
        def __init__(self, path):
            self.path = path

# Paths
WEB_CHAT_DIR = Path('memories/communication/message_bus/web_chat')
AGENT_RESPONSE_DIR = Path('memories/communication/message_bus/agent_responses')
PROCESSED_DIR = Path('memories/communication/message_bus/processed')

# Ensure directories exist
WEB_CHAT_DIR.mkdir(parents=True, exist_ok=True)
AGENT_RESPONSE_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

class ChatAgentBridge:
    """Bridges web chat with agent message bus"""
    
    def __init__(self):
        self.message_bus = MessageBus(
            storage=JSONFileStorage('memories/communication/message_bus/messages.json')
        )
        self.running = False
        self.monitor_thread = None
        
        # Register core agents
        self.register_agents()
    
    def register_agents(self):
        """Register agents with the message bus"""
        agents = [
            'primary-ai',
            'architect',
            'coder',
            'tester',
            'reviewer',
            'researcher',
            'email-monitor',
            'tg-archi'
        ]
        
        for agent in agents:
            self.message_bus.register_agent(agent)
            # Subscribe to chat messages
            self.message_bus.subscribe(agent, 'chat.message')
    
    def start(self):
        """Start the bridge"""
        self.running = True
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_chat_messages)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        print("🌉 Chat-Agent Bridge started")
        print("Monitoring for chat messages...")
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the bridge"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join()
        print("\n🛑 Chat-Agent Bridge stopped")
    
    def monitor_chat_messages(self):
        """Monitor for new chat messages and route to agents"""
        while self.running:
            try:
                # Check for new chat messages
                for msg_file in WEB_CHAT_DIR.glob('msg_*.json'):
                    self.process_chat_message(msg_file)
                
                # Small delay to prevent CPU spinning
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error in monitor loop: {e}")
    
    def process_chat_message(self, msg_file: Path):
        """Process a single chat message"""
        try:
            # Read the message
            with open(msg_file, 'r') as f:
                data = json.load(f)
            
            # Create a Message object for the bus
            message = Message(
                sender='web_chat',
                recipient='broadcast',  # Broadcast to all agents
                content={
                    'type': 'chat_message',
                    'user_id': data['user_id'],
                    'room_id': data['room_id'],
                    'message': data['message'],
                    'timestamp': data['timestamp']
                },
                metadata={
                    'source': 'web_chat',
                    'priority': 'normal',
                    'requires_response': True
                }
            )
            
            # Set topic for pub-sub
            message.set_topic('chat.message')
            
            # Send through message bus
            self.message_bus.send(message)
            
            print(f"📨 Routed chat message to agents: {data['message'][:50]}...")
            
            # Move processed file
            processed_file = PROCESSED_DIR / f"chat_{msg_file.name}"
            msg_file.rename(processed_file)
            
        except Exception as e:
            print(f"Error processing message {msg_file}: {e}")
    
    def send_agent_response(self, agent_name: str, response: str, room_id: str):
        """Send agent response back to chat"""
        response_data = {
            'timestamp': datetime.now().isoformat(),
            'agent': agent_name,
            'room_id': room_id,
            'response': response,
            'type': 'agent_response'
        }
        
        response_file = AGENT_RESPONSE_DIR / f"resp_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        with open(response_file, 'w') as f:
            json.dump(response_data, f, indent=2)
        
        print(f"🤖 {agent_name} responded: {response[:50]}...")

def main():
    """Main entry point"""
    bridge = ChatAgentBridge()
    bridge.start()

if __name__ == '__main__':
    main()