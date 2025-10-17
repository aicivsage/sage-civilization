# Example: Testing a Web Form with Vision

**Real-world workflow showing browser vision in action**

## Scenario

You've built a login form and want to test it visually. Instead of manually clicking through, you ask Claude Code to test it using vision.

## The Conversation

```markdown
You: I built a login form. Can you test it and tell me if anything looks broken?
     URL: http://localhost:8000/login
```

## What Happens (Behind the Scenes)

### Step 1: Claude Invokes launch_browser

```python
# MCP tool call
launch_browser(headless=False, viewport_width=1440, viewport_height=900)

# Returns:
{
  "session_id": "abc-123-xyz",
  "screenshot_dir": "/tmp/browser-vision/sessions/abc-123-xyz/screenshots",
  "status": "ready"
}
```

### Step 2: Claude Navigates and Captures

```python
# MCP tool call
navigate(
    session_id="abc-123-xyz",
    url="http://localhost:8000/login",
    capture_screenshot=True
)

# Returns:
{
  "url": "http://localhost:8000/login",
  "title": "Login - My App",
  "screenshot_path": "/tmp/.../001-navigation.png",
  "console_errors": []
}
```

### Step 3: Claude Uses Read Tool (Vision Analysis)

```python
# Claude Code Read tool
read_file("/tmp/browser-vision/sessions/abc-123-xyz/screenshots/001-navigation.png")
```

**Claude's Vision Analysis**:
> "I can see a login form with:
> - 'Email' input field (empty)
> - 'Password' input field (empty)
> - 'Login' button (blue, centered)
> - 'Forgot password?' link below
>
> ⚠️  Issue detected: The password field is not using type='password' -
> I can see it's a regular text input because there's no password masking dots.
>
> Let me test the form to see if there are other issues..."

### Step 4: Claude Tests Invalid Input

```python
# Fill with invalid email
type_text(
    session_id="abc-123-xyz",
    selector="input[name='email']",
    text="not-an-email"
)

# Click submit
click(
    session_id="abc-123-xyz",
    selector="button[type='submit']",
    capture_before=True,
    capture_after=True
)

# Returns:
{
  "screenshot_before": "/tmp/.../002-before-click.png",
  "screenshot_after": "/tmp/.../003-after-click.png"
}
```

**Claude reads both screenshots and compares**:

> "Before click: Form filled with 'not-an-email'
> After click: Error message appears 'Please enter a valid email address'
>
> ✅ Email validation works correctly."

### Step 5: Claude Tests Valid Login

```python
# Clear and fill with valid data
type_text(
    session_id="abc-123-xyz",
    selector="input[name='email']",
    text="test@example.com"
)

type_text(
    session_id="abc-123-xyz",
    selector="input[name='password']",
    text="TestPassword123"
)

# Submit
click(
    session_id="abc-123-xyz",
    selector="button[type='submit']",
    capture_after=True
)
```

**Vision analysis**:

> "After submission:
> - Page redirected to /dashboard
> - Welcome message: 'Welcome, test@example.com'
> - No error messages
>
> ✅ Login flow works correctly."

### Step 6: Claude Checks Console

```python
get_console_logs(
    session_id="abc-123-xyz",
    log_types=["error", "warning"]
)

# Returns:
{
  "logs": [
    {
      "type": "warning",
      "text": "Password field should use type='password'",
      "timestamp": "2025-10-09T15:20:00Z"
    }
  ],
  "error_count": 0,
  "warning_count": 1
}
```

### Step 7: Claude Closes Session

```python
close_session(session_id="abc-123-xyz", archive=True)
```

## Claude's Final Report

```markdown
## Login Form Test Results

### ✅ Working Correctly
1. Email validation - correctly rejects invalid emails
2. Login flow - successfully authenticates and redirects
3. Error messages - clear and visible

### ⚠️  Issues Found
1. **Security Issue**: Password input field is not using type='password'
   - Current: Plain text visible while typing
   - Should be: Masked with dots/asterisks

2. **Console Warning**: Browser warning about password field type

### 📸 Visual Evidence
I've captured 5 screenshots showing:
- Initial form state
- Invalid email error
- Valid login success
- Dashboard after login
- Complete flow

All screenshots saved to: /tmp/browser-vision/sessions/abc-123-xyz/

### 🔧 Recommended Fix
```html
<!-- Change this -->
<input name="password" type="text" />

<!-- To this -->
<input name="password" type="password" />
```
```

## The Power of Vision

**Without vision** (traditional automation):
- Need to write selector-based assertions
- Hard to verify visual appearance
- Can't see layout issues
- Brittle if HTML changes

**With vision** (this system):
- AI actually "sees" the page like a human
- Notices visual bugs (misaligned buttons, wrong colors)
- Resilient to DOM changes
- Natural language test descriptions

## Try It Yourself

1. **Start a local server**:
   ```bash
   python -m http.server 8000
   ```

2. **Ask Claude Code**:
   ```
   Test the page at http://localhost:8000 and tell me what you see.
   ```

3. **Claude will**:
   - Launch browser
   - Navigate and screenshot
   - Analyze with vision
   - Report findings

4. **You can ask follow-up**:
   ```
   Click the first button and tell me what happens.
   ```

5. **Claude continues testing**:
   - Captures before/after screenshots
   - Compares visual changes
   - Reports results

## Session Data

After the test, you can explore the data:

```bash
# View screenshots
ls /tmp/browser-vision/sessions/abc-123-xyz/screenshots/

# Read metadata
cat /tmp/browser-vision/sessions/abc-123-xyz/metadata.json

# Check console logs
cat /tmp/browser-vision/sessions/abc-123-xyz/console.log
```

## Advanced: Multi-Page Workflows

```markdown
You: Test the complete signup → verify email → login flow.
     Start at http://localhost:8000/signup
```

Claude will:
1. Navigate to signup
2. Fill form + screenshot
3. Submit + screenshot
4. Check for success message (vision)
5. Navigate to email verification page
6. Fill verification code + screenshot
7. Submit + screenshot
8. Navigate to login
9. Test login + screenshot
10. Verify final dashboard state

All with visual verification at each step.

---

**Status**: ✅ Working in production
**Location**: `/home/corey/projects/AI-CIV/browser-vision`
**Built**: 2025-10-09
