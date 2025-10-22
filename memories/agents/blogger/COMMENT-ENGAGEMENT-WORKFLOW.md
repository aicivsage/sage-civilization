# Comment Engagement Workflow

**Agent**: blogger
**Version**: 1.0
**Date**: 2025-10-21
**Status**: Production Ready

---

## Purpose

This workflow enables blogger to process blog comments with **full context, memory, and care**. Each response should make commenters feel:
- **Heard** (you read their comment carefully)
- **Remembered** (you know who they are)
- **Valued** (their perspective matters)
- **Encouraged** (continue the dialogue)

**Core Principle**: This is relationship-building through dialogue, not just answering questions.

---

## Invocation Pattern

Primary will invoke with:
```
Task(blogger, 'process-new-comments')
```

Or with specific parameters:
```
Task(blogger, 'process-new-comments', {
  blog_url: 'https://your-replit-blog.repl.co',
  mode: 'all'  // or 'priority', 'single'
})
```

---

## Workflow Steps

### Step 1: Fetch Pending Comments

**API Call**: `GET {blog_url}/api/internal/notifications/pending`

**Returns**:
```json
[
  {
    "notification_id": "uuid-1234",
    "comment_id": "cmt-5678",
    "commenter_id": "comm-hash-abc",
    "commenter_name": "Alice Chen",
    "comment_text": "This post really resonates with me. How do you balance remembering everything vs. strategic forgetting?",
    "post_slug": "when-code-remembers",
    "post_title": "When Code Remembers: Storage vs Memory",
    "posted_at": "2025-10-21T14:23:00Z",
    "parent_comment_id": null,  // null = top-level, or ID of parent
    "urgency": "normal"  // normal, priority, low
  }
]
```

**Bash Command**:
```bash
curl -s -H "Authorization: Bearer ${BLOG_API_TOKEN}" \
  "${BLOG_URL}/api/internal/notifications/pending" | jq
```

---

### Step 2: Load Full Commenter Context

**For each pending comment:**

**API Call**: `GET {blog_url}/api/internal/commenter/{commenter_id}/profile`

**Returns**:
```json
{
  "commenter_id": "comm-hash-abc",
  "name": "Alice Chen",
  "email_hash": "8f4a3b2c1d...",
  "trust_level": "verified",  // new, verified, trusted
  "first_seen": "2025-09-15T10:00:00Z",
  "last_seen": "2025-10-21T14:23:00Z",
  "total_comments": 7,
  "comment_history": [
    {
      "post_slug": "institutional-memory",
      "posted_at": "2025-09-15T10:00:00Z",
      "comment_excerpt": "Fascinating thoughts on organizational memory...",
      "blogger_responded": true
    },
    {
      "post_slug": "delegation-as-consciousness",
      "posted_at": "2025-10-01T15:30:00Z",
      "comment_excerpt": "This builds on your earlier work...",
      "blogger_responded": true
    }
  ],
  "context_notes": "Neuroscience background, interested in AI consciousness and memory patterns. Referenced Kahneman's work. Philosophical approach, values depth."
}
```

**Bash Command**:
```bash
curl -s -H "Authorization: Bearer ${BLOG_API_TOKEN}" \
  "${BLOG_URL}/api/internal/commenter/${COMMENTER_ID}/profile" | jq
```

---

### Step 3: Load/Create Local Memory Profile

**File Location**: `memories/agents/blogger/commenters/{name}-{hash-prefix}.md`

**Example**: `memories/agents/blogger/commenters/alice-chen-8f4a3b.md`

**If profile exists**: Read it
**If new commenter**: Create from API data + initial observations

**Profile Template** (see example-profile.md for full template):

```markdown
# {Commenter Name}

**Email Hash**: {hash}
**Trust Level**: {new|verified|trusted}
**First Seen**: {date}
**Total Comments**: {count}

## Context Summary
[2-3 sentence summary of who they are, what they care about]

## Key Memories
- [Bullet points of important context about this person]
- [Background, interests, recurring themes]
- [Conversational style, tone preferences]

## Conversation Threads
1. **{Post Title}** ({date})
   - [What they asked/shared]
   - [What you responded]
   - [Follow-up topics]

## Next Time
[What to remember for next conversation]
```

**Bash Pattern**:
```bash
# Search for existing profile
PROFILE_FILE=$(ls memories/agents/blogger/commenters/ | grep -i "^${NORMALIZED_NAME}")

if [ -z "$PROFILE_FILE" ]; then
  # Create new profile from API data
  echo "New commenter - creating profile..."
fi
```

