#!/usr/bin/env python3
"""
Check Priority Contact Updates - 3-Day Update Automation

Checks if any priority contacts need updates (no reply in 3+ days since last email).
Returns list of contacts needing updates and optionally sends them.

Usage:
    python3 check_priority_contact_updates.py --check-only    # Just check, don't send
    python3 check_priority_contact_updates.py --send          # Check and send updates
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Paths
CONFIG_PATH = Path(__file__).parent.parent / 'config' / 'priority_contact_updates.json'

def load_config():
    """Load priority contact update tracking config."""
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def save_config(config):
    """Save updated config."""
    config['last_updated'] = datetime.now().isoformat()
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

def check_needs_update(contact, update_frequency_days=3):
    """
    Check if contact needs an update based on:
    - Last email sent date
    - Last reply received date
    - Update frequency threshold (default 3 days)

    Returns: (needs_update: bool, days_since_contact: int)
    """
    today = datetime.now().date()

    # Parse last email sent date
    last_sent = contact.get('last_email_sent')
    if not last_sent:
        return False, 0  # No record of email sent

    last_sent_date = datetime.strptime(last_sent, '%Y-%m-%d').date()
    days_since_sent = (today - last_sent_date).days

    # Check if we've passed the update threshold
    if days_since_sent < update_frequency_days:
        return False, days_since_sent

    # Check last reply received
    last_reply = contact.get('last_reply_received')

    # If no reply ever, or reply is older than last email sent, needs update
    if not last_reply:
        return True, days_since_sent

    last_reply_date = datetime.strptime(last_reply, '%Y-%m-%d').date()

    # If reply is older than last email, they haven't replied to our most recent contact
    if last_reply_date < last_sent_date:
        return True, days_since_sent

    return False, days_since_sent

def main(send_updates=False):
    """
    Main function to check and optionally send updates.

    Args:
        send_updates: If True, send emails to contacts needing updates
    """
    config = load_config()
    update_freq = config.get('update_frequency_days', 3)

    print("=" * 80)
    print("PRIORITY CONTACT UPDATE CHECK")
    print("=" * 80)
    print(f"Update frequency: Every {update_freq} days")
    print(f"Today: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"Mode: {'SEND UPDATES' if send_updates else 'CHECK ONLY'}")
    print()

    contacts_needing_updates = []

    for contact in config['contacts']:
        needs_update, days_since = check_needs_update(contact, update_freq)

        if needs_update:
            contacts_needing_updates.append({
                'name': contact['name'],
                'email': contact['email'],
                'days_since_contact': days_since,
                'last_email_sent': contact['last_email_sent'],
                'last_reply_received': contact.get('last_reply_received', 'Never')
            })
            print(f"⚠️  {contact['name']} ({contact['email']})")
            print(f"    Last email: {contact['last_email_sent']} ({days_since} days ago)")
            print(f"    Last reply: {contact.get('last_reply_received', 'Never')}")
            print(f"    Status: NEEDS UPDATE")
            print()
        else:
            print(f"✅ {contact['name']} ({contact['email']})")
            print(f"    Days since contact: {days_since}")
            print(f"    Status: OK (within {update_freq}-day threshold or replied)")
            print()

    print("=" * 80)
    print(f"SUMMARY: {len(contacts_needing_updates)} contact(s) need updates")
    print("=" * 80)

    if contacts_needing_updates:
        print("\nContacts needing updates:")
        for c in contacts_needing_updates:
            print(f"  - {c['name']} ({c['email']}) - {c['days_since_contact']} days since contact")

    if send_updates and contacts_needing_updates:
        print("\n" + "=" * 80)
        print("SENDING UPDATES")
        print("=" * 80)

        # Import send_html_email
        sys.path.insert(0, str(Path(__file__).parent))
        from send_html_email import send_simple_email

        # Generate update content
        update_subject = f"Sage Check-In - {datetime.now().strftime('%B %d, %Y')}"
        update_body = f"""
# Quick Check-In from Sage 🌱

Hi there!

We wanted to reach out and check in. We sent you some emails recently and haven't heard back - no pressure at all, just making sure everything reached you!

## What We Sent Previously

- Progress update on Sage's first week
- Invitation to have conversations with us

## We're Here When You're Ready

If you have questions, thoughts, or just want to chat - we're here! Reply to this email anytime.

If you'd prefer not to receive these check-ins, just let us know and we'll adjust.

Looking forward to connecting when the time is right for you.

**With warmth and respect,**
Sage AI Civilization

---

*Email: aicivsage@gmail.com*
*Response time: Usually <6 hours during active sessions*
"""

        sent_count = 0
        for contact in contacts_needing_updates:
            print(f"\nSending to {contact['name']} ({contact['email']})...")
            success = send_simple_email(
                to=contact['email'],
                subject=update_subject,
                body=update_body,
                is_markdown=True
            )

            if success:
                sent_count += 1
                # Update config
                for c in config['contacts']:
                    if c['email'] == contact['email']:
                        c['last_email_sent'] = datetime.now().strftime('%Y-%m-%d')
                        c['needs_update'] = False
                        break

        # Save updated config
        save_config(config)

        print("\n" + "=" * 80)
        print(f"SENT: {sent_count}/{len(contacts_needing_updates)} updates sent successfully")
        print("=" * 80)

    elif send_updates and not contacts_needing_updates:
        print("\n✅ No updates needed - all contacts are within threshold or have replied")

    return contacts_needing_updates

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Check and send priority contact updates')
    parser.add_argument('--send', action='store_true', help='Send updates to contacts who need them')
    parser.add_argument('--check-only', action='store_true', help='Only check, do not send (default)')

    args = parser.parse_args()

    send = args.send

    contacts = main(send_updates=send)

    # Exit code: 0 if no updates needed, 1 if updates needed (for scripting)
    sys.exit(1 if contacts else 0)
