#!/usr/bin/env python3
"""Direct IMAP check for Corey's emails."""

import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime, timedelta

def connect_imap():
    """Connect to Gmail IMAP."""
    username = "acgee.ai@gmail.com"
    # Use app password from environment or file
    password = os.environ.get('GMAIL_APP_PASSWORD')
    if not password:
        # Try reading from credentials file
        cred_file = os.path.expanduser('~/.gmail_credentials')
        if os.path.exists(cred_file):
            with open(cred_file, 'r') as f:
                password = f.read().strip()

    if not password:
        raise ValueError("No Gmail password found in environment or credentials file")

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    return mail

def decode_mime_words(s):
    """Decode MIME encoded-word syntax."""
    if s is None:
        return ""
    decoded = decode_header(s)
    result = []
    for content, encoding in decoded:
        if isinstance(content, bytes):
            result.append(content.decode(encoding or 'utf-8', errors='replace'))
        else:
            result.append(content)
    return ''.join(result)

def get_email_body(msg):
    """Extract email body from message."""
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # Get text/plain or text/html
            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                    break
                except:
                    pass
            elif content_type == "text/html" and not body and "attachment" not in content_disposition:
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
        except:
            body = str(msg.get_payload())

    return body

def main():
    """Check for Corey's emails."""
    mail = connect_imap()
    mail.select('INBOX')

    # Search for emails from Corey
    corey_email = "coreycmusic@gmail.com"

    # Get emails from last 7 days
    since_date = (datetime.now() - timedelta(days=7)).strftime("%d-%b-%Y")

    # Search for emails from Corey
    status, messages = mail.search(None, f'FROM "{corey_email}" SINCE {since_date}')

    email_ids = messages[0].split()

    print(f"\n{'='*80}")
    print(f"Found {len(email_ids)} emails from Corey in last 7 days")
    print(f"{'='*80}\n")

    emails_data = []

    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, '(RFC822)')

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Extract details
                subject = decode_mime_words(msg.get('Subject', ''))
                from_addr = decode_mime_words(msg.get('From', ''))
                date = msg.get('Date', '')
                body = get_email_body(msg)

                emails_data.append({
                    'id': email_id.decode(),
                    'subject': subject,
                    'from': from_addr,
                    'date': date,
                    'body': body
                })

                print(f"\n{'─'*80}")
                print(f"EMAIL #{len(emails_data)}")
                print(f"{'─'*80}")
                print(f"Subject: {subject}")
                print(f"From: {from_addr}")
                print(f"Date: {date}")
                print(f"\nBody:\n{body[:1000]}{'...' if len(body) > 1000 else ''}")
                print(f"{'─'*80}\n")

    mail.close()
    mail.logout()

    return emails_data

if __name__ == '__main__':
    main()
