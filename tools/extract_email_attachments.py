#!/usr/bin/env python3
"""
Extract attachments from emails
Usage: python3 extract_email_attachments.py [sender] [output_dir]
"""
import imaplib
import email
from email.header import decode_header
import sys
import os

USERNAME = 'aicivsage@gmail.com'
PASSWORD = 'cxztvfahncbehuxz'

def extract_attachments(sender, output_dir='./voice_bridge'):
    os.makedirs(output_dir, exist_ok=True)

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(USERNAME, PASSWORD)
    mail.select('INBOX')

    _, msgs = mail.search(None, f'FROM "{sender}"')
    msg_ids = msgs[0].split()

    saved = []
    for msg_id in msg_ids[-3:]:  # Last 3 emails
        _, data = mail.fetch(msg_id, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])

        if msg.is_multipart():
            for part in msg.walk():
                filename = part.get_filename()
                if filename:
                    # Decode filename if needed
                    if isinstance(filename, bytes):
                        filename = filename.decode()

                    filepath = os.path.join(output_dir, filename)
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    saved.append(filename)
                    print(f"✓ Saved: {filename}")

    mail.logout()

    if saved:
        print(f"\n{len(saved)} files saved to {output_dir}/")
    else:
        print("No attachments found")

if __name__ == '__main__':
    sender = sys.argv[1] if len(sys.argv) > 1 else 'russellkorus@gmail.com'
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './voice_bridge'
    extract_attachments(sender, output_dir)
