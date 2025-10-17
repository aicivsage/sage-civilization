# 🤖 Minetest Bot Usage Guide

**What is it?** A command-driven bot that controls the Minetest player perspective for autonomous gameplay.

---

## Quick Start

```python
from tools.minetest_bot import MinetestBot

# Create bot instance
bot = MinetestBot()

# Take a screenshot
screenshot = bot.look()  # Returns path to PNG file

# Execute a command
bot.execute_command('/energy')

# Spawn an AI
bot.spawn_ai('Alice')

# Move around
bot.move_forward(duration=2.0)  # Move forward 2 seconds
bot.jump()
```

---

## 📸 Perception Commands

### `bot.look()`
Take a screenshot of current player view.
- **Returns**: Path to screenshot PNG file
- **Usage**: `screenshot = bot.look()`
- **Note**: Screenshots saved to `/mnt/c/temp/claude_screenshots/`

### `bot.check_chat()`
Take screenshot specifically for reading chat messages.
- **Returns**: Screenshot path
- **Usage**: Use with Claude vision to read chat

---

## 🏃 Movement Commands

### `bot.move_forward(duration)`
Move forward for specified seconds.
- **Args**: `duration` (float, default=1.0)
- **Example**: `bot.move_forward(3.0)  # Move 3 seconds`

### `bot.move_backward(duration)`
Move backward.

### `bot.strafe_left(duration)`
Strafe left.

### `bot.strafe_right(duration)`
Strafe right.

### `bot.jump()`
Jump once.

### `bot.fly_up(duration)`
Fly upward (requires fly privilege).

### `bot.fly_down(duration)`
Fly downward.

---

## ⚡ Command Execution

### `bot.execute_command(command, wait=2.0)`
Execute any Minetest chat command.
- **Args**:
  - `command` (str): Command to execute (e.g., `/energy`, `/ai_spawn Alice`)
  - `wait` (float): Seconds to wait for command result
- **Returns**: Screenshot path after command execution
- **Example**:
  ```python
  bot.execute_command('/grantme all')
  bot.execute_command('/setpos1')
  bot.execute_command('/plot_create myplot singleplayer')
  ```

### `bot.get_energy()`
Check current energy level.
- **Returns**: Screenshot (use vision to read number)

### `bot.get_points(player='singleplayer')`
Check points for a player.
- **Returns**: Screenshot (use vision to read points)

---

## 🎯 High-Level Actions

### `bot.spawn_ai(name)`
Spawn an AI entity.
- **Args**: `name` (str) - Name for AI (e.g., 'Alice', 'Bob')
- **Returns**: Screenshot of spawn confirmation
- **Example**: `bot.spawn_ai('Alice')`

### `bot.talk(target, message)`
Use !talk command to persuade an AI.
- **Args**:
  - `target` (str): AI name
  - `message` (str): Message (use novelty keywords: new, cool, game, event, better)
- **Example**: `bot.talk('Alice', 'check out this new cool plot')`

### `bot.create_plot(plot_name, size=10)`
Automatically create a plot.
- **Args**:
  - `plot_name` (str): Name for plot
  - `size` (int): Approximate size in blocks
- **How it works**:
  1. Sets position 1
  2. Moves to create area
  3. Sets position 2
  4. Creates plot
- **Example**: `bot.create_plot('myplot', size=15)`

### `bot.grant_self_privileges()`
Grant all privileges to player.

---

## 🎮 Autonomous Behaviors

### `bot.explore(duration)`
Random exploration with screenshots.
- **Args**: `duration` (int): Seconds to explore
- **Returns**: List of screenshot paths
- **Example**: `screenshots = bot.explore(30)`

### `bot.autonomous_setup()`
Automated setup routine.
- Grants privileges
- Checks energy
- Checks points
- **Returns**: Dict with results and screenshots

### `bot.autonomous_gameplay_demo()`
Full autonomous gameplay demonstration.
- **Includes**:
  1. Setup (privileges, energy check)
  2. Create plot
  3. Spawn 3 AIs (Alice, Bob, Charlie)
  4. Interact with AIs
  5. Check final state
- **Returns**: Complete results dict
- **Duration**: ~2 minutes

---

## 🛠️ Utility Commands

### `bot.wait(seconds)`
Wait/pause for specified time.

### `bot.get_state()`
Get current bot state.
- **Returns**: Dict with energy, position, spawned_ais, plots, etc.

### `bot.reset_state()`
Reset bot state tracking.

