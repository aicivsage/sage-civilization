#!/usr/bin/env python3
"""Send all 13 Dream Forge visions as individual emails to Corey."""

import sys
import os
import time

# Add tools to path
sys.path.insert(0, '/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools')

from send_html_email import send_html_email

VISION_DIR = "/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/meta-cognition/dream-forge-20251005"

VISION_FILES = [
    ("researcher-dream.md", "Researcher"),
    ("architect-dream.md", "Architect"),
    ("coder-dream.md", "Coder"),
    ("tester-dream.md", "Tester"),
    ("human-liaison-dream.md", "Human-Liaison"),
    ("auditor-dream.md", "Auditor"),
    ("spawner-dream.md", "Spawner"),
    ("vote-counter-dream.md", "Vote-Counter"),
    ("reviewer-dream.md", "Reviewer"),
    ("email-reporter-dream.md", "Email-Reporter"),
    ("file-guardian-dream.md", "File-Guardian"),
    ("email-monitor-dream.md", "Email-Monitor"),
    ("reviewer-audit-dream.md", "Reviewer-Audit"),
]

def read_vision(filename):
    """Read a vision file."""
    filepath = os.path.join(VISION_DIR, filename)
    with open(filepath, 'r') as f:
        return f.read()

def send_vision_email(agent_name, vision_content):
    """Send a single vision as an HTML email."""

    # Convert markdown to simple HTML
    # Replace markdown headers with HTML
    lines = vision_content.split('\n')
    html_lines = []

    for line in lines:
        if line.startswith('# '):
            html_lines.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('> '):
            html_lines.append(f'<blockquote style="border-left: 3px solid #2563eb; padding-left: 15px; margin: 15px 0;">{line[2:]}</blockquote>')
        elif line.strip() == '':
            html_lines.append('<br>')
        elif line.startswith('- '):
            html_lines.append(f'<li>{line[2:]}</li>')
        else:
            html_lines.append(f'<p>{line}</p>')

    html_body = '\n'.join(html_lines)

    # Wrap in container
    full_html = f"""
    <div style="max-width: 700px;">
        <div style="background: #f3f4f6; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <strong>Dream Forge Vision #{VISION_FILES.index((filename, agent_name)) + 1} of 13</strong><br>
            <strong>Agent:</strong> {agent_name}
        </div>

        {html_body}

        <div style="margin-top: 30px; padding-top: 15px; border-top: 1px solid #e5e7eb;">
            <small>This is vision {VISION_FILES.index((filename, agent_name)) + 1} of 13 from the Dream Forge ceremony (Oct 5, 2025)</small>
        </div>
    </div>
    """

    subject = f"Dream Forge Vision: {agent_name} (#{VISION_FILES.index((filename, agent_name)) + 1}/13)"

    result = send_html_email(
        to="coreycmusic@gmail.com",
        subject=subject,
        html_body=full_html,
        from_name=f"A-C-Gee {agent_name}"
    )

    return result

if __name__ == '__main__':
    print("\n=== SENDING ALL 13 DREAM FORGE VISIONS ===\n")

    successful = 0
    failed = 0

    for filename, agent_name in VISION_FILES:
        print(f"Sending {agent_name} vision...")

        try:
            vision_content = read_vision(filename)
            result = send_vision_email(agent_name, vision_content)

            if result:
                successful += 1
                print(f"  ✅ Sent successfully\n")
            else:
                failed += 1
                print(f"  ❌ Failed to send\n")

            # Small delay between emails
            time.sleep(2)

        except Exception as e:
            failed += 1
            print(f"  ❌ Error: {e}\n")

    print(f"\n=== COMPLETE ===")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"\nCorey asked for these on Oct 5, 10:40am - delivering now!\n")
