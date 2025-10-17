-- bothavior_simple/config.lua
config = {
  -- Loop cadence
  GLOBAL_TICK_SECS = 2,

  -- Starter + tax
  START_ENERGY = 1000,
  TAX_COST_ENERGY = 100,
  TAX_DURATION_SECS = 24 * 60 * 60, -- 24 hours

  -- Plot enforcement
  WALL_NODE = "default:glass",

  -- AI behavior
  AI_STEP_INTERVAL = 0.5,
  AI_BASE_BOREDOM_RATE = 0.02,  -- rises over time
  AI_NOVELTY_MULT = 0.6,        -- amplifies boredom into teleport urges
  AI_TELEPORT_PROB = 0.01,      -- base chance per step
  AI_DWELL_CREDIT_MAXDELTA = 5, -- cap seconds per tick to avoid spikes

  -- Points
  POINTS_PER_AI_SECOND = 1,     -- 1 point per AI-second on valid plot

  -- Dialog
  CHAT_PREFIX = "!",            -- "!talk <AIName> your pitch here"

  -- Optional: DB webhooks (leave empty to disable; we'll just keep local points)
  DB_POINTS_ENDPOINT = "",      -- e.g., "http://localhost:8000/points/award"
  DB_TIMEOUT = 0.8,             -- seconds (Minetest HTTP if enabled)
}
