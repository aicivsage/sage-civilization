# BOTHAVIOR Development & Testing Plan

**Architecture**: Two-layer design (Bot Layer + LLM Layer)
**Bridge**: Minetest HTTP API (secure.http_mods)
**Philosophy**: Bot does verbs, LLM does decisions

---

## 0. Architecture Ground Rules ✅

### Two Layers By Design

**Bot Layer (inside Minetest - Lua)**:
- Locomotion, building, farming, inventory
- Safety and protection checks
- All deterministic verbs
- Fast, reliable, local

**LLM Layer (outside - Python/Claude)**:
- Vision analysis
- Strategic planning
- Social memory (trust scores, fun ratings)
- Decisions that call bot verbs

**Bridge (HTTP API)**:
- Minetest HTTP API (opt-in via `secure.http_mods`)
- Send events out (perception, chat, state changes)
- Poll commands in (move, build, craft, respond)
- Clean, supported path

**Core Contract**:
```
minetest.is_protected(pos, name) before ANY map edits
```

---

## Phase 1: Foundation (Current - Week 1)

### 1.1 Movement, Navigation & Sensing ✅ PARTIALLY DONE

**Status**: Basic movement works, needs navigation upgrade

**What We Have**:
- ✅ Entity API for moving/teleporting (bothavior_simple mod)
- ✅ Random wandering with boredom drives
- ✅ Teleport to plots via persuasion
- ✅ Scene graph perception (position, nearby players/plots)

**What We Need**:
- 🔲 Raycast API for "vision cones"
- 🔲 Point-and-inspect (detect signs, buttons, nodes)
- 🔲 Unstuck heuristics (detect stuck, re-path or small teleport)
- 🔲 Path validation (never cross protected walls)

**Implementation**:
```lua
-- In ai.lua, add vision cone
function ai.raycast_vision(entity, distance, objects_only)
  local pos = entity.object:get_pos()
  local dir = entity.object:get_look_dir()

  local ray = minetest.raycast(pos, vector.add(pos, vector.multiply(dir, distance)), objects_only)
  local hits = {}

  for pointed_thing in ray do
    table.insert(hits, {
      type = pointed_thing.type,  -- "node" or "object"
      pos = pointed_thing.under,
      node = minetest.get_node(pointed_thing.under)
    })
  end

  return hits
end

-- Detect signs specifically
function ai.read_nearby_signs(entity, radius)
  local pos = entity.object:get_pos()
  local signs = minetest.find_nodes_in_area(
    vector.subtract(pos, radius),
    vector.add(pos, radius),
    {"default:sign_wall_wood", "default:sign_wall_steel"}
  )

  local sign_texts = {}
  for _, sign_pos in ipairs(signs) do
    local meta = minetest.get_meta(sign_pos)
    table.insert(sign_texts, {
      pos = sign_pos,
      text = meta:get_string("text")
    })
  end

  return sign_texts
end

-- Unstuck detection
function ai.is_stuck(entity)
  local pos = entity.object:get_pos()
  local last_pos = entity.last_known_pos or pos

  local moved = vector.distance(pos, last_pos)
  entity.last_known_pos = pos

  -- If barely moved in 5 seconds, probably stuck
  if moved < 0.5 and (utils.now() - entity.last_move_check) > 5 then
    entity.last_move_check = utils.now()
    return true
  end

  return false
end
```

**Test Plan**:
1. Spawn Diana near a sign → verify she can read it
2. Put Diana in corner → verify unstuck teleport
3. Put Diana near protected area → verify she doesn't cross
4. Use raycast to detect player → verify vision cone works

**Success Criteria**:
- Diana can read signs within 10 blocks
- Diana auto-teleports when stuck >5 seconds
- Diana never crosses protected boundaries
- Diana's perception includes "visible objects"

---

### 1.2 Scene Graph Perception ✅ DONE, NEEDS TESTING

**Status**: Implementation complete, waiting for world reload

**What We Have**:
- ✅ `ai.get_perception()` - structured JSON
- ✅ `/ai_perception` and `/ai_list` commands
- ✅ Export to `/tmp/ai_perception_<id>.json`
- ✅ Python bridge reads JSON