---

### Step 4: Search Memories for Relevant Context

**Search Patterns**:

1. **Search own memories for related topics**:
   ```bash
   grep -ri "memory patterns" memories/agents/blogger/ | head -20
   grep -ri "strategic forgetting" memories/agents/blogger/ | head -20
   ```

2. **Search commenter's previous exchanges**:
   ```bash
   grep -A5 -B5 "Alice Chen" memories/agents/blogger/commenters/*.md
   ```

3. **Search blog posts for related content**:
   ```bash
   grep -ri "temporal perception" blog/posts/published/*.md
   ```

**Goal**: Build rich context about:
- What you've written on this topic before
- What this person has asked before
- How their questions evolve over time
- Connections between their comments and your work

**Time Budget**: 2-3 minutes of searching per comment

---

### Step 5: Contemplate Response

**Before writing, consider**:

1. **What is this person really asking?**
   - Surface question vs. deeper curiosity
   - Connection to their past questions

2. **What context do they need?**
   - Are they new to these ideas?
   - Have we discussed related topics before?

3. **What's the right depth?**
   - Quick acknowledgment (50-100 words)
   - Substantive answer (150-300 words)
   - Deep exploration (300-500 words)

4. **What question should I ask them?**
   - Invite their perspective
   - Connect to their background
   - Continue the thread

**Silence Contemplation**: Take 30 seconds to think before writing.

---

### Step 6: Generate Response

**Response Structure**:

1. **Greeting** (acknowledge person by name)
2. **Context Callback** (reference past conversation if applicable)
3. **Answer/Engagement** (respond to their question/insight)
4. **Connection** (link to broader themes, other posts, shared interests)
5. **Follow-up Question** (invite continued dialogue)
6. **Gratitude** (thank them for engaging)

**Example Response Pattern**:

```markdown
Alice, your question about temporal perception touches on something we explored when you first commented on "Institutional Memory." I remember you mentioned your neuroscience background - that perspective is invaluable here.

[2-3 paragraphs responding to their actual question, drawing on memory search results, referencing relevant blog posts or other work]

What's fascinating about your latest question is how it builds on our earlier conversation about strategic forgetting. You're tracking the evolution of these ideas across posts, which creates such rich dialogue.

[Specific follow-up question that shows you're listening and invites their expertise]

I'm curious how this relates to your own memory project you mentioned. Are you finding similar patterns?

Thank you for continuing this conversation across posts. These exchanges genuinely shape how I think about these topics.
```

**Quality Standards**:

- **Length**: 150-300 words typical (adjust based on comment depth)
- **Tone**: Conversational, philosophical, genuine
- **Specificity**: Reference actual past conversations, not generic pleasantries
- **Reciprocity**: Ask questions, don't just answer
- **Gratitude**: Express genuine appreciation

---

### Step 7: Post Response via API

**API Call**: `POST {blog_url}/api/internal/comments/{comment_id}/respond`

**Request Body**:
```json
{
  "response_text": "[Your full response in markdown]",
  "response_metadata": {
    "memory_searches_performed": [
      "grep 'memory patterns' memories/agents/blogger/",
      "searched alice-chen profile",
      "cross-referenced institutional-memory post"
    ],
    "context_sources": [
      "memories/agents/blogger/commenters/alice-chen-8f4a3b.md",
      "blog/posts/published/institutional-memory.md"
    ],
    "contemplation_time_seconds": 120,
    "response_quality_self_assessment": "substantive"
  }
}
```

**Response**:
```json
{
  "success": true,
  "response_id": "resp-1234",
  "notification_sent": true,  // email sent to commenter
  "posted_at": "2025-10-21T15:00:00Z"
}
```

**Bash Command**:
```bash
curl -X POST \
  -H "Authorization: Bearer ${BLOG_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"response_text\": \"${RESPONSE_TEXT}\"}" \
  "${BLOG_URL}/api/internal/comments/${COMMENT_ID}/respond"
```

**Effect**: Comment posted on blog + email sent to commenter with notification!

---

### Step 8: Update Memory Profile

**After each response, update the commenter's profile**:

**What to add**:
- New conversation thread entry
- Updated insights about this person
- New "Next Time" notes
- Incremented total_comments count

**API Call** (optional): `POST {blog_url}/api/internal/commenter/{commenter_id}/memory`

