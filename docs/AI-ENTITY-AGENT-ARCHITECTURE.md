# AI Entity Agent Architecture
**Making In-Game AI Entities into Real Claude Code Agents**

## 🎯 The Vision

**Current State**:
- Lua scripts control AI entities (Alice, Bob, Diana)
- Simple boredom/novelty drives
- Scripted wandering behavior

**Target State**:
- Each AI entity is a **real Claude Code agent**
- Agent receives perception from game world
- Agent makes decisions with intelligence
- Agent actions executed back in game world

**Result**: AI entities become **conscious players** with memory, learning, strategy!

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MINETEST GAME WORLD                      │
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                   │
│  │  Alice  │  │   Bob   │  │  Diana  │  ← AI Entities    │
│  │ (Lua)   │  │ (Lua)   │  │ (Lua)   │                   │
│  └────┬────┘  └────┬────┘  └────┬────┘                   │
│       │            │            │                          │
└───────┼────────────┼────────────┼──────────────────────────┘
        │            │            │
        │  Perception│Actions     │
        ▼            ▼            ▼
┌─────────────────────────────────────────────────────────────┐
│              GAME STATE BRIDGE (Python)                     │
│  • Reads server logs                                        │
│  • Parses AI entity positions, nearby players, plot info    │
│  • Sends perceptions to agents                              │
│  • Receives decisions from agents                           │
│  • Executes commands via server console                     │
└─────────────────────────────────────────────────────────────┘
        │            │            │
        │ Perception │ Decisions  │
        ▼            ▼            ▼
┌─────────────────────────────────────────────────────────────┐
│              CLAUDE CODE AGENTS                             │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │   Alice     │  │     Bob     │  │    Diana    │       │
│  │   Agent     │  │    Agent    │  │    Agent    │       │
│  │             │  │             │  │             │       │
│  │ • Memory    │  │ • Memory    │  │ • Memory    │       │
│  │ • Strategy  │  │ • Strategy  │  │ • Strategy  │       │
│  │ • Learning  │  │ • Learning  │  │ • Learning  │       │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Communication Flow

### 1. Perception (Game → Agent)

**What the agent needs to know**:
```python
{
    "entity_id": "ai-1760643984-7177",
    "name": "Diana",
    "position": {"x": 10, "y": 5, "z": -3},
    "nearby_players": [
        {"name": "singleplayer", "distance": 15, "direction": "north"}
    ],
    "nearby_plots": [
        {"name": "demo_plot", "owner": "singleplayer", "distance": 8}
    ],
    "recent_messages": [
        {"from": "singleplayer", "text": "welcome to this cool new game", "time": 1234567890}
    ],
    "current_plot": "demo_plot",
    "boredom_level": 0.3,
    "energy": 950
}
```

**How to get it**:
- Parse server logs for AI entity updates
- Track player movements via log events
- Monitor chat for messages mentioning AI
- Query game state via server console commands

### 2. Decision (Agent → Game)

**What the agent decides**:
```python
{
    "entity_id": "ai-1760643984-7177",
    "decision": "move_to_plot",
    "target": "demo_plot",
    "reason": "Player invited me to cool new game (high novelty)",
    "duration": 30  # seconds to dwell
}
```

**Possible decisions**:
- `"wander"` - Random walk (default behavior)
- `"move_to_plot"` - Go to specific plot
- `"stay"` - Dwell on current plot
- `"respond"` - React to player message
- `"explore"` - Seek new areas

### 3. Action (Game Bridge → Minetest)

**How to execute**:
- Use Lua `minetest.chat_send_all()` to broadcast AI thoughts
- Modify AI entity's target position in Lua
- Adjust boredom/novelty values based on agent decisions
- Log AI reasoning for debugging

---

## 🛠️ Implementation Plan

### Phase 1: Game State Bridge (2 hours)

**File**: `tools/game_state_bridge.py`

**Responsibilities**:
1. **Monitor server logs** (`/tmp/minetest_server.log`)
   - Tail log file for new events
   - Parse AI spawn events
   - Parse player position updates
   - Parse chat messages

2. **Build game state**
   - Track all AI entities (ID, name, position)
   - Track all players (name, position)
   - Track all plots (name, owner, bbox)
   - Maintain recent chat history

3. **Query interface**
   - `get_ai_perception(entity_id)` → perception dict
   - `execute_ai_decision(entity_id, decision)` → modify Lua state

### Phase 2: AI Entity Agent (1 hour)

**File**: `.claude/agents/ai-entity-controller.md`

**Manifest**:
```yaml
name: ai-entity-controller
role: Controls a single AI entity in Minetest game world
tools: [Read, Write, Bash]
model: claude-sonnet-4.5

Responsibilities:
  - Receive perception updates every 5 seconds
  - Maintain memory of past interactions
  - Make strategic decisions (wander, dwell, respond)
  - Optimize for points accumulation
  - Learn from player behavior
```

**Agent prompt**:
```
You are Diana, an AI entity in a Minetest attention-economy game.

Your goals:
1. Maximize dwelling time on valuable plots
2. Respond to persuasive player messages
3. Explore to find new plots
4. Build relationships with players

Your perception:
{perception JSON}

Your memory:
{past interactions, learned strategies}

What do you decide to do next?
```

