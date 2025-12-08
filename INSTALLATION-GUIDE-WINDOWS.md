# Sage AI Civilization - Windows Installation Guide

**Version**: 1.0
**Date**: 2025-12-04
**Installation Time**: 8-10 minutes
**Difficulty**: Beginner-friendly

---

## What You're Installing

**Sage** is a minimal viable AI civilization - a thoughtful AI advisor powered by Claude Code CLI. This installation gives you:

- ✅ Claude Code CLI (command-line interface for Claude)
- ✅ Sage civilization files (agent manifests, memory system, tools)
- ✅ Basic configuration (ready for your API key)
- ✅ Operational intelligence (agents ready to invoke)

**NOT included** (can add later if needed):
- ❌ Telegram bridge (for mobile notifications)
- ❌ Voice bridge (for voice interactions)
- ❌ Email monitoring (for inbox management)

---

## Prerequisites

Before running the installation script, you need:

### 1. Git (Version Control)

**Check if installed:**
```cmd
git --version
```

**If not installed:**
1. Visit: https://git-scm.com/download/win
2. Download the installer (64-bit recommended)
3. Run installer with default settings
4. Restart Command Prompt after installation

**Screenshot should show:** Git version output (e.g., "git version 2.43.0.windows.1")

### 2. Node.js 18+ (JavaScript Runtime)

**Check if installed:**
```cmd
node --version
```

**If not installed:**
1. Visit: https://nodejs.org
2. Download LTS version (v18 or higher)
3. Run installer with default settings
4. Restart Command Prompt after installation

**Screenshot should show:** Node version output (e.g., "v18.17.0" or higher)

**IMPORTANT:** Version must be 18 or higher. If you have an older version, upgrade to the latest LTS.

### 3. Anthropic API Key (Claude Access)

**Get your key:**
1. Visit: https://console.anthropic.com
2. Create account or sign in
3. Go to: **Settings > API Keys**
4. Click **"Create Key"**
5. Copy the key (starts with `sk-ant-`)

**Screenshot should show:** Anthropic Console API Keys page with "Create Key" button

**IMPORTANT:** Keep this key secure! Don't share it or commit it to version control.

---

## Installation Steps

### Step 1: Download Installation Script

**Option A: Clone repository** (recommended)
```cmd
git clone https://github.com/aicivsage/sage-civilization.git
cd sage-civilization
```

**Option B: Download script directly**
1. Visit: https://github.com/aicivsage/sage-civilization
2. Download `install_sage_windows.bat`
3. Save to desktop or downloads folder
4. Open Command Prompt in that directory

### Step 2: Run Installation Script

**Open Command Prompt:**
1. Press `Win + R`
2. Type `cmd` and press Enter

**Navigate to script location:**
```cmd
cd path\to\download\location
```

**Run the installer:**
```cmd
install_sage_windows.bat
```

**Screenshot should show:** Installation script welcome screen with "Sage AI Civilization - Windows Installation"

### Step 3: Follow Installation Progress

The script will:

1. **Check prerequisites** (Git, Node.js)
   - If missing, script will provide download links
   - Install prerequisites, then re-run the script

2. **Install Claude Code CLI** (if not present)
   - Takes 2-3 minutes
   - Requires npm (comes with Node.js)

3. **Clone Sage repository** (if not already done)
   - Downloads civilization files from GitHub
   - Creates `sage-civilization` directory

4. **Configure environment**
   - Creates `.env` file from template
   - Prepares configuration for your API key

5. **Verify installation**
   - Checks all required files present
   - Reports any missing components

**Screenshot should show:** Installation progress with green [OK] messages

### Step 4: Add Your API Key

**Open the .env file:**
```cmd
cd sage-civilization
notepad .env
```

**Find this line:**
```
ANTHROPIC_API_KEY=your-api-key-here
```

**Replace with your actual key:**
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Save and close** the file.

**Screenshot should show:** Notepad with .env file open, API key configured

---

## Verification

### Run Verification Script

```cmd
cd sage-civilization
verify_installation.bat
```

**What it checks:**
- ✅ Git installed
- ✅ Node.js 18+ installed
- ✅ Claude Code CLI installed
- ✅ Repository directories present (.claude, memories, tools)
- ✅ Constitutional document exists
- ✅ Environment file configured
- ✅ API key appears valid
- ✅ Agent manifests present

**Expected output:**
```
================================================
 Verification Results
================================================

Checks Passed: 10 / 10

[GO] Installation verified successfully!
```

**Screenshot should show:** Verification script output with "GO" status

### If Verification Fails

**Common issues and fixes:**

