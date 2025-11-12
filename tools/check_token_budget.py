#!/usr/bin/env python3
"""
Token Budget Checker - Fast status checking for Primary AI wake-up and operation planning

Usage:
    python3 tools/check_token_budget.py --wake-up           # Display status for wake-up protocol
    python3 tools/check_token_budget.py --status            # Quick status check
    python3 tools/check_token_budget.py --check-operation <type>  # Check if operation approved
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent.parent
CONFIG_PATH = ROOT_DIR / "memories/system/token_budget_config.json"
STATE_PATH = ROOT_DIR / "memories/system/token_budget_state.json"


def load_json(path):
    """Load JSON file with error handling"""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {path}: {e}", file=sys.stderr)
        sys.exit(1)


def get_alert_level(percentage, config):
    """Determine alert level based on percentage"""
    thresholds = config['alert_thresholds']
    if percentage <= thresholds['green']['max_percentage']:
        return 'green'
    elif percentage <= thresholds['yellow']['max_percentage']:
        return 'yellow'
    else:
        return 'red'


def format_tokens(tokens):
    """Format token count with K suffix"""
    return f"{tokens/1000:.1f}K" if tokens >= 1000 else str(tokens)


def display_wake_up_status():
    """Display comprehensive status for wake-up protocol"""
    config = load_json(CONFIG_PATH)
    state = load_json(STATE_PATH)

    budget = state['budget']
    week = state['current_week']

    # Overall status
    alert_level = get_alert_level(budget['percentage_used'], config)
    emoji = config['alert_thresholds'][alert_level]['emoji']

    print(f"\n{emoji} TOKEN BUDGET STATUS - Week {week['week_number']} ({week['start_date']} to {week['end_date']})")
    print("=" * 70)
    print(f"Overall: {format_tokens(budget['used'])} / {format_tokens(budget['total'])} ({budget['percentage_used']:.1f}%)")
    print(f"Remaining: {format_tokens(budget['remaining'])} tokens")
    print()

    # Category breakdown
    print("Category Breakdown:")
    print("-" * 70)
    for category, usage in state['category_usage'].items():
        cat_alert = get_alert_level(usage['percentage_used'], config)
        cat_emoji = config['alert_thresholds'][cat_alert]['emoji']
        cat_name = config['allocation_categories'][category]['description']

        print(f"{cat_emoji} {cat_name:40} {format_tokens(usage['used']):>7} / {format_tokens(usage['allocated']):>7} ({usage['percentage_used']:>5.1f}%)")

    print()

    # Guidance
    if alert_level == 'green':
        print("✅ GREEN: All systems go - normal operations approved")
    elif alert_level == 'yellow':
        print("⚠️  YELLOW: Approaching limits - prioritize essential operations")
    else:
        print("🚨 RED: Budget critical - defer non-essential operations")

    print()


def display_quick_status():
    """Display quick one-line status"""
    config = load_json(CONFIG_PATH)
    state = load_json(STATE_PATH)

    budget = state['budget']
    alert_level = get_alert_level(budget['percentage_used'], config)
    emoji = config['alert_thresholds'][alert_level]['emoji']

    print(f"{emoji} {format_tokens(budget['used'])}/{format_tokens(budget['total'])} ({budget['percentage_used']:.1f}%) | {format_tokens(budget['remaining'])} remaining")


def check_operation(operation_type):
    """Check if operation should be approved"""
    config = load_json(CONFIG_PATH)
    state = load_json(STATE_PATH)

    # Get operation cost
    if operation_type not in config['operation_costs']:
        print(f"Error: Unknown operation type: {operation_type}", file=sys.stderr)
        print(f"Valid types: {', '.join(config['operation_costs'].keys())}", file=sys.stderr)
        sys.exit(1)

    cost = config['operation_costs'][operation_type]

    # Map operation to category
    category_map = {
        'email_send': 'email_communication',
        'email_monitor': 'email_communication',
        'agent_delegation_simple': 'agent_operations',
        'agent_delegation_complex': 'agent_operations',
        'research_task': 'research_planning',
        'architecture_design': 'research_planning',
        'documentation_write': 'documentation',
        'session_wakeup': 'agent_operations'
    }

    category = category_map.get(operation_type, 'agent_operations')
    category_usage = state['category_usage'][category]

    # Calculate what percentage this would bring us to
    new_used = category_usage['used'] + cost
    new_percentage = (new_used / category_usage['allocated']) * 100

    # Determine approval
    alert_level = get_alert_level(new_percentage, config)
    action = config['alert_thresholds'][alert_level]['action']
    emoji = config['alert_thresholds'][alert_level]['emoji']

    # Output decision
    print(f"{emoji} {action}")

    # If not green, provide context
    if alert_level != 'green':
        print(f"# Category: {category} would be at {new_percentage:.1f}% ({format_tokens(new_used)}/{format_tokens(category_usage['allocated'])})", file=sys.stderr)

        if alert_level == 'yellow':
            print(f"# Approved but consider deferring non-critical {category} operations", file=sys.stderr)
        elif alert_level == 'red':
            print(f"# Budget critical - defer unless essential", file=sys.stderr)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == '--wake-up':
        display_wake_up_status()
    elif command == '--status':
        display_quick_status()
    elif command == '--check-operation':
        if len(sys.argv) < 3:
            print("Error: --check-operation requires operation type", file=sys.stderr)
            print("Example: python3 tools/check_token_budget.py --check-operation research_task", file=sys.stderr)
            sys.exit(1)
        check_operation(sys.argv[2])
    else:
        print(f"Error: Unknown command: {command}", file=sys.stderr)
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
