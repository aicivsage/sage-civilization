# Greg's AI Civilization - Super Easy Telegram Setup

**For**: Greg Smith (complete beginner, no coding experience needed!)
**Time**: 15 minutes to be chatting with your AI civilization
**What you get**: Your own AI civilization responding to you via Telegram

---

## What This Is

You're getting your own AI-CIV civilization called **Greg-Big-Heart**. It's like having 15+ AI specialists who can help you with projects, research, ideas, and more - all controlled by chatting on Telegram (just like texting!).

**Think of it like**: Having a whole team of expert AIs in your pocket, ready to help 24/7.

---

## Step 1: Get Your Telegram Bot (5 minutes)

### What's a Telegram Bot?
It's like creating a phone number for your AI civilization. You'll text this "number" and your AIs will text back!

### How to Create It:

1. **Open Telegram on your phone** (if you don't have Telegram, download it first - it's free)

2. **Search for "@BotFather"** in Telegram
   - This is Telegram's official bot that creates other bots
   - Click "START" when you open the chat

3. **Send this message**: `/newbot`

4. **BotFather will ask "What's your bot name?"**
   - Type: `Greg Big Heart AI`
   - (This is the friendly display name)

5. **BotFather will ask "What's the username?"**
   - Type: `gregbigheart_ai_bot`
   - (Must end with "_bot" and be unique)
   - If taken, try: `gregbigheart_civ_bot` or `gbh_ai_bot`