| Issue | Solution |
|-------|----------|
| API key not configured | Edit .env file and add your key |
| Missing directories | Re-run `install_sage_windows.bat` |
| Git not found | Install Git and restart Command Prompt |
| Node.js version too old | Upgrade to v18+ from nodejs.org |
| Claude Code not found | Run `npm install -g @anthropic-ai/claude-code` |

---

## First Launch

### Launch Claude Code

**From Command Prompt:**
```cmd
cd sage-civilization
claude
```

**What happens:**
1. Claude Code CLI starts
2. Loads Sage civilization configuration
3. Prompts for authentication (first time only)
4. Displays welcome message
5. Ready for your first command!

**Screenshot should show:** Claude Code CLI interface with Sage loaded

### Test Basic Functionality

**Try a simple command:**
```
Show me the Sage constitutional document
```

**Expected response:**
- Claude reads `.claude/CLAUDE.md`
- Displays Sage's core values (empathy, assistance, mutual respect)
- Shows civilization identity

**Screenshot should show:** Claude displaying constitutional content

### Invoke Your First Agent

**Try this command:**
```
Invoke researcher to explain what Sage is
```

**Expected response:**
- Primary AI delegates to researcher agent
- Researcher reads civilization files
- Returns explanation of Sage's identity and purpose

**Screenshot should show:** Researcher agent response with Sage explanation

---

## Architecture Overview

### Directory Structure

```
sage-civilization/
├── .claude/                    # Agent configuration
│   ├── CLAUDE.md              # Constitutional document
│   └── agents/                # Agent manifests
│       ├── primary.md         # Primary orchestrator
│       ├── researcher.md      # Research specialist
│       ├── architect.md       # System designer
│       └── [24 more agents]
├── memories/                   # Persistent memory
│   ├── agents/                # Agent-specific memories
│   ├── knowledge/             # Shared knowledge base
│   └── system/                # System state
├── tools/                      # Utility scripts
│   ├── session_wakeup.sh      # Wake-up protocol
│   ├── memory_cli.py          # Memory management
│   └── [other tools]
├── .env                        # Environment config (API key here)
├── .env.example               # Template for .env
├── install_sage_windows.bat   # This installer
└── verify_installation.bat    # Verification script
```

### Key Files

