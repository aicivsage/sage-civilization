-- bothavior_simple/tax.lua
-- 100 ENERGY → 24 hours of access (no glass walls). Then walls return.

tax = {}

local function now() return utils.now() end

local function pay_plot(owner, plot)
  if plot.owner ~= owner and not minetest.check_player_privs(owner, {server=true}) then
    return false, "Only plot owner or admin can pay."
  end
  if not points.sub_energy(owner, config.TAX_COST_ENERGY) then
    return false, ("Need %d ENERGY. Use /energy to check balance."):format(config.TAX_COST_ENERGY)
  end
  plot.tax_paid_until = now() + config.TAX_DURATION_SECS
  minetest.get_mod_storage():set_string("plot:"..plot.id, minetest.serialize(plot))
  land.set_walled(plot, false)
  return true, "Tax paid. Plot is open for 24 hours."
end

function tax.cmd_pay(name, param)
  local pid = (param or ""):match("(%S+)")
  if not pid then return false, "Usage: /plot_taxpay <plot_id>" end
  local p = land.by_id(pid)
  if not p then return false, "Plot not found." end
  return pay_plot(name, p)
end

function tax.is_open(plot)
  return plot.tax_paid_until ~= nil and now() < plot.tax_paid_until
end

function tax.enforce_all()
  for _,p in ipairs(land.all()) do
    if tax.is_open(p) then
      if p.walled then land.set_walled(p, false) end
    else
      if not p.walled then land.set_walled(p, true) end
    end
  end
end
