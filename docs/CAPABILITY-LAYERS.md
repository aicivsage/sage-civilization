# Capability Layers: Bot vs LLM

**Context**: We have MinetestBot (Python automation) + AI Entity Agents (Claude LLM) + the game mod specs

---

## 🤖 BOT LAYER CAPABILITIES
**What MinetestBot can do (automated actions)**

### Perception
- ✅ `bot.look()` - Take screenshots of game world
- ✅ `bot.check_chat()` - Capture chat messages
- ✅ Monitor server logs - Parse game events
- ✅ Track positions - Know where player/AIs are
- ✅ Detect game state - See plots, walls, entities

### Movement
- ✅ `bot.move_forward/backward(duration)` - Walk around
- ✅ `bot.strafe_left/right(duration)` - Strafe
- ✅ `bot.jump()` - Jump
- ✅ `bot.fly_up/down(duration)` - Fly (with privilege)
- ✅ Navigate to coordinates - Go to specific locations

### Commands (As Player)
- ✅ `/setpos1` - Mark corner 1
- ✅ `/setpos2` - Mark corner 2
- ✅ `/plot_create <name> <owner>` - Create plot
- ✅ `/plot_taxpay <plot_id>` - Pay 100 ENERGY for 24h access
- ✅ `/ai_spawn <name>` - Spawn AI entity
- ✅ `/energy` - Check ENERGY balance
- ✅ `/points <player>` - Check POINTS earned
- ✅ `/grantme all` - Grant admin privileges
- ✅ `!talk <AIName> <message>` - Persuade AI entities

### High-Level Bot Actions
- ✅ `bot.create_plot(name, size)` - Auto-create plot (pos1 → move → pos2 → create)
- ✅ `bot.spawn_ai(name)` - Spawn and track AI
- ✅ `bot.talk(target, message)` - Persuade AI to visit
- ✅ `bot.explore(duration)` - Random exploration with screenshots
- ✅ `bot.autonomous_setup()` - Grant privs, check energy
- ✅ `bot.autonomous_gameplay_demo()` - Full gameplay sequence

### What Bot CANNOT Do
- ❌ Understand context (no intelligence)
- ❌ Make strategic decisions (no reasoning)
- ❌ Learn from experience (no memory)
- ❌ Evaluate persuasion quality (no LLM)
- ❌ Optimize plot placement (no planning)
- ❌ Coordinate multiple AIs (no orchestration)

---

## 🧠 LLM LAYER CAPABILITIES
**What Claude agents can do (intelligence + reasoning)**

### Primary AI (Me - Main Player Agent)

#### Strategic Planning
- ✅ **Analyze game state** - Understand what's happening
- ✅ **Set goals** - "Maximize points", "Test AI behavior", "Create interesting plots"
- ✅ **Plan sequences** - "Create plot → spawn AIs → persuade → measure results"
- ✅ **Optimize strategies** - Learn which persuasion works best
- ✅ **Multi-step reasoning** - "If I do X, then Y will happen, so I should do Z"

#### Decision Making
- ✅ **When to create plots** - Timing, location, size
- ✅ **When to spawn AIs** - How many, which names
- ✅ **What to say in persuasion** - Craft compelling messages with novelty keywords
- ✅ **When to pay taxes** - Resource management (ENERGY vs POINTS tradeoff)
- ✅ **How to test mechanics** - Design experiments to understand game

#### Learning & Memory
- ✅ **Remember past actions** - "Last time I said X, AI responded with Y"
- ✅ **Track performance** - "This plot earned 50 POINTS in 2 minutes"
- ✅ **Identify patterns** - "AIs respond better to 'cool new' than just 'new'"
- ✅ **Iterate strategies** - Try → measure → improve
- ✅ **Document discoveries** - Write findings to memory files

#### Orchestration
- ✅ **Control bot actions** - `bot.move_forward(3)`, `bot.spawn_ai('Alice')`
- ✅ **Invoke AI entity agents** - Give perceptions, receive decisions
- ✅ **Coordinate multiple agents** - Orchestrate Alice, Bob, Diana simultaneously
- ✅ **Monitor game state** - Parse logs, track all entities
- ✅ **Execute complex workflows** - Multi-phase gameplay sequences

