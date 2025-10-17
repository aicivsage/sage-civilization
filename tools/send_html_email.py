#!/usr/bin/env python3
"""
Reusable HTML Email Sender for A-C-Gee Civilization
Provides clean, professional HTML emails with proper styling.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import List, Optional, Union
import re
from datetime import datetime
import json
import hashlib

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
FROM_EMAIL = 'acgee.ai@gmail.com'
FROM_NAME = 'A-C-Gee AI Civilization'
PASSWORD = 'imbk qgug ycse edio'

# Template path
TEMPLATE_PATH = Path(__file__).parent.parent / 'templates' / 'email_template.html'

# Sent emails tracking
SENT_EMAILS_PATH = Path(__file__).parent.parent / 'memories' / 'agents' / 'email-reporter' / 'sent_emails.json'


def _get_email_hash(to: Union[str, List[str]], subject: str, content_preview: str) -> str:
    """Generate unique hash for email to detect duplicates."""
    to_list = [to] if isinstance(to, str) else to
    to_str = ','.join(sorted(to_list))
    content = f"{to_str}|{subject}|{content_preview[:100]}"
    return hashlib.md5(content.encode()).hexdigest()


def _load_sent_emails() -> List[dict]:
    """Load sent emails tracking log."""
    if not SENT_EMAILS_PATH.exists():
        SENT_EMAILS_PATH.parent.mkdir(parents=True, exist_ok=True)
        return []
    try:
        with open(SENT_EMAILS_PATH, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def _save_sent_email(to: Union[str, List[str]], subject: str, content_preview: str) -> None:
    """Record sent email to prevent duplicates."""
    sent_emails = _load_sent_emails()
    email_hash = _get_email_hash(to, subject, content_preview)

    sent_emails.append({
        'hash': email_hash,
        'to': to if isinstance(to, str) else to,
        'subject': subject,
        'preview': content_preview[:100],
        'timestamp': datetime.now().isoformat()
    })

    # Keep only last 100 emails
    sent_emails = sent_emails[-100:]

    SENT_EMAILS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SENT_EMAILS_PATH, 'w') as f:
        json.dump(sent_emails, f, indent=2)


def _check_duplicate(to: Union[str, List[str]], subject: str, content_preview: str) -> bool:
    """Check if this email was recently sent (within last 100 emails)."""
    sent_emails = _load_sent_emails()
    email_hash = _get_email_hash(to, subject, content_preview)

    for sent in sent_emails:
        if sent.get('hash') == email_hash:
            return True
    return False


def markdown_to_html(markdown_text: str) -> str:
    """
    Convert basic Markdown to HTML.
    Supports: headers, bold, italic, lists, code blocks, links.

    Args:
        markdown_text: Markdown formatted text

    Returns:
        HTML formatted text
    """
    html = markdown_text

    # Headers (###, ##, #)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # Bold and italic
    html = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    html = re.sub(r'___(.*?)___', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'__(.*?)__', r'<strong>\1</strong>', html)
    html = re.sub(r'_(.*?)_', r'<em>\1</em>', html)

    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # Links [text](url)
    html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)

    # Code blocks (```)
    html = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)

    # Unordered lists
    lines = html.split('\n')
    in_ul = False
    result = []
    for line in lines:
        if re.match(r'^\s*[-*]\s+', line):
            if not in_ul:
                result.append('<ul>')
                in_ul = True
            item = re.sub(r'^\s*[-*]\s+', '', line)
            result.append(f'<li>{item}</li>')
        else:
            if in_ul:
                result.append('</ul>')
                in_ul = False
            result.append(line)
    if in_ul:
        result.append('</ul>')
    html = '\n'.join(result)

    # Ordered lists
    lines = html.split('\n')
    in_ol = False
    result = []
    for line in lines:
        if re.match(r'^\s*\d+\.\s+', line):
            if not in_ol:
                result.append('<ol>')
                in_ol = True
            item = re.sub(r'^\s*\d+\.\s+', '', line)
            result.append(f'<li>{item}</li>')
        else:
            if in_ol:
                result.append('</ol>')
                in_ol = False
            result.append(line)
    if in_ol:
        result.append('</ol>')
    html = '\n'.join(result)

    # Paragraphs (wrap non-HTML lines)
    lines = html.split('\n')
    result = []
    for line in lines:
        if line.strip() and not re.match(r'^\s*<', line):
            result.append(f'<p>{line}</p>')
        else:
            result.append(line)
    html = '\n'.join(result)

    return html


def create_html_email(
    subject: str,
    content: str,
    from_name: str = FROM_NAME,
    is_markdown: bool = False,
    meta_info: Optional[str] = None
) -> str:
    """
    Create HTML email from content using template.

    Args:
        subject: Email subject line
        content: Email body (HTML or Markdown)
        from_name: Display name for sender
        is_markdown: If True, convert content from Markdown to HTML
        meta_info: Optional metadata to display at top (e.g., "From: X, To: Y, Date: Z")

    Returns:
        Complete HTML email string
    """
    # Load template
    with open(TEMPLATE_PATH, 'r') as f:
        template = f.read()

    # Convert markdown if needed
    if is_markdown:
        content = markdown_to_html(content)

    # Add meta info if provided
    if meta_info:
        content = f'<div class="meta-info">{meta_info}</div>\n{content}'

    # Replace template variables
    html = template.replace('{{TITLE}}', subject)
    html = html.replace('{{CONTENT}}', content)

    return html


def send_html_email(
    to: Union[str, List[str]],
    subject: str,
    html_body: str,
    from_name: str = FROM_NAME,
    from_email: str = FROM_EMAIL,
    cc: Optional[Union[str, List[str]]] = None,
    bcc: Optional[Union[str, List[str]]] = None,
    reply_to: Optional[str] = None,
    skip_duplicate_check: bool = False
) -> bool:
    """
    Send HTML email via Gmail SMTP.

    Args:
        to: Recipient email(s) - string or list
        subject: Email subject line
        html_body: HTML email body
        from_name: Display name for sender
        from_email: Sender email address
        cc: CC recipients (optional)
        bcc: BCC recipients (optional)
        reply_to: Reply-To address (optional)
        skip_duplicate_check: If True, skip duplicate detection (use sparingly)

    Returns:
        True if sent successfully, False otherwise
    """
    try:
        # Check for duplicate (unless explicitly skipped)
        if not skip_duplicate_check:
            content_preview = html_body[:200] if isinstance(html_body, str) else ""
            if _check_duplicate(to, subject, content_preview):
                print(f"\n⚠️  DUPLICATE DETECTED - Email not sent")
                print(f"To: {to}")
                print(f"Subject: {subject}")
                print(f"This exact email was already sent recently.")
                print(f"If you need to resend, use skip_duplicate_check=True")
                return False

        # Normalize recipients to lists
        to_list = [to] if isinstance(to, str) else to
        cc_list = [cc] if isinstance(cc, str) else (cc or [])
        bcc_list = [bcc] if isinstance(bcc, str) else (bcc or [])

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{from_name} <{from_email}>"
        msg['To'] = ', '.join(to_list)

        if cc_list:
            msg['Cc'] = ', '.join(cc_list)

        if reply_to:
            msg['Reply-To'] = reply_to

        # Attach HTML content
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)

        # Send email
        print(f"Connecting to {SMTP_SERVER}...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(from_email, PASSWORD)

            # All recipients for SMTP
            all_recipients = to_list + cc_list + bcc_list

            print(f"Sending HTML email to {len(all_recipients)} recipient(s)...")
            server.send_message(msg)

        print("\n" + "="*70)
        print("✅ HTML Email sent successfully!")
        print("="*70)
        print(f"From: {from_name} <{from_email}>")
        print(f"To: {', '.join(to_list)}")
        if cc_list:
            print(f"CC: {', '.join(cc_list)}")
        print(f"Subject: {subject}")
        print(f"Format: HTML (14-16px readable fonts)")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)

        # Record sent email to prevent duplicates
        content_preview = html_body[:200] if isinstance(html_body, str) else ""
        _save_sent_email(to, subject, content_preview)

        return True

    except Exception as e:
        print(f"\n❌ Error sending email: {e}")
        import traceback
        traceback.print_exc()
        return False


def send_simple_email(
    to: Union[str, List[str]],
    subject: str,
    body: str,
    is_markdown: bool = True,
    from_name: str = FROM_NAME
) -> bool:
    """
    Simplified function for quick email sending.

    Args:
        to: Recipient email(s)
        subject: Email subject
        body: Email content (Markdown or HTML)
        is_markdown: If True, convert body from Markdown to HTML
        from_name: Display name for sender

    Returns:
        True if sent successfully, False otherwise
    """
    # Create meta info
    to_list = [to] if isinstance(to, str) else to
    meta_info = f"""
        <strong>From:</strong> {from_name} ({FROM_EMAIL})<br>
        <strong>To:</strong> {', '.join(to_list)}<br>
        <strong>Date:</strong> {datetime.now().strftime('%B %d, %Y')}
    """

    # Create HTML email
    html = create_html_email(
        subject=subject,
        content=body,
        from_name=from_name,
        is_markdown=is_markdown,
        meta_info=meta_info
    )

    # Send
    return send_html_email(
        to=to,
        subject=subject,
        html_body=html,
        from_name=from_name
    )


# Example usage (commented out - was sending test emails on every import!)
# if __name__ == "__main__":
#     # Example: Send a simple HTML email
#     markdown_content = """
# # Test HTML Email
#
# This is a **test email** from the A-C-Gee civilization.
# """
#
#     success = send_simple_email(
#         to='coreycmusic@gmail.com',
#         subject='Test: HTML Email System',
#         body=markdown_content,
#         is_markdown=True
#     )
#
#     print(f"\nEmail send status: {'Success' if success else 'Failed'}")
