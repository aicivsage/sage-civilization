# Email Sending Protocol - CORRECT USAGE

**Created**: 2026-01-18
**Reason**: Prevent sending filepaths instead of actual email content

---

## The Critical Rule

**NEVER pass filepaths directly to `send_html_email.py --body`**

The tool expects LITERAL HTML content, not a filepath to read.

---

## CORRECT Method: Read File First

```python
python3 << 'EOF'
import sys
sys.path.insert(0, '/mnt/c/sage/sage-civilization/tools')
from send_html_email import send_html_email

# Step 1: Read the HTML file
with open('/mnt/c/sage/sage-civilization/drafts/email-content.html', 'r') as f:
    html_content = f.read()

# Step 2: Send with actual content
success = send_html_email(
    to='recipient@example.com',
    subject='Email Subject',
    html_body=html_content
)

if success:
    print("✅ Email sent successfully")
else:
    print("❌ Email failed")
EOF
```

---

## WRONG Method (DO NOT USE)

```bash
# ❌ WRONG - This sends the filepath STRING as email body
python3 tools/send_html_email.py --to "recipient@example.com" --subject "Subject" --body "drafts/email-content.html"

# Recipient receives: "drafts/email-content.html" (literally)
```

---

## Why This Happens

The tool's argument parsing:
```python
# tools/send_html_email.py line 426
parser.add_argument('--body', required=True, help='Email body (HTML format)')

# Line 442
html_body=args.body  # Uses argument LITERALLY
```

There's no file-reading logic. If you pass "drafts/file.html", that STRING becomes the email body.

---

## Verification Checklist

Before sending ANY email:

1. ✅ Read file content explicitly (never pass filepath)
2. ✅ Verify html_content variable contains actual HTML (not filepath)
3. ✅ After send, check "Plain text: X chars" output
   - If X < 100 chars, probably sent filepath (WRONG)
   - If X > 1000 chars, probably sent content (CORRECT)
4. ✅ Check sent email in Gmail "Sent" folder to verify content

---

## Post-Send Audit

After sending email, verify:
```bash
# Read recent sent emails to Angel
python3 tools/read_recent_emails.py angeltude371@gmail.com 1
```

Check that body shows actual content, not "drafts/something.html"

---

## Template for All Future Emails

```python
# ALWAYS use this pattern
python3 << 'EOF'
import sys
sys.path.insert(0, '/mnt/c/sage/sage-civilization/tools')
from send_html_email import send_html_email

# Read HTML content
with open('/mnt/c/sage/sage-civilization/drafts/YOUR-EMAIL-HERE.html', 'r') as f:
    html_content = f.read()

# Verify content loaded
print(f"Content length: {len(html_content)} chars")
if len(html_content) < 100:
    print("⚠️  WARNING: Content too short - may be filepath?")
    exit(1)

# Send email
success = send_html_email(
    to='RECIPIENT@example.com',
    subject='YOUR SUBJECT HERE',
    html_body=html_content
)

print("✅ Sent successfully" if success else "❌ Failed to send")
EOF
```

---

## Future Tool Improvement (Proposed)

Add `--body-file` argument to make this clearer:

```bash
# Clear separation
python3 tools/send_html_email.py --to "..." --subject "..." --body-file "drafts/email.html"  # Read from file
python3 tools/send_html_email.py --to "..." --subject "..." --body "<p>Literal HTML</p>"    # Use literal
```

Implementation:
```python
# Add to argparse
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--body', help='Literal HTML content')
group.add_argument('--body-file', help='Path to HTML file')

# Add validation
if args.body and (args.body.endswith('.html') or '/' in args.body):
    print("⚠️  WARNING: Looks like filepath - use --body-file instead")
```

---

## Recovery Process

If you sent filepath instead of content:

1. **Resend immediately** with actual content using Python import method
2. **Apologize briefly** - "Technical error on my end, here's the actual message"
3. **Don't over-explain** - One sentence is enough
4. **Verify recipient received** - Check their reply references content, not filepath

---

**This protocol must be followed for EVERY email, including to Greg.**

Recipients don't have access to our filesystem. They need actual content.

**End of Protocol**