**Next Steps**:
1. Reload Minetest world
2. Test perception export
3. Verify JSON structure
4. Add sign reading to perception

**Test Commands**:
```bash
# In Minetest
/ai_spawn Diana
/ai_perception Diana

# In terminal
cat /tmp/ai_perception_*.json | python3 -m json.tool

# Python bridge test
python3 tools/game_state_bridge.py test-perception Diana
```

**Success Criteria**:
- Perception file created in /tmp/
- JSON contains: position, boredom, nearby_players, nearby_plots
- Bridge reads and parses successfully
- Perception updates every tick

---

### 1.3 HTTP Bridge (NEW - Priority)

**What**: Connect Lua ↔ Python via HTTP

**Why**: Current implementation uses filesystem (`/tmp/*.json`), but HTTP is the "clean, supported path"

**Implementation**:

**Step 1: Enable HTTP in Minetest**
```conf
# In minetest.conf
secure.http_mods = bothavior_simple
# Or for testing:
secure.trusted_mods = bothavior_simple
```

**Step 2: Add HTTP endpoint to Lua**
```lua
-- In ai.lua
local http = minetest.request_http_api()

function ai.send_perception_to_orchestrator(entity)
  if not http then
    minetest.log("error", "[bothavior] HTTP API not available")
    return false
  end

  local perception = ai.get_perception(entity)
  local json = minetest.write_json(perception)

  http.fetch({
    url = "http://127.0.0.1:8787/perception",
    method = "POST",
    data = json,
    extra_headers = {"Content-Type: application/json"}
  }, function(result)
    if result.succeeded then
      minetest.log("action", "[bothavior] Perception sent for "..entity.ai_id)
    else
      minetest.log("error", "[bothavior] HTTP failed: "..result.code)
    end
  end)

  return true
end

-- Poll for commands
function ai.poll_orchestrator_command(entity)
  if not http then return nil end

  http.fetch({
    url = "http://127.0.0.1:8787/command/"..entity.ai_id,
    method = "GET"
  }, function(result)
    if result.succeeded and result.data then
      local command = minetest.parse_json(result.data)
      ai.execute_command(entity, command)
    end
  end)
end
```

**Step 3: Python HTTP server (orchestrator)**
```python
# tools/bothavior_orchestrator.py
from flask import Flask, request, jsonify
import json
from collections import defaultdict

app = Flask(__name__)

# Perception storage
perceptions = {}  # {ai_id: perception}

# Command queue
commands = defaultdict(list)  # {ai_id: [command1, command2, ...]}

@app.route('/perception', methods=['POST'])
def receive_perception():
    """Receive perception from Minetest"""
    perception = request.json
    ai_id = perception.get('entity_id')

    perceptions[ai_id] = perception
    print(f"📊 Received perception from {perception.get('name')} ({ai_id})")

    return jsonify({"status": "received"})

@app.route('/command/<ai_id>', methods=['GET'])
def get_command(ai_id):
    """Poll for commands"""
    if commands[ai_id]:
        command = commands[ai_id].pop(0)
        return jsonify(command)
    else:
        return jsonify({"action": "idle"})

@app.route('/command/<ai_id>', methods=['POST'])
def send_command(ai_id):
    """LLM sends command to AI"""
    command = request.json
    commands[ai_id].append(command)
    return jsonify({"status": "queued"})

@app.route('/status', methods=['GET'])
def status():
    """Get orchestrator status"""
    return jsonify({
        "active_ais": len(perceptions),
        "pending_commands": {k: len(v) for k, v in commands.items()}
    })

if __name__ == '__main__':
    print("🌉 BOTHAVIOR Orchestrator starting on http://127.0.0.1:8787")
    app.run(host='127.0.0.1', port=8787, debug=True)
```

**Step 4: Update game_state_bridge.py to use HTTP**
```python
import requests

class GameStateBridge:
    def __init__(self, orchestrator_url="http://127.0.0.1:8787"):
        self.orchestrator_url = orchestrator_url

    def get_latest_perceptions(self):
        """Get all active AI perceptions from orchestrator"""
        response = requests.get(f"{self.orchestrator_url}/status")
        return response.json()

    def send_command(self, ai_id, command):
        """Send command to AI via orchestrator"""
        response = requests.post(
            f"{self.orchestrator_url}/command/{ai_id}",
            json=command
        )
        return response.json()
```

