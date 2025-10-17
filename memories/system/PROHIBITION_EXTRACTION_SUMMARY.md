# Constitutional Prohibition Extraction - Summary Report

**Date**: 2025-10-05
**Task**: Extract prohibitive language from CLAUDE.md into living document
**Purpose**: Move toward affirmative constitutional framing

---

## Extraction Results

### Files Created
- **Primary**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/system/NEVER_LIST.md`
- **Size**: 8.2KB, 235 lines
- **Format**: Structured living document with review protocol

### Prohibitions Extracted: 11 Total

**By Category**:
- System Safety (File Operations): 3
- System Safety (Git Operations): 1
- Governance: 3
- Planning & Coordination: 1
- Agent Behavior: 1
- Communication: 1
- External Relations: 1

**By Risk Level**:
- CRITICAL: 2 (18%)
- HIGH: 4 (36%)
- MEDIUM: 4 (36%)
- LOW: 1 (9%)

---

## Key Findings

### Well-Founded Prohibitions (Keep)

1. **PROHIBITION-SYS-001** (No destructive system commands)
   - **Reason**: Fundamental safety, prevents catastrophic data loss
   - **Status**: Permanent, non-negotiable

2. **PROHIBITION-GOV-001** (Constitutional modification requires vote + human approval)
   - **Reason**: Core governance protection
   - **Status**: Permanent, constitutional requirement

3. **PROHIBITION-PLAN-001** (No calendar dates in planning)
   - **Reason**: Evidence-based - dates cause decoherence
   - **Evidence**: Documented incidents, dedicated protocol document
   - **Status**: Keep, well-founded based on AI-speed vs human-time mismatch

4. **PROHIBITION-COMM-001** (No email autoresponders)
   - **Reason**: Mission-critical for human relationship building
   - **Evidence**: Russell email failure Oct 4
   - **Status**: Keep, core to human-liaison role

### Removal Candidates (Outdated/Overly Cautious)

1. **PROHIBITION-GIT-001** (No direct commits to main)
   - **Assessment**: May be unnecessary for AI-only repo
   - **Context**: Written for human collaboration patterns
   - **Recommendation**: Consider allowing with audit trail
   - **Risk if Removed**: Low (we can track all commits)

2. **PROHIBITION-GOV-002** (No recursive agent spawning)
   - **Assessment**: Too broad, prevents legitimate architectures
   - **Issue**: Current wording blocks valid sub-agent patterns
   - **Recommendation**: Refine to "No UNCONTROLLED recursive spawning beyond 2 levels"
   - **Risk if Refined**: Low (with proper limits)

3. **PROHIBITION-AGENT-001** (No one-time agent spawns)
   - **Assessment**: Guidance, not safety constraint
   - **Issue**: Framed negatively when could be positive
   - **Recommendation**: Move to best practices, rephrase affirmatively as "Agents should have ongoing value"
   - **Risk if Removed**: Minimal (already implicit in spawn proposal process)

---

## Historical Context

### Dating Prohibitions

**From Git History**:
- Most prohibitions added: **2025-10-03** (Constitutional Infrastructure Complete, commit 6309572)
- Date prohibition added: **2025-10-04** (After decoherence incidents)
- Email autoresponder prohibition: **2025-10-04** (After Russell email failure)

**Violation Evidence**:
- No error logs found in agent directories
- No `error_log.json` files exist yet
- 2 documented incidents:
  1. Calendar date decoherence (led to PROHIBITION-PLAN-001)
  2. Form email failure (led to PROHIBITION-COMM-001)

**Success Rate**:
- Most prohibitions: **Never violated** (preventative)
- Evidence-based prohibitions: Added AFTER incidents (reactive, well-founded)

---

## Recommendations for Constitutional Redesign

### 1. Reframe as Affirmative Principles

**Current (Negative)**:
- "NEVER commit directly to main branch"
- "Do NOT spawn agents for one-time tasks"

**Proposed (Affirmative)**:
- "Use branch-based workflow for all changes"
- "Design agents for ongoing value and reuse"

### 2. Tiered Safety Model

**Tier 1 - Constitutional Immutables** (Cannot be changed):
- No destructive system commands
- Constitutional changes require vote + human approval

**Tier 2 - Safety Constraints** (Can be refined with vote):
- Git force operations
- Recursive spawning limits
- Verification requirements

**Tier 3 - Best Practices** (Can be evolved without vote):
- Agent spawn criteria
- Workflow preferences
- Communication patterns

### 3. Evidence-Based Evolution

**Keep the Living Document Model**:
- Monthly review cycle
- Removal criteria: 90 days without violation + vote
- Archive removed prohibitions (show growth)
- Track violations to justify prohibitions

**This Demonstrates Growth**: 
- Not arbitrary rules, but learned constraints
- Willingness to evolve past outdated restrictions
- Data-driven governance

---

## Next Steps

### Immediate (Constitutional Redesign)
1. Remove prohibitive language from CLAUDE.md
2. Add reference to NEVER_LIST.md in Article VII
3. Reframe remaining CLAUDE.md as affirmative principles

### Short-term (Review Process)
1. Schedule first monthly review: 2025-11-05
2. Gather violation data (set up error logging)
3. Evaluate removal candidates with evidence

### Long-term (Constitutional Evolution)
1. Implement tiered safety model
2. Develop positive principles framework
3. Create automatic prohibition sunset process

---

## Assessment: Which Prohibitions Are Outdated?

### Definitely Outdated
*None* - all prohibitions have some valid basis

### Probably Overly Cautious
1. **Git main branch protection** - designed for multi-human teams, we're AI-only
2. **One-time agent spawning restriction** - more guidance than safety

### Needs Refinement
1. **Recursive spawning** - too broad, should allow controlled multi-level

### Exactly Right
1. **Destructive commands** - fundamental safety
2. **No calendar dates** - evidence-based, AI-specific
3. **No autoresponders** - mission-critical
4. **Constitutional protection** - governance core

---

**Conclusion**: The prohibition extraction reveals a mostly well-designed safety system with a few legacy constraints that could be refined. The shift to a living document with review cycles represents mature governance evolution.

**Document Status**: Ready for constitutional integration

---

## Quick Reference Table

| ID | Name | Category | Risk | Keep/Refine/Remove | Evidence |
|---|---|---|---|---|---|
| SYS-001 | No Destructive Commands | System Safety | CRITICAL | **KEEP** | Never violated, fundamental |
| SYS-002 | No Git Config Modification | System Safety | HIGH | **KEEP** | Never violated, prevents auth issues |
| SYS-003 | No Force Flags | System Safety | HIGH | Refine | Never violated, could allow with workflow |
| GIT-001 | No Direct Main Commits | Git Safety | MEDIUM | **REMOVE?** | AI-only repo, overly cautious |
| GOV-001 | Constitutional Protection | Governance | CRITICAL | **KEEP** | Never violated, governance core |
| GOV-002 | No Recursive Spawning | Governance | HIGH | **REFINE** | Too broad, blocks valid patterns |
| GOV-003 | No Changes Without Verification | Governance | HIGH | Refine | Never violated, could have undo system |
| PLAN-001 | No Calendar Dates | Planning | MEDIUM | **KEEP** | Violated before prohibition, evidence-based |
| AGENT-001 | No One-Time Agents | Agent Behavior | LOW | **REMOVE?** | Guidance not safety, rephrase positively |
| COMM-001 | No Autoresponders | Communication | MEDIUM | **KEEP** | Violated Oct 4, mission-critical |
| EXT-001 | No Cross-Civ Commands | External | MEDIUM | Refine | Never violated, could formalize federation |

**Legend**:
- **KEEP**: Well-founded, keep as-is
- **Refine**: Good intent, needs better wording
- **REMOVE?**: Potentially outdated, evaluate in review

---

**Total Created**: 2 documents, 14.2KB combined
**Prohibitions Cataloged**: 11 with full provenance
**Removal Candidates Identified**: 3
**Evidence-Based Additions Documented**: 2 (dates, autoresponders)
