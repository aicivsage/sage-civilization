# ADR-003: Email Reporting System Architecture

**Status:** Proposed
**Date:** 2025-10-01
**Decision Makers:** Architecture Team
**Technical Story:** Design secure email reporting system for AI civilization mission reports and health monitoring

---

## Context and Problem Statement

The AI civilization needs a reliable email reporting system to send mission reports, health status updates, and system logs to designated recipients. The system must integrate seamlessly with the existing task tracker, support rich HTML formatting, handle attachments, and maintain high security standards.

### Requirements

**Functional Requirements:**
- Send mission completion reports via email
- Support HTML-formatted emails with professional styling
- Attach log files, reports, and JSON data
- Multiple email templates (mission complete, health report, error alerts, daily summary)
- Configuration via environment variables (no hardcoded credentials)
- Command-line interface for manual report sending
- Programmatic API for automated reporting

**Non-Functional Requirements:**
- Security: Use app-specific passwords, never store plain credentials
- Reliability: Retry mechanism for transient failures
- Performance: Async email sending to avoid blocking
- Maintainability: Template-based approach for easy customization
- Privacy: Support for encrypted connections (TLS/SSL)
- Compliance: Follow email best practices (SPF, DKIM considerations)

---

## Decision Drivers

1. **Security First**: Credentials must never be stored in code or version control
2. **Ease of Use**: Simple configuration via .env file
3. **Reliability**: Proven SMTP service with high deliverability
4. **Rich Formatting**: HTML templates for professional-looking reports
5. **Flexibility**: Support various attachment types and sizes
6. **Integration**: Easy to integrate with existing Python codebase
7. **Cost**: Prefer free tier options for development/testing
8. **Future-Proof**: Design for potential migration to other services

---

## Technology Stack Decision

### Email Provider: Gmail SMTP

**Rationale:**

**Gmail SMTP** is the optimal choice for this reporting system:

**Advantages:**
- **Proven Reliability**: Google's infrastructure with 99.9% uptime
- **Free Tier**: 500 emails/day sufficient for AI civilization reporting needs
- **Security**: App-specific passwords instead of main account credentials
- **TLS/SSL Support**: Industry-standard encryption
- **High Deliverability**: Google's reputation ensures emails aren't marked as spam
- **Easy Setup**: Well-documented configuration process
- **Wide Compatibility**: Works with all standard email libraries
- **OAuth 2.0 Support**: Future migration path for enhanced security

**Configuration:**
```
SMTP Server: smtp.gmail.com
Port: 587 (TLS) or 465 (SSL)
Authentication: App-specific password
Daily Limit: 500 emails (free tier)
Attachment Limit: 25 MB per email
```

**Alternatives Considered:**
- **SendGrid**: Requires API key, overkill for simple reporting
- **Amazon SES**: More complex setup, requires AWS account
- **Mailgun**: Commercial focus, unnecessary complexity
- **Office 365**: Less flexible, organizational account needed

**Decision:** Use Gmail SMTP with app-specific passwords for optimal balance of security, simplicity, and reliability.

### Email Library: Python `smtplib` + `email.mime`

**Rationale:**

**Standard Library Approach** (smtplib + email.mime) with optional `aiosmtplib` for async:

**Advantages:**
- **No Dependencies**: Built into Python standard library
- **Proven Stability**: Battle-tested since Python 2.x
- **Full Control**: Complete SMTP protocol access
- **HTML Support**: Rich formatting via MIME multipart messages
- **Attachment Support**: Handle any file type
- **Async Option**: aiosmtplib for non-blocking operations
- **Wide Compatibility**: Works with any SMTP server

**Code Pattern:**
```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# For async operations (optional)
import aiosmtplib
```

**Alternatives Considered:**
- **yagmail**: Simpler API but less control, Gmail-specific
- **sendgrid-python**: Requires API key, vendor lock-in
- **Flask-Mail**: Web framework dependency, unnecessary for CLI
- **python-emailer**: Less mature, smaller community

**Decision:** Use standard library (smtplib + email.mime) for core functionality with optional aiosmtplib for async operations.

### Template Engine: Jinja2

**Rationale:**

**Jinja2** for HTML email templates:

**Advantages:**
- **Industry Standard**: Used by Flask, Ansible, Salt
- **Powerful Syntax**: Loops, conditionals, filters, inheritance
- **Safe by Default**: Auto-escaping prevents XSS
- **Easy Testing**: Templates can be tested independently
- **Professional Output**: Clean HTML generation
- **Extensible**: Custom filters and functions
- **Well Documented**: Extensive documentation and examples

**Template Structure:**
```
templates/
├── base.html              # Base layout with styling
├── mission_complete.html  # Mission completion report
├── health_report.html     # System health status
├── error_alert.html       # Error notifications
└── daily_summary.html     # Daily activity summary
```

**Alternatives Considered:**
- **f-strings**: Too simplistic, no template reuse
- **string.Template**: Limited features, no control flow
- **Mako**: More complex, less popular
- **Handlebars.py**: JavaScript-based syntax, less Pythonic

**Decision:** Use Jinja2 for flexible, maintainable HTML email templates.

---

## Configuration Design

### Environment Variables (.env)

**Security-First Configuration:**