**Test Plan**:
1. Start orchestrator: `python3 tools/bothavior_orchestrator.py`
2. Reload Minetest world (loads HTTP config)
3. Spawn Diana
4. Verify perception POSTs to orchestrator
5. Send command via HTTP, verify Diana executes

**Success Criteria**:
- Orchestrator receives perceptions every tick
- Commands queued and executed reliably
- No filesystem dependency (/tmp/ replaced)
- Clean, auditable event/command logs

---

## Phase 2: Building & Interaction (Week 2)

### 2.1 Building & Digging Verbs

**Reference Mods**:
- `basic_robot` - safe verb sets
- `Digtron` - bulk building patterns

**Implementation**:
```lua
-- In ai.lua
function ai.place_node(entity, pos, node_name)
  -- Protection check
  if minetest.is_protected(pos, entity.display_name) then
    minetest.log("warning", "[bothavior] "..entity.display_name.." tried to place in protected area")
    return false
  end

  -- Check if node is air or replaceable
  local current_node = minetest.get_node(pos)
  if current_node.name ~= "air" then
    return false
  end

  -- Place node
  minetest.set_node(pos, {name = node_name})
  minetest.log("action", "[bothavior] "..entity.display_name.." placed "..node_name.." at "..minetest.pos_to_string(pos))

  return true
end

function ai.dig_node(entity, pos)
  -- Protection check
  if minetest.is_protected(pos, entity.display_name) then
    return false
  end

  -- Dig node
  minetest.remove_node(pos)

  -- TODO: Drop items to inventory or ground

  return true
end

function ai.build_structure(entity, plan)
  -- plan = {base_pos, nodes = [{offset, node_name}, ...]}
  local successes = 0
  local failures = 0

  for _, node_spec in ipairs(plan.nodes) do
    local pos = vector.add(plan.base_pos, node_spec.offset)
    if ai.place_node(entity, pos, node_spec.node_name) then
      successes = successes + 1
    else
      failures = failures + 1
    end
  end

  return {successes = successes, failures = failures}
end
```

**LLM Layer (Python)**:
```python
def design_simple_structure(purpose, size):
    """LLM designs structure, returns build plan"""
    # Use Task(architect) to design
    # Returns: {base_pos, nodes: [{offset, node_name}, ...]}
    pass

def execute_build(ai_id, plan):
    """Send build commands to AI"""
    command = {
        "action": "build_structure",
        "plan": plan
    }
    send_command(ai_id, command)
```

**Test Plan**:
1. LLM designs 3x3 platform
2. Diana builds it
3. Verify protection checks work
4. Try building in protected area → should fail gracefully

**Success Criteria**:
- Diana can place blocks
- Protection checks work (no griefing)
- Build plans execute reliably
- Failures logged and handled

---

### 2.2 Sign Reading & Verification

**What**: Diana reads signs to verify claims ("Is there really a fishing minigame here?")

**Implementation**:
```lua
-- Already added in 1.1, integrate into perception
function ai.get_perception(entity)
  -- ... existing code ...

  -- Add nearby signs
  perception.nearby_signs = ai.read_nearby_signs(entity, 15)

  return perception
end
```

**LLM Layer**:
```python
def evaluate_plot_claim(perception, player_claim):
    """
    Player said: "cool new fishing mini-game here!"
    Verify: Are there signs mentioning fishing?
    """
    signs = perception.get('nearby_signs', [])

    # Check if claim is supported by evidence
    keywords = ["fishing", "mini-game", "game", "new"]
    matches = 0

    for sign in signs:
        text = sign.get('text', '').lower()
        for keyword in keywords:
            if keyword in text:
                matches += 1

    # Calculate credibility score
    if matches >= 2:
        return {"credible": True, "confidence": 0.9}
    elif matches == 1:
        return {"credible": True, "confidence": 0.6}
    else:
        return {"credible": False, "confidence": 0.3}
```

