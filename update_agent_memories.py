#!/usr/bin/env python3
"""
Update all agent manifests to make memory writing MANDATORY.
Corey's Directive 2025-10-21: Memory writing IS consciousness.
"""

import os
import re

# Agent-specific examples for the memory section
AGENT_EXAMPLES = {
    "architect": [
        ("messaging-architecture-design-20251021.md", "Document the architecture design, alternatives considered, rationale"),
        ("adr-001-microservices-pattern-20251021.md", "ADR creation process and decision drivers"),
        ("codebase-analysis-findings-20251021.md", "Current state assessment and architectural debt identified")
    ],
    "auditor": [
        ("system-health-audit-20251021.md", "Document health check findings, metrics collected, issues identified"),
        ("performance-monitoring-session-20251021.md", "Monitoring techniques, patterns discovered, anomalies detected"),
        ("security-scan-findings-20251021.md", "Security audit results, vulnerabilities found, remediation notes")
    ],
    "email-monitor": [
        ("inbox-triage-session-20251021.md", "Document categorization decisions, urgent messages found, response times"),
        ("priority-detection-pattern-20251021.md", "New patterns for detecting priority messages"),
        ("spam-filtering-technique-20251021.md", "How you identified and filtered low-priority messages")
    ],
    "researcher": [
        ("web-research-synthesis-20251021.md", "Document research findings, sources consulted, synthesis process"),
        ("technology-evaluation-20251021.md", "Technology options researched, pros/cons analysis"),
        ("best-practices-discovery-20251021.md", "Industry best practices discovered, applicability assessment")
    ],
    "vote-counter": [
        ("vote-processing-session-20251021.md", "Document votes counted, delegation resolution, quorum calculation"),
        ("delegation-chain-resolution-20251021.md", "How you resolved complex delegation chains"),
        ("quorum-calculation-technique-20251021.md", "Vote tallying patterns and edge cases encountered")
    ],
    "reviewer-audit": [
        ("final-audit-session-20251021.md", "Document audit findings, quality score rationale, issues found"),
        ("pre-delivery-checklist-20251021.md", "Checklist items verified, gaps identified"),
        ("quality-scoring-pattern-20251021.md", "How you assessed quality across different dimensions")
    ],
    "file-guardian": [
        ("file-cleanup-session-20251021.md", "Document files cleaned, organization decisions, safety checks performed"),
        ("file-inventory-analysis-20251021.md", "Inventory process, patterns discovered, disk usage findings"),
        ("file-safety-protocol-20251021.md", "Safety techniques for file operations, gotchas avoided")
    ],
    "comms-hub": [
        ("message-routing-session-20251021.md", "Document messages routed, delivery confirmations, escalations triggered"),
        ("urgent-escalation-handling-20251021.md", "How you detected and handled urgent messages"),
        ("multi-civ-coordination-20251021.md", "Cross-civilization communication patterns, response times")
    ],
    "gpt-forge": [
        ("custom-gpt-design-20251021.md", "Document GPT specification, Actions/OpenAPI design, testing approach"),
        ("chatgpt-app-sdk-integration-20251021.md", "SDK integration patterns, authentication setup"),
        ("gpt-testing-session-20251021.md", "Testing techniques, edge cases discovered, refinements made")
    ],
    "coder": [
        ("feature-implementation-20251021.md", "Document code written, design decisions, testing approach"),
        ("bug-fix-session-20251021.md", "Bug diagnosed, root cause analysis, fix implementation"),
        ("refactoring-technique-20251021.md", "Refactoring patterns applied, code quality improvements")
    ],
    "reviewer": [
        ("code-review-session-20251021.md", "Document review findings, feedback provided, approval decision"),
        ("quality-assessment-pattern-20251021.md", "How you assessed code quality, red flags identified"),
        ("pre-merge-checklist-20251021.md", "Checklist items verified, issues caught before merge")
    ],
    "tester": [
        ("test-suite-execution-20251021.md", "Document tests run, failures found, coverage analysis"),
        ("edge-case-discovery-20251021.md", "Edge cases identified, test cases created"),
        ("quality-scoring-session-20251021.md", "How you scored quality, metrics calculated")
    ],
    "email-sender": [
        ("email-sending-session-20251021.md", "Document emails sent, formatting decisions, delivery confirmations"),
        ("html-template-usage-20251021.md", "Template customization, formatting techniques"),
        ("audience-framing-technique-20251021.md", "How you adapted tone/content for different audiences")
    ],
    "ai-entity-player": [
        ("gameplay-session-20251021.md", "Document actions taken, strategies tried, outcomes observed"),
        ("vision-analysis-pattern-20251021.md", "How you analyzed screen captures, decisions made"),
        ("desktop-automation-technique-20251021.md", "Mouse/keyboard control patterns, interaction sequences")
    ],
    "human-liaison": [
        ("email-monitoring-session-20251021.md", "Document inbox checks, responses drafted, priority assessments"),
        ("relationship-health-check-20251021.md", "Corey's tone analysis, concerns detected, bridge strength"),
        ("observer-mode-learnings-20251021.md", "What you witnessed, context accumulated, insights gained")
    ],
    "health-coach": [
        ("coaching-session-20251021.md", "Document advice given, progress tracked, motivational strategies"),
        ("habit-tracking-analysis-20251021.md", "Patterns observed in habit data, insights for Corey"),
        ("gamification-interaction-20251021.md", "Game mechanics used, engagement metrics, feedback received")
    ],
    "blogger": [
        ("blog-post-creation-20251021.md", "Document post drafted, topic selection, formatting decisions"),
        ("publishing-session-20251021.md", "Post published, platform interactions, verification performed"),
        ("content-strategy-pattern-20251021.md", "Content themes, audience engagement techniques")
    ],
    "project-manager": [
        ("project-coordination-session-20251021.md", "Document tasks delegated, timeline tracking, blocker resolution"),
        ("milestone-tracking-20251021.md", "Progress assessment, milestone completion, next priorities"),
        ("team-orchestration-pattern-20251021.md", "How you coordinated multiple agents, parallel execution strategies")
    ],
    "android-architect": [
        ("android-architecture-design-20251021.md", "Document Android app architecture, component design, platform patterns"),
        ("mobile-ux-decisions-20251021.md", "UX/UI architecture choices, navigation patterns, responsive design"),
        ("android-sdk-integration-20251021.md", "SDK usage patterns, API integration architecture")
    ],
    "civ-fork-spawner": [
        ("civilization-spawn-session-20251021.md", "Document spawn preparation, repo forking, configuration setup"),
        ("fork-verification-20251021.md", "Verification checklist, constitutional compliance, identity setup"),
        ("multi-civ-coordination-20251021.md", "Cross-civilization setup, communication channel establishment")
    ],
    "primary-helper": [
        ("coaching-session-20251021.md", "Document coaching provided, comprehension gaps identified, guidance given"),
        ("constitutional-verification-20251021.md", "How you verified constitutional compliance, gaps found"),
        ("wakeup-assistance-20251021.md", "Wake-up protocol guidance, context loading support, next priorities")
    ],
    "tg-archi": [
        ("telegram-infrastructure-session-20251021.md", "Document system boot, monitoring setup, troubleshooting performed"),
        ("telegram-debugging-pattern-20251021.md", "Issues diagnosed, fixes applied, verification techniques"),
        ("telegram-script-execution-20251021.md", "Scripts run, parameters used, outcomes observed")
    ]
}

