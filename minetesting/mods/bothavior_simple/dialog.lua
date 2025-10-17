-- bothavior_simple/dialog.lua
-- Players persuade AIs: "!talk <AIName> <message>" boosts teleport chance.

local prefix = config.CHAT_PREFIX

minetest.register_on_chat_message(function(name, msg)
  if msg:sub(1,#prefix) ~= prefix then return false end
  local line = msg:sub(#prefix+1)
  local cmd, ai_name, text = line:match("^(%S+)%s+(%S+)%s+(.+)$")
  if cmd ~= "talk" or not ai_name or not text then
    minetest.chat_send_player(name, "Usage: !talk <AIName> <message>")
    return true
  end

  local player = minetest.get_player_by_name(name)
  if not player then return true end
  local here = land.find_by_pos(player:get_pos())
  if not here then
    minetest.chat_send_player(name, "Stand on a defined plot to invite the AI.")
    return true
  end

  -- Very dumb novelty heuristic (swap in your LLM later)
  local w = 0.2
  local tl = text:lower()
  if tl:find("new") or tl:find("game") or tl:find("event") or tl:find("cool") or tl:find("better") then w = w + 0.5 end
  if not tax.is_open(here) then w = w * 0.4 end  -- closed plots are less compelling

  local ok = ai.try_visit(ai_name, here.id, w)
  if ok then
    minetest.chat_send_all(("AI %s accepted %s's invitation to plot %s."):format(ai_name, name, here.name))
  else
    minetest.chat_send_player(name, "AI declined. Try offering more novelty—or pay your taxes.")
  end
  return true
end)