---

## 📋 Usage Examples

### Example 1: Basic Commands
```python
from tools.minetest_bot import MinetestBot

bot = MinetestBot()

# Look around
screenshot = bot.look()

# Check energy
bot.get_energy()

# Spawn AI
bot.spawn_ai('TestBot')
```

### Example 2: Create Plot & Spawn AIs
```python
bot = MinetestBot()

# Setup
bot.grant_self_privileges()

# Create plot
bot.create_plot('myplot', size=12)

# Spawn AIs
bot.spawn_ai('Alice')
bot.spawn_ai('Bob')

# Interact
bot.talk('Alice', 'check out this cool new plot')
bot.talk('Bob', 'this game is better than ever')

# Check results
bot.get_energy()
bot.get_points()
```

### Example 3: Exploration Loop
```python
bot = MinetestBot()

# Explore for 60 seconds
screenshots = bot.explore(60)

print(f"Captured {len(screenshots)} screenshots")
for screenshot in screenshots:
    # Use Claude vision to analyze each screenshot
    print(f"Analyzing: {screenshot}")
```

### Example 4: Full Autonomous Demo
```python
bot = MinetestBot()

# Run complete autonomous gameplay
results = bot.autonomous_gameplay_demo()

# Check results
print(f"Plots created: {len(bot.state['plots'])}")
print(f"AIs spawned: {len(bot.state['spawned_ais'])}")
```

### Example 5: Custom Autonomous Loop
```python
import time
from tools.minetest_bot import MinetestBot

bot = MinetestBot()
bot.grant_self_privileges()

# Custom gameplay loop
for i in range(10):
    print(f"\n=== Loop {i+1} ===")

    # Perceive
    screenshot = bot.look()
    # TODO: Use Claude vision to analyze screenshot

    # Decide & Act
    if i % 3 == 0:
        bot.spawn_ai(f'AI_{i}')
    elif i % 3 == 1:
        bot.move_forward(2)
        bot.jump()
    else:
        bot.execute_command('/energy')

    time.sleep(3)

print("Autonomous loop complete!")
```

---

## 🎯 Integration with Claude Vision

The bot is designed to work with Claude's vision analysis:

```python
# Take screenshot
screenshot = bot.look()

# Read screenshot with Claude Code's Read tool
# (This returns the image for vision analysis)
# You can then see:
# - Player position
# - Nearby entities (AI cubes)
# - Chat messages
# - Plot glass walls
# - Game state

# Make decisions based on what you see
# Then execute actions:
bot.move_forward(2)
bot.spawn_ai('NewAI')
```

---

## ⚙️ Technical Details

### Window Focus
The bot automatically focuses the Minetest window before sending keyboard commands using PowerShell's `AppActivate()`.

### Screenshot Storage
All screenshots saved to: `/mnt/c/temp/claude_screenshots/screenshot_YYYYMMDD_HHMMSS_mmm.png`

### Timing
- Commands wait 2 seconds by default (configurable)
- Movement duration is in seconds (0.5s ≈ 1 block traveled)
- Screenshot capture takes ~200ms

### State Tracking
Bot maintains state dictionary:
```python
{
    'energy': None,
    'position': None,
    'last_screenshot': 'path/to/screenshot.png',
    'spawned_ais': ['Alice', 'Bob'],
    'plots': ['myplot', 'demo_plot']
}
```

---

## 🚀 Running Demos

### Quick Demo
```bash
python3 tools/minetest_bot.py demo
```

### Full Autonomous Gameplay
```bash
python3 tools/minetest_bot.py full-demo
```

### Custom Script
```bash
python3 test_bot.py
```

---

## 💡 Tips

1. **Use vision analysis** after each `bot.look()` to make intelligent decisions
2. **Adjust timing** if commands are too fast/slow
3. **Check state** with `bot.get_state()` to track what's been done
4. **Chain commands** for complex behaviors
5. **Take screenshots frequently** to monitor game state

---

## 🎓 Next Steps

Now that you have bot control, you can:
1. **Implement strategy optimization** (which plots are best?)
2. **Create learning loops** (try action → observe result → learn)
3. **Build autonomous agents** (let bot play for hours)
4. **Test mod mechanics** (validate game balance)
5. **Generate training data** (screenshots + actions)

---

**Status**: ✅ Production Ready
**Lines of Code**: 350+
**Commands Available**: 20+

**This bot gives you FULL CONTROL of the Minetest player through simple Python commands!** 🎮🤖
