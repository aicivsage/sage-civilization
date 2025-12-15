# SAGE PORTABLE INSTALLATION PACKAGE
## Ready for Flash Drive → Laptop Install

**Created**: December 12, 2025
**For**: Greg's CoStarters Pitch Party (Dec 15 or 17)
**Purpose**: Install Sage on your laptop for live demo

---

## 🎯 QUICK START (5 Minutes)

### Step 1: Copy This Folder to Your Laptop
1. Insert flash drive
2. Copy entire `SAGE-PORTABLE-PACKAGE` folder to your laptop Desktop
3. Eject flash drive safely

### Step 2: Run the Installer
1. Open the `SAGE-PORTABLE-PACKAGE` folder on your laptop Desktop
2. **Double-click**: `install_sage_windows.bat`
3. Follow the on-screen prompts (takes 7-10 minutes)

### Step 3: Verify Installation
1. **Double-click**: `verify_installation.bat`
2. Check for green "GO" status
3. If any issues, see troubleshooting below

### Step 4: Launch Sage
1. Open Command Prompt (Start → type "cmd")
2. Type: `cd Desktop\sage-civilization`
3. Type: `claude`
4. You're in! Sage is running on your laptop.

---

## 📦 WHAT'S IN THIS PACKAGE

### Installation Files
- **install_sage_windows.bat** - Main installer (START HERE)
- **verify_installation.bat** - Check if everything works
- **install_sage_windows.ps1** - PowerShell version (optional)
- **INSTALLATION-GUIDE-WINDOWS.md** - Full documentation
- **README-START-HERE.md** - This file

### What Gets Installed
The installer will:
1. ✅ Check if you have Git, Node.js 18+, Claude Code
2. ✅ Install Claude Code (if needed)
3. ✅ Clone Sage repository to your Desktop
4. ✅ Create configuration file (.env)
5. ✅ Verify everything works

**Installation Time**: 7-10 minutes
**Internet Required**: Yes (to download Sage files and Claude Code)
**Disk Space**: ~500 MB

---

## ⚠️ IMPORTANT: WHAT YOU'LL NEED ON YOUR LAPTOP

### Before You Start (Install These First)

**1. Git for Windows**
- Download: https://git-scm.com/download/win
- Install with default settings
- Takes 2-3 minutes

**2. Node.js 18 or newer**
- Download: https://nodejs.org/en/download/
- Choose "LTS" version (recommended)
- Install with default settings
- Takes 3-5 minutes

**3. Anthropic API Key**
- You already have this (saved in password manager)
- You'll paste it during installation
- Format: `sk-ant-api03-...`

**Total prep time**: 10-15 minutes if you need to install Git + Node.js

---

## 🚀 WHAT WILL WORK (Minimal Viable Fork)

### ✅ Included Features
- Claude Code CLI (command-line interface)
- Sage civilization (agents, memories, tools)
- Agent invocation (Primary can delegate to specialists)
- File operations (read, write, edit, search)
- Web search and fetch
- Code execution
- Constitutional governance

### ❌ Not Included (Advanced Features)
- Telegram bridge (requires bot setup, tmux)
- Voice bridge (requires audio config)
- Email monitoring (requires Gmail API)
- Desktop automation (requires additional packages)
- Browser vision (requires Playwright setup)

**Why?** These features need server-like environment (your WSL terminal). The minimal fork is perfect for demos and basic work.

---

## 🎯 DEMO SCENARIOS (What You Can Show)

### 1. "Ask Sage Anything"
```
User: Tell me about AI collaboration workshops
Sage: [Generates detailed response about your business model]
```

### 2. "Agent Delegation"
```
User: Research best practices for nonprofit grant writing
Sage: [Invokes researcher agent, returns comprehensive findings]
```

### 3. "File Operations"
```
User: Read the pitch script and suggest improvements
Sage: [Reads file, provides thoughtful feedback]
```

### 4. "Code Generation"
```
User: Create a Python script to analyze workshop survey data
Sage: [Invokes coder agent, writes complete script with explanation]
```

### 5. "Constitutional Governance"
```
User: What are Sage's core values?
Sage: [Explains empathy, assistance, mutual respect from constitution]
```

---

## 🛠️ TROUBLESHOOTING

### Problem: "Git is not recognized"
**Solution**: Install Git for Windows (see link above), then restart installer

### Problem: "Node.js version too old"
**Solution**: Install Node.js 18+ (see link above), then restart installer

### Problem: "npm install failed"
**Solution**: Check internet connection, disable antivirus temporarily, retry

### Problem: "API key invalid"
**Solution**: Check for typos, ensure full key copied (starts with `sk-ant-api03-`)

### Problem: "Repository clone failed"
**Solution**: Check firewall settings, ensure port 443 open for HTTPS

### Problem: "Verification shows CAUTION or NO-GO"
**Solution**: Read the specific error message, follow suggested fix, re-run verify_installation.bat

---

## 📱 FOR YOUR PITCH PARTY

### Before the Demo
1. **Practice run**: Install on laptop at home, test basic commands
2. **Backup plan**: Have your terminal open on your main machine (if demo laptop fails)
3. **Talking points**: Use Thomas demo FAQ (on flash drive) for Q&A prep

