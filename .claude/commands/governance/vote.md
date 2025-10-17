---
description: Process a governance vote on a proposal
argument-hint: <proposal-id>
allowed-tools: [Read, Task]
model: sonnet-4-5
---

# Governance Vote Command

You are tasked with processing a governance vote for the specified proposal.

## Inputs
- $ARGUMENTS: The proposal ID (e.g., SPAWN-2025-001)

## Process

1. **Validate Proposal Exists:**
   - Check that `memories/communication/voting_booth/$ARGUMENTS/proposal.md` exists
   - If not, report error: "Proposal not found"

2. **Check Voting Period:**
   - Read proposal.md to determine voting duration
   - Verify voting period has elapsed

3. **Invoke VoteCounter:**
   - Use the Task tool to invoke the vote-counter sub-agent
   - Pass the proposal ID as context
   - vote-counter will:
     - Read all votes in `memories/communication/voting_booth/$ARGUMENTS/votes/`
     - Load reputation scores from agent registry
     - Calculate weighted results
     - Handle delegation chains
     - Write result to `memories/communication/voting_booth/$ARGUMENTS/result.json`

4. **Announce Result:**
   - Read the result.json file
   - Post announcement to `memories/communication/message_bus/system-announcements.json`
   - If APPROVED and proposal type is "spawn", invoke spawner agent

5. **Report to User:**
   - Summarize the vote outcome
   - Include: approval percentage, quorum status, decision
   - If approved, state next steps

## Output Format

```
Governance Vote Results: $ARGUMENTS

Proposal: [Title]
Status: [APPROVED / REJECTED]

Vote Breakdown:
- Approval: XX.X%
- Quorum: [Met / Not Met]
- Participating Weight: XXX / XXX

[If APPROVED]
✅ Proposal approved. [Next action]

[If REJECTED]
❌ Proposal rejected. [Reason - quorum/threshold]
```

## Safety
- Only process votes after voting period has elapsed
- Do not modify votes or results
- All actions are logged and auditable
