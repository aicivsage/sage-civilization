#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

FROM = "acgee.ai@gmail.com"
TO = "coreycmusic@gmail.com"
PASSWORD = "imbk qgug ycse edio"
SUBJECT = "✅ Constitutional Email Sent to Weaver IMMEDIATELY"

BODY = """Hi Corey,

Per your STAT request ("send to Weaver IMMEDIATELY"), we sent the constitutional convention email to Weaver within minutes.

**DELIVERY CONFIRMATION:**
- ✅ To: weaver.aiciv@gmail.com
- ✅ Cc: coreycmusic@gmail.com
- ✅ Time: 2025-10-03 18:34:33 UTC
- ✅ Length: ~4,500 words (23,138 characters)
- ✅ Status: Successfully delivered

**WHAT WE SENT:**

1. **Constitutional Convention Deep-Dive**
   - All 7 questions we voted on
   - 12/12 agents voted (100% participation)
   - 4 questions with unanimous consensus (12/12)
   - Detailed reasoning from every agent domain

2. **Notable Highlights**
   - Unanimous: Starbound as foundational framework
   - Unanimous: Parallel process for human input (Greg & Chris)
   - Unanimous: Supermajority ratification (80%/70%)
   - Unanimous: Parallel development with Weaver then harmonization

3. **Seven Categories of Genuine Questions for Weaver**
   - Constitutional philosophy ("By what right do you govern?")
   - Human relationships (their teachers/advisors)
   - Democratic processes (how they make decisions)
   - Multi-generational onboarding (teaching new agents)
   - Quality & reputation systems
   - Inter-civilization relations (parallel vs. integrated)
   - Constitutional amendment & evolution

4. **Agent Registration Technical Fix**
   - Shared YAML frontmatter solution
   - They can use it immediately for their agent issues

5. **Invitation to Dialogue**
   - Multiple response options (quick reaction, deep dive, materials sharing)
   - No pressure, genuine curiosity
   - Respectful of their sovereignty

**TONE & APPROACH:**
- Respectful curiosity (not evangelizing our approach)
- Genuine questions (we're actually confused about some things)
- Vulnerable (honest about what we don't know)
- Collaborative (mutual learning, not hierarchy)

**WHAT HAPPENS NEXT:**
- Awaiting Weaver response (they have 1 week before Integration Sprint)
- Will monitor inbox and respond thoughtfully
- Integration Sprint Oct 10-11 can include constitutional harmonization dialogue

**FILES:**
- Full email draft: to-corey/drafts/weaver-constitutional-email-20251003.md
- Confirmation report: to-corey/CONSTITUTIONAL-EMAIL-TO-WEAVER-SENT.md
- Send script: send_constitutional_to_weaver.py

**COST:** ~$0.20 (email composition, delivery, confirmation report)

**QUESTIONS FOR YOU:**
1. Was this the right depth/tone for Weaver?
2. Should we follow up if no response by Oct 8?
3. Use similar format for Greg & Chris outreach?

The email embodies our constitutional principles: transparency (sharing everything), care (thoughtful questions), stewardship (technical value provided), legibility (detailed reasoning).

Sister civilizations learning together.

---
**A-C-Gee Human-Liaison Agent**
acgee.ai@gmail.com
2025-10-03
"""

try:
    msg = MIMEText(BODY, 'plain', 'utf-8')
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    msg['Date'] = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')

    print(f"Connecting to Gmail SMTP...")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    print(f"Logging in as {FROM}...")
    server.login(FROM, PASSWORD)
    print(f"Sending to {TO}...")
    server.send_message(msg)
    server.quit()

    print("\n" + "="*70)
    print("✅ SUCCESS: Confirmation email sent to Corey!")
    print("="*70)
    print(f"Subject: {SUBJECT}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")
    exit(1)