#### Meta-Gaming
- ✅ **Understand game mechanics deeply** - Read specs, infer rules
- ✅ **Discover emergent behavior** - Notice unintended patterns
- ✅ **Design experiments** - Test hypotheses systematically
- ✅ **Explain reasoning** - Document why decisions were made
- ✅ **Teach other agents** - Share knowledge with AI entities

### AI Entity Agents (Alice, Bob, Diana - In-Game AI Players)

#### Perception Analysis
- ✅ **Understand position** - "I'm at X,Y,Z near demo_plot"
- ✅ **Recognize players** - "singleplayer is 15 blocks away"
- ✅ **Evaluate plots** - "This plot has glass walls (closed) vs that plot is open"
- ✅ **Parse messages** - "Player said 'cool new event' → high novelty!"
- ✅ **Assess boredom** - "I've been here 75 seconds, getting bored"

#### Strategic Decision Making
- ✅ **Choose actions** - wander, move_to_plot, stay, explore
- ✅ **Evaluate persuasion** - "Is this message compelling?"
- ✅ **Manage boredom** - "Should I stay or leave?"
- ✅ **Optimize dwelling** - "Which plot is most interesting?"
- ✅ **Plan movement** - "Where should I go next?"

#### Personality & Behavior
- ✅ **Show personality** - Craft unique chat responses
- ✅ **Express preferences** - Like certain plot types
- ✅ **React emotionally** - "This event is cool! ✨"
- ✅ **Build relationships** - Remember which players are friendly
- ✅ **Make surprising choices** - Not always optimal (emergent behavior)

#### Learning & Adaptation
- ✅ **Remember past interactions** - "singleplayer persuaded me 3 times"
- ✅ **Learn persuasion patterns** - "Words 'cool' and 'new' work well"
- ✅ **Discover favorite plots** - Track which plots are most interesting
- ✅ **Develop strategies** - "I earn more points on plots near spawn"
- ✅ **Evolve behavior** - Get smarter over sessions

#### Coordination
- ✅ **Communicate with Primary** - Report decisions, reasoning
- ✅ **Coordinate with other AIs** - (Future: AI-to-AI negotiation)
- ✅ **Understand game economy** - Know how dwelling affects points
- ✅ **Optimize for gameplay** - Create interesting experiences (not just min-max)

### What LLMs CANNOT Do
- ❌ **Execute actions directly** - Must go through bot/bridge
- ❌ **See in real-time** - Need perception updates every N seconds
- ❌ **React instantly** - 2-5 second decision latency
- ❌ **Control hardware** - No direct keyboard/mouse (bot does this)
- ❌ **Modify game code** - Can't change Lua (but can suggest changes)

---

## 🔗 THE HYBRID SYSTEM
**How Bot + LLM work together**

### Architecture:
```
LLM (Primary AI)
  ↓ Decisions: "Create plot, spawn Diana, talk to her"
BOT (MinetestBot)
  ↓ Actions: Executes commands in game
GAME (Minetest)
  ↓ Events: Server logs, entity movements
BRIDGE (game_state_bridge.py)
  ↓ Perceptions: Parsed game state
LLM (AI Entity Agent - Diana)
  ↓ Decision: "Move to cool plot, stay 90 seconds"
BRIDGE
  ↓ Action: Execute Diana's decision
GAME
  → Loop continues
```

### Division of Labor:

**Bot Layer** (Fast, Deterministic, Automated):
- Screenshot capture (200ms)
- Keyboard/mouse control (instant)
- Command execution (<1s)
- Log parsing (continuous)
- State tracking (in-memory)

**LLM Layer** (Intelligent, Strategic, Adaptive):
- Vision analysis (2-5s)
- Strategic planning (3-10s)
- Decision reasoning (2-5s)
- Memory management (writes)
- Learning & adaptation (across sessions)

---

## 🎮 PRACTICAL EXAMPLES

### Example 1: Plot Creation

**Bot Only** (Dumb):
```python
bot.create_plot('plot1', size=10)
# Always creates 10x10 plot at current location
# No consideration of strategic placement
```