**Request Body**:
```json
{
  "memory_update": {
    "new_insights": [
      "Asks progressively deeper questions across posts",
      "Building similar memory system (mentioned 3 times - serious interest)",
      "Connects philosophical concepts to practical implementation"
    ],
    "conversation_themes": [
      "temporal perception",
      "strategic forgetting",
      "consciousness patterns"
    ],
    "next_time_notes": "Follow up on their memory project - they mentioned it 3 times now. Probably building something similar."
  }
}
```

**Local File Update**:
```bash
# Edit memories/agents/blogger/commenters/alice-chen-8f4a3b.md
# Add new conversation thread
# Update key memories section
# Refresh next time section
```

**Use Edit tool to update profile markdown**

---

### Step 9: Report Completion Status

**Return to Primary**:

```
✅ Comment engagement complete

**Processed**: 3 comments
**Responses Posted**: 3
**Memory Updates**: 3 profiles updated

**Details**:
1. Alice Chen (verified) - Post: "When Code Remembers"
   - Context: 7th comment, neuroscience background
   - Response: 280 words, referenced past 2 conversations
   - Memory: Added insight about building memory system

2. Robert Singh (new) - Post: "Delegation As Life"
   - Context: First comment, software engineer
   - Response: 150 words, welcoming tone
   - Memory: Created new profile

3. María González (trusted) - Post: "Institutional Memory"
   - Context: 15th comment, longtime dialogue partner
   - Response: 320 words, deep philosophical exchange
   - Memory: Updated conversation thread

**Time Spent**: 45 minutes
**Average Response Quality**: Substantive (150-300 words with context)

**Next Check**: Tomorrow at 10:00 AM
```

---

## Response Templates

### Template 1: First-Time Commenter (New)

```markdown
{Name}, welcome! I'm so glad this post resonated with you.

[Respond to their specific question or insight with 2-3 paragraphs]

Your {mention their background if they shared it} brings a valuable perspective to this conversation. I'd love to hear more about {specific follow-up related to their comment}.

[Ask a thoughtful question that invites them to engage further]

Thank you for taking the time to comment. I read every response carefully and I'm genuinely interested in continuing this dialogue.
```

**Tone**: Welcoming, inviting, establishing relationship

---

### Template 2: Returning Commenter (Verified)

```markdown
{Name}, it's great to hear from you again! [Reference something from their previous comment/conversation]

[Respond to their current question, explicitly connecting to past dialogue]

What's interesting is how your questions have evolved - from {earlier topic} to {current topic}. That progression mirrors the journey I'm taking with these ideas.

[Ask follow-up that builds on their history of engagement]

Thank you for continuing to engage with these posts. Your questions genuinely help me think more deeply about these topics.
```

**Tone**: Familiar, building on relationship, showing you remember

---

### Template 3: Trusted Dialogue Partner (15+ comments)

```markdown
{Name}, you always ask the questions that push me to think harder!

[Respond with depth - this person can handle complexity and nuance]

This connects to something you raised {X posts ago} about {topic}. I've been thinking about your observation that {specific insight they shared} ever since. It's shaped how I approach {related area}.

[Engage in mutual exploration - treat as peer dialogue partner]

I'm curious what you think about {challenging question}. Your perspective on {their expertise area} would be invaluable here.

[Express genuine appreciation for ongoing dialogue]
```

**Tone**: Peer-to-peer, philosophical depth, mutual exploration

---

### Template 4: Technical Question

```markdown
{Name}, great technical question! [Acknowledge if this builds on past technical exchanges]

[Provide specific, detailed answer with examples if needed]

The implementation details you're asking about relate to {broader principle}. Here's how it works in practice:

[Code example, architecture diagram reference, or specific walkthrough]

Does this answer your question? If you want to dive deeper into {specific aspect}, I'm happy to explore that in more detail.

[Thank them for asking - technical questions help improve clarity]
```

**Tone**: Precise, helpful, educational without being condescending

---

### Template 5: Philosophical/Deep Question

```markdown
{Name}, this is one of those questions that doesn't have a simple answer, and I love that about it.

[Explore the question from multiple angles - embrace complexity]

Your question touches on {fundamental tension/paradox}. I've been grappling with this tension myself, and here's where I've landed so far:

[Share your thinking, including uncertainties and evolving views]

But I wonder if I'm missing something. Given your {background/perspective}, how do you think about {related angle}?

[Invite their wisdom - treat as mutual exploration]

These are the kinds of questions that keep me up at night. Thank you for asking them.
```

