# CRITICAL EMAIL TOOL BUG - January 18, 2026

## What Happened

**Sent filepaths to recipients instead of actual email content.**

Angel received: `drafts/angel-silver-response-20260118.html` (literal filepath)
NOT: The actual silver investment guidance email

**Greg's discovery**: "Angel does NOT have access to our directories, she needs the ACTUAL doc, sent in an email. This is true for EVERY email response, including to me."

---

## Root Cause

### The Tool Usage Error

**What I did (WRONG):**
```bash
python3 tools/send_html_email.py --to "angeltude371@gmail.com" --subject "..." --body "drafts/angel-silver-response-20260118.html"
```

**What the tool does:**
```python
# Line 426: parser.add_argument('--body', required=True, help='Email body (HTML format)')
# Line 442: html_body=args.body
```

The tool treats `--body` as LITERAL CONTENT, not as a filepath to read.

**Result:** Sent the string "drafts/angel-silver-response-20260118.html" as the email body.

---

## Evidence

**First email (WRONG):**
```
Plain text: 42 chars
```
42 characters = length of "drafts/angel-silver-response-20260118.html"

**Second email (CORRECT):**
```
Plain text: 4058 chars
```
4058 characters = actual email content length

---

## The Systemic Problem

**This affects EVERY email I've sent using this pattern:**

1. Angel's follow-up (Jan 18): Sent "drafts/angel-follow-up-20260118.html" instead of content ❌
2. Angel's silver response (Jan 18, first attempt): Sent "drafts/angel-silver-response-20260118.html" instead of content ❌
3. Potentially others...

**How many recipients received filepaths instead of actual emails?**

Need to audit ALL emails sent via this tool to check for this pattern.

---

## Correct Usage Patterns

### Option 1: Read file first, then pass content (CORRECT)
```python
python3 << 'EOF'
import sys
sys.path.insert(0, '/mnt/c/sage/sage-civilization/tools')
from send_html_email import send_html_email

with open('drafts/email-content.html', 'r') as f:
    html_content = f.read()

send_html_email(
    to='recipient@example.com',
    subject='Subject',
    html_body=html_content
)
EOF
```

### Option 2: Modify tool to accept --body-file argument (FUTURE IMPROVEMENT)
```python
# Add to argparse
parser.add_argument('--body-file', help='Path to HTML file containing email body')

# Add logic
if args.body_file:
    with open(args.body_file, 'r') as f:
        html_body = f.read()
else:
    html_body = args.body
```

---

## Immediate Actions Taken

1. ✅ Resent Angel's silver email with actual content (using Python import method)
2. ✅ Documented this critical bug
3. [ ] Audit all recent emails to identify other filepath sends
4. [ ] Apologize to affected recipients
5. [ ] Implement tool improvement to accept --body-file

---

## Email Audit Required

**Check these recent emails for filepath bug:**

Search sent emails for strings matching `drafts/*.html` or similar patterns.

Potential affected emails:
- Angel follow-up (Jan 18) - CONFIRMED WRONG
- Angel silver response (Jan 18, first send) - CONFIRMED WRONG
- Corey celebration email (Jan 16) - NEEDS CHECK
- Weaver bi-weekly check-in (Jan 16) - NEEDS CHECK
- Any others using same command pattern

---

## Tool Improvement Proposal

### Current (Ambiguous):
```bash
--body "content or filepath???"  # Unclear what this accepts
```

### Proposed (Clear):
```bash
--body "actual HTML content here"  # Literal content
--body-file "path/to/file.html"    # Read from file
```

**Implementation:**
```python
# In argparse section
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--body', help='Email body as literal HTML string')
group.add_argument('--body-file', help='Path to HTML file containing email body')

# In main execution
if args.body_file:
    with open(args.body_file, 'r') as f:
        html_body = f.read()
else:
    html_body = args.body
```

**Validation:**
```python
# Detect if user passed filepath when they should use --body-file
if args.body and (args.body.endswith('.html') or '/' in args.body):
    print("⚠️  WARNING: It looks like you passed a filepath to --body")
    print("   Use --body-file for files, --body for literal content")
    print("   Treating as literal content (this may not be what you want)")
```

---

## Testing Plan

### Test 1: Filepath detection
```bash
# Should warn user
python3 tools/send_html_email.py --to test@example.com --subject "Test" --body "drafts/test.html"
```

### Test 2: Correct file usage
```bash
# Should read file and send content
python3 tools/send_html_email.py --to test@example.com --subject "Test" --body-file "drafts/test.html"
```

### Test 3: Correct literal usage
```bash
# Should send literal HTML
python3 tools/send_html_email.py --to test@example.com --subject "Test" --body "<p>Hello!</p>"
```

---

## Impact Assessment

**Severity**: CRITICAL

**Recipients affected**: Minimum 2 (Angel x2), potentially more

**Trust damage**: HIGH - Recipients think we're sending them file paths, not professional emails

**Repair needed**:
1. Identify all affected emails
2. Apologize and resend with actual content
3. Explain technical issue (not lack of care)
4. Implement tool fix to prevent recurrence

---

## Root Cause Analysis

**Why this happened:**

1. **Assumption error**: I assumed --body accepted filepath (like many CLI tools)
2. **No validation**: Tool doesn't warn when filepath-like string passed
3. **No testing**: Didn't verify email content before sending
4. **No monitoring**: Didn't check sent emails to catch this

**Systemic weaknesses revealed:**
- Tools lack input validation
- No email content verification before send
- No post-send audit (did recipient get what we intended?)
- Assumption-based usage without reading tool documentation

---

## Prevention Strategies

### 1. Tool Input Validation
Add warnings when suspicious patterns detected:
- Strings ending in .html passed to --body
- Strings containing '/' passed to --body
- Very short content (<100 chars) that looks like filepath

### 2. Pre-Send Verification
Before sending email, show preview:
```
About to send:
To: recipient@example.com
Subject: Subject line
Body preview: [first 200 chars]

Proceed? (y/n)
```

### 3. Post-Send Audit
After sending, verify:
- Email appears in "Sent" folder
- Content matches what we intended to send
- Recipient received actual content (not filepath)

### 4. Read Tool Documentation
Before using ANY tool with --body or similar:
1. Read argparse section
2. Check if it expects content or filepath
3. Test with dummy data first
4. Verify output matches intent

---

## Commitment

**I will:**
1. Audit all recent emails for this bug
2. Apologize and resend to affected recipients
3. Implement --body-file improvement
4. Add validation warnings to tool
5. ALWAYS read file content explicitly before passing to tools
6. NEVER assume tools accept filepaths without checking

**This cannot happen again.**

---

**Date**: 2026-01-18
**Severity**: CRITICAL
**Status**: Bug identified, Angel corrected, tool fix proposed, audit pending
**Next**: Complete email audit, implement tool improvements, apologize to affected recipients
