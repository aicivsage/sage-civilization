#!/usr/bin/env python3
"""
Setup and Test Diana's Perception System
Complete workflow: Resume game → Spawn Diana → Test perception
"""

import sys
import os
import json
import time
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent))
from minetest_bot import MinetestBot

def main():
    print("🚀 Setting up Diana Perception Test\n")
    print("="*60)

    bot = MinetestBot()

    # Step 1: Resume game if paused
    print("\n1️⃣ Resuming game...")
    bot.controller.keyboard_press('escape')
    time.sleep(0.5)

    # Step 2: Spawn Diana
    print("\n2️⃣ Spawning Diana...")
    result = bot.spawn_ai('Diana')
    print(f"   Result: {result}")
    time.sleep(1.0)

    # Step 3: Check energy
    print("\n3️⃣ Checking ENERGY...")
    bot.execute_command('/energy', wait=1.5)

    # Step 4: Export Diana's perception
    print("\n4️⃣ Exporting Diana's perception...")
    bot.execute_command('/ai_perception Diana', wait=2.0)

    # Step 5: Check if perception file was created
    print("\n5️⃣ Checking for perception file...")

    # Try to find any ai_perception files in /tmp/
    import glob
    perception_files = glob.glob('/tmp/ai_perception_*.json')

    if perception_files:
        print(f"   ✅ Found {len(perception_files)} perception file(s)!")
        for pf in perception_files:
            print(f"      • {pf}")
            with open(pf, 'r') as f:
                perception = json.load(f)
                print(f"\n📊 Perception Data:")
                print(json.dumps(perception, indent=2))

                print(f"\n🔍 Quick Analysis:")
                print(f"   Entity: {perception.get('name')} ({perception.get('entity_id')})")
                print(f"   Position: {perception.get('position')}")
                print(f"   Boredom: {perception.get('boredom', 0):.2f}")
                print(f"   Nearby Players: {len(perception.get('nearby_players', []))}")
                print(f"   Nearby Plots: {len(perception.get('nearby_plots', []))}")
    else:
        print("   ❌ No perception files found")
        print("\n🔧 Debugging info:")
        print("   Checking game chat output from screenshot...")
        screenshot = bot.look()
        print(f"   Screenshot: {screenshot}")

        # Check server privs
        print("\n   Checking server privileges...")
        bot.execute_command('/privs', wait=1.5)
        bot.look()

    print("\n" + "="*60)
    print("✅ Test complete!")
    print("="*60)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
