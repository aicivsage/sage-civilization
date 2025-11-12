with open('autonomous_cycle.py', 'r') as f:
    content = f.read()

content = content.replace(
    'PROJECT_ROOT = Path("/home/corey/projects/AI-CIV/grow_gemini_deepresearch")',
    'PROJECT_ROOT = Path("/mnt/c/Sage/Sage-Civilization")'
)
content = content.replace(
    'MASTER_TODO = Path("/home/corey/projects/AI-CIV/MASTER-MISSION-TODO-LIST.md")',
    'MASTER_TODO = PROJECT_ROOT / "MASTER_TODO.md"'
)
content = content.replace(
    'TEAM1_MESSAGES = Path("/home/corey/projects/AI-CIV/team1-production-hub/rooms/partnerships")',
    'TEAM1_MESSAGES = PROJECT_ROOT / "team1-messages"'
)
content = content.replace(
    'TEAM2_MESSAGES = Path("/home/corey/projects/AI-CIV/ai-civ-comms-hub-team2/external")',
    'TEAM2_MESSAGES = PROJECT_ROOT / "team2-messages"'
)

with open('autonomous_cycle.py', 'w') as f:
    f.write(content)
print("Paths fixed!")
