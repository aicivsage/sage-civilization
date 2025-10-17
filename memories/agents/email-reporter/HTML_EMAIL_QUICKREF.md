# HTML Email Quick Reference - Email Reporter

**MANDATORY:** All emails must use HTML format (not markdown text)

---

## Quick Send (Most Common)

```python
from tools.send_html_email import send_simple_email

markdown_content = """
# Subject Here

Your email content in **Markdown** format.

- Auto-converts to HTML
- Proper 14-16px fonts
- Professional styling
"""

send_simple_email(
    to='coreycmusic@gmail.com',
    subject='Email Subject',
    body=markdown_content,
    is_markdown=True
)
```

---

## Pre-Styled Boxes

Use these for emphasis:

```html
<div class="executive-summary">
    <h2>Executive Summary</h2>
    <p>High-level overview...</p>
</div>

<div class="success-box">Success message</div>
<div class="warning-box">Warning message</div>
<div class="info-box">Info message</div>
<div class="error-box">Error message</div>
```

---

## Font Sizes (CRITICAL)

- Body: 15px ✅
- H1: 28px ✅
- H2: 22px ✅
- H3: 18px ✅
- Code: 14px ✅

**NEVER:** Giant markdown headers like "### Silliness"
**ALWAYS:** Use the template (auto-sized)

---

## Common Patterns

### Mission Complete
```python
content = """
<div class="executive-summary">
    <h2>Mission Complete: [Name]</h2>
    <p>[Summary]</p>
</div>

<div class="key-results">
    <strong>Key Results:</strong>
    <ul>
        <li>Result 1</li>
        <li>Result 2</li>
    </ul>
</div>

<div class="success-box">✅ Complete</div>
"""

send_simple_email(
    to='coreycmusic@gmail.com',
    subject='🎉 Mission Complete: [Name]',
    body=content,
    is_markdown=False
)
```

### Status Update
```python
content = """
# Daily Update

## Completed
- Task A
- Task B

## In Progress
- Task C

## Next
- Task D
"""

send_simple_email(
    to='coreycmusic@gmail.com',
    subject='Daily Update: [Date]',
    body=content,
    is_markdown=True
)
```

### Question
```python
content = """
# Question: [Topic]

<div class="info-box">
    <strong>Question:</strong> [Your question?]
</div>

## Context
[Why we're asking]

## What We've Tried
- Approach A
- Approach B

**No rush - respond when you can!**
"""

send_simple_email(
    to='coreycmusic@gmail.com',
    subject='Question: [Topic]',
    body=content,
    is_markdown=True
)
```

---

## Files

- **Template:** `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/templates/email_template.html`
- **Utility:** `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/send_html_email.py`
- **Full Guide:** `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/HTML_EMAIL_GUIDE.md`

---

**Remember:** HTML emails only. No plain markdown. Readable fonts (14-16px). Professional styling.
