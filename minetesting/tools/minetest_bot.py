#!/usr/bin/env python3
"""
Minetest Autonomous Bot
A command-driven bot that controls the main player perspective for autonomous gameplay.

Usage:
    from minetest_bot import MinetestBot

    bot = MinetestBot()

    # Perception
    bot.look()  # Take screenshot and return path

    # Movement
    bot.move_forward(duration=2)
    bot.move_backward(duration=1)
    bot.turn_left(duration=0.5)
    bot.jump()

    # Commands
    bot.execute_command('/energy')
    bot.execute_command('/ai_spawn Alice')

    # Interaction
    bot.talk('Alice', 'come see this cool plot')

    # High-level actions
    bot.create_plot('myplot', size=10)
    bot.spawn_ai('Bob')
"""

import sys
import os
import time
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))
from autonomous_control import DesktopController


class MinetestBot:
    """Autonomous bot for controlling Minetest player"""

    def __init__(self):
        self.controller = DesktopController()
        self.state = {
            'energy': None,
            'position': None,
            'last_screenshot': None,
            'spawned_ais': [],
            'plots': []
        }
        print("🤖 MinetestBot initialized!")

    # ========== PERCEPTION ==========

    def look(self, save_to_state=True):
        """
        Take a screenshot of current view.
        Returns: path to screenshot file
        """
        screenshot_path = self.controller.take_screenshot()
        if save_to_state:
            self.state['last_screenshot'] = screenshot_path
        print(f"👀 Screenshot captured: {screenshot_path}")
        return screenshot_path

    def check_chat(self):
        """
        Take screenshot and return it for vision analysis of chat.
        You can then use Claude's vision to read chat messages.
        """
        return self.look(save_to_state=False)

    # ========== MOVEMENT ==========

    def move_forward(self, duration=1.0):
        """Move forward for specified duration (seconds)"""
        print(f"🏃 Moving forward for {duration}s...")
        self.controller.keyboard_press('w')
        time.sleep(duration)
        # Release key (press something neutral)
        self.controller.keyboard_press('ESC')
        time.sleep(0.1)
        self.controller.keyboard_press('ESC')  # Cancel any menu that opened

    def move_backward(self, duration=1.0):
        """Move backward for specified duration"""
        print(f"🏃 Moving backward for {duration}s...")
        self.controller.keyboard_press('s')
        time.sleep(duration)
        self.controller.keyboard_press('ESC')
        time.sleep(0.1)
        self.controller.keyboard_press('ESC')

    def strafe_left(self, duration=1.0):
        """Strafe left for specified duration"""
        print(f"🏃 Strafing left for {duration}s...")
        self.controller.keyboard_press('a')
        time.sleep(duration)
        self.controller.keyboard_press('ESC')
        time.sleep(0.1)
        self.controller.keyboard_press('ESC')

    def strafe_right(self, duration=1.0):
        """Strafe right for specified duration"""
        print(f"🏃 Strafing right for {duration}s...")
        self.controller.keyboard_press('d')
        time.sleep(duration)
        self.controller.keyboard_press('ESC')
        time.sleep(0.1)
        self.controller.keyboard_press('ESC')

    def jump(self):
        """Jump once"""
        print("🦘 Jumping...")
        self.controller.keyboard_press('SPACE')
        time.sleep(0.3)

    def fly_up(self, duration=1.0):
        """Fly upward (requires fly privilege)"""
        print(f"🚀 Flying up for {duration}s...")
        # In Minetest, SPACE while flying goes up
        self.controller.keyboard_press('SPACE')
        time.sleep(duration)
        self.controller.keyboard_press('ESC')

    def fly_down(self, duration=1.0):
        """Fly downward (requires fly privilege)"""
        print(f"⬇️  Flying down for {duration}s...")
        # Shift while flying goes down
        # Note: Might need to hold Shift, this presses it
        self.controller.keyboard_press('SHIFT')
        time.sleep(duration)

    # ========== COMMANDS ==========

    def execute_command(self, command, wait=2.0):
        """
        Execute a chat command (like /energy, /ai_spawn, etc.)

        Args:
            command: Command string (e.g., '/energy' or '/ai_spawn Alice')
            wait: Seconds to wait for command to execute

        Returns: Screenshot path after command execution
        """
        print(f"⚡ Executing command: {command}")

        # Open chat
        self.controller.keyboard_press('F10')
        time.sleep(0.3)

        # Type command
        self.controller.keyboard_type(command)
        time.sleep(0.2)

        # Execute
        self.controller.keyboard_press('ENTER')
        time.sleep(wait)

        # Take screenshot to capture result
        return self.look()

    def get_energy(self):
        """
        Check current energy level.
        Returns screenshot path (use vision to read the number)
        """
        print("🔋 Checking energy...")
        screenshot = self.execute_command('/energy', wait=1.5)
        return screenshot

    def get_points(self, player='singleplayer'):
        """
        Check points for a player.
        Returns screenshot path (use vision to read points)
        """
        print(f"⭐ Checking points for {player}...")
        screenshot = self.execute_command(f'/points {player}', wait=1.5)
        return screenshot

    # ========== HIGH-LEVEL ACTIONS ==========

    def spawn_ai(self, name):
        """
        Spawn an AI entity with given name.

        Args:
            name: Name for the AI (e.g., 'Alice', 'Bob')

        Returns: Screenshot path showing spawn confirmation
        """
        print(f"🤖 Spawning AI: {name}")
        screenshot = self.execute_command(f'/ai_spawn {name}', wait=2.0)
        self.state['spawned_ais'].append(name)
        return screenshot

    def talk(self, target, message):
        """
        Use !talk command to persuade an AI.

        Args:
            target: AI name to talk to
            message: Message to send (use novelty keywords: new, cool, game, event, better)

        Returns: Screenshot path
        """
        print(f"💬 Talking to {target}: {message}")
        screenshot = self.execute_command(f'!talk {target} {message}', wait=2.0)
        return screenshot

    def create_plot(self, plot_name, size=10):
        """
        Create a plot by setting two positions and creating it.

        Args:
            plot_name: Name for the plot
            size: Approximate size in blocks (will move this distance)

        Returns: Screenshot path after plot creation
        """
        print(f"🏗️  Creating plot '{plot_name}' with size ~{size} blocks...")

        # Set position 1
        print("  📍 Setting position 1...")
        self.execute_command('/setpos1', wait=1.0)

        # Move to create plot area
        print(f"  🏃 Moving {size} blocks...")
        self.move_forward(duration=size * 0.5)  # Rough timing: 0.5s per block
        time.sleep(0.5)
        self.strafe_right(duration=size * 0.5)
        time.sleep(0.5)

        # Set position 2
        print("  📍 Setting position 2...")
        self.execute_command('/setpos2', wait=1.0)

        # Create plot
        print(f"  ✅ Creating plot...")
        screenshot = self.execute_command(f'/plot_create {plot_name} singleplayer', wait=2.0)

        self.state['plots'].append(plot_name)
        print(f"✅ Plot '{plot_name}' created!")
        return screenshot

    def grant_self_privileges(self):
        """Grant all privileges to self"""
        print("🔓 Granting all privileges...")
        return self.execute_command('/grantme all', wait=2.0)

    # ========== AUTONOMOUS BEHAVIORS ==========

    def explore(self, duration=10):
        """
        Autonomous exploration: move around randomly and take screenshots.

        Args:
            duration: Seconds to explore

        Returns: List of screenshot paths captured during exploration
        """
        print(f"🗺️  Exploring for {duration} seconds...")
        screenshots = []
        start_time = time.time()

        while time.time() - start_time < duration:
            # Random action
            import random
            action = random.choice([
                ('forward', 2),
                ('backward', 1),
                ('strafe_left', 1),
                ('strafe_right', 1),
                ('jump', 0)
            ])

            if action[0] == 'forward':
                self.move_forward(action[1])
            elif action[0] == 'backward':
                self.move_backward(action[1])
            elif action[0] == 'strafe_left':
                self.strafe_left(action[1])
            elif action[0] == 'strafe_right':
                self.strafe_right(action[1])
            elif action[0] == 'jump':
                self.jump()

            # Take screenshot
            screenshot = self.look()
            screenshots.append(screenshot)

            time.sleep(1)

        print(f"✅ Exploration complete! Captured {len(screenshots)} screenshots")
        return screenshots

    def autonomous_setup(self):
        """
        Autonomous setup routine: grant privileges, check starting state.

        Returns: Dict with energy and screenshots
        """
        print("🚀 Running autonomous setup...")

        results = {
            'screenshots': [],
            'energy': None
        }

        # Grant privileges
        screenshot = self.grant_self_privileges()
        results['screenshots'].append(screenshot)
        time.sleep(1)

        # Check energy
        screenshot = self.get_energy()
        results['screenshots'].append(screenshot)
        results['energy'] = "Use vision to read from screenshot"
        time.sleep(1)

        # Check points
        screenshot = self.get_points()
        results['screenshots'].append(screenshot)

        print("✅ Setup complete!")
        return results

    def autonomous_gameplay_demo(self):
        """
        Full autonomous gameplay demo: setup → create plot → spawn AIs → interact

        Returns: Dict with all results and screenshots
        """
        print("🎮 Starting autonomous gameplay demo...")

        results = {
            'setup': None,
            'plot': None,
            'ai_spawns': [],
            'interactions': [],
            'final_state': None
        }

        # Setup
        print("\n=== PHASE 1: SETUP ===")
        results['setup'] = self.autonomous_setup()
        time.sleep(2)

        # Create plot
        print("\n=== PHASE 2: CREATE PLOT ===")
        results['plot'] = self.create_plot('demo_plot', size=8)
        time.sleep(2)

        # Spawn AIs
        print("\n=== PHASE 3: SPAWN AIS ===")
        for name in ['Alice', 'Bob', 'Charlie']:
            screenshot = self.spawn_ai(name)
            results['ai_spawns'].append({'name': name, 'screenshot': screenshot})
            time.sleep(2)

        # Interact with AIs
        print("\n=== PHASE 4: INTERACT ===")
        messages = [
            ('Alice', 'check out this new cool plot'),
            ('Bob', 'this game is better than ever'),
            ('Charlie', 'come see this cool event')
        ]
        for target, message in messages:
            screenshot = self.talk(target, message)
            results['interactions'].append({'target': target, 'message': message, 'screenshot': screenshot})
            time.sleep(2)

        # Final state check
        print("\n=== PHASE 5: FINAL STATE ===")
        energy_screenshot = self.get_energy()
        points_screenshot = self.get_points()
        results['final_state'] = {
            'energy': energy_screenshot,
            'points': points_screenshot
        }

        print("\n🎉 AUTONOMOUS GAMEPLAY DEMO COMPLETE!")
        print(f"📊 Results:")
        print(f"   - Plots created: {len(self.state['plots'])}")
        print(f"   - AIs spawned: {len(self.state['spawned_ais'])}")
        print(f"   - Interactions: {len(results['interactions'])}")
        print(f"   - Screenshots: {len([s for s in self.state.values() if isinstance(s, str) and 'screenshot' in s])}")

        return results

    # ========== UTILITY ==========

    def wait(self, seconds):
        """Wait for specified seconds"""
        print(f"⏳ Waiting {seconds}s...")
        time.sleep(seconds)

    def get_state(self):
        """Get current bot state"""
        return self.state

    def reset_state(self):
        """Reset bot state"""
        self.state = {
            'energy': None,
            'position': None,
            'last_screenshot': None,
            'spawned_ais': [],
            'plots': []
        }
        print("🔄 Bot state reset")