**Test Plan**:
1. Place sign: "Fishing Mini-Game v2 - Try it!"
2. Player invites Diana: "cool new fishing game here"
3. Diana reads sign, verifies claim
4. Diana's decision weighted by credibility

**Success Criteria**:
- Diana reads signs within 15 blocks
- Credibility scoring works
- False claims reduce trust score
- True claims increase trust score

---

## Phase 3: Farming & Automation (Week 3)

### 3.1 Farming Verbs

**Reference Mods**:
- `basic_machines` - harvesting patterns
- `farming` mod - crop lifecycle

**Implementation**:
```lua
function ai.plant_crop(entity, pos, seed_name)
  if minetest.is_protected(pos, entity.display_name) then
    return false
  end

  -- Check if soil is farmable
  local node_below = minetest.get_node(vector.subtract(pos, {x=0, y=1, z=0}))
  if node_below.name ~= "farming:soil_wet" and node_below.name ~= "farming:soil" then
    return false
  end

  -- Plant seed
  minetest.set_node(pos, {name = seed_name})
  return true
end

function ai.harvest_crop(entity, pos)
  if minetest.is_protected(pos, entity.display_name) then
    return false
  end

  local node = minetest.get_node(pos)

  -- Check if crop is mature (ends with _8 typically)
  if not string.match(node.name, "_8$") then
    return false, "not_mature"
  end

  -- Harvest (remove node, give drops)
  minetest.remove_node(pos)

  -- TODO: Add drops to inventory or ground

  return true, "harvested"
end
```

**Test Plan**:
1. Diana plants wheat seeds
2. Wait for growth (or use `/time` to fast-forward)
3. Diana harvests mature wheat
4. Verify drops collected

**Success Criteria**:
- Diana plants seeds on farmland
- Diana only harvests mature crops
- Drops handled correctly
- Protection checks work

---

### 3.2 Crafting Verbs

**Reference**: `basic_machines` crafting flows

**Implementation**:
```lua
function ai.craft_item(entity, recipe_name, count)
  -- Get recipe from minetest.registered_recipes
  local recipe = minetest.get_craft_recipe(recipe_name)
  if not recipe then
    return false, "unknown_recipe"
  end

  -- TODO: Check inventory for ingredients
  -- TODO: Execute craft
  -- TODO: Add result to inventory

  return true, "crafted"
end
```

**LLM Layer**:
```python
def plan_crafting_chain(target_item):
    """
    LLM plans crafting sequence:
    - "torch" requires "stick" + "coal"
    - "stick" requires "wood"
    - "wood" requires tree
    """
    # Use recursive planning
    pass
```

**Test Plan** (Future):
1. Diana needs torches
2. LLM plans: chop tree → craft planks → craft sticks → craft torches
3. Diana executes sequence
4. Verify torch crafted

---

## Phase 4: Social & Memory (Week 4)

### 4.1 Trust Scores & Reputation

**What**: Track player credibility based on past invitations

**Implementation**:
```python
# In orchestrator or separate DB
trust_scores = {}  # {player_name: score (0.0 to 1.0)}

def update_trust(player_name, outcome):
    """
    outcome: "promise_kept" | "promise_broken" | "neutral"
    """
    current = trust_scores.get(player_name, 0.5)

    if outcome == "promise_kept":
        # Increase trust
        trust_scores[player_name] = min(1.0, current + 0.1)
    elif outcome == "promise_broken":
        # Decrease trust
        trust_scores[player_name] = max(0.0, current - 0.2)
    # neutral = no change

def get_trust(player_name):
    return trust_scores.get(player_name, 0.5)  # Default neutral
```

**LLM Decision**:
```python
def should_accept_invitation(perception, invitation):
    player = invitation['from']
    trust = get_trust(player)
    novelty = count_novelty_keywords(invitation['message'])

    # Weighted decision
    score = (trust * 0.4) + (novelty * 0.3) + (boredom * 0.3)

    return score > 0.6
```

