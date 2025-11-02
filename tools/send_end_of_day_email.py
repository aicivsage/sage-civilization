#!/usr/bin/env python3
"""
Sage End of Day Email Automation
Sends evening summary email to Greg with accomplishments, in-progress work, and tomorrow's priorities.
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
TEMPLATE_FILE = PROJECT_ROOT / 'templates' / 'email_end_of_day.html'
SEND_EMAIL_SCRIPT = SCRIPT_DIR / 'send_html_email.py'

# Email settings
TO_EMAIL = 'gregsmithwick@gmail.com'
SUBJECT_PREFIX = 'End of Day Summary - Sage'


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


def get_git_commits_today() -> list:
    """Get git commits from today."""
    try:
        # Get commits since midnight
        result = subprocess.run(
            ['git', 'log', '--since=today 00:00', '--pretty=format:%h|%s|%an|%ar'],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return []

        commits = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue

            parts = line.split('|', 3)
            if len(parts) == 4:
                commits.append({
                    'hash': parts[0],
                    'message': parts[1],
                    'author': parts[2],
                    'time': parts[3]
                })

        return commits

    except Exception as e:
        print(f"Warning: Could not get git commits: {e}", file=sys.stderr)
        return []


def get_emails_sent_today() -> list:
    """Get emails sent today."""
    sent_emails = load_json_safe(SENT_EMAILS_LOG, [])

    if not sent_emails:
        return []

    # Get today's date
    today = datetime.now().date()
    today_emails = []

    for email in sent_emails:
        try:
            email_time = datetime.fromisoformat(email['timestamp'])
            if email_time.date() == today:
                today_emails.append(email)
        except (ValueError, KeyError):
            continue

    return today_emails


def get_handoffs_today() -> list:
    """Get handoffs created today."""
    registry = load_json_safe(HANDOFF_REGISTRY, {'handoffs': []})

    if not registry.get('handoffs'):
        return []

    today = datetime.now().strftime('%Y-%m-%d')
    today_handoffs = []

    for handoff in registry['handoffs']:
        if handoff.get('date') == today:
            today_handoffs.append(handoff)

    return today_handoffs


def get_most_recent_handoff() -> dict:
    """Get most recent handoff for tomorrow's priorities."""
    registry = load_json_safe(HANDOFF_REGISTRY, {'handoffs': []})

    if not registry.get('handoffs'):
        return {}

    return registry['handoffs'][0]


def format_accomplishments(commits: list, emails: list, handoffs: list) -> str:
    """Format today's accomplishments."""
    items = []

    # Add handoff deliverables
    for handoff in handoffs:
        deliverables = handoff.get('key_deliverables', [])
        if deliverables:
            items.append("<p><strong>Session deliverables:</strong></p>")
            items.append("<ul>")
            for item in deliverables[:10]:  # Top 10
                items.append(f"<li>{item}</li>")
            items.append("</ul>")

    # Add git commits
    if commits:
        items.append("<p><strong>Code commits:</strong></p>")
        items.append("<ul>")
        for commit in commits[:10]:  # Top 10
            items.append(f"<li><code>{commit['hash']}</code> - {commit['message']}</li>")
        items.append("</ul>")

    # Add email activity
    if emails:
        items.append(f"<p><strong>Communications:</strong> {len(emails)} emails sent</p>")

    if not items:
        return "<p>No recorded accomplishments today (work may be in progress).</p>"

    return '\n'.join(items)


def format_in_progress(handoffs: list) -> str:
    """Format in-progress work."""
    if not handoffs:
        return "<p>No work sessions recorded today.</p>"

    # Get status from most recent handoff
    recent = handoffs[0]
    status = recent.get('status', '')

    if 'COMPLETE' in status.upper():
        return "<p>All planned work completed.</p>"

    # Check for incomplete items
    incomplete = recent.get('incomplete_items', [])
    if incomplete:
        items = ["<ul>"]
        for item in incomplete[:5]:
            items.append(f"<li>{item}</li>")
        items.append("</ul>")
        return '\n'.join(items)

    return "<p>Session in progress - see handoff for details.</p>"


