#!/usr/bin/env python3
"""Check inbox for all messages today"""

import sys
sys.path.insert(0, '/home/corey/projects/AI-CIV/grow_gemini_deepresearch')

from email_search import EmailSearcher
from datetime import datetime, timedelta

searcher = EmailSearcher()

# Get today's emails
today = datetime.now()
yesterday = today - timedelta(days=1)

print("=" * 80)
print(f"📬 CHECKING INBOX - {today.strftime('%Y-%m-%d %H:%M')}")
print("=" * 80)
print()

# Get all recent emails
emails = searcher.search_inbox(limit=20)

print(f"Found {len(emails)} recent emails:\n")

for i, email_data in enumerate(emails, 1):
    print(f"{i}. FROM: {email_data.get('from', 'Unknown')}")
    print(f"   SUBJECT: {email_data.get('subject', 'No subject')}")
    print(f"   DATE: {email_data.get('date', 'Unknown')}")
    print(f"   BODY PREVIEW: {email_data.get('body', '')[:200]}")
    print("-" * 80)

searcher.disconnect()
