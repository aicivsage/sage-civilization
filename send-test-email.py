#!/usr/bin/env python3
"""
Send test email to Greg to verify delivery
"""

import sys
sys.path.insert(0, '/mnt/c/sage/sage-civilization/tools')

from send_html_email import send_html_email

# Read test email HTML
with open('/mnt/c/sage/sage-civilization/test-email-greg.html', 'r') as f:
    html_content = f.read()

print("=" * 70)
print("EMAIL DELIVERY TEST")
print("=" * 70)
print("\nSending test email to Greg...")
print("From: acgee.ai@gmail.com")
print("To: gregsmithwick@gmail.com")
print("Subject: 🔍 Email Delivery Test - Please Confirm Receipt")
print("\nThis will help diagnose why earlier daily summary wasn't received.")
print("\n" + "=" * 70)

result = send_html_email(
    to='gregsmithwick@gmail.com',
    subject='🔍 Email Delivery Test - Please Confirm Receipt',
    html_body=html_content,
    skip_duplicate_check=True  # Send even if duplicate (this is a test)
)

print("\n" + "=" * 70)
if result:
    print("✓ Test email sent successfully!")
    print("\nNext steps:")
    print("1. Wait for Greg to confirm receipt (reply or Telegram)")
    print("2. If he receives this, check spam folder for earlier email")
    print("3. If he doesn't receive this either, need to set up Sage Gmail account")
else:
    print("✗ Test email FAILED to send")
    print("\nThis suggests SMTP configuration issue.")
    print("Investigate send_html_email.py credentials and SMTP settings.")
print("=" * 70)

sys.exit(0 if result else 1)
