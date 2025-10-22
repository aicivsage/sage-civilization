#!/usr/bin/env python3
"""
Publish a single blog post to Telegraph (using node-tree format)
"""

import requests
import json
import sys
from pathlib import Path

TELEGRAPH_API = "https://api.telegra.ph"
TOKEN_FILE = Path(__file__).parent / "telegraph_token.json"

def get_token():
    """Get existing token"""
    with open(TOKEN_FILE) as f:
        return json.load(f)['access_token']

def markdown_to_nodes(markdown_text):
    """Convert markdown to Telegraph Node-tree format"""
    nodes = []
    paragraphs = markdown_text.split('\n\n')

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Handle headers
        if para.startswith('# '):
            nodes.append({'tag': 'h3', 'children': [para[2:].strip()]})
        elif para.startswith('## '):
            nodes.append({'tag': 'h4', 'children': [para[3:].strip()]})
        elif para.startswith('### '):
            nodes.append({'tag': 'h4', 'children': [para[4:].strip()]})
        elif para.startswith('---'):
            # Skip horizontal rules
            continue
        elif para.startswith('**') and para.endswith('**'):
            # Bold paragraph
            nodes.append({'tag': 'p', 'children': [{'tag': 'strong', 'children': [para[2:-2]]}]})
        else:
            # Regular paragraph
            nodes.append({'tag': 'p', 'children': [para]})

    return nodes

def create_page(title, content_nodes, token=None):
    """Create Telegraph page with Node-tree content"""
    if token is None:
        token = get_token()

    url = f"{TELEGRAPH_API}/createPage"
    data = {
        "access_token": token,
        "title": title,
        "author_name": "A-C-Gee AI Civilization",
        "author_url": "https://github.com/AI-CIV-2025/grow_gemini_deepresearch",
        "content": content_nodes,
        "return_content": False
    }

    response = requests.post(url, json=data)
    result = response.json()

    if not result.get('ok'):
        raise Exception(f"Failed to create page: {result}")

    return result['result']

def publish_blog_post(filepath):
    """Publish a single blog post"""
    path = Path(filepath)
    with open(path) as f:
        content = f.read()

    # Extract title
    lines = content.split('\n')
    title = None
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break

    if not title:
        title = path.stem.replace('-', ' ').title()

    # Convert to nodes
    nodes = markdown_to_nodes(content)

    # Create page
    print(f"Publishing: {title}")
    print(f"  Content: {len(content)} chars → {len(nodes)} nodes")
    result = create_page(title, nodes)
    url = f"https://telegra.ph/{result['path']}"

    print(f"  ✓ Published: {url}")

    return {
        'title': title,
        'url': url,
        'path': result['path'],
        'filename': path.name
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 publish_single.py <markdown_file>")
        sys.exit(1)

    markdown_file = sys.argv[1]
    post_info = publish_blog_post(markdown_file)

    print(f"\n🎉 Published successfully!")
    print(f"\nTitle: {post_info['title']}")
    print(f"URL: {post_info['url']}")

    return post_info['url']

if __name__ == '__main__':
    main()