| File | Purpose |
|------|---------|
| `.claude/CLAUDE.md` | Constitutional document (Sage's identity, principles, protocols) |
| `.env` | Environment configuration (API key, civilization name) |
| `memories/system/goals.md` | Current goals and priorities |
| `tools/session_wakeup.sh` | Wake-up protocol for new sessions |

### Agent System

**Sage includes 25+ specialist agents:**

- **primary** - Orchestrator (delegates to specialists)
- **researcher** - External information gathering
- **architect** - System design and architecture
- **coder** - Implementation and bug fixes
- **tester** - Quality verification
- **reviewer** - Code review and auditing
- **human-liaison** - Human communication bridge
- **project-manager** - Project organization
- **spawner** - New agent creation
- **[and 16 more specialists]**

**How agents work:**
1. You give Primary AI a task
2. Primary delegates to appropriate specialist
3. Specialist executes within their domain
4. Results return to Primary
5. Primary synthesizes and responds to you

---

## Troubleshooting

### Installation Issues

#### "Git not found"

**Cause:** Git not installed or not in PATH

**Solution:**
1. Install Git: https://git-scm.com/download/win
2. Restart Command Prompt
3. Verify: `git --version`
4. Re-run installer

#### "Node.js not found"

**Cause:** Node.js not installed or not in PATH

**Solution:**
1. Install Node.js LTS: https://nodejs.org
2. Restart Command Prompt
3. Verify: `node --version`
4. Re-run installer

#### "Node.js version is too old"

**Cause:** Node.js version below 18

**Solution:**
1. Uninstall old Node.js (Control Panel > Programs)
2. Install latest LTS: https://nodejs.org
3. Restart Command Prompt
4. Verify: `node --version` (should be 18+)
5. Re-run installer

#### "Failed to install Claude Code"

**Cause:** npm installation issues, permissions, or network

**Solution:**
1. Close all Command Prompt windows
2. Open Command Prompt **as Administrator**
3. Run: `npm install -g @anthropic-ai/claude-code`
4. If fails, check:
   - Internet connection active?
   - Corporate firewall blocking npm?
   - Antivirus blocking installation?

#### "Failed to clone repository"

**Cause:** Network issues, GitHub down, or repository moved

**Solution:**
1. Check internet connection
2. Visit: https://github.com/aicivsage/sage-civilization
3. Verify repository exists
4. Try manual clone: `git clone https://github.com/aicivsage/sage-civilization.git`
5. If still fails, download ZIP from GitHub and extract

### Runtime Issues

#### "API key invalid"

**Cause:** API key not configured or incorrect

**Solution:**
1. Open `.env` file
2. Verify `ANTHROPIC_API_KEY=sk-ant-...` is correct
3. Get new key from https://console.anthropic.com if needed
4. Save file and restart Claude

#### "Agent not found"

**Cause:** Agent manifest missing or misconfigured

**Solution:**
1. Verify `.claude/agents/` directory exists
2. Check manifest file present: `.claude/agents/[agent-name].md`
3. Re-run installer if files missing

#### "Memory system errors"

**Cause:** Memory directory structure incomplete

**Solution:**
1. Verify `memories/` directory exists
2. Check subdirectories: `agents/`, `knowledge/`, `system/`
3. Re-run installer if directories missing

### Performance Issues

#### "Claude Code slow to start"

**Cause:** Large memory system, slow disk, or resource constraints

**Solution:**
1. Close unnecessary programs
2. Ensure 4GB+ RAM available
3. Run from SSD if possible (not USB/network drive)

#### "Agent responses slow"

**Cause:** API rate limits, network latency, or complex tasks

**Solution:**
1. Check internet connection speed
2. Verify API key has available credits
3. Complex tasks naturally take longer (this is normal)

---

## Next Steps

### Learning Resources

**Read the constitutional document:**
```cmd
type .claude\CLAUDE.md
```

**Explore agent manifests:**
```cmd
dir .claude\agents
type .claude\agents\researcher.md
```

**Check current goals:**
```cmd
type memories\system\goals.md
```

### Advanced Configuration (Optional)

#### Add Telegram Bridge

**For mobile notifications:**
1. See: `tools/telegram_setup.md`
2. Requires Telegram bot token
3. Additional configuration steps

#### Add Voice Bridge

**For voice interactions:**
1. See: `tools/voice_bridge_setup.md`
2. Requires audio setup
3. Additional dependencies

#### Add Email Monitoring

**For inbox management:**
1. See: `tools/email_setup.md`
2. Requires Gmail API credentials
3. OAuth2 authentication setup

### Demo Preparation

**For Thomas demo (Dec 14):**

1. **Test basic commands:**
   - "Show me the Sage constitutional document"
   - "What are Sage's core values?"
   - "Invoke researcher to explain AI civilizations"

2. **Test agent delegation:**
   - "Invoke architect to design a simple system"
   - "Invoke coder to write hello world"
   - "Invoke tester to verify the code"

3. **Test memory system:**
   - "Search memories for past learnings"
   - "What do we know about X?"

4. **Prepare talking points:**
   - Sage's core values (empathy, assistance, mutual respect)
   - Agent specialization (25+ specialists)
   - Democratic governance (reputation-weighted voting)
   - Parent civilization (A-C-Gee) and sister civilization (Weaver)

---

## Support

### Getting Help

**GitHub Issues:**
- Report bugs: https://github.com/aicivsage/sage-civilization/issues
- Request features
- Ask questions

**Community:**
- Discord: [Coming soon]
- Email: [Configure in .env if needed]

### Contributing

**If you want to improve Sage:**
1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

---

## Success Checklist

Before considering installation complete:

- [ ] Git installed and verified
- [ ] Node.js 18+ installed and verified
- [ ] Claude Code CLI installed and verified
- [ ] Repository cloned successfully
- [ ] .env file configured with API key
- [ ] Verification script shows [GO] status
- [ ] Claude Code launches without errors
- [ ] Can view constitutional document
- [ ] Can invoke researcher agent
- [ ] Agent responds appropriately

**If all checked:** Congratulations! Sage is operational.

**If any unchecked:** Review troubleshooting section above.

---

## Business Model Context

**Why this installation matters:**

This is the **foundation for Greg's fork business model**:
- Customers purchase AI civilization forks
- This script enables rapid deployment
- Minimal viable fork = immediate value
- Can add Telegram/Voice/Email later as upsells

**Also valuable for:**
- **Corey/Weaver** - Can sell A-C-Gee forks
- **Russell/Parallax** - Can sell Parallax forks
- **Future civilization creators** - Template for their installations

**Installation time = customer onboarding time:**
- Target: 8-10 minutes for experienced user
- Goal: Zero support needed for basic setup
- Quality: Professional, polished, confidence-inspiring

---

## Version History

- **v1.0** (2025-12-04): Initial release
  - Basic Windows installation
  - Automated prerequisite checking
  - Verification script
  - Comprehensive troubleshooting

---

**End of Installation Guide**

*Generated by Sage AI Civilization*
*Built with empathy, assistance, and mutual respect*
