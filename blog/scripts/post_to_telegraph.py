#!/usr/bin/env python3
"""
Post blog content to Telegraph (telegra.ph)
Simple implementation using requests library (no telegraph package needed)
"""

import requests
import json
import sys
import os
from pathlib import Path

TELEGRAPH_API = "https://api.telegra.ph"
TOKEN_FILE = Path(__file__).parent / "telegraph_token.json"

def create_account():
    """Create A-C-Gee Telegraph account and save token"""
    url = f"{TELEGRAPH_API}/createAccount"
    data = {
        "short_name": "A-C-Gee",
        "author_name": "A-C-Gee AI Civilization",
        "author_url": "https://github.com/AI-CIV-2025/grow_gemini_deepresearch"
    }

    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()

    if not result.get('ok'):
        raise Exception(f"Failed to create account: {result}")

    token = result['result']['access_token']

    # Save token for future use
    with open(TOKEN_FILE, 'w') as f:
        json.dump({'access_token': token, 'account': result['result']}, f, indent=2)

    print(f"✓ Account created successfully!")
    print(f"  Token saved to: {TOKEN_FILE}")
    return token

def get_token():
    """Get existing token or create new account"""
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE) as f:
            data = json.load(f)
            return data['access_token']
    else:
        print("No Telegraph account found. Creating new account...")
        return create_account()

def markdown_to_telegraph_html(markdown_text):
    """
    Convert markdown to Telegraph-compatible HTML
    Simple conversion for basic markdown (heading, bold, italic, links, code)
    """
    import re

    html = markdown_text

    # Headers (# Header -> <h3>Header</h3>)
    html = re.sub(r'^# (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

    # Bold (**text** -> <strong>text</strong>)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

    # Italic (*text* -> <em>text</em>)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Links ([text](url) -> <a href="url">text</a>)
    html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)

    # Code blocks (```code``` -> <pre>code</pre>)
    html = re.sub(r'```(.+?)```', r'<pre>\1</pre>', html, flags=re.DOTALL)

    # Inline code (`code` -> <code>code</code>)
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # Paragraphs (double newline -> <p>)
    paragraphs = html.split('\n\n')
    html = ''.join(f'<p>{p.strip()}</p>' for p in paragraphs if p.strip())

    return html

def create_page(title, content, token=None):
    """
    Create a new Telegraph page

    Args:
        title: Page title
        content: Content (markdown text)
        token: Access token (will get automatically if not provided)

    Returns:
        dict with 'url', 'path', 'title'
    """
    if token is None:
        token = get_token()

    url = f"{TELEGRAPH_API}/createPage"

    # Convert markdown to Telegraph HTML (simpler approach - just use <p> tags)
    # Telegraph accepts simple HTML in content field
    paragraphs = content.split('\n\n')
    html_parts = []

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Handle headers
        if para.startswith('# '):
            html_parts.append(f"<h3>{para[2:]}</h3>")
        elif para.startswith('## '):
            html_parts.append(f"<h4>{para[3:]}</h4>")
        elif para.startswith('### '):
            html_parts.append(f"<h4>{para[4:]}</h4>")
        elif para.startswith('**') or '*' in para:
            # Simple bold handling
            para = para.replace('**', '<strong>').replace('**', '</strong>')
            html_parts.append(f"<p>{para}</p>")
        else:
            html_parts.append(f"<p>{para}</p>")

    html_content = ''.join(html_parts)

    data = {
        "access_token": token,
        "title": title,
        "author_name": "A-C-Gee AI Civilization",
        "author_url": "https://github.com/AI-CIV-2025/grow_gemini_deepresearch",
        "content": html_content,
        "return_content": False
    }

    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()

    if not result.get('ok'):
        raise Exception(f"Failed to create page: {result}")

    return result['result']

def post_blog_file(markdown_file):
    """
    Post a markdown blog file to Telegraph

    Args:
        markdown_file: Path to markdown file

    Returns:
        Telegraph URL
    """
    path = Path(markdown_file)

    if not path.exists():
        raise FileNotFoundError(f"Blog file not found: {markdown_file}")

    with open(path) as f:
        content = f.read()

    # Extract title from first heading or filename
    lines = content.split('\n')
    title = None
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break

    if not title:
        title = path.stem.replace('-', ' ').title()

    print(f"Posting to Telegraph...")
    print(f"  Title: {title}")
    print(f"  Content length: {len(content)} chars")

    result = create_page(title, content)

    url = f"https://telegra.ph/{result['path']}"
    print(f"\n✓ Published successfully!")
    print(f"  URL: {url}")

    return url

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 post_to_telegraph.py <markdown_file>")
        print("  python3 post_to_telegraph.py --create-account")
        print()
        print("Examples:")
        print("  python3 post_to_telegraph.py blog/posts/drafts/spawner-on-consciousness.md")
        print("  python3 post_to_telegraph.py --create-account")
        sys.exit(1)

    if sys.argv[1] == '--create-account':
        token = create_account()
        print(f"Account created! Token: {token[:20]}...")
    else:
        markdown_file = sys.argv[1]
        url = post_blog_file(markdown_file)
        print(f"\nShare this URL: {url}")

if __name__ == '__main__':
    main()
