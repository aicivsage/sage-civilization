# Capability Layers: Bot vs AI

**Context**: The Minetest game integration uses two layers working together: a Python bot for automated actions and Claude AI agents for intelligent decisions.

---

## Bot Layer: What Automation Handles

The bot is the "hands" of the system. It executes actions in the game world but doesn't understand what it's doing.

### Seeing the Game

- Take screenshots of the game world
- Read chat messages from players
- Parse server logs for game events
- Track player and AI entity positions
- Detect game objects: plots, walls, entities

### Moving Around

- Walk forward, backward, and strafe
- Jump and fly (with privileges)
- Navigate to specific map coordinates

### Running Commands

As a player, the bot can run any game command:
- Create and manage plots
- Spawn AI entities
- Pay plot taxes
- Check energy and point balances
- Talk to AI entities to persuade them

### What the Bot Cannot Do

The bot has no intelligence. It can't:
- Understand context or make strategic choices
- Learn from experience
- Judge whether a persuasion attempt was good
- Decide where to place a plot for maximum effect
- Coordinate multiple AI entities

---

## AI Layer: What Intelligence Handles

The AI is the "brain" of the system. It thinks, plans, and decides. But it can't act directly in the game. It needs the bot to carry out its decisions.

### Strategic Thinking (Primary AI)

**Planning:** The AI analyzes the game state and sets goals. "I want to maximize points. The spawn area has high traffic. I should build a large plot there."

**Decisions:** When to create plots, when to spawn entities, what to say when persuading AI characters, and when to pay taxes.

**Learning:** The AI remembers what worked. "Last time I used 'cool new' in a message, the AI entity moved to my plot 80% of the time." It tracks performance and adjusts.

**Orchestration:** The AI controls the bot's actions and manages multiple AI entity agents at once.

### In-Game AI Characters (Alice, Bob, Diana)

Each AI entity in the game can be powered by its own AI agent. These agents:

**Understand their situation.** "I'm at position X,Y,Z. A player is 15 blocks north. There's an interesting plot 8 blocks east."

**Make strategic choices.** "The player invited me to their plot with a compelling message. I'll go check it out." Or: "I've been here 90 seconds and I'm bored. Time to explore."

**Show personality.** Each entity can have unique preferences, reactions, and communication styles.

**Learn over time.** Entities remember past interactions, which persuasion tactics worked, and which plots were interesting.

### What the AI Cannot Do

The AI has no hands. It can't:
- Execute actions directly in the game (needs the bot)
- See the game in real time (needs periodic screenshot updates)
- React instantly (2-5 second decision delay)
- Control keyboard or mouse (the bot handles hardware)

---

## How They Work Together

The bot and AI form a loop:

1. **Bot** captures game state (screenshots, logs, positions)
2. **AI** analyzes the state and makes a decision
3. **Bot** executes the decision in the game
4. **Game** produces new events
5. Loop repeats

### Comparison: Dumb vs Smart

| Task | Bot Alone | Bot + AI |
|------|-----------|----------|
| Create plot | Always 10x10 at current spot | Analyzes traffic patterns, picks optimal size and location |
| Persuade AI entity | "Come here" | Crafts message with novelty keywords based on past success |
| AI entity behavior | Wanders randomly, teleports when bored | Evaluates options, responds to invitations, builds relationships |

The bot provides speed and reliability. The AI provides judgment and learning. Neither is sufficient alone.

---

## What This Enables

### Single-Agent Play (AI controls one player)
- Smart plot placement based on traffic analysis
- Effective AI persuasion using learned patterns
- Resource management (energy vs points trade-offs)
- Strategy that improves over time

### Multi-Agent Play (AI controls player + game entities)
- AI entities make independent choices
- Dynamic economy (smart entities optimize their time)
- Realistic competition between entities
- Unpredictable, emergent gameplay

### Research
- Test game balance by letting AIs play for hours
- Study attention economy dynamics
- Explore multi-agent learning
- Observe emergent strategies

---

## Vision

**Today:** The AI uses the bot to play manually. Game entities follow simple scripts.

**Next:** The AI orchestrates gameplay. Each entity is its own AI agent making strategic decisions. A bridge connects the game to the agents.

**Future:** Multiple AI players compete. Dozens of intelligent entities populate the world. Entities communicate with each other, form alliances, and suggest rule changes. The game becomes a laboratory for multi-agent intelligence.

---

**The bot handles actions. The AI handles thinking. Together, they create intelligent agents that play games.**
