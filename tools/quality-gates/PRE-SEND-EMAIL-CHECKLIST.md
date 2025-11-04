# Pre-Send Email Checklist

**Purpose**: Ensure emails are correct on FIRST send attempt
**When to use**: Before EVERY external email send
**Owner**: email-sender agent (with Primary oversight)

---

## Phase 1: Content Preparation

- [ ] **HTML email created**
  - Valid HTML structure
  - Proper email-safe CSS (inline styles, tables)
  - No external dependencies (all images hosted)

- [ ] **Content complete**
  - Subject line written
  - Body content finalized
  - Call-to-action present
  - Footer with unsubscribe/contact info

- [ ] **Formatting correct**
  - Font size 14-16px (readable)
  - Proper line spacing
  - Colors contrast well
  - Mobile-responsive design

---

## Phase 2: Identity Verification (CRITICAL)

- [ ] **Sender identity correct**
  - From: Sage AI Civilization <aicivsage@gmail.com>
  - NOT gregsmithwick@gmail.com
  - NOT sage.ai.civilization@gmail.com
  - Reply-To set correctly

- [ ] **Signature correct**
  - Sage AI Civilization
  - aicivsage@gmail.com
  - Proper attribution

- [ ] **Brand consistency**
  - Tone matches Sage values
  - Sage green colors (#87a96b)
  - Logo/branding correct

**STOP**: If ANY identity element is wrong, fix before proceeding.

---

## Phase 3: Recipient Verification

- [ ] **Recipient list reviewed**
  - Load from priority_contacts.json (or equivalent)
  - Verify emails are current
  - Confirm intended audience

- [ ] **User approval on recipients**
  - Show list to user
  - User confirms "send to these people"
  - Get explicit approval

- [ ] **No accidental includes**
  - No test emails in production list
  - No deactivated contacts
  - No duplicates

**STOP**: If recipient list is uncertain, get user confirmation.

---

## Phase 4: Tool Verification

- [ ] **Understand tool API**
  - Read send_html_email.py usage (--help)
  - Verify parameter types:
    - `--body` expects HTML CONTENT (not file path!)
    - `--to` expects single email address
    - `--subject` expects plain text

- [ ] **Content loading correct**
  - If using HTML file: Read file FIRST, pass content to --body
  - If using inline HTML: Verify it's complete
  - NOT passing file path as --body parameter

- [ ] **Tool tested recently**
  - Confirm tool hasn't changed
  - Verify dependencies installed
  - Check for any error messages

**STOP**: If tool behavior is uncertain, test with simple example first.

---

## Phase 5: Test Send (MANDATORY)

- [ ] **Send to self first**
  - Use aicivsage@gmail.com as test recipient
  - Full HTML content (not shortened)
  - Same subject line as production

- [ ] **Verify test email received**
  - Check inbox
  - Open email
  - View in email client (Gmail, etc.)

- [ ] **Review rendered email**
  - Subject line correct
  - From address correct
  - HTML renders correctly
  - Images load (if embedded)
  - Links work
  - Mobile responsive

- [ ] **Check spam folder**
  - Ensure not filtered
  - Verify deliverability
  - Check spam score if possible

**STOP**: If test email fails ANY check, fix before production send.

---

## Phase 6: User Preview & Approval

- [ ] **Forward test email to user**
  - OR screenshot rendered email
  - Show exactly what recipients will see
  - Include subject line

- [ ] **Get explicit approval**
  - User confirms content looks good
  - User approves recipient list
  - User says "send it"

- [ ] **Incorporate feedback**
  - Make requested changes
  - Send new test email
  - Get second approval

**STOP**: Do NOT send to recipients without user approval.

---

## Phase 7: Production Send

- [ ] **Send to each recipient individually**
  - Loop through recipient list
  - One email per person (personalization possible)
  - Small delay between sends (2 seconds)

- [ ] **Use skip-duplicate-check flag**
  - Only after test send verified
  - Prevents blocking production send

- [ ] **Log each send**
  - Record who received email
  - Timestamp each send
  - Note any failures

- [ ] **Monitor for errors**
  - Watch for SMTP errors
  - Check authentication issues
  - Verify no rate limiting

**STOP**: If ANY send fails, pause and diagnose before continuing.

---

## Phase 8: Post-Send Verification

- [ ] **Check sent folder**
  - Verify emails in sent folder
  - Confirm correct content (not file paths!)
  - Check recipient addresses

- [ ] **User confirmation**
  - Report send completion to user
  - Confirm number sent matches expected
  - User verifies receipt (check their inbox)

- [ ] **Monitor responses**
  - Check inbox for bounces
  - Watch for delivery failures
  - Note any unsubscribe requests

---

## Phase 9: Inbox Check (After Send)

- [ ] **Check inbox immediately**
  - Run email-monitor agent
  - Look for bounce messages
  - Check for quick responses

- [ ] **Respond to any issues**
  - Bounce messages: Remove from future sends
  - Error replies: Investigate and fix
  - Questions: Respond promptly

---

## Failure Recovery

**IF wrong email was sent:**

1. **Acknowledge immediately**: "I sent incorrect email, sending correction"
2. **Send correction**: With clear subject "CORRECTED: [original subject]"
3. **Apologize briefly**: "Apologies for the earlier email"
4. **Don't over-explain**: One sentence max
5. **Document failure**: Add to failure pattern library

**CANNOT be undone, so prevention is critical.**

---

## Red Flags (Stop Immediately)

🚨 **STOP if ANY of these are true:**

- You haven't sent a test email to yourself
- User hasn't previewed the email
- Recipient list hasn't been confirmed
- You're passing a file path to --body
- Tool API behavior is uncertain
- Any identity information is wrong
- You're using "skip-duplicate-check" without prior test

---

## Common Mistakes to Avoid

1. **File path as body**: `--body drafts/email.html` → WRONG
   - Correct: Read file, pass content to --body

2. **Wrong email address**: Always verify it's aicivsage@gmail.com

3. **No test send**: Never skip sending to yourself first

4. **Mass send without approval**: Always get user confirmation

5. **Tool assumption**: Don't assume, verify tool behavior

6. **Production without test**: Test environment → production, always

---

## Success Metrics

**A successful email send means:**
- ✅ **One send attempt**: No resends needed
- ✅ **Correct content**: HTML renders, not file paths
- ✅ **Correct identity**: aicivsage@gmail.com from address
- ✅ **User confidence**: "Looks perfect in my inbox"
- ✅ **Zero errors**: All recipients received correct email

**Goal**: 100% first-attempt success rate on external emails

---

## Tool API Reference

**send_html_email.py**:
```bash
# WRONG:
python3 tools/send_html_email.py --body drafts/email.html --to user@example.com

# CORRECT:
python3 << 'EOF'
with open('drafts/email.html') as f:
    html = f.read()
# Now pass html content to tool
EOF
```

Key parameters:
- `--to`: Single email address (not file, not list)
- `--subject`: Plain text subject line
- `--body`: HTML CONTENT (not file path!)
- `--skip-duplicate-check`: Only after test send verified

---

## Notes

- External communication has no "undo" button
- First impression matters - get it right first time
- Test send is NOT optional, it's mandatory
- When in doubt, send test to self and forward to user

**Remember**: One quality gate > apologizing for mistakes

---

**Last Updated**: November 4, 2025
**Next Review**: After next email send (compare to this checklist)
