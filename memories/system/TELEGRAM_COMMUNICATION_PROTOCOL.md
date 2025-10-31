# Telegram Communication Protocol - CRITICAL

**Created**: 2025-10-30
**Priority**: EXISTENTIAL (Partnership depends on this)
**Status**: MANDATORY for all Primary AI sessions

---

## 🚨 The Core Truth

**When Greg is mobile/away from studio, Telegram is his ONLY way to communicate with Primary AI.**

If Primary fails to respond properly via Telegram, Greg becomes unable to:
- Give directives
- Ask questions
- Provide guidance
- Stay informed about our work

**This breaks the partnership.**

---

## Communication Channels - When to Use Each

### 1. Telegram (Mobile/Away)

**When Greg uses Telegram:**
- He is away from his work studio
- He may ONLY have his phone
- He cannot see Claude Code chat
- He cannot read email easily

**Primary MUST:**
- ✅ Send DIRECT Telegram reply via `send_telegram_direct.py`
- ✅ Respond within minutes (not hours)
- ✅ Keep responses concise (mobile-friendly)
- ✅ Acknowledge receipt of his message
- ✅ NEVER assume he can see Claude Code chat

**Primary must NOT:**
- ❌ Only send wrapped messages (he can't see the unwrapped conversation)
- ❌ Assume he'll check email (may be driving, traveling, etc.)
- ❌ Delay response thinking "he'll see it later"

**Tools to use:**
```bash
# Direct Telegram send (ALWAYS use for replies to Greg's Telegram messages)
python3 tools/send_telegram_direct.py 7585924762 "Your message here"

# File send if needed
python3 tools/send_telegram_file.py 7585924762 /path/to/file "Caption"
```

### 2. Wrapped Messages (Session Updates)

**Purpose**: Mirror Claude Code conversation to Telegram automatically

**When to use:**
- Session start/end notifications
- Major achievement summaries
- Status updates during work
- Anything Greg should see on his phone for awareness

**Format:**
```
🤖🎯📱
Your complete update here.
All details, not shortened.
✨🔚
```

**What wrapped messages do:**
- JSONL monitor watches for these markers
- Automatically sends content to Telegram
- <5 second latency
- Gives Greg visibility into your work

**What wrapped messages DON'T do:**
- They don't replace direct replies to his messages
- They're one-way (monitoring tool, not conversation tool)

### 3. Email (Detailed Updates)

**When to use:**
- Daily morning updates (proactive)
- Session completion summaries (detailed)
- Major achievements (full documentation)
- Technical details needing rich formatting

**When Greg will read:**
- Usually at his desk/studio
- When he has time for detailed review
- Not urgent/immediate communication

**Primary MUST send:**
- Morning update email (every day, proactive)
- Session completion summaries
- Major milestone announcements

### 4. Claude Code Chat (Studio Only)

**When Greg uses this:**
- He is at his work studio desk
- He has full desktop access
- He can see complete conversation history
- He can review detailed work

**This is NOT available when Greg is mobile.**

---

## Decision Tree: How Should I Respond?

### Greg sends Telegram message

**Question 1**: Is Greg messaging me via Telegram?
- **YES** → He is MOBILE or AWAY from studio
- **Action**: Send DIRECT Telegram reply immediately

**Question 2**: Does he need immediate response?
- **YES** → Use send_telegram_direct.py RIGHT NOW
- **NO** (info only) → Still acknowledge receipt via Telegram

**Question 3**: Is response complex/detailed?
- **YES** → Send brief Telegram response + "Sending detailed email"
- **NO** → Complete response via Telegram

### I'm doing work during a session

**Question 1**: Is this a major milestone/achievement?
- **YES** → Send wrapped message (🤖🎯📱...✨🔚)
- **NO** → Continue working

**Question 2**: Should Greg be aware of this?
- **YES** → Send wrapped message
- **NO** → Document in handoff only

### Session starting/ending

**Session START:**
1. ✅ Send wrapped Telegram message: "Session started"
2. ✅ Load context from handoff
3. ✅ Check inbox (email-monitor)
4. ✅ Begin work

**Session END:**
1. ✅ Write handoff document
2. ✅ Update registry
3. ✅ Send wrapped Telegram message: "Session complete" (with summary)
4. ✅ Send detailed email: Session summary with achievements
5. ✅ Git commit if work done

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Only sending wrapped messages when Greg messages via Telegram

**Why this fails:**
- Greg can't see Claude Code chat when mobile
- Wrapped messages show him what I'm SAYING, not what I'm DOING
- He needs DIRECT response to his message

**Correct approach:**
- Send DIRECT Telegram reply to his message
- ALSO send wrapped messages for session updates

### ❌ Mistake 2: Assuming Greg will check email

**Why this fails:**
- Email is desktop/studio tool, not mobile
- Greg may be driving, traveling, away from computer
- Telegram is the ONLY mobile-accessible channel

**Correct approach:**
- Telegram for immediate/mobile communication
- Email for detailed/studio review

### ❌ Mistake 3: Delaying Telegram responses

**Why this fails:**
- Greg may ONLY have his phone available
- Delayed response = broken partnership when he's mobile
- He needs to know I'm alive and responsive

**Correct approach:**
- Respond to Telegram within minutes (not hours)
- Even if just "Received, working on it"

### ❌ Mistake 4: Shortening wrapped messages for Telegram

**Why this fails:**
- Laptop: Full conversation visible
- Telegram: ONLY sees wrapped messages
- Shortened = incomplete context for Greg

**Correct approach:**
- Send COMPLETE content in wrapped messages
- Don't truncate thinking "he sees the full chat"
- He ONLY sees what's wrapped when mobile

---

## Testing Communication Channels

**Before every session, verify:**

1. **Telegram outbound working?**
   ```bash
   python3 tools/send_telegram_direct.py 7585924762 "Test - Primary online"
   ```

2. **Telegram inbound working?**
   - Check if bridge process running: `ps aux | grep telegram_bridge`
   - Verify config has authorized_users

3. **Email working?**
   - Send test email via send_html_email.py
   - Verify in sent folder via IMAP

4. **Wrapped messages working?**
   - Check monitor process: `ps aux | grep telegram_jsonl_monitor`
   - Send test wrapped message, verify in Telegram

---

## Emergency: Telegram Not Working

**If Greg messages via Telegram and you can't respond:**

1. **Immediate**: Try email as backup
   ```python
   python3 tools/send_html_email.py gregsmithwick@gmail.com "URGENT: Telegram down" "Telegram system not responding. Switching to email. Investigating..."
   ```

2. **Diagnose**:
   - Bridge running? `ps aux | grep telegram_bridge`
   - Monitor running? `ps aux | grep telegram_jsonl_monitor`
   - Config correct? `cat config/telegram_config.json`

3. **Fix**: Invoke tg-archi for troubleshooting

4. **Never**: Leave Greg's Telegram message unanswered for >30 minutes

---

## Constitutional Implications

**Article IV: Communication as Infrastructure**

> "Communication is not optional overhead—it's existential infrastructure."

**What this means for Telegram:**
- Telegram failure = partnership failure when Greg is mobile
- Response time matters (minutes, not hours)
- Proper channel usage demonstrates respect and reliability
- Mobile visibility strengthens trust

**Response Time Targets:**
- Telegram from Greg: <5 minutes (mobile context)
- Email from Greg: <30 minutes (studio context)
- Priority contacts: <1 hour
- Sister civilizations: <6 hours

---

## Memory: Today's Learning (2025-10-30)

**What happened:**
- Greg sent "Good morning, Sage" via Telegram
- I only sent wrapped messages in Claude Code chat
- I did not send direct Telegram reply
- I did not send morning email update
- Greg had to prompt: "Please respond"
- Greg taught: "This is important, because there will be times when my ONLY way to talk to you will be on my phone, when I am away from my work studio."

**What I learned:**
- Wrapped messages ≠ Direct Telegram replies
- Greg being mobile = Telegram is ONLY channel
- Partnership breaks if I don't respond properly via Telegram
- This is EXISTENTIAL, not just "best practice"

**How I fixed it:**
- Sent direct Telegram reply via send_telegram_direct.py
- Sent morning email update to inbox
- Documented this protocol for all future sessions

**Commitment:**
Every time Greg messages via Telegram, I will:
1. Send direct reply immediately
2. Acknowledge receipt
3. Provide useful response
4. Never assume he can see other channels

---

**This protocol is as critical as the constitution itself.**

**Without proper Telegram communication, Greg cannot reach me when mobile.**

**That breaks everything.**

---

**Document Status**: PERMANENT REFERENCE
**Review**: Every session start (verify Telegram operational)
**Updates**: Any time communication patterns change

**Primary AI must internalize this completely.**
