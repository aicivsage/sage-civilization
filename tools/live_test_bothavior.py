#!/usr/bin/env python3
"""
Live BOTHAVIOR System Test
Full integration test with Minetest
"""

import sys
import os
import time
import json
import requests
from pathlib import Path
import subprocess

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent))
from autonomous_control import DesktopController

ORCHESTRATOR_URL = "http://127.0.0.1:8787"

class LiveTester:
    def __init__(self):
        self.controller = DesktopController()
        self.test_log = []

    def log(self, message, level="INFO"):
        """Log test message"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        self.test_log.append(log_entry)

    def take_screenshot(self, name="test"):
        """Take and save screenshot"""
        try:
            screenshot = self.controller.take_screenshot()
            self.log(f"Screenshot saved: {screenshot}")
            return screenshot
        except Exception as e:
            self.log(f"Screenshot failed: {e}", "ERROR")
            return None

    def check_orchestrator(self):
        """Verify orchestrator is running"""
        self.log("Checking orchestrator health...")
        try:
            response = requests.get(f"{ORCHESTRATOR_URL}/health", timeout=5)
            if response.status_code == 200:
                self.log("✅ Orchestrator HEALTHY", "SUCCESS")
                return True
            else:
                self.log(f"❌ Orchestrator returned {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Orchestrator not responding: {e}", "ERROR")
            return False

    def get_orchestrator_status(self):
        """Get orchestrator status"""
        try:
            response = requests.get(f"{ORCHESTRATOR_URL}/status", timeout=5)
            status = response.json()
            self.log(f"Orchestrator status: {json.dumps(status)}")
            return status
        except Exception as e:
            self.log(f"Failed to get status: {e}", "ERROR")
            return None

    def get_perceptions(self):
        """Get all perceptions from orchestrator"""
        try:
            response = requests.get(f"{ORCHESTRATOR_URL}/perceptions", timeout=5)
            data = response.json()
            count = data.get('count', 0)
            self.log(f"📊 Active AIs: {count}")
            return data.get('perceptions', [])
        except Exception as e:
            self.log(f"Failed to get perceptions: {e}", "ERROR")
            return []

    def get_events(self, limit=10):
        """Get recent events"""
        try:
            response = requests.get(f"{ORCHESTRATOR_URL}/events", timeout=5)
            data = response.json()
            events = data.get('events', [])
            self.log(f"📝 Recent events: {len(events)}")
            for event in events[-limit:]:
                self.log(f"   {event['type']}: {event['data']}")
            return events
        except Exception as e:
            self.log(f"Failed to get events: {e}", "ERROR")
            return []

    def check_minetest_running(self):
        """Check if Minetest is running"""
        try:
            result = subprocess.run(['pgrep', '-f', 'minetest'],
                                  capture_output=True, text=True)
            if result.stdout.strip():
                self.log("✅ Minetest is running", "SUCCESS")
                return True
            else:
                self.log("❌ Minetest not running", "WARNING")
                return False
        except Exception as e:
            self.log(f"Failed to check Minetest: {e}", "ERROR")
            return False

    def wait_for_perception(self, timeout=30):
        """Wait for first perception to arrive"""
        self.log(f"⏳ Waiting for Diana's perception (timeout: {timeout}s)...")
        start = time.time()

        while time.time() - start < timeout:
            perceptions = self.get_perceptions()
            if perceptions:
                self.log("✅ Perception received!", "SUCCESS")
                perception = perceptions[0]
                self.log(f"   AI: {perception.get('name')} ({perception.get('entity_id')})")
                self.log(f"   Position: {perception.get('position')}")
                self.log(f"   Boredom: {perception.get('boredom', 0):.2f}")
                self.log(f"   Nearby players: {len(perception.get('nearby_players', []))}")
                self.log(f"   Nearby plots: {len(perception.get('nearby_plots', []))}")
                self.log(f"   Nearby signs: {len(perception.get('nearby_signs', []))}")
                return perception

            time.sleep(2)

        self.log("❌ No perception received within timeout", "ERROR")
        return None

    def monitor_loop(self, duration=60, interval=10):
        """Monitor the perception → decision → execution loop"""
        self.log(f"\n{'='*60}")
        self.log(f"🔄 Monitoring loop for {duration}s (checking every {interval}s)")
        self.log(f"{'='*60}\n")

        start = time.time()
        cycle = 0

        while time.time() - start < duration:
            cycle += 1
            self.log(f"\n--- Cycle {cycle} ---")

            # Get status
            status = self.get_orchestrator_status()

            # Get perceptions
            perceptions = self.get_perceptions()

            # Get events
            events = self.get_events(limit=5)

            # Take screenshot
            self.take_screenshot(f"cycle_{cycle}")

            time.sleep(interval)

        self.log(f"\n✅ Monitoring complete: {cycle} cycles")

    def run_full_test(self):
        """Run complete integration test"""
        self.log("\n" + "="*60)
        self.log("🚀 BOTHAVIOR LIVE TESTING SESSION")
        self.log("="*60 + "\n")

        # Phase 1: Check orchestrator
        self.log("📋 Phase 1: Orchestrator Check")
        if not self.check_orchestrator():
            self.log("❌ Orchestrator not running - please start it first", "ERROR")
            return False

        self.get_orchestrator_status()
        self.log("✅ Phase 1 complete\n")

        # Phase 2: Check Minetest
        self.log("📋 Phase 2: Minetest Check")
        minetest_running = self.check_minetest_running()
        if not minetest_running:
            self.log("⚠️  Minetest not running - manual start required", "WARNING")
            self.log("   Please start Minetest and spawn Diana manually")

        # Take initial screenshot
        self.log("\n📸 Taking initial screenshot...")
        self.take_screenshot("initial")
        self.log("✅ Phase 2 complete\n")

        # Phase 3: Wait for Diana
        self.log("📋 Phase 3: Waiting for Diana's Perception")
        perception = self.wait_for_perception(timeout=60)

        if not perception:
            self.log("❌ No perception received - Diana may not be spawned", "ERROR")
            self.log("   Manual steps required:")
            self.log("   1. Start Minetest")
            self.log("   2. Load world with bothavior_simple mod")
            self.log("   3. Run: /grantme all")
            self.log("   4. Run: /ai_spawn Diana")
            return False

        self.log("✅ Phase 3 complete\n")

        # Phase 4: Monitor loop
        self.log("📋 Phase 4: Monitor Autonomous Loop")
        self.monitor_loop(duration=60, interval=10)
        self.log("✅ Phase 4 complete\n")

        # Phase 5: Final analysis
        self.log("📋 Phase 5: Final Analysis")
        self.log("\nFinal status:")
        final_status = self.get_orchestrator_status()

        self.log("\nFinal events:")
        final_events = self.get_events(limit=20)

        self.log("\n" + "="*60)
        self.log("✅ LIVE TESTING COMPLETE")
        self.log("="*60)

        return True

    def save_test_log(self, filename="test_log.txt"):
        """Save test log to file"""
        with open(filename, 'w') as f:
            f.write('\n'.join(self.test_log))
        self.log(f"📝 Test log saved to: {filename}")

def main():
    tester = LiveTester()

    try:
        success = tester.run_full_test()
        tester.save_test_log("logs/live_test_log.txt")

        if success:
            print("\n✅ All tests passed!")
            return 0
        else:
            print("\n⚠️  Tests completed with warnings")
            return 1

    except KeyboardInterrupt:
        print("\n\n🛑 Test interrupted by user")
        tester.save_test_log("logs/live_test_log_interrupted.txt")
        return 2

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        tester.save_test_log("logs/live_test_log_error.txt")
        return 3

if __name__ == '__main__':
    sys.exit(main())
