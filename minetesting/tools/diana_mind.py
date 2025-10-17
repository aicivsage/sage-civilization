#!/usr/bin/env python3
"""
Diana's Mind - AI Agent Decision Layer
Connects to orchestrator, receives perceptions, makes decisions via Task(ai-entity-player)
"""

import sys
import os
import json
import time
import requests
from pathlib import Path
from datetime import datetime

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent))

ORCHESTRATOR_URL = "http://127.0.0.1:8787"

class DianaMind:
    """Diana's decision-making layer"""

    def __init__(self, ai_id=None, ai_name="Diana"):
        self.ai_id = ai_id
        self.ai_name = ai_name
        self.memory = {
            "experiences": [],
            "favorite_plots": {},
            "player_relationships": {}
        }

    def get_latest_perception(self):
        """Get Diana's latest perception from orchestrator"""
        try:
            response = requests.get(f"{ORCHESTRATOR_URL}/perceptions")
            data = response.json()

            # Find Diana's perception
            for perception in data.get('perceptions', []):
                if perception.get('name') == self.ai_name:
                    self.ai_id = perception.get('entity_id')
                    return perception

            return None

        except Exception as e:
            print(f"❌ Error fetching perception: {e}")
            return None

    def make_decision(self, perception):
        """
        Make decision based on perception.
        TODO: Replace with actual Task(ai-entity-player) invocation
        """

        # Extract context
        boredom = perception.get('boredom', 0.0)
        current_plot = perception.get('current_plot')
        nearby_players = perception.get('nearby_players', [])
        nearby_plots = perception.get('nearby_plots', [])
        nearby_signs = perception.get('nearby_signs', [])
        dwelling_time = perception.get('dwelling_time', 0)

        # Decision logic (simplified - will be replaced with Task invocation)

        # High boredom → explore
        if boredom > 0.8 and nearby_plots:
            # Find most interesting plot
            best_plot = self._find_interesting_plot(nearby_plots, nearby_signs)
            if best_plot:
                return {
                    "action": "move_to_plot",
                    "target": best_plot['id'],
                    "reason": f"High boredom ({boredom:.2f}), exploring {best_plot['name']}",
                    "chat_response": f"This looks interesting! I'll check out {best_plot['name']}. ✨"
                }

        # Found interesting signs → stay and explore
        if nearby_signs and boredom < 0.5:
            sign_text = " | ".join([s['text'][:30] for s in nearby_signs[:2]])
            return {
                "action": "stay",
                "duration": 60,
                "reason": f"Interesting signs found: {sign_text}",
                "chat_response": f"Ooh, I see: '{nearby_signs[0]['text'][:50]}...' Let me stay a bit!"
            }

        # Player nearby and not bored → be social
        if nearby_players and boredom < 0.6:
            player = nearby_players[0]
            return {
                "action": "stay",
                "duration": 30,
                "reason": f"Player {player['name']} is {player['distance']} blocks away",
                "chat_response": f"Hi {player['name']}! Nice to see you here!"
            }

        # Been here a while and getting bored → wander
        if dwelling_time > 120 and boredom > 0.5:
            return {
                "action": "wander",
                "reason": f"Dwelling for {dwelling_time:.0f}s, boredom {boredom:.2f}",
                "chat_response": "I think I'll explore a bit..."
            }

        # Default: stay where you are
        return {
            "action": "stay",
            "duration": 30,
            "reason": "Content for now",
            "chat_response": None
        }

    def _find_interesting_plot(self, nearby_plots, nearby_signs):
        """Find most interesting plot based on distance and signs"""
        if not nearby_plots:
            return None

        # Prefer open plots
        open_plots = [p for p in nearby_plots if p.get('tax_open')]
        if not open_plots:
            open_plots = nearby_plots

        # Prefer closer plots
        sorted_plots = sorted(open_plots, key=lambda p: p.get('distance', 999))

        # Bonus for plots with signs nearby (indicates content)
        if nearby_signs:
            sign_plot_ids = set()
            for plot in sorted_plots:
                for sign in nearby_signs:
                    sign_pos = sign.get('pos', {})
                    # Rough proximity check
                    if sign.get('distance', 999) < 20:
                        sign_plot_ids.add(plot['id'])

            # Prefer plots with signs
            for plot in sorted_plots:
                if plot['id'] in sign_plot_ids:
                    return plot

        return sorted_plots[0] if sorted_plots else None

    def send_decision(self, decision):
        """Send decision to orchestrator"""
        if not self.ai_id:
            print("⚠️  No AI ID yet")
            return False

        try:
            response = requests.post(
                f"{ORCHESTRATOR_URL}/command/{self.ai_id}",
                json=decision
            )
            return response.json().get('status') == 'queued'

        except Exception as e:
            print(f"❌ Error sending decision: {e}")
            return False

    def remember_experience(self, perception, decision, outcome):
        """Store experience for learning"""
        experience = {
            "timestamp": datetime.now().isoformat(),
            "perception_summary": {
                "boredom": perception.get('boredom'),
                "plot": perception.get('current_plot', {}).get('name'),
                "nearby_players": len(perception.get('nearby_players', [])),
                "nearby_signs": len(perception.get('nearby_signs', []))
            },
            "decision": decision.get('action'),
            "reason": decision.get('reason'),
            "outcome": outcome
        }

        self.memory['experiences'].append(experience)

        # Limit memory size
        if len(self.memory['experiences']) > 100:
            self.memory['experiences'] = self.memory['experiences'][-100:]

    def run_forever(self, interval=5):
        """Main decision loop"""
        print(f"\n🧠 Diana's Mind starting...")
        print(f"   Decision interval: {interval}s")
        print(f"   Orchestrator: {ORCHESTRATOR_URL}")
        print(f"   Press Ctrl+C to stop\n")

        cycle = 0
        try:
            while True:
                cycle += 1
                print(f"{'='*60}")
                print(f"💭 Decision Cycle {cycle} - {datetime.now().strftime('%H:%M:%S')}")
                print(f"{'='*60}")

                # Get perception
                perception = self.get_latest_perception()

                if not perception:
                    print("⚠️  No perception found")
                    time.sleep(interval)
                    continue

                # Display perception
                print(f"\n📊 Perception:")
                print(f"   Position: {perception.get('position')}")
                print(f"   Boredom: {perception.get('boredom', 0):.2f}")
                print(f"   Dwelling: {perception.get('dwelling_time', 0):.0f}s")
                print(f"   Current plot: {perception.get('current_plot', {}).get('name', 'None')}")
                print(f"   Nearby players: {len(perception.get('nearby_players', []))}")
                print(f"   Nearby plots: {len(perception.get('nearby_plots', []))}")
                print(f"   Nearby signs: {len(perception.get('nearby_signs', []))}")

                # Make decision
                decision = self.make_decision(perception)

                print(f"\n🎯 Decision:")
                print(f"   Action: {decision.get('action')}")
                print(f"   Reason: {decision.get('reason')}")
                if decision.get('chat_response'):
                    print(f"   💬 Chat: {decision.get('chat_response')}")

                # Send decision
                success = self.send_decision(decision)
                if success:
                    print(f"   ✅ Command queued")
                else:
                    print(f"   ❌ Command failed")

                # Remember experience
                self.remember_experience(perception, decision, "pending")

                print(f"\n💤 Sleeping {interval}s...\n")
                time.sleep(interval)

        except KeyboardInterrupt:
            print(f"\n\n🛑 Diana's Mind stopped by user")
            print(f"   Processed {cycle} cycles")
            print(f"   Stored {len(self.memory['experiences'])} experiences")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Test single decision cycle
        diana = DianaMind()
        perception = diana.get_latest_perception()

        if perception:
            print("✅ Perception received:")
            print(json.dumps(perception, indent=2))

            decision = diana.make_decision(perception)
            print("\n✅ Decision made:")
            print(json.dumps(decision, indent=2))

            success = diana.send_decision(decision)
            print(f"\n{'✅' if success else '❌'} Decision sent: {success}")
        else:
            print("❌ No perception found - is orchestrator running? Is Diana spawned?")

    else:
        # Run forever
        diana = DianaMind()
        diana.run_forever(interval=5)

if __name__ == '__main__':
    main()
