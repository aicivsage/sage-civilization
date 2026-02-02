#!/usr/bin/env python3
"""Fetch all unread emails with full content"""

from dotenv import load_dotenv
load_dotenv()

import imaplib
import email
from email.header import decode_header
import json
import os
from datetime import datetime

def decode_str(s):
    """Decode email header string"""
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

def get_body(msg):
    """Extract email body"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in disposition:
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
                except:
                    pass
            elif content_type == "text/html" and "attachment" not in disposition and not body:
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

def main():
    # Get credentials from environment
    email_addr = os.getenv('GMAIL_USERNAME', 'acgee.ai@gmail.com')
    password = os.getenv('GOOGLE_APP_PASSWORD')

    if not password:
        print("ERROR: GOOGLE_APP_PASSWORD not set in environment")
        return

    # Remove spaces from app password
    password = password.replace(' ', '')

    print(f"Connecting to Gmail for {email_addr}...")

    # Connect to Gmail
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_addr, password)
    mail.select("inbox")

    # Search for unread messages
    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split()

    print(f"\nFound {len(email_ids)} unread emails\n")
    print("="*80)

    emails = []

    for email_id in email_ids:
        # Fetch email
        status, msg_data = mail.fetch(email_id, "(RFC822)")

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Extract metadata
                subject = decode_str(msg.get("Subject", ""))
                sender = decode_str(msg.get("From", ""))
                date = msg.get("Date", "")

                # Extract body
                body = get_body(msg)

                email_data = {
                    "id": email_id.decode(),
                    "from": sender,
                    "subject": subject,
                    "date": date,
                    "body": body
                }

                emails.append(email_data)

                print(f"\n📧 EMAIL {len(emails)}")
                print(f"From: {sender}")
                print(f"Subject: {subject}")
                print(f"Date: {date}")
                print(f"\nBody:")
                print("-" * 80)
                print(body[:3000])  # Show first 3000 chars for preview
                if len(body) > 3000:
                    print(f"\n... (body continues, {len(body)} total chars)")
                print("-" * 80)

    mail.close()
    mail.logout()

    # Save to JSON
    output_file = "/mnt/c/sage/sage-civilization/drafts/unread_emails_full.json"
    with open(output_file, 'w') as f:
        json.dump(emails, f, indent=2)

    print(f"\n✅ Saved {len(emails)} emails to {output_file}")

if __name__ == "__main__":
    main()