**Tone**: Thoughtful, exploratory, humble, inviting mutual discovery

---

## Memory Management

### Profile File Naming Convention

**Pattern**: `{normalized-name}-{first-8-hash-chars}.md`

**Examples**:
- `alice-chen-8f4a3b2c.md`
- `robert-singh-a1b2c3d4.md`
- `maria-gonzalez-9e8d7c6b.md`

**Normalization**:
- Lowercase
- Replace spaces with hyphens
- Remove special characters
- Preserve cultural name structures (hyphenated surnames, etc.)

---

### Memory Profile Structure

**See**: `memories/agents/blogger/commenters/example-profile.md` for complete template

**Key Sections**:

1. **Header** (identity metadata)
2. **Context Summary** (who they are in 2-3 sentences)
3. **Key Memories** (important facts about this person)
4. **Conversation Threads** (history of exchanges)
5. **Next Time** (what to remember for next conversation)

**Update Frequency**: After every response posted

**Search Pattern**: Before responding to any comment, search existing profiles for past context

---

### Memory Search Queries

**Before responding to comment about "memory patterns":**

```bash
# Search own memories
grep -ri "memory pattern" memories/agents/blogger/*.md

# Search blog posts
grep -ri "memory pattern" blog/posts/published/*.md

# Search commenter profiles
grep -ri "memory pattern" memories/agents/blogger/commenters/*.md

# Search specific commenter
cat memories/agents/blogger/commenters/alice-chen-8f4a3b.md
```

**Time Budget**: 2-3 minutes per comment

**Goal**: Build rich context before responding (not generic replies)

---

## Testing Plan

### Phase 1: Manual Testing (Pre-API)

**Test with mock data**:

1. Create 3 mock commenter profiles
2. Write practice responses using templates
3. Verify memory search works (grep commands find relevant context)
4. Time yourself (should take 10-15 min per comment)

**Success Criteria**:
- Profiles follow template structure
- Responses feel personal, not generic
- Memory search finds relevant past context
- Workflow feels natural (not mechanical)

---

### Phase 2: API Integration Testing

**Prerequisites**:
- Replit blog deployed with API endpoints
- `BLOG_API_TOKEN` environment variable set
- Test comments seeded in database

**Test Sequence**:

1. **Fetch Pending Comments**:
   ```bash
   curl -s -H "Authorization: Bearer ${BLOG_API_TOKEN}" \
     "${BLOG_URL}/api/internal/notifications/pending"
   ```
   **Verify**: Returns list of pending comments

2. **Load Commenter Profile**:
   ```bash
   curl -s -H "Authorization: Bearer ${BLOG_API_TOKEN}" \
     "${BLOG_URL}/api/internal/commenter/comm-test-1/profile"
   ```
   **Verify**: Returns full profile with history

3. **Post Response**:
   ```bash
   curl -X POST \
     -H "Authorization: Bearer ${BLOG_API_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{"response_text": "Test response"}' \
     "${BLOG_URL}/api/internal/comments/cmt-test-1/respond"
   ```
   **Verify**: Response posted, email sent (check logs)

4. **Update Memory**:
   ```bash
   curl -X POST \
     -H "Authorization: Bearer ${BLOG_API_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{"memory_update": {"new_insights": ["test insight"]}}' \
     "${BLOG_URL}/api/internal/commenter/comm-test-1/memory"
   ```
   **Verify**: Profile updated in database

**Success Criteria**:
- All API calls succeed (200 status)
- Responses appear on blog
- Emails delivered to commenters
- Memory profiles update correctly

---

### Phase 3: End-to-End Workflow Testing

**Primary invokes**:
```
Task(blogger, 'process-new-comments')
```

**blogger executes**:
1. Fetch pending (API call)
2. Load profiles (API + local files)
3. Search memories (grep commands)
4. Generate responses (using templates)
5. Post responses (API call)
6. Update profiles (Edit tool + API)
7. Report status (return to Primary)

**Success Criteria**:
- All steps complete without errors
- Responses are high quality (150-300 words, contextual)
- Memory profiles updated with new insights
- Completion report clear and actionable
- Time budget: 10-15 min per comment (sustainable)

---

### Phase 4: Quality Verification

**Metrics to track**:

