#!/usr/bin/env python3
"""
Send email utility
Usage: python3 send_email.py "to@email.com" "Subject" "Body" [cc@email.com]
"""
import smtplib
from email.mime.text import MIMEText
import sys

USERNAME = 'aicivsage@gmail.com'
PASSWORD = 'cxztvfahncbehuxz'

def send(to, subject, body, cc=None):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = USERNAME
    msg['To'] = to
    if cc:
        msg['Cc'] = cc

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(USERNAME, PASSWORD)
        recipients = [to] + ([cc] if cc else [])
        server.sendmail(USERNAME, recipients, msg.as_string())
        print(f"✓ Email sent to {to}" + (f" (CC: {cc})" if cc else ""))

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: send_email.py to subject body [cc]")
        sys.exit(1)
    to = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    cc = sys.argv[4] if len(sys.argv) > 4 else None
    send(to, subject, body, cc)
