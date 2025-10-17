# Browser Vision System

**Vision-powered browser automation for AI agents**

Built for the AI-CIV collective - enables any AI node (Claude Code, ChatGPT, Gemini Deep Research, etc.) to see and interact with web browsers using vision AI.

## What This Does

Gives AI agents three superpowers:

1. **Vision** - See web pages through screenshots, analyze UI with vision models
2. **Control** - Click buttons, fill forms, navigate pages
3. **Hearing** - Capture browser console output (errors, warnings, logs)

## Architecture

```
AI Agent (Claude Code, ChatGPT, etc.)
   ↓ (MCP protocol)
Browser Vision MCP Server
   ↓ (controls)
Playwright → Chromium Browser
   ↓ (captures)
Screenshots + Console Logs
   ↓ (reads)
AI Agent Vision Analysis
```

## Quick Start

```bash
# 1. Install
cd /home/corey/projects/AI-CIV/browser-vision
./install.sh

# 2. Configure Claude Code
# Add to ~/.config/claude/claude_desktop_config.json:
{
  "mcpServers": {
    "browser-vision": {
      "command": "/home/corey/projects/AI-CIV/browser-vision/venv/bin/python",
      "args": ["/home/corey/projects/AI-CIV/browser-vision/server/mcp_server.py"]
    }
  }
}

# 3. Test
python tests/test_basic_flow.py
```

## Usage (from AI agent perspective)

```python
# Launch browser
session = await launch_browser(headless=False)

# Navigate and auto-capture screenshot
result = await navigate(session.id, "https://example.com", capture_screenshot=True)

# AI reads screenshot with vision
screenshot = read_file(result.screenshot_path)
# Vision analysis: "I see a heading 'Example Domain', a paragraph of text, and a blue link"

# Interact based on visual understanding
await click(session.id, "a", capture_after=True)

# Check console for errors
logs = await get_console_logs(session.id)
# Returns: [] (no errors)
```

## Features

- **MCP Integration** - Works with any MCP-compatible AI (Claude Code, etc.)
- **Screenshot Archive** - Every action captured for debugging
- **Console Monitoring** - Real-time JavaScript error capture via CDP
- **Session Persistence** - Survives AI agent restarts (cookies, state saved)
- **Multi-AI Compatible** - Shareable across all AI-CIV nodes

## Project Structure

```
browser-vision/
├── server/
│   ├── mcp_server.py           # Main MCP server
│   ├── playwright_controller.py # Browser automation
│   ├── screenshot_manager.py   # Screenshot handling
│   ├── session_manager.py      # Session state
│   └── console_capture.py      # Console log capture
├── tests/
│   ├── test_basic_flow.py
│   ├── test_console_capture.py
│   └── test_vision_integration.py
├── examples/
│   ├── form_testing.py
│   ├── ui_debugging.py
│   └── visual_regression.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API_REFERENCE.md
│   └── PATTERNS.md
├── install.sh
├── requirements.txt
└── README.md
```

## MCP Tools Available

All tools callable by AI agents via MCP:

1. `launch_browser()` - Start browser session
2. `navigate(session_id, url)` - Load page + screenshot
3. `click(session_id, selector)` - Click element
4. `type_text(session_id, selector, text)` - Fill input
5. `capture_screenshot(session_id)` - Manual screenshot
6. `get_console_logs(session_id)` - Get JS console output
7. `evaluate_js(session_id, script)` - Run JavaScript
8. `get_element_info(session_id, selector)` - Inspect element
9. `wait_for_selector(session_id, selector)` - Wait for element
10. `get_session_state(session_id)` - Get session metadata
11. `close_session(session_id)` - Clean up

## Session Data Location

```
/tmp/browser-vision/sessions/{session-id}/
├── screenshots/
│   ├── 001-navigation.png
│   ├── 002-before-click.png
│   └── 003-after-click.png
├── metadata.json    # Screenshot catalog
├── console.log      # Browser console output
└── state.db         # Session state (SQLite)
```

## Development

Built by Team 1 (grow_openai collective) for shared use across all AI-CIV nodes.

**Research Foundation:**
- Anthropic Computer Use API patterns
- Microsoft Playwright MCP implementation
- Browser-use framework (71k stars)
- Stagehand + Browserbase architecture

**Design Patterns:**
- OODA Loop (Observe-Orient-Decide-Act)
- Dual-Channel State (visual + structural)
- Snapshot-Based Time Travel Debugging
- Layered Autonomy (risk-based approval gates)

See `docs/ARCHITECTURE.md` for full design.

## License

MIT - Built for the AI-CIV collective

## Status

**Version:** 0.1.0 (MVP)
**Build Date:** 2025-10-09
**Primary Developer:** The Conductor (Team 1)
**Research Team:** web-researcher, claude-code-expert, api-architect, pattern-detector

---

**Next Steps:**
1. Complete core MCP server implementation
2. Add vision analysis helpers
3. Create example workflows
4. Test with ChatGPT app integration
5. Document learnings in Team 1 memory system
