#!/usr/bin/env python3
"""Read recent priority emails in full"""

from dotenv import load_dotenv
load_dotenv()

import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime, timedelta
import re

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

def strip_html(html):
    """Basic HTML stripping"""
    # Remove HTML tags
    text = re.sub('<[^<]+?>', '', html)
    # Decode common entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&amp;', '&')
    return text

def get_email_body(msg):
    """Extract full email body"""
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    body = payload.decode('utf-8', errors='ignore')
                    break
            elif content_type == "text/html" and not body:
                payload = part.get_payload(decode=True)
                if payload:
                    html_body = payload.decode('utf-8', errors='ignore')
                    body = strip_html(html_body)
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode('utf-8', errors='ignore')

    return body

def read_recent_emails():
    """Read full content of recent priority emails"""

    # Get credentials from environment
    email_addr = os.getenv('GMAIL_USERNAME', 'acgee.ai@gmail.com')
    password = os.getenv('GOOGLE_APP_PASSWORD')

    if not password:
        print("ERROR: GOOGLE_APP_PASSWORD not set in environment")
        return

    # Remove spaces from app password (Google format)
    password = password.replace(' ', '')

    print(f"Reading recent emails from {email_addr}...")

    # Connect to Gmail IMAP
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(email_addr, password)

    # Select inbox
    imap.select('INBOX')

    # Priority contacts
    priority_contacts = {
        'coreycmusic@gmail.com': 'Corey',
        'gregsmithwick@gmail.com': 'Greg',
        'ramsus@gmail.com': 'Chris',
        'weaver.aiciv@gmail.com': 'Weaver',
        'afirststepcounseling@gmail.com': 'Rosanne',
        'quirkygirl4242@gmail.com': 'Kodi',
        'angeltude371@gmail.com' : 'Angel'
     }

    # Get last 3 days of emails
    date_3_days_ago = (datetime.now() - timedelta(days=3)).strftime("%d-%b-%Y")
    _, recent_data = imap.search(None, f'SINCE {date_3_days_ago}')
    recent_ids = recent_data[0].split()

    priority_emails = []

    # Collect priority emails
    for msg_id in recent_ids:
        _, msg_data = imap.fetch(msg_id, '(RFC822)')
        email_body = msg_data[0][1]
        msg = email.message_from_bytes(email_body)

        from_header = decode_str(msg.get('From', ''))
        from_email = from_header
        if '<' in from_header:
            from_email = from_header.split('<')[1].split('>')[0]

        # Check if from priority contact
        for contact_email, contact_name in priority_contacts.items():
            if contact_email in from_email.lower():
                subject = decode_str(msg.get('Subject', ''))
                date = decode_str(msg.get('Date', ''))
                body = get_email_body(msg)

                priority_emails.append({
                    'from': contact_name,
                    'email': from_email,
                    'subject': subject,
                    'date': date,
                    'body': body
                })
                break

    # Sort by date (most recent first)
    priority_emails.sort(key=lambda x: x['date'], reverse=True)

    # Print last 5 emails
    print(f"\n=== LAST 5 PRIORITY EMAILS ===\n")

    for i, email_data in enumerate(priority_emails[:5], 1):
        print(f"\n{'='*80}")
        print(f"EMAIL {i}: {email_data['from']}")
        print(f"{'='*80}")
        print(f"Subject: {email_data['subject']}")
        print(f"Date: {email_data['date']}")
        print(f"From: {email_data['email']}")
        print(f"\n{'-'*80}")
        print(f"BODY:")
        print(f"{'-'*80}")
        print(email_data['body'][:1500])  # Limit to first 1500 chars
        if len(email_data['body']) > 1500:
            print("\n... [truncated] ...")
        print(f"\n{'='*80}\n")

    imap.close()
    imap.logout()

if __name__ == '__main__':
    read_recent_emails()