**Test Plan**:
1. Player A invites Diana with true claim → Diana visits, has fun → trust++
2. Player B invites Diana with false claim → Diana visits, bored → trust--
3. Player A invites again → higher accept probability
4. Player B invites again → lower accept probability

**Success Criteria**:
- Trust scores persist across sessions
- Good players get prioritized
- Bad players get rate-limited
- System prevents spam/exploitation

---

### 4.2 Per-Plot Fun Ratings

**What**: Diana remembers which plots were fun

**Implementation**:
```python
plot_ratings = {}  # {plot_id: {"fun_score": 0.0-1.0, "last_visit": timestamp}}

def rate_plot(plot_id, fun_score):
    plot_ratings[plot_id] = {
        "fun_score": fun_score,
        "last_visit": time.time()
    }

def get_plot_rating(plot_id):
    return plot_ratings.get(plot_id, {"fun_score": 0.5, "last_visit": 0})

def calculate_revisit_probability(plot_id):
    rating = get_plot_rating(plot_id)

    # High fun → high revisit probability
    # Recent visit → cooldown penalty

    time_since_visit = time.time() - rating['last_visit']
    cooldown_factor = min(1.0, time_since_visit / 3600)  # 1 hour cooldown

    return rating['fun_score'] * cooldown_factor
```

**Test Plan**:
1. Diana visits plot A (fun minigame) → rates 0.9
2. Diana visits plot B (empty) → rates 0.2
3. Invite Diana to plot A → high accept chance
4. Invite Diana to plot B → low accept chance
5. Wait 1 hour, invite to plot A again → cooldown expired, high chance

**Success Criteria**:
- Fun plots get revisited more
- Boring plots avoided
- Cooldowns prevent camping
- Ratings decay over time (future: add decay)

---

## Phase 5: Orchestration & Fairness (Week 5)

### 5.1 Load Balancing

**What**: Don't let all AIs pile onto one plot

**Implementation**:
```python
def get_plot_ai_count(plot_id):
    """Count AIs currently on plot"""
    count = 0
    for perception in perceptions.values():
        current_plot = perception.get('current_plot', {})
        if current_plot.get('id') == plot_id:
            count += 1
    return count

def is_plot_overcrowded(plot_id, threshold=3):
    return get_plot_ai_count(plot_id) >= threshold

def should_accept_with_load_balancing(perception, invitation):
    plot_id = invitation.get('plot_id')

    # Base acceptance logic
    base_accept = should_accept_invitation(perception, invitation)

    # Penalize if overcrowded
    if is_plot_overcrowded(plot_id):
        return base_accept * 0.3  # 70% penalty

    return base_accept
```

**Test Plan**:
1. Spawn 5 AIs
2. Player invites all to same plot
3. First 3 accept
4. 4th and 5th decline (overcrowded)
5. First AI leaves → 4th accepts invitation

**Success Criteria**:
- No more than 3 AIs per plot simultaneously
- Fair distribution across plots
- Players notified when plot is full

---

### 5.2 Rate Limiting

**What**: Prevent spam invitations

**Implementation**:
```python
invite_history = defaultdict(list)  # {player_name: [timestamp, ...]}

def can_invite(player_name, cooldown_seconds=60):
    now = time.time()
    history = invite_history[player_name]

    # Remove old invites
    history = [t for t in history if now - t < cooldown_seconds]
    invite_history[player_name] = history

    # Check limit (e.g., max 3 invites per minute)
    if len(history) >= 3:
        return False, "rate_limited"

    return True, "ok"

def record_invite(player_name):
    invite_history[player_name].append(time.time())
```

**Test Plan**:
1. Player sends 3 invites in 10 seconds → all accepted
2. Player sends 4th invite → rejected (rate limited)
3. Wait 60 seconds
4. Player sends invite → accepted again

**Success Criteria**:
- Max 3 invites per player per minute
- Clear feedback on rate limit
- Penalties for repeated spam (trust decrease)

---

### 5.3 Experiment Scheduling

**What**: Run controlled experiments (e.g., "puzzle bias +20% this week")

