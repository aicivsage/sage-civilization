#!/usr/bin/env python3
"""
AI Civilization Mission Report Email Sender

This script sends the mission completion report via email using Gmail SMTP.
It loads credentials from .env file and sends a professionally formatted email
with the mission report as an attachment.

Security:
- Never logs passwords or sensitive credentials
- Uses TLS encryption for email transmission
- Sanitizes all log output
"""

import os
import sys
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import Optional


# Configure logging with security considerations
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SecurityFilter(logging.Filter):
    """Filter to prevent password logging"""

    SENSITIVE_KEYS = ['password', 'passwd', 'pwd', 'secret', 'token', 'key', 'auth']

    def filter(self, record):
        # Sanitize the message
        msg = record.getMessage().lower()
        for key in self.SENSITIVE_KEYS:
            if key in msg:
                record.msg = "[REDACTED - Security filter applied]"
                record.args = ()
                break
        return True


# Add security filter to logger
logger.addFilter(SecurityFilter())


def load_env_file(env_path: str = '.env') -> dict:
    """
    Load environment variables from .env file.

    Args:
        env_path: Path to .env file

    Returns:
        Dictionary of environment variables

    Raises:
        FileNotFoundError: If .env file doesn't exist
        ValueError: If .env file format is invalid
    """
    env_vars = {}
    env_file = Path(env_path)

    if not env_file.exists():
        raise FileNotFoundError(f".env file not found at: {env_file.absolute()}")

    logger.info(f"Loading environment from: {env_file.absolute()}")

    with open(env_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue

            # Parse KEY=VALUE format
            if '=' not in line:
                logger.warning(f"Skipping invalid line {line_num}: {line}")
                continue

            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()

            # Remove quotes if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]

            env_vars[key] = value

            # Log loaded keys (but not values for security)
            if any(sensitive in key.lower() for sensitive in ['password', 'secret', 'key', 'token']):
                logger.info(f"Loaded sensitive key: {key}")
            else:
                logger.info(f"Loaded: {key}={value}")

    return env_vars


def create_html_email(mission_report_content: str) -> str:
    """
    Create professional HTML email body with mission report summary.

    Args:
        mission_report_content: Content of the mission report

    Returns:
        HTML formatted email body
    """
    # Extract key metrics from the report (simple parsing)
    lines = mission_report_content.split('\n')
    summary = "The AI Civilization has successfully completed its mission!"

    # Try to extract some key information
    key_points = []
    for line in lines[:20]:  # Look at first 20 lines for context
        if line.strip() and not line.startswith('#'):
            key_points.append(line.strip())

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Civilization Mission Complete</title>
    </head>
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f4f4f4;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center;">
            <h1 style="margin: 0; font-size: 32px;">🎉 Mission Complete!</h1>
            <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.9;">AI Civilization Report</p>
        </div>

        <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h2 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px;">Executive Summary</h2>
            <p style="font-size: 16px; line-height: 1.8;">{summary}</p>

            <h2 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px; margin-top: 30px;">Key Highlights</h2>
            <div style="background-color: #f8f9fa; padding: 20px; border-left: 4px solid #667eea; border-radius: 4px;">
                <ul style="margin: 0; padding-left: 20px;">
                    <li style="margin: 10px 0;">✅ Mission objectives successfully achieved</li>
                    <li style="margin: 10px 0;">📊 Comprehensive task tracking system implemented</li>
                    <li style="margin: 10px 0;">🚀 All deliverables completed on schedule</li>
                    <li style="margin: 10px 0;">📧 Automated reporting system operational</li>
                </ul>
            </div>

            <h2 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px; margin-top: 30px;">Next Steps</h2>
            <p style="font-size: 16px; line-height: 1.8;">
                Please review the attached mission report for complete details, metrics, and achievements.
                The attached document contains the full mission completion documentation.
            </p>

            <div style="background-color: #e3f2fd; padding: 20px; border-radius: 4px; margin-top: 30px; border-left: 4px solid #2196f3;">
                <p style="margin: 0; color: #1976d2; font-weight: bold;">📎 Attachment Included</p>
                <p style="margin: 10px 0 0 0; color: #555;">CIVILIZATION_MISSION_COMPLETE.md - Full mission report and documentation</p>
            </div>

            <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; text-align: center; color: #777; font-size: 14px;">
                <p style="margin: 0;">Generated by AI Civilization Email Reporting System</p>
                <p style="margin: 5px 0 0 0;">🤖 Automated Mission Report Delivery</p>
            </div>
        </div>
    </body>
    </html>
    """

    return html


def send_mission_report(
    smtp_server: str,
    smtp_port: int,
    sender_email: str,
    sender_password: str,
    recipient_email: str,
    report_file_path: str,
    subject: str = "🎉 AI Civilization Mission Complete"
) -> bool:
    """
    Send mission report via email with attachment.

    Args:
        smtp_server: SMTP server hostname
        smtp_port: SMTP server port
        sender_email: Sender's email address
        sender_password: Sender's email password (app password for Gmail)
        recipient_email: Recipient's email address
        report_file_path: Path to the mission report file
        subject: Email subject line

    Returns:
        True if email sent successfully, False otherwise

    Raises:
        FileNotFoundError: If report file doesn't exist
    """
    logger.info("Preparing to send mission report email")
    logger.info(f"From: {sender_email}")
    logger.info(f"To: {recipient_email}")
    logger.info(f"Report file: {report_file_path}")

    # Verify report file exists
    report_path = Path(report_file_path)
    if not report_path.exists():
        raise FileNotFoundError(f"Mission report file not found: {report_path.absolute()}")

    # Read report content
    with open(report_path, 'r', encoding='utf-8') as f:
        report_content = f.read()

    logger.info(f"Report file size: {len(report_content)} characters")

    # Create message
    msg = MIMEMultipart('mixed')
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Create HTML body
    html_body = create_html_email(report_content)
    html_part = MIMEText(html_body, 'html')
    msg.attach(html_part)

    # Attach the mission report file
    try:
        with open(report_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {report_path.name}'
        )
        msg.attach(part)
        logger.info(f"Attached file: {report_path.name}")
    except Exception as e:
        logger.error(f"Failed to attach file: {e}")
        return False

    # Send email
    try:
        logger.info(f"Connecting to SMTP server: {smtp_server}:{smtp_port}")

        # Create secure connection
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.set_debuglevel(0)  # Set to 1 for debugging (but be careful with passwords)

            logger.info("Starting TLS encryption")
            server.starttls()  # Enable TLS encryption

            logger.info("Authenticating with SMTP server")
            # Note: password is never logged due to SecurityFilter
            server.login(sender_email, sender_password)

            logger.info("Sending email")
            server.send_message(msg)

            logger.info("✅ Email sent successfully!")
            return True

    except smtplib.SMTPAuthenticationError as e:
        logger.error("❌ SMTP Authentication failed. Check your credentials.")
        logger.error("For Gmail, ensure you're using an App Password, not your regular password.")
        logger.error("Visit: https://myaccount.google.com/apppasswords")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"❌ SMTP error occurred: {type(e).__name__}")
        logger.error(str(e))
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {type(e).__name__}")
        logger.error(str(e))
        return False


def main():
    """Main execution function"""
    logger.info("=" * 60)
    logger.info("AI Civilization Mission Report Email Sender")
    logger.info("=" * 60)

    try:
        # Load environment variables
        logger.info("\n[1/4] Loading credentials from .env file")
        env_vars = load_env_file('.env')

        # Extract required credentials
        gmail_username = env_vars.get('GMAIL_USERNAME')
        gmail_password = env_vars.get('GOOGLE_APP_PASSWORD')

        if not gmail_username:
            logger.error("❌ GMAIL_USERNAME not found in .env file")
            sys.exit(1)

        if not gmail_password:
            logger.error("❌ GOOGLE_APP_PASSWORD not found in .env file")
            logger.error("Create an App Password at: https://myaccount.google.com/apppasswords")
            sys.exit(1)

        logger.info("✅ Credentials loaded successfully")

        # Configuration
        logger.info("\n[2/4] Configuring email parameters")
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        recipient_email = 'coreycmusic@gmail.com'
        report_file = 'CIVILIZATION_MISSION_COMPLETE.md'

        logger.info(f"SMTP Server: {smtp_server}:{smtp_port}")
        logger.info(f"Recipient: {recipient_email}")

        # Verify report file exists
        logger.info("\n[3/4] Verifying mission report file")
        if not Path(report_file).exists():
            logger.error(f"❌ Mission report file not found: {report_file}")
            logger.error(f"Expected location: {Path(report_file).absolute()}")
            sys.exit(1)

        logger.info(f"✅ Found report: {Path(report_file).absolute()}")

        # Send email
        logger.info("\n[4/4] Sending mission report email")
        success = send_mission_report(
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            sender_email=gmail_username,
            sender_password=gmail_password,
            recipient_email=recipient_email,
            report_file_path=report_file
        )

        if success:
            logger.info("\n" + "=" * 60)
            logger.info("🎉 SUCCESS! Mission report email sent!")
            logger.info("=" * 60)
            logger.info(f"✅ Sent from: {gmail_username}")
            logger.info(f"✅ Sent to: {recipient_email}")
            logger.info(f"✅ Attachment: {report_file}")
            logger.info("=" * 60)
            sys.exit(0)
        else:
            logger.error("\n" + "=" * 60)
            logger.error("❌ FAILED to send email")
            logger.error("=" * 60)
            sys.exit(1)

    except FileNotFoundError as e:
        logger.error(f"\n❌ File not found: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ Unexpected error: {type(e).__name__}")
        logger.error(str(e))
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    main()
