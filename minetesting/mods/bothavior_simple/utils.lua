-- bothavior_simple/utils.lua
utils = {}

function utils.now() return os.time() end

function utils.clamp(x, a, b)
  if x < a then return a end
  if x > b then return b end
  return x
end

function utils.rand_int(a,b)
  return a + math.random(0, b-a)
end
