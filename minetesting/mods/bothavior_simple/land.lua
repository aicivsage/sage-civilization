-- bothavior_simple/land.lua
-- Axis-aligned rectangular plots with owner and 24h tax windows.

land = {}
local storage = minetest.get_mod_storage()

local function idx_key() return "plots:index" end
local function plot_key(id) return "plot:"..id end

local function load_idx()
  local raw = storage:get_string(idx_key())
  return raw ~= "" and minetest.deserialize(raw) or {}
end
local function save_idx(t) storage:set_string(idx_key(), minetest.serialize(t)) end

local plots_index = load_idx() -- list of plot_ids

local function load_plot(id)
  local raw = storage:get_string(plot_key(id))
  return raw ~= "" and minetest.deserialize(raw) or nil
end
local function save_plot(p) storage:set_string(plot_key(p.id), minetest.serialize(p)) end

local function sort_bbox(a,b)
  return {
    x1 = math.min(a.x,b.x), y1 = math.min(a.y,b.y), z1 = math.min(a.z,b.z),
    x2 = math.max(a.x,b.x), y2 = math.max(a.y,b.y), z2 = math.max(a.z,b.z),
  }
end
local function contains(bb, pos)
  return pos.x>=bb.x1 and pos.x<=bb.x2 and pos.y>=bb.y1 and pos.y<=bb.y2 and pos.z>=bb.z1 and pos.z<=bb.z2
end

function land.all()
  local out = {}
  for _,id in ipairs(plots_index) do
    local p = load_plot(id)
    if p then table.insert(out, p) end
  end
  return out
end

function land.by_id(id) return load_plot(id) end

function land.find_by_pos(pos)
  for _,id in ipairs(plots_index) do
    local p = load_plot(id)
    if p and contains(p.bbox, pos) then return p end
  end
  return nil
end

local function border_glass(p, place)
  local bb = p.bbox
  local y = bb.y1
  for x=bb.x1, bb.x2 do
    for z=bb.z1, bb.z2 do
      if x==bb.x1 or x==bb.x2 or z==bb.z1 or z==bb.z2 then
        for yy=y, y+3 do
          local pos = {x=x,y=yy,z=z}
          if place then
            minetest.set_node(pos, {name=config.WALL_NODE})
          else
            local n = minetest.get_node(pos)
            if n and n.name == config.WALL_NODE then minetest.remove_node(pos) end
          end
        end
      end
    end
  end
end

function land.set_walled(p, on)
  p.walled = on and true or false
  save_plot(p)
  border_glass(p, p.walled)
end

function land.cmd_create(invoker, plot_name, owner_name)
  local marks = bothavior_get_posmarks(invoker)
  if not (marks and marks.pos1 and marks.pos2) then
    return false, "Set pos1/pos2 first."
  end
  local id = ("%s-%d"):format(plot_name, utils.now())
  local p = {
    id = id,
    name = plot_name,
    owner = owner_name,
    bbox = sort_bbox(marks.pos1, marks.pos2),
    tax_paid_until = 0,  -- UNIX time
    walled = true       -- start walled until first payment
  }
  table.insert(plots_index, id); save_idx(plots_index); save_plot(p)
  land.set_walled(p, true)
  return true, ("Plot %s created for %s; currently walled until taxes are paid."):format(id, owner_name)
end