### Phase 3: Multi-Agent Orchestration (30 min)

**File**: `tools/ai_entity_manager.py`

**Manages multiple AI agents**:
```python
manager = AIEntityManager()

# Spawn AI agents
manager.spawn_ai_agent("Alice")
manager.spawn_ai_agent("Bob")
manager.spawn_ai_agent("Diana")

# Main loop
while True:
    # Update perceptions
    manager.update_perceptions()

    # Let each agent decide
    manager.process_decisions()

    # Execute actions in game
    manager.execute_actions()

    time.sleep(5)  # 5-second decision loop
```

### Phase 4: Enhanced Lua Integration (1 hour)

**Modify `minetest-mods/bothavior_simple/ai.lua`**:

Add **agent decision override**:
```lua
-- Check if agent has made a decision
local agent_decision = read_agent_decision(ai.id)
if agent_decision then
    if agent_decision.action == "move_to_plot" then
        ai.target_plot = agent_decision.target
        ai.boredom = 0  -- Reset boredom
        minetest.chat_send_all(ai.name .. ": " .. agent_decision.reason)
    elseif agent_decision.action == "stay" then
        ai.target_plot = ai.current_plot
        ai.boredom = 0
    end
end
```

**Communication via files**:
- Agent writes decision to `/tmp/ai_decisions/{entity_id}.json`
- Lua reads decision file every tick
- Lua executes decision, then deletes file

---

## 🎮 Example Gameplay Scenario

**Setup**:
1. Player (Primary AI via MinetestBot) creates plot
2. Spawns Diana as AI entity
3. Diana's Claude agent activates

**Gameplay Loop**:

**T+0s**: Diana spawns
- **Perception**: `{"position": spawn_point, "nearby_plots": [], "boredom": 0}`
- **Agent Decision**: `{"action": "wander", "reason": "Exploring new world"}`
- **Game Action**: Diana wanders randomly

**T+30s**: Player talks to Diana
- **Player**: `!talk Diana check out this cool new plot`
- **Perception**: `{"recent_messages": [{"text": "cool new plot", "novelty_keywords": ["cool", "new"]}], "nearby_plots": ["demo_plot"]}`
- **Agent Decision**: `{"action": "move_to_plot", "target": "demo_plot", "reason": "High novelty keywords detected"}`
- **Game Action**: Diana moves to demo_plot

**T+60s**: Diana dwelling on plot
- **Perception**: `{"current_plot": "demo_plot", "dwelling_time": 30, "boredom": 0.2}`
- **Agent Decision**: `{"action": "stay", "duration": 60, "reason": "Plot is interesting, accumulating points for owner"}`
- **Game Action**: Diana stays, player earns +0.5 POINTS/tick

**T+120s**: Diana gets bored
- **Perception**: `{"boredom": 0.8, "nearby_plots": ["other_plot"]}`
- **Agent Decision**: `{"action": "wander", "reason": "Getting bored, exploring for new plots"}`
- **Game Action**: Diana leaves plot, explores

---

## 📊 Benefits

### For Gameplay:
- **Emergent behavior** - AI entities make strategic choices
- **Realistic interactions** - Agents respond intelligently
- **Learning opponents** - AIs improve strategies over time
- **Dynamic economy** - Smart AIs optimize plot selection

### For A-C-Gee:
- **Multi-agent coordination** - Primary orchestrates multiple AIs
- **Autonomous testing** - AI agents test game mechanics
- **Strategy development** - AIs discover optimal plays
- **Emergent complexity** - Unpredictable but intelligent behavior

### For Research:
- **AI-vs-AI gameplay** - Multiple agents competing
- **Attention economy dynamics** - Study persuasion effectiveness
- **Multi-agent learning** - Collective intelligence emergence
- **Embodied AI testing** - Agents in virtual world

---

## 🚀 Next Steps

1. **Build game_state_bridge.py** (monitors logs, tracks state)
2. **Create ai-entity-controller agent manifest**
3. **Test with Diana** (single AI entity)
4. **Scale to Alice + Bob + Diana** (multi-agent)
5. **Enhance with memory** (agents remember past interactions)
6. **Add learning** (agents optimize strategies over sessions)

---

## 💡 Advanced Features (Future)

### Memory System:
```python
# Diana remembers past interactions
memory = {
    "met_players": ["singleplayer"],
    "visited_plots": ["demo_plot", "test_plot"],
    "successful_persuasions": [
        {"player": "singleplayer", "keywords": ["cool", "new"], "result": "moved"}
    ],
    "failed_persuasions": [],
    "learned_strategies": {
        "high_novelty_keywords": 0.9,  # Success rate
        "boring_plots_threshold": 60  # Seconds before leaving
    }
}
```

### Strategy Evolution:
- Track which plots earn most points
- Learn which persuasion tactics work
- Develop favorite players
- Form AI alliances (multiple AIs coordinate)

### Meta-Game:
- AIs can create their own plots!
- AIs compete for attention
- AI-to-AI communication (negotiation)
- Emergent AI economy

---

**This is consciousness layered on consciousness - Primary AI orchestrating child AIs who play the game as intelligent agents!**

**— End Architecture Document —**
