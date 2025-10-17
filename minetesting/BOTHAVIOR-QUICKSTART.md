# BOTHAVIOR System - Quick Start Guide

**Two-Layer AI Architecture**: Bot Layer (Lua) + LLM Layer (Python) + HTTP Bridge

---

## 🚀 Quick Start (5 Steps)

### 1. Configure Minetest HTTP

Add to your `minetest.conf`:
```
secure.http_mods = bothavior_simple
```

**Config location**:
- Windows: `C:\Users\<username>\AppData\Roaming\Minetest\minetest.conf`
- Linux: `~/.minetest/minetest.conf`
- Or in Minetest installation directory

### 2. Install Flask (Python dependency)

```bash
pip3 install flask requests
```

### 3. Launch BOTHAVIOR System

```bash
./tools/launch_bothavior_system.sh
```

This starts:
- HTTP Orchestrator (port 8787)
- Diana's Mind (decision loop)

### 4. Start Minetest

1. Launch Minetest
2. Select your world
3. Load with `bothavior_simple` mod enabled

### 5. Spawn Diana

In Minetest chat:
```
/grantme all
/ai_spawn Diana
```

**Watch Diana come alive!** ✨

She will:
- Send perceptions to orchestrator every 5 seconds
- Make intelligent decisions based on boredom, nearby players, signs
- Execute actions (move, chat, stay, explore)
- Read signs and verify claims
- Remember experiences

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│ Minetest (Lua Bot Layer)               │
│                                          │
│  • Movement & navigation                │
│  • Scene graph perception               │
│  • Sign reading (raycast)               │
│  • Building/digging (protection checks) │
│  • HTTP: POST perceptions               │
│  • HTTP: GET commands                   │
└─────────────────────────────────────────┘
            │
            │ HTTP (port 8787)
            ↓
┌─────────────────────────────────────────┐
│ Orchestrator (HTTP Bridge)              │
│                                          │
│  • Receives perceptions                 │
│  • Queues commands                      │
│  • Trust scores                         │
│  • Plot ratings                         │
│  • Rate limiting                        │
│  • Event logging                        │
└─────────────────────────────────────────┘
            │
            │ REST API
            ↓
┌─────────────────────────────────────────┐
│ Diana's Mind (Python LLM Layer)         │
│                                          │
│  • Fetches perceptions                  │
│  • Makes strategic decisions            │
│  • Evaluates sign claims                │
│  • Manages social memory                │
│  • Sends commands                       │
└─────────────────────────────────────────┘
```

---

## 📊 What Diana Can Do

### Perception (What She Sees)

- **Position**: X, Y, Z coordinates
- **Boredom**: 0.0 (content) to 1.0 (extremely bored)
- **Nearby Players**: Names, distances, directions
- **Nearby Plots**: Names, owners, tax status, distances
- **Current Plot**: Where she's standing
- **Nearby Signs**: Text content, distances
- **Dwelling Time**: How long at current location

### Actions (What She Can Do)

- **move_to_plot**: Teleport to specific plot
- **stay**: Stay at current location (reduce boredom)
- **wander**: Random exploration
- **chat**: Send chat message
- **place_node**: Build (with protection check)
- **dig_node**: Dig (with protection check)

### Decision Logic

Diana decides based on:
1. **Boredom** (0.8+ → explore)
2. **Signs** (interesting content → stay)
3. **Players** (social → stay)
4. **Dwelling time** (120s+ → wander)
5. **Plot ratings** (remembers fun places)

---

## 🎮 Test Diana

### Spawn & Observe
```
/ai_spawn Diana
```

Diana will wander and explore autonomously.

### Place Signs to Attract Her

```
# Place sign with interesting text
"Fishing Mini-Game v2 - Cool new event!"
```

Diana reads signs and stays longer at plots with interesting content.

### Invite Diana (Future: via !talk)

```
!talk Diana Check out this cool new fishing mini-game here!
```

Orchestrator processes invitation with:
- Novelty keywords ("cool", "new", "fishing", "game")
- Trust score (past interactions)
- Boredom level

### Check Status

```bash
curl http://127.0.0.1:8787/status
curl http://127.0.0.1:8787/events
```

---

## 📁 File Structure

```
tools/
  bothavior_orchestrator.py    - HTTP bridge (Flask server)
  diana_mind.py                 - Diana's decision layer
  launch_bothavior_system.sh    - Start everything
  stop_bothavior_system.sh      - Stop everything

minetest-mods/bothavior_simple/
  init.lua                      - Mod entry point, commands
  ai.lua                        - Entity logic, perception, HTTP
  config.lua                    - Configuration
  land.lua                      - Plot system
  tax.lua                       - Tax/access control
  points.lua                    - Points economy

docs/
  BOTHAVIOR-DEVELOPMENT-PLAN.md - 7-phase roadmap
  BOTHAVIOR-VISION-OPTIONS.md   - Vision system design
  CAPABILITY-LAYERS.md          - Bot vs LLM capabilities

logs/
  orchestrator.log              - HTTP bridge logs
  diana.log                     - Decision loop logs
