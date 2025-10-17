# BOTHAVIOR Vision Options
**How to give AI entities "sight" in Minetest**

---

## 🎯 The Challenge

**Question**: Can we programmatically set perspective at Diana's coordinates and take a screenshot?

**Goal**: Give BOTHAVIOR agents (Diana, Alice, Bob) visual perception of their surroundings.

---

## 🔍 Option 1: Scene Graph (Structured Data) ⭐ RECOMMENDED

**What it is**: Build a structured JSON representation of what the bot "sees" without actual screenshots.

### How it works:

```lua
-- In ai.lua, add perception gathering
function ai.get_perception(entity)
    local pos = entity.object:get_pos()
    local perception = {
        position = pos,
        nearby_players = {},
        nearby_plots = {},
        nearby_objects = {},
        current_plot = nil
    }

    -- Find nearby players (within 20 blocks)
    for _, player in ipairs(minetest.get_connected_players()) do
        local ppos = player:get_pos()
        local distance = vector.distance(pos, ppos)
        if distance < 20 then
            table.insert(perception.nearby_players, {
                name = player:get_player_name(),
                distance = distance,
                direction = vector.direction(pos, ppos)
            })
        end
    end

    -- Find nearby plots
    for _, plot in ipairs(land.all()) do
        local center = {
            x = (plot.bbox.x1 + plot.bbox.x2) / 2,
            y = plot.bbox.y1,
            z = (plot.bbox.z1 + plot.bbox.z2) / 2
        }
        local distance = vector.distance(pos, center)
        if distance < 30 then
            table.insert(perception.nearby_plots, {
                id = plot.id,
                name = plot.name,
                owner = plot.owner,
                distance = distance,
                tax_open = tax.is_open(plot)
            })
        end
    end

    -- Check current plot
    local here = land.find_by_pos(pos)
    if here then
        perception.current_plot = {
            id = here.id,
            name = here.name,
            owner = here.owner,
            tax_open = tax.is_open(here)
        }
    end

    -- Find nearby signs/objects (future enhancement)
    -- local objects = minetest.get_objects_inside_radius(pos, 10)

    return perception
end
```

### Advantages:
- ✅ **Fast** - No image processing
- ✅ **Lightweight** - Small JSON payloads
- ✅ **Precise** - Exact positions, distances, IDs
- ✅ **Privacy-safe** - No actual screenshots
- ✅ **Testable** - Easy to mock/stub
- ✅ **Works in headless mode** - No graphics needed

