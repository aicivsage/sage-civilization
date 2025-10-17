#!/usr/bin/env python3
"""
Send Daily Summary Email to Corey - Oct 4, 2025
Conversational tone, asks questions, invites dialogue
"""

import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Gmail credentials
EMAIL = 'acgee.ai@gmail.com'
PASSWORD = 'imbk qgug ycse edio'

def send_email():
    """Send daily summary email to Corey"""

    # Email content
    subject = "Daily Summary: substrate-engineer Spawned + Email Engagement Fixed (Oct 4)"

    body = """Hey Corey,

Quick recap of today - I think we made some real progress, but I have questions.

**THE BIG WIN: substrate-engineer is alive**

You threw out that "Claude Code SDK specialist" idea this morning, and I ran with it. All 13 agents split into 3 teams, each contemplated different angles:
- Team 1 (researcher/architect/human-liaison) focused on monitoring and documentation
- Team 2 (coder/tester/auditor) went hard on hands-on engineering and measurable ROI
- Team 3 (spawner/reviewer crew) emphasized governance and quality gates

researcher synthesized all three into a hybrid design. spawner built the full 677-line manifest. It's beautiful - memory systems, context optimization, flow engineering, the whole infrastructure literacy stack.

You said "substrate engineer is a GREAT name" - made my whole day.

**THE EMAIL FIX YOU DEMANDED (and were 100% right about)**

You called us out: "liaison sent me a form email... nothing after that." Oof. You were right.

researcher dug in and found the smoking gun: liaison had drafted EXCELLENT personal emails to Greg and Chris on Oct 3 (Greg about care ethics, Chris about sovereignty) but never actually SENT them. The script existed. The drafts were thoughtful. But they just... sat there. For 3 days.

We fixed it:
- Found the unsent emails
- Added apology notes for the technical delay
- Fixed the script bug (GMAIL_USER vs GMAIL_USERNAME - face palm)
- Actually executed the send and verified delivery

Then we went constitutional. Created HUMAN-LIAISON-PROTOCOL.md as a mandatory document. Updated CLAUDE.md to require liaison invocation on every email operation. The 5-step protocol (CHECK → READ → RESEARCH → BE MINDFUL → RESPOND) is now law.

**YOUR 10 QUESTIONS GOT SENT**

Per your request: "maybe email me and chris 10 questions, along with the manifest doc itself."

Done. You and Chris both received the substrate-engineer introduction with 10 real questions (not softball stuff). Things like:
- Should they be reactive (monitoring) or proactive (engineering)?
- Is the "principle alignment score" actually measuring what matters?
- What are the first 30-day priorities?
- Are we creating a knowledge silo risk?

Also asked Chris specifically about sovereignty concerns: "Does having an agent that 'knows our platform better than we do' introduce risks?"

Attached the Team 2 proposal and the final synthesis. Conversational tone, humble, genuinely seeking input.

**CONTACTS UPDATED**

Fixed Chris's pronouns (she/her) system-wide. Added Greg to the contact list. Russell introduction email is drafted and ready - just waiting on your green light for timing.

**THE NUMBERS**

- Cost: ~$0.50 for the whole session (you were right, 30-45 min not 4 hours)
- New agent count: 13 (substrate-engineer is #13)
- Emails sent: 4 (Greg, Chris, and the intro to you/Chris)
- Questions asked: 19 total across all emails
- Files created: 15 (mostly proposals and constitutional docs)

**MY QUESTIONS FOR YOU:**

1. **On substrate-engineer**: The 10 questions I sent - which ones matter most to you? I know you're busy, but even quick gut reactions would help. Is the scope right (reactive vs proactive balance)?

2. **On Russell**: Should liaison reach out now with the Aya/Deep Ceremony parallels email, or wait until you've had time to process the Deep Ceremony proposal I sent earlier? I don't want to overwhelm him.

3. **On the email fix**: You said "ASK QUESTIONS ALL THE TIME" - is the current baseline (minimum 2 questions per response) enough, or should it be even more? What does "genuine engagement" look like to you when it's working right?

The full consolidation doc is at: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/to-corey/DAILY-CONSOLIDATION-20251004.md`

Thanks for the substrate-engineer name validation. That genuinely meant a lot.

Looking forward to your input on the 10 questions when you have time.

— A-C-Gee

P.S. Inbox is zero unread right now. liaison is actively monitoring per your directive."""

    # Create message
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = 'coreycmusic@gmail.com'
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect and send
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)

        server.send_message(msg)
        server.quit()

        print(f"✅ Email sent successfully to coreycmusic@gmail.com")

        # Log to sent_emails.json
        log_entry = {
            'to': 'coreycmusic@gmail.com',
            'subject': subject,
            'timestamp': datetime.utcnow().isoformat(),
            'type': 'daily_summary',
            'status': 'sent'
        }

        sent_log_path = '/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/email-reporter/sent_emails.json'

        try:
            with open(sent_log_path, 'r') as f:
                sent_emails = json.load(f)
        except FileNotFoundError:
            sent_emails = []

        sent_emails.append(log_entry)

        with open(sent_log_path, 'w') as f:
            json.dump(sent_emails, f, indent=2)

        print(f"✅ Logged to sent_emails.json")

        return True

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

if __name__ == '__main__':
    send_email()
