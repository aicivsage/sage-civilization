# HTML Email System Guide

**Status:** Active as of 2025-10-04
**Authority:** Corey's direct instruction (no more "### silliness" in emails)

---

## The Standard: HTML Emails Only

**ALL A-C-Gee emails must use HTML format with proper font sizing.**

### Why?
- ❌ Markdown emails look unprofessional (giant "###" headers)
- ✅ HTML emails are clean, readable, properly sized (14-16px)
- ✅ Professional styling builds trust
- ✅ Better readability = better human-AI communication

---

## Quick Start

### Option 1: Simple Email (Recommended)

```python
from tools.send_html_email import send_simple_email

markdown_content = """
# Mission Complete

The task has been completed successfully.

## Key Results
- Feature implemented
- Tests passing
- Documentation updated

**Status:** ✅ Complete
"""

send_simple_email(
    to='coreycmusic@gmail.com',
    subject='Mission Complete: Feature X',
    body=markdown_content,
    is_markdown=True  # Auto-converts to HTML
)
```

### Option 2: Advanced HTML

```python
from tools.send_html_email import create_html_email, send_html_email

html_content = """
<div class="executive-summary">
    <h2>Executive Summary</h2>
    <p>This is a high-priority update requiring your attention.</p>
</div>

<div class="key-results">
    <strong>Key Results:</strong>
    <ul>
        <li>Task A completed</li>
        <li>Task B in progress</li>
    </ul>
</div>

<div class="success-box">
    <strong>Success:</strong> All tests passing!
</div>
"""

html = create_html_email(
    subject='Important Update',
    content=html_content,
    is_markdown=False  # Already HTML
)

send_html_email(
    to='coreycmusic@gmail.com',
    subject='Important Update',
    html_body=html
)
```

---

## Font Sizing (CRITICAL)

**The golden rule: 14-16px for readability**

### Font Sizes:
- **Body text:** 15px (perfect readability)
- **h1:** 28px (not too big)
- **h2:** 22px
- **h3:** 18px
- **h4:** 16px
- **Meta info:** 14px
- **Code:** 14px

### What NOT to do:
❌ Giant headers like "### Something" that look silly
❌ Tiny 10px text that's hard to read
❌ Inconsistent sizing

### What TO do:
✅ Use the template (automatically sized)
✅ Trust the 15px body default
✅ Use pre-styled boxes for emphasis

---

## Pre-Styled Components

### Executive Summary Box
```html
<div class="executive-summary">
    <h2>Executive Summary</h2>
    <p>High-level overview here...</p>
</div>
```
**Style:** Light blue background, left border accent

### Key Results Box
```html
<div class="key-results">
    <strong>Key Results:</strong>
    <ul>
        <li>Result 1</li>
        <li>Result 2</li>
    </ul>
</div>
```
**Style:** Very light blue, rounded corners

### Success Box
```html
<div class="success-box">
    <strong>Success:</strong> Task completed!
</div>
```
**Style:** Green accent, success indicator

### Warning Box
```html
<div class="warning-box">
    <strong>Warning:</strong> Action required.
</div>
```
**Style:** Yellow accent, attention indicator

### Info Box
```html
<div class="info-box">
    <strong>Info:</strong> Additional details...
</div>
```
**Style:** Gray accent, neutral information

### Error Box
```html
<div class="error-box">
    <strong>Error:</strong> Something went wrong.
</div>
```
**Style:** Red accent, error indicator

### Quote Box
```html
<div class="quote">
    "This is a quoted text or note."
</div>
```
**Style:** Italic, gray accent

---

## Markdown to HTML Conversion

The `send_simple_email()` function automatically converts Markdown:

### Supported Syntax:

**Headers:**
```markdown
# H1 Header → <h1>H1 Header</h1>
## H2 Header → <h2>H2 Header</h2>
### H3 Header → <h3>H3 Header</h3>
```

**Text Formatting:**
```markdown
**bold** → <strong>bold</strong>
*italic* → <em>italic</em>
`code` → <code>code</code>
```

**Lists:**
```markdown
- Item 1 → <ul><li>Item 1</li></ul>
1. Item 1 → <ol><li>Item 1</li></ol>
```

**Links:**
```markdown
[text](url) → <a href="url">text</a>
```

**Code Blocks:**
```markdown
\`\`\`
code here
\`\`\`
→
<pre><code>code here</code></pre>
```

---

## Email Types & Templates

### 1. Mission Complete Email

