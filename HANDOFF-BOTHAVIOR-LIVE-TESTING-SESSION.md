# BOTHAVIOR System - Live Testing Session Handoff

**Date**: 2025-10-16
**Session**: Full system integration test
**Goal**: Run Minetest, spawn Diana, test complete perception → decision → execution loop

---

## 🎯 Testing Plan

### Phase 1: System Launch ✅
- [x] Start HTTP orchestrator
- [x] Verify Flask server health
- [x] Confirm endpoints responding

### Phase 2: Minetest Integration
- [ ] Launch Minetest
- [ ] Configure HTTP permissions
- [ ] Load world with bothavior_simple mod
- [ ] Verify Lua mod loaded

### Phase 3: Diana Spawning
- [ ] Grant admin privileges
- [ ] Spawn Diana entity
- [ ] Verify entity appears in game
- [ ] Confirm AI ID assigned

### Phase 4: Perception Testing
- [ ] Wait for Diana's first perception POST
- [ ] Verify perception received by orchestrator
- [ ] Check perception contains: position, boredom, nearby_players, nearby_plots, nearby_signs
- [ ] Confirm JSON structure correct

### Phase 5: Decision Testing
- [ ] Start Diana's Mind decision loop
- [ ] Verify Diana fetches perception
- [ ] Check Diana makes decision
- [ ] Confirm decision sent to orchestrator
- [ ] Verify command queued

### Phase 6: Execution Testing
- [ ] Verify Lua polls for command
- [ ] Check command retrieved
- [ ] Confirm action executed in game
- [ ] Observe Diana's behavior change

### Phase 7: Sign Reading Test
- [ ] Place sign with text in game
- [ ] Move Diana near sign
- [ ] Verify perception includes sign text
- [ ] Check if decision influenced by sign
- [ ] Confirm Diana stays near interesting content

### Phase 8: Building Test
- [ ] Send place_node command to Diana
- [ ] Verify protection check works
- [ ] Confirm block placed in game
- [ ] Test dig_node command
- [ ] Verify block removed

### Phase 9: Full Autonomous Loop
- [ ] Let Diana run for 5 minutes
- [ ] Monitor perception → decision → execution cycles
- [ ] Count successful loops
- [ ] Check for errors in logs
- [ ] Verify no crashes or hangs

### Phase 10: Performance & Stability
- [ ] Measure perception latency
- [ ] Measure decision latency
- [ ] Measure command execution latency
- [ ] Check memory usage
- [ ] Verify no leaks

---

## 📊 Test Results

(Will be filled during testing)

### System Performance
- Perception latency: TBD
- Decision latency: TBD
- Command execution latency: TBD
- Total loop time: TBD
- Successful cycles: TBD
- Failed cycles: TBD

### Observations
- Diana's behavior: TBD
- Sign reading: TBD
- Decision quality: TBD
- Error handling: TBD

---

## 🔧 Testing Log

(Live updates during testing session)

