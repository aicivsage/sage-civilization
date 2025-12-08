#!/usr/bin/env python3
"""
Fetch specific email by subject and sender for detailed analysis
"""

import imaplib
import email
from email.header import decode_header
import json
import sys

def fetch_email(sender, subject_contains, since_date=None):
    """Fetch email matching criteria and print full body"""

    # Connect to Gmail
    mail = imaplib.IMAP4_SSL('imap.gmail.com')

    # Load credentials
    with open('/mnt/c/sage/sage-civilization/config/email_config.json') as f:
        config = json.load(f)

    mail.login(config['email'], config['password'])
    mail.select('inbox')

    # Build search criteria
    search_parts = [f'FROM "{sender}"']
    if since_date:
        search_parts.append(f'SINCE {since_date}')

    # Search
    status, messages = mail.search(None, *search_parts)

    if status != 'OK':
        print(f"Search failed: {status}")
        return

    email_ids = messages[0].split()
    if not email_ids:
        print(f"No emails found from {sender}")
        return

    print(f"Found {len(email_ids)} emails from {sender}")

    # Check each email for subject match
    for email_id in reversed(email_ids):  # Most recent first
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        if status != 'OK':
            continue

        email_body = msg_data[0][1]
        msg = email.message_from_bytes(email_body)

        subject = msg['subject']
        if subject_contains.lower() in subject.lower():
            print(f"\n{'='*80}")
            print(f"FOUND MATCHING EMAIL")
            print(f"{'='*80}")
            print(f"Subject: {subject}")
            print(f"From: {msg['from']}")
            print(f"Date: {msg['date']}")
            print(f"{'='*80}\n")

            # Extract body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == 'text/plain':
                        try:
                            body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                            break
                        except:
                            pass
            else:
                try:
                    body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                except:
                    pass

            print(body)
            print(f"\n{'='*80}\n")
            break

    mail.close()
    mail.logout()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: fetch_specific_email.py <sender_email> <subject_contains> [since_date]")
        sys.exit(1)

    sender = sys.argv[1]
    subject = sys.argv[2]
    since = sys.argv[3] if len(sys.argv) > 3 else None

    fetch_email(sender, subject, since)
