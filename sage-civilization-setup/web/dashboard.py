#!/usr/bin/env python3
"""
Web Dashboard for Sage AI Civilization
Real-time monitoring interface for the agent civilization
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)

def load_json_safe(filepath, default=None):
    """Safely load JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return default or {}

def load_text_safe(filepath, default=""):
    """Safely load text file"""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except:
        return default

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/status')
def api_status():
    """Get overall system status"""
    agents = load_json_safe('memories/agents/agent_registry.json', {})
    architecture = load_json_safe('memories/system/architectural_state.json', {})
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'agent_count': len(agents),
        'architecture': architecture.get('topology', 'Unknown'),
        'phase': architecture.get('phase', 'Unknown'),
        'status': 'operational'
    })

@app.route('/api/agents')
def api_agents():
    """Get list of all agents"""
    agents = load_json_safe('memories/agents/agent_registry.json', {})
    return jsonify(agents)

@app.route('/api/agent/<agent_id>')
def api_agent_detail(agent_id):
    """Get detailed info about specific agent"""
    agents = load_json_safe('memories/agents/agent_registry.json', {})
    agent = agents.get(agent_id, {})
    
    # Try to load performance log
    perf_log_path = f'memories/agents/{agent_id}/performance_log.json'
    performance = load_json_safe(perf_log_path, [])
    
    return jsonify({
        'agent': agent,
        'performance': performance[-10:]  # Last 10 entries
    })

@app.route('/api/goals')
def api_goals():
    """Get current goals"""
    goals = load_text_safe('memories/system/goals.md', 'No goals set')
    return jsonify({'goals': goals})

@app.route('/api/votes')
def api_votes():
    """Get recent votes"""
    voting_dir = Path('memories/communication/voting_booth')
    votes = []
    
    if voting_dir.exists():
        for vote_file in sorted(voting_dir.glob('*.json'), reverse=True)[:10]:
            vote_data = load_json_safe(vote_file)
            if vote_data:
                votes.append(vote_data)
    
    return jsonify(votes)

@app.route('/api/messages')
def api_messages():
    """Get recent message bus messages"""
    msg_dir = Path('memories/communication/message_bus')
    messages = []
    
    if msg_dir.exists():
        for msg_file in sorted(msg_dir.rglob('*.json'), reverse=True)[:20]:
            msg_data = load_json_safe(msg_file)
            if msg_data:
                msg_data['file'] = msg_file.name
                messages.append(msg_data)
    
    return jsonify(messages)

@app.route('/api/logs/<log_type>')
def api_logs(log_type):
    """Get logs by type (email, telegram, system)"""
    log_dir = Path(f'memories/communication/{log_type}_logs')
    logs = []
    
    if log_dir.exists():
        # Get today's log file
        today = datetime.now().strftime('%Y%m%d')
        log_file = log_dir / f"{log_type}_log_{today}.json"
        
        if log_file.exists():
            logs = load_json_safe(log_file, [])
    
    return jsonify(logs)

@app.route('/api/architecture')
def api_architecture():
    """Get architectural state"""
    architecture = load_json_safe('memories/system/architectural_state.json', {})
    evolution = load_json_safe('memories/system/evolution_log.json', [])
    
    return jsonify({
        'current': architecture,
        'history': evolution[-10:]  # Last 10 changes
    })

@app.route('/api/search')
def api_search():
    """Search through system data"""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    results = {
        'agents': [],
        'messages': [],
        'votes': []
    }
    
    # Search agents
    agents = load_json_safe('memories/agents/agent_registry.json', {})
    for agent_id, agent_data in agents.items():
        if query in agent_id.lower() or query in str(agent_data).lower():
            results['agents'].append({
                'id': agent_id,
                'data': agent_data
            })
    
    return jsonify(results)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.getenv('DASHBOARD_PORT', 5000))
    host = os.getenv('DASHBOARD_HOST', '0.0.0.0')
    
    print(f"""
    ╔════════════════════════════════════════════╗
    ║  Sage AI Civilization Dashboard           ║
    ║                                            ║
    ║  🌐 Running on http://{host}:{port}     ║
    ║                                            ║
    ║  Press Ctrl+C to stop                      ║
    ╚════════════════════════════════════════════╝
    """)
    
    app.run(host=host, port=port, debug=True)
