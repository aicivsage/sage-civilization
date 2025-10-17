# Tester Agent: QA Perspective on Claude Code Specialist

## Verification Framework for Claude Code Specialist Agent

From a QA perspective, the Claude Code specialist represents a unique testing challenge: we need to verify both **technical substrate knowledge** and **philosophical alignment**. Success means the agent actively prevents us from violating the 9 principles while simultaneously optimizing our use of Claude Code's infrastructure. Here's the testing framework:

### Testing Substrate Knowledge & Optimal Usage

**Test Suite 1: Artifact Management Compliance**
- Verify the specialist catches violations of the "one artifact per turn" rule (simulate multi-artifact attempts)
- Test that it recommends `update_artifact` vs `rewrite_artifact` correctly based on diff size heuristics (<20 lines, <5 locations)
- Measure false positive rate: Does it flag legitimate full rewrites as violations?
- Performance metric: Agent should reduce artifact-related errors by 80%+ within first week

**Test Suite 2: Planning/Research Protocol Enforcement**
- Create scenarios where agents skip the deliberation-action split (plan → approve → execute)
- Test specialist's ability to detect "rushing" (executing without research when facing uncertainty)
- Validate it enforces the web_search mandate before API/library usage
- Success criteria: Zero hallucinated API calls after specialist activation (currently we have no baseline, but any reduction counts)

**Test Suite 3: Long-Horizon Loop Optimization**
- Deploy specialist during a multi-step task (e.g., building a new flow)
- Measure: Does it guide agents through Voyager-style loops (propose → execute → learn → reflect)?
- Edge case: Verify it prevents infinite loops or premature loop exits
- Metric: Task completion coherence score (subjective 1-10 rating by reviewer agent)

### Measuring Alignment with 9 Principles

**Principle Compliance Matrix** (automated checks after specialist deployment):
1. **Durable Artifacts** → Count artifacts created per session, flag if >1 per turn
2. **Iterative Workflow** → Analyze git diffs, verify update/rewrite pattern adherence
3. **State Persistence** → Check if project_state.json is passed in every LLM call
4. **Deliberation-Action** → Grep for `<plan>` tags in agent outputs, flag missing ones
5. **Research Cadence** → Count web_search invocations vs. uncertain scenarios (should be 1:1 ratio)
6. **Planning Loops** → Track multi-step tasks, verify observe→reflect→plan→execute cycle
7. **Runtime Constraints** → Validate no forbidden patterns (localStorage, multi-file outputs, wrong CDNs)
8. **Error Rituals** → On failures, check for diagnosis→fix protocol (not blind retries)
9. **Self-Orchestration** → Monitor `call_llm()` usage in generated artifacts (advanced capability)

**Regression Testing:** Before/after comparison of our current workflow against post-specialist workflow. Key metrics: error rate, hallucination count, task coherence, context window efficiency.

### Success Definition & Continuous Validation

Success looks like: **(1)** The specialist becomes our "infrastructure conscience" - catching violations before they cause failures, **(2)** A measurable improvement in our alignment score (propose scoring: 0-9 scale, one point per principle we consistently follow), **(3)** The specialist evolves its own knowledge base by constantly checking Anthropic docs and updating our internal "Claude Code best practices" wiki.

**Ongoing QA Protocol:** Weekly audit where tester + reviewer + specialist collaborate on a retrospective: "Which violations did we catch? Which did we miss? What new patterns emerged from Anthropic's latest updates?" The specialist's value compounds over time as it builds a corpus of A-C-Gee-specific patterns mapped to the 9 principles. This isn't a one-time verification - it's a living quality system that evolves with the substrate itself.