# ========== DEMO SCRIPT ==========

def demo_bot_commands():
    """Demo script showing bot command usage"""
    print("=" * 60)
    print("🤖 MINETEST BOT DEMO")
    print("=" * 60)

    bot = MinetestBot()

    print("\n--- Basic Commands Demo ---")

    # Look around
    print("\n1. Taking screenshot...")
    screenshot = bot.look()
    print(f"   Screenshot saved: {screenshot}")

    # Check energy
    print("\n2. Checking energy...")
    bot.get_energy()

    # Spawn AI
    print("\n3. Spawning AI...")
    bot.spawn_ai('TestBot')

    # Movement demo
    print("\n4. Movement demo...")
    bot.move_forward(2)
    bot.turn_left(0.5)
    bot.jump()

    print("\n✅ Demo complete!")
    print(f"\nBot state: {bot.get_state()}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        demo_bot_commands()
    elif len(sys.argv) > 1 and sys.argv[1] == 'full-demo':
        bot = MinetestBot()
        results = bot.autonomous_gameplay_demo()
        print("\n📊 Final Results:")
        print(results)
    else:
        print("Minetest Bot - Command Interface")
        print("\nUsage:")
        print("  python3 minetest_bot.py demo          # Run basic demo")
        print("  python3 minetest_bot.py full-demo     # Run full autonomous gameplay")
        print("\nOr import and use in Python:")
        print("  from minetest_bot import MinetestBot")
        print("  bot = MinetestBot()")
        print("  bot.look()  # Take screenshot")
        print("  bot.execute_command('/energy')  # Run command")
