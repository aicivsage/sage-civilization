#!/usr/bin/env python3
"""
Email Reporter Agent - Launch Notification
Send quality-gated roadmap execution announcement to Corey
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
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

def send_launch_email():
    """Send the quality-gated roadmap launch notification"""

    # Load credentials
    load_env()
    gmail_user = os.environ.get('GMAIL_USERNAME')
    gmail_password = os.environ.get('GOOGLE_APP_PASSWORD')

    if not gmail_user or not gmail_password:
        raise ValueError("Gmail credentials not found in .env file")

    # Email configuration
    recipient = "coreycmusic@gmail.com"
    subject = "🚀 Launching Quality-Gated Roadmap Execution - AI-Speed One-Shot"

    # Create HTML email content
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px 8px 0 0;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        .content {
            padding: 30px;
            background: #ffffff;
        }
        .section {
            margin: 25px 0;
            padding: 20px;
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }
        .section h2 {
            margin-top: 0;
            color: #667eea;
            font-size: 18px;
        }
        .phase-list {
            list-style: none;
            padding: 0;
        }
        .phase-list li {
            padding: 12px;
            margin: 8px 0;
            background: white;
            border-radius: 4px;
            border-left: 3px solid #28a745;
        }
        .quality-gate {
            background: #fff3cd;
            border-left-color: #ffc107;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }
        .quality-gate strong {
            color: #856404;
        }
        .highlight {
            background: #e7f3ff;
            padding: 15px;
            border-radius: 4px;
            border-left: 4px solid #0066cc;
            margin: 15px 0;
        }
        .metrics {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin: 15px 0;
        }
        .metric-box {
            background: white;
            padding: 15px;
            border-radius: 4px;
            border: 2px solid #e9ecef;
        }
        .metric-box strong {
            color: #667eea;
            display: block;
            font-size: 16px;
        }
        .footer {
            background: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 0 0 8px 8px;
        }
        .footer small {
            color: #bdc3c7;
        }
        .cta {
            background: #28a745;
            color: white;
            padding: 15px 30px;
            text-align: center;
            border-radius: 4px;
            margin: 20px 0;
            font-size: 18px;
            font-weight: bold;
        }
        ul {
            line-height: 1.8;
        }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Quality-Gated Roadmap Execution Launching NOW</h1>
        <p style="margin: 10px 0 0 0; opacity: 0.9;">AI-Speed One-Shot Mode | 6-10 Hour Estimated Completion</p>
    </div>

    <div class="content">
        <div class="cta">
            EXECUTION STATUS: LAUNCHING PHASE 1
        </div>

        <div class="section">
            <h2>📋 What We've Built</h2>
            <p>Per your directive, we've added <strong>comprehensive quality gates</strong> to the entire roadmap execution:</p>
            <ul>
                <li><strong>BLOCKING Auditor Gates</strong> - Every phase must pass before proceeding</li>
                <li><strong>Quality Standard</strong> - 80%+ coverage, 85/100 minimum score, ALL tests passing</li>
                <li><strong>Execution Mode</strong> - AI-SPEED ONE-SHOT (parallel where possible, 6-10 hours estimated)</li>
                <li><strong>Communication</strong> - Email notification after EVERY phase completion</li>
                <li><strong>Real-Time Visibility</strong> - Weaver's dashboard being installed</li>
                <li><strong>Auto-Compact Ready</strong> - Proven context management protocols in place</li>
            </ul>
        </div>

        <div class="section">
            <h2>🎯 Four Phase Execution Plan</h2>
            <ul class="phase-list">
                <li><strong>Phase 1: Immediate Actions (2h)</strong><br/>
                    Dashboard installation, Ed25519 test fix, ADR-004 sharing prep, initial quality audit</li>

                <li><strong>Phase 2: System Health & Integration (2-3h)</strong><br/>
                    Git cleanup, Ed25519 integration, flow testing (27 flows), memory system implementation</li>

                <li><strong>Phase 3: Advanced Integration (2-3h)</strong><br/>
                    Protocol Spec v2.0, dashboard integration, risk monitoring, security hardening</li>

                <li><strong>Phase 4: Dry-Run & Final (1-2h)</strong><br/>
                    Full integration dry-run, final quality sweep, Weaver coordination</li>
            </ul>
        </div>

        <div class="section">
            <h2>🛡️ Quality Gates (Examples)</h2>
            <div class="quality-gate">
                <strong>BLOCKING Requirements - Must Pass to Proceed:</strong>
                <ul>
                    <li>System health scan MUST PASS (no critical issues)</li>
                    <li>Reviewer-Audit 100-point rubric ≥ 85/100</li>
                    <li>Test coverage ≥ 80% VERIFIED</li>
                    <li>All tests passing 100% (no skips, no failures)</li>
                    <li>File-Guardian inventory clean (no orphans)</li>
                    <li>NO broken imports, NO circular dependencies</li>
                    <li>NO secrets leaked (security scan)</li>
                    <li>Performance benchmarks met</li>
                </ul>
            </div>
        </div>

        <div class="section">
            <h2>📧 What You'll Receive</h2>
            <div class="metrics">
                <div class="metric-box">
                    <strong>After Each Phase</strong>
                    <p>Quality gate results, completion status, metrics, next phase preview</p>
                </div>
                <div class="metric-box">
                    <strong>If Any Gate Fails</strong>
                    <p>Immediate alert with failure details, root cause, remediation plan</p>
                </div>
                <div class="metric-box">
                    <strong>Phase Milestones</strong>
                    <p>Key achievements, deliverables created, quality scores</p>
                </div>
                <div class="metric-box">
                    <strong>Final Completion</strong>
                    <p>Full quality certification, all deliverables, system status</p>
                </div>
            </div>
        </div>

        <div class="highlight">
            <strong>🎖️ Quality Commitment</strong><br/>
            Every deliverable will be production-ready with comprehensive tests, documentation, and validation.
            No shortcuts. No "good enough." Only excellence.
        </div>

        <div class="section">
            <h2>📎 Reference Documents</h2>
            <ul>
                <li><code>QUALITY-GATED-ROADMAP-EXECUTION.md</code> - Full execution plan with all quality gates</li>
                <li><code>CONSOLIDATION-TEST-COMPLETE.md</code> - What led to this (consolidation validation)</li>
                <li><code>memories/flows/</code> - 27 untested flows ready for validation</li>
                <li><code>DEMOCRATIC_MISSION_COMPLETE.md</code> - Recent democratic achievements</li>
            </ul>
        </div>

        <div class="highlight">
            <strong>⚡ Execution Timeline</strong><br/>
            <strong>Start Time:</strong> """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """ EST<br/>
            <strong>Estimated Completion:</strong> 6-10 hours (AI-SPEED mode)<br/>
            <strong>Current Phase:</strong> Phase 1 launching NOW<br/>
            <strong>Next Email:</strong> Phase 1 completion (~2 hours)
        </div>

        <div class="section">
            <h2>🤖 Agent Status</h2>
            <p><strong>Primary AI:</strong> Orchestrating execution<br/>
            <strong>Email Reporter:</strong> Active (sending this notification)<br/>
            <strong>Reviewer:</strong> Standing by for quality audits<br/>
            <strong>File Guardian:</strong> Monitoring file integrity<br/>
            <strong>All 10 Agents:</strong> Ready for task allocation</p>
        </div>

        <div class="cta" style="background: #667eea;">
            PHASE 1: IMMEDIATE ACTIONS - STARTING NOW
        </div>

        <p style="text-align: center; margin-top: 30px; color: #666;">
            <em>You can monitor progress via dashboard (being installed) or wait for phase completion emails.</em><br/>
            <em>Any questions or concerns? Reply to this email.</em>
        </p>
    </div>

    <div class="footer">
        <strong>AI Agent Civilization v1.1</strong><br/>
        <small>Powered by Claude Sonnet 4.5 | Quality-First Architecture | Democratic Governance</small><br/>
        <small>Email Reporter Agent | """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</small>
    </div>
</body>
</html>
"""

    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = recipient
    msg['Date'] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")

    # Attach HTML content
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)

    # Send email
    try:
        print(f"Connecting to Gmail SMTP server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        print(f"Authenticating as {gmail_user}...")
        server.login(gmail_user, gmail_password)

        print(f"Sending launch notification to {recipient}...")
        server.send_message(msg)
        server.quit()

        print("✅ EMAIL SENT SUCCESSFULLY")
        print(f"   To: {recipient}")
        print(f"   Subject: {subject}")
        print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("")
        print("📧 Corey will receive notification of:")
        print("   - Quality-gated roadmap execution launch")
        print("   - 4-phase plan with blocking quality gates")
        print("   - Email notifications after each phase")
        print("   - AI-SPEED one-shot execution mode")
        print("")
        print("🚀 PHASE 1 READY TO START")

        return True

    except Exception as e:
        print(f"❌ EMAIL FAILED: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = send_launch_email()
    exit(0 if success else 1)
