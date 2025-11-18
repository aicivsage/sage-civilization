#!/usr/bin/env python3
"""
Check for GitHub security alert email from November 17
"""
import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

GMAIL_USERNAME = os.getenv('GMAIL_USERNAME')
GOOGLE_APP_PASSWORD = os.getenv('GOOGLE_APP_PASSWORD')

def connect_to_gmail():
    """Connect to Gmail IMAP"""
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(GMAIL_USERNAME, GOOGLE_APP_PASSWORD)
    return mail

def decode_email_part(part):
    """Decode email part safely"""
    if isinstance(part, bytes):
        try:
            return part.decode()
        except:
            return part.decode('utf-8', errors='ignore')
    return str(part)

def get_body(msg):
    """Extract email body"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
            elif content_type == "text/html" and not body and "attachment" not in content_disposition:
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode()
        except:
            body = str(msg.get_payload())

    return body

def search_github_emails(mail, days_back=7):
    """Search for GitHub emails in recent days"""
    mail.select('inbox')

    # Search for GitHub emails
    search_criteria = 'FROM "github.com"'
    status, messages = mail.search(None, search_criteria)

    if status != 'OK':
        print(f"Failed to search emails")
        return []

    email_ids = messages[0].split()

    # Get recent emails
    cutoff_date = datetime.now() - timedelta(days=days_back)

    results = []
    for email_id in reversed(email_ids):  # Most recent first
        status, msg_data = mail.fetch(email_id, '(RFC822)')

        if status != 'OK':
            continue

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Get date
                date_str = msg['Date']

                # Decode subject
                subject = decode_header(msg['Subject'])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()

                # Get sender
                from_addr = msg['From']

                # Get body
                body = get_body(msg)

                results.append({
                    'from': from_addr,
                    'date': date_str,
                    'subject': subject,
                    'body': body
                })

    return results

if __name__ == '__main__':
    print("Connecting to Gmail...")
    mail = connect_to_gmail()

    print("Searching for GitHub emails from last 7 days...")
    emails = search_github_emails(mail, days_back=7)

    print(f"\nFound {len(emails)} GitHub email(s):\n")

    for i, email_data in enumerate(emails, 1):
        print("=" * 80)
        print(f"Email {i}:")
        print("=" * 80)
        print(f"From: {email_data['from']}")
        print(f"Date: {email_data['date']}")
        print(f"Subject: {email_data['subject']}")
        print(f"\nBody:\n{email_data['body'][:2000]}")  # First 2000 chars
        if len(email_data['body']) > 2000:
            print(f"\n... (body truncated, total length: {len(email_data['body'])} chars)")
        print("\n")

    mail.close()
    mail.logout()