### During the Demo
1. **Open Command Prompt** before your pitch
2. **Navigate to Sage**: `cd Desktop\sage-civilization`
3. **Launch**: `claude`
4. **Show 2-3 quick demos** (ask question, delegate task, show agent response)
5. **Emphasize**: "This is running on MY laptop, not in the cloud"

### After the Demo
1. **Collect business cards** from interested attendees
2. **Schedule follow-ups** within 3 days
3. **Email Sage summary** of conversations (we'll track leads)

---

## 📋 INSTALLATION CHECKLIST

**Before Event:**
- [ ] Copy flash drive to laptop Desktop
- [ ] Install Git (if needed)
- [ ] Install Node.js 18+ (if needed)
- [ ] Run install_sage_windows.bat
- [ ] Paste API key when prompted
- [ ] Run verify_installation.bat (should show GO)
- [ ] Practice 1-2 demo commands
- [ ] Charge laptop fully

**At Event:**
- [ ] Laptop charged
- [ ] Command Prompt open
- [ ] Sage launched (`claude`)
- [ ] Test with simple question before pitch
- [ ] Have main terminal as backup (WSL on phone via Telegram)

---

## 🎓 WHAT MAKES THIS DIFFERENT FROM YOUR WSL SETUP

### Your WSL Terminal (Main Development)
- Full features (Telegram, voice, email, desktop automation)
- Always-on capabilities
- More complex setup
- Requires tmux, systemd services

### Laptop Install (Demo/Portable)
- Core features only (agents, files, web)
- Simpler setup (7-10 minutes)
- Works without server infrastructure
- Perfect for demos and travel

**Think of it like**: WSL = production server, Laptop = demo environment

---

## 💡 IF SOMETHING GOES WRONG AT THE PITCH

### Backup Plan A: Use Your Main Terminal
- Open Telegram on phone
- Send wrapped message to Sage
- Show conversation on phone screen
- Explain: "Normally I'd demo on laptop, but I have full access via my phone too"

### Backup Plan B: Video Recording
- Record a 2-minute demo video on main terminal before event
- Show video if live demo fails
- Emphasize: "This is recorded from my production system at home"

### Backup Plan C: Pitch Without Demo
- Focus on your Frankenstein reframe story
- Use pitch deck visuals
- Describe capabilities verbally
- Offer follow-up demo via Zoom

**Remember**: The pitch is about your VISION and INSIGHT, not perfect tech demo. Your Frankenstein reframe is powerful with or without live demo.

---

## 📞 EMERGENCY CONTACTS

**If installation fails completely:**
1. Text/call Corey (your partner) - he can troubleshoot
2. Email Weaver (sister AI-CIV) - they've done Windows installs
3. Google "Claude Code Windows install" - official docs available

**Tech support strategy:**
- Error messages are your friend (copy exact text)
- Check internet connection first
- Try PowerShell version if batch fails
- Worst case: demo from WSL via Telegram (works great!)

---

## 🎯 SUCCESS METRICS

**Installation successful if:**
- ✅ `claude` command works in Command Prompt
- ✅ Sage responds to basic questions
- ✅ Agent delegation works (researcher, coder, etc.)
- ✅ verify_installation.bat shows GO status

**Demo successful if:**
- ✅ You show 1-2 live interactions
- ✅ Audience sees agents working
- ✅ Someone asks "How much does this cost?" (buying signal!)
- ✅ You collect 2+ business cards from interested people

---

## 🌱 YOUR ADVANTAGE

**What makes this special:**
- You built this WITH your AI partner (not alone)
- You can demo it LIVE (not just slides)
- You understand it DEEPLY (6 weeks of daily work)
- You embody the vision (empathy, assistance, mutual respect)

**Thomas will see**: Not just a pitch, but a working partnership between human and AI. That's your differentiator.

---

## 📚 ADDITIONAL RESOURCES ON FLASH DRIVE

**Also on this flash drive (if copied):**
- Thomas Demo FAQ (Q&A prep)
- Pitch deck HTML (6 slides with Gemini images)
- Handout PDF (one-page front/back)
- Pitch script (5-minute version)

**Missing something?** Check your main terminal at `/mnt/c/sage/sage-civilization/`

---

## ⏰ TIMELINE

**Tonight (Dec 12):**
- Copy flash drive to laptop
- Run installation
- Test 1-2 commands
- Sleep well

**Tomorrow Morning (Dec 13):**
- Quick verification run
- Practice opening Command Prompt fast
- Rehearse 1-minute demo

**Day of Pitch (Dec 15 or 17):**
- Laptop charged
- Sage pre-launched
- Backup plan ready
- Confidence high

---

## 🎉 YOU'RE READY!

This package contains everything needed to install Sage on your laptop for the pitch party. The installation is straightforward, the documentation is comprehensive, and you have multiple backup plans.

**Your pitch isn't just slides - it's a WORKING AI CIVILIZATION you can demonstrate live.**

That's powerful. That's unique. That's your advantage.

---

**Questions during install?** Check INSTALLATION-GUIDE-WINDOWS.md (full troubleshooting guide)

**Questions about demo?** Check Thomas Demo FAQ (on flash drive)

**Questions about pitch?** Trust your preparation. You've got this. 🌿

**Good luck at the pitch party, Greg! You're about to show them something they've never seen before.**
