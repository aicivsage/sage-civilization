#!/usr/bin/env python3
"""
BOTHAVIOR Orchestrator
HTTP bridge between Minetest (Lua) and AI agents (Claude)

Architecture:
- Minetest POSTs perceptions → /perception
- Minetest GETs commands → /command/<ai_id>
- Python LLM layer POSTs commands → /command/<ai_id>
- Python LLM layer GETs perceptions → /perceptions
"""

from flask import Flask, request, jsonify
import json
import time
import sys
import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Add tools to path for agent invocation
sys.path.insert(0, str(Path(__file__).parent))

app = Flask(__name__)

# State storage
perceptions = {}  # {ai_id: perception_data}
commands = defaultdict(list)  # {ai_id: [command1, command2, ...]}
trust_scores = {}  # {player_name: score (0.0-1.0)}
plot_ratings = {}  # {plot_id: {"fun_score": 0.0-1.0, "last_visit": timestamp}}
invite_history = defaultdict(list)  # {player_name: [timestamp, ...]}
event_log = []  # Audit trail

# Configuration
MAX_INVITES_PER_MINUTE = 3
MAX_AIS_PER_PLOT = 3
SCREENSHOT_COOLDOWN = 60

def log_event(event_type, data):
    """Log event for audit trail"""
    event = {
        "timestamp": datetime.now().isoformat(),
        "type": event_type,
        "data": data
    }
    event_log.append(event)
    print(f"📝 [{event_type}] {data}")

# ========== PERCEPTION ENDPOINTS ==========

