#!/usr/bin/env python3
"""Quick check for Angel Nally's latest email."""

import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime, timedelta

# Get credentials from environment
GMAIL_USER = os.environ.get('GMAIL_USERNAME')
GMAIL_PASS = os.environ.get('GOOGLE_APP_PASSWORD')

if not GMAIL_USER or not GMAIL_PASS:
    print("ERROR: Gmail credentials not found in environment")
    exit(1)

# Connect to Gmail
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(GMAIL_USER, GMAIL_PASS)
mail.select('inbox')

# Search for emails from Angel in last 7 days
since_date = (datetime.now() - timedelta(days=7)).strftime("%d-%b-%Y")
search_criteria = f'(FROM "angeltude371@gmail.com" SINCE {since_date})'

status, messages = mail.search(None, search_criteria)

if status != 'OK':
    print(f"Search failed: {status}")
    exit(1)

message_ids = messages[0].split()

if not message_ids:
    print("No recent emails from Angel found")
    exit(0)

# Get the most recent email
latest_id = message_ids[-1]
status, msg_data = mail.fetch(latest_id, '(RFC822)')

if status != 'OK':
    print(f"Fetch failed: {status}")
    exit(1)

# Parse the email
raw_email = msg_data[0][1]
msg = email.message_from_bytes(raw_email)

# Extract headers
subject = decode_header(msg['Subject'])[0][0]
if isinstance(subject, bytes):
    subject = subject.decode()

from_header = msg.get('From', '')
date_header = msg.get('Date', '')

# Extract body
body = ""
if msg.is_multipart():
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            try:
                body = part.get_payload(decode=True).decode()
                break
            except:
                pass
        elif part.get_content_type() == "text/html" and not body:
            try:
                body = part.get_payload(decode=True).decode()
            except:
                pass
else:
    try:
        body = msg.get_payload(decode=True).decode()
    except:
        body = str(msg.get_payload())

print("=" * 80)
print("ANGEL NALLY - LATEST EMAIL")
print("=" * 80)
print(f"From: {from_header}")
print(f"Subject: {subject}")
print(f"Date: {date_header}")
print("=" * 80)
print("BODY:")
print(body)
print("=" * 80)

mail.close()
mail.logout()
