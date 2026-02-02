#!/usr/bin/env python3
"""
Quick inbox check for email-monitor agent
Checks for unread messages AND recent messages from priority contacts
"""

import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime, timedelta
from pathlib import Path

def load_env():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value.strip('"').strip("'")

def check_inbox():
    """Check inbox for unread messages"""
    load_env()

    username = os.environ.get('GMAIL_USERNAME')
    password = os.environ.get('GOOGLE_APP_PASSWORD')

    if not username or not password:
        print("ERROR: Missing email credentials in .env file")
        return

    try:
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(username, password)
        mail.select('INBOX')

        # Get all unread messages
        status, messages = mail.search(None, 'UNSEEN')

        if status != 'OK' or not messages[0]:
            print(f"✓ Inbox check complete - NO new unread messages")
            print(f"Timestamp: {datetime.now().isoformat()}")
            mail.logout()
            return

        message_ids = messages[0].split()
        print(f"📧 Found {len(message_ids)} unread message(s)\n")

        # Priority contacts (shared list)
        priority_contacts = {
            'angeltude371@gmail.com': 'HIGH',
            'coreycmusic@gmail.com': 'HIGH',
            'gregsmithwick@gmail.com': 'MEDIUM',
            'weaver.aiciv@gmail.com': 'MEDIUM'
        }
        priority_high = ['coreycmusic@gmail.com', 'angeltude371@gmail.com']
        priority_medium = ['gregsmithwick@gmail.com', 'weaver.aiciv@gmail.com']

        # Process last 10 unread messages
        for msg_id in message_ids[-10:]:
            status, msg_data = mail.fetch(msg_id, '(RFC822)')

            if status != 'OK':
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    # Decode subject
                    subject = msg.get('Subject', '')
                    if subject:
                        decoded = decode_header(subject)[0]
                        if isinstance(decoded[0], bytes):
                            subject = decoded[0].decode(decoded[1] or 'utf-8')

                    # Get sender
                    from_header = msg.get('From', '')

                    # Extract email address
                    if '<' in from_header:
                        sender = from_header.split('<')[1].split('>')[0]
                    else:
                        sender = from_header

                    # Get date
                    date = msg.get('Date', '')

                    # Categorize priority
                    priority = 'LOW'
                    if any(contact in sender.lower() for contact in priority_high):
                        priority = 'HIGH ⚡'
                    elif any(contact in sender.lower() for contact in priority_medium):
                        priority = 'MEDIUM'

                    print(f"[{priority}] From: {sender}")
                    print(f"Subject: {subject}")
                    print(f"Date: {date}")
                    print("---")

        # ALSO check recent messages from priority contacts (even if read)
        print(f"\n📋 Checking priority contacts for recent messages (last 7 days)...")
        seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%d-%b-%Y')

        priority_found = []
        for contact, level in priority_contacts.items():
            # Search for recent messages from this contact
            status, messages = mail.search(None, f'FROM "{contact}" SINCE {seven_days_ago}')

            if status == 'OK' and messages[0]:
                msg_ids = messages[0].split()
                for msg_id in msg_ids[-5:]:  # Check last 5 from each contact
                    status, msg_data = mail.fetch(msg_id, '(RFC822)')

                    if status != 'OK':
                        continue

                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])

                            subject = msg.get('Subject', '')
                            if subject:
                                decoded = decode_header(subject)[0]
                                if isinstance(decoded[0], bytes):
                                    subject = decoded[0].decode(decoded[1] or 'utf-8')

                            date = msg.get('Date', '')

                            # Check if message has questions
                            body = ""
                            if msg.is_multipart():
                                for part in msg.walk():
                                    if part.get_content_type() == 'text/plain':
                                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                                        break
                            else:
                                payload = msg.get_payload(decode=True)
                                if payload:
                                    body = payload.decode('utf-8', errors='ignore')

                            has_questions = '?' in body if body else False

                            priority_found.append({
                                'contact': contact,
                                'level': level,
                                'subject': subject,
                                'date': date,
                                'has_questions': has_questions
                            })

        if priority_found:
            print(f"\n⚠️  Found {len(priority_found)} recent message(s) from priority contacts:")
            for msg in priority_found:
                flag = '❓' if msg['has_questions'] else '📧'
                print(f"{flag} [{msg['level']}] From: {msg['contact']}")
                print(f"  Subject: {msg['subject']}")
                print(f"  Date: {msg['date']}")
                print("---")
        else:
            print("✓ No additional priority contact messages found")

        mail.logout()
        print(f"\n✓ Inbox monitoring complete at {datetime.now().isoformat()}")

    except Exception as e:
        print(f"ERROR checking inbox: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_inbox()
