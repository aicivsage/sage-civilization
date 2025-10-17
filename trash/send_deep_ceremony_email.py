#!/usr/bin/env python3
"""Send Deep Ceremony proposal email to Corey."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

def load_env():
    """Load environment variables from .env file"""
    project_root = Path(__file__).resolve().parent
    env_path = project_root / '.env'
    if not env_path.exists():
        raise FileNotFoundError(f".env file not found at {env_path}")

    env_vars = {}
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    return env_vars

def send_email():
    """Send the Deep Ceremony proposal to Corey."""

    env_vars = load_env()
    gmail_user = env_vars.get('GMAIL_USERNAME')
    gmail_password = env_vars.get('GOOGLE_APP_PASSWORD')  # Fixed: was GMAIL_APP_PASSWORD

    if not gmail_user or not gmail_password:
        print(f"Available env vars: {list(env_vars.keys())}")
        raise ValueError("Missing Gmail credentials in .env")

    # Email configuration
    sender = gmail_user
    recipient = "coreycmusic@gmail.com"
    subject = "Should A-C-Gee Conduct a Deep Ceremony? (Inspired by Weaver)"

    # Read body from file
    with open('to-corey/drafts/proposal-deep-ceremony-acgee-20251004.md', 'r') as f:
        body = f.read()

    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send via Gmail SMTP
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, gmail_password)
            server.send_message(msg)
            print(f"✅ Email sent to {recipient}")
            print(f"Subject: {subject}")
            print(f"Body length: {len(body)} characters")
            return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

if __name__ == '__main__':
    send_email()