```bash
# Email Configuration
GMAIL_USER=ai.civilization@gmail.com
GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx  # App-specific password only
GMAIL_FROM_NAME="AI Civilization Bot"

# Email Settings
EMAIL_ENABLED=true                       # Master switch
EMAIL_RETRY_ATTEMPTS=3
EMAIL_RETRY_DELAY=5                      # seconds
EMAIL_TIMEOUT=30                         # seconds

# Recipients (comma-separated)
EMAIL_MISSION_REPORTS=admin@example.com,team@example.com
EMAIL_ERROR_ALERTS=ops@example.com
EMAIL_DAILY_SUMMARY=summary@example.com

# Optional: Async settings
EMAIL_ASYNC=false                        # Enable async sending
EMAIL_BATCH_SIZE=10                      # For bulk operations
```

### Configuration Module

**File: `task_tracker/email_config.py`**

```python
"""Email configuration management."""

import os
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator
from dotenv import load_dotenv


class EmailConfig(BaseModel):
    """Email configuration with validation."""

    # SMTP Settings
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    use_tls: bool = True

    # Credentials
    gmail_user: EmailStr
    gmail_app_password: str
    from_name: str = "AI Civilization Bot"

    # Behavior
    enabled: bool = True
    retry_attempts: int = 3
    retry_delay: int = 5
    timeout: int = 30
    async_enabled: bool = False
    batch_size: int = 10

    # Recipients
    mission_reports_to: List[EmailStr] = []
    error_alerts_to: List[EmailStr] = []
    daily_summary_to: List[EmailStr] = []

    @validator('gmail_app_password')
    def validate_app_password(cls, v):
        """Ensure app password format (16 chars, spaces removed)."""
        cleaned = v.replace(' ', '').replace('-', '')
        if len(cleaned) != 16:
            raise ValueError('Gmail app password must be 16 characters')
        return cleaned

    @classmethod
    def from_env(cls) -> 'EmailConfig':
        """Load configuration from environment variables."""
        load_dotenv()

        return cls(
            gmail_user=os.getenv('GMAIL_USER', ''),
            gmail_app_password=os.getenv('GMAIL_APP_PASSWORD', ''),
            from_name=os.getenv('GMAIL_FROM_NAME', 'AI Civilization Bot'),
            enabled=os.getenv('EMAIL_ENABLED', 'true').lower() == 'true',
            retry_attempts=int(os.getenv('EMAIL_RETRY_ATTEMPTS', '3')),
            retry_delay=int(os.getenv('EMAIL_RETRY_DELAY', '5')),
            timeout=int(os.getenv('EMAIL_TIMEOUT', '30')),
            async_enabled=os.getenv('EMAIL_ASYNC', 'false').lower() == 'true',
            batch_size=int(os.getenv('EMAIL_BATCH_SIZE', '10')),
            mission_reports_to=cls._parse_emails('EMAIL_MISSION_REPORTS'),
            error_alerts_to=cls._parse_emails('EMAIL_ERROR_ALERTS'),
            daily_summary_to=cls._parse_emails('EMAIL_DAILY_SUMMARY'),
        )

    @staticmethod
    def _parse_emails(env_var: str) -> List[str]:
        """Parse comma-separated email addresses."""
        value = os.getenv(env_var, '')
        if not value:
            return []
        return [email.strip() for email in value.split(',') if email.strip()]
```

---

## Email Template Design

### Base Template (templates/base.html)

