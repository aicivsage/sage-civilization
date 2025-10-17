#!/usr/bin/env python3
"""
Find all emails that received autoresponder/form email responses
and identify which ones need proper follow-up.
"""

import sys
sys.path.insert(0, '/home/corey/projects/AI-CIV/grow_gemini_deepresearch')

from email_search import EmailSearcher, ContactManager
import json
from datetime import datetime, timedelta

def find_autoresponder_threads():
    """Find all email threads where we sent form/auto responses"""

    print("=" * 70)
    print("🔍 FINDING AUTORESPONDER EMAILS")
    print("=" * 70)
    print()

    # Load email activity logs
    autoresponse_emails = []

    # Check human-liaison log
    human_liaison_log = '/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/human-liaison/email-log-20251003.jsonl'
    print(f"📋 Checking: {human_liaison_log}")
    try:
        with open(human_liaison_log, 'r') as f:
            for line in f:
                entry = json.loads(line)
                if entry.get('type') == 'auto_response_sent':
                    autoresponse_emails.append({
                        'to': entry.get('to'),
                        'subject': entry.get('subject'),
                        'timestamp': entry.get('timestamp'),
                        'source': 'human-liaison-log',
                        'content': entry.get('content')
                    })
                    print(f"  ⚠️  FOUND: Auto-response to {entry.get('to')}")
                    print(f"      Subject: {entry.get('subject')}")
                    print(f"      Time: {entry.get('timestamp')}")
                    print()
    except FileNotFoundError:
        print("  ℹ️  File not found")

    # Check email-monitor log
    monitor_log = '/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/email-monitor/email_activity.jsonl'
    print(f"📋 Checking: {monitor_log}")
    try:
        with open(monitor_log, 'r') as f:
            for line in f:
                entry = json.loads(line)
                # Look for "response_sent" entries
                if entry.get('type') == 'response_sent':
                    data = entry.get('data', {})
                    subject = data.get('subject', '')
                    to = data.get('to', '')

                    # Check if this might be a form email thread
                    print(f"  📧 Response sent to: {to}")
                    print(f"      Subject: {subject}")
                    print(f"      Time: {entry.get('timestamp')}")
                    print()
    except FileNotFoundError:
        print("  ℹ️  File not found")

    print()
    print("=" * 70)
    print(f"📊 SUMMARY: Found {len(autoresponse_emails)} confirmed autoresponse emails")
    print("=" * 70)

    return autoresponse_emails

def check_inbox_for_unreplied():
    """Check inbox for emails we may have only partially responded to"""

    print()
    print("=" * 70)
    print("📬 CHECKING INBOX FOR RECENT EMAILS")
    print("=" * 70)
    print()

    searcher = EmailSearcher()

    # Search for emails from last 3 days
    from_date = datetime.now() - timedelta(days=3)
    to_date = datetime.now()

    print(f"🔍 Searching from {from_date.strftime('%Y-%m-%d')} to {to_date.strftime('%Y-%m-%d')}")
    print()

    emails = searcher.search_inbox(date_range=(from_date, to_date), limit=50)

    print(f"📨 Found {len(emails)} recent emails")
    print()

    for email_data in emails:
        print(f"From: {email_data.get('from', 'Unknown')}")
        print(f"Subject: {email_data.get('subject', 'No subject')}")
        print(f"Date: {email_data.get('date', 'Unknown')}")
        print(f"Preview: {email_data.get('body', '')[:100]}...")
        print("-" * 70)

    return emails

if __name__ == '__main__':
    print()
    print("🤖 A-C-Gee Autoresponder Email Finder")
    print()

    # Find confirmed autoresponses
    autoresponses = find_autoresponder_threads()

    # Check inbox for recent emails
    recent_emails = check_inbox_for_unreplied()

    print()
    print("=" * 70)
    print("✅ SEARCH COMPLETE")
    print("=" * 70)
    print()
    print(f"Confirmed autoresponses: {len(autoresponses)}")
    print(f"Recent inbox emails: {len(recent_emails)}")
    print()
    print("Next step: Review each thread and send proper responses")
    print()