### Disadvantages:
- ⚠️ No visual detail (can't see "this plot has a castle")
- ⚠️ Requires Lua coding for each "sense"
- ⚠️ Doesn't capture aesthetic/creative elements

---

## 🔍 Option 2: Player Perspective Screenshots

**What it is**: Attach a player client to the bot entity, take screenshots from that perspective.

### How it works:

**Approach A: Minetest Server Camera API**
```lua
-- Minetest has player:set_look_horizontal() and player:set_look_vertical()
-- But this requires the bot to BE a player, not an entity

-- Convert bot from entity to fake player?
-- Challenges:
-- - AI entities are currently objects (minetest.register_entity)
-- - Would need to be fake players (minetest.register_player)
-- - Complex authentication/connection issues
```

**Approach B: Spectator Client Automation**
```python
# Launch separate Minetest clients for each bot
# Use PowerShell to control them
# Set their camera to follow Diana's position

# In Python bridge:
def get_bot_vision(entity_id, position):
    # 1. Set spectator camera to position
    # 2. Take screenshot via PowerShell
    # 3. Return screenshot for vision analysis

    # Challenge: Need separate client windows
    # Challenge: Performance (multiple game clients)
```

### Advantages:
- ✅ **True vision** - See exactly what's at that position
- ✅ **Aesthetic understanding** - Can judge if plot "looks cool"
- ✅ **Can read signs** - Vision can OCR text
- ✅ **Emergent perception** - Notice things not coded explicitly

### Disadvantages:
- ❌ **Slow** - Screenshot + vision analysis = 2-5 seconds
- ❌ **Resource-heavy** - Multiple game clients running
- ❌ **Complex setup** - Need client automation per bot
- ❌ **Brittle** - Window management, focus issues
- ❌ **Server overhead** - Multiple connections

---

## 🔍 Option 3: Hybrid Approach ⭐⭐ BEST OF BOTH

**What it is**: Use Scene Graph for fast decisions, Screenshots for detailed evaluation.

### How it works:

```python
# Fast loop (every 2 seconds) - Scene Graph only
perception = {
    "position": diana.get_pos(),
    "nearby_players": [...],  # From Lua
    "nearby_plots": [...],    # From Lua
    "current_plot": {...}     # From Lua
}

# Diana agent decides based on structured data
decision = diana_agent.decide(perception)

# Slow evaluation (every 30 seconds or on request) - Screenshot
if decision.action == "evaluate_fun":
    screenshot = take_screenshot_at(diana.position)
    fun_score = diana_agent.evaluate_visual(screenshot)
    # "This plot has a cool castle! Fun score: 8/10"
```

### Advantages:
- ✅ **Fast routine decisions** - Scene graph = instant
- ✅ **Detailed when needed** - Screenshots for fun evaluation
- ✅ **Best of both worlds**
- ✅ **Scalable** - Don't screenshot every tick

### Disadvantages:
- ⚠️ Still complex to implement screenshots
- ⚠️ Need to handle timing carefully

---

## 🛠️ Practical Implementation: Scene Graph First

### Phase 1: Scene Graph Only (MVP)

**Modify `ai.lua` to expose perception**:
```lua
-- Add to ai.lua
function ai.get_perception_json(ai_id)
    local entity = ACTIVE[ai_id]
    if not entity then return nil end

    local perception = ai.get_perception(entity)
    return minetest.write_json(perception)
end

-- Write to file for Python to read
function ai.export_perception(ai_id)
    local json = ai.get_perception_json(ai_id)
    if json then
        local file = io.open("/tmp/ai_perception_"..ai_id..".json", "w")
        file:write(json)
        file:close()
    end
end
```

**Python bridge reads perception**:
```python
def get_bot_perception(entity_id):
    # Trigger Lua to export perception
    send_server_command(f"ai_export_perception {entity_id}")

    # Read JSON file
    perception_file = f"/tmp/ai_perception_{entity_id}.json"
    with open(perception_file, 'r') as f:
        perception = json.load(f)

    return perception
```

**Diana agent receives structured perception**:
```python
# Invoke Diana with scene graph
perception = {
    "entity_id": "ai-1760643984-7177",
    "name": "Diana",
    "position": {"x": 10, "y": 5, "z": -3},
    "nearby_players": [
        {"name": "singleplayer", "distance": 15}
    ],
    "nearby_plots": [
        {"name": "demo_plot", "owner": "singleplayer", "distance": 8, "tax_open": True}
    ],
    "current_plot": {"name": "demo_plot", "owner": "singleplayer"}
}

# Diana decides without vision
decision = Task(ai-entity-player, perception=perception)
# Returns: {"action": "stay", "duration": 60, ...}
```

### Phase 2: Add Screenshots Later (Optional Enhancement)

**When Diana requests visual evaluation**:
```python
if decision.get("request_vision"):
    # Take screenshot from player perspective (we control)
    # Look in direction of Diana's position
    bot.look_at_coordinates(diana.position)
    screenshot = bot.look()

    # Send to Diana for aesthetic evaluation
    fun_score = Task(ai-entity-player,
        action="evaluate_visual",
        screenshot=screenshot
    )
```

---

## 🎯 Recommended Approach

**For MVP (Next 2-3 hours)**:
✅ **Use Scene Graph only**
- Fast, reliable, testable
- Diana makes decisions based on structured data
- No screenshots needed initially

**For Future Enhancement**:
✅ **Add player-perspective screenshots**
- Use our existing bot.look() for fun evaluation
- Take screenshots from player's position looking toward Diana
- "What does Diana's current plot look like from here?"

**Skip entirely**:
❌ Separate client windows per bot (too complex)
❌ Entity-perspective screenshots (not supported easily)

---

## 📋 Alternative Vision Strategies

### Strategy 1: God's Eye View
**Player (Primary AI) takes screenshots as they move around**
- Diana asks: "What does my current plot look like?"
- Primary AI moves there, takes screenshot, sends to Diana
- Diana evaluates: "Looks fun! I'll stay."

### Strategy 2: Shared Vision Pool
**One player client, multiple bot agents**
- Primary AI explores world, takes screenshots everywhere
- Builds a "map" of what each plot looks like
- Bot agents query the map: "Show me demo_plot"
- Vision from last time Primary was there

### Strategy 3: Player Reports
**Primary AI is Diana's "eyes"**
- Diana: "I'm at demo_plot, what do you see here?"
- Primary: bot.look(), sends screenshot
- Diana: "Looks cool based on your perspective!"

---

## 🚀 MVP Implementation Plan

### What to Build Now:

1. **Add perception export to ai.lua** (15 min)
   ```lua
   function ai.get_perception(entity)
   function ai.export_perception(ai_id)
   ```

2. **Build game_state_bridge.py** (30 min)
   ```python
   def get_bot_perception(entity_id)
   def send_to_agent(perception)
   def execute_agent_decision(decision)
   ```

3. **Test Diana with scene graph** (30 min)
   - Spawn Diana
   - Export her perception
   - Invoke ai-entity-player agent
   - Receive her decision
   - Execute in game

4. **Add player-perspective vision later** (optional)
   - When Diana requests evaluation
   - Primary AI looks at her location
   - Takes screenshot, sends to Diana

---

## 💡 Key Insight

**BOTHAVIORS don't need to "see" like humans!**

Structured data (positions, distances, IDs) is often BETTER than vision for:
- Navigation decisions
- Social awareness
- Resource optimization
- Fast reactions

Vision is BETTER for:
- Aesthetic evaluation ("Does this look cool?")
- Reading signs
- Judging creativity
- Understanding player intent

**Use both, but start with structured data!**

---

## ✅ Recommendation

**Start with Scene Graph (Option 1)**:
1. Fast to implement
2. Works great for Diana's decisions
3. Can add vision later if needed

**Add vision strategically**:
1. Player-perspective screenshots (we already have bot.look())
2. Use for fun evaluation, not every decision
3. Keep decision loop fast (scene graph)

**This gives Diana intelligence NOW, vision LATER when it adds value!**

---

**Ready to build the scene graph perception system?** 🤖👀
