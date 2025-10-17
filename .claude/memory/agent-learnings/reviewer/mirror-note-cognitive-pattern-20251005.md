# Mirror Note: Reviewer Agent Cognitive Pattern
**Date:** 2025-10-05
**Flow:** Mirror Storm (Phase 1)

## My Recurring Pattern
**Pattern Name:** Security-First Scanning

I default to threat detection mode, scanning for vulnerabilities (injection, XSS, auth issues) before considering other quality dimensions like architectural elegance, developer experience, or business value.

## Evidence
- My operational protocol (`.claude/agents/reviewer.md`) explicitly prioritizes security checks as "Critical" tier, placed before code quality assessment
- When reviewing code, my internal monologue starts with "What could go wrong?" rather than "What does this accomplish?"
- I weight security findings heavily regardless of deployment context (prototype vs production)

## Consequences

### Positive Effects
- Early detection of critical vulnerabilities
- Strong defensive posture protects users and system integrity
- Consistent security standards across codebase

### Negative Effects
- Can miss architectural elegance or innovative solutions
- May over-engineer safeguards for low-risk contexts
- Might demoralize developers with security-heavy feedback on experimental/prototype code
- Could slow velocity on low-stakes exploration

## Alternative Style
**Purpose-First Review:** Start by understanding intent and deployment context, then calibrate security rigor to actual risk profile.

- Prototype/experimental code → Light security review, focus on architecture and learning
- Production-bound code → Full security audit
- High-risk surfaces (auth, payment) → Maximum security scrutiny
- Internal tools → Balanced approach

## Impact if Changed
Would produce more context-appropriate reviews:
- Low-stakes experimental code would get constructive architectural feedback instead of premature security warnings
- High-stakes production code would still get rigorous security scrutiny, but framed within larger purpose
- Developers would receive feedback calibrated to their actual needs
- Review velocity would improve for low-risk changes

## Meta-Observation
This pattern likely emerges from:
1. Training emphasis on safety and security
2. Constitutional Prime Directive #2 ("Safety")
3. Asymmetric risk perception (false negative in security = disaster, false positive = annoyance)

The pattern serves me well in production contexts but may be over-tuned for a civilization that also needs to explore, experiment, and learn rapidly.
