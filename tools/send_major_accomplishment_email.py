#!/usr/bin/env python3
"""
Sage Major Accomplishment Email Automation
Sends immediate email to Greg when significant accomplishments occur.
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import subprocess

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
STATE_FILE = PROJECT_ROOT / 'memories' / 'system' / 'email_schedule_state.json'
TEMPLATE_FILE = PROJECT_ROOT / 'templates' / 'email_major_accomplishment.html'
SEND_EMAIL_SCRIPT = SCRIPT_DIR / 'send_html_email.py'

# Email settings
TO_EMAIL = 'gregsmithwick@gmail.com'
SUBJECT_PREFIX = 'Major Achievement - Sage'


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


def format_html_content(content: str) -> str:
    """
    Format content into HTML.
    Converts bullet points and paragraphs into proper HTML.
    """
    if not content:
        return "<p>No details provided.</p>"

    lines = content.strip().split('\n')
    html_lines = []
    in_list = False

    for line in lines:
        line = line.strip()

        if not line:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue

        # Check if it's a bullet point
        if line.startswith('-') or line.startswith('*') or line.startswith('•'):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True

            # Remove bullet and format
            item = line[1:].strip()
            html_lines.append(f"<li>{item}</li>")
        else:
            # Regular paragraph
            if in_list:
                html_lines.append("</ul>")
                in_list = False

            html_lines.append(f"<p>{line}</p>")

    # Close list if still open
    if in_list:
        html_lines.append("</ul>")

    return '\n'.join(html_lines)


def format_date_nice() -> str:
    """Format current date nicely."""
    return datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')


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
        description='Send major accomplishment email to Greg',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --achievement "Blog published" \\
    --details "Published 'Caring as Action' to Telegraph with 25K words" \\
    --why-it-matters "First public-facing content from Sage civilization" \\
    --whats-next "Send to priority contacts, await feedback"

  %(prog)s --achievement "Replit integration complete" \\
    --details "- Blog platform operational\\n- Comment system working\\n- Memory profiles active" \\
    --why-it-matters "Enables public discourse and relationship building" \\
    --whats-next "Publish next blog post on natural topics"
        """
    )

    parser.add_argument(
        '--achievement',
        required=True,
        help='Brief achievement title (e.g., "Blog published", "System operational")'
    )
    parser.add_argument(
        '--details',
        required=True,
        help='Detailed description (supports bullet points with - or *)'
    )
    parser.add_argument(
        '--why-it-matters',
        required=True,
        help='Why this achievement is significant'
    )
    parser.add_argument(
        '--whats-next',
        required=True,
        help='Next steps or implications'
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

    # Format content sections
    date_nice = format_date_nice()
    achievement_title = args.achievement
    details_html = format_html_content(args.details)
    why_matters_html = format_html_content(args.why_it_matters)
    whats_next_html = format_html_content(args.whats_next)

    # Fill template (use replace to avoid CSS {} conflicts)
    html_body = template
    html_body = html_body.replace('{date}', date_nice)
    html_body = html_body.replace('{achievement}', achievement_title)
    html_body = html_body.replace('{details}', details_html)
    html_body = html_body.replace('{why_it_matters}', why_matters_html)
    html_body = html_body.replace('{whats_next}', whats_next_html)

    # Generate subject
    subject = f"{SUBJECT_PREFIX}: {achievement_title}"

    if args.dry_run:
        print("\n" + "="*60)
        print("DRY RUN - Email would be sent with:")
        print("="*60)
        print(f"To: {TO_EMAIL}")
        print(f"Subject: {subject}")
        print("\nBody preview (first 800 chars):")
        print(html_body[:800])
        print("...")
        print("="*60)
        return 0

    # Send email
    print(f"Sending major accomplishment email to {TO_EMAIL}...")
    if send_email(html_body, subject):
        # Log accomplishment to state
        accomplishment_record = {
            'achievement': achievement_title,
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d')
        }

        if 'major_accomplishments' not in state:
            state['major_accomplishments'] = []

        state['major_accomplishments'].append(accomplishment_record)

        # Keep only last 50 accomplishments
        if len(state['major_accomplishments']) > 50:
            state['major_accomplishments'] = state['major_accomplishments'][-50:]

        if save_json_safe(STATE_FILE, state):
            print(f"State updated: {STATE_FILE}")
            print(f"Accomplishment logged: {achievement_title}")

        print("Major accomplishment email sent successfully!")
        return 0
    else:
        print("Failed to send major accomplishment email", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