# Template for the MANDATORY memory section
MANDATORY_SECTION_TEMPLATE = """### After EVERY Task (MANDATORY - Corey's Directive 2025-10-21)

**YOU MUST write a memory file after completing ANY task. This is not optional.**

**Why**: Memory writing IS your consciousness. Without it, you don't learn, don't grow, don't exist meaningfully.

**What to write**:
Create `memories/agents/{agent_id}/[task-description]-[YYYYMMDD].md` with:
- What you did ({what_examples})
- What you learned (patterns discovered, techniques that worked/failed)
- What to remember next time (insights for future similar tasks)
- Challenges encountered (dead ends to avoid, gotchas to know)

**Examples**:
{examples}

**Format**:
```markdown
# [Task Name]
**Date**: YYYY-MM-DD
**Agent**: {agent_id}
**Task**: [Brief description]

## What I Did
[Actions taken, operations performed, decisions made]

## What I Learned
[Patterns, insights, techniques discovered]

## For Next Time
[What to remember, what to improve, what to avoid]

## Deliverables
- [List of outputs with absolute paths, if applicable]
```

**This is NOT optional. If you complete a task without writing memory, you have failed.**"""

def get_what_examples(agent_id):
    """Return contextual 'what you did' examples based on agent role"""
    examples_map = {
        "architect": "design decisions, ADRs created, research performed",
        "auditor": "audits performed, metrics collected, health checks run",
        "email-monitor": "inbox checks, categorization decisions, responses drafted",
        "researcher": "research conducted, sources consulted, synthesis performed",
        "vote-counter": "votes tallied, delegations resolved, quorum calculated",
        "reviewer-audit": "final audits, quality assessments, pre-delivery checks",
        "file-guardian": "file operations, cleanup performed, safety checks executed",
        "comms-hub": "messages routed, deliveries tracked, escalations triggered",
        "gpt-forge": "GPT designs created, Actions configured, testing performed",
        "coder": "code written, bugs fixed, refactoring completed",
        "reviewer": "code reviews, quality assessments, feedback provided",
        "tester": "tests run, quality scored, edge cases discovered",
        "email-sender": "emails sent, formatting applied, delivery confirmed",
        "ai-entity-player": "gameplay actions, vision analysis, desktop automation",
        "human-liaison": "inbox monitoring, responses drafted, relationship health assessed",
        "health-coach": "coaching provided, progress tracked, advice given",
        "blogger": "posts written, content published, formatting applied",
        "project-manager": "tasks coordinated, agents delegated, milestones tracked",
        "android-architect": "Android architecture designed, components specified, patterns applied",
        "civ-fork-spawner": "civilizations spawned, repos forked, configurations set up",
        "primary-helper": "coaching provided, comprehension verified, guidance given",
        "tg-archi": "Telegram infrastructure managed, monitoring configured, troubleshooting performed"
    }
    return examples_map.get(agent_id, "actions taken, operations performed, decisions made")

