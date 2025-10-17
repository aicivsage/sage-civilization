-- bothavior_simple/ai.lua
-- Minimal Bothavior entity: boredom/novelty drives, wander, teleport, dwell points.

ai = {}

-- Track all entities to run dwell/points credit per tick
local ACTIVE = {}

-- HTTP API for orchestrator communication
local http = minetest.request_http_api()
local ORCHESTRATOR_URL = "http://127.0.0.1:8787"

if not http then
  minetest.log("warning", "[bothavior_simple] HTTP API not available - enable with secure.http_mods or secure.trusted_mods")
end

-- Perception system: Build scene graph for AI agents
function ai.get_perception(entity)
  local pos = entity.object:get_pos()
  local perception = {
    entity_id = entity.ai_id,
    name = entity.display_name,
    position = {x=pos.x, y=pos.y, z=pos.z},
    boredom = entity.boredom,
    nearby_players = {},
    nearby_plots = {},
    current_plot = nil,
    dwelling_time = utils.now() - entity.stay_since
  }

  -- Find nearby players (within 30 blocks)
  for _, player in ipairs(minetest.get_connected_players()) do
    local ppos = player:get_pos()
    local distance = vector.distance(pos, ppos)
    if distance < 30 then
      table.insert(perception.nearby_players, {
        name = player:get_player_name(),
        distance = math.floor(distance),
        direction = {
          x = ppos.x - pos.x,
          y = ppos.y - pos.y,
          z = ppos.z - pos.z
        }
      })
    end
  end

  -- Find nearby plots
  for _, plot in ipairs(land.all()) do
    local center = {
      x = math.floor((plot.bbox.x1 + plot.bbox.x2) / 2),
      y = plot.bbox.y1,
      z = math.floor((plot.bbox.z1 + plot.bbox.z2) / 2)
    }
    local distance = vector.distance(pos, center)
    if distance < 50 then
      table.insert(perception.nearby_plots, {
        id = plot.id,
        name = plot.name,
        owner = plot.owner,
        distance = math.floor(distance),
        tax_open = tax.is_open(plot),
        center = center
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

  -- Add raycast vision (read nearby signs)
  perception.nearby_signs = ai.read_nearby_signs(entity, 15)

  return perception
end

-- Raycast vision: Read nearby signs
function ai.read_nearby_signs(entity, radius)
  local pos = entity.object:get_pos()
  local signs = minetest.find_nodes_in_area(
    vector.subtract(pos, {x=radius, y=radius, z=radius}),
    vector.add(pos, {x=radius, y=radius, z=radius}),
    {"default:sign_wall_wood", "default:sign_wall_steel", "signs:sign_wall_wood", "signs:sign_wall_steel"}
  )

  local sign_texts = {}
  for _, sign_pos in ipairs(signs) do
    local meta = minetest.get_meta(sign_pos)
    local text = meta:get_string("text")
    if text and text ~= "" then
      table.insert(sign_texts, {
        pos = {x=sign_pos.x, y=sign_pos.y, z=sign_pos.z},
        text = text,
        distance = math.floor(vector.distance(pos, sign_pos))
      })
    end
  end

  return sign_texts
end

-- Send perception to HTTP orchestrator
function ai.send_perception_http(entity)
  if not http then
    return false
  end

  local perception = ai.get_perception(entity)
  local json = minetest.write_json(perception)

  http.fetch({
    url = ORCHESTRATOR_URL.."/perception",
    method = "POST",
    data = json,
    extra_headers = {"Content-Type: application/json"}
  }, function(result)
    if result.succeeded then
      minetest.log("action", "[bothavior_simple] Perception sent for "..entity.display_name)
    else
      minetest.log("error", "[bothavior_simple] HTTP POST failed: "..(result.code or "unknown"))
    end
  end)

  return true
end

-- Poll for commands from orchestrator
function ai.poll_command_http(entity)
  if not http then
    return nil
  end

  http.fetch({
    url = ORCHESTRATOR_URL.."/command/"..entity.ai_id,
    method = "GET"
  }, function(result)
    if result.succeeded and result.data then
      local command = minetest.parse_json(result.data)
      if command and command.action and command.action ~= "idle" then
        minetest.log("action", "[bothavior_simple] Command received for "..entity.display_name..": "..command.action)
        ai.execute_command(entity, command)
      end
    end
  end)
end

-- Execute command from orchestrator
function ai.execute_command(entity, command)
  local action = command.action

  if action == "move_to" then
    local target_pos = command.target
    if target_pos then
      entity.object:move_to(target_pos, true)
      entity.boredom = 0.0
      entity.stay_since = utils.now()
    end

  elseif action == "move_to_plot" then
    local plot_id = command.target
    local plot = land.by_id(plot_id)
    if plot then
      local center = {
        x = math.floor((plot.bbox.x1 + plot.bbox.x2) / 2),
        y = plot.bbox.y1 + 1,
        z = math.floor((plot.bbox.z1 + plot.bbox.z2) / 2)
      }
      entity.object:move_to(center, true)
      entity.boredom = 0.0
      entity.stay_since = utils.now()
      entity.current_plot_id = plot.id
    end

  elseif action == "stay" then
    -- Reset boredom to stay longer
    entity.boredom = max(0.0, entity.boredom - 0.5)

  elseif action == "chat" then
    local message = command.message
    if message then
      minetest.chat_send_all("<"..entity.display_name.."> "..message)
    end

  elseif action == "place_node" then
    ai.place_node(entity, command.pos, command.node_name)

  elseif action == "dig_node" then
    ai.dig_node(entity, command.pos)

  else
    minetest.log("warning", "[bothavior_simple] Unknown command: "..action)
  end
end

-- Place node with protection check
function ai.place_node(entity, pos, node_name)
  -- Protection check
  if minetest.is_protected(pos, entity.display_name) then
    minetest.log("warning", "[bothavior_simple] "..entity.display_name.." tried to place in protected area")
    return false
  end

  -- Check if node is air or replaceable
  local current_node = minetest.get_node(pos)
  if current_node.name ~= "air" then
    return false
  end

  -- Place node
  minetest.set_node(pos, {name = node_name})
  minetest.log("action", "[bothavior_simple] "..entity.display_name.." placed "..node_name.." at "..minetest.pos_to_string(pos))

  return true
end

-- Dig node with protection check
function ai.dig_node(entity, pos)
  -- Protection check
  if minetest.is_protected(pos, entity.display_name) then
    minetest.log("warning", "[bothavior_simple] "..entity.display_name.." tried to dig in protected area")
    return false
  end

  -- Dig node
  local node = minetest.get_node(pos)
  minetest.remove_node(pos)
  minetest.log("action", "[bothavior_simple] "..entity.display_name.." dug "..node.name.." at "..minetest.pos_to_string(pos))

  -- TODO: Drop items to inventory or ground

  return true
end

-- Export perception to file for Python bridge (fallback)
function ai.export_perception(ai_id)
  local entity = ACTIVE[ai_id]
  if not entity then
    minetest.log("warning", "[bothavior_simple] Cannot export perception for unknown AI: "..ai_id)
    return false
  end

  local perception = ai.get_perception(entity)
  local json = minetest.write_json(perception)

  local filepath = "/tmp/ai_perception_"..ai_id..".json"
  local file = io.open(filepath, "w")
  if file then
    file:write(json)
    file:close()
    return true
  else
    minetest.log("error", "[bothavior_simple] Failed to write perception file: "..filepath)
    return false
  end
end

-- Export all active AI perceptions
function ai.export_all_perceptions()
  local count = 0
  for ai_id, _ in pairs(ACTIVE) do
    if ai.export_perception(ai_id) then
      count = count + 1
    end
  end
  return count
end

-- Get AI by name or ID
function ai.get_by_name_or_id(name_or_id)
  for _, entity in pairs(ACTIVE) do
    if entity.display_name == name_or_id or entity.ai_id == name_or_id then
      return entity
    end
  end
  return nil
end

minetest.register_entity("bothavior_simple:ai", {
  initial_properties = {
    physical = true,
    collide_with_objects = true,
    visual = "cube",
    visual_size = {x=0.6, y=1.8},
    textures = {"default_steel_block.png","default_steel_block.png",
                "default_steel_block.png","default_steel_block.png",
                "default_steel_block.png","default_steel_block.png"},
    static_save = true,
  },

  ai_id = "",
  display_name = "",
  boredom = 0.0,
  last_step_at = 0,
  stay_since = 0,
  current_plot_id = nil,

  on_activate = function(self, staticdata)
    if staticdata and staticdata ~= "" then
      local d = minetest.deserialize(staticdata); if d then for k,v in pairs(d) do self[k]=v end end
    else
      self.ai_id = "ai-"..utils.now().."-"..utils.rand_int(1000,9999)
      self.display_name = "Bothavior"
      self.boredom = 0.0
    end
    self.last_step_at = utils.now()
    self.stay_since = utils.now()
    ACTIVE[self.ai_id] = self
  end,

  get_staticdata = function(self)
    return minetest.serialize({
      ai_id=self.ai_id, display_name=self.display_name, boredom=self.boredom,
      last_step_at=self.last_step_at, stay_since=self.stay_since, current_plot_id=self.current_plot_id
    })
  end,

  on_deactivate = function(self) ACTIVE[self.ai_id] = nil end,

  on_step = function(self, dtime)
    -- Per-entity movement handled in ai.tick_all()
  end
})

function ai.cmd_spawn(invoker, name)
  local p = minetest.get_player_by_name(invoker); if not p then return false,"Player not found" end
  local pos = vector.add(p:get_pos(), {x=1,y=1,z=0})
  local obj = minetest.add_entity(pos, "bothavior_simple:ai")
  local ent = obj:get_luaentity()
  if name and name ~= "" then ent.display_name = name end
  return true, ("AI spawned: %s (%s)"):format(ent.display_name, ent.ai_id)
end

-- Called by dialog or system to request a teleport to a plot
function ai.try_visit(ai_name_or_id, plot_id, persuasion_weight)
  for _,o in ipairs(minetest.get_objects_inside_radius({x=0,y=0,z=0}, 1e8)) do
    local e = o:get_luaentity()
    if e and e.name == "bothavior_simple:ai" then
      if e.display_name == ai_name_or_id or e.ai_id == ai_name_or_id then
        if math.random() < utils.clamp(persuasion_weight or 0.5, 0, 1) then
          local p = land.by_id(plot_id); if not p then return false end
          local center = {x=math.floor((p.bbox.x1+p.bbox.x2)/2), y=p.bbox.y1+1, z=math.floor((p.bbox.z1+p.bbox.z2)/2)}
          e.object:move_to(center, true)
          e.boredom = 0.0
          e.stay_since = utils.now()
          e.current_plot_id = p.id
          return true
        else
          return false
        end
      end
    end
  end
  return false
end

-- Dwell → points, boredom → wander/teleport
function ai.tick_all()
  local now = utils.now()
  for _,e in pairs(ACTIVE) do
    -- Step cadence
    if now - e.last_step_at < config.AI_STEP_INTERVAL then goto cont end
    e.last_step_at = now

    -- Send perception to orchestrator (every AI_STEP_INTERVAL seconds)
    if http then
      ai.send_perception_http(e)
      ai.poll_command_http(e)
    end

    local pos = e.object:get_pos()
    local plot = land.find_by_pos(pos)

    -- Dwell credit if plot is open and has an owner
    if plot and plot.owner and tax.is_open(plot) then
      local dt = utils.clamp(now - e.stay_since, 0, config.AI_DWELL_CREDIT_MAXDELTA)
      if dt > 0 then
        points.add_points(plot.owner, dt * config.POINTS_PER_AI_SECOND)
        e.stay_since = now
      end
      e.current_plot_id = plot.id
    else
      e.current_plot_id = nil
    end

    -- Drive update
    e.boredom = utils.clamp(e.boredom + config.AI_BASE_BOREDOM_RATE, 0, 1)

    -- Random walk
    local step = {x=utils.rand_int(-1,1), y=0, z=utils.rand_int(-1,1)}
    local newpos = vector.add(pos, step)
    e.object:set_velocity({x=step.x, y=0, z=step.z})
    e.object:move_to(newpos)

    -- Teleport urge
    if math.random() < (config.AI_TELEPORT_PROB * (1 + e.boredom * config.AI_NOVELTY_MULT)) then
      local plots = land.all()
      if #plots > 0 then
        local target = plots[utils.rand_int(1,#plots)]
        local center = {x=math.floor((target.bbox.x1+target.bbox.x2)/2), y=target.bbox.y1+1, z=math.floor((target.bbox.z1+target.bbox.z2)/2)}
        e.object:move_to(center, true)
        e.boredom = 0.0
        e.stay_since = now
        e.current_plot_id = target.id
      end
    end
    ::cont::
  end
end
