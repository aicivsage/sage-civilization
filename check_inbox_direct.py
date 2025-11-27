#!/usr/bin/env python3
"""Direct IMAP inbox checker for A-C-Gee"""

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

def check_inbox():
    """Check A-C-Gee Gmail inbox"""

    # Get credentials from environment
    email_addr = os.getenv('GMAIL_USERNAME', 'acgee.ai@gmail.com')
    password = os.getenv('GOOGLE_APP_PASSWORD')

    if not password:
        print("ERROR: GOOGLE_APP_PASSWORD not set in environment")
        return

    # Remove spaces from app password (Google format)
    password = password.replace(' ', '')

    print(f"Connecting to Gmail inbox for {email_addr}...")

    # Connect to Gmail IMAP
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(email_addr, password)

    # Select inbox
    imap.select('INBOX')

    # Search for all unseen messages
    _, unseen_data = imap.search(None, 'UNSEEN')
    unseen_ids = unseen_data[0].split()

    # Search for recent messages (last 7 days)
    date_7_days_ago = (datetime.now() - timedelta(days=7)).strftime("%d-%b-%Y")
    _, recent_data = imap.search(None, f'SINCE {date_7_days_ago}')
    recent_ids = recent_data[0].split()

    print(f"\n=== INBOX STATUS ===")
    print(f"Unread messages: {len(unseen_ids)}")
    print(f"Recent messages (7 days): {len(recent_ids)}")

    # Priority contacts
    priority_contacts = {
        'coreycmusic@gmail.com': 'Corey (HIGHEST)',
        'gregsmithwick@gmail.com': 'Greg (Big Heart)',
        'ramsus@gmail.com': 'Chris (Giant Brain)',
        'weaver.aiciv@gmail.com': 'Weaver (Sister Civ)'
    }

    if unseen_ids:
        print(f"\n=== UNREAD MESSAGES ({len(unseen_ids)}) ===")

        for msg_id in unseen_ids:
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

            # Check priority
            priority = "NORMAL"
            sender_name = from_email
            for contact_email, contact_info in priority_contacts.items():
                if contact_email in from_email.lower():
                    priority = "HIGH"
                    sender_name = contact_info
                    break

            print(f"\n[{priority}] From: {sender_name}")
            print(f"  Email: {from_email}")
            print(f"  Subject: {subject}")
            print(f"  Date: {date}")

            # Get body preview
            body_preview = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            body_preview = payload.decode('utf-8', errors='ignore')[:200]
                            break
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body_preview = payload.decode('utf-8', errors='ignore')[:200]

            if body_preview:
                print(f"  Preview: {body_preview.strip()[:150]}...")

    else:
        print("\n✅ No unread messages in inbox")

    # Check recent messages from priority contacts
    print(f"\n=== RECENT MESSAGES FROM PRIORITY CONTACTS ===")
    priority_found = False

    for msg_id in reversed(recent_ids[-20:]):  # Last 20 recent messages
        _, msg_data = imap.fetch(msg_id, '(RFC822 FLAGS)')
        email_body = msg_data[0][1]
        msg = email.message_from_bytes(email_body)

        from_header = decode_str(msg.get('From', ''))
        from_email = from_header
        if '<' in from_header:
            from_email = from_header.split('<')[1].split('>')[0]

        # Check if from priority contact
        for contact_email, contact_info in priority_contacts.items():
            if contact_email in from_email.lower():
                priority_found = True
                subject = decode_str(msg.get('Subject', ''))
                date = decode_str(msg.get('Date', ''))

                # Check if seen
                flags = str(msg_data[0][0])
                is_read = '\\Seen' in flags
                status = "READ" if is_read else "UNREAD"

                print(f"\n[{status}] {contact_info}")
                print(f"  Subject: {subject}")
                print(f"  Date: {date}")
                break

    if not priority_found:
        print("No recent messages from priority contacts")

    imap.close()
    imap.logout()

    print(f"\n=== CHECK COMPLETE ===")
    print(f"Timestamp: {datetime.now().isoformat()}")

if __name__ == '__main__':
    check_inbox()
