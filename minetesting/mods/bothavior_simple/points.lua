-- bothavior_simple/points.lua
-- Minimal local balances for ENERGY (for taxes) and POINTS (for attention).
-- Swap these with your real DB layer later; optional HTTP hook included.

local storage = minetest.get_mod_storage()
points = {}

local function k_energy(player) return "energy:"..player end
local function k_points(player) return "points:"..player end

function points.get_energy(name)
  local v = storage:get_string(k_energy(name))
  if v == "" then return nil end
  return tonumber(v)
end
function points.set_energy(name, amt)
  storage:set_string(k_energy(name), tostring(math.max(0, math.floor(amt))))
end
function points.add_energy(name, delta)
  local cur = points.get_energy(name) or 0
  points.set_energy(name, cur + delta)
end
function points.sub_energy(name, delta)
  local cur = points.get_energy(name) or 0
  if cur < delta then return false end
  points.set_energy(name, cur - delta)
  return true
end

function points.get_points(name)
  local v = storage:get_string(k_points(name))
  if v == "" then return 0 end
  return tonumber(v)
end
function points.add_points(name, delta)
  local cur = points.get_points(name)
  storage:set_string(k_points(name), tostring(math.max(0, math.floor(cur + delta))))
  -- Optional: HTTP webhook to your DB; disabled if endpoint empty
  if config.DB_POINTS_ENDPOINT ~= "" then
    local http = minetest.request_http_api()
    if http then
      http.fetch({
        url = config.DB_POINTS_ENDPOINT,
        timeout = config.DB_TIMEOUT,
        method = "POST",
        data = minetest.write_json({player=name, delta=delta, ts=utils.now()}),
        extra_headers = {"Content-Type: application/json"}
      }, function() end)
    end
  end
end
