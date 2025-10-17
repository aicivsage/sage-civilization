-- bothavior_simple/init.lua
-- Minimal attention-economy MVP: land, taxes, wandering AIs, talk-to-teleport, points.
-- SPDX-License-Identifier: MIT

local MOD = minetest.get_current_modname()
local MP  = minetest.get_modpath(MOD)

dofile(MP.."/utils.lua")
dofile(MP.."/config.lua")
dofile(MP.."/points.lua")
dofile(MP.."/land.lua")
dofile(MP.."/tax.lua")
dofile(MP.."/ai.lua")
dofile(MP.."/dialog.lua")

minetest.log("action", "[bothavior_simple] Loaded v0.2.0")

-- Give first-time players their starter ENERGY
minetest.register_on_joinplayer(function(player)
  local name = player:get_player_name()
  if points.get_energy(name) == nil then
    points.set_energy(name, config.START_ENERGY)
    minetest.chat_send_player(name, ("Welcome! You received %d ENERGY."):format(config.START_ENERGY))
  end
end)

-- Global upkeep: enforce tax walls; tick points from AI dwell
local function global_tick()
  tax.enforce_all()        -- Hard-wall or clear based on expiry
  ai.tick_all()            -- Dwell-time → points, wander/teleport
  minetest.after(config.GLOBAL_TICK_SECS, global_tick)
end
minetest.after(config.GLOBAL_TICK_SECS, global_tick)

-- Handy chat commands
local posmarks = {}
local function set_mark(which, name)
  local p = minetest.get_player_by_name(name)
  if not p then return false, "Player not found" end
  posmarks[name] = posmarks[name] or {}
  posmarks[name][which] = vector.round(p:get_pos())
  return true, which.." set to "..minetest.pos_to_string(posmarks[name][which])
end

minetest.register_chatcommand("setpos1", {description="Mark pos1", func=function(n) return set_mark("pos1",n) end})
minetest.register_chatcommand("setpos2", {description="Mark pos2", func=function(n) return set_mark("pos2",n) end})

function bothavior_get_posmarks(name) return posmarks[name] end

minetest.register_chatcommand("plot_create", {
  params = "<plot_name> <owner_name>",
  description = "Create a plot from your pos1/pos2, assign owner.",
  privs = {server=true},
  func = function(invoker, param)
    local name, owner = param:match("^(%S+)%s+(%S+)$")
    if not (name and owner) then return false, "Usage: /plot_create <plot_name> <owner_name>" end
    return land.cmd_create(invoker, name, owner)
  end
})

minetest.register_chatcommand("plot_taxpay", {
  params = "<plot_id>",
  description = "Pay 100 ENERGY for 24 hours of access on your plot.",
  func = function(name, param) return tax.cmd_pay(name, param) end
})

minetest.register_chatcommand("ai_spawn", {
  params = "<AIName>",
  description = "Spawn a Bothavior at your feet.",
  privs = {server=true},
  func = function(name, param) return ai.cmd_spawn(name, param) end
})

minetest.register_chatcommand("energy", {
  description="Show your ENERGY",
  func=function(name) return true, "ENERGY: "..(points.get_energy(name) or 0) end
})

minetest.register_chatcommand("points", {
  params="<player>",
  description="Show attention points for a player",
  func=function(_, param)
    local who = param ~= "" and param or nil
    if not who then return false,"Usage: /points <player>" end
    return true, ("POINTS[%s]: %d"):format(who, points.get_points(who) or 0)
  end
})

minetest.register_chatcommand("ai_perception", {
  params="<ai_name_or_id>",
  description="Export AI perception to /tmp/ for bridge",
  privs={server=true},
  func=function(_, param)
    local ai_id = (param or ""):match("(%S+)")
    if not ai_id then return false, "Usage: /ai_perception <ai_name_or_id>" end

    -- Try to find AI by name or ID
    local entity = ai.get_by_name_or_id(ai_id)
    if not entity then return false, "AI not found: "..ai_id end

    local ok = ai.export_perception(entity.ai_id)
    if ok then
      return true, ("Perception exported to /tmp/ai_perception_%s.json"):format(entity.ai_id)
    else
      return false, "Failed to export perception"
    end
  end
})

minetest.register_chatcommand("ai_list", {
  description="List all active AI entities",
  func=function()
    local count = ai.export_all_perceptions()
    return true, ("Exported perception for %d active AIs"):format(count)
  end
})
