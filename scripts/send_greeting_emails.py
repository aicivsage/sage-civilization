#!/usr/bin/env python3
"""Send greeting emails to all priority contacts"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import json

# Load configuration
config_path = Path('config/email_config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

contacts_path = Path('config/priority_contacts.json')
with open(contacts_path, 'r') as f:
    contacts_data = json.load(f)

# Load HTML email template
html_path = Path('drafts/greeting_email_priority_list.html')
with open(html_path, 'r') as f:
    html_content = f.read()

# Email settings
FROM_EMAIL = config['email_address']
PASSWORD = config['app_password']
SMTP_SERVER = config['smtp_server']
SMTP_PORT = config['smtp_port']

def send_email(to_email, to_name):
    """Send greeting email to one contact"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{config['display_name']} <{FROM_EMAIL}>"
        msg['To'] = to_email
        msg['Subject'] = "Introducing Sage - AI Civilization"

        # Attach HTML
        msg.attach(MIMEText(html_content, 'html'))

        # Send
        print(f"Sending to {to_name} ({to_email})...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(FROM_EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"  ✓ Success: {to_name}")
        return True

    except Exception as e:
        print(f"  ✗ Failed: {to_name} - {e}")
        return False

def main():
    """Send emails to all priority contacts"""
    print("\n" + "="*60)
    print("SAGE AI CIVILIZATION - GREETING EMAILS")
    print("="*60 + "\n")

    contacts = contacts_data['priority_contacts']
    success_count = 0
    fail_count = 0

    for contact in contacts:
        if send_email(contact['email'], contact['name']):
            success_count += 1
        else:
            fail_count += 1
        print()  # Blank line

    print("="*60)
    print(f"SUMMARY: {success_count} sent successfully, {fail_count} failed")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
