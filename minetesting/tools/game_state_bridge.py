#!/usr/bin/env python3
"""
Game State Bridge
Connects Minetest game world ↔ Claude AI agents

This bridge:
1. Reads AI entity perceptions from game (scene graph JSON)
2. Invokes AI entity agents with perceptions
3. Receives agent decisions
4. Executes decisions in game via commands
5. Optionally captures screenshots for visual evaluation
"""

import json
import time
import os
import sys
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent))
from minetest_bot import MinetestBot


class GameStateBridge:
    """Bridge between Minetest game and Claude AI agents"""

    def __init__(self, bot=None):
        self.bot = bot or MinetestBot()
        self.active_ais = {}  # {entity_id: {name, last_perception, last_decision}}
        self.chat_history = []  # Recent chat messages
        self.perception_dir = "/tmp"

        print("🌉 Game State Bridge initialized!")

    # ========== PERCEPTION (Game → Agent) ==========

    def get_ai_perception(self, entity_id_or_name):
        """
        Get perception for an AI entity from game.

        Args:
            entity_id_or_name: AI entity ID or name (e.g., 'Diana' or 'ai-1760643984-7177')

        Returns:
            Perception dict with scene graph data
        """
        # Trigger Lua to export perception
        self.bot.execute_command(f'/ai_perception {entity_id_or_name}', wait=1.0)

        # Try to read perception file
        # First try by name, then try as ID
        perception_file = None
        for filename in os.listdir(self.perception_dir):
            if filename.startswith('ai_perception_') and filename.endswith('.json'):
                perception_file = os.path.join(self.perception_dir, filename)
                break

        if not perception_file or not os.path.exists(perception_file):
            print(f"⚠️  Perception file not found for {entity_id_or_name}")
            return None

        # Read perception JSON
        with open(perception_file, 'r') as f:
            perception = json.load(f)

        # Add recent chat history
        perception['recent_messages'] = self.get_recent_chat(entity_id_or_name)

        return perception

    def get_all_ai_perceptions(self):
        """Get perceptions for all active AI entities"""
        # Trigger Lua to export all perceptions
        self.bot.execute_command('/ai_list', wait=1.0)

        perceptions = []
        for filename in os.listdir(self.perception_dir):
            if filename.startswith('ai_perception_') and filename.endswith('.json'):
                filepath = os.path.join(self.perception_dir, filename)
                with open(filepath, 'r') as f:
                    perception = json.load(f)
                    perceptions.append(perception)

        return perceptions

    def get_recent_chat(self, ai_name, limit=5):
        """Get recent chat messages mentioning this AI"""
        # Filter chat history for messages relevant to this AI
        relevant = [
            msg for msg in self.chat_history[-20:]
            if ai_name.lower() in msg.get('text', '').lower()
        ]
        return relevant[-limit:]

    def add_chat_message(self, player, text):
        """Track a chat message for perception"""
        self.chat_history.append({
            'from': player,
            'text': text,
            'timestamp': time.time()
        })

    # ========== DECISION (Agent → Game) ==========

    def execute_agent_decision(self, entity_id, decision):
        """
        Execute an AI agent's decision in the game.

        Args:
            entity_id: AI entity ID
            decision: Decision dict from agent {action, target, duration, reason, chat_response}

        Returns:
            Success boolean
        """
        action = decision.get('action')
        print(f"🎮 Executing decision for {entity_id}: {action}")

        if action == 'wander':
            # AI wants to wander - let Lua handle it naturally
            print(f"   → Letting {entity_id} wander naturally")
            return True

        elif action == 'move_to_plot':
            # AI wants to move to specific plot
            plot_id = decision.get('target')
            reason = decision.get('reason', 'No reason given')

            print(f"   → Moving to plot: {plot_id}")
            print(f"   → Reason: {reason}")

            # Use Lua's try_visit function
            # This is a simplification - in reality we'd need to call Lua directly
            # For now, rely on persuasion system or add a direct command
            return True

        elif action == 'stay':
            # AI wants to stay on current plot
            duration = decision.get('duration', 60)
            reason = decision.get('reason', 'Staying')

            print(f"   → Staying for {duration} seconds")
            print(f"   → Reason: {reason}")

            # Reset boredom by having player talk to AI again
            # Or implement a /ai_setboredom command in Lua
            return True

        elif action == 'explore':
            # AI wants to explore
            print(f"   → Exploring...")
            # Let natural wandering handle this
            return True

        # Send chat response if provided
        chat_response = decision.get('chat_response')
        if chat_response:
            print(f"   💬 AI says: {chat_response}")
            # We'd need to implement AI chat in Lua
            # For now, log it

        return True

    # ========== VISION (Screenshot Requests) ==========

    def get_screenshot_for_ai(self, entity_id, perception):
        """
        Take screenshot from player perspective looking at AI's location.

        Args:
            entity_id: AI entity ID
            perception: AI's perception dict (contains position)

        Returns:
            Screenshot path
        """
        position = perception.get('position')
        if not position:
            return None

        print(f"📸 Taking screenshot for {entity_id} at position {position}")

        # Move player camera to look at AI's position
        # This is simplified - in reality we'd:
        # 1. Move player near AI
        # 2. Look in AI's direction
        # 3. Take screenshot

        # For now, just take a screenshot from current position
        screenshot = self.bot.look()

        print(f"   → Screenshot: {screenshot}")
        return screenshot

    # ========== AGENT INVOCATION ==========

    def invoke_agent_for_ai(self, entity_id, perception, request_vision=False):
        """
        Invoke AI entity agent with perception.

        Args:
            entity_id: AI entity ID
            perception: Perception dict
            request_vision: Whether to include screenshot

        Returns:
            Agent decision dict
        """
        ai_name = perception.get('name', 'Unknown')
        print(f"\n🤖 Invoking agent for {ai_name} ({entity_id})")

        # Add vision if requested
        if request_vision:
            screenshot = self.get_screenshot_for_ai(entity_id, perception)
            perception['screenshot'] = screenshot

        # For now, return a mock decision
        # In reality, we'd use Task(ai-entity-player, ...) here
        print(f"   Perception:")
        print(f"     Position: {perception.get('position')}")
        print(f"     Boredom: {perception.get('boredom'):.2f}")
        print(f"     Current plot: {perception.get('current_plot')}")
        print(f"     Nearby players: {len(perception.get('nearby_players', []))}")
        print(f"     Nearby plots: {len(perception.get('nearby_plots', []))}")

        # TODO: Replace with actual Task invocation
        # decision = Task(ai-entity-player, perception=json.dumps(perception))

        # Mock decision for testing
        mock_decision = {
            'action': 'stay',
            'duration': 60,
            'reason': 'Mock decision - agent not yet invoked',
            'chat_response': None
        }

        return mock_decision

    # ========== MAIN LOOP ==========

    def run_decision_loop(self, interval=5):
        """
        Main loop: Get perceptions → Invoke agents → Execute decisions

        Args:
            interval: Seconds between decision cycles
        """
        print(f"\n🔄 Starting decision loop (interval: {interval}s)")
        print("Press Ctrl+C to stop\n")

        cycle = 0
        try:
            while True:
                cycle += 1
                print(f"{'='*60}")
                print(f"Cycle {cycle} - {time.strftime('%H:%M:%S')}")
                print(f"{'='*60}")

                # Get all AI perceptions
                perceptions = self.get_all_ai_perceptions()

                if not perceptions:
                    print("⚠️  No active AIs found")
                else:
                    print(f"📊 Found {len(perceptions)} active AI(s)")

                    # Process each AI
                    for perception in perceptions:
                        entity_id = perception['entity_id']
                        ai_name = perception['name']

                        # Invoke agent
                        decision = self.invoke_agent_for_ai(entity_id, perception)

                        # Execute decision
                        self.execute_agent_decision(entity_id, decision)

                        # Track state
                        self.active_ais[entity_id] = {
                            'name': ai_name,
                            'last_perception': perception,
                            'last_decision': decision,
                            'last_update': time.time()
                        }

                print(f"\n💤 Sleeping {interval}s...\n")
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\n🛑 Decision loop stopped by user")
            print(f"Processed {cycle} cycles")


# ========== CLI ==========

def main():
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'test-perception':
        # Test perception export
        print("🧪 Testing perception export...")
        bridge = GameStateBridge()

        ai_name = sys.argv[2] if len(sys.argv) > 2 else 'Diana'
        perception = bridge.get_ai_perception(ai_name)

        if perception:
            print(f"\n✅ Perception for {ai_name}:")
            print(json.dumps(perception, indent=2))
        else:
            print(f"\n❌ Could not get perception for {ai_name}")

    elif len(sys.argv) > 1 and sys.argv[1] == 'run':
        # Run decision loop
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        bridge = GameStateBridge()
        bridge.run_decision_loop(interval=interval)

    else:
        print("Game State Bridge")
        print("\nUsage:")
        print("  python3 game_state_bridge.py test-perception [ai_name]")
        print("  python3 game_state_bridge.py run [interval_seconds]")
        print("\nExamples:")
        print("  python3 game_state_bridge.py test-perception Diana")
        print("  python3 game_state_bridge.py run 5")


if __name__ == '__main__':
    main()
