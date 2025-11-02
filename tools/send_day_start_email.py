#!/usr/bin/env python3
"""
Sage Day Start Email Automation
Sends morning email to Greg with priorities, overnight developments, and context.
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import subprocess

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
STATE_FILE = PROJECT_ROOT / 'memories' / 'system' / 'email_schedule_state.json'
HANDOFF_REGISTRY = PROJECT_ROOT / 'memories' / 'system' / 'HANDOFF_REGISTRY.json'
SENT_EMAILS_LOG = PROJECT_ROOT / 'memories' / 'agents' / 'email-reporter' / 'sent_emails.json'
TEMPLATE_FILE = PROJECT_ROOT / 'templates' / 'email_day_start.html'
SEND_EMAIL_SCRIPT = SCRIPT_DIR / 'send_html_email.py'

# Email settings
TO_EMAIL = 'gregsmithwick@gmail.com'
SUBJECT_PREFIX = 'Good Morning - Sage Daily Start'


def load_json_safe(filepath: Path, default=None):
    """Load JSON file with error handling."""
    if default is None:
        default = {}

    if not filepath.exists():
        return default

    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Warning: Could not load {filepath}: {e}", file=sys.stderr)
        return default


def save_json_safe(filepath: Path, data: dict):
    """Save JSON file with error handling."""
    filepath.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error: Could not save {filepath}: {e}", file=sys.stderr)
        return False


def check_already_sent_today(state: dict) -> bool:
    """Check if day start email already sent today."""
    last_sent = state.get('last_day_start_email', '')
    today = datetime.now().strftime('%Y-%m-%d')
    return last_sent == today


def get_most_recent_handoff() -> dict:
    """Get most recent handoff from registry."""
    registry = load_json_safe(HANDOFF_REGISTRY, {'handoffs': []})

    if not registry.get('handoffs'):
        return {
            'path': 'No handoffs found',
            'date': 'unknown',
            'focus': 'Starting fresh',
            'key_deliverables': [],
            'incomplete_items': []
        }

    # First handoff is most recent
    return registry['handoffs'][0]


def get_overnight_developments() -> str:
    """Check for overnight activity (emails, work)."""
    sent_emails = load_json_safe(SENT_EMAILS_LOG, [])

    if not sent_emails:
        return "<p>No overnight activity detected.</p>"

    # Check last 12 hours for emails
    cutoff = datetime.now() - timedelta(hours=12)
    recent_emails = []

    for email in sent_emails:
        try:
            email_time = datetime.fromisoformat(email['timestamp'])
            if email_time > cutoff:
                recent_emails.append(email)
        except (ValueError, KeyError):
            continue

    if not recent_emails:
        return "<p>No overnight activity detected.</p>"

    # Format email activity
    developments = ["<p>Recent email activity:</p>", "<ul>"]
    for email in recent_emails[-5:]:  # Last 5 emails
        to = email.get('to', 'unknown')
        subject = email.get('subject', 'No subject')
        timestamp = email.get('timestamp', 'unknown time')

        # Format timestamp nicely
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime('%I:%M %p')
        except:
            time_str = timestamp

        developments.append(f"<li><strong>{time_str}</strong> - Email to {to}: {subject}</li>")

    developments.append("</ul>")
    return '\n'.join(developments)


def format_priorities(handoff: dict) -> str:
    """Format priorities from handoff."""
    incomplete = handoff.get('incomplete_items', [])

    if not incomplete:
        # Fall back to focus or deliverables
        focus = handoff.get('focus', 'Continue productive work')
        return f"<p><strong>Focus:</strong> {focus}</p>"

    # Format incomplete items as priority list
    priorities = ["<ul>"]
    for item in incomplete[:5]:  # Top 5 priorities
        priorities.append(f"<li>{item}</li>")
    priorities.append("</ul>")

    return '\n'.join(priorities)


def format_context_summary(handoff: dict) -> str:
    """Format context from yesterday's handoff."""
    deliverables = handoff.get('key_deliverables', [])

    if not deliverables:
        focus = handoff.get('focus', 'Previous session work')
        return f"<p>{focus}</p>"

    # Format key deliverables
    context = ["<p><strong>Yesterday's achievements:</strong></p>", "<ul>"]
    for item in deliverables[:7]:  # Top 7 deliverables
        context.append(f"<li>{item}</li>")
    context.append("</ul>")

    return '\n'.join(context)


def format_date_nice() -> str:
    """Format current date nicely."""
    return datetime.now().strftime('%A, %B %d, %Y')


def send_email(html_body: str, subject: str) -> bool:
    """Send email using send_html_email.py script."""
    try:
        # Call send_html_email.py with proper arguments
        result = subprocess.run(
            [
                sys.executable,
                str(SEND_EMAIL_SCRIPT),
                '--to', TO_EMAIL,
                '--subject', subject,
                '--body', html_body
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print(f"Email sent successfully to {TO_EMAIL}")
            return True
        else:
            print(f"Error sending email: {result.stderr}", file=sys.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("Error: Email sending timed out after 30 seconds", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error sending email: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Send day start email to Greg with priorities and overnight developments'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force send even if already sent today'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print email content without sending'
    )

    args = parser.parse_args()

    # Load state
    state = load_json_safe(STATE_FILE, {
        'last_day_start_email': '',
        'day_start_count': 0,
        'end_of_day_count': 0,
        'major_accomplishments': []
    })

    # Check if already sent today
    if not args.force and check_already_sent_today(state):
        print("Day start email already sent today. Use --force to override.")
        return 0

    # Load template
    if not TEMPLATE_FILE.exists():
        print(f"Error: Template file not found: {TEMPLATE_FILE}", file=sys.stderr)
        return 1

    try:
        with open(TEMPLATE_FILE, 'r') as f:
            template = f.read()
    except Exception as e:
        print(f"Error reading template: {e}", file=sys.stderr)
        return 1

    # Gather data
    print("Gathering session data...")
    handoff = get_most_recent_handoff()
    priorities = format_priorities(handoff)
    overnight = get_overnight_developments()
    context = format_context_summary(handoff)
    date_nice = format_date_nice()

    # Fill template (use replace to avoid CSS {} conflicts)
    html_body = template
    html_body = html_body.replace('{date}', date_nice)
    html_body = html_body.replace('{priorities}', priorities)
    html_body = html_body.replace('{overnight_developments}', overnight)
    html_body = html_body.replace('{context_summary}', context)

    # Generate subject
    subject = f"{SUBJECT_PREFIX} ({datetime.now().strftime('%b %d, %Y')})"

    if args.dry_run:
        print("\n" + "="*60)
        print("DRY RUN - Email would be sent with:")
        print("="*60)
        print(f"To: {TO_EMAIL}")
        print(f"Subject: {subject}")
        print("\nBody preview (first 500 chars):")
        print(html_body[:500])
        print("...")
        print("="*60)
        return 0

    # Send email
    print(f"Sending day start email to {TO_EMAIL}...")
    if send_email(html_body, subject):
        # Update state
        state['last_day_start_email'] = datetime.now().strftime('%Y-%m-%d')
        state['day_start_count'] = state.get('day_start_count', 0) + 1

        if save_json_safe(STATE_FILE, state):
            print(f"State updated: {STATE_FILE}")

        print("Day start email sent successfully!")
        return 0
    else:
        print("Failed to send day start email", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