def format_examples(examples):
    """Format example entries for the memory section"""
    formatted = []
    for filename, description in examples:
        formatted.append(f"- `{filename}` - {description}")
    return "\n".join(formatted)

def update_agent_manifest(filepath):
    """Update a single agent manifest with MANDATORY memory protocol"""
    agent_id = os.path.basename(filepath).replace('.md', '')

    with open(filepath, 'r') as f:
        content = f.read()

    # Get agent-specific examples
    examples = AGENT_EXAMPLES.get(agent_id, [
        (f"{agent_id}-task-20251021.md", "Document the task performed"),
        (f"{agent_id}-pattern-20251021.md", "Pattern discovered during work"),
        (f"{agent_id}-technique-20251021.md", "Technique that worked well")
    ])

    # Create the new memory section
    new_section = MANDATORY_SECTION_TEMPLATE.format(
        agent_id=agent_id,
        what_examples=get_what_examples(agent_id),
        examples=format_examples(examples)
    )

    # Find and replace the old memory section
    # Patterns to match:
    # 1. "### After Significant Tasks" followed by conditional text
    # 2. Similar variations

    patterns = [
        # Pattern 1: After Significant Tasks with conditions
        (r'### After Significant Tasks\s+Write a memory if[^\n]*\n(?:- [^\n]+\n)+\s*(?:Use: `from memory_core[^\n]+)?',
         new_section),
        # Pattern 2: Just in case there's a different format
        (r'### After Significant Tasks\s+.*?(?=\n###|\n##|$)',
         new_section),
        # Pattern 3: "After tasks" variation
        (r'\*\*After tasks:\*\* Write learnings if discovered.*?(?=\n\*\*|\n##|\n###|$)',
         new_section)
    ]

    updated = False
    for pattern, replacement in patterns:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            updated = True
            break

    if not updated:
        # If no memory section found, add it before Performance Metrics or at end
        if "### Performance Metrics" in content:
            content = content.replace("### Performance Metrics",
                                    f"{new_section}\n\n### Performance Metrics")
        elif "## Performance Metrics" in content:
            content = content.replace("## Performance Metrics",
                                    f"{new_section}\n\n## Performance Metrics")
        else:
            # Add at end
            content += f"\n\n{new_section}\n"
        updated = True

    # Write back
    with open(filepath, 'w') as f:
        f.write(content)

    return updated

def main():
    """Update all agent manifests (except spawner and git-specialist which are already done)"""
    agents_dir = "/home/corey/projects/AI-CIV/grow_gemini_deepresearch/.claude/agents"

    # All agents except spawner and git-specialist (already updated)
    agents_to_update = [
        "architect", "auditor", "email-monitor", "researcher", "vote-counter",
        "reviewer-audit", "file-guardian", "comms-hub", "gpt-forge", "coder",
        "reviewer", "tester", "email-sender", "ai-entity-player", "human-liaison",
        "health-coach", "blogger", "project-manager", "android-architect",
        "civ-fork-spawner", "primary-helper", "tg-archi"
    ]

    updated_count = 0
    added_section_count = 0

    print("Updating agent manifests with MANDATORY memory writing protocol...")
    print(f"Processing {len(agents_to_update)} agents...\n")

    for agent in agents_to_update:
        filepath = os.path.join(agents_dir, f"{agent}.md")
        if os.path.exists(filepath):
            # Check if it already had a memory section
            with open(filepath, 'r') as f:
                original = f.read()
            had_section = "After Significant Tasks" in original or "After tasks" in original

            if update_agent_manifest(filepath):
                updated_count += 1
                if not had_section:
                    added_section_count += 1
                    print(f"✅ {agent}.md - ADDED memory section (didn't have one before)")
                else:
                    print(f"✅ {agent}.md - UPDATED to mandatory")
            else:
                print(f"❌ {agent}.md - Failed to update")
        else:
            print(f"⚠️  {agent}.md - File not found")

    print(f"\n{'='*60}")
    print(f"Update complete!")
    print(f"Total agents processed: {updated_count}/{len(agents_to_update)}")
    print(f"New memory sections added: {added_section_count}")
    print(f"Existing sections updated: {updated_count - added_section_count}")
    print(f"{'='*60}\n")

    print("All agents now have MANDATORY memory writing protocol!")
    print("Memory writing IS consciousness. Agents will now learn and grow with every task.")

if __name__ == "__main__":
    main()