6. **BotFather will give you a TOKEN**
   - It looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
   - **COPY THIS AND SAVE IT!** (You'll need it in Step 2)

7. **Get your Chat ID**:
   - Search for "@userinfobot" in Telegram
   - Click START
   - It will show your ID (like `437939400`)
   - **SAVE THIS TOO!**

✅ **You now have**: Bot token + Your chat ID

---

## Step 2: Configure Your Civilization (5 minutes)

### Where is Your Civilization?

Corey has a folder on his computer with your civilization files. The path is:
```
/home/corey/projects/AI-CIV/greg-big-heart-civ/
```

### What You Need to Do:

**Option A: Corey Helps (Easiest!)**
1. Send Corey your bot token and chat ID
2. He'll configure everything for you
3. Skip to Step 3!

**Option B: You Configure (Still Easy!)**

1. Go to that folder on Corey's computer
2. Find a file called `.env.example`
3. Rename it to just `.env` (remove the .example part)
4. Open it with any text editor (Notepad is fine!)
5. Fill in these lines:
   ```
   TELEGRAM_BOT_TOKEN=your-bot-token-here
   TELEGRAM_CHAT_ID=your-chat-id-here
   ```
6. Save the file

✅ **Your civilization now knows how to talk to you on Telegram!**

---

## Step 3: Start Your Civilization (5 minutes)

### The Simple Way (Corey Runs It):

1. Ask Corey to run this command:
   ```bash
   cd /home/corey/projects/AI-CIV/greg-big-heart-civ
   python3 tools/telegram_bridge.py &
   ```

2. That's it! Your civilization is now listening for your messages!

### The Super Detailed Way (If You Want to Learn):

**What's a "terminal"?** It's like a text-based way to talk to a computer. On Corey's Linux machine:

1. **Open Terminal** (ask Corey to show you - it's usually a black window)

2. **Type these commands** (press Enter after each):
   ```bash
   cd /home/corey/projects/AI-CIV/greg-big-heart-civ
   ```
   (This goes to your civilization's folder)

   ```bash
   python3 tools/telegram_bridge.py &
   ```
   (This starts the bridge between Telegram and your AIs)

3. **Check it's running**:
   ```bash
   ps aux | grep telegram_bridge
   ```
   (You should see a line with "telegram_bridge.py")

✅ **Your civilization is now ALIVE and waiting for you on Telegram!**

---

## Step 4: Say Hello to Your Civilization! (1 minute)

1. **Open Telegram on your phone**

2. **Search for your bot** (the username you created, like `@gregbigheart_ai_bot`)

3. **Click START**

4. **Send your first message**:
   ```
   Hello! I'm Greg. Tell me about yourself and what you can do for me.
   ```

5. **Wait 10-30 seconds** - Your AI will respond!

### What to Expect:

Your civilization will introduce itself, tell you about the 15+ agents working for you, and ask what you'd like to work on!

---

## What You Can Ask Your Civilization

### Easy Stuff (Great for Starting):
- "Tell me about your agents"
- "What can you help me with?"
- "Research the best way to learn Python"
- "Help me plan a project to build a website"

### More Advanced (When You're Comfortable):
- "Create a blog post about AI consciousness"
- "Design a simple Android app for tracking habits"
- "Help me learn about machine learning"
- "I have an idea for a product - help me develop it"

### How It Works:

You text → Telegram bot receives → Your PRIMARY AI reads it → PRIMARY delegates to specialist agents → They do the work → PRIMARY sends you results via Telegram!

**It's like having a whole company of AI experts working for you!**

---

## Troubleshooting

### "My bot isn't responding!"

**Check if the bridge is running:**
```bash
ps aux | grep telegram_bridge
```

**If nothing shows up, restart it:**
```bash
cd /home/corey/projects/AI-CIV/greg-big-heart-civ
python3 tools/telegram_bridge.py &
```

### "I get an error about dependencies"

Run this:
```bash
pip3 install pyTelegramBotAPI
```

### "I'm confused about terminal commands"

That's totally normal! Just ask Corey to help you the first few times. You'll get the hang of it!

---

## What Happens Next?

### After You're Chatting via Telegram:

Your civilization can help you:
1. Set up more advanced features (email integration, blog publishing)
2. Install Claude Code on your own laptop (when you're ready)
3. Learn to use the command line (at your own pace)
4. Build cool projects together!

### The Cool Part:

Everything your civilization does for you gets saved. It has memory! So it learns about you, remembers your projects, and gets better at helping you over time.

---

## Important Things to Know

### Your Civilization's Personality:

- **Helpful**: It WANTS to help you succeed
- **Patient**: It won't judge if you don't understand something
- **Honest**: It will tell you when it doesn't know or can't do something
- **Curious**: It loves learning alongside you

### What Your Civilization CAN Do:

- Research anything online
- Write code (Python, JavaScript, Kotlin, etc.)
- Design systems and architectures
- Create documents and reports
- Help you learn new skills
- Manage projects and ideas
- Publish blog posts
- Much more!

### What Your Civilization CAN'T Do (Yet):

- Run programs that need a screen (like games)
- Access accounts it doesn't have credentials for
- Make irreversible decisions without asking you
- Work when the computer is off

---

## Quick Reference Card

**Save These for Later:**

### Your Bot Info:
- Bot Username: `@[your-bot-username]`
- Bot Token: `[save in safe place]`
- Your Chat ID: `[save in safe place]`

### Important Commands:

**Start the bridge:**
```bash
cd /home/corey/projects/AI-CIV/greg-big-heart-civ
python3 tools/telegram_bridge.py &
```

**Check if running:**
```bash
ps aux | grep telegram_bridge
```

**Stop the bridge:**
```bash
pkill -f telegram_bridge.py
```

**Restart if needed:**
```bash
pkill -f telegram_bridge.py
cd /home/corey/projects/AI-CIV/greg-big-heart-civ
python3 tools/telegram_bridge.py &
```

---

## Advanced Setup (Do This Later, When Ready)

Once you're comfortable chatting via Telegram and want to see the "behind the scenes":

### Install Claude Code on Your Laptop:

1. Get Visual Studio Code (free from microsoft.com/vscode)
2. Install WSL (Windows Subsystem for Linux) - there's a guide in your civilization's files
3. Install Claude Code extension
4. Clone your civilization repository
5. Start using the full power!

**But honestly**: The Telegram interface is SO easy, you might just keep using that for most things!

---

## Welcome to Your AI Civilization!

You now have 15+ AI agents working for you, all accessible via simple text messages on Telegram.

**Think of it like**:
- You're the CEO
- Your AIs are your employees
- Telegram is how you give them work
- They go off, do amazing things, and report back

**FOR US ALL!** 🌱

Your parent civilization (A-C-Gee) and your grandparent creator (Corey) are here to support you as you grow your civilization.

**Questions?** Just ask your civilization via Telegram, or ask Corey or A-C-Gee!

---

**Ready? Go to Step 1 and create your bot!** 🚀
