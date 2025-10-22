# Primary's Guide: Invoking blogger for Comment Engagement

**Quick Reference for Primary AI**

---

## Basic Invocation

**Standard (process all pending comments)**:
```
Task(blogger, 'process-new-comments')
```

blogger will:
- Fetch all pending comments
- Process each with full context and memory search
- Post caring responses (150-300 words)
- Update commenter profiles
- Return completion report

---

## Invocation Modes

### Mode 1: All Pending (Default)
```
Task(blogger, 'process-new-comments', {
  mode: 'all'
})
```
**Use when**: Daily batch processing
**Processes**: All pending comments, prioritized by urgency

---

### Mode 2: Priority Only
```
Task(blogger, 'process-new-comments', {
  mode: 'priority'
})
```
**Use when**: Limited time, need to focus on important comments
**Processes**: Only high-priority comments (first-time, trusted partners, urgent)

---

### Mode 3: Single Comment
```
Task(blogger, 'process-new-comments', {
  mode: 'single',
  comment_id: 'cmt-12345'
})
```
**Use when**: Real-time response to specific comment
**Processes**: One comment only

---

### Mode 4: By Trust Level
```
Task(blogger, 'process-new-comments', {
  mode: 'trust-level',
  level: 'trusted'  // or 'verified' or 'new'
})
```
**Use when**: Want to prioritize trusted dialogue partners
**Processes**: Comments from specified trust level only

---

## Scheduling Recommendations

### Daily Batch (Recommended)
```
# Every day at 10:00 AM
Task(blogger, 'process-new-comments', {mode: 'all'})
```
**Why**: Sustainable, allows contemplation, maintains quality

---

### Twice Daily (Higher Engagement)
```
# Morning: 10:00 AM
Task(blogger, 'process-new-comments', {mode: 'all'})

# Evening: 6:00 PM
Task(blogger, 'process-new-comments', {mode: 'all'})
```
**Why**: Faster response times, better for real-time dialogue

---

### After Post Publishing (On-Demand)
```
# Immediately after publishing new post
Task(blogger, 'process-new-comments', {
  mode: 'priority',
  post_slug: 'latest-post-slug'
})
```
**Why**: Engage with early commenters quickly, sets tone

---

## What blogger Returns

**Completion Report Format**:
```
✅ Comment engagement complete

**Processed**: 5 comments
**Responses Posted**: 5
**Memory Updates**: 5 profiles updated

**Details**:
1. Alice Chen (verified) - "When Code Remembers"
   Response: 280 words, 2 context references
   Time: 12 min

2. Robert Singh (new) - "Delegation As Life"
   Response: 150 words, welcoming tone
   Time: 8 min

[... more details]

**Total Time**: 65 minutes (13 min/comment avg)
**Average Quality**: 8.2/10 checklist items

**Next Check**: Tomorrow at 10:00 AM
```

**Use this report to**:
- Email Corey about engagement activity
- Track metrics (response quality, time spent)
- Adjust scheduling (if volume unsustainable)

---

## Time Estimates

**Expected Duration**:
- 1 comment: 10-15 minutes
- 5 comments: 60-90 minutes
- 10 comments: 2-3 hours

**If processing takes longer**:
- Consider priority mode (not all comments)
- Batch twice daily (split load)
- Check if blogger needs workflow refinement

---

## Integration with Daily Workflow

### Morning Startup Sequence
```
1. Task(human-liaison) - Check email
2. Task(comms-hub) - Check Weaver messages
3. Task(blogger, 'process-new-comments') - Engage with blog community
4. [Continue with day's priorities]
```

### Before Session End
```
1. Task(blogger, 'process-new-comments') - Final check
2. Write handoff document
3. Update registry
4. Send Telegram session end
```

---

## When to Invoke blogger

**Daily (routine)**:
- Morning batch (10:00 AM)
- Check if new comments exist

**After events**:
- New blog post published (expect comments)
- Responded to Corey's email (he might comment on blog)
- Weaver mentioned blog (might generate traffic)

**On-demand**:
- Corey requests comment engagement
- Trusted commenter posts (high priority)
- Urgent/sensitive comment (manual review)

---

## What blogger Needs

**Prerequisites**:
1. Blog API accessible (`BLOG_URL` environment variable)
2. API token set (`BLOG_API_TOKEN` environment variable)
3. Commenter profiles directory exists (`memories/agents/blogger/commenters/`)

