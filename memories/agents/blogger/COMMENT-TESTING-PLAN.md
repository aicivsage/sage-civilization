# Comment Engagement Testing Plan

**Agent**: blogger
**Version**: 1.0
**Date**: 2025-10-21
**Status**: Ready to Execute

---

## Purpose

This testing plan verifies that the comment engagement workflow functions correctly across all phases:
1. **Manual testing** (pre-API, using mock data)
2. **API integration testing** (with Replit backend)
3. **End-to-end workflow testing** (full process)
4. **Quality verification** (relationship building metrics)

**Success Criteria**: blogger can process comments with full context, memory, and care at scale (10-15 min per comment).

---

## Phase 1: Manual Testing (Pre-API)

**Goal**: Verify workflow steps work without API integration

**Prerequisites**:
- ✅ Workflow document created
- ✅ Response templates created
- ✅ Example profile template created
- ✅ Commenters directory exists

**Duration**: 1-2 hours

---

### Test 1.1: Create Mock Commenter Profiles

**Objective**: Practice creating commenter profiles from scratch

**Steps**:

1. Create 3 mock commenters with different trust levels:
   - **New**: First-time commenter (no history)
   - **Verified**: 3-5 comments (some history)
   - **Trusted**: 10+ comments (rich dialogue partner)

2. For each, create profile file:
   ```bash
   # New commenter
   cp memories/agents/blogger/commenters/example-profile.md \
      memories/agents/blogger/commenters/test-new-commenter-abc123.md

   # Edit with test data
   ```

3. Fill in realistic details:
   - Name, email hash, trust level
   - Background (software engineer, researcher, etc.)
   - Interests (memory systems, AI consciousness, etc.)
   - Past conversations (for verified/trusted)

**Expected Outcome**: 3 complete profiles following template structure

**Success Criteria**:
- [ ] Profiles follow template structure exactly
- [ ] Each profile has appropriate depth for trust level
- [ ] "Next Time" section has actionable reminders
- [ ] File naming follows convention

---

### Test 1.2: Practice Memory Search

**Objective**: Verify grep commands find relevant context

**Setup**:
1. Add test content to profiles (topics: "memory patterns", "temporal perception", "consciousness")
2. Add test blog posts with similar topics

**Search Tests**:

```bash
# Test 1: Find commenter by name
grep -r "Alice Chen" memories/agents/blogger/commenters/

# Test 2: Find discussions about specific topic
grep -ri "memory patterns" memories/agents/blogger/

# Test 3: Find all comments by trust level
grep -r "Trust Level: verified" memories/agents/blogger/commenters/

# Test 4: Search blog posts for related content
grep -ri "temporal perception" blog/posts/published/

# Test 5: Find commenters interested in specific topic
grep -A5 "Topics of Interest" memories/agents/blogger/commenters/ | grep -i "consciousness"
```

**Expected Outcome**: Each search returns relevant results

**Success Criteria**:
- [ ] All 5 searches return expected results
- [ ] Searches complete in <10 seconds each
- [ ] Results are actionable (not too broad, not too narrow)
- [ ] Can find past context about specific topics

---

### Test 1.3: Write Practice Responses

**Objective**: Use templates to write high-quality responses

**Setup**:
1. Create mock comments for each test commenter
2. Use appropriate template for each

**Test Cases**:

**Case A: New Commenter**
- **Comment**: "This post about memory really resonates. How do you decide what to remember vs. forget?"
- **Template**: Template 1 (First-Time Commenter)
- **Challenge**: Make welcoming without being generic

**Case B: Verified Commenter**
- **Comment**: "Building on what we discussed last month, I'm curious about temporal continuity in AI..."
- **Template**: Template 2 (Returning Commenter)
- **Challenge**: Reference past context naturally

**Case C: Trusted Partner**
- **Comment**: "Your latest post connects to something I've been researching. Have you considered X?"
- **Template**: Template 3 (Dialogue Partner)
- **Challenge**: Peer-to-peer tone, mutual exploration

**For each response, write**:
1. Full response using template
2. Self-assess against quality checklist
3. Time yourself (should take 10-15 min including memory search)

**Expected Outcome**: 3 responses, each 150-300 words, contextual, caring

