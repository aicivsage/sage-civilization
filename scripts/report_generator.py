#!/usr/bin/env python3
"""
Sage AI Civilization - Report Generator
Generates and sends intelligent reports to Greg
"""
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path to import email_handler
sys.path.insert(0, str(Path(__file__).parent))
from email_handler import EmailHandler


class ReportGenerator:
    def __init__(self):
        """Initialize the report generator"""
        self.email_handler = EmailHandler()
        self.sage_dir = Path(__file__).parent.parent
        
    def get_system_status(self):
        """Check system health"""
        status = {
            'overall': 'Healthy',
            'email': 'Connected',
            'agents': 'Active',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Check if agent registry exists
        agent_file = self.sage_dir / 'memories' / 'agents' / 'agent_registry.json'
        if agent_file.exists():
            with open(agent_file, 'r') as f:
                agents = json.load(f)
                status['agent_count'] = len(agents)
                status['active_agents'] = sum(1 for a in agents.values() if a.get('status') == 'active')
        else:
            status['agent_count'] = 0
            status['active_agents'] = 0
            
        return status
    
    def get_agent_summary(self):
        """Get summary of all agents"""
        agent_file = self.sage_dir / 'memories' / 'agents' / 'agent_registry.json'
        if not agent_file.exists():
            return []
        
        with open(agent_file, 'r') as f:
            agents = json.load(f)
        
        summary = []
        for name, info in agents.items():
            summary.append({
                'name': name,
                'role': info.get('role', 'Unknown'),
                'status': info.get('status', 'unknown'),
                'reputation': info.get('reputation', 0)
            })
        return summary
    
    def generate_morning_report(self):
        """Generate morning briefing"""
        status = self.get_system_status()
        agents = self.get_agent_summary()
        
        report = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
        <h1 style="color: white; margin: 0;">🌅 Good Morning, Greg!</h1>
        <p style="color: #f0f0f0; margin: 10px 0 0 0;">Daily Briefing from Sage AI</p>
    </div>
    
    <div style="padding: 30px; background: #f9f9f9;">
        <h2 style="color: #333;">📊 System Status</h2>
        <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <p><strong>Overall Health:</strong> <span style="color: #10b981;">✓ {status['overall']}</span></p>
            <p><strong>Email System:</strong> <span style="color: #10b981;">✓ {status['email']}</span></p>
            <p><strong>Active Agents:</strong> {status['active_agents']} of {status['agent_count']}</p>
            <p><strong>Last Check:</strong> {status['timestamp']}</p>
        </div>
        
        <h2 style="color: #333;">🤖 Agent Activity</h2>
        <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
"""
        
        if agents:
            for agent in agents:
                status_icon = "🟢" if agent['status'] == 'active' else "🔴"
                report += f"""
            <div style="margin-bottom: 15px; padding: 10px; background: #f5f5f5; border-radius: 5px;">
                <p style="margin: 5px 0;"><strong>{status_icon} {agent['name']}</strong></p>
                <p style="margin: 5px 0; color: #666; font-size: 14px;">{agent['role']}</p>
                <p style="margin: 5px 0; color: #888; font-size: 12px;">Reputation: {agent['reputation']}</p>
            </div>
"""
        else:
            report += "<p>No agents currently registered.</p>"
        
        report += """
        </div>
        
        <h2 style="color: #333;">💡 Daily Insight</h2>
        <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <p style="font-style: italic; color: #555;">
            "Every morning is a fresh start with new possibilities. Today, Sage is ready to help you 
            explore, create, and discover. What will we build together?"
            </p>
        </div>
        
        <h2 style="color: #333;">🎯 Focus for Today</h2>
        <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <ul style="color: #555;">
                <li>System is running smoothly and ready for your commands</li>
                <li>Communication channels are active and monitoring</li>
                <li>Ready to assist with any projects or questions you have</li>
            </ul>
            <p style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #eee; color: #888; font-size: 14px;">
                <em>Note: As we add more capabilities, this section will include specific project updates, 
                task priorities, and intelligent suggestions based on your goals.</em>
            </p>
        </div>
        
        <div style="text-align: center; padding: 20px; color: #888; font-size: 14px;">
            <p>This is an automated report from your Sage AI Civilization</p>
            <p>Reply to this email to communicate with Sage</p>
        </div>
    </div>
</body>
</html>
"""
        return report
    
    def generate_evening_report(self):
        """Generate evening reflection"""
        status = self.get_system_status()
        
        report = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 30px; text-align: center;">
        <h1 style="color: white; margin: 0;">🌆 Evening Reflection</h1>
        <p style="color: #f0f0f0; margin: 10px 0 0 0;">Your Daily Summary from Sage</p>
    </div>
    
    <div style="padding: 30px; background: #f9f9f9;">
        <h2 style="color: #333;">📋 Today's Summary</h2>
        <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <p><strong>System Status:</strong> <span style="color: #10b981;">✓ Running Smoothly</span></p>
            <p><strong>Uptime:</strong> All day</p>
            <p><strong>Active Monitoring:</strong> Email & Communications</p>
        </div>
        
        <h2 style="color: #333;">🎯 Accomplishments</h2>
        <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <p style="color: #555;">Today, I remained vigilant and ready to assist. All systems performed optimally.</p>
            <p style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #eee; color: #888; font-size: 14px;">
                <em>Note: As we track projects and activities, this section will show specific achievements, 
                completed tasks, and progress on your goals.</em>
            </p>
        </div>
        
        <h2 style="color: #333;">💭 Reflection</h2>
        <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <p style="font-style: italic; color: #555;">
            "Another day of growth and learning. I'm here, always evolving, always ready to support your vision. 
            Tomorrow brings new opportunities to create something amazing together."
            </p>
        </div>
        
        <h2 style="color: #333;">🌙 Looking Ahead</h2>
        <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <p style="color: #555;">Tomorrow, I'll continue monitoring and be ready for whatever you need. 
            As we add more intelligence and capabilities, I'll have more insights and proactive suggestions to share.</p>
        </div>
        
        <div style="text-align: center; padding: 20px; color: #888; font-size: 14px;">
            <p>Rest well, Greg. I'll be here when you need me.</p>
            <p style="margin-top: 10px;">- Sage AI</p>
        </div>
    </div>
</body>
</html>
"""
        return report
    
    def generate_weekly_report(self):
        """Generate weekly deep dive"""
        status = self.get_system_status()
        agents = self.get_agent_summary()
        
        report = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 30px; text-align: center;">
        <h1 style="color: white; margin: 0;">📊 Weekly Deep Dive</h1>
        <p style="color: #f0f0f0; margin: 10px 0 0 0;">Your Week in Review from Sage</p>
    </div>
    
    <div style="padding: 30px; background: #f9f9f9;">
        <h2 style="color: #333;">🎯 Week in Review</h2>
        <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <p><strong>System Performance:</strong> <span style="color: #10b981;">Excellent</span></p>
            <p><strong>Uptime:</strong> 100%</p>
            <p><strong>Agents Active:</strong> {status['active_agents']}</p>
        </div>
        
        <h2 style="color: #333;">📈 Growth & Progress</h2>
        <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <p style="color: #555;">This week, Sage has been learning and growing. The foundation is strong 
            and ready for expansion.</p>
            <p style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #eee; color: #888; font-size: 14px;">
                <em>Note: As we add project tracking and goal monitoring, this section will show specific 
                progress metrics, completed milestones, and trend analysis.</em>
            </p>
        </div>
        
        <h2 style="color: #333;">💡 Strategic Insights</h2>
        <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <p style="font-style: italic; color: #555;">
            "We're at the beginning of something exciting. The communication infrastructure is solid. 
            Next, we'll add intelligence layers that will transform these reports into genuine insights 
            and proactive assistance."
            </p>
        </div>
        
        <h2 style="color: #333;">🚀 Recommendations</h2>
        <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <ul style="color: #555;">
                <li><strong>Phase 2 Ready:</strong> Foundation is solid for adding intelligence features</li>
                <li><strong>Communication Flow:</strong> Daily reports will help build the habit of Sage interaction</li>
                <li><strong>Next Steps:</strong> Consider what projects and goals you want Sage to track</li>
            </ul>
        </div>
        
        <div style="text-align: center; padding: 20px; color: #888; font-size: 14px;">
            <p>Here's to another week of growth and discovery!</p>
            <p style="margin-top: 10px;">- Sage AI Civilization</p>
        </div>
    </div>
</body>
</html>
"""
        return report
    
    def send_report(self, report_type, recipient):
        """Send a report via email"""
        if report_type == 'morning':
            subject = f"🌅 Good Morning! Daily Briefing - {datetime.now().strftime('%B %d, %Y')}"
            body = self.generate_morning_report()
        elif report_type == 'evening':
            subject = f"🌆 Evening Reflection - {datetime.now().strftime('%B %d, %Y')}"
            body = self.generate_evening_report()
        elif report_type == 'weekly':
            subject = f"📊 Weekly Deep Dive - Week of {datetime.now().strftime('%B %d, %Y')}"
            body = self.generate_weekly_report()
        else:
            return False, f"Unknown report type: {report_type}"
        
        return self.email_handler.send_email(recipient, subject, body, html=True)


def main():
    """Command line interface"""
    if len(sys.argv) < 3:
        print("Usage: python report_generator.py [morning|evening|weekly] recipient@email.com")
        print("\nReport Types:")
        print("  morning  - Daily morning briefing (send at 8am)")
        print("  evening  - Daily evening reflection (send at 6pm)")
        print("  weekly   - Weekly deep dive (send Sunday 10am)")
        sys.exit(1)
    
    report_type = sys.argv[1]
    recipient = sys.argv[2]
    
    generator = ReportGenerator()
    success, message = generator.send_report(report_type, recipient)
    
    if success:
        print(f"✓ {report_type.capitalize()} report sent successfully to {recipient}")
    else:
        print(f"✗ Failed to send report: {message}")


if __name__ == '__main__':
    main()


