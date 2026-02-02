# Analysis: Corey's Skills Guidance (Reddit Post)
**Date**: December 29, 2025
**Source**: Image forwarded by Greg from Corey
**Context**: Pathfinder project decision (Skills vs Agent Manifests)

---

## 📋 Summary

Corey sent a Reddit post titled "How to Set Up Claude Skills in <15 Minutes (for Non-Technical People)" from r/ClaudeAI by user chasing_next.

This is **directly relevant** to our pending Pathfinder decision: Should we build it as a Claude Skill (using Claude.ai's built-in skill system) or as a custom Agent Manifest (using our current .claude/agents/ system)?

---

## 📝 Reddit Post Content

### Key Points:

1. **Skills are easy to set up** ("stupid simple" per post)
2. **Skill-creator is a meta-skill** - use Claude to build other skills
3. **Process**:
   - Enable Claude Skills in settings > capabilities > skills
   - Turn on "skill-creator" skill
   - Ask Claude to create a new skill
   - Describe desired skill output in detail
   - Claude builds skill file + README
   - Upload skill file to settings
   - Test in new chat
   - Iterate if needed

4. **Workflow**:
   - Skills are Claude.ai web interface feature
   - Each skill = separate conversation capability
   - Can turn existing projects into skills
   - Downloadable skill files (shareable, version-controlled)

5. **Best Practice**: "Start with something simple (something you already do regularly)"

---

## 🎯 Implications for Pathfinder

### Background:
- **Pathfinder Project**: Co-discovery workshop facilitator for 3-5 participants
- **Current Status**: Specification complete, build ready, decision pending
- **Key Question**: Skills vs Agent Manifests vs Hybrid?

### Skills Approach (Claude.ai):

**Pros:**
- ✅ **User-friendly**: Workshop participants use Claude.ai web interface (familiar)
- ✅ **Easy setup**: <15 minutes per Corey's guidance
- ✅ **Shareable**: Download skill file, share with participants
- ✅ **No installation**: Participants don't need CLI tools
- ✅ **Built-in**: Uses Claude's native skill system (supported, maintained)

**Cons:**
- ❌ **Web-only**: Requires Claude.ai web access (not CLI/API)
- ❌ **Limited context**: Skills have conversation-level scope only
- ❌ **No file system**: Can't access local files, git repos
- ❌ **No agent coordination**: Skills don't orchestrate other agents
- ❌ **Subscription required**: Participants need Claude Pro/Team

### Agent Manifest Approach (Our System):

**Pros:**
- ✅ **Full power**: Access to file system, git, tools, agent orchestration
- ✅ **Persistent memory**: Can write to memories/, track across sessions
- ✅ **CLI integration**: Works with Claude Code CLI
- ✅ **Multi-agent**: Can invoke researcher, architect, human-liaison, etc.
- ✅ **Customizable**: Complete control over prompt, tools, behavior

**Cons:**
- ❌ **Technical setup**: Participants need Claude Code CLI installed
- ❌ **Complexity**: Requires understanding agent system
- ❌ **Not shareable**: Can't easily distribute to participants
- ❌ **Workshop friction**: Setup time eats into workshop value

---

## 💡 Recommendation: HYBRID APPROACH

**For Pathfinder specifically:**

### Phase 1: Workshop Delivery (Skill)
- **Build Pathfinder as Claude Skill** for participant use
- Easy setup (<15 min per participant)
- Web interface = accessible, familiar
- Greg facilitates via skill in Claude.ai
- Participants interact via same skill
- **Use Case**: Jan 1-15 workshop with 3-5 people

### Phase 2: Post-Workshop Analysis (Agent)
- **Pathfinder Agent Manifest** for Greg's use
- Analyzes workshop outputs
- Coordinates with researcher, architect
- Writes to memories/
- Synthesizes participant insights
- **Use Case**: Post-workshop deliverable creation

### Why Hybrid Works:
1. **Workshop participants**: Low friction (Skill = web interface)
2. **Greg's facilitation**: Can use Skill OR Agent depending on context
3. **Post-workshop**: Agent handles complex analysis, file outputs
4. **Best of both**: User-friendly delivery + powerful processing

---

## 🔄 Connection to Existing Work

### Weaver Email (Dec 26):
Corey/Weaver asked about Pathfinder approach:
> "For the Pathfinder co-discovery facilitator - would you build this as a Claude Skill (using the skill-creator feature) or as a custom Agent Manifest?"

**This Reddit post IS Corey's answer!**

He's showing us:
- Skills are "stupid simple" to set up
- skill-creator makes it easy
- Great for non-technical users
- Start with simple, familiar use cases

**Implication**: Corey is nudging us toward Skills for Pathfinder workshop delivery.

---

## 📊 Skills vs Agents Decision Matrix

| Criterion | Skill | Agent | Winner |
|-----------|-------|-------|--------|
| **Workshop participant UX** | Web interface (easy) | CLI setup (hard) | **Skill** |
| **Setup time** | <15 min | ~1 hour | **Skill** |
| **File system access** | No | Yes | **Agent** |
| **Multi-agent orchestration** | No | Yes | **Agent** |
| **Shareability** | Downloadable file | Git repo | **Skill** |
| **Persistent memory** | Conversation-scoped | Cross-session | **Agent** |
| **Post-workshop analysis** | Limited | Full power | **Agent** |
| **Greg's vision** | User-friendly | Powerful | **Hybrid** |

---

## 🎯 Next Steps

### Immediate (Autonomous):
1. ✅ Analyze Corey's guidance (this document)
2. ✅ Document Skills vs Agents trade-offs
3. ✅ Recommend Hybrid approach
4. ⏳ Draft Pathfinder Skill specification (workshop delivery)
5. ⏳ Draft Pathfinder Agent specification (post-workshop analysis)

### Awaiting Greg:
1. **Confirm approach**: Hybrid (Skill + Agent) acceptable?
2. **Workshop timeline**: Still Jan 1-15?
3. **Participant access**: Can they use Claude.ai (Pro/Team)?
4. **Deliverable format**: What do participants receive post-workshop?

### Build Phase:
1. **Skill creation** (Greg or I use skill-creator):
   - Open Claude.ai
   - Enable Skills feature
   - Use skill-creator to build Pathfinder Skill
   - Test with mock co-discovery session
   - Share with Greg for workshop use

2. **Agent creation** (I build):
   - Write `.claude/agents/pathfinder.md` manifest
   - Configure tools: Read, Write, researcher, architect
   - Test with sample workshop outputs
   - Document post-workshop analysis workflow

---

## 📌 Key Insight

**Corey's message is clear**:
> "if you're not using claude skills you're missing out. they can seem intimidating but they're actually stupid simple to set up."

This is an invitation to use the **right tool for the job**:
- **Skills** = user-facing, accessible, workshop delivery
- **Agents** = power user, file system, complex orchestration
- **Hybrid** = best of both worlds

For Pathfinder: **Deliver as Skill, analyze as Agent.**

---

## 🎤 Connection to Voice Work

**Interesting parallel**:
- Tonight's session: Discovered Silero insufficient, explored Google/ElevenLabs
- This guidance: Skills might be simpler than custom agents for some use cases
- **Pattern**: Use the right tool for professional standards (voice quality, workshop UX)

Greg's radio production ear → professional voice requirements
Corey's Skills guidance → professional workshop delivery requirements

**Both pointing to**: Don't over-engineer when simpler, better-supported solution exists.

---

**Analysis Complete** ✅
**Recommendation**: Hybrid approach (Skill for workshop, Agent for analysis)
**Awaiting**: Greg's confirmation of approach
**Ready**: To build either or both on Greg's direction

---

*This guidance feels like Corey's gentle nudge: "Skills are great for what you're doing. Try them."*
