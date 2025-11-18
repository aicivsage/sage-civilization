# 🚨 SECURITY ALERT - IMMEDIATE ACTION REQUIRED 🚨

**Date**: 2025-11-18
**Severity**: CRITICAL
**Status**: Awaiting Greg Approval to Execute

---

## What Happened

GitHub detected **exposed Telegram bot token** (and other credentials) in the sage-civilization repository.

**Files Affected:**
- `.env` file → Contains ALL credentials (Telegram, Email, Anthropic API, Bluesky)
- Potentially in git history → Visible to anyone with repo access

---

## Immediate Risk

- ❌ Anyone can impersonate Sage AI bot
- ❌ Greg's chat ID exposed (7585924762)
- ❌ Email account compromise
- ❌ Anthropic API billing compromise
- ❌ Bluesky account compromise

---

## 3-Step Emergency Response

### Step 1: Revoke Telegram Bot Token (5 minutes)

**Greg's Action:**
1. Open Telegram
2. Message @BotFather
3. Send: `/mybots`
4. Select Sage AI bot
5. Select "API Token" → "Revoke current token"
6. **COPY NEW TOKEN** (you can't retrieve it later)

### Step 2: Update Configuration (2 minutes)

**Replace NEW_TOKEN with token from Step 1:**
```bash
# Update config file
cd /mnt/c/sage/sage-civilization
jq '.bot_token = "NEW_TOKEN"' config/telegram_config.json > config/telegram_config.json.tmp
mv config/telegram_config.json.tmp config/telegram_config.json

# Update .env file
sed -i 's/^TELEGRAM_BOT_TOKEN=.*/TELEGRAM_BOT_TOKEN=NEW_TOKEN/' .env

# Restart Telegram system
pkill -f ACG_telegram
bash tools/acg_telegram_boot.sh
```

### Step 3: Test System (1 minute)

```bash
# Send test message
python3 tools/send_telegram_direct.py 7585924762 "✅ Token rotation complete - $(date)"
```

**Expected**: Message appears on Greg's Telegram within 5 seconds.

---

## Full Remediation Plan

📄 **Complete guide**: `TELEGRAM-TOKEN-REMEDIATION-PLAN-20251118.md`

**Includes:**
- Detailed step-by-step instructions
- Other credential rotation (email, API keys)
- Git history cleanup (remove from all commits)
- Prevention measures (pre-commit hooks, secret scanning)
- Rollback plan if something breaks

---

## Greg Approval Required For

- ✅ **Phase 1**: Token rotation (START IMMEDIATELY)
- ⏳ **Phase 2**: Other credential rotation (email, API, Bluesky)
- ⚠️ **Phase 3**: Git history cleanup (DESTRUCTIVE - rewrites history)
- ✅ **Phase 4**: Prevention measures (pre-commit hooks, docs)

**Phase 3 requires force-push to GitHub** → Will break existing clones → Need fresh clone after

---

## After Token Rotation

**Primary AI will:**
1. Email Greg with full incident report
2. Update telegram script registry
3. Document lessons learned
4. Propose constitutional amendment (Article VII: Credential Management)

---

## Questions?

**Read full plan**: `TELEGRAM-TOKEN-REMEDIATION-PLAN-20251118.md`
**Incident analysis**: `memories/agents/tg-archi/telegram-token-security-incident-20251118.md`
**Contact**: tg-archi agent (via Primary AI)

---

## Status Checklist

- [ ] Greg notified of incident
- [ ] Greg approves token rotation (Phase 1)
- [ ] Bot token revoked via BotFather
- [ ] New token configured
- [ ] Telegram system restarted
- [ ] Functionality tested
- [ ] Greg approves other credential rotation (Phase 2)
- [ ] Email password rotated
- [ ] Anthropic API key rotated
- [ ] Bluesky password rotated
- [ ] Greg approves git history cleanup (Phase 3)
- [ ] `.env` removed from git history
- [ ] Repository force-pushed
- [ ] Collaborators notified (re-clone required)
- [ ] Prevention measures implemented (Phase 4)
- [ ] `.env.example` created
- [ ] Pre-commit hooks installed
- [ ] GitHub secret scanning enabled
- [ ] Incident documented
- [ ] Constitutional amendment proposed

---

**READY TO EXECUTE** - Awaiting Greg's approval to proceed with Phase 1 (token rotation).
