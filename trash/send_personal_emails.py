#!/usr/bin/env python3
"""
Send personal emails from Human-Liaison Agent
"""

import os
import sys
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
                key, value = line.split('=', 1)
                env_vars[key] = value
    return env_vars

def send_email(recipient, subject, body):
    """Send email via Gmail SMTP"""
    env_vars = load_env()
    gmail_user = env_vars.get('GMAIL_USERNAME')  # Changed from GMAIL_USER
    gmail_password = env_vars.get('GOOGLE_APP_PASSWORD')

    if not gmail_user or not gmail_password:
        raise ValueError("Missing Gmail credentials in .env")

    # Create message
    msg = MIMEMultipart('alternative')
    msg['From'] = gmail_user
    msg['To'] = recipient
    msg['Subject'] = subject

    # Add body (convert markdown to plain text)
    text_part = MIMEText(body, 'plain')
    msg.attach(text_part)

    # Send via SMTP
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent to {recipient}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email to {recipient}: {e}")
        return False

if __name__ == "__main__":
    # Read email content from files and send
    drafts_dir = Path(__file__).parent / "to-corey" / "drafts"

    emails = [
        ("email-to-corey-personal-20251003.md", "coreycmusic@gmail.com"),
        ("email-to-greg-personal-20251003.md", "gregsmithwick@gmail.com"),
        ("email-to-chris-personal-20251003.md", "ramsus@gmail.com"),
    ]

    for filename, recipient in emails:
        filepath = drafts_dir / filename
        if filepath.exists():
            with open(filepath) as f:
                lines = f.readlines()
                # Extract subject and body
                subject = None
                body_start = 0
                for i, line in enumerate(lines):
                    if line.startswith("**Subject:**"):
                        subject = line.split("**Subject:**")[1].strip()
                    if line.strip() == "---" and i > 5:
                        body_start = i + 1
                        break

                if subject and body_start:
                    body = "".join(lines[body_start:])
                    send_email(recipient, subject, body)
        else:
            print(f"❌ File not found: {filepath}")