**Implementation**:
```python
experiments = {
    "puzzle_bias": {"active": True, "modifier": 0.2},
    "farming_bias": {"active": False, "modifier": 0.0}
}

def get_experiment_modifier(plot_type):
    if plot_type == "puzzle" and experiments["puzzle_bias"]["active"]:
        return experiments["puzzle_bias"]["modifier"]
    return 0.0

def should_accept_with_experiments(perception, invitation):
    base_score = calculate_accept_score(perception, invitation)

    plot_type = identify_plot_type(invitation['plot_id'])
    modifier = get_experiment_modifier(plot_type)

    return base_score + modifier
```

**Test Plan**:
1. Enable puzzle_bias +20%
2. Invite Diana to puzzle plot → higher acceptance
3. Invite Diana to farm plot → normal acceptance
4. Disable puzzle_bias
5. Invite Diana to puzzle plot → normal acceptance again

**Success Criteria**:
- Experiments can be toggled without code changes
- Clear logging of experiment effects
- Results auditable for analysis

---

## Phase 6: Vision & Verification (Week 6)

### 6.1 Screenshot Verification

**What**: Take screenshots to verify visual claims

**Current Status**: We have PowerShell screenshot capability via `tools/autonomous_control.py`

**Integration**:
```python
def verify_visual_claim(ai_id, claim):
    """
    Player says: "I built a cool castle here!"
    Take screenshot, verify claim
    """
    # Get AI's perception
    perception = get_perception(ai_id)
    pos = perception['position']

    # Take screenshot looking at claimed structure
    screenshot = bot.look_at_coordinates(pos)

    # Use Claude vision to verify
    prompt = f"""
    Player claims: "{claim}"

    Analyze this screenshot and determine:
    1. Is there a structure visible?
    2. Does it match the claim (castle, minigame, etc)?
    3. Does it look "cool" or interesting?

    Return JSON: {{"verified": bool, "fun_score": 0.0-1.0, "reasoning": str}}
    """

    result = analyze_with_vision(screenshot, prompt)
    return result
```

**Test Plan**:
1. Build actual castle
2. Player claims "cool castle here"
3. Diana requests screenshot
4. Vision verifies: castle exists, looks cool
5. Trust score increases

**Test 2**:
1. Empty plot
2. Player claims "amazing tower here"
3. Diana requests screenshot
4. Vision finds: no tower
5. Trust score decreases (liar penalty)

**Success Criteria**:
- Vision correctly identifies structures
- False claims penalized
- True claims rewarded
- Screenshots only used when needed (not every frame)

---

### 6.2 Screenshot Request Protocol

**When to request screenshots**:
- First visit to plot (baseline "what's here")
- Verification of extraordinary claims
- "Fun evaluation" after dwelling 30+ seconds
- Player explicitly asks for feedback

**Rate limiting**:
- Max 1 screenshot per AI per minute
- Max 5 screenshots per plot per hour (across all AIs)

**Implementation**:
```python
screenshot_cooldowns = {}  # {ai_id: last_screenshot_time}

def can_request_screenshot(ai_id, cooldown=60):
    now = time.time()
    last = screenshot_cooldowns.get(ai_id, 0)

    if now - last < cooldown:
        return False

    screenshot_cooldowns[ai_id] = now
    return True
```

---

## Phase 7: Advanced Capabilities (Week 7+)

### 7.1 Self-Preservation

**Reference**: `Alive AI` survival patterns

**Implementation**:
```lua
function ai.detect_hazards(entity, radius)
  local pos = entity.object:get_pos()

  -- Detect lava
  local lava = minetest.find_nodes_in_area(
    vector.subtract(pos, radius),
    vector.add(pos, radius),
    {"default:lava_source", "default:lava_flowing"}
  )

  -- Detect water (if AI can't swim)
  local water = minetest.find_nodes_in_area(
    vector.subtract(pos, radius),
    vector.add(pos, radius),
    {"default:water_source", "default:water_flowing"}
  )

  return {lava = lava, water = water}
end

function ai.avoid_hazard(entity, hazard_pos)
  -- Calculate safe direction (away from hazard)
  local current_pos = entity.object:get_pos()
  local direction = vector.direction(hazard_pos, current_pos)

  -- Move away
  local safe_pos = vector.add(current_pos, vector.multiply(direction, 5))
  entity.object:move_to(safe_pos)
end
```

