# Computer Use for Autonomous Minetest Play

**Date**: 2025-10-16
**Context**: Research how A-C-Gee can autonomously control and play Minetest

## Answer: YES - 85% Confidence

## RECOMMENDED: MCP Desktop Automation

**Best tool**: `mcp-desktop-automation` (RobotJS-based)
- Mouse control (move, click)
- Keyboard control (press, type)
- Screenshots
- **Production-ready TODAY**

## Setup Steps

### 1. Install MCP Desktop Automation
```bash
npm install -g mcp-desktop-automation
```

### 2. Configure Claude Code
Edit `~/.claude.json`:
```json
{
  "mcpServers": {
    "desktop-automation": {
      "command": "npx",
      "args": ["-y", "mcp-desktop-automation"]
    }
  }
}
```

**✅ COMPLETED**: Configuration added to `/home/corey/projects/AI-CIV/grow_gemini_deepresearch` project on 2025-10-16

### 3. Restart Claude Code
**⚠️ REQUIRED**: User must restart Claude Code for MCP tools to load.

After restart, MCP tools become available:
- `mouse_move`
- `mouse_click`
- `keyboard_type`
- `screen_capture`

## WSL2 Limitation

**Problem**: WSL2 Linux processes cannot control Windows GUI apps directly

**Solutions**:
1. **Run Minetest in WSL2 with WSLg** (recommended)
   - `sudo apt-get install minetest`
   - Display renders on Windows via WSLg
   - MCP can control it from WSL2

2. **Windows PowerShell bridge**
   - Run automation tools on Windows side
   - Invoke via `powershell.exe -Command "..."`

3. **Use mcp-windows-desktop-automation**
   - AutoIt-based, native Windows automation
   - Best for game automation

## Autonomous Gameplay Loop

```
1. screen_capture → get screenshot
2. Vision analysis → "What do I see?"
3. Decision → "What should I do?"
4. mouse_move/click or keyboard_type → execute action
5. Wait → observe result
6. Repeat
```

## Sources
- Claude Computer Use: https://docs.claude.com/en/docs/build-with-claude/computer-use
- MCP Desktop Automation: https://github.com/tanob/mcp-desktop-automation
- Claude Code MCP: https://docs.claude.com/en/docs/claude-code/mcp

**Status**: Ready to implement - estimated 2-4 hours for proof of concept