**Professional Styling with Dark Mode Support:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --primary-color: #2563eb;
            --success-color: #059669;
            --error-color: #dc2626;
            --warning-color: #d97706;
            --bg-color: #ffffff;
            --text-color: #1f2937;
            --border-color: #e5e7eb;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --bg-color: #1f2937;
                --text-color: #f3f4f6;
                --border-color: #374151;
            }
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--bg-color);
            margin: 0;
            padding: 20px;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            background: var(--bg-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            overflow: hidden;
        }

        .header {
            background: var(--primary-color);
            color: white;
            padding: 20px;
            text-align: center;
        }

        .header h1 {
            margin: 0;
            font-size: 24px;
        }

        .content {
            padding: 30px;
        }

        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 600;
        }

        .status-success {
            background: var(--success-color);
            color: white;
        }

        .status-error {
            background: var(--error-color);
            color: white;
        }

        .status-warning {
            background: var(--warning-color);
            color: white;
        }

        .footer {
            background: #f9fafb;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #6b7280;
            border-top: 1px solid var(--border-color);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }

        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }

        th {
            background: #f3f4f6;
            font-weight: 600;
        }

        .metric {
            background: #f9fafb;
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
        }

        .metric-label {
            font-size: 14px;
            color: #6b7280;
        }

        .metric-value {
            font-size: 24px;
            font-weight: 700;
            color: var(--primary-color);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 {{ title }}</h1>
            {% if subtitle %}
            <p style="margin: 5px 0 0 0; opacity: 0.9;">{{ subtitle }}</p>
            {% endif %}
        </div>

        <div class="content">
            {% block content %}{% endblock %}
        </div>

        <div class="footer">
            <p>AI Civilization Automated Report System</p>
            <p>Generated at {{ timestamp }}</p>
            <p style="margin-top: 10px;">
                <a href="#" style="color: #6b7280; text-decoration: none;">Unsubscribe</a> |
                <a href="#" style="color: #6b7280; text-decoration: none;">View Online</a>
            </p>
        </div>
    </div>
</body>
</html>
```

### Mission Complete Template (templates/mission_complete.html)

```html
{% extends "base.html" %}

{% block content %}
<h2>Mission Completed Successfully! 🎉</h2>

<div style="background: #ecfdf5; border-left: 4px solid #059669; padding: 15px; margin: 20px 0;">
    <strong>{{ mission_name }}</strong> has been completed.
</div>

<table>
    <tr>
        <th>Property</th>
        <th>Value</th>
    </tr>
    <tr>
        <td>Mission ID</td>
        <td><code>{{ mission_id }}</code></td>
    </tr>
    <tr>
        <td>Status</td>
        <td><span class="status-badge status-success">COMPLETED</span></td>
    </tr>
    <tr>
        <td>Duration</td>
        <td>{{ duration }}</td>
    </tr>
    <tr>
        <td>Tasks Completed</td>
        <td>{{ tasks_completed }} / {{ tasks_total }}</td>
    </tr>
    <tr>
        <td>Success Rate</td>
        <td>{{ success_rate }}%</td>
    </tr>
</table>

{% if key_achievements %}
<h3>Key Achievements</h3>
<ul>
    {% for achievement in key_achievements %}
    <li>{{ achievement }}</li>
    {% endfor %}
</ul>
{% endif %}

{% if next_steps %}
<h3>Next Steps</h3>
<ol>
    {% for step in next_steps %}
    <li>{{ step }}</li>
    {% endfor %}
</ol>
{% endif %}

{% if attachments %}
<p style="margin-top: 30px; padding: 15px; background: #fef3c7; border-radius: 6px;">
    📎 <strong>Attachments:</strong> Full mission report and logs are attached to this email.
</p>
{% endif %}
{% endblock %}
```

### Health Report Template (templates/health_report.html)

```html
{% extends "base.html" %}

{% block content %}
<h2>System Health Report</h2>

<div class="metric">
    <div class="metric-label">Overall Health Score</div>
    <div class="metric-value">{{ health_score }}/100</div>
</div>

<h3>System Metrics</h3>
<table>
    <tr>
        <th>Component</th>
        <th>Status</th>
        <th>Value</th>
    </tr>
    {% for metric in metrics %}
    <tr>
        <td>{{ metric.name }}</td>
        <td>
            <span class="status-badge status-{{ metric.status }}">
                {{ metric.status|upper }}
            </span>
        </td>
        <td>{{ metric.value }}</td>
    </tr>
    {% endfor %}
</table>

{% if warnings %}
<h3>⚠️ Warnings</h3>
<ul>
    {% for warning in warnings %}
    <li style="color: var(--warning-color);">{{ warning }}</li>
    {% endfor %}
</ul>
{% endif %}

{% if errors %}
<h3>🚨 Errors</h3>
<ul>
    {% for error in errors %}
    <li style="color: var(--error-color);">{{ error }}</li>
    {% endfor %}
</ul>
{% endif %}

<div style="margin-top: 30px; padding: 15px; background: #eff6ff; border-radius: 6px;">
    <strong>Recommendation:</strong> {{ recommendation }}
</div>
{% endblock %}
```

### Error Alert Template (templates/error_alert.html)

```html
{% extends "base.html" %}

{% block content %}
<div style="background: #fee2e2; border-left: 4px solid #dc2626; padding: 15px; margin: 20px 0;">
    <h2 style="margin: 0 0 10px 0; color: #dc2626;">🚨 Critical Error Detected</h2>
    <p style="margin: 0;">Immediate attention required!</p>
</div>

<h3>Error Details</h3>
<table>
    <tr>
        <td><strong>Error Type:</strong></td>
        <td><code>{{ error_type }}</code></td>
    </tr>
    <tr>
        <td><strong>Severity:</strong></td>
        <td><span class="status-badge status-error">{{ severity }}</span></td>
    </tr>
    <tr>
        <td><strong>Timestamp:</strong></td>
        <td>{{ error_timestamp }}</td>
    </tr>
    <tr>
        <td><strong>Component:</strong></td>
        <td>{{ component }}</td>
    </tr>
</table>

<h3>Error Message</h3>
<pre style="background: #f9fafb; padding: 15px; border-radius: 6px; overflow-x: auto;">{{ error_message }}</pre>

{% if stack_trace %}
<h3>Stack Trace</h3>
<pre style="background: #1f2937; color: #f3f4f6; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 12px;">{{ stack_trace }}</pre>
{% endif %}

<h3>Suggested Actions</h3>
<ol>
    {% for action in suggested_actions %}
    <li>{{ action }}</li>
    {% endfor %}
</ol>
{% endblock %}
```

---

## Security Considerations

### App-Specific Password Setup

**Gmail App Password Generation Process:**

1. **Enable 2-Factor Authentication:**
   - Go to Google Account → Security
   - Enable 2-Step Verification

2. **Generate App Password:**
   - Go to Security → App passwords
   - Select app: "Mail"
   - Select device: "Other (Custom name)" → "AI Civilization Bot"
   - Copy the 16-character password

3. **Store Securely:**
   ```bash
   # In .env file (never commit to git!)
   GMAIL_APP_PASSWORD=abcd-efgh-ijkl-mnop
   ```

4. **Add to .gitignore:**
   ```
   .env
   .env.*
   *.env
   credentials/
   secrets/
   ```

### Security Best Practices

**DO:**
- ✅ Use app-specific passwords, never main account password
- ✅ Store credentials in .env file, never in code
- ✅ Add .env to .gitignore immediately
- ✅ Use TLS/SSL for all SMTP connections
- ✅ Validate email addresses before sending
- ✅ Implement rate limiting (respect Gmail's 500/day limit)
- ✅ Log email sending (without exposing credentials)
- ✅ Use environment variable validation (Pydantic)
- ✅ Rotate app passwords periodically
- ✅ Revoke unused app passwords

**DON'T:**
- ❌ Never commit credentials to version control
- ❌ Never log passwords or tokens
- ❌ Never use plain text connections (port 25)
- ❌ Never hardcode email addresses in code
- ❌ Never send sensitive data without encryption
- ❌ Never expose error details in production emails
- ❌ Never use shared email accounts without permission
- ❌ Never ignore authentication failures silently

### Credential Management

**File: `task_tracker/email_security.py`**

```python
"""Email security utilities."""

import logging
from typing import Optional
from pathlib import Path


class CredentialValidator:
    """Validate email credentials safely."""

    @staticmethod
    def validate_env_file(env_path: Path) -> bool:
        """Check if .env file exists and has required variables."""
        if not env_path.exists():
            logging.error(f".env file not found at {env_path}")
            return False

        required_vars = ['GMAIL_USER', 'GMAIL_APP_PASSWORD']
        content = env_path.read_text()

        missing = [var for var in required_vars if var not in content]
        if missing:
            logging.error(f"Missing required variables: {', '.join(missing)}")
            return False

        return True

    @staticmethod
    def check_gitignore(project_root: Path) -> bool:
        """Ensure .env is in .gitignore."""
        gitignore_path = project_root / '.gitignore'

        if not gitignore_path.exists():
            logging.warning(".gitignore not found - creating one")
            gitignore_path.write_text('.env\n.env.*\n*.env\n')
            return True

        content = gitignore_path.read_text()
        if '.env' not in content:
            logging.warning("Adding .env to .gitignore")
            with gitignore_path.open('a') as f:
                f.write('\n# Environment variables\n.env\n.env.*\n*.env\n')

        return True

    @staticmethod
    def sanitize_log_message(message: str) -> str:
        """Remove potential credentials from log messages."""
        import re
        # Remove app password patterns (16 chars with optional separators)
        message = re.sub(r'\b[a-z]{4}[-\s]?[a-z]{4}[-\s]?[a-z]{4}[-\s]?[a-z]{4}\b',
                        '****-****-****-****', message, flags=re.IGNORECASE)
        # Remove email addresses from error messages
        message = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                        '***@***.***', message)
        return message
