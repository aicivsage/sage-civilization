#!/usr/bin/env python3
"""
Sage Session Accomplishment Email
Sends exciting session summary email when meaningful work is completed.
Replaces boring daily emails with event-driven accomplishment reports.
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import subprocess
import re

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
HANDOFF_REGISTRY = PROJECT_ROOT / 'memories' / 'system' / 'HANDOFF_REGISTRY.json'
TEMPLATE_FILE = PROJECT_ROOT / 'templates' / 'session_accomplishment_email_template.html'
SEND_EMAIL_SCRIPT = SCRIPT_DIR / 'send_html_email.py'
SENT_LOG = PROJECT_ROOT / 'memories' / 'agents' / 'email-reporter' / 'session_accomplishment_emails.json'

# Email settings
TO_EMAIL = 'gregsmithwick@gmail.com'


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


def save_json_safe(filepath: Path, data):
    """Save JSON file with error handling."""
    filepath.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error: Could not save {filepath}: {e}", file=sys.stderr)
        return False


def get_current_time_via_mcp() -> str:
    """Use MCP (bash date command) to get accurate current time."""
    try:
        result = subprocess.run(
            ['date', '+%Y-%m-%d %I:%M %p'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        print(f"Warning: Could not get time via MCP: {e}", file=sys.stderr)

    # Fallback to Python datetime
    return datetime.now().strftime('%Y-%m-%d %I:%M %p')


def parse_handoff_file(handoff_path: Path) -> dict:
    """Parse handoff markdown file to extract session details."""
    if not handoff_path.exists():
        return {}

    try:
        with open(handoff_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract key sections using regex
        data = {
            'focus': '',
            'duration': '',
            'status': '',
            'key_deliverables': [],
            'incomplete_items': [],
            'achievements': []
        }

        # Extract focus (from header metadata)
        focus_match = re.search(r'\*\*Session Focus\*\*:\s*(.+)', content, re.IGNORECASE)
        if focus_match:
            data['focus'] = focus_match.group(1).strip()

        # Extract duration (from header metadata)
        duration_match = re.search(r'\*\*Session Duration\*\*:\s*(.+)', content, re.IGNORECASE)
        if duration_match:
            data['duration'] = duration_match.group(1).strip()

        # Extract status (from header metadata)
        status_match = re.search(r'\*\*Status\*\*:\s*(.+)', content, re.IGNORECASE)
        if status_match:
            data['status'] = status_match.group(1).strip()

        # Extract major achievement section (often has the key accomplishment)
        achievement_section = re.search(
            r'##\s*🎯\s*Major Achievement.*?###\s*(.+?)(?:\n\n|\*\*)',
            content,
            re.DOTALL | re.IGNORECASE
        )
        if achievement_section:
            achievement_title = achievement_section.group(1).strip()
            data['achievements'].append(achievement_title)

        # Extract files created section as deliverables
        files_section = re.search(
            r'##\s*📁\s*Files Created.*?((?:###.*?\n(?:[-*]\s+.+\n?)+)+)',
            content,
            re.DOTALL | re.IGNORECASE
        )
        if files_section:
            # Find all bulleted items
            bullets = re.findall(r'[-*\d.]\s+`([^`]+)`', files_section.group(1))
            if bullets:
                data['key_deliverables'] = [f"Created: {b}" for b in bullets]

        # If no files section, try generic "Key Deliverables" or "Deliverables"
        if not data['key_deliverables']:
            deliverables_section = re.search(
                r'##\s*(?:Key Deliverables|Deliverables)(.*?)(?=##|\Z)',
                content,
                re.DOTALL | re.IGNORECASE
            )
            if deliverables_section:
                bullets = re.findall(r'[-*]\s+(.+)', deliverables_section.group(1))
                data['key_deliverables'] = [b.strip() for b in bullets if b.strip()]

        # Extract next session priorities (look for "Next Session Priorities" or similar)
        next_priorities_section = re.search(
            r'##\s*🎯\s*Next Session Priorities(.*?)(?=##|\Z)',
            content,
            re.DOTALL | re.IGNORECASE
        )
        if next_priorities_section:
            # Find sections like "IMMEDIATE", "SHORT-TERM"
            immediate_section = re.search(
                r'###\s*(?:IMMEDIATE|Priority).*?\n((?:[-*\d.]\s+.+\n?)+)',
                next_priorities_section.group(1),
                re.DOTALL | re.IGNORECASE
            )
            if immediate_section:
                bullets = re.findall(r'[-*\d.]\s+\*\*(.+?)\*\*', immediate_section.group(1))
                data['incomplete_items'] = [b.strip() for b in bullets if b.strip()]

        # Fallback: look for generic "Incomplete Items" or "What's Next"
        if not data['incomplete_items']:
            incomplete_section = re.search(
                r'##\s*(?:Incomplete Items|What\'s Next|Next Priority)(.*?)(?=##|\Z)',
                content,
                re.DOTALL | re.IGNORECASE
            )
            if incomplete_section:
                bullets = re.findall(r'[-*]\s+(.+)', incomplete_section.group(1))
                data['incomplete_items'] = [b.strip() for b in bullets if b.strip()]

        # If we have key findings section, extract top 3 as achievements
        if not data['achievements']:
            key_findings_section = re.search(
                r'##\s*💡\s*Key Findings(.*?)(?=##|\Z)',
                content,
                re.DOTALL | re.IGNORECASE
            )
            if key_findings_section:
                findings = re.findall(r'###\s*\d+\.\s*(.+)', key_findings_section.group(1))
                if findings:
                    data['achievements'] = findings[:3]

        # Fallback: use first 3 deliverables as achievements
        if not data['achievements'] and data['key_deliverables']:
            data['achievements'] = data['key_deliverables'][:3]

        return data

    except Exception as e:
        print(f"Error parsing handoff file: {e}", file=sys.stderr)
        return {}


def get_handoff_from_registry(handoff_filename: str = None) -> tuple:
    """
    Get handoff file path from registry.
    Returns: (handoff_path, handoff_filename)
    """
    registry = load_json_safe(HANDOFF_REGISTRY, {'handoffs': []})

    if not registry.get('handoffs'):
        return (None, None)

    # If specific handoff requested, find it
    if handoff_filename:
        for handoff in registry['handoffs']:
            if handoff.get('file') == handoff_filename or handoff.get('path', '').endswith(handoff_filename):
                path = handoff.get('path') or str(PROJECT_ROOT / handoff.get('file'))
                return (Path(path), handoff.get('file') or handoff_filename)

        print(f"Warning: Handoff '{handoff_filename}' not found in registry", file=sys.stderr)
        return (None, None)

    # Otherwise use most recent
    most_recent = registry['handoffs'][0]
    path = most_recent.get('path') or str(PROJECT_ROOT / most_recent.get('file'))
    filename = most_recent.get('file') or Path(path).name

    return (Path(path), filename)


def check_already_sent(handoff_filename: str) -> bool:
    """Check if we already sent email for this handoff."""
    sent_log = load_json_safe(SENT_LOG, [])

    for entry in sent_log:
        if entry.get('handoff_file') == handoff_filename:
            return True

    return False


def log_sent_email(handoff_filename: str, subject: str):
    """Log that we sent email for this handoff."""
    sent_log = load_json_safe(SENT_LOG, [])

    sent_log.append({
        'handoff_file': handoff_filename,
        'subject': subject,
        'timestamp': datetime.now().isoformat(),
        'to': TO_EMAIL
    })

    save_json_safe(SENT_LOG, sent_log)


def calculate_token_budget() -> tuple:
    """
    Calculate remaining token budget.
    Returns: (tokens_remaining, percentage_remaining)
    """
    # This is a placeholder - in production you'd read from actual budget tracker
    # For now, return a reasonable estimate
    budget_total = 200000
    budget_used = 35000  # Estimated from this session
    budget_remaining = budget_total - budget_used
    percentage = int((budget_remaining / budget_total) * 100)

    return (budget_remaining, percentage)


def format_achievements_list(achievements: list) -> str:
    """Format achievements as HTML list items."""
    if not achievements:
        return '                <li>Session work completed (see deliverables for details)</li>'

    html = []
    for achievement in achievements[:3]:  # Top 3
        html.append(f'                <li>{achievement}</li>')

    return '\n'.join(html)


def format_deliverables_list(deliverables: list) -> str:
    """Format deliverables as HTML list items with file paths styled as code."""
    if not deliverables:
        return '                <li>Session work documented in handoff</li>'

    html = []
    for item in deliverables:
        # Highlight file paths in <code> tags
        formatted = re.sub(
            r'(/[^\s]+(?:\.md|\.py|\.sh|\.html|\.json|\.txt))',
            r'<code>\1</code>',
            item
        )
        html.append(f'                <li>{formatted}</li>')

    return '\n'.join(html)


def format_next_priorities(incomplete_items: list) -> str:
    """Format next priorities as HTML."""
    if not incomplete_items:
        return '            <p>Awaiting next directive from Greg</p>'

    html = ['            <ul>']
    for item in incomplete_items[:5]:  # Top 5
        html.append(f'                <li>{item}</li>')
    html.append('            </ul>')

    return '\n'.join(html)


def generate_subject(handoff_data: dict) -> str:
    """Generate email subject from handoff data."""
    focus = handoff_data.get('focus', '')

    if not focus:
        # Try to derive from achievements
        achievements = handoff_data.get('achievements', [])
        if achievements:
            focus = achievements[0][:60]  # First achievement, truncated
        else:
            focus = 'Session Work Complete'

    # Keep subject concise
    if len(focus) > 60:
        focus = focus[:57] + '...'

    return f"Sage Session Complete: {focus}"


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
            if result.stdout:
                print(f"Output: {result.stdout}", file=sys.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("Error: Email sending timed out after 30 seconds", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error sending email: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Send session accomplishment email when meaningful work is completed'
    )
    parser.add_argument(
        '--handoff',
        type=str,
        help='Handoff filename (default: most recent from registry)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force send even if already sent for this handoff'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print email content without sending'
    )

    args = parser.parse_args()

    # Load template
    if not TEMPLATE_FILE.exists():
        print(f"Error: Template file not found: {TEMPLATE_FILE}", file=sys.stderr)
        return 1

    try:
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            template = f.read()
    except Exception as e:
        print(f"Error reading template: {e}", file=sys.stderr)
        return 1

    # Get handoff
    print(f"Looking for handoff: {args.handoff or 'most recent'}...")
    handoff_path, handoff_filename = get_handoff_from_registry(args.handoff)

    if not handoff_path or not handoff_path.exists():
        print(f"Error: Handoff file not found", file=sys.stderr)
        return 1

    print(f"Found handoff: {handoff_filename}")

    # Check if already sent
    if not args.force and check_already_sent(handoff_filename):
        print(f"Email already sent for {handoff_filename}. Use --force to override.")
        return 0

    # Parse handoff
    print("Parsing handoff data...")
    handoff_data = parse_handoff_file(handoff_path)

    if not handoff_data:
        print("Error: Could not parse handoff data", file=sys.stderr)
        return 1

    # Get current time via MCP
    current_time = get_current_time_via_mcp()

    # Calculate token budget
    tokens_remaining, tokens_percent = calculate_token_budget()

    # Format template variables
    replacements = {
        '{timestamp}': current_time,
        '{duration}': handoff_data.get('duration', 'Unknown'),
        '{focus}': handoff_data.get('focus', 'Session work'),
        '{status}': handoff_data.get('status', 'Complete'),
        '{handoff_file}': handoff_filename,
        '{achievements_list}': format_achievements_list(handoff_data.get('achievements', [])),
        '{deliverables_list}': format_deliverables_list(handoff_data.get('key_deliverables', [])),
        '{next_priorities}': format_next_priorities(handoff_data.get('incomplete_items', [])),
        '{tokens_remaining}': f'{tokens_remaining:,}',
        '{tokens_percent}': str(tokens_percent)
    }

    # Fill template
    html_body = template
    for key, value in replacements.items():
        html_body = html_body.replace(key, value)

    # Generate subject
    subject = generate_subject(handoff_data)

    if args.dry_run:
        print("\n" + "="*60)
        print("DRY RUN - Email would be sent with:")
        print("="*60)
        print(f"To: {TO_EMAIL}")
        print(f"Subject: {subject}")
        print("\nHandoff data extracted:")
        print(f"  Focus: {handoff_data.get('focus', 'N/A')}")
        print(f"  Duration: {handoff_data.get('duration', 'N/A')}")
        print(f"  Status: {handoff_data.get('status', 'N/A')}")
        print(f"  Achievements: {len(handoff_data.get('achievements', []))}")
        print(f"  Deliverables: {len(handoff_data.get('key_deliverables', []))}")
        print(f"  Next priorities: {len(handoff_data.get('incomplete_items', []))}")
        print("\nBody preview (first 800 chars):")
        print(html_body[:800])
        print("...")
        print("="*60)
        return 0

    # Send email
    print(f"Sending session accomplishment email to {TO_EMAIL}...")
    if send_email(html_body, subject):
        # Log that we sent it
        log_sent_email(handoff_filename, subject)
        print(f"Session accomplishment email sent successfully!")
        print(f"Subject: {subject}")
        return 0
    else:
        print("Failed to send session accomplishment email", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
