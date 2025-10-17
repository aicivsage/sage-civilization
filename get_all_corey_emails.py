#!/usr/bin/env python3
"""Get ALL emails from Corey, not just last 5."""

import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime, timedelta

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
    """Get ALL emails from Corey from last 7 days."""
    # Connect
    username = "acgee.ai@gmail.com"
    password = os.getenv('GOOGLE_APP_PASSWORD')
    if not password:
        print("ERROR: GOOGLE_APP_PASSWORD not set")
        return

    password = password.replace(' ', '')

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select('INBOX')

    # Search for ALL emails from Corey in last 7 days
    since_date = (datetime.now() - timedelta(days=7)).strftime("%d-%b-%Y")
    status, messages = mail.search(None, f'FROM "coreycmusic@gmail.com" SINCE {since_date}')

    email_ids = messages[0].split()

    print(f"\n{'='*80}")
    print(f"FOUND {len(email_ids)} EMAILS FROM COREY")
    print(f"{'='*80}\n")

    emails_data = []

    # Process in reverse chronological order (newest first)
    for email_id in reversed(email_ids):
        status, msg_data = mail.fetch(email_id, '(RFC822)')

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

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

                print(f"\n{'='*80}")
                print(f"EMAIL #{len(emails_data)}")
                print(f"{'='*80}")
                print(f"Subject: {subject}")
                print(f"Date: {date}")
                print(f"\n{body}\n")

    mail.close()
    mail.logout()

    return emails_data

if __name__ == '__main__':
    main()
