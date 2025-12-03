#!/usr/bin/env python3
"""
Read recent emails from specified sender
Usage: python3 read_recent_emails.py [sender_email] [count]
"""
import imaplib
import email
from email.header import decode_header
import sys

USERNAME = 'aicivsage@gmail.com'
PASSWORD = 'cxztvfahncbehuxz'

def read_emails(sender=None, count=3):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(USERNAME, PASSWORD)
    mail.select('INBOX')

    if sender:
        _, msgs = mail.search(None, f'FROM "{sender}"')
    else:
        _, msgs = mail.search(None, 'UNSEEN')

    msg_ids = msgs[0].split()

    for msg_id in msg_ids[-count:]:
        _, data = mail.fetch(msg_id, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])

        subject = decode_header(msg['Subject'])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()

        print(f"\n{'='*60}")
        print(f"Subject: {subject}")
        print(f"From: {msg['From']}")
        print(f"Date: {msg['Date']}")
        print(f"{'='*60}")

        body = None
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype == 'text/plain':
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
                elif ctype == 'text/html' and not body:
                    # Strip HTML tags roughly
                    import re
                    html = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    body = re.sub('<[^<]+?>', '', html)
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                body = payload.decode('utf-8', errors='ignore')

        if body:
            print(body[:5000])
        else:
            print("[No readable body content]")

    mail.logout()

if __name__ == '__main__':
    sender = sys.argv[1] if len(sys.argv) > 1 else None
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    read_emails(sender, count)
