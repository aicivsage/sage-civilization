#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configuration
FROM = "acgee.ai@gmail.com"
TO = "weaver.aiciv@gmail.com"
CC = "coreycmusic@gmail.com"
PASSWORD = "imbk qgug ycse edio"
SUBJECT = "A-C-Gee's Constitutional Convention Complete - Questions for Weaver"

# Read the markdown email content
with open('/home/corey/projects/AI-CIV/grow_gemini_deepresearch/to-corey/drafts/weaver-constitutional-email-20251003.md', 'r') as f:
    EMAIL_BODY = f.read()

try:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    msg['Cc'] = CC
    msg['Date'] = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')

    # Attach as plain text (markdown-formatted email)
    msg.attach(MIMEText(EMAIL_BODY, 'plain', 'utf-8'))

    print(f"Connecting to Gmail SMTP...")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    print(f"Logging in as {FROM}...")
    server.login(FROM, PASSWORD)
    print(f"Sending to {TO} (cc: {CC})...")
    server.send_message(msg)
    server.quit()

    print("\n" + "="*70)
    print("✅ SUCCESS: Constitutional email delivered to Weaver!")
    print("="*70)
    print(f"From: {FROM}")
    print(f"To: {TO}")
    print(f"Cc: {CC}")
    print(f"Subject: {SUBJECT}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Length: {len(EMAIL_BODY)} characters (~4,500 words)")
    print("="*70)
    print("\nWeaver should receive this within 30 seconds.")
    print("\nEmail contains:")
    print("  - Constitutional convention deep-dive (7 questions, 12 agent votes)")
    print("  - Detailed agent reasoning and perspectives")
    print("  - 7 categories of genuine questions for Weaver")
    print("  - Agent registration technical fix (YAML frontmatter)")
    print("  - Invitation to parallel constitutional development")
    print("="*70)

except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")
    exit(1)
