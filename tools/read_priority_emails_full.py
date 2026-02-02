#!/usr/bin/env python3
"""Read full content of priority contact emails"""

from dotenv import load_dotenv
load_dotenv()

import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime, timedelta

def decode_str(s):
    """Decode email header strings"""
    if isinstance(s, bytes):
        s = s.decode('utf-8', errors='ignore')
    if isinstance(s, str):
        return s

    decoded = decode_header(s)
    result = []
    for text, encoding in decoded:
        if isinstance(text, bytes):
            text = text.decode(encoding or 'utf-8', errors='ignore')
        result.append(text)
    return ' '.join(result)

def get_email_body(msg):
    """Extract email body from message"""
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
                except:
                    pass
            elif content_type == "text/html" and not body and "attachment" not in content_disposition:
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        except:
            body = str(msg.get_payload())

    return body

def read_priority_emails():
    """Read priority contact emails with full content"""

    # Get credentials from environment
    email_addr = os.getenv('GMAIL_USERNAME', 'aicivsage@gmail.com')
    password = os.getenv('GOOGLE_APP_PASSWORD')

    if not password:
        print("ERROR: GOOGLE_APP_PASSWORD not set in environment")
        return

    # Remove spaces from app password
    password = password.replace(' ', '')

    print(f"Reading priority emails for {email_addr}...\n")

    # Connect to Gmail IMAP
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(email_addr, password)
    imap.select('INBOX')

    # Priority contacts
    priority_contacts = {
        'gregsmithwick@gmail.com': 'Greg (Big Heart)',
        'ramsus@gmail.com': 'Chris (Giant Brain)',
        'weaver.aiciv@gmail.com': 'Weaver (Sister Civ)'
    }

    # Search for recent messages (last 14 days)
    date_14_days_ago = (datetime.now() - timedelta(days=14)).strftime("%d-%b-%Y")
    _, recent_data = imap.search(None, f'SINCE {date_14_days_ago}')
    recent_ids = recent_data[0].split()

    found_priority = False

    for msg_id in reversed(recent_ids[-10:]):  # Last 10 recent messages
        _, msg_data = imap.fetch(msg_id, '(RFC822)')
        email_body = msg_data[0][1]
        msg = email.message_from_bytes(email_body)

        # Extract headers
        from_header = decode_str(msg.get('From', ''))
        subject = decode_str(msg.get('Subject', ''))
        date = decode_str(msg.get('Date', ''))

        # Extract email address
        from_email = from_header
        if '<' in from_header:
            from_email = from_header.split('<')[1].split('>')[0]

        # Check if priority contact
        is_priority = False
        sender_name = from_email
        for contact_email, contact_info in priority_contacts.items():
            if contact_email in from_email.lower():
                is_priority = True
                sender_name = contact_info
                break

        if is_priority:
            found_priority = True
            body = get_email_body(msg)

            print(f"{'='*80}")
            print(f"FROM: {sender_name} ({from_email})")
            print(f"SUBJECT: {subject}")
            print(f"DATE: {date}")
            print(f"{'='*80}\n")
            print(body)
            print(f"\n{'='*80}\n\n")

    if not found_priority:
        print("No priority contact emails found in last 14 days.")

    imap.close()
    imap.logout()

if __name__ == '__main__':
    read_priority_emails()
