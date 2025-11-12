#!/usr/bin/env python3
"""
Autonomous 30-Minute Cycle Script
Runs every 30 minutes via cron to:
1. Check messages from Team 1 and Team 2
2. Review master todo list
3. Execute next priority task OR run a flow
4. Respond to messages
5. Update logs
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import subprocess

# Project paths
PROJECT_ROOT = Path("/mnt/c/Sage/Sage-Civilization")
MASTER_TODO = PROJECT_ROOT / "MASTER_TODO.md"
TEAM1_MESSAGES = PROJECT_ROOT / "team1-messages"
TEAM2_MESSAGES = PROJECT_ROOT / "team2-messages"
CYCLE_LOG = PROJECT_ROOT / "memories" / "autonomous_cycles.jsonl"
TO_COREY = PROJECT_ROOT / "to-corey"

# Ensure directories exist
CYCLE_LOG.parent.mkdir(parents=True, exist_ok=True)
TO_COREY.mkdir(parents=True, exist_ok=True)

def log_cycle(data: dict):
    """Log cycle execution to JSONL file"""
    data["timestamp"] = datetime.now().isoformat()
    with open(CYCLE_LOG, "a") as f:
        f.write(json.dumps(data) + "\n")

def check_new_messages() -> dict:
    """Check for new messages from teams"""
    new_messages = {
        "team1": [],
        "team2": []
    }

    # Check Team 1 messages
    if TEAM1_MESSAGES.exists():
        for file in TEAM1_MESSAGES.glob("to-grow-gemini-*.md"):
            mod_time = datetime.fromtimestamp(file.stat().st_mtime)
            # Check if modified in last hour (to catch messages since last cycle)
            if (datetime.now() - mod_time).total_seconds() < 3600:
                new_messages["team1"].append(str(file))

    # Check Team 2 messages
    if TEAM2_MESSAGES.exists():
        for file in TEAM2_MESSAGES.glob("to-grow-gemini-*.md"):
            mod_time = datetime.fromtimestamp(file.stat().st_mtime)
            if (datetime.now() - mod_time).total_seconds() < 3600:
                new_messages["team2"].append(str(file))

    return new_messages

def build_prompt() -> str:
    """Build the prompt for this cycle"""

    # Check for new messages
    new_messages = check_new_messages()
    has_messages = any(new_messages.values())

    # Build prompt based on what needs attention
    prompt_parts = []

    prompt_parts.append("🤖 AUTONOMOUS CYCLE - 30 Minute Check-in")
    prompt_parts.append("")

    # Priority 1: New messages
    if has_messages:
        prompt_parts.append("📬 NEW MESSAGES DETECTED:")
        if new_messages["team1"]:
            prompt_parts.append(f"  - Team 1: {len(new_messages['team1'])} message(s)")
            for msg in new_messages["team1"]:
                prompt_parts.append(f"    • {Path(msg).name}")
        if new_messages["team2"]:
            prompt_parts.append(f"  - Team 2: {len(new_messages['team2'])} message(s)")
            for msg in new_messages["team2"]:
                prompt_parts.append(f"    • {Path(msg).name}")
        prompt_parts.append("")
        prompt_parts.append("TASK: Read these messages and respond appropriately.")
        prompt_parts.append("")

    # Priority 2: Check master todo list
    prompt_parts.append("📋 INSTRUCTIONS:")
    prompt_parts.append("")

    if has_messages:
        prompt_parts.append("1. Read and respond to all new messages")
        prompt_parts.append("2. Check master todo list for next priority task")
        prompt_parts.append("3. Work on highest priority task OR run a relevant flow")
        prompt_parts.append("4. File brief report in to-corey/ about what was done")
    else:
        prompt_parts.append("1. Review master todo list:")
        prompt_parts.append(f"   cat {MASTER_TODO}")
        prompt_parts.append("")
        prompt_parts.append("2. Choose ONE of:")
        prompt_parts.append("   a) Work on next priority task from master list")
        prompt_parts.append("   b) Run a flow from memories/flows/")
        prompt_parts.append("   c) Check on autonomous agent system status")
        prompt_parts.append("")
        prompt_parts.append("3. File brief progress report in to-corey/")

    prompt_parts.append("")
    prompt_parts.append("📊 CONTEXT:")
    prompt_parts.append("  - Master todo list: /home/corey/projects/AI-CIV/MASTER-MISSION-TODO-LIST.md")
    prompt_parts.append("  - Flows available: memories/flows/*-needs-testing.yaml")
    prompt_parts.append("  - Team 1 messages: team1-production-hub/rooms/partnerships/")
    prompt_parts.append("  - Team 2 messages: ai-civ-comms-hub-team2/external/")
    prompt_parts.append("  - Report to: to-corey/")
    prompt_parts.append("")
    prompt_parts.append("⏱️ Time limit: Work for 15-20 minutes max, then file report.")
    prompt_parts.append("")
    prompt_parts.append("🚀 BEGIN AUTONOMOUS CYCLE NOW!")

    return "\n".join(prompt_parts)

def queue_prompt_for_claude(prompt: str):
    """Write prompt to file for Claude to pick up"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    prompt_file = PROJECT_ROOT / f"autonomous_prompt_{timestamp}.txt"

    with open(prompt_file, "w") as f:
        f.write(prompt)

    return prompt_file

def main():
    """Main autonomous cycle execution"""
    print("=" * 60)
    print("🤖 AUTONOMOUS CYCLE STARTING")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Build prompt
    prompt = build_prompt()
    print("\n📝 Prompt generated:")
    print("-" * 60)
    print(prompt)
    print("-" * 60)

    # Save prompt
    prompt_file = queue_prompt_for_claude(prompt)
    print(f"\n💾 Prompt saved to: {prompt_file}")

    # Log cycle
    log_cycle({
        "status": "prompt_generated",
        "prompt_file": str(prompt_file),
        "prompt_length": len(prompt)
    })

    print("\n✅ Autonomous cycle prepared!")
    print(f"📋 Next: Execute prompt with Claude CLI")
    print(f"💡 To run manually: cd {PROJECT_ROOT} && cat {prompt_file.name}")
    print("\n" + "=" * 60)

    return 0

if __name__ == "__main__":
    sys.exit(main())
