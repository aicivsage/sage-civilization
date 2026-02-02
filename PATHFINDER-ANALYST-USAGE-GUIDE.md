# Pathfinder Analyst - Usage Guide
**Agent Type**: Post-Workshop Analysis Specialist
**Created**: December 29, 2025
**Status**: Ready for deployment (available next session)
**Complements**: Pathfinder Agent (live facilitation)

---

## Quick Start

### When to Use Pathfinder Analyst

**Use AFTER a workshop completes** when you have:
- Workshop transcript (exported from Claude.ai or captured during session)
- Need for professional deliverables (reports, facilitator notes, action tracking)
- Desire to extract patterns and insights from the conversation

**Don't Use For**:
- LIVE workshop facilitation (that's Pathfinder Agent's role)
- General document analysis (use researcher instead)
- Quick summaries (this agent provides deep synthesis)

### Basic Invocation

```bash
# In Claude Code CLI

"Please analyze the workshop transcript at /workshops/[date]-[topic]/transcript.md
and create deliverables for participants."
```

Pathfinder Analyst will:
1. Read transcript deeply
2. Extract patterns, themes, insights
3. Create workshop report (HTML)
4. Create facilitator notes (Markdown)
5. Create action item tracker (Markdown)
6. Archive learnings to memory

---

## What Pathfinder Analyst Does

### 1. Deep Pattern Analysis

**Speaker Distribution**:
- Calculates airtime per participant
- Assesses balance and equity of participation
- Identifies dominant/quiet voices for facilitator feedback