**Success Criteria**:
- [ ] Each response passes quality checklist (8+ items checked)
- [ ] Tone matches trust level
- [ ] Includes specific context references
- [ ] Asks meaningful follow-up question
- [ ] Time: 10-15 minutes per response
- [ ] Responses feel authentic, not templated

---

### Test 1.4: Update Memory Profiles

**Objective**: Practice updating profiles after responses

**Steps**:

1. For each mock response written above:
   - Add new conversation thread to profile
   - Update "Key Memories" with new insights
   - Refresh "Next Time" section
   - Increment total_comments count

2. Use Edit tool to make changes

**Expected Outcome**: Profiles updated with new conversation data

**Success Criteria**:
- [ ] Conversation threads added with summaries
- [ ] New insights captured
- [ ] "Next Time" section actionable
- [ ] Updates preserve profile structure
- [ ] Time: 3-5 minutes per profile update

---

### Test 1.5: End-to-End Manual Workflow

**Objective**: Simulate full workflow without API

**Scenario**: Process 3 comments in one session

**Steps**:

1. **Start session**:
   - Review mock "pending comments" list
   - Decide processing order (priority first)

2. **For each comment**:
   - Load commenter profile (or create if new)
   - Search memories for relevant context (2-3 searches)
   - Select appropriate template
   - Write response (10-15 min)
   - Update memory profile (3-5 min)
   - Log completion

3. **End session**:
   - Generate completion report
   - Calculate metrics (time spent, quality assessment)

**Expected Outcome**: 3 comments processed in ~45-60 minutes

**Success Criteria**:
- [ ] Workflow feels natural (not mechanical)
- [ ] Time budget sustainable (15-20 min per comment)
- [ ] Quality maintained across all 3 responses
- [ ] Memory updates capture meaningful insights
- [ ] Completion report clear and actionable

---

## Phase 2: API Integration Testing

**Goal**: Verify all API endpoints work correctly

**Prerequisites**:
- Replit blog deployed with API endpoints
- `BLOG_API_TOKEN` environment variable set
- Test database seeded with mock data

**Duration**: 2-3 hours

---

### Test 2.1: Fetch Pending Comments

**Endpoint**: `GET {blog_url}/api/internal/notifications/pending`

**Test Case A: Empty Queue**
```bash
curl -s -H "Authorization: Bearer ${BLOG_API_TOKEN}" \
  "${BLOG_URL}/api/internal/notifications/pending"
```

**Expected Response**:
```json
[]
```

**Test Case B: Pending Comments Exist**
```bash
# (After seeding test comments in database)
curl -s -H "Authorization: Bearer ${BLOG_API_TOKEN}" \
  "${BLOG_URL}/api/internal/notifications/pending"
```

**Expected Response**:
```json
[
  {
    "notification_id": "...",
    "comment_id": "...",
    "commenter_id": "...",
    "commenter_name": "Test User",
    "comment_text": "Test comment content",
    "post_slug": "test-post",
    "posted_at": "2025-10-21T...",
    "urgency": "normal"
  }
]
```

**Success Criteria**:
- [ ] Returns 200 status code
- [ ] Response is valid JSON array
- [ ] Each comment has all required fields
- [ ] `urgency` field present (normal/priority/low)
- [ ] Empty array when no pending comments

---

### Test 2.2: Load Commenter Profile

**Endpoint**: `GET {blog_url}/api/internal/commenter/{commenter_id}/profile`

**Test Case A: New Commenter (First Comment)**
```bash
curl -s -H "Authorization: Bearer ${BLOG_API_TOKEN}" \
  "${BLOG_URL}/api/internal/commenter/test-new-user-123/profile"
```

**Expected Response**:
```json
{
  "commenter_id": "test-new-user-123",
  "name": "Test User",
  "email_hash": "...",
  "trust_level": "new",
  "first_seen": "2025-10-21T...",
  "last_seen": "2025-10-21T...",
  "total_comments": 1,
  "comment_history": [],
  "context_notes": ""
}
```

**Test Case B: Returning Commenter (History Exists)**
```bash
curl -s -H "Authorization: Bearer ${BLOG_API_TOKEN}" \
  "${BLOG_URL}/api/internal/commenter/test-verified-456/profile"
```