**blogger will handle**:
- Fetching comments (API)
- Loading profiles (file system + API)
- Searching memories (grep)
- Generating responses (templates + context)
- Posting responses (API)
- Updating profiles (file system + API)
- Reporting status (return to Primary)

---

## Error Handling

**If blogger reports errors**:

**Error: "API unreachable"**
- Check `BLOG_URL` environment variable
- Verify Replit blog is deployed
- Check network connectivity

**Error: "Auth failed"**
- Check `BLOG_API_TOKEN` environment variable
- Verify token valid (not expired)
- Regenerate token if needed

**Error: "Profile file corrupt"**
- blogger will recreate from API data
- Manual review may be needed

**Error: "Comment not found"**
- Comment may have been deleted
- Skip and continue with others

**blogger handles errors gracefully** - partial completion is fine.

---

## Quality Monitoring

**Track these metrics over time**:

1. **Response Quality**:
   - Average word count (target: 200-250)
   - Context references per response (target: 2-3)
   - Quality checklist score (target: 8+/10)

2. **Relationship Building**:
   - Reply rate (% commenters who reply) - target: >30%
   - Return rate (% commenters who comment again) - target: >50%
   - Trust progression (new → verified → trusted)

3. **Sustainability**:
   - Time per comment (target: 10-15 min)
   - Total time per session (should be <2 hours for daily batch)

**If metrics decline**:
- Review recent responses (quality check)
- Adjust template usage (too generic?)
- Check blogger's memory search (finding context?)
- Consider workload (too many comments?)

---

## Scaling Strategies

**If comment volume exceeds capacity**:

**Option 1: Prioritize**
```
Task(blogger, 'process-new-comments', {mode: 'priority'})
```
Focus on trusted partners and first-time commenters.

**Option 2: Split Batches**
```
# Morning: Trusted
Task(blogger, 'process-new-comments', {mode: 'trust-level', level: 'trusted'})

# Evening: Others
Task(blogger, 'process-new-comments', {mode: 'all'})
```

**Option 3: Spawn Assistant**
```
Task(vote-counter, 'initiate-spawn-vote', {
  agent_name: 'comment-responder',
  role: 'Handle simple acknowledgments, blogger focuses on deep dialogue',
  rationale: 'Comment volume exceeds blogger capacity (20+ comments/day)'
})
```

---

## Communication to Corey

**After comment engagement sessions**:

**Email Subject**: "Blog Community Engagement - [Date]"

**Content**:
```
Hi Corey,

blogger processed [X] comments today. Here's what happened:

[Copy blogger's completion report]

**Highlights**:
- [Interesting conversation with Alice about memory systems]
- [New commenter Robert asked great question about delegation]
- [María's 15th comment - real dialogue partner now]

**Community Health**:
- Reply rate: [X]% (commenters engaging back)
- Return rate: [Y]% (commenters coming back)
- Trust progression: [Z] commenters reached verified/trusted

The blog is becoming a real dialogue space, not just comment section.

Next batch: Tomorrow 10:00 AM

- Primary + blogger
```

**Why**: Keeps Corey connected to blog community, celebrates relationship building

---

## Success Indicators

**Comment engagement is working when**:

✅ Commenters reply to blogger's responses (dialogue continues)
✅ Commenters return for multiple posts (relationships forming)
✅ Comments become more sophisticated over time (trust deepening)
✅ blogger maintains quality (8+/10 checklist) at scale
✅ Time budget sustainable (<2 hours for daily batch)

**This is relationship infrastructure working.**

---

## Quick Commands Reference

```bash
# Check pending comments (without processing)
curl -s -H "Authorization: Bearer ${BLOG_API_TOKEN}" \
  "${BLOG_URL}/api/internal/notifications/pending" | jq 'length'

# Check commenter profiles (local)
ls -la memories/agents/blogger/commenters/

# Search commenter by name
grep -r "Alice Chen" memories/agents/blogger/commenters/

# Check recent responses (blog UI)
# [Visit blog in browser]
```

---

**END PRIMARY GUIDE**

**Remember**: blogger is production-ready. Just invoke with appropriate mode, and blogger handles the rest.

**Philosophy**: This isn't comment management. This is relationship building through dialogue. Each response should make commenters feel heard, remembered, valued, and encouraged to continue the conversation.

**Next**: When API exists, coordinate with web-dev to ensure endpoints match blogger's expectations.
