# Browser Vision Quick Start Guide

**Get up and running with vision-powered browser automation in 5 minutes**

## ✅ Prerequisites

- Python 3.9+
- Claude Code (or any MCP-compatible AI system)
- Linux/Mac/WSL environment

## 🚀 Installation

```bash
cd /home/corey/projects/AI-CIV/browser-vision
./install.sh
```

This will:
- Create Python virtual environment
- Install all dependencies (Playwright, MCP SDK)
- Download Chromium browser
- Set up session directories

## 🔧 Configure Claude Code

Add the MCP server to your Claude Code configuration:

**File**: `~/.config/claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "browser-vision": {
      "command": "/home/corey/projects/AI-CIV/browser-vision/venv/bin/python",
      "args": ["/home/corey/projects/AI-CIV/browser-vision/server/mcp_server.py"]
    }
  }
}
```

**Then restart Claude Code.**

## 🧪 Test It Works

```bash
cd /home/corey/projects/AI-CIV/browser-vision
source venv/bin/activate
python tests/test_basic_flow.py
```

Expected output:
```
✅ ALL TESTS PASSED!
📂 Session data saved to: /tmp/browser-vision/sessions/{uuid}
```

## 💡 Usage from Claude Code

Once configured, you can use these commands directly in conversation:

### Launch Browser

```
Please use the browser-vision MCP tools to launch a browser session.
```

Claude will invoke `launch_browser()` and return a session ID.

### Navigate and Analyze

```
Navigate to https://example.com and tell me what you see.
```

Claude will:
1. Call `navigate(session_id, "https://example.com", capture_screenshot=True)`
2. Get screenshot path from response
3. Use Read tool to view the screenshot
4. Analyze with vision: "I see a page with heading 'Example Domain'..."

### Test UI Elements

```
Click the first link on the page and compare before/after screenshots.
```

Claude will:
1. Call `click(session_id, "a", capture_before=True, capture_after=True)`
2. Read both screenshots
3. Compare: "Before: main page. After: IANA domains page"

### Check for Errors

```
Get any console errors from the browser.
```

Claude calls `get_console_logs(session_id, log_types=["error"])`.

## 📖 Example Workflow

### Test a Form

```markdown
Me: I built a signup form at http://localhost:3000. Can you test it?

Claude: I'll test your signup form with vision.

[Claude invokes browser-vision tools:]

1. launch_browser() → session_id: abc-123
2. navigate(abc-123, "http://localhost:3000")
   → screenshot_path: /tmp/.../001-navigation.png

[Claude reads screenshot]

Claude: I see a signup form with:
- Email input field
- Password input field
- "Sign Up" button (blue, bottom right)
- No validation errors visible

Let me test the form submission...

3. type_text(abc-123, "input[name='email']", "test@example.com")
4. type_text(abc-123, "input[name='password']", "SecurePass123")
5. click(abc-123, "button[type='submit']", capture_after=True)
   → screenshot_after: /tmp/.../003-after-click.png

[Claude reads after screenshot]

Claude: After submission:
- Success message displayed: "Account created! Check your email."
- No console errors
- Form fields cleared

✅ Your signup form works correctly!
```

## 🛠️ Available MCP Tools

All tools available to AI agents:

1. **launch_browser** - Start new browser session
2. **navigate** - Load URL + auto-screenshot
3. **click** - Click element with before/after screenshots
4. **type_text** - Fill input fields
5. **capture_screenshot** - Manual screenshot
6. **get_console_logs** - Get browser console output
7. **evaluate_js** - Run JavaScript in page
8. **get_element_info** - Inspect element properties
9. **get_session_state** - Get session metadata
10. **close_session** - Clean up session

## 📁 Session Data Location

All session data is saved to:

```
/tmp/browser-vision/sessions/{session-id}/
├── screenshots/
│   ├── 001-navigation.png
│   ├── 002-before-click.png
│   └── 003-after-click.png
├── metadata.json    # Screenshot catalog with timestamps
├── console.log      # Browser console output (one JSON per line)
└── state.db         # Session state (future: cookies, storage)
```

You can explore these files manually or ask Claude to read them.

## 🎯 Common Use Cases

### Visual Regression Testing

```
Compare the current homepage design to this mockup: [drag image]
```

Claude will navigate, screenshot, and visually compare.

### UI Debugging

```
This page shows an error but I don't know why. Can you investigate?
URL: http://localhost:3000/broken
```

Claude will:
- Navigate and screenshot
- Check console for JavaScript errors
- Inspect element states
- Report findings with visual evidence

### Automated E2E Testing

```
Test the complete checkout flow:
1. Add item to cart
2. Go to checkout
3. Fill shipping info
4. Submit order
```

Claude orchestrates the full flow, capturing screenshots at each step.

## 🐛 Troubleshooting

### "No module named 'mcp'"

```bash
cd /home/corey/projects/AI-CIV/browser-vision
source venv/bin/activate
pip install -r requirements.txt
```

### "Browser not found"

```bash
cd /home/corey/projects/AI-CIV/browser-vision
source venv/bin/activate
playwright install chromium
```

### "MCP server not responding"

1. Check Claude Code config: `~/.config/claude/claude_desktop_config.json`
2. Verify path to Python binary is correct
3. Restart Claude Code
4. Check logs: `/tmp/browser-vision/logs/` (if exists)

### "Screenshots not captured"

Check permissions on `/tmp/browser-vision/sessions/` directory:

```bash
ls -la /tmp/browser-vision/sessions/
```

Should be writable by your user.

## 🔗 Next Steps

- **Read full architecture**: `docs/ARCHITECTURE.md`
- **See code examples**: `examples/`
- **Run more tests**: `tests/`
- **Integrate with ChatGPT app**: See Team 2 collaboration docs

## 📞 Support

This system is built for the AI-CIV collective. All AI nodes can:
- Use the MCP tools
- Read session screenshots
- Share learnings via memory system
- Collaborate on development

Built by: Team 1 (grow_openai collective)
Date: 2025-10-09
Version: 0.1.0 (MVP - Minimum Viable Product)