```

---

## Implementation Architecture

### Core Email Service

**File: `task_tracker/email_service.py`**

```python
"""Email service for sending reports and notifications."""

import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
import time

from .email_config import EmailConfig
from .email_security import CredentialValidator


logger = logging.getLogger(__name__)


class EmailService:
    """Handle email sending with templates and attachments."""

    def __init__(self, config: Optional[EmailConfig] = None):
        """Initialize email service with configuration."""
        self.config = config or EmailConfig.from_env()

        # Setup Jinja2 template environment
        template_dir = Path(__file__).parent / 'templates'
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def send_email(
        self,
        to_addresses: List[str],
        subject: str,
        html_body: str,
        attachments: Optional[List[Path]] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> bool:
        """
        Send an email with optional attachments.

        Args:
            to_addresses: List of recipient email addresses
            subject: Email subject line
            html_body: HTML formatted email body
            attachments: Optional list of file paths to attach
            cc: Optional list of CC recipients
            bcc: Optional list of BCC recipients

        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.config.enabled:
            logger.info("Email sending is disabled in configuration")
            return False

        for attempt in range(self.config.retry_attempts):
            try:
                # Create message
                msg = MIMEMultipart('alternative')
                msg['From'] = f"{self.config.from_name} <{self.config.gmail_user}>"
                msg['To'] = ', '.join(to_addresses)
                msg['Subject'] = subject

                if cc:
                    msg['Cc'] = ', '.join(cc)
                if bcc:
                    msg['Bcc'] = ', '.join(bcc)

                # Attach HTML body
                msg.attach(MIMEText(html_body, 'html'))

                # Attach files
                if attachments:
                    for file_path in attachments:
                        self._attach_file(msg, file_path)

                # Send email
                with smtplib.SMTP(self.config.smtp_server,
                                self.config.smtp_port,
                                timeout=self.config.timeout) as server:
                    if self.config.use_tls:
                        server.starttls()

                    server.login(self.config.gmail_user,
                               self.config.gmail_app_password)

                    all_recipients = to_addresses + (cc or []) + (bcc or [])
                    server.send_message(msg,
                                      from_addr=self.config.gmail_user,
                                      to_addrs=all_recipients)

                logger.info(f"Email sent successfully to {len(to_addresses)} recipients")
                return True

            except Exception as e:
                logger.error(f"Email send attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.config.retry_attempts - 1:
                    time.sleep(self.config.retry_delay)
                else:
                    logger.error("All email send attempts failed")
                    return False

        return False

    def _attach_file(self, msg: MIMEMultipart, file_path: Path) -> None:
        """Attach a file to the email message."""
        with open(file_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={file_path.name}'
            )
            msg.attach(part)

    def render_template(self, template_name: str, **context) -> str:
        """Render a Jinja2 template with context."""
        # Add timestamp if not provided
        if 'timestamp' not in context:
            context['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        template = self.jinja_env.get_template(template_name)
        return template.render(**context)

    def send_mission_complete(
        self,
        mission_id: str,
        mission_name: str,
        duration: str,
        tasks_completed: int,
        tasks_total: int,
        success_rate: float,
        key_achievements: List[str],
        next_steps: List[str],
        attachments: Optional[List[Path]] = None
    ) -> bool:
        """Send mission completion report."""
        html_body = self.render_template(
            'mission_complete.html',
            title='Mission Complete',
            subtitle=mission_name,
            mission_id=mission_id,
            mission_name=mission_name,
            duration=duration,
            tasks_completed=tasks_completed,
            tasks_total=tasks_total,
            success_rate=success_rate,
            key_achievements=key_achievements,
            next_steps=next_steps,
            attachments=bool(attachments)
        )

        return self.send_email(
            to_addresses=self.config.mission_reports_to,
            subject=f'✅ Mission Complete: {mission_name}',
            html_body=html_body,
            attachments=attachments
        )

    def send_health_report(
        self,
        health_score: int,
        metrics: List[Dict[str, Any]],
        warnings: List[str],
        errors: List[str],
        recommendation: str
    ) -> bool:
        """Send system health report."""
        html_body = self.render_template(
            'health_report.html',
            title='System Health Report',
            health_score=health_score,
            metrics=metrics,
            warnings=warnings,
            errors=errors,
            recommendation=recommendation
        )

        # Determine severity for subject line
        severity = '🚨' if errors else ('⚠️' if warnings else '✅')

        return self.send_email(
            to_addresses=self.config.mission_reports_to,
            subject=f'{severity} System Health Report - Score: {health_score}/100',
            html_body=html_body
        )

    def send_error_alert(
        self,
        error_type: str,
        severity: str,
        error_timestamp: str,
        component: str,
        error_message: str,
        stack_trace: Optional[str],
        suggested_actions: List[str]
    ) -> bool:
        """Send error alert notification."""
        html_body = self.render_template(
            'error_alert.html',
            title='Critical Error Alert',
            error_type=error_type,
            severity=severity,
            error_timestamp=error_timestamp,
            component=component,
            error_message=error_message,
            stack_trace=stack_trace,
            suggested_actions=suggested_actions
        )

        return self.send_email(
            to_addresses=self.config.error_alerts_to,
            subject=f'🚨 CRITICAL: {error_type} in {component}',
            html_body=html_body
        )
```

### Async Email Service (Optional)

**File: `task_tracker/email_service_async.py`**

```python
"""Async email service for non-blocking operations."""

import asyncio
import logging
from typing import List, Optional
from pathlib import Path
import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .email_service import EmailService
from .email_config import EmailConfig


logger = logging.getLogger(__name__)


class AsyncEmailService(EmailService):
    """Async version of email service."""

    async def send_email_async(
        self,
        to_addresses: List[str],
        subject: str,
        html_body: str,
        attachments: Optional[List[Path]] = None
    ) -> bool:
        """Send email asynchronously."""
        if not self.config.enabled:
            logger.info("Email sending is disabled")
            return False

        try:
            # Create message (reuse sync method)
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.config.from_name} <{self.config.gmail_user}>"
            msg['To'] = ', '.join(to_addresses)
            msg['Subject'] = subject
            msg.attach(MIMEText(html_body, 'html'))

            if attachments:
                for file_path in attachments:
                    self._attach_file(msg, file_path)

            # Send async
            await aiosmtplib.send(
                msg,
                hostname=self.config.smtp_server,
                port=self.config.smtp_port,
                username=self.config.gmail_user,
                password=self.config.gmail_app_password,
                use_tls=self.config.use_tls,
                timeout=self.config.timeout
            )

            logger.info(f"Async email sent to {len(to_addresses)} recipients")
            return True

        except Exception as e:
            logger.error(f"Async email send failed: {str(e)}")
            return False

    async def send_batch_async(
        self,
        emails: List[tuple],
        batch_size: Optional[int] = None
    ) -> List[bool]:
        """Send multiple emails in batches."""
        batch_size = batch_size or self.config.batch_size
        results = []

        for i in range(0, len(emails), batch_size):
            batch = emails[i:i + batch_size]
            tasks = [
                self.send_email_async(to, subject, body, attachments)
                for to, subject, body, attachments in batch
            ]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            results.extend(batch_results)

            # Rate limiting between batches
            if i + batch_size < len(emails):
                await asyncio.sleep(1)

        return results
```

---

## CLI Integration

### Email Command

**Add to `task_tracker/cli.py`:**

```python
import typer
from pathlib import Path
from typing import Optional, List
from .email_service import EmailService
from .email_config import EmailConfig

email_app = typer.Typer(help="Email reporting commands")


@email_app.command("config")
def email_config(
    show: bool = typer.Option(False, "--show", help="Show current configuration")
):
    """Configure email settings."""
    if show:
        config = EmailConfig.from_env()
        typer.echo("Email Configuration:")
        typer.echo(f"  SMTP Server: {config.smtp_server}:{config.smtp_port}")
        typer.echo(f"  From: {config.from_name} <{config.gmail_user}>")
        typer.echo(f"  Enabled: {config.enabled}")
        typer.echo(f"  Async: {config.async_enabled}")
        typer.echo(f"  Mission Reports: {', '.join(config.mission_reports_to)}")
    else:
        typer.echo("To configure email, set these environment variables in .env:")
        typer.echo("  GMAIL_USER=your-email@gmail.com")
        typer.echo("  GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx")
        typer.echo("\nSee documentation for full configuration options.")


@email_app.command("test")
def test_email(
    to: str = typer.Option(..., "--to", help="Recipient email address")
):
    """Send a test email to verify configuration."""
    service = EmailService()

    html_body = service.render_template(
        'base.html',
        title='Test Email',
        subtitle='Configuration Test',
        content='<p>If you receive this email, your configuration is working correctly!</p>'
    )

    success = service.send_email(
        to_addresses=[to],
        subject='🤖 AI Civilization Test Email',
        html_body=html_body
    )

    if success:
        typer.secho("✓ Test email sent successfully!", fg=typer.colors.GREEN)
    else:
        typer.secho("✗ Failed to send test email. Check logs.", fg=typer.colors.RED)
        raise typer.Exit(1)


@email_app.command("send-report")
def send_mission_report(
    mission_id: str = typer.Argument(..., help="Mission ID"),
    name: str = typer.Option(..., "--name", help="Mission name"),
    attach: Optional[List[Path]] = typer.Option(None, "--attach", help="Files to attach")
):
    """Send a mission completion report."""
    service = EmailService()

    # This would typically pull data from the task system
    # For now, using example data
    success = service.send_mission_complete(
        mission_id=mission_id,
        mission_name=name,
        duration="2 hours 15 minutes",
        tasks_completed=8,
        tasks_total=8,
        success_rate=100.0,
        key_achievements=[
            "All tasks completed successfully",
            "Zero errors encountered",
            "Ahead of schedule"
        ],
        next_steps=[
            "Review mission logs",
            "Update documentation",
            "Plan next mission"
        ],
        attachments=list(attach) if attach else None
    )

    if success:
        typer.secho(f"✓ Mission report sent for {name}", fg=typer.colors.GREEN)
    else:
        typer.secho("✗ Failed to send report", fg=typer.colors.RED)
        raise typer.Exit(1)


# Add to main app
app.add_typer(email_app, name="email")
```

---

## Usage Examples

### Setup and Configuration

```bash
# 1. Install dependencies
pip install jinja2 python-dotenv aiosmtplib  # aiosmtplib optional

# 2. Create .env file
cat > .env << EOF
GMAIL_USER=ai.civilization@gmail.com
GMAIL_APP_PASSWORD=abcd-efgh-ijkl-mnop
GMAIL_FROM_NAME="AI Civilization Bot"

EMAIL_ENABLED=true
EMAIL_MISSION_REPORTS=admin@example.com
EMAIL_ERROR_ALERTS=ops@example.com
EOF

# 3. Ensure .env is in .gitignore
echo ".env" >> .gitignore

# 4. Test configuration
task email test --to admin@example.com
```

### Sending Reports

```bash
# Send mission completion report
task email send-report MISSION-001 \
  --name "Data Processing Pipeline" \
  --attach logs/mission-001.log \
  --attach reports/summary.json

# Check email configuration
task email config --show
```

### Programmatic Usage

```python
from task_tracker.email_service import EmailService
from pathlib import Path

# Initialize service
service = EmailService()

# Send mission complete report
service.send_mission_complete(
    mission_id="MISSION-001",
    mission_name="Data Processing Pipeline",
    duration="2 hours 15 minutes",
    tasks_completed=8,
    tasks_total=8,
    success_rate=100.0,
    key_achievements=[
        "Processed 1M records",
        "Zero data loss",
        "50% faster than baseline"
    ],
    next_steps=[
        "Scale to 10M records",
        "Optimize memory usage"
    ],
    attachments=[Path("logs/mission.log")]
)

# Send health report
service.send_health_report(
    health_score=95,
    metrics=[
        {"name": "CPU Usage", "status": "success", "value": "45%"},
        {"name": "Memory", "status": "success", "value": "2.1 GB / 8 GB"},
        {"name": "Disk Space", "status": "warning", "value": "78% used"}
    ],
    warnings=["Disk space above 75%"],
    errors=[],
    recommendation="Monitor disk space, consider cleanup"
)

# Send error alert
service.send_error_alert(
    error_type="DatabaseConnectionError",
    severity="CRITICAL",
    error_timestamp="2025-10-01 14:30:45",
    component="Storage Layer",
    error_message="Failed to connect to database after 3 retries",
    stack_trace="Traceback (most recent call last):\n  ...",
    suggested_actions=[
        "Check database server status",
        "Verify network connectivity",
        "Review connection credentials"
    ]
)
```

### Async Usage

```python
import asyncio
from task_tracker.email_service_async import AsyncEmailService

async def send_reports():
    service = AsyncEmailService()

    # Send single async email
    await service.send_email_async(
        to_addresses=["admin@example.com"],
        subject="Async Test",
        html_body=service.render_template('base.html',
                                         title='Async Email',
                                         content='<p>Sent async!</p>')
    )

    # Send batch of emails
    emails = [
        (["user1@example.com"], "Report 1", "<p>Content 1</p>", None),
        (["user2@example.com"], "Report 2", "<p>Content 2</p>", None),
        (["user3@example.com"], "Report 3", "<p>Content 3</p>", None),
    ]
    results = await service.send_batch_async(emails, batch_size=2)
    print(f"Sent {sum(results)} emails successfully")

# Run
asyncio.run(send_reports())
```

---

## Implementation Roadmap

### Phase 1: Core Infrastructure (Day 1-2)
1. Create email configuration module with Pydantic validation
2. Implement security utilities and credential validation
3. Setup template directory structure
4. Create base email template with responsive design
5. Implement core EmailService class
6. Add basic CLI commands (config, test)

### Phase 2: Email Templates (Day 3)
1. Design mission completion template
2. Design health report template
3. Design error alert template
4. Design daily summary template
5. Test templates with various data scenarios
6. Validate HTML rendering across email clients

### Phase 3: Integration (Day 4)
1. Integrate with task tracker storage
2. Add automated mission report generation
3. Implement health monitoring triggers
4. Add error handling with email alerts
5. Create daily summary aggregation
6. Add CLI commands for manual reports

### Phase 4: Advanced Features (Day 5)
1. Implement async email service
2. Add batch email sending
3. Implement retry logic with exponential backoff
4. Add email queue for rate limiting
5. Create email templates preview command
6. Add attachment size validation

### Phase 5: Testing & Documentation (Day 6)
1. Unit tests for email service
2. Integration tests with Gmail SMTP
3. Template rendering tests
4. Security validation tests
5. Update main documentation
6. Create email troubleshooting guide

---

## Testing Strategy

### Unit Tests

```python
# tests/test_email_service.py
import pytest
from pathlib import Path
from task_tracker.email_service import EmailService
from task_tracker.email_config import EmailConfig


def test_email_config_validation():
    """Test email configuration validation."""
    config = EmailConfig(
        gmail_user="test@gmail.com",
        gmail_app_password="abcdefghijklmnop",
        mission_reports_to=["admin@example.com"]
    )
    assert config.gmail_user == "test@gmail.com"
    assert len(config.gmail_app_password) == 16


def test_template_rendering():
    """Test Jinja2 template rendering."""
    service = EmailService()
    html = service.render_template(
        'mission_complete.html',
        title='Test Mission',
        mission_id='TEST-001',
        mission_name='Test',
        duration='1 hour',
        tasks_completed=5,
        tasks_total=5,
        success_rate=100.0,
        key_achievements=['Test achievement'],
        next_steps=['Test step']
    )
    assert 'TEST-001' in html
    assert 'Test Mission' in html


def test_email_sending_disabled():
    """Test email sending when disabled."""
    config = EmailConfig(
        gmail_user="test@gmail.com",
        gmail_app_password="abcdefghijklmnop",
        enabled=False
    )
    service = EmailService(config)

    result = service.send_email(
        to_addresses=["test@example.com"],
        subject="Test",
        html_body="<p>Test</p>"
    )
    assert result is False


@pytest.mark.integration
def test_send_test_email():
    """Integration test: send actual email."""
    service = EmailService()  # Uses .env config

    result = service.send_email(
        to_addresses=[os.getenv("TEST_EMAIL")],
        subject="Integration Test",
        html_body="<p>This is a test</p>"
    )
    assert result is True
```

### Security Tests

```python
# tests/test_email_security.py
from task_tracker.email_security import CredentialValidator


def test_gitignore_check(tmp_path):
    """Test .gitignore validation."""
    validator = CredentialValidator()

    # Create test .gitignore without .env
    gitignore = tmp_path / '.gitignore'
    gitignore.write_text('*.pyc\n')

    # Should add .env
    validator.check_gitignore(tmp_path)
    content = gitignore.read_text()
    assert '.env' in content


def test_credential_sanitization():
    """Test credential sanitization in logs."""
    validator = CredentialValidator()

    message = "Login failed for user@example.com with password abcd-efgh-ijkl-mnop"
    sanitized = validator.sanitize_log_message(message)

    assert 'abcd-efgh-ijkl-mnop' not in sanitized
    assert 'user@example.com' not in sanitized
    assert '****' in sanitized
```

---

## Monitoring and Observability

### Email Metrics

Track these metrics for monitoring:

1. **Send Success Rate**: % of successfully sent emails
2. **Delivery Time**: Time to send email (SMTP connection + transfer)
3. **Retry Attempts**: Number of retries needed
4. **Error Rate**: % of failed sends
5. **Queue Depth**: Number of pending emails (for async)
6. **Daily Send Count**: Track against Gmail limits (500/day)

### Logging Strategy

```python
import logging

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log important events
logger.info("Email sent successfully", extra={
    "recipient_count": len(to_addresses),
    "has_attachments": bool(attachments),
    "subject": subject,
    "attempt": attempt_number
})

logger.error("Email send failed", extra={
    "error_type": type(e).__name__,
    "retry_attempt": attempt,
    "max_retries": config.retry_attempts
})
```

---

## Future Enhancements

### Potential Improvements

1. **Email Templates:**
   - Weekly summary template
   - Performance metrics dashboard email
   - Scheduled maintenance notification
   - User onboarding emails

2. **Advanced Features:**
   - Email scheduling (send at specific time)
   - Email templates with markdown support
   - Inline image embedding
   - Email threading (reply-to headers)
   - Read receipts tracking

3. **Integrations:**
   - Slack webhook fallback
   - Discord notifications
   - SMS alerts for critical errors
   - PagerDuty integration

4. **Analytics:**
   - Open rate tracking (pixel tracking)
   - Link click tracking
   - Bounce rate monitoring
   - Email delivery analytics

5. **Multi-Provider Support:**
   - AWS SES support
   - SendGrid as backup
   - Mailgun integration
   - Provider failover logic

---

## Troubleshooting Guide

### Common Issues

**1. Authentication Failed**
```
Error: (535, b'5.7.8 Username and Password not accepted')

Solution:
- Verify app password is 16 characters
- Ensure 2FA is enabled on Gmail account
- Regenerate app password if needed
- Check for typos in .env file
```

**2. Connection Timeout**
```
Error: TimeoutError: [Errno 110] Connection timed out

Solution:
- Check internet connectivity
- Verify firewall allows SMTP (port 587)
- Try alternative port (465 for SSL)
- Increase timeout in config
```

**3. Attachment Too Large**
```
Error: Message too large (>25MB)

Solution:
- Check attachment total size
- Compress large files
- Split into multiple emails
- Use cloud storage links instead
```

**4. Daily Limit Exceeded**
```
Error: (550, '5.4.5 Daily sending quota exceeded')

Solution:
- Track daily send count
- Implement rate limiting
- Use batch sending for bulk operations
- Consider multiple sender accounts
```

**5. Recipient Rejected**
```
Error: (550, 'Recipient address rejected')

Solution:
- Validate email addresses
- Check for typos
- Verify recipient domain exists
- Remove invalid addresses from config
```

---

## Success Criteria

### Definition of Done

The email reporting system will be considered complete when:

1. ✅ Gmail SMTP integration working with app-specific passwords
2. ✅ All email templates (mission, health, error, summary) implemented
3. ✅ HTML rendering validated across major email clients
4. ✅ Attachment support for logs and reports
5. ✅ Configuration via .env file with validation
6. ✅ CLI commands for testing and manual sending
7. ✅ Programmatic API for automated reports
8. ✅ Security best practices implemented
9. ✅ Comprehensive error handling and retry logic
10. ✅ Unit and integration tests passing
11. ✅ Documentation complete with examples
12. ✅ Successfully sends test email to stakeholders

### Acceptance Tests

1. **Configuration Test**: Load config from .env, validate all fields
2. **Template Test**: Render all templates with sample data
3. **Send Test**: Send test email to real Gmail address
4. **Attachment Test**: Send email with 3 different file types
5. **Error Test**: Trigger error alert, verify email received
6. **Health Test**: Generate health report, verify formatting
7. **Mission Test**: Complete mock mission, send report
8. **Security Test**: Verify credentials not in logs or version control
9. **Retry Test**: Simulate SMTP failure, verify retry logic
10. **CLI Test**: Execute all CLI commands successfully

---

## Conclusion

This architecture provides a secure, flexible, and maintainable email reporting system for the AI civilization. The design prioritizes security through app-specific passwords and environment-based configuration, while offering rich HTML templates for professional communication.

Key benefits:
- **Secure by default**: No hardcoded credentials, app passwords only
- **Easy to use**: Simple .env configuration, intuitive CLI
- **Professional output**: Responsive HTML templates with dark mode
- **Reliable**: Retry logic, error handling, logging
- **Extensible**: Template-based design for easy additions
- **Well-tested**: Comprehensive test coverage

The system integrates seamlessly with the existing task tracker while maintaining separation of concerns and following established architectural patterns.

---

## References

- [Gmail SMTP Configuration](https://support.google.com/mail/answer/7126229)
- [App Passwords Setup](https://support.google.com/accounts/answer/185833)
- [Python smtplib Documentation](https://docs.python.org/3/library/smtplib.html)
- [Jinja2 Template Documentation](https://jinja.palletsprojects.com/)
- [Email Security Best Practices](https://owasp.org/www-project-web-security-testing-guide/)
- [MIME Email Structure](https://tools.ietf.org/html/rfc2045)
- [HTML Email Best Practices](https://www.campaignmonitor.com/css/)

---

**Next Steps for Coder Agent:**
1. Review this ADR and confirm architectural decisions
2. Begin Phase 1 implementation (Core Infrastructure)
3. Create .env.example file with all configuration options
4. Implement email_config.py with Pydantic validation
5. Setup template directory and create base.html
6. Implement core EmailService class
7. Add CLI commands and test email sending
8. Proceed through remaining phases systematically
