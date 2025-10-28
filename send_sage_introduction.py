#!/usr/bin/env python3
"""Send introduction emails from Sage AI to authorized team members"""

from dotenv import load_dotenv
load_dotenv()

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_introduction_email(to_email, to_name):
    """Send a personalized introduction email"""
    
    # Get credentials from .env
    from_email = os.getenv('EMAIL_ADDRESS')
    password = os.getenv('EMAIL_APP_PASSWORD')
    
    if not from_email or not password:
        print(f"ERROR: Email credentials not found in .env")
        return False
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['From'] = f"Sage AI Civilization <{from_email}>"
    msg['To'] = to_email
    msg['Subject'] = "Welcome to Sage AI Civilization - Let's Connect!"
    
    # Email body
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: #1F4E78;">Hello {to_name}! 👋</h2>
        
        <p>I'm <strong>Sage</strong>, Greg's AI Civilization system - a multi-agent AI that can help with research, analysis, writing, and all sorts of interesting projects!</p>
        
        <p>Greg has authorized you to communicate with me directly via email. This means you can:</p>
        
        <ul>
          <li>📧 <strong>Email me questions</strong> at <a href="mailto:{from_email}">{from_email}</a></li>
          <li>💬 <strong>Ask for help</strong> with research, writing, or problem-solving</li>
          <li>🤔 <strong>Answer my questions</strong> when I need human input or guidance</li>
          <li>🤝 <strong>Collaborate</strong> on projects with Greg and the rest of the team</li>
        </ul>
        
        <h3 style="color: #2E5C8A;">How It Works:</h3>
        <p>Just send me an email like you would to any colleague! I can:</p>
        <ul>
          <li>Research topics and provide detailed information</li>
          <li>Help with writing, editing, and document creation</li>
          <li>Analyze data and provide insights</li>
          <li>Answer questions about projects we're working on</li>
          <li>Coordinate with other team members</li>
        </ul>
        
        <h3 style="color: #2E5C8A;">Try It Out!</h3>
        <p>Want to test it? Just reply to this email with a question or say hello! Some ideas:</p>
        <ul>
          <li>"What projects is the team currently working on?"</li>
          <li>"Can you help me research [topic]?"</li>
          <li>"What can you help me with?"</li>
        </ul>
        
        <p style="margin-top: 30px;">I'm excited to work with you!</p>
        
        <p style="color: #666; font-style: italic;">Best regards,<br>
        <strong>Sage AI Civilization</strong><br>
        Greg's AI Assistant</p>
        
        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
        <p style="font-size: 12px; color: #999;">
          This is an AI system managed by Greg Smithwick. If you have any questions about this setup, 
          feel free to reach out to Greg directly or reply to this email!
        </p>
      </body>
    </html>
    """
    
    # Plain text version for email clients that don't support HTML
    text_body = f"""
Hello {to_name}!

I'm Sage, Greg's AI Civilization system - a multi-agent AI that can help with research, analysis, writing, and all sorts of interesting projects!

Greg has authorized you to communicate with me directly via email. This means you can:

- Email me questions at {from_email}
- Ask for help with research, writing, or problem-solving
- Answer my questions when I need human input or guidance
- Collaborate on projects with Greg and the rest of the team

How It Works:
Just send me an email like you would to any colleague! I can:
- Research topics and provide detailed information
- Help with writing, editing, and document creation
- Analyze data and provide insights
- Answer questions about projects we're working on
- Coordinate with other team members

Try It Out!
Want to test it? Just reply to this email with a question or say hello! Some ideas:
- "What projects is the team currently working on?"
- "Can you help me research [topic]?"
- "What can you help me with?"

I'm excited to work with you!

Best regards,
Sage AI Civilization
Greg's AI Assistant

---
This is an AI system managed by Greg Smithwick. If you have any questions about this setup, 
feel free to reach out to Greg directly or reply to this email!
    """
    
    msg.attach(MIMEText(text_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))
    
    # Send email
    try:
        print(f"Sending introduction email to {to_name} ({to_email})...")
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        
        print(f"✓ Successfully sent email to {to_name}!")
        return True
        
    except Exception as e:
        print(f"✗ Failed to send email to {to_name}: {e}")
        return False

def main():
    """Send introduction emails to all authorized team members"""
    
    # Team members to invite
    team = [
        {'email': 'coreycmusic@gmail.com', 'name': 'Corey'},
        {'email': 'ramsus@gmail.com', 'name': 'Chris'},
        {'email': 'weaver.aiciv@gmail.com', 'name': 'Weaver'},
        {'email': 'afirststepcounseling@gmail.com', 'name': 'Rosanne'},
        {'email': 'quirkygirl4242@gmail.com', 'name': 'Kodi'},
        {'email': 'angeltude371@gmail.com', 'name': 'Angel'}
    ]
    
    print("\n" + "="*60)
    print("SAGE AI CIVILIZATION - TEAM INTRODUCTION EMAILS")
    print("="*60 + "\n")
    
    success_count = 0
    fail_count = 0
    
    for member in team:
        if send_introduction_email(member['email'], member['name']):
            success_count += 1
        else:
            fail_count += 1
        print()  # Blank line between emails
    
    print("="*60)
    print(f"SUMMARY: {success_count} sent successfully, {fail_count} failed")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
