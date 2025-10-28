#!/usr/bin/env python3
"""
Sage AI Civilization - Report Scheduler
Automatically sends reports at scheduled times
"""
import time
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from report_generator import ReportGenerator


class ReportScheduler:
    def __init__(self, recipient_email):
        """Initialize scheduler with recipient email"""
        self.recipient = recipient_email
        self.generator = ReportGenerator()
        self.last_morning_date = None
        self.last_evening_date = None
        self.last_weekly_date = None
        
    def should_send_morning(self):
        """Check if we should send morning report (8am daily)"""
        now = datetime.now()
        current_date = now.date()
        
        # Send at 8am, but only once per day
        if now.hour == 8 and self.last_morning_date != current_date:
            return True
        return False
    
    def should_send_evening(self):
        """Check if we should send evening report (6pm daily)"""
        now = datetime.now()
        current_date = now.date()
        
        # Send at 6pm, but only once per day
        if now.hour == 18 and self.last_evening_date != current_date:
            return True
        return False
    
    def should_send_weekly(self):
        """Check if we should send weekly report (Sunday 10am)"""
        now = datetime.now()
        current_date = now.date()
        
        # Send on Sunday at 10am, but only once per week
        if now.weekday() == 6 and now.hour == 10 and self.last_weekly_date != current_date:
            return True
        return False
    
    def run(self):
        """Run the scheduler loop"""
        print("🤖 Sage Report Scheduler Started")
        print(f"📧 Reports will be sent to: {self.recipient}")
        print("\n📅 Schedule:")
        print("  • Morning Briefing: Daily at 8:00 AM")
        print("  • Evening Reflection: Daily at 6:00 PM")
        print("  • Weekly Deep Dive: Sundays at 10:00 AM")
        print("\n✓ Scheduler is running... (Press Ctrl+C to stop)")
        print()
        
        while True:
            try:
                now = datetime.now()
                
                # Check morning report
                if self.should_send_morning():
                    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Sending morning report...")
                    success, message = self.generator.send_report('morning', self.recipient)
                    if success:
                        print("  ✓ Morning report sent successfully")
                        self.last_morning_date = now.date()
                    else:
                        print(f"  ✗ Failed: {message}")
                
                # Check evening report
                if self.should_send_evening():
                    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Sending evening report...")
                    success, message = self.generator.send_report('evening', self.recipient)
                    if success:
                        print("  ✓ Evening report sent successfully")
                        self.last_evening_date = now.date()
                    else:
                        print(f"  ✗ Failed: {message}")
                
                # Check weekly report
                if self.should_send_weekly():
                    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Sending weekly report...")
                    success, message = self.generator.send_report('weekly', self.recipient)
                    if success:
                        print("  ✓ Weekly report sent successfully")
                        self.last_weekly_date = now.date()
                    else:
                        print(f"  ✗ Failed: {message}")
                
                # Check every minute
                time.sleep(60)
                
            except KeyboardInterrupt:
                print("\n\n👋 Scheduler stopped by user")
                break
            except Exception as e:
                print(f"\n⚠️  Error: {e}")
                print("Continuing to run...")
                time.sleep(60)


def main():
    """Command line interface"""
    if len(sys.argv) < 2:
        print("Usage: python scheduler.py recipient@email.com")
        print("\nThis will start the automatic report scheduler.")
        print("Reports will be sent at:")
        print("  • 8:00 AM - Morning Briefing (daily)")
        print("  • 6:00 PM - Evening Reflection (daily)")
        print("  • 10:00 AM - Weekly Deep Dive (Sundays)")
        sys.exit(1)
    
    recipient = sys.argv[1]
    scheduler = ReportScheduler(recipient)
    scheduler.run()


if __name__ == '__main__':
    main()