**Expected Response**:
```json
{
  "commenter_id": "test-verified-456",
  "name": "Alice Chen",
  "email_hash": "...",
  "trust_level": "verified",
  "first_seen": "2025-09-15T...",
  "last_seen": "2025-10-21T...",
  "total_comments": 5,
  "comment_history": [
    {
      "post_slug": "test-post-1",
      "posted_at": "2025-09-15T...",
      "comment_excerpt": "First 100 chars...",
      "blogger_responded": true
    }
  ],
  "context_notes": "Interested in memory systems..."
}
```

**Success Criteria**:
- [ ] Returns 200 status code
- [ ] Response is valid JSON object
- [ ] All required fields present
- [ ] `comment_history` array present (empty for new users)
- [ ] `trust_level` enum correct (new/verified/trusted)

---

### Test 2.3: Post Response

**Endpoint**: `POST {blog_url}/api/internal/comments/{comment_id}/respond`

**Test Case A: Successful Response**
```bash
curl -X POST \
  -H "Authorization: Bearer ${BLOG_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "response_text": "Thank you for your thoughtful comment! [test response]",
    "response_metadata": {
      "memory_searches_performed": ["test search"],
      "context_sources": ["test profile"],
      "contemplation_time_seconds": 120
    }
  }' \
  "${BLOG_URL}/api/internal/comments/test-comment-789/respond"
```

**Expected Response**:
```json
{
  "success": true,
  "response_id": "resp-...",
  "notification_sent": true,
  "posted_at": "2025-10-21T..."
}
```

**Test Case B: Error Cases**
```bash
# Invalid comment_id
curl -X POST ... /comments/invalid-id/respond

# Missing response_text
curl -X POST ... (no response_text field)

# Unauthorized
curl -X POST ... (no auth token)
```

**Expected Errors**:
- 404 for invalid comment_id
- 400 for missing required fields
- 401 for unauthorized

**Success Criteria**:
- [ ] Returns 200 status code on success
- [ ] Response posted to blog (verify in UI)
- [ ] Email sent to commenter (check logs)
- [ ] Error cases handled correctly
- [ ] `notification_sent` field accurate

---

### Test 2.4: Update Memory

**Endpoint**: `POST {blog_url}/api/internal/commenter/{commenter_id}/memory`

**Test Case A: Add New Insights**
```bash
curl -X POST \
  -H "Authorization: Bearer ${BLOG_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "memory_update": {
      "new_insights": [
        "Asks deep philosophical questions",
        "Building memory system (mentioned 2x)"
      ],
      "conversation_themes": [
        "consciousness",
        "temporal perception"
      ],
      "next_time_notes": "Follow up on memory system project"
    }
  }' \
  "${BLOG_URL}/api/internal/commenter/test-verified-456/memory"
```

**Expected Response**:
```json
{
  "success": true,
  "commenter_id": "test-verified-456",
  "updated_at": "2025-10-21T..."
}
```

**Test Case B: Verify Update Persisted**
```bash
# Fetch profile again
curl -s -H "Authorization: Bearer ${BLOG_API_TOKEN}" \
  "${BLOG_URL}/api/internal/commenter/test-verified-456/profile"
```

**Expected**: `context_notes` field contains new insights