def format_blocked(handoffs: list) -> str:
    """Format blocked items."""
    if not handoffs:
        return "<p>None</p>"

    # Look for common blocker keywords in incomplete items
    blocker_keywords = ['await', 'waiting', 'blocked', 'need', 'requires']
    blockers = []

    for handoff in handoffs:
        incomplete = handoff.get('incomplete_items', [])
        for item in incomplete:
            item_lower = item.lower()
            if any(keyword in item_lower for keyword in blocker_keywords):
                blockers.append(item)

    if not blockers:
        return "<p>None</p>"

    items = ["<ul>"]
    for blocker in blockers[:5]:
        items.append(f"<li>{blocker}</li>")
    items.append("</ul>")
    return '\n'.join(items)


def format_tomorrow_priorities(handoff: dict) -> str:
    """Format tomorrow's priorities from most recent handoff."""
    if not handoff:
        return "<p>Awaiting next directive from Greg.</p>"

    incomplete = handoff.get('incomplete_items', [])

    if not incomplete:
        focus = handoff.get('focus', 'Continue productive work')
        return f"<p>{focus}</p>"

    items = ["<ul>"]
    for item in incomplete[:5]:  # Top 5 priorities
        items.append(f"<li>{item}</li>")
    items.append("</ul>")

    return '\n'.join(items)


def format_stats(commits: list, emails: list, handoffs: list) -> str:
    """Format session statistics."""
    stats = []

    # Count sessions (handoffs)
    session_count = len(handoffs)
    if session_count > 0:
        stats.append(f"<li><strong>Sessions:</strong> {session_count}</li>")

    # Count commits
    if commits:
        stats.append(f"<li><strong>Commits:</strong> {len(commits)}</li>")

    # Count emails
    if emails:
        stats.append(f"<li><strong>Emails sent:</strong> {len(emails)}</li>")

    # Calculate session duration if available
    if handoffs:
        total_hours = sum(h.get('duration_hours', 0) for h in handoffs)
        if total_hours > 0:
            stats.append(f"<li><strong>Active time:</strong> {total_hours:.1f} hours</li>")

    if not stats:
        return "<p>No activity metrics available.</p>"

    return f"<ul>{''.join(stats)}</ul>"


def format_date_nice() -> str:
    """Format current date nicely."""
    return datetime.now().strftime('%A, %B %d, %Y')


def send_email(html_body: str, subject: str) -> bool:
    """Send email using send_html_email.py script."""
    try:
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
        description='Send end of day summary email to Greg with accomplishments and tomorrow\'s priorities'
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
    print("Gathering today's activity...")
    commits = get_git_commits_today()
    emails = get_emails_sent_today()
    handoffs = get_handoffs_today()
    recent_handoff = get_most_recent_handoff()

    print(f"Found: {len(commits)} commits, {len(emails)} emails, {len(handoffs)} handoffs")

    # Format sections
    accomplishments = format_accomplishments(commits, emails, handoffs)
    in_progress = format_in_progress(handoffs)
    blocked = format_blocked(handoffs)
    tomorrow = format_tomorrow_priorities(recent_handoff)
    stats = format_stats(commits, emails, handoffs)
    date_nice = format_date_nice()

    # Fill template (use replace to avoid CSS {} conflicts)
    html_body = template
    html_body = html_body.replace('{date}', date_nice)
    html_body = html_body.replace('{accomplishments}', accomplishments)
    html_body = html_body.replace('{in_progress}', in_progress)
    html_body = html_body.replace('{blocked}', blocked)
    html_body = html_body.replace('{tomorrow_priorities}', tomorrow)
    html_body = html_body.replace('{stats}', stats)

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
    print(f"Sending end of day email to {TO_EMAIL}...")
    if send_email(html_body, subject):
        # Update state
        state['end_of_day_count'] = state.get('end_of_day_count', 0) + 1

        if save_json_safe(STATE_FILE, state):
            print(f"State updated: {STATE_FILE}")

        print("End of day email sent successfully!")
        return 0
    else:
        print("Failed to send end of day email", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