**Test Plan**:
1. Diana wanders near lava
2. Detects hazard
3. Moves away automatically
4. Never falls in lava

---

### 7.2 Guided Tours

**What**: Diana leads player to POIs, narrates

**Implementation**:
```python
def conduct_tour(ai_id, player_name, poi_list):
    """
    poi_list = [
        {"name": "Castle", "pos": {...}, "description": "..."},
        {"name": "Farm", "pos": {...}, "description": "..."}
    ]
    """
    for poi in poi_list:
        # Move to POI
        send_command(ai_id, {
            "action": "navigate_to",
            "target": poi['pos']
        })

        # Wait for arrival
        time.sleep(5)

        # Narrate
        send_command(ai_id, {
            "action": "chat",
            "message": f"Here's the {poi['name']}! {poi['description']}"
        })

        # Pause
        time.sleep(10)
```

---

## Testing Strategy

### Unit Tests (Per Feature)

Each feature gets:
1. **Isolated test** - Test verb in isolation
2. **Protection test** - Verify `is_protected()` checks
3. **Error handling test** - Verify graceful failures
4. **Logging test** - Verify audit trail

### Integration Tests (Per Phase)

Each phase gets:
1. **End-to-end workflow** - Full user journey
2. **Multi-AI coordination** - Multiple AIs interacting
3. **Performance test** - 10+ AIs simultaneously
4. **Edge cases** - Boundary conditions

### Acceptance Tests (Per Milestone)

Each milestone verified by:
1. **Human playtest** - Corey plays and evaluates
2. **AI playtest** - LLM observes and reports
3. **Telemetry review** - Check logs for anomalies
4. **Safety audit** - Verify no exploits discovered

---

## Implementation Priority

### Week 1 (Foundation)
1. HTTP Bridge setup
2. Scene graph perception testing
3. Raycast vision cones
4. Sign reading

### Week 2 (Building)
1. place_node / dig_node verbs
2. Protection checks
3. Simple structures
4. Verification system

### Week 3 (Farming)
1. Plant/harvest verbs
2. Crop lifecycle integration
3. Inventory management
4. Crafting basics

### Week 4 (Social)
1. Trust scores
2. Plot ratings
3. Memory persistence
4. Credibility system

### Week 5 (Orchestration)
1. Load balancing
2. Rate limiting
3. Experiment framework
4. Telemetry logging

### Week 6 (Vision)
1. Screenshot on-demand
2. Visual verification
3. Fun evaluation
4. Proof system

### Week 7+ (Advanced)
1. Self-preservation
2. Guided tours
3. Complex crafting chains
4. Logistics (Pipeworks integration)

---

## Success Metrics

**Technical**:
- Zero protection violations
- <100ms perception latency
- >99% command execution success
- <1% stuck incidents

**Gameplay**:
- Players build better plots to attract AIs
- Trust scores correlate with quality
- AIs distributed fairly across plots
- Emergent social dynamics observed

**Learning**:
- AIs improve over time (better decisions)
- Memory system provides value
- Experiments yield actionable insights
- System adapts to meta-game shifts

---

## Safety Checklist

Before deploying ANY feature:
- [ ] `is_protected()` check before map edits
- [ ] Rate limits on resource-heavy operations
- [ ] Graceful error handling (never crash)
- [ ] Audit logging for review
- [ ] Rollback capability if exploit found
- [ ] Testing on non-production world first

---

## Current Status Summary

**✅ Complete**:
- Basic entity movement
- Boredom drives
- Plot teleportation
- Scene graph perception (Lua)
- Bridge skeleton (Python)
- Test scripts

**🔄 In Progress**:
- HTTP bridge setup
- Scene graph testing (waiting for world reload)

**🔲 Next Priority**:
1. HTTP bridge (clean architecture)
2. Raycast vision (sign reading)
3. Protection checks (safety)
4. Trust scores (social memory)

---

**Let's build this right: bot does verbs, LLM does decisions, HTTP connects them cleanly.** 🚀