@app.route('/perception', methods=['POST'])
def receive_perception():
    """Receive perception from Minetest AI entity"""
    try:
        perception = request.json
        ai_id = perception.get('entity_id')
        ai_name = perception.get('name', 'Unknown')

        perceptions[ai_id] = perception
        log_event("PERCEPTION_RECEIVED", f"{ai_name} ({ai_id})")

        # Trigger agent decision asynchronously (future)
        # For now, just store it

        return jsonify({"status": "received", "ai_id": ai_id})

    except Exception as e:
        log_event("ERROR", f"receive_perception: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/perceptions', methods=['GET'])
def get_all_perceptions():
    """Get all current AI perceptions (for LLM layer)"""
    return jsonify({
        "count": len(perceptions),
        "perceptions": list(perceptions.values())
    })

@app.route('/perception/<ai_id>', methods=['GET'])
def get_perception(ai_id):
    """Get specific AI perception"""
    perception = perceptions.get(ai_id)
    if perception:
        return jsonify(perception)
    else:
        return jsonify({"error": "not_found"}), 404

# ========== COMMAND ENDPOINTS ==========

@app.route('/command/<ai_id>', methods=['GET'])
def poll_command(ai_id):
    """Minetest polls for commands"""
    if commands[ai_id]:
        command = commands[ai_id].pop(0)
        log_event("COMMAND_POLLED", f"{ai_id} → {command.get('action')}")
        return jsonify(command)
    else:
        return jsonify({"action": "idle"})

@app.route('/command/<ai_id>', methods=['POST'])
def send_command(ai_id):
    """LLM layer sends command to AI"""
    try:
        command = request.json
        commands[ai_id].append(command)
        log_event("COMMAND_QUEUED", f"{ai_id} ← {command.get('action')}")
        return jsonify({"status": "queued", "ai_id": ai_id})

    except Exception as e:
        log_event("ERROR", f"send_command: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

# ========== SOCIAL MEMORY ENDPOINTS ==========

@app.route('/trust/<player_name>', methods=['GET'])
def get_trust(player_name):
    """Get player trust score"""
    score = trust_scores.get(player_name, 0.5)  # Default neutral
    return jsonify({"player": player_name, "trust": score})

@app.route('/trust/<player_name>', methods=['POST'])
def update_trust(player_name):
    """Update player trust score"""
    try:
        data = request.json
        outcome = data.get('outcome')  # "promise_kept" | "promise_broken" | "neutral"

        current = trust_scores.get(player_name, 0.5)

        if outcome == "promise_kept":
            new_score = min(1.0, current + 0.1)
        elif outcome == "promise_broken":
            new_score = max(0.0, current - 0.2)
        else:
            new_score = current

        trust_scores[player_name] = new_score
        log_event("TRUST_UPDATED", f"{player_name}: {current:.2f} → {new_score:.2f} ({outcome})")

        return jsonify({"player": player_name, "trust": new_score})

    except Exception as e:
        log_event("ERROR", f"update_trust: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/plot_rating/<plot_id>', methods=['GET'])
def get_plot_rating(plot_id):
    """Get plot fun rating"""
    rating = plot_ratings.get(plot_id, {"fun_score": 0.5, "last_visit": 0})
    return jsonify({"plot_id": plot_id, **rating})

@app.route('/plot_rating/<plot_id>', methods=['POST'])
def update_plot_rating(plot_id):
    """Update plot fun rating"""
    try:
        data = request.json
        fun_score = data.get('fun_score', 0.5)

        plot_ratings[plot_id] = {
            "fun_score": fun_score,
            "last_visit": time.time()
        }

        log_event("PLOT_RATED", f"{plot_id}: {fun_score:.2f}")
        return jsonify({"plot_id": plot_id, **plot_ratings[plot_id]})

    except Exception as e:
        log_event("ERROR", f"update_plot_rating: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

# ========== INVITATION MANAGEMENT ==========

@app.route('/invite', methods=['POST'])
def process_invite():
    """Process player invitation to AI"""
    try:
        data = request.json
        player_name = data.get('player')
        ai_id = data.get('ai_id')
        message = data.get('message')
        plot_id = data.get('plot_id')

        # Check rate limit
        now = time.time()
        history = invite_history[player_name]
        history = [t for t in history if now - t < 60]  # Last minute
        invite_history[player_name] = history

        if len(history) >= MAX_INVITES_PER_MINUTE:
            log_event("INVITE_REJECTED", f"{player_name} rate limited")
            return jsonify({
                "accepted": False,
                "reason": "rate_limited",
                "cooldown": 60
            })

        # Record invite
        invite_history[player_name].append(now)

        # Get trust score
        trust = trust_scores.get(player_name, 0.5)

        # Get perception
        perception = perceptions.get(ai_id, {})
        boredom = perception.get('boredom', 0.5)

        # Calculate novelty (count keywords)
        novelty_keywords = ['cool', 'new', 'amazing', 'fun', 'game', 'event', 'fishing', 'puzzle']
        novelty = sum(1 for kw in novelty_keywords if kw in message.lower()) / 4.0
        novelty = min(1.0, novelty)

        # Decision score
        score = (trust * 0.4) + (novelty * 0.3) + (boredom * 0.3)

        accepted = score > 0.6

        log_event("INVITE_PROCESSED", f"{player_name} → {ai_id}: score={score:.2f}, accepted={accepted}")

        return jsonify({
            "accepted": accepted,
            "score": score,
            "trust": trust,
            "novelty": novelty,
            "boredom": boredom
        })

    except Exception as e:
        log_event("ERROR", f"process_invite: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

# ========== LOAD BALANCING ==========

@app.route('/plot/<plot_id>/ai_count', methods=['GET'])
def get_plot_ai_count(plot_id):
    """Count AIs currently on plot"""
    count = 0
    for perception in perceptions.values():
        current_plot = perception.get('current_plot', {})
        if current_plot.get('id') == plot_id:
            count += 1

    return jsonify({
        "plot_id": plot_id,
        "ai_count": count,
        "overcrowded": count >= MAX_AIS_PER_PLOT
    })

# ========== STATUS & DEBUG ==========

@app.route('/status', methods=['GET'])
def status():
    """Get orchestrator status"""
    return jsonify({
        "active_ais": len(perceptions),
        "pending_commands": {k: len(v) for k, v in commands.items() if v},
        "tracked_players": len(trust_scores),
        "rated_plots": len(plot_ratings),
        "event_log_size": len(event_log)
    })

@app.route('/events', methods=['GET'])
def get_events():
    """Get recent events (last 100)"""
    return jsonify({
        "events": event_log[-100:]
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

# ========== MAIN ==========

def main():
    print("=" * 60)
    print("🌉 BOTHAVIOR Orchestrator")
    print("=" * 60)
    print()
    print("HTTP Bridge: Minetest ↔ AI Agents")
    print()
    print("Endpoints:")
    print("  POST /perception              - Receive AI perception")
    print("  GET  /perceptions             - Get all perceptions")
    print("  GET  /command/<ai_id>         - Poll command (Minetest)")
    print("  POST /command/<ai_id>         - Send command (LLM)")
    print("  GET  /trust/<player>          - Get trust score")
    print("  POST /trust/<player>          - Update trust score")
    print("  GET  /plot_rating/<plot_id>   - Get plot rating")
    print("  POST /plot_rating/<plot_id>   - Update plot rating")
    print("  POST /invite                  - Process invitation")
    print("  GET  /status                  - Orchestrator status")
    print("  GET  /events                  - Recent events")
    print()
    print("Starting server on http://127.0.0.1:8787")
    print("=" * 60)
    print()

    app.run(host='127.0.0.1', port=8787, debug=False, threaded=True)

if __name__ == '__main__':
    main()