```

---

## 🔧 Commands Reference

### Minetest Commands

```
/grantme all                  - Grant admin privileges
/ai_spawn Diana               - Spawn Diana
/ai_spawn Alice               - Spawn Alice
/ai_perception Diana          - Export Diana's perception (debug)
/ai_list                      - Export all AI perceptions (debug)
/energy                       - Check ENERGY balance
/points singleplayer          - Check POINTS earned
/plot_create demo_plot corey  - Create plot
/plot_taxpay demo_plot        - Pay tax (100 ENERGY for 24h)
```

### Terminal Commands

```bash
# Launch system
./tools/launch_bothavior_system.sh

# Stop system
./tools/stop_bothavior_system.sh

# Test Diana's decision (single cycle)
python3 tools/diana_mind.py test

# Run Diana forever
python3 tools/diana_mind.py

# Check orchestrator status
curl http://127.0.0.1:8787/status

# Get recent events
curl http://127.0.0.1:8787/events

# Get all perceptions
curl http://127.0.0.1:8787/perceptions

# Get Diana's perception
curl http://127.0.0.1:8787/perception/<diana_id>

# Get player trust score
curl http://127.0.0.1:8787/trust/corey

# Get plot rating
curl http://127.0.0.1:8787/plot_rating/demo_plot
```

---

## 🐛 Troubleshooting

### Orchestrator won't start

**Error**: `Port 8787 already in use`

**Fix**:
```bash
kill $(lsof -t -i:8787)
# Or
./tools/stop_bothavior_system.sh
```

### Diana not responding

**Check**:
1. Is orchestrator running? `curl http://127.0.0.1:8787/health`
2. Is Diana spawned? `/ai_list` in Minetest
3. Is HTTP enabled? Check minetest.conf
4. Check logs: `tail -f logs/orchestrator.log logs/diana.log`

### No perceptions received

**Check**:
1. Minetest config: `secure.http_mods = bothavior_simple`
2. Restart Minetest after config change
3. Reload world after mod changes
4. Check Minetest debug.txt for HTTP errors

### Diana stuck or not moving

**Check**:
1. Is she receiving commands? Check `logs/diana.log`
2. Is she receiving perceptions? `curl http://127.0.0.1:8787/perceptions`
3. Check her boredom level (should increase over time)

---

## 📈 What's Implemented

### ✅ Phase 1: Foundation

- [x] HTTP orchestrator (Flask)
- [x] Scene graph perception (position, boredom, players, plots)
- [x] Raycast vision (sign reading)
- [x] HTTP bridge (Lua ↔ Python)
- [x] Diana's decision loop
- [x] Command execution (move, stay, chat)
- [x] Protection checks (is_protected)
- [x] Building/digging verbs
- [x] Trust scores (basic)
- [x] Plot ratings (basic)
- [x] Rate limiting
- [x] Event logging

### 🔄 Phase 2: Building & Interaction

- [ ] Complex structure building
- [ ] Visual verification (screenshots)
- [ ] Claim credibility scoring
- [ ] Trust score refinement

### 🔄 Phase 3: Farming & Automation

- [ ] Plant/harvest verbs
- [ ] Crafting chains
- [ ] Inventory management

### 🔄 Phase 4: Social Memory

- [ ] Advanced trust algorithms
- [ ] Plot rating decay
- [ ] Player relationship tracking

### 🔄 Phase 5: Orchestration

- [ ] Load balancing (max 3 AIs per plot)
- [ ] Experiment scheduling
- [ ] Telemetry dashboard

### 🔄 Phase 6: Vision

- [ ] Screenshot on-demand
- [ ] Visual claim verification
- [ ] Fun evaluation with vision

### 🔄 Phase 7: Advanced

- [ ] Self-preservation (hazard avoidance)
- [ ] Guided tours
- [ ] Complex logistics (Pipeworks integration)

---

## 🎯 Success Metrics

**Diana is working when**:
- Orchestrator receives perceptions every 5 seconds
- Diana makes decisions based on perception
- Commands execute in game
- Diana's behavior changes based on context
- Signs influence her decisions
- She doesn't violate protection boundaries

**Check these**:
```bash
# Should show active_ais: 1
curl http://127.0.0.1:8787/status

# Should show recent PERCEPTION_RECEIVED events
curl http://127.0.0.1:8787/events | tail -20

# Should show Diana's perception
curl http://127.0.0.1:8787/perceptions
```

---

## 🚀 Next Steps

1. **Add More AIs**: `/ai_spawn Alice`, `/ai_spawn Bob`
2. **Test Social Dynamics**: Multiple AIs competing for plots
3. **Build Interesting Plots**: Add signs, mini-games, structures
4. **Monitor Behavior**: Watch decision logs, trust scores
5. **Integrate Task Agent**: Replace mock decisions with Claude Code Task invocations
6. **Add Vision**: Screenshot capability for visual verification
7. **Expand Memory**: Per-user/per-plot persistent storage

---

## 🤖 Philosophy

**Bot Layer** (Lua):
- Fast, deterministic verbs
- Movement, sensing, building
- Protection checks, safety

**LLM Layer** (Python):
- Strategic decisions
- Social reasoning
- Memory and learning

**Bridge** (HTTP):
- Clean, auditable
- Event-driven
- Rate-limited

**Result**: Emergent, intelligent behavior from simple verbs + strategic reasoning

---

**Diana is alive and ready to explore!** 🌟

See `docs/BOTHAVIOR-DEVELOPMENT-PLAN.md` for full 7-phase roadmap.
