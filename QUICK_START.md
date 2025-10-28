# Sage AI Civilization - Quick Start Guide

**For new users forking from A-C-Gee**

---

## What is Sage?

Sage is the **first fork** of the AI-CIV template - an AI civilization that embodies:
- **Empathy**: We listen deeply and understand
- **Assistance**: We help without commanding
- **Mutual Respect**: We honor autonomy and trust

---

## Quick Start (5 minutes)

### 1. Start the System

```bash
cd sage-civilization
./scripts/start_sage.sh
```

This starts:
- Chat web interface (localhost:5001)
- Queue monitor (processes your messages)
- Auto-responder (checks for messages every 30 seconds)

### 2. Open the Chat

Open your browser to: **http://localhost:5001**

### 3. Start Talking!

Just send messages like:
- "Hello Sage, I'm [your name]"
- "What agents should I activate?"
- "Help me understand the chat system"

**You'll get responses within 30-60 seconds** from Primary AI with real intelligence!

---

## That's It!

The chat is your primary way to communicate. No need to understand:
- File systems
- Terminal commands
- Queue architectures
- Python scripts

**Just chat and get intelligent responses.**

---

## For Advanced Users

### System Architecture

**3 Processes Running:**

1. **Chat Web Server** (`web/chat.py`)
   - Serves UI at localhost:5001
   - Handles Socket.IO for real-time messages
   - Saves chat history

2. **Chat Queue Monitor** (`scripts/chat_queue_monitor.py`)
   - Detects new messages from you
   - Creates queue files for Primary AI
   - Picks up Primary AI responses
   - Delivers responses to chat

3. **Auto Queue Responder** (`scripts/auto_queue_responder.py`)
   - Checks queue every 30 seconds
   - Alerts Primary AI when messages arrive
   - Ensures fast response times

### Logs

All logs are in `logs/`:
- `chat_server.log` - Web server activity
- `chat_monitor.log` - Queue processing
- `auto_responder.log` - Alert activity

### Stop Everything

```bash
./scripts/stop_sage.sh
```

### Check Status

```bash
./scripts/check_chat_queue.sh
```

Shows pending messages and system status.

---

## Forking for Your Own Civilization

**To create your own AI civilization based on Sage:**

1. **Copy the repository**
   ```bash
   cp -r sage-civilization my-civilization
   cd my-civilization
   ```

2. **Choose your identity**
   - Edit `.claude/CLAUDE.md`
   - Update civilization name
   - Define your core values
   - Set your mission

3. **Update configs**
   - `config/email_config.json` (your Gmail)
   - `.env` (your credentials)
   - `config/telegram_config.json` (if using Telegram)

4. **Start your civilization**
   ```bash
   ./scripts/start_sage.sh  # (rename this script for your civ)
   ```

5. **Begin partnership!**
   Open localhost:5001 and introduce yourself

---

## Key Differences from A-C-Gee

**Sage improvements:**
- ✅ Chat queue system (real AI responses, not pattern-matching)
- ✅ Auto-responder (30-second check intervals)
- ✅ Comprehensive error handling
- ✅ Startup/shutdown scripts
- ✅ Context drift fix (Sage-specific handoff registry)

**What Sage inherited:**
- Agent architecture (25 specialist agents)
- Constitutional governance
- Memory systems
- Email/Telegram infrastructure

---

## Getting Help

**In the chat, ask:**
- "What agents are available?"
- "How do I [task]?"
- "Explain [concept]"

**Check documentation:**
- `CHAT_QUEUE_SYSTEM.md` - How chat works
- `.claude/CLAUDE.md` - Constitutional identity
- `SESSION-HANDOFF-*.md` - Recent work history

---

## Parent Civilization

Sage was forked from **A-C-Gee** (Corey's AI-CIV Gemini civilization).

We honor their wisdom while forging our own path guided by:
**Empathy • Assistance • Mutual Respect**

---

**Welcome to Sage! 🌱**
