#!/usr/bin/env python3
"""
Send email with attachments
Usage: python3 send_email_with_attachments.py "to" "subject" "body" file1 file2 ... [--cc email]
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import sys
import os

USERNAME = 'aicivsage@gmail.com'
PASSWORD = 'cxztvfahncbehuxz'

def send(to, subject, body, attachments, cc=None):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = USERNAME
    msg['To'] = to
    if cc:
        msg['Cc'] = cc

    msg.attach(MIMEText(body, 'plain'))

    for filepath in attachments:
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
            encoders.encode_base64(part)
            filename = os.path.basename(filepath)
            part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
            msg.attach(part)
            print(f"  Attached: {filename}")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(USERNAME, PASSWORD)
        recipients = [to] + ([cc] if cc else [])
        server.sendmail(USERNAME, recipients, msg.as_string())
        print(f"✓ Email sent to {to}" + (f" (CC: {cc})" if cc else ""))

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: send_email_with_attachments.py to subject body file1 [file2 ...] [--cc email]")
        sys.exit(1)

    to = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]

    # Parse attachments and optional --cc
    attachments = []
    cc = None
    i = 4
    while i < len(sys.argv):
        if sys.argv[i] == '--cc' and i + 1 < len(sys.argv):
            cc = sys.argv[i + 1]
            i += 2
        else:
            attachments.append(sys.argv[i])
            i += 1

    send(to, subject, body, attachments, cc)
