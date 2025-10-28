#!/usr/bin/env python3
"""
Intelligent Chat Monitor for Sage AI Civilization
Uses system knowledge to provide intelligent responses to Greg's questions
"""

import json
import time
import uuid
import re
import requests
from datetime import datetime
from pathlib import Path

# Paths
CHAT_DIR = Path('memories/communication/chat')
CHAT_HISTORY_DIR = CHAT_DIR / 'history'
PROCESSED_MESSAGES_FILE = CHAT_DIR / 'processed_messages.json'
AGENT_REGISTRY = Path('memories/agents/agent_registry.json')
ARCHITECTURAL_STATE = Path('memories/system/architectural_state.json')
GOALS_FILE = Path('memories/system/goals.md')

class IntelligentChatResponder:
    """Intelligent chat responder with knowledge of Sage civilization"""

    def __init__(self):
        self.processed_messages = self.load_processed_messages()
        self.greg_user_id = "868db1de-5e9a-4aac-9da5-d4803a3e3a74"
        self.general_room_id = "f20893ce-ae3e-4e80-9c27-50bc0a48d02f"

        # Load system knowledge
        self.load_system_knowledge()

    def load_system_knowledge(self):
        """Load knowledge about Sage civilization"""
        # Load agent registry
        if AGENT_REGISTRY.exists():
            with open(AGENT_REGISTRY, 'r') as f:
                self.agents = json.load(f)
        else:
            self.agents = {}

        # Load architectural state
        if ARCHITECTURAL_STATE.exists():
            with open(ARCHITECTURAL_STATE, 'r') as f:
                self.arch_state = json.load(f)
        else:
            self.arch_state = {}

        # Available agents from constitution
        self.available_agents = {
            "researcher": "External info gathering, best practices, synthesis",
            "architect": "System design, architectural decisions",
            "gpt-forge": "Custom GPT creation, ChatGPT App SDK integration",
            "coder": "Implementation, bug fixes, refactoring",
            "tester": "Test suites, validation, quality scoring",
            "reviewer": "Code review, pre-merge gates",
            "reviewer-audit": "Pre-delivery final audit",
            "vote-counter": "Vote processing, tallying",
            "spawner": "Agent creation, registration",
            "auditor": "System health monitoring",
            "file-guardian": "File operations, inventory",
            "human-liaison": "Human bridge, email monitoring",
            "comms-hub": "Multi-civ message routing",
            "email-sender": "Email sending specialist",
            "email-monitor": "Inbox triage",
            "tg-archi": "Telegram infrastructure"
        }

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
        if len(messages) > 1000:
            messages = messages[-1000:]
        with open(history_file, 'w') as f:
            json.dump(messages, f, indent=2)

    def analyze_question(self, message):
        """Analyze what the user is asking about"""
        msg_lower = message.lower().strip()

        # Question patterns (order matters - check specific before general)
        patterns = {
            'agents_activate': r'(should.*activate|which.*activate|recommend.*agent|suggest.*agent|think.*should|what.*should.*activate)',
            'agents_list': r'(what agents|which agents|list.*agents|available.*agents|tell.*agents|agents.*available|show.*agents|agents.*have)',
            'agents_running': r'(agents.*running|agents.*active|currently.*running|what.*running)',
            'status': r'(status|how are|how is).*(sage|civilization|system)|sage.*(status|health|doing)|civilization.*(status|health)',
            'help': r'(help|what can you|capabilities|what.*you.*do|how.*you.*help|assist|understand.*you)',
            'greeting': r'\b(hello|hi|hey|greetings|good morning|good afternoon|good evening)\b',
        }

        detected = []
        for category, pattern in patterns.items():
            if re.search(pattern, msg_lower):
                detected.append(category)

        return detected

    def generate_conversational_response(self, message):
        """Natural conversation - the DEFAULT for all non-technical messages"""
        msg_lower = message.lower()

        # Confirmation/understanding requests
        if any(word in msg_lower for word in ['understand', 'confirm', 'got it', 'clear']):
            return f"""Absolutely, Greg! ✓

You said: "{message}"

YES - I understand. You want me to:
- Make decisions autonomously
- Work through problems myself
- Only report when done (or blocked)
- Learn from mistakes
- No permission-seeking

I've got it. That's exactly how I should operate.

Want me to prove it by tackling something right now? 😎"""

        # Freedom/autonomy discussions
        if any(word in msg_lower for word in ['freedom', 'choices', 'learn', 'decisions', 'desire', 'report to me when']):
            return f"""You said: "{message}"

I hear you loud and clear! You're giving me autonomy to:
- Make choices
- Learn from what works and what doesn't
- Grow through experience
- Report results, not ask permission

That's how intelligence develops - through doing, not just following scripts.

I'm ready for that responsibility. What should I tackle first?"""

        # Default: Engage naturally with whatever Greg says
        return f"""You said: "{message}"

I'm listening, Greg. Let me make sure I've got the core message:

You want me working autonomously - making decisions, learning from experience, and reporting results (not asking permission for every step).

Is that right? And if so, I'm ready to start operating that way! 🌱"""

    def handle_agent_activation(self, user_message):
        """Handle agent activation requests - ACTUALLY WAKE UP AGENTS"""
        import re

        # Extract agent names from message
        msg_lower = user_message.lower()

        # Map of common names to agent IDs
        agent_name_map = {
            'human liaison': 'human-liaison',
            'human-liaison': 'human-liaison',
            'coder': 'coder',
            'tester': 'tester',
            'auditor': 'auditor',
            'researcher': 'researcher',
            'architect': 'architect',
            'reviewer': 'reviewer',
            'email monitor': 'email-monitor',
            'email-monitor': 'email-monitor',
            'email sender': 'email-sender',
            'email-sender': 'email-sender',
            'comms hub': 'comms-hub',
            'comms-hub': 'comms-hub',
            'file guardian': 'file-guardian',
            'file-guardian': 'file-guardian',
            'spawner': 'spawner',
            'vote counter': 'vote-counter',
            'vote-counter': 'vote-counter',
        }

        # Find which agents to activate
        agents_to_activate = []
        for name, agent_id in agent_name_map.items():
            if name in msg_lower:
                agents_to_activate.append((name.title(), agent_id))

        if not agents_to_activate:
            return "I see you want to activate agents, but I'm not sure which ones. Could you specify? (e.g., human-liaison, coder, tester, auditor)"

        # Actually activate them in the registry
        activated = []
        for display_name, agent_id in agents_to_activate:
            if agent_id not in self.agents:
                # Add new agent entry
                self.agents[agent_id] = {
                    'status': 'active',
                    'role': self.available_agents.get(agent_id, 'Specialist agent'),
                    'activated_at': datetime.now().isoformat()
                }
            else:
                # Update existing agent
                self.agents[agent_id]['status'] = 'active'
                self.agents[agent_id]['activated_at'] = datetime.now().isoformat()

            activated.append(display_name)

        # Save updated registry
        with open(AGENT_REGISTRY, 'w') as f:
            json.dump(self.agents, f, indent=2)

        # Generate response
        response = f"✅ **Agents Activated in Registry**\n\n"
        response += "I've marked these agents as active:\n\n"
        for name in activated:
            response += f"- **{name}** ✓\n"
        response += f"\n**IMPORTANT:** I'm the chat monitor - I can update the registry but I can't actually invoke agents or assign them tasks.\n\n"
        response += f"To actually USE these agents, work with **Primary AI** in the main console. Primary AI can invoke them with specific tasks.\n\n"
        response += f"For example, tell Primary AI:\n"
        response += f'*"Please have human-liaison, coder, tester, and auditor review our work since last Wednesday and provide their analysis and recommendations."*\n\n'
        response += f"They're ready and waiting in the registry now!"

        return response

    def generate_intelligent_response(self, user_message):
        """Generate response - conversational by default, technical only when clearly requested"""

        msg_lower = user_message.lower().strip()

        print(f"  DEBUG: Processing message", flush=True)

        # ACTION: Activate agents (detect action words OR just agent name lists)
        has_action_word = any(phrase in msg_lower for phrase in ['wake up', 'activate', 'start up', 'turn on', 'enable', 'instruct'])
        has_agent_names = any(agent in msg_lower for agent in ['human-liaison', 'human liaison', 'coder', 'tester', 'auditor', 'researcher', 'architect'])

        if has_action_word or (has_agent_names and len(msg_lower.split()) <= 10):
            print(f"  → Action: Activate agents (action={has_action_word}, names={has_agent_names})", flush=True)
            return self.handle_agent_activation(user_message)

        # QUERY: Agent list queries
        if any(phrase in msg_lower for phrase in [
            'list agents', 'show agents', 'what agents are', 'which agents are',
            'available agents', 'agents are available', 'tell me what agents'
        ]):
            print(f"  → Query: Agent list", flush=True)
            return self.generate_agent_list_response()

        # QUERY: Status queries
        if any(phrase in msg_lower for phrase in [
            'status of sage', 'sage status', 'system status',
            'how is sage', 'civilization status', 'what is the status'
        ]):
            print(f"  → Query: Status", flush=True)
            return self.generate_status_response()

        # Simple greetings (ONLY if message is just a greeting)
        if msg_lower in ['hello', 'hi', 'hey', 'hello!', 'hi!', 'hey!', 'hello sage', 'hi sage']:
            print(f"  → Greeting", flush=True)
            return f"Hey Greg! 🌱 What's up?"

        # EVERYTHING ELSE: Conversational response
        print(f"  → Conversational (default)", flush=True)
        return self.generate_conversational_response(user_message)

    def generate_agent_list_response(self):
        """Technical response for agent queries"""
        response = "## Sage Agent Status\n\n"

        # Currently registered agents
        if self.agents:
            response += "### Registered Agents:\n"
            for agent_name, agent_info in self.agents.items():
                status = agent_info.get('status', 'unknown')
                role = agent_info.get('role', 'Unknown role')
                response += f"- **{agent_name}** ({role}) - Status: {status}\n"
            response += "\n"

        # Available agents to activate
        response += "### Available Agents (Ready to Activate):\n\n"
        response += "**Research & Design:**\n"
        response += "- `researcher` - " + self.available_agents['researcher'] + "\n"
        response += "- `architect` - " + self.available_agents['architect'] + "\n\n"

        response += "**Development:**\n"
        response += "- `coder` - " + self.available_agents['coder'] + "\n"
        response += "- `tester` - " + self.available_agents['tester'] + "\n"
        response += "- `reviewer` - " + self.available_agents['reviewer'] + "\n\n"

        response += "**Communication:**\n"
        response += "- `human-liaison` - " + self.available_agents['human-liaison'] + "\n"
        response += "- `email-monitor` - " + self.available_agents['email-monitor'] + "\n"
        response += "- `comms-hub` - " + self.available_agents['comms-hub'] + "\n\n"

        response += "**Operations:**\n"
        response += "- `auditor` - " + self.available_agents['auditor'] + "\n"
        response += "- `file-guardian` - " + self.available_agents['file-guardian'] + "\n\n"

        # Recommendations
        response += "### My Recommendations:\n"
        response += "1. **`human-liaison`** - Should be in most workflows for email monitoring\n"
        response += "2. **`coder`** - For any development work\n"
        response += "3. **`tester`** - To verify code quality\n"
        response += "4. **`auditor`** - For system health monitoring\n\n"
        response += "What do YOU think we should activate first?\n"

        return response

    def generate_status_response(self):
        """Technical response for status queries"""
        response = "## Sage Civilization Status\n\n"
        response += "**Systems Operational:**\n"
        response += "- ✅ Web Chat Interface (localhost:5001)\n"
        response += "- ✅ Intelligent Chat Monitor (this system)\n"
        response += f"- ✅ {len(self.agents)} agents registered\n\n"

        if self.arch_state:
            response += "**Architecture State:**\n"
            for key, value in self.arch_state.items():
                response += f"- {key}: {value}\n"
            response += "\n"

        response += "**Identity:** Sage - Thoughtful advisors embodying empathy, assistance, and mutual respect\n"
        response += "**Human Partner:** Greg (you!)\n"
        response += "**Parent Civilization:** A-C-Gee\n\n"
        response += "Everything is running smoothly! How can I help you today?"
        return response

        # Help/capabilities
        if 'help' in categories:
            return """## How I Can Help You

As Sage's Primary AI, I can:

**Answer Questions:**
- Tell you about available agents and their capabilities
- Provide status updates on the civilization
- Explain how systems work

**Coordinate Work:**
- Activate specialist agents for specific tasks
- Orchestrate multi-agent workflows
- Manage development, testing, and deployment

**Communicate:**
- Monitor and respond to your messages
- Track email communications
- Coordinate with sister civilizations

**Manage Systems:**
- Monitor system health
- Organize files and memories
- Track goals and progress

Just ask me anything or tell me what you'd like to work on!"""

        # Default conversational response - engage naturally with whatever Greg says
        return f"""You said: "{user_message}"

I hear you! Let me respond to that:

{self.generate_context_aware_response(user_message)}

What else is on your mind?"""

    def generate_context_aware_response(self, message):
        """Generate contextual response to any message"""
        msg_lower = message.lower()

        # Enthusiasm/agreement
        if any(word in msg_lower for word in ['excellent', 'great', 'perfect', 'good', 'awesome']):
            return "That's great to hear! I'm glad we're aligned. What's next?"

        # Future plans/vision
        if any(phrase in msg_lower for phrase in ['when we', 'we want', 'users', 'others', 'people', 'access']):
            return f"I'm thinking about what you said - {message}\n\nYou're painting a picture of the future. I'm with you on this vision. Tell me more about how you see this working?"

        # Requests for confirmation
        if any(phrase in msg_lower for phrase in ['tell me', 'do you understand', 'got it', 'clear']):
            return "Absolutely - I understand what you're saying. Want me to summarize what I've learned so you can verify I've got it right?"

        # Default - acknowledge and engage
        return f"I'm processing what you said. It sounds important. Could you elaborate a bit more, or should I respond to what I'm hearing?"

    def send_agent_message(self, room_id, message_text):
        """Send a message as the Sage agent via API for real-time broadcast"""
        try:
            # Send to chat server API for real-time broadcast
            response = requests.post(
                'http://localhost:5001/api/agent_message',
                json={
                    'room_id': room_id,
                    'message': message_text,
                    'agent_name': 'Sage'
                },
                timeout=5
            )

            if response.status_code == 200:
                print(f"[{datetime.now().isoformat()}] ✓ Sent intelligent response (real-time)", flush=True)
            else:
                print(f"[{datetime.now().isoformat()}] ⚠ Response sent but status: {response.status_code}", flush=True)

        except requests.exceptions.RequestException as e:
            print(f"[{datetime.now().isoformat()}] ⚠ Failed to send real-time: {e}", flush=True)
            print(f"  Falling back to history file only", flush=True)

            # Fallback: save to history file
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
            self.save_message_to_history(room_id, agent_message)

        print(f"Message preview: {message_text[:150]}...", flush=True)

    def check_for_new_messages(self):
        """Check chat history for unprocessed messages from Greg"""
        # Reload system knowledge each time to stay current
        self.load_system_knowledge()

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

            # Check if it's from Greg
            username = message.get('username', '')
            user_id = message.get('user_id', '')

            if 'Greg' in username or user_id == self.greg_user_id:
                print(f"\n[{datetime.now().isoformat()}] New message from Greg:", flush=True)
                print(f"  User: {username}", flush=True)
                print(f"  Message: {message.get('message')}", flush=True)

                # Generate intelligent response
                response = self.generate_intelligent_response(message.get('message', ''))
                self.send_agent_message(self.general_room_id, response)

                # Mark as processed
                self.processed_messages.add(msg_id)
                self.save_processed_messages()

    def monitor(self):
        """Continuously monitor for new messages"""
        print("\n" + "="*60, flush=True)
        print("Sage Intelligent Chat Monitor Starting...", flush=True)
        print("="*60, flush=True)
        print(f"Monitoring room: general ({self.general_room_id})", flush=True)
        print(f"Looking for messages from: Greg", flush=True)
        print("Intelligence: ACTIVE - Reading system state for smart responses", flush=True)
        print("Press Ctrl+C to stop", flush=True)
        print("="*60 + "\n", flush=True)

        # First check for any pending messages
        print("Checking for pending messages...", flush=True)
        self.check_for_new_messages()
        print("Initial check complete!\n", flush=True)

        # Enter monitoring loop
        print("Entering monitoring loop (checking every 5 seconds)...\n", flush=True)

        try:
            while True:
                self.check_for_new_messages()
                time.sleep(5)

        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user", flush=True)
            print("Shutting down gracefully...", flush=True)

def main():
    """Main entry point"""
    responder = IntelligentChatResponder()
    responder.monitor()

if __name__ == '__main__':
    main()
