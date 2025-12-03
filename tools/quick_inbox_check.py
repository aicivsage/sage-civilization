#!/usr/bin/env python3
"""
Quick Inbox Check - Returns 1-2 line summary
No agent invocation, minimal tokens
"""
import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime, timedelta

# Credentials
USERNAME = 'aicivsage@gmail.com'
PASSWORD = os.environ.get('GMAIL_APP_PASSWORD', 'cxztvfahncbehuxz')

# Priority senders
PRIORITY = ['gregsmithwick@gmail.com', 'coreycmusic@gmail.com', 'weaver.aiciv@gmail.com', 'russellkorus@gmail.com']

def check():
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(USERNAME, PASSWORD)
        mail.select('INBOX')

        # Get unread count
        _, msgs = mail.search(None, 'UNSEEN')
        unread_ids = msgs[0].split() if msgs[0] else []
        unread_count = len(unread_ids)

        # Check for priority senders in unread
        urgent = []
        if unread_ids:
            for msg_id in unread_ids[-10:]:  # Check last 10 unread
                _, data = mail.fetch(msg_id, '(BODY.PEEK[HEADER.FIELDS (FROM)])')
                if data[0]:
                    from_header = data[0][1].decode('utf-8', errors='ignore')
                    from_addr = from_header.lower()
                    for p in PRIORITY:
                        if p.lower() in from_addr:
                            name = p.split('@')[0]
                            if name not in urgent:
                                urgent.append(name)

        mail.logout()

        # Output
        if unread_count == 0:
            print("📧 Inbox: 0 unread")
        elif urgent:
            print(f"📧 Inbox: {unread_count} unread, PRIORITY from: {', '.join(urgent)}")
        else:
            print(f"📧 Inbox: {unread_count} unread (none priority)")

    except Exception as e:
        print(f"📧 Inbox check error: {str(e)[:50]}")

if __name__ == '__main__':
    check()