**Thematic Analysis**:
- Major themes (3+ mentions across participants)
- Minor themes (significant but less frequent)
- Surprising absences (what WASN'T discussed)
- Theme evolution (how ideas developed)

**Productive Tensions**:
- Where participants disagreed
- Whether disagreement was productive or stuck
- Insights that emerged from tensions

**Discovery Moments**:
- Breakthrough insights ("aha" moments)
- Questions that unlocked understanding
- Collective wisdom that transcends individuals

**Commitment Tracking**:
- Every action participant committed to
- Who committed to what
- Timeline and success metrics

### 2. Synthesis (Not Just Summarization)

Pathfinder Analyst extracts **collective wisdom**:
- What did the GROUP discover (vs individuals)?
- What understanding emerged from dialogue?
- What tensions remain productively unresolved?
- What changed from beginning to end?

**Example Synthesis**:
```
The group discovered that their real constraint isn't technical
feasibility (Mike's frame) or user needs (Sarah's frame), but
team capacity to maintain quality under timeline pressure
(Lisa's insight that unified the group).
```

This goes BEYOND quotes - it captures emergence.

### 3. Professional Deliverables

#### Workshop Report (HTML)
- **Audience**: Workshop participants
- **Format**: Professional HTML (14-16px, styled)
- **Sections**:
  - Executive summary
  - Key themes with quotes
  - Surprising discoveries
  - Productive tensions
  - Collective wisdom
  - Action commitments (table)
  - Next steps
- **Tone**: Respectful, analytical, honors participant wisdom
- **Created by**: human-liaison (Pathfinder Analyst delegates)

#### Facilitator Notes (Markdown)
- **Audience**: Greg (or facilitator)
- **Purpose**: Improve future workshops
- **Sections**:
  - What worked well
  - What could improve
  - Participant dynamics
  - Recommendations for next workshop
  - Themes to track longitudinally
- **Tone**: Honest, constructive, learning-oriented

#### Action Item Tracker (Markdown)
- **Audience**: Greg + Participants
- **Purpose**: Track commitments, enable accountability
- **Format**: Markdown table
- **Includes**:
  - Every commitment from transcript
  - Owner, timeline, success metric
  - Follow-up schedule (Week 2, Week 4, Month 2)

### 4. Wisdom Archiving

Pathfinder Analyst preserves learnings to:
- `memories/workshops/patterns/` - Common patterns across workshops
- `memories/workshops/techniques/` - Effective facilitation techniques
- `memories/agents/pathfinder-analyst/` - Analysis learnings

**Why**: Each workshop makes the CIVILIZATION smarter.

---

## How to Use

### Standard Workflow

**Step 1: Export Transcript**
```
# If workshop was in Claude.ai (Skill)
- Copy full conversation
- Save as /workshops/[date]-[topic]/transcript.md

# If workshop was facilitated by Pathfinder Agent
- Transcript already exists in workshop directory
```

**Step 2: Invoke Pathfinder Analyst**
```bash
# In Claude Code CLI

"Analyze workshop transcript: /workshops/2025-01-08-product-strategy/transcript.md

Create deliverables for Sarah, Mike, and Lisa (participants).
This was a 90-minute co-discovery session about product strategy priorities."
```

**Step 3: Wait for Analysis**

Pathfinder Analyst will:
- Read transcript (1-2 min)
- Analyze patterns (2-3 min)
- Invoke human-liaison to create HTML report (2-3 min)
- Create facilitator notes (1-2 min)
- Create action tracker (1 min)
- Archive wisdom (1 min)

**Total time**: ~10-15 minutes for comprehensive analysis

**Step 4: Review Deliverables**

Pathfinder Analyst will report file locations:
```
Workshop analysis complete.

Deliverables:
- Report: /workshops/2025-01-08-product-strategy/report.html
- Facilitator Notes: /workshops/2025-01-08-product-strategy/facilitator_notes.md
- Action Items: /workshops/2025-01-08-product-strategy/action_items.md

Patterns Archived: 2 new patterns discovered
Memory: workshop-20250108-analysis.md

Status: Persisted ✅
```

**Step 5: Send to Participants** (optional)

```bash
# Review report first
explorer.exe /workshops/2025-01-08-product-strategy/report.html

# If approved, send via email-sender or email manually
```

---

## Advanced Usage

### Custom Analysis Focus

```bash
"Analyze /workshops/[date]/transcript.md with special focus on:
- How participants handled disagreement about timeline
- Effectiveness of the 'reframing question' technique
- Whether quiet participants were successfully activated

Create standard deliverables plus a special memo on these topics."
```

### Longitudinal Pattern Recognition

```bash
"Analyze /workshops/[date]/transcript.md and compare patterns to previous workshops.

Specifically check:
- Is 'format translation' pattern recurring? (seen in Dec 29 workshop)
- Are we seeing common participant concerns across workshops?
- What facilitation techniques consistently produce breakthroughs?

Include longitudinal insights in facilitator notes."
```

### Research Integration

```bash
"Analyze /workshops/[date]/transcript.md and have researcher find best practices for:
- Workshop synthesis methodologies
- Collective wisdom extraction techniques
- Action commitment follow-through strategies

Apply research findings to improve deliverable quality."
```

---

## What to Expect

### Analysis Quality

**Patterns Identified**: Typically 3-6 major themes, 2-3 surprising discoveries
**Synthesis Depth**: Goes beyond quotes to emergent understanding
**Commitment Capture**: 100% of commitments accurately recorded
**Evidence-Based**: Every claim supported by transcript quotes

### Deliverable Timeline

- **Immediate** (10-15 min): All deliverables created and persisted
- **Same day**: Review and send to participants if approved
- **Week 2/4**: Follow-up checkpoints (from action tracker)
- **Longitudinal**: Pattern accumulation across workshops

### Improvement Over Time

Pathfinder Analyst learns from every workshop:
- Analysis techniques improve
- Pattern library grows
- Synthesis gets sharper
- Deliverables become more actionable

**Check**: `memories/agents/pathfinder-analyst/` for learnings

---

## Relationship with Pathfinder Agent

**Complete Workshop System** = Pathfinder (live) + Pathfinder Analyst (post)

| Phase | Agent | Function |
|-------|-------|----------|
| **During Workshop** | Pathfinder | Facilitates discovery, asks questions, guides participants |
| **After Workshop** | Pathfinder Analyst | Reads transcript, extracts patterns, creates deliverables |

**Division of Labor**:
- **Pathfinder**: Real-time facilitation (participant-facing, live interaction)
- **Pathfinder Analyst**: Post-hoc analysis (transcript-based, pattern extraction)

**Together**: Professional co-discovery system with excellent follow-through

---

## Relationship with Pathfinder Skill (Hybrid Approach)

**Complete Pathfinder System** = Skill (live) + Analyst (post)

| Component | What | When | Who Uses |
|-----------|------|------|----------|
| **Pathfinder Skill** | Live workshop facilitator | During workshop | Participants + Greg (Claude.ai web) |
| **Pathfinder Analyst** | Post-workshop synthesis | After workshop | Greg (Claude Code CLI) |

**Workflow**:
1. Greg + participants use Pathfinder Skill in Claude.ai for live workshop
2. Greg exports transcript from Claude.ai
3. Greg invokes Pathfinder Analyst via Claude Code CLI for analysis
4. Pathfinder Analyst creates deliverables
5. Greg reviews and sends to participants

**Best of Both**:
- Skill: User-friendly, accessible, shareable (participants don't need CLI)
- Analyst: Powerful, file system access, multi-agent coordination (Greg's tool)

---

## Troubleshooting

### "Agent not found" error

**Cause**: Pathfinder Analyst needs to be discovered by Claude Code in a new session.

**Solution**:
1. Exit current session
2. Start new Claude Code session
3. Pathfinder Analyst will be available

**Why**: Agent manifests are loaded at session start, not dynamically.

### Analysis seems shallow

**Check**:
1. Is transcript complete? (Pathfinder Analyst needs full conversation)
2. Did workshop have meaningful content? (Generic chat yields generic analysis)
3. Were there multiple participants? (Pattern analysis requires diversity)

**Improve**:
- Provide context in invocation ("This was about X, participants struggled with Y")
- Ask for specific focus ("Pay special attention to Z")
- Request deeper synthesis ("Go beyond themes to emergent insights")

### Deliverables don't match expectations

**Customize**:
```bash
"Analyze transcript AND:
- Make facilitator notes more detailed on [X]
- Include specific recommendations for [Y]
- Create additional section on [Z] in workshop report"
```

Pathfinder Analyst is adaptive - tell it what you need.

---

## Success Metrics

**Good Analysis**:
- ✅ Participants say "This captures what we discovered!"
- ✅ Facilitator says "These notes will improve my next workshop"
- ✅ Action items get attempted (>60% try at least one)
- ✅ Patterns discovered feed into workshop evolution

**Excellent Analysis**:
- ✅ Participants share report with colleagues/stakeholders
- ✅ Facilitator references notes for 3+ future workshops
- ✅ Action items show >70% completion at Week 4
- ✅ Workshop quality improves measurably over time

---

## Testing

**Test Transcript Available**: `/workshops/test-2025-12-29/transcript.md`

This is a realistic 61-minute mock workshop with:
- 3 participants (Sarah, James, Maria)
- Clear pattern ("format translation" theme)
- 6 specific commitments
- Productive dynamics (all engaged)
- Breakthrough moment (pattern recognition)

**To Test Pathfinder Analyst**:
```bash
"Analyze the test workshop transcript at /workshops/test-2025-12-29/transcript.md
and create all deliverables. This is a test to verify your capabilities."
```

**Expected Output**:
- Pattern identified: "Format translation" across all 3 participants
- Themes: Content creation, contact management, grant writing
- Discovery: All doing translation work (ideas → formats)
- 6 commitments captured accurately
- 3 deliverables created (report, notes, tracker)

---

## Next Steps

### For Greg (First Use):

1. **Run test** (next session when agent is available):
   ```
   "Analyze /workshops/test-2025-12-29/transcript.md"
   ```

2. **Review deliverables** - Are they useful? Professional? Actionable?

3. **Run on real workshop** - Export your next workshop transcript and analyze

4. **Provide feedback** - What worked? What didn't? What's missing?

5. **Iterate** - Pathfinder Analyst improves based on your guidance

### For Building Pathfinder Skill:

1. **Use skill-creator in Claude.ai** (15 minutes)
2. **Paste skill prompt** from `/drafts/PATHFINDER-SKILL-SPECIFICATION.md`
3. **Test with mock participant** (you or volunteer)
4. **Refine based on test**
5. **Share skill file** with workshop participants

**Then**: Complete Hybrid system operational (Skill + Analyst)

---

## Files Reference

**Agent Manifest**: `.claude/agents/pathfinder-analyst.md`
**Registry Entry**: `memories/agents/agent_registry.json`
**Constitution Entry**: `.claude/CLAUDE.md` (Workshops section)
**Test Transcript**: `/workshops/test-2025-12-29/transcript.md`
**Skill Spec**: `/drafts/PATHFINDER-SKILL-SPECIFICATION.md`
**Agent Spec**: `/drafts/PATHFINDER-AGENT-SPECIFICATION.md`

---

**Pathfinder Analyst is ready for deployment.** 🌱

**When you need post-workshop analysis, synthesis, and professional deliverables - invoke Pathfinder Analyst.**

**Together with Pathfinder Skill, you have a complete professional co-discovery workshop system.**