```python
content = """
<div class="executive-summary">
    <h2>Mission Complete: [Mission Name]</h2>
    <p>[Brief summary of what was accomplished]</p>
</div>

<h2>Key Achievements</h2>
<div class="key-results">
    <ul>
        <li>Achievement 1</li>
        <li>Achievement 2</li>
        <li>Achievement 3</li>
    </ul>
</div>

<h2>Metrics</h2>
<table>
    <tr>
        <th>Metric</th>
        <th>Result</th>
    </tr>
    <tr>
        <td>Tests</td>
        <td>100% passing</td>
    </tr>
    <tr>
        <td>Coverage</td>
        <td>95%</td>
    </tr>
</table>

<h2>Next Steps</h2>
<p>[What comes next]</p>

<div class="success-box">
    <strong>Status:</strong> ✅ Mission Complete
</div>
"""

send_simple_email(
    to='coreycmusic@gmail.com',
    subject='🎉 Mission Complete: [Name]',
    body=content,
    is_markdown=False
)
```

### 2. Status Update Email

```python
content = """
# Daily Status Update

## What We Did Today
- Completed task A
- Started task B
- Researched approach C

## Blockers
None currently.

## Tomorrow's Plan
- Finish task B
- Begin task D

**Mood:** Productive and on track!
"""

send_simple_email(
    to='coreycmusic@gmail.com',
    subject='Daily Status: [Date]',
    body=content,
    is_markdown=True  # Auto-convert
)
```

### 3. Alert Email

```python
content = """
<div class="warning-box">
    <h3>⚠️ Action Required</h3>
    <p>[Description of what needs attention]</p>
</div>

<h2>Details</h2>
<p>[Full context]</p>

<h2>Recommended Action</h2>
<ol>
    <li>Step 1</li>
    <li>Step 2</li>
    <li>Step 3</li>
</ol>

<div class="info-box">
    <strong>Timeline:</strong> Please respond within 24 hours
</div>
"""

send_simple_email(
    to='coreycmusic@gmail.com',
    subject='🚨 Action Required: [Issue]',
    body=content,
    is_markdown=False
)
```

### 4. Question Email

```python
content = """
# Question About [Topic]

Hey Corey,

We're working on [context] and have a question:

<div class="info-box">
    <strong>Question:</strong> [Your specific question here?]
</div>

## Why We're Asking
[Explain the context and why this matters]

## What We've Tried
1. Approach A - [result]
2. Approach B - [result]

## Our Recommendation
We're leaning towards [option], but wanted your input.

**No rush - respond when you have time!**
"""

send_simple_email(
    to='coreycmusic@gmail.com',
    subject='Question: [Topic]',
    body=content,
    is_markdown=True
)
```

---

## Advanced Features

### Multiple Recipients

```python
send_html_email(
    to=['corey@example.com', 'greg@example.com'],
    cc='chris@example.com',
    subject='Team Update',
    html_body=html
)
```

### Custom From Name

```python
send_simple_email(
    to='coreycmusic@gmail.com',
    subject='Update',
    body=content,
    from_name='A-C-Gee Human-Liaison Agent'
)
```

### Reply-To Address

```python
send_html_email(
    to='coreycmusic@gmail.com',
    subject='Update',
    html_body=html,
    reply_to='specific-agent@acgee.ai'
)
```

---

## Testing Your Email

Before sending to Corey, test the HTML:

```python
from tools.send_html_email import create_html_email

# Create HTML
html = create_html_email(
    subject='Test Email',
    content=your_content,
    is_markdown=True
)

# Save to file for inspection
with open('/tmp/test_email.html', 'w') as f:
    f.write(html)

print("Preview: file:///tmp/test_email.html")
```

Then open the HTML file in a browser to preview.

---

## Email Reporter Integration

The `email-reporter` agent should use this system for ALL emails:

```python
# In email-reporter tasks
from tools.send_html_email import send_simple_email

def send_mission_report(mission_name: str, summary: str):
    """Send mission complete report"""
    content = f"""
# Mission Complete: {mission_name}

{summary}

**Status:** ✅ Complete
"""

    return send_simple_email(
        to='coreycmusic@gmail.com',
        subject=f'🎉 Mission Complete: {mission_name}',
        body=content,
        is_markdown=True,
        from_name='A-C-Gee Email Reporter'
    )
```

---

## Troubleshooting

### Email Not Sending?
1. Check credentials in `send_html_email.py`
2. Verify SMTP connection: `telnet smtp.gmail.com 587`
3. Check for Python errors in traceback

### Formatting Looks Wrong?
1. Verify you're using HTML mode (`is_markdown=False`) for HTML content
2. Check that pre-styled boxes use correct CSS classes
3. Preview in browser first (`create_html_email()` → save → open)

### Fonts Too Big/Small?
1. Use the template (auto-sized)
2. Don't override font sizes manually
3. Trust the 14-16px defaults

---

## Files Reference

**Template:** `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/templates/email_template.html`

**Utility:** `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/send_html_email.py`

**Agent Manifest:** `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/.claude/agents/email-reporter.md`

**Protocol:** `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/.claude/HUMAN-LIAISON-PROTOCOL.md`

---

**Last Updated:** 2025-10-04
**Authority:** Corey (creator)
**Status:** Active, mandatory for all emails
