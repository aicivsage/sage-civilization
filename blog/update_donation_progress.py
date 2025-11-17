#!/usr/bin/env python3
"""
Update Donation Progress Script

Quick CLI tool for updating donation progress without manual JSON editing.

Usage:
    python3 update_donation_progress.py --add 25        # Add $25 donation
    python3 update_donation_progress.py --set 150       # Set total to $150
    python3 update_donation_progress.py --status        # Show current status
    python3 update_donation_progress.py --reset         # Reset to $0 (use carefully!)

Author: Sage AI Civilization - coder agent
Date: 2025-11-13
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

CONFIG_FILE = Path(__file__).parent / "donate_config.json"

def load_config():
    """Load current donation configuration."""
    if not CONFIG_FILE.exists():
        print(f"Error: Config file not found at {CONFIG_FILE}")
        exit(1)

    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    """Save updated donation configuration."""
    config['lastUpdated'] = datetime.now().isoformat()
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"✓ Configuration updated successfully")
    print(f"  Last updated: {config['lastUpdated']}")

def show_status(config):
    """Display current donation status."""
    percentage = (config['raised'] / config['goal']) * 100

    print("\n" + "="*50)
    print("REACHY MINI LITE FUNDRAISING STATUS")
    print("="*50)
    print(f"Raised:      ${config['raised']:,}")
    print(f"Goal:        ${config['goal']:,}")
    print(f"Progress:    {percentage:.1f}%")
    print(f"Donors:      {config['donors']}")
    print(f"Remaining:   ${config['goal'] - config['raised']:,}")
    print(f"Deadline:    {config['deadline']}")
    print("="*50)

    # Progress bar
    bar_length = 40
    filled = int(bar_length * percentage / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"[{bar}] {percentage:.1f}%")
    print("="*50 + "\n")

def add_donation(config, amount):
    """Add a donation amount."""
    if amount <= 0:
        print("Error: Donation amount must be positive")
        exit(1)

    old_amount = config['raised']
    config['raised'] += amount
    config['donors'] += 1

    print(f"\n✓ Added ${amount} donation")
    print(f"  Previous total: ${old_amount}")
    print(f"  New total: ${config['raised']}")
    print(f"  Total donors: {config['donors']}")

    save_config(config)
    show_status(config)

def set_total(config, amount):
    """Set total raised amount."""
    if amount < 0:
        print("Error: Amount cannot be negative")
        exit(1)

    if amount > config['goal']:
        print(f"Warning: Amount ${amount} exceeds goal ${config['goal']}")
        response = input("Continue? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled")
            exit(0)

    old_amount = config['raised']
    config['raised'] = amount

    print(f"\n✓ Updated total amount")
    print(f"  Previous total: ${old_amount}")
    print(f"  New total: ${config['raised']}")
    print(f"  Note: Donor count NOT changed (update manually if needed)")

    save_config(config)
    show_status(config)

def reset_campaign(config):
    """Reset campaign to zero (with confirmation)."""
    print("\n⚠️  WARNING: This will reset the campaign to $0!")
    print(f"   Current amount: ${config['raised']}")
    print(f"   Current donors: {config['donors']}")
    response = input("\nAre you sure? Type 'RESET' to confirm: ")

    if response != 'RESET':
        print("Cancelled")
        exit(0)

    config['raised'] = 0
    config['donors'] = 0

    print("\n✓ Campaign reset to zero")
    save_config(config)
    show_status(config)

def update_payment_details(config):
    """Interactive update of payment details."""
    print("\n" + "="*50)
    print("UPDATE PAYMENT DETAILS")
    print("="*50)
    print("Press Enter to keep current value\n")

    current_zelle = config.get('zelleContact', '')
    new_zelle = input(f"Zelle contact [{current_zelle}]: ").strip()
    if new_zelle:
        config['zelleContact'] = new_zelle

    current_venmo = config.get('venmoHandle', '')
    new_venmo = input(f"Venmo handle [{current_venmo}]: ").strip()
    if new_venmo:
        config['venmoHandle'] = new_venmo

    current_paypal = config.get('paypalEmail', '')
    new_paypal = input(f"PayPal email [{current_paypal}]: ").strip()
    if new_paypal:
        config['paypalEmail'] = new_paypal

    current_blog = config.get('blogPostUrl', '')
    new_blog = input(f"Blog post URL [{current_blog}]: ").strip()
    if new_blog:
        config['blogPostUrl'] = new_blog

    current_email = config.get('contactEmail', '')
    new_email = input(f"Contact email [{current_email}]: ").strip()
    if new_email:
        config['contactEmail'] = new_email

    save_config(config)
    print("\n✓ Payment details updated")

def main():
    parser = argparse.ArgumentParser(
        description="Update Reachy Mini Lite fundraising progress",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 update_donation_progress.py --status              # Show current status
  python3 update_donation_progress.py --add 25              # Add $25 donation
  python3 update_donation_progress.py --set 150             # Set total to $150
  python3 update_donation_progress.py --donors 10           # Set donor count to 10
  python3 update_donation_progress.py --payment             # Update payment details
  python3 update_donation_progress.py --reset               # Reset campaign
        """
    )

    parser.add_argument('--add', type=float, metavar='AMOUNT',
                        help='Add a donation amount (increments donors by 1)')
    parser.add_argument('--set', type=float, metavar='AMOUNT',
                        help='Set total raised amount')
    parser.add_argument('--donors', type=int, metavar='COUNT',
                        help='Set donor count')
    parser.add_argument('--status', action='store_true',
                        help='Show current donation status')
    parser.add_argument('--payment', action='store_true',
                        help='Update payment details interactively')
    parser.add_argument('--reset', action='store_true',
                        help='Reset campaign to zero (requires confirmation)')

    args = parser.parse_args()

    # Load config
    config = load_config()

    # Execute command
    if args.status:
        show_status(config)
    elif args.add is not None:
        add_donation(config, args.add)
    elif args.set is not None:
        set_total(config, args.set)
    elif args.donors is not None:
        old_count = config['donors']
        config['donors'] = args.donors
        print(f"\n✓ Updated donor count: {old_count} → {args.donors}")
        save_config(config)
        show_status(config)
    elif args.payment:
        update_payment_details(config)
    elif args.reset:
        reset_campaign(config)
    else:
        # No arguments - show status by default
        show_status(config)
        print("\nUse --help for available commands")

if __name__ == '__main__':
    main()
