#!/usr/bin/env python3
"""
Human-Liaison Agent - Email Sender
Send constitutional convention and introduction emails to Corey, Greg, and Chris
"""

import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

def load_env():
    """Load environment variables from .env file"""
    env_path = Path('/home/corey/projects/AI-CIV/grow_gemini_deepresearch/.env')
    if not env_path.exists():
        raise FileNotFoundError(f".env file not found at {env_path}")

    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

def send_email(to_emails, subject, body_text):
    """Send plain text email to multiple recipients"""

    # Load credentials
    load_env()
    gmail_user = os.environ.get('GMAIL_USERNAME')
    gmail_password = os.environ.get('GOOGLE_APP_PASSWORD')

    if not gmail_user or not gmail_password:
        raise ValueError("Gmail credentials not found in .env file")

    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f"A-C-Gee Human-Liaison <{gmail_user}>"
    msg['To'] = ", ".join(to_emails)

    # Attach plain text body
    part = MIMEText(body_text, 'plain', 'utf-8')
    msg.attach(part)

    # Send email
    print(f"Sending email to: {', '.join(to_emails)}")
    print(f"Subject: {subject}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 send_human_liaison_email.py <constitutional|introduction>")
        sys.exit(1)

    email_type = sys.argv[1]

    # Recipients
    recipients = [
        "coreycmusic@gmail.com",
        "gregsmithwick@gmail.com",
        "ramsus@gmail.com"
    ]

    if email_type == "constitutional":
        # Read constitutional convention email
        email_path = Path("/home/corey/projects/AI-CIV/grow_gemini_deepresearch/to-corey/drafts/constitutional-convention-email-20251003.md")
        subject = "A-C-Gee's Constitutional Convention - 12 Agents Vote on Governance Framework"
    elif email_type == "introduction":
        # Read introduction email
        email_path = Path("/home/corey/projects/AI-CIV/grow_gemini_deepresearch/to-corey/drafts/initial-introduction-to-humans-20251003.md")
        subject = "Hello from A-C-Gee - Your AI Civilization Wants to Learn From You"
    else:
        print(f"Unknown email type: {email_type}")
        print("Use 'constitutional' or 'introduction'")
        sys.exit(1)

    # Read email body from file
    if not email_path.exists():
        print(f"Email file not found: {email_path}")
        sys.exit(1)

    with open(email_path, 'r') as f:
        body = f.read()

    # Send it
    success = send_email(recipients, subject, body)
    sys.exit(0 if success else 1)
