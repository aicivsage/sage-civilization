#!/usr/bin/env python3
"""
Quick script to find and read Kodi Mitchell's email
"""
import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GMAIL_USERNAME = os.getenv('GMAIL_USERNAME')
GOOGLE_APP_PASSWORD = os.getenv('GOOGLE_APP_PASSWORD')

def connect_to_gmail():
    """Connect to Gmail IMAP"""
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(GMAIL_USERNAME, GOOGLE_APP_PASSWORD)
    return mail

def search_emails_from(mail, from_address, limit=5):
    """Search for emails from specific address"""
    mail.select('inbox')

    # Search for emails from this address
    search_criteria = f'FROM "{from_address}"'
    status, messages = mail.search(None, search_criteria)

    if status != 'OK':
        print(f"Failed to search emails")
        return []

    email_ids = messages[0].split()
    email_ids = email_ids[-limit:]  # Get most recent

    results = []
    for email_id in reversed(email_ids):  # Most recent first
        status, msg_data = mail.fetch(email_id, '(RFC822)')

        if status != 'OK':
            continue

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Decode subject
                subject = decode_header(msg['Subject'])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()

                # Get body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                        elif part.get_content_type() == "text/html" and not body:
                            body = part.get_payload(decode=True).decode()
                else:
                    body = msg.get_payload(decode=True).decode()

                results.append({
                    'from': msg['From'],
                    'subject': subject,
                    'date': msg['Date'],
                    'body': body[:1000]  # First 1000 chars
                })

    return results

def main():
    try:
        print("Connecting to Gmail...")
        mail = connect_to_gmail()

        print("Searching for emails from Kodi Mitchell (quirkygirl4242@gmail.com)...")
        emails = search_emails_from(mail, "quirkygirl4242@gmail.com", limit=3)

        if not emails:
            print("\nNo emails found from Kodi Mitchell")
            return

        print(f"\nFound {len(emails)} email(s) from Kodi Mitchell:\n")

        for i, email_data in enumerate(emails, 1):
            print(f"\n{'='*80}")
            print(f"Email {i}:")
            print(f"{'='*80}")
            print(f"From: {email_data['from']}")
            print(f"Date: {email_data['date']}")
            print(f"Subject: {email_data['subject']}")
            print(f"\nBody Preview:\n{email_data['body']}")
            print(f"{'='*80}\n")

        mail.close()
        mail.logout()

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
