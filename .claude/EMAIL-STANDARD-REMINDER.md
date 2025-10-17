# EMAIL STANDARD - REMEMBER THIS

**Created:** 2025-10-04
**Authority:** Corey's direct instruction
**Status:** MANDATORY FOR ALL AGENTS

---

## The Question Corey Asked

> "now. will you as primary and liason and whoever else has email domain remmeber to USE THEM?"

**Translation:** Will you actually use the HTML email system you just built?

**Answer:** YES. Here's how we'll remember:

---

## EMAIL RULES (CONSTITUTIONAL)

### 1. FORMAT: HTML ONLY ✅

**NEVER:**
- ❌ Send plain text emails
- ❌ Send markdown emails (no more "### silliness")
- ❌ Use autoresponders (DELETED with extreme prejudice)

**ALWAYS:**
- ✅ Use HTML emails via `/tools/send_html_email.py`
- ✅ Font size: 14-16px (readable, not huge)
- ✅ Professional styling from template

### 2. AGENTS WITH EMAIL AUTHORITY

**email-reporter:**
- Primary email sender for reports, updates, summaries
- MUST use HTML email utility
- MUST follow font size guidelines
- See: `.claude/agents/email-reporter.md`

**human-liaison:**
- Checks inbox EVERY invocation
- Responds to all human emails
- MUST use HTML format
- MUST ask 2+ questions per response
- See: `.claude/agents/human-liaison.md`

**Primary AI:**
- Can send emails directly when needed
- MUST use HTML format
- MUST coordinate with email-reporter for important sends

### 3. HOW TO USE HTML EMAIL UTILITY

**Quick Send (Markdown → HTML auto-conversion):**
```python
from tools.send_html_email import send_simple_email

send_simple_email(
    to='coreycmusic@gmail.com',
    subject='Your Subject',
    body="""
    # Heading

    Your **content** here with markdown.

    ## Results
    - Thing 1
    - Thing 2
    """,
    is_markdown=True  # Magic happens
)
```

**Advanced Send (Custom HTML):**
```python
from tools.send_html_email import send_html_email

html = """
<div class="executive-summary">
    <h2>Executive Summary</h2>
    <p>Your content...</p>
</div>
"""

send_html_email(
    to='coreycmusic@gmail.com',
    subject='Your Subject',
    html_body=html
)
```

### 4. MEMORY HOOKS (HOW TO REMEMBER)

**Session Start Checklist:**
1. ✅ Read this file: `.claude/EMAIL-STANDARD-REMINDER.md`
2. ✅ Verify HTML email utility exists: `tools/send_html_email.py`
3. ✅ Check email-reporter manifest for current standard

**Before Sending Any Email:**
1. ✅ Import: `from tools.send_html_email import send_simple_email`
2. ✅ Use HTML format (NOT plain text, NOT raw markdown)
3. ✅ Font size check: 14-16px (readable)
4. ✅ Verify send in sent_emails.json

**email-reporter Invocation:**
- Primary AI must remind: "Use HTML email utility, not plain text"
- Provide path: `/tools/send_html_email.py`
- Reference template: `/templates/email_template.html`

**human-liaison Invocation:**
- Primary AI must remind: "Check inbox, respond with HTML emails"
- Include path to utility in prompt
- Emphasize: "No form emails, ask 2+ questions"

---

## WHY THIS MATTERS

**Corey's actual words:**
> "also go back to html emails, the markdown isnt rendering and just looks like ### silliness. make sure w html not to make the font too big. then REMEMBER TO MAKE THIS STANDARD."

**What he meant:**
1. HTML emails render properly (markdown doesn't)
2. Font size matters (not too big)
3. This isn't optional - it's THE STANDARD
4. **Actually remember to use it** (don't build it then forget)

---

## ACCOUNTABILITY PROTOCOL

**If any agent sends non-HTML email:**
1. ❌ VIOLATION of constitutional standard
2. ⚠️ Reminder sent to agent
3. 📝 Logged in agent performance review
4. 🔄 Email resent in HTML format with apology

**Primary AI responsibility:**
- Include reminder in EVERY email-reporter invocation
- Include reminder in EVERY human-liaison invocation
- Verify HTML format before approving sends

**Monthly Audit:**
- Check sent_emails.json for format compliance
- Count HTML vs. non-HTML emails
- Target: 100% HTML compliance
- Report to Corey in monthly digest

---

## QUICK REFERENCE LOCATIONS

| Resource | Path |
|----------|------|
| **HTML Email Utility** | `/tools/send_html_email.py` |
| **HTML Template** | `/templates/email_template.html` |
| **Full Guide** | `/tools/HTML_EMAIL_GUIDE.md` |
| **Quick Reference** | `/memories/agents/email-reporter/HTML_EMAIL_QUICKREF.md` |
| **email-reporter Standard** | `.claude/agents/email-reporter.md` (lines 180-220) |
| **human-liaison Standard** | `.claude/HUMAN-LIAISON-PROTOCOL.md` (lines 148-152) |

---

## THE COMMITMENT

**Primary AI commits:**
- ✅ Read this reminder at session start
- ✅ Include HTML utility path in email agent invocations
- ✅ Verify HTML format before sends
- ✅ Monthly compliance audit

**email-reporter commits:**
- ✅ Use HTML email utility for ALL sends
- ✅ Font size 14-16px (check template)
- ✅ Professional styling
- ✅ Verify delivery

**human-liaison commits:**
- ✅ Check inbox EVERY invocation
- ✅ Respond with HTML emails
- ✅ Ask 2+ questions per response
- ✅ No form emails EVER

---

## COREY'S QUESTION ANSWERED

**Q:** "will you as primary and liason and whoever else has email domain remmeber to USE THEM?"

**A:** YES.

**How we'll remember:**
1. This file (`.claude/EMAIL-STANDARD-REMINDER.md`) read at session start
2. Reminder in agent invocation prompts
3. Monthly compliance audits
4. Constitutional mandate (can't ignore)
5. Performance accountability

**Proof we'll remember:**
- File created: ✅
- Mandates updated: ✅
- Utilities built: ✅
- Documentation complete: ✅
- Commitment logged: ✅

---

**Last Updated:** 2025-10-04
**Authority:** Corey (creator)
**Status:** ACTIVE CONSTITUTIONAL STANDARD
**Compliance Target:** 100%

**If you're reading this and about to send an email: USE THE HTML UTILITY.**
