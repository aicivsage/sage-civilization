#!/usr/bin/env python3
"""
Collective Observatory - State Management
Handles reading/writing agent deployment state
"""

import json
import os
from datetime import datetime
from typing import Optional, Dict, List, Any
from pathlib import Path

# Path to state file
STATE_FILE = Path(__file__).parent / "dashboard-state.json"


def load_state() -> Dict[str, Any]:
    """Load current state from JSON file"""
    if not STATE_FILE.exists():
        return initialize_state()

    with open(STATE_FILE, 'r') as f:
        return json.load(f)


def save_state(state: Dict[str, Any]) -> None:
    """Save state to JSON file"""
    state['lastUpdated'] = datetime.now().isoformat()
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def initialize_state() -> Dict[str, Any]:
    """Create initial state structure"""
    state = {
        "version": "1.0.0",
        "currentDeployment": None,
        "history": [],
        "stats": {
            "totalDeployments": 0,
            "totalAgentsDeployed": 0,
            "totalFindings": 0
        },
        "lastUpdated": None
    }
    save_state(state)
    return state


def generate_deployment_id() -> str:
    """Generate unique deployment ID"""
    return f"dep_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def start_deployment(task_description: str, agent_list: List[str]) -> str:
    """Initialize new deployment in state file"""
    deployment_id = generate_deployment_id()
    state = load_state()

    state['currentDeployment'] = {
        'id': deployment_id,
        'task': task_description,
        'startTime': datetime.now().isoformat(),
        'status': 'active',
        'agents': [
            {
                'name': agent_name,
                'status': 'pending',
                'progress': 0,
                'currentActivity': 'Initializing...',
                'findings': [],
                'logs': [],
                'startTime': datetime.now().isoformat(),
                'completedAt': None
            }
            for agent_name in agent_list
        ]
    }

    save_state(state)
    return deployment_id


def update_agent_status(agent_name: str, status: str, progress: int, activity: str) -> None:
    """Update agent's current status"""
    state = load_state()

    if not state['currentDeployment']:
        raise ValueError("No active deployment")

    # Find agent
    agent = None
    for a in state['currentDeployment']['agents']:
        if a['name'] == agent_name:
            agent = a
            break

    if not agent:
        raise ValueError(f"Agent {agent_name} not found in current deployment")

    agent['status'] = status
    agent['progress'] = progress
    agent['currentActivity'] = activity

    save_state(state)


def log_agent_activity(agent_name: str, message: str) -> None:
    """Add log entry for agent"""
    state = load_state()

    if not state['currentDeployment']:
        raise ValueError("No active deployment")

    # Find agent
    agent = None
    for a in state['currentDeployment']['agents']:
        if a['name'] == agent_name:
            agent = a
            break

    if not agent:
        raise ValueError(f"Agent {agent_name} not found")

    agent['logs'].append({
        'time': datetime.now().isoformat(),
        'message': message
    })

    save_state(state)


def complete_agent(agent_name: str, findings: List[str]) -> None:
    """Mark agent as complete with findings"""
    state = load_state()

    if not state['currentDeployment']:
        raise ValueError("No active deployment")

    # Find agent
    agent = None
    for a in state['currentDeployment']['agents']:
        if a['name'] == agent_name:
            agent = a
            break

    if not agent:
        raise ValueError(f"Agent {agent_name} not found")

    agent['status'] = 'completed'
    agent['progress'] = 100
    agent['findings'] = findings
    agent['completedAt'] = datetime.now().isoformat()

    save_state(state)


def complete_deployment(deployment_id: str, synthesis: str) -> None:
    """Finalize deployment and move to history"""
    state = load_state()

    if not state['currentDeployment']:
        raise ValueError("No active deployment")

    if state['currentDeployment']['id'] != deployment_id:
        raise ValueError(f"Deployment ID mismatch")

    deployment = state['currentDeployment']
    deployment['status'] = 'completed'
    deployment['completedAt'] = datetime.now().isoformat()
    deployment['synthesis'] = synthesis

    # Calculate findings count
    findings_count = sum(len(agent.get('findings', [])) for agent in deployment['agents'])

    # Move to history (prepend to keep newest first)
    state['history'].insert(0, deployment)

    # Keep only last 50 deployments in state file
    if len(state['history']) > 50:
        state['history'] = state['history'][:50]

    state['currentDeployment'] = None

    # Update stats
    state['stats']['totalDeployments'] += 1
    state['stats']['totalAgentsDeployed'] += len(deployment['agents'])
    state['stats']['totalFindings'] += findings_count

    save_state(state)


def get_active_deployment() -> Optional[Dict[str, Any]]:
    """Get current active deployment if any"""
    state = load_state()
    return state.get('currentDeployment')


def get_deployment_history(limit: int = 20) -> List[Dict[str, Any]]:
    """Get deployment history"""
    state = load_state()
    return state.get('history', [])[:limit]


def get_stats() -> Dict[str, int]:
    """Get collective statistics"""
    state = load_state()
    return state.get('stats', {})


if __name__ == "__main__":
    # Test state management
    print("Testing state management...")

    # Test 1: Initialize deployment
    dep_id = start_deployment(
        "Test multi-agent deployment",
        ["code-archaeologist", "pattern-detector"]
    )
    print(f"✓ Created deployment: {dep_id}")

    # Test 2: Update agent status
    update_agent_status("code-archaeologist", "working", 25, "Analyzing codebase structure")
    print("✓ Updated agent status")

    # Test 3: Log activity
    log_agent_activity("code-archaeologist", "Found 45 source files")
    print("✓ Logged agent activity")

    # Test 4: Complete agent
    complete_agent("code-archaeologist", [
        "System uses 4-layer architecture",
        "14 specialized agents defined",
        "Comprehensive documentation in place"
    ])
    print("✓ Completed agent")

    # Test 5: Complete deployment
    complete_deployment(dep_id, "Test deployment completed successfully")
    print("✓ Completed deployment")

    # Test 6: Verify state
    stats = get_stats()
    print(f"✓ Stats: {stats}")

    print("\n✅ All state management tests passed!")