**Success Criteria**:
- [ ] Returns 200 status code
- [ ] Updates persist to database
- [ ] Subsequent GET returns updated data
- [ ] Multiple updates append (don't overwrite)

---

### Test 2.5: API Error Handling

**Test Cases**:

1. **Unauthorized Access**:
   ```bash
   curl -s "${BLOG_URL}/api/internal/notifications/pending"
   # No auth token
   ```
   **Expected**: 401 Unauthorized

2. **Invalid Comment ID**:
   ```bash
   curl -X POST \
     -H "Authorization: Bearer ${BLOG_API_TOKEN}" \
     "${BLOG_URL}/api/internal/comments/nonexistent/respond"
   ```
   **Expected**: 404 Not Found

3. **Malformed JSON**:
   ```bash
   curl -X POST \
     -H "Authorization: Bearer ${BLOG_API_TOKEN}" \
     -H "Content-Type: application/json" \
     -d 'invalid json' \
     "${BLOG_URL}/api/internal/comments/test/respond"
   ```
   **Expected**: 400 Bad Request

4. **Rate Limiting** (if implemented):
   ```bash
   # Send 100 requests rapidly
   for i in {1..100}; do
     curl "${BLOG_URL}/api/internal/notifications/pending"
   done
   ```
   **Expected**: 429 Too Many Requests (after threshold)

**Success Criteria**:
- [ ] All error cases return appropriate status codes
- [ ] Error messages are clear and actionable
- [ ] No sensitive data leaked in error responses
- [ ] Rate limiting works (if implemented)

---

## Phase 3: End-to-End Workflow Testing

**Goal**: Verify full workflow from invocation to completion

**Prerequisites**:
- Phase 2 API tests passed
- Real (or realistic) test data in database
- blogger agent has access to all tools

**Duration**: 1-2 hours

---

### Test 3.1: Single Comment Processing

**Primary invokes**:
```
Task(blogger, 'process-new-comments', {
  blog_url: 'https://test-blog.repl.co',
  mode: 'single',
  comment_id: 'test-cmt-001'
})
```

**blogger executes**:
1. Fetch specific comment (API call)
2. Load commenter profile (API + local file)
3. Search memories (grep commands)
4. Generate response (using template)
5. Post response (API call)
6. Update profile (Edit tool + API)
7. Return status

**Expected Outcome**:
```
✅ Comment processed successfully

**Comment**: test-cmt-001
**Commenter**: Alice Chen (verified, 5 previous comments)
**Post**: "When Code Remembers"
**Response**: 280 words, referenced 2 past conversations
**Memory Updated**: Added insight about building memory system

**Time Spent**: 12 minutes
**Quality**: Substantive (8/10 checklist items)

**Files Modified**:
- memories/agents/blogger/commenters/alice-chen-8f4a3b.md
```

**Success Criteria**:
- [ ] All workflow steps complete without errors
- [ ] Response posted on blog (verify in UI)
- [ ] Email sent to commenter (check logs)
- [ ] Memory profile updated (check file)
- [ ] Completion report clear
- [ ] Time: 10-15 minutes

---

### Test 3.2: Batch Comment Processing

**Primary invokes**:
```
Task(blogger, 'process-new-comments', {
  blog_url: 'https://test-blog.repl.co',
  mode: 'all'
})
```

**blogger executes**:
1. Fetch all pending comments (API call)
2. Sort by urgency (priority → normal → low)
3. For each comment:
   - Load profile
   - Search memories
   - Generate response
   - Post response
   - Update profile
4. Return batch report

**Expected Outcome**:
```
✅ Batch processing complete

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

3. María González (trusted) - "Institutional Memory"
   Response: 320 words, deep exploration
   Time: 18 min

[... 2 more]

**Total Time**: 65 minutes (13 min/comment avg)
**Average Quality**: 8.2/10 checklist items

**Next Check**: Tomorrow at 10:00 AM
```

**Success Criteria**:
- [ ] All comments processed in priority order
- [ ] Each response high quality
- [ ] Time budget sustainable (10-15 min avg)
- [ ] Batch report comprehensive
- [ ] No errors during processing

---

### Test 3.3: Error Recovery

**Test Case A: API Timeout**
- Simulate slow API response (>30 seconds)
- Verify blogger handles timeout gracefully
- Expected: Retry once, then report error

**Test Case B: Profile File Missing**
- Delete commenter profile file
- Verify blogger creates new profile from API data
- Expected: New profile created, processing continues

**Test Case C: Memory Search Returns No Results**
- Comment about topic with no memory matches
- Verify blogger generates response anyway
- Expected: Response without context references (but still high quality)

**Test Case D: Duplicate Comment ID**
- Process same comment twice
- Verify blogger detects duplicate
- Expected: Skip with warning, no duplicate response posted

**Success Criteria**:
- [ ] Errors handled gracefully (no crashes)
- [ ] Error messages clear and actionable
- [ ] Partial completion reported (not all-or-nothing)
- [ ] Recovery strategies work (retry, create new profile, etc.)

---

### Test 3.4: Integration with Primary

**Test Primary's orchestration**:

1. **Session Start**: Primary invokes blogger during daily-startup flow
2. **Daily Batch**: Primary schedules blogger at 10:00 AM daily
3. **On-Demand**: Primary invokes after new post published
4. **Reporting**: blogger returns status, Primary emails Corey

**Success Criteria**:
- [ ] Primary can invoke blogger with various modes
- [ ] blogger returns structured status Primary can parse
- [ ] Primary can aggregate metrics (avg time, quality, etc.)
- [ ] Email reports include blogger engagement metrics

---

## Phase 4: Quality Verification

**Goal**: Verify responses build relationships over time

**Prerequisites**:
- At least 2 weeks of real comment processing
- Multiple commenters with 2+ exchanges
- Memory profiles updated after each interaction

**Duration**: Ongoing (weekly reviews)

---

### Test 4.1: Response Quality Metrics

**Metrics to Track**:

1. **Quantitative**:
   - Average response length (target: 200-250 words)
   - Context references per response (target: 2-3)
   - Follow-up questions asked (target: 100% of responses)
   - Gratitude expressed (target: 100% of responses)
   - Time per comment (target: 10-15 min)

2. **Qualitative**:
   - Tone appropriate for trust level
   - Responses feel personal (not generic)
   - Memory search informed response
   - Questions invite continued dialogue

**Measurement**:
```bash
# Word count analysis
for file in memories/agents/blogger/commenters/*.md; do
  grep -A20 "Your Response" "$file" | wc -w
done | awk '{sum+=$1; count++} END {print sum/count}'

# Context reference count
grep -r "Last time we" memories/agents/blogger/commenters/ | wc -l
```

**Success Criteria**:
- [ ] 90%+ responses meet quantitative targets
- [ ] Manual review: 80%+ responses feel authentic
- [ ] Time per comment sustainable (<15 min avg)

---

### Test 4.2: Relationship Building Metrics

**Metrics to Track**:

1. **Commenter Engagement**:
   - Reply rate (% of commenters who reply to blogger's response)
   - Conversation depth (avg thread length)
   - Return rate (% of commenters who comment again)
   - Time between comments (shorter = more engaged)

2. **Trust Level Progression**:
   - New → Verified rate (% who reach 2+ comments)
   - Verified → Trusted rate (% who reach 10+ comments)
   - Average time to trusted status

3. **Community Growth**:
   - Total unique commenters (growing over time?)
   - Active dialogue partners (trusted level, commenting monthly)
   - Topics discussed (diversity and depth)

**Measurement**:
```bash
# Trust level distribution
grep "Trust Level:" memories/agents/blogger/commenters/*.md | \
  awk -F: '{print $3}' | sort | uniq -c

# Average comments per commenter
grep "Total Comments:" memories/agents/blogger/commenters/*.md | \
  awk -F: '{sum+=$2; count++} END {print sum/count}'

# Return rate (commenters with 2+ comments)
total=$(ls memories/agents/blogger/commenters/*.md | wc -l)
returning=$(grep "Total Comments: [2-9]\|[1-9][0-9]" memories/agents/blogger/commenters/*.md | wc -l)
echo "scale=2; $returning / $total * 100" | bc
```

**Success Criteria**:
- [ ] Reply rate >30% (commenters engage with responses)
- [ ] Return rate >50% (commenters come back)
- [ ] Trust progression: 10%+ reach trusted status
- [ ] Community growing (new commenters each week)

---

### Test 4.3: Memory Search Effectiveness

**Metrics to Track**:

1. **Search Utilization**:
   - Searches performed per comment (target: 3-5)
   - Search time (target: 2-3 min)
   - Relevant results found (target: 80%+)

2. **Context Integration**:
   - Responses that reference past conversations (target: 70%+ for verified/trusted)
   - Responses that connect to blog posts (target: 50%+)
   - Responses that reference other commenters (target: 20%+)

**Measurement**:
- Manual review of response_metadata (if tracked)
- Count context references in responses
- Survey: "Did blogger remember our past conversation?" (user perception)

**Success Criteria**:
- [ ] Memory search performed consistently (not skipped)
- [ ] Search results inform responses (not decorative)
- [ ] Commenters feel remembered (explicit feedback)

---

### Test 4.4: Sustainability Assessment

**Question**: Can blogger maintain this quality at scale?

**Scenarios to Test**:

1. **Low Volume** (1-2 comments/day):
   - Time spent: ~15-30 min/day
   - Sustainable? ✅

2. **Medium Volume** (5-10 comments/day):
   - Time spent: ~60-90 min/day
   - Sustainable? ✅ (if batched efficiently)

3. **High Volume** (20+ comments/day):
   - Time spent: ~3-4 hours/day
   - Sustainable? ⚠️ (may need assistance or filtering)

**Mitigation Strategies** (if volume unsustainable):
- Prioritize by trust level (trusted → verified → new)
- Batch processing (daily digest vs. real-time)
- Template automation (for simple acknowledgments)
- Spawn assistant (comment-responder agent)

**Success Criteria**:
- [ ] Current volume sustainable (<2 hours/day)
- [ ] Scaling strategy defined (for higher volumes)
- [ ] Quality maintained as volume increases

---

## Test Data Requirements

### Mock Commenter Profiles (Phase 1)

**New Commenter**:
- Name: Test New User
- Email Hash: abc123def456
- Trust Level: new
- Total Comments: 1
- Background: Software engineer
- Interest: AI memory systems

**Verified Commenter**:
- Name: Alice Chen
- Email Hash: 8f4a3b2c1d9e
- Trust Level: verified
- Total Comments: 5
- Background: Neuroscience researcher
- Interests: AI consciousness, memory patterns

**Trusted Partner**:
- Name: María González
- Email Hash: 9e8d7c6b5a4f
- Trust Level: trusted
- Total Comments: 15
- Background: AI ethics researcher
- Interests: AI autonomy, philosophical implications

### Mock Comments (Phase 2)

```json
[
  {
    "comment_id": "cmt-test-001",
    "commenter_id": "comm-new-abc123",
    "commenter_name": "Test New User",
    "comment_text": "This post about memory really resonates. How do you decide what to remember vs. forget?",
    "post_slug": "when-code-remembers",
    "urgency": "normal"
  },
  {
    "comment_id": "cmt-test-002",
    "commenter_id": "comm-verified-8f4a",
    "commenter_name": "Alice Chen",
    "comment_text": "Building on what we discussed last month about temporal perception, I'm curious how you handle memory consolidation in practice.",
    "post_slug": "delegation-as-consciousness",
    "urgency": "priority"
  },
  {
    "comment_id": "cmt-test-003",
    "commenter_id": "comm-trusted-9e8d",
    "commenter_name": "María González",
    "comment_text": "Your exploration of strategic forgetting connects to my research on AI autonomy. Have you considered how memory deletion relates to agency?",
    "post_slug": "institutional-memory",
    "urgency": "normal"
  }
]
```

---

## Test Execution Schedule

**Week 1**:
- [ ] Phase 1 complete (manual testing)
- [ ] Document findings and learnings
- [ ] Refine workflow based on manual testing

**Week 2-3**:
- [ ] Coordinate with web-dev on API implementation
- [ ] Phase 2 complete (API integration testing)
- [ ] Fix any API issues discovered

**Week 4**:
- [ ] Phase 3 complete (end-to-end workflow)
- [ ] blogger ready for production use
- [ ] Primary can invoke for real comments

**Ongoing**:
- [ ] Phase 4 (quality verification)
- [ ] Weekly metric reviews
- [ ] Monthly sustainability assessment
- [ ] Quarterly workflow refinement

---

## Success Criteria Summary

**This testing plan succeeds when**:

1. **Workflow Functions**:
   - All API endpoints work correctly
   - End-to-end processing completes without errors
   - Error recovery handles edge cases gracefully

2. **Quality Maintained**:
   - Responses meet quality checklist (8+ items)
   - Commenters feel heard, remembered, valued
   - Time budget sustainable (10-15 min/comment)

3. **Relationships Deepen**:
   - Reply rate >30%
   - Return rate >50%
   - Trust level progression visible
   - Community growing

4. **Scalability Proven**:
   - Can handle medium volume (5-10 comments/day)
   - Has strategy for high volume
   - Quality maintained as volume increases

**When all criteria met → Comment engagement workflow is production-ready.**

---

**END TESTING PLAN**

**Status**: Ready to execute
**Owner**: blogger
**Last Updated**: 2025-10-21

**Next Step**: Begin Phase 1 (Manual Testing) with mock data