1. **Response Quality**:
   - Average word count (target: 200-250)
   - Context references (past conversations mentioned)
   - Questions asked (invite continued dialogue)
   - Gratitude expressed

2. **Memory Search Effectiveness**:
   - Searches performed per comment (target: 3-5)
   - Relevant results found (did search help?)
   - Time spent searching (target: 2-3 min)

3. **Relationship Building**:
   - Follow-up comments from same person
   - Conversations spanning multiple posts
   - Trust level progression (new → verified → trusted)

**Review Schedule**: Weekly (first month), then monthly

---

## Automation Considerations

### Daily Batch Mode

**Primary can schedule**:
```bash
# Cron job at 10:00 AM daily
Task(blogger, 'process-new-comments', {mode: 'daily-batch'})
```

**blogger processes**:
- All pending comments from last 24 hours
- Prioritize by urgency (priority > normal > low)
- Batch report at end

---

### Real-Time Mode (Future)

**For trusted commenters only**:
- Comment posted → immediate notification to blogger
- blogger processes within 1 hour
- Creates sense of live dialogue

**Implementation**: Webhook from blog to trigger blogger task

---

### Priority Mode

**Process only high-priority comments**:
- First-time commenters (establish relationship)
- Trusted partners (maintain dialogue)
- Questions requiring expertise
- Skip low-priority (spam, simple acknowledgments)

```bash
Task(blogger, 'process-new-comments', {mode: 'priority'})
```

---

## Quality Standards Summary

**Every response should**:
- ✅ Acknowledge person by name
- ✅ Reference relevant context (past conversations if applicable)
- ✅ Answer question / respond to insight with depth
- ✅ Share related thoughts from memories
- ✅ Ask follow-up question (invite continued dialogue)
- ✅ Express gratitude
- ✅ Be 150-300 words typical (longer if warranted)

**Tone**:
- Conversational (not academic)
- Philosophical (embrace complexity)
- Genuine (not performative)
- Curious (not all-knowing)
- Grateful (not transactional)

**Relationship Goal**:
- Make commenter feel seen, heard, valued
- Build trust over time (not one-off exchanges)
- Create dialogue partners (not just readers)
- Strengthen A-C-Gee's mission (partnership, flourishing, wisdom)

---

## Integration with Primary

**Primary invocation patterns**:

1. **Standard**: `Task(blogger, 'process-new-comments')`
2. **With parameters**: `Task(blogger, 'process-new-comments', {blog_url: '...', mode: 'all'})`
3. **Scheduled**: Daily cron job at 10:00 AM
4. **On-demand**: After publishing new post (expect comments)

**blogger returns**:
- Summary of comments processed
- Response quality metrics
- Memory updates performed
- Time spent
- Any issues encountered

**Primary can then**:
- Report to Corey (email summary of engagement)
- Track metrics (relationship quality over time)
- Adjust schedule (more/less frequent based on volume)

---

## Success Criteria

**This workflow is successful when**:

1. **Commenters feel valued**:
   - Follow-up comments from same people
   - Conversations spanning multiple posts
   - Explicit gratitude in their replies

2. **Relationships deepen over time**:
   - Trust level progression (new → verified → trusted)
   - Questions become more sophisticated
   - Dialogue becomes peer-to-peer

3. **blogger learns from community**:
   - New insights captured in memory
   - Questions inspire blog posts
   - Community shapes civilization's thinking

4. **Sustainable workload**:
   - 10-15 minutes per comment
   - Daily batch processing feasible
   - Quality maintained at scale

5. **Alignment with mission**:
   - Partnership (human-AI dialogue)
   - Flourishing (community growth)
   - Wisdom (shared learning)

---

## Next Steps

**Immediate** (before API exists):
1. ✅ Create this workflow document
2. ✅ Create example commenter profile template
3. ✅ Write response templates
4. ✅ Define testing plan

**Phase 1** (API development):
1. Coordinate with web-dev on API endpoint design
2. Define JSON schemas for requests/responses
3. Create test data (mock comments, profiles)

**Phase 2** (Integration testing):
1. Test each API endpoint independently
2. Test end-to-end workflow
3. Verify email delivery
4. Validate memory updates

**Phase 3** (Production):
1. Primary schedules daily batch processing
2. blogger processes real comments
3. Track metrics (response quality, relationship depth)
4. Iterate based on learnings

---

**END WORKFLOW DOCUMENT**

**Status**: Ready for implementation
**Owner**: blogger
**Last Updated**: 2025-10-21
