#!/usr/bin/env python3
"""
Demo script for pattern_extractor.py

Shows all major features:
1. Pattern extraction from files
2. Similarity detection
3. Pattern suggestions
4. Recent commit scanning
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, description: str):
    """Run a command and display output."""
    print(f"\n{'='*70}")
    print(f"DEMO: {description}")
    print(f"{'='*70}")
    print(f"Command: {cmd}\n")

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    print()


def main():
    """Run comprehensive demo of pattern extractor."""

    print("\n" + "="*70)
    print("PATTERN EXTRACTOR DEMO")
    print("Automated Pattern Extraction Tool for AI-CIV")
    print("="*70)

    # Demo 1: Extract patterns from specific files
    run_command(
        "python3 tools/pattern_extractor.py "
        "--files 'task-tracker/task_tracker/models.py,task-tracker/task_tracker/storage.py' "
        "--output memories/agents/coder/patterns/demo "
        "--auto-suggest",
        "Extract patterns from task-tracker models and storage"
    )

    # Demo 2: Similarity detection
    run_command(
        "python3 tools/pattern_extractor.py "
        "--similarity 'task-tracker/task_tracker/models.py' "
        "--codebase task-tracker",
        "Find similar code to models.py in task-tracker"
    )

    # Demo 3: Pattern suggestions
    run_command(
        "python3 tools/pattern_extractor.py "
        "--task-description 'Build data model with validation and JSON serialization' "
        "--suggest-from memories/agents/coder/patterns",
        "Suggest patterns for data modeling task"
    )

    # Demo 4: Scan recent commits
    run_command(
        "python3 tools/pattern_extractor.py "
        "--scan-recent-commits 2 "
        "--agent coder",
        "Scan last 2 commits for patterns"
    )

    # Show extracted pattern example
    print("\n" + "="*70)
    print("SAMPLE EXTRACTED PATTERN")
    print("="*70)

    pattern_files = list(Path("memories/agents/coder/patterns/demo/class").glob("*.md"))
    if pattern_files:
        with open(pattern_files[0], 'r') as f:
            print(f.read()[:500] + "...\n")
    else:
        print("No pattern files found in demo directory")

    print("\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70)
    print("\nPattern files saved to: memories/agents/coder/patterns/demo/")
    print("View them with: ls -R memories/agents/coder/patterns/demo/")
    print()


if __name__ == '__main__':
    main()