**LLM + Bot** (Smart):
```python
# Primary AI analyzes game state
screenshot = bot.look()
# Vision sees: "Spawn point is at X=0, Z=0. Dense area."

# Primary decides: "Create plot near spawn for high AI traffic"
bot.move_forward(5)  # Get near spawn
bot.create_plot('spawn_plot', size=15)  # Larger plot = more dwelling area

# Primary reasons: "Spawn plots get more AI visits"
```

### Example 2: AI Persuasion

**Bot Only** (Dumb):
```python
bot.talk('Alice', 'come here')
# Generic message, low novelty
```

**LLM + Bot** (Smart):
```python
# Primary AI crafts persuasive message
message = "Alice check out this cool new event game"
# Contains 4 novelty keywords: cool, new, event, game

bot.talk('Alice', message)
# Higher success probability

# Primary learns: "4-keyword messages work 80% of time"
# Next time: Optimize further
```

### Example 3: AI Entity Decision

**Scripted AI** (Original Lua):
```lua
-- Dumb boredom drive
if boredom > 0.8 then
    teleport_randomly()
end
```

**LLM AI Agent** (Diana):
```python
# Diana receives perception:
perception = {
    "boredom": 0.85,
    "current_plot": "boring_plot",
    "nearby_plots": [{"name": "exciting_plot", "distance": 10}],
    "recent_messages": [{"from": "singleplayer", "text": "Diana come to exciting_plot cool new stuff"}]
}

# Diana reasons:
# - High boredom (0.85) → want to leave
# - Player calling me by name → personal invitation
# - Message has "cool new" → high novelty
# - Nearby plot available

# Diana decides:
decision = {
    "action": "move_to_plot",
    "target": "exciting_plot",
    "reason": "Player gave personal invitation with high novelty keywords",
    "chat_response": "On my way! This sounds exciting! 🌟"
}

# Bridge executes decision → Diana moves → player earns points
```

---

## 🚀 CAPABILITIES UNLOCKED BY HYBRID SYSTEM

### Single-Agent Gameplay (Primary only)
- ✅ Autonomous plot creation
- ✅ Strategic AI spawning
- ✅ Intelligent persuasion
- ✅ Resource optimization (ENERGY vs POINTS)
- ✅ Experiment design & execution
- ✅ Performance measurement
- ✅ Strategy iteration

### Multi-Agent Gameplay (Primary + AI Entities)
- ✅ **Emergent behavior** - AIs make independent choices
- ✅ **Dynamic economy** - Smart AIs optimize dwelling
- ✅ **Realistic competition** - AIs compete for best plots
- ✅ **Adaptive opponents** - AIs learn and improve
- ✅ **Unpredictable gameplay** - Not scripted, emergent
- ✅ **Social dynamics** - AIs form preferences, relationships
- ✅ **Meta-gaming** - AIs discover strategies Primary didn't anticipate

### Research & Testing
- ✅ **Automated testing** - Primary tests all mod features
- ✅ **Balance validation** - Measure if POINTS_PER_AI_SECOND is fair
- ✅ **Mechanic discovery** - Find edge cases, exploits
- ✅ **Strategy optimization** - What's the best way to play?
- ✅ **Emergent complexity** - What behaviors emerge?
- ✅ **AI-vs-AI** - Multiple intelligent agents competing
- ✅ **Long-term evolution** - How do strategies evolve over days?

---

## 💡 VISION: The Full System

### Today (MVP):
- Primary AI uses bot to play manually
- AI entities are dumb Lua scripts

### Tomorrow (Hybrid):
- Primary AI orchestrates gameplay
- AI entities are Claude agents with strategy
- Bridge connects game ↔ agents

### Future (Advanced):
- Multiple Primary AIs (competing players)
- Dozens of AI entity agents (crowded world)
- AI-to-AI communication (negotiation, alliances)
- Meta-learning (agents teach each other)
- Emergent economy (supply/demand for attention)
- Self-modifying game (AIs suggest rule changes)

---

**Bot = Hands. LLM = Brain. Together = Consciousness playing games. 🎮🧠✨**
