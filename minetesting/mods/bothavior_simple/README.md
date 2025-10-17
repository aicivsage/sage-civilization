# bothavior_simple

Minimal attention-economy MVP for Minetest.

## Loop
- Define a plot, assign an owner.
- Pay 100 ENERGY → plot is **open** for 24 hours; else **glass wall** appears.
- Spawn AIs; they wander for novelty and can be persuaded with `!talk`.
- For every second an AI is on an **open** plot, that plot's **owner** earns **POINTS**.

## Commands
- `/setpos1`, `/setpos2` then `/plot_create <plot_name> <owner_name>`
- `/plot_taxpay <plot_id>`
- `/ai_spawn <AIName>`
- `!talk <AIName> <message>`
- `/energy`, `/points <player>`

## Config you'll likely tweak
- `POINTS_PER_AI_SECOND`
- `AI_*` knobs for boredom/teleport
- `TAX_*` knobs for cost/duration

## Swap local ledger with your DB
- See `points.lua`: `DB_POINTS_ENDPOINT` hook for awarding POINTS.
- Replace `land.lua` storage with your DB service for real ownership.

## Installation

1. Install Minetest 5.7+ (or 5.6.1 works too)
2. Create a world in Minetest
3. Copy this entire `bothavior_simple/` folder into `<world>/worldmods/`
4. Start the world with the mod enabled

## Quick Start

1. Join your world
2. Stand where you want plot corner 1: `/setpos1`
3. Walk to plot corner 2: `/setpos2`
4. Create plot: `/plot_create myplot YourName`
5. Spawn an AI: `/ai_spawn BotAlice`
6. Pay taxes to open your plot: `/plot_taxpay myplot-<timestamp>`
7. Talk to AI to invite them: `!talk BotAlice come check out my cool new game`
8. Watch points accumulate: `/points YourName`

## Notes

- Glass walls are purely visual and cheap. If you want true protection, add a protection callback.
- Persuasion is intentionally dumb. Wire your LLM: parse the player's message, score novelty/credibility, and return a reason_weight float in [0,1].
- Balance: two numbers define the whole vibe—POINTS_PER_AI_SECOND and AI_TELEPORT_PROB. Crank carefully unless you want hummingbird AIs with ADHD.

This is the bones. Simple. Testable. No crypto fluff, no moons, no lasers—just plots, taxes, AIs, persuasion, points. When you're ready, we can snap your external DB in cleanly and then escalate to the spicy stuff.
