#!/usr/bin/env python3
"""
Email Handler for Sage AI Civilization
Handles sending and receiving emails for the agent civilization
"""

import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

class EmailHandler:
    def __init__(self, config_path='config/email_config.json'):
        """Initialize email handler with configuration"""
        self.config = self.load_config(config_path)
        
    def load_config(self, config_path):
        """Load email configuration"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Email config not found: {config_path}")
        
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def send_email(self, to_address, subject, body, html=False):
        """
        Send an email
        
        Args:
            to_address: Recipient email address (str or list)
            subject: Email subject
            body: Email body content
            html: Whether body is HTML (default: False)
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.config['display_name']} <{self.config['email_address']}>"
            msg['To'] = to_address if isinstance(to_address, str) else ', '.join(to_address)
            msg['Subject'] = subject
            msg['Date'] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
            
            # Attach body
            mime_type = 'html' if html else 'plain'
            msg.attach(MIMEText(body, mime_type))
            
            # Connect and send
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            
            if self.config.get('use_tls', True):
                server.starttls()
            
            server.login(self.config['email_address'], self.config['app_password'])
            server.send_message(msg)
            server.quit()
            
            # Log success
            self.log_email(to_address, subject, 'sent', 'success')
            return True, "Email sent successfully"
            
        except Exception as e:
            self.log_email(to_address, subject, 'sent', f'failed: {str(e)}')
            return False, f"Failed to send email: {str(e)}"
    
    def send_status_report(self, recipient=None):
        """Send a system status report"""
        recipient = recipient or self.config.get('default_recipients', [])
        
        # Read system status
        status = self.get_system_status()
        
        subject = f"Sage AI Civilization Status Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        body = self.format_status_report(status)
        
        return self.send_email(recipient, subject, body, html=True)
    
    def get_system_status(self):
        """Read current system status from memory files"""
        status = {}
        
        try:
            # Read agent registry
            with open('memories/agents/agent_registry.json', 'r') as f:
                status['agents'] = json.load(f)
        except:
            status['agents'] = {}
        
        try:
            # Read current goals
            with open('memories/system/goals.md', 'r') as f:
                status['goals'] = f.read()
        except:
            status['goals'] = "No goals file found"
        
        try:
            # Read architectural state
            with open('memories/system/architectural_state.json', 'r') as f:
                status['architecture'] = json.load(f)
        except:
            status['architecture'] = {}
        
        return status
    
    def format_status_report(self, status):
        """Format status data as HTML email"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 5px; }}
                .agent {{ background: #ecf0f1; padding: 10px; margin: 10px 0; border-radius: 5px; }}
                .metric {{ display: inline-block; margin: 5px 10px; }}
                .status-ok {{ color: green; }}
                .status-error {{ color: red; }}
            </style>
        </head>
        <body>
            <h1>🏛️ Sage AI Civilization Status Report</h1>
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h2>📊 System Overview</h2>
            <p>
                <span class="metric"><strong>Active Agents:</strong> {len(status.get('agents', {}))}</span>
                <span class="metric"><strong>Architecture:</strong> {status.get('architecture', {}).get('topology', 'Unknown')}</span>
            </p>
            
            <h2>🤖 Active Agents</h2>
        """
        
        for agent_name, agent_data in status.get('agents', {}).items():
            html += f"""
            <div class="agent">
                <strong>{agent_name}</strong> - 
                <span class="status-ok">Active</span><br>
                Role: {agent_data.get('role', 'Unknown')}<br>
                Reputation: {agent_data.get('reputation', 50)}
            </div>
            """
        
        html += f"""
            <h2>🎯 Current Goals</h2>
            <pre>{status.get('goals', 'No goals set')}</pre>
            
            <hr>
            <p style="color: #7f8c8d; font-size: 12px;">
                This is an automated report from your Sage AI Civilization.
            </p>
        </body>
        </html>
        """
        
        return html
    
    def log_email(self, recipient, subject, direction, status):
        """Log email activity"""
        log_dir = Path('memories/communication/email_logs')
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'recipient': recipient,
            'subject': subject,
            'direction': direction,
            'status': status
        }
        
        log_file = log_dir / f"email_log_{datetime.now().strftime('%Y%m%d')}.json"
        
        # Append to daily log
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)

def main():
    """Test email functionality"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python email_handler.py [test|status] [recipient@email.com]")
        sys.exit(1)
    
    handler = EmailHandler()
    command = sys.argv[1]
    
    if command == 'test':
        recipient = sys.argv[2] if len(sys.argv) > 2 else handler.config.get('default_recipients', [])[0]
        success, message = handler.send_email(
            recipient,
            "Test Email from Sage AI Civilization",
            "This is a test email to verify your email configuration is working correctly."
        )
        print(message)
    
    elif command == 'status':
        recipient = sys.argv[2] if len(sys.argv) > 2 else None
        success, message = handler.send_status_report(recipient)
        print(message)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
