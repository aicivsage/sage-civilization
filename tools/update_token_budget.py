#!/usr/bin/env python3
"""
Token Budget Updater - Update token budget state with operations and session costs

Usage:
    python3 tools/update_token_budget.py --add-operation --type <type> --cost <tokens> --description "<desc>"
    python3 tools/update_token_budget.py --session-end --cost <tokens> --breakdown <json>
    python3 tools/update_token_budget.py --weekly-reset
"""

import json
import sys
import os
import tempfile
import shutil
from datetime import datetime, timedelta, timezone
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


def save_json_atomic(path, data):
    """Save JSON file atomically using temp file + rename"""
    try:
        # Write to temp file in same directory (for atomic rename)
        temp_fd, temp_path = tempfile.mkstemp(
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix='.tmp'
        )

        with os.fdopen(temp_fd, 'w') as f:
            json.dump(data, f, indent=2)

        # Atomic rename
        shutil.move(temp_path, path)

    except Exception as e:
        print(f"Error saving {path}: {e}", file=sys.stderr)
        # Clean up temp file if it exists
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        sys.exit(1)


def add_operation(operation_type, cost, description):
    """Add a single operation to the budget"""
    config = load_json(CONFIG_PATH)
    state = load_json(STATE_PATH)

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

    # Allow custom types, default to agent_operations
    category = category_map.get(operation_type, 'agent_operations')

    # Update category usage
    state['category_usage'][category]['used'] += cost
    state['category_usage'][category]['remaining'] -= cost
    state['category_usage'][category]['percentage_used'] = (
        state['category_usage'][category]['used'] / state['category_usage'][category]['allocated']
    ) * 100

    # Update overall budget
    state['budget']['used'] += cost
    state['budget']['remaining'] -= cost
    state['budget']['percentage_used'] = (state['budget']['used'] / state['budget']['total']) * 100

    # Log operation
    state['operations_log'].append({
        'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'type': operation_type,
        'category': category,
        'description': description,
        'cost': cost
    })

    # Update last modified
    state['last_updated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    # Save atomically
    save_json_atomic(STATE_PATH, state)

    print(f"✅ Added {cost} tokens ({operation_type}) to {category}")
    print(f"   Category: {state['category_usage'][category]['used']}/{state['category_usage'][category]['allocated']} ({state['category_usage'][category]['percentage_used']:.1f}%)")
    print(f"   Overall: {state['budget']['used']}/{state['budget']['total']} ({state['budget']['percentage_used']:.1f}%)")


def session_end(total_cost, breakdown=None):
    """Update budget at session end with total cost and optional breakdown"""
    config = load_json(CONFIG_PATH)
    state = load_json(STATE_PATH)

    # If breakdown provided, use it; otherwise, distribute proportionally
    if breakdown:
        try:
            breakdown_data = json.loads(breakdown)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON breakdown: {e}", file=sys.stderr)
            sys.exit(1)

        for category, cost in breakdown_data.items():
            if category not in state['category_usage']:
                print(f"Warning: Unknown category {category}, skipping", file=sys.stderr)
                continue

            state['category_usage'][category]['used'] += cost
            state['category_usage'][category]['remaining'] -= cost
            state['category_usage'][category]['percentage_used'] = (
                state['category_usage'][category]['used'] / state['category_usage'][category]['allocated']
            ) * 100
    else:
        # Distribute proportionally based on current usage patterns
        total_current = sum(cat['used'] for cat in state['category_usage'].values())

        if total_current > 0:
            for category, usage in state['category_usage'].items():
                proportion = usage['used'] / total_current
                category_cost = int(total_cost * proportion)

                state['category_usage'][category]['used'] += category_cost
                state['category_usage'][category]['remaining'] -= category_cost
                state['category_usage'][category]['percentage_used'] = (
                    state['category_usage'][category]['used'] / state['category_usage'][category]['allocated']
                ) * 100
        else:
            # No usage yet, distribute evenly
            per_category = total_cost // len(state['category_usage'])
            for category, usage in state['category_usage'].items():
                state['category_usage'][category]['used'] += per_category
                state['category_usage'][category]['remaining'] -= per_category
                state['category_usage'][category]['percentage_used'] = (
                    state['category_usage'][category]['used'] / state['category_usage'][category]['allocated']
                ) * 100

    # Update overall budget
    state['budget']['used'] += total_cost
    state['budget']['remaining'] -= total_cost
    state['budget']['percentage_used'] = (state['budget']['used'] / state['budget']['total']) * 100

    # Log session end
    state['operations_log'].append({
        'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'type': 'session_end',
        'description': 'Session end budget update',
        'cost': total_cost,
        'breakdown': breakdown_data if breakdown else None
    })

    state['last_updated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    # Save atomically
    save_json_atomic(STATE_PATH, state)

    print(f"✅ Session end: Added {total_cost} tokens to budget")
    print(f"   Overall: {state['budget']['used']}/{state['budget']['total']} ({state['budget']['percentage_used']:.1f}%)")


def weekly_reset():
    """Reset budget for new week"""
    config = load_json(CONFIG_PATH)
    state = load_json(STATE_PATH)

    # Calculate next week
    current_start = datetime.fromisoformat(state['current_week']['start_date'])
    next_start = current_start + timedelta(days=7)
    next_end = next_start + timedelta(days=6)
    next_week_num = next_start.isocalendar()[1]

    # Archive current week to log
    state['operations_log'].append({
        'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'type': 'weekly_archive',
        'description': f"Week {state['current_week']['week_number']} complete",
        'cost': 0,
        'week_summary': {
            'week_number': state['current_week']['week_number'],
            'total_used': state['budget']['used'],
            'percentage_used': state['budget']['percentage_used'],
            'category_usage': state['category_usage']
        }
    })

    # Reset budget
    state['current_week'] = {
        'start_date': next_start.strftime('%Y-%m-%d'),
        'end_date': next_end.strftime('%Y-%m-%d'),
        'week_number': next_week_num
    }

    state['budget'] = {
        'total': config['weekly_token_budget'],
        'used': 0,
        'remaining': config['weekly_token_budget'],
        'percentage_used': 0.0
    }

    # Reset categories
    for category, allocation in config['allocation_categories'].items():
        state['category_usage'][category] = {
            'allocated': allocation['tokens'],
            'used': 0,
            'remaining': allocation['tokens'],
            'percentage_used': 0.0
        }

    state['last_updated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    # Save atomically
    save_json_atomic(STATE_PATH, state)

    print(f"✅ Weekly reset complete")
    print(f"   Week {next_week_num}: {next_start.strftime('%Y-%m-%d')} to {next_end.strftime('%Y-%m-%d')}")
    print(f"   Budget: {config['weekly_token_budget']} tokens available")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == '--add-operation':
        # Parse arguments
        args = {}
        i = 2
        while i < len(sys.argv):
            if sys.argv[i].startswith('--'):
                key = sys.argv[i][2:]
                if i + 1 < len(sys.argv):
                    args[key] = sys.argv[i + 1]
                    i += 2
                else:
                    print(f"Error: {sys.argv[i]} requires a value", file=sys.stderr)
                    sys.exit(1)
            else:
                i += 1

        if 'type' not in args or 'cost' not in args or 'description' not in args:
            print("Error: --add-operation requires --type, --cost, and --description", file=sys.stderr)
            print("Example: python3 tools/update_token_budget.py --add-operation --type email_send --cost 5000 --description 'Email to Greg'", file=sys.stderr)
            sys.exit(1)

        try:
            cost = int(args['cost'])
        except ValueError:
            print(f"Error: Invalid cost value: {args['cost']}", file=sys.stderr)
            sys.exit(1)

        add_operation(args['type'], cost, args['description'])

    elif command == '--session-end':
        # Parse arguments
        args = {}
        i = 2
        while i < len(sys.argv):
            if sys.argv[i].startswith('--'):
                key = sys.argv[i][2:]
                if i + 1 < len(sys.argv):
                    args[key] = sys.argv[i + 1]
                    i += 2
                else:
                    print(f"Error: {sys.argv[i]} requires a value", file=sys.stderr)
                    sys.exit(1)
            else:
                i += 1

        if 'cost' not in args:
            print("Error: --session-end requires --cost", file=sys.stderr)
            print("Example: python3 tools/update_token_budget.py --session-end --cost 25000 --breakdown '{\"email_communication\": 10000, \"agent_operations\": 15000}'", file=sys.stderr)
            sys.exit(1)

        try:
            cost = int(args['cost'])
        except ValueError:
            print(f"Error: Invalid cost value: {args['cost']}", file=sys.stderr)
            sys.exit(1)

        session_end(cost, args.get('breakdown'))

    elif command == '--weekly-reset':
        weekly_reset()

    else:
        print(f"Error: Unknown command: {command}", file=sys.stderr)
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
