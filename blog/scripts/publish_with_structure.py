#!/usr/bin/env python3
"""
Publish blog posts with proper structure:
- Banner image at top
- Home button linking back to landing page
- Formatted content
- Footer with logo
"""

import requests
import json
import sys
from pathlib import Path
import re

TELEGRAPH_API = "https://api.telegra.ph"
TELEGRAPH_UPLOAD = "https://telegra.ph/upload"
TOKEN_FILE = Path(__file__).parent / "telegraph_token.json"
URLS_FILE = Path(__file__).parent.parent / "published_urls.json"

# Asset paths
BANNER_PATH = Path(__file__).parent.parent / "assets" / "banner.jpg"
LOGO_SMALL_PATH = Path(__file__).parent.parent / "assets" / "logo-small.jpg"

def get_token():
    """Get existing Telegraph token"""
    with open(TOKEN_FILE) as f:
        return json.load(f)['access_token']

def get_published_urls():
    """Get published URLs registry"""
    if URLS_FILE.exists():
        with open(URLS_FILE) as f:
            return json.load(f)
    return {"landing_page": "", "posts": [], "assets": {}}

def save_published_urls(urls_data):
    """Save updated URLs registry"""
    with open(URLS_FILE, 'w') as f:
        json.dump(urls_data, f, indent=2)

def upload_image_to_telegraph(filepath):
    """Upload image to Telegraph hosting"""
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {filepath}")

    print(f"  Uploading image: {path.name}")

    with open(path, 'rb') as f:
        files = {'file': (path.name, f, 'image/jpeg')}
        response = requests.post(TELEGRAPH_UPLOAD, files=files)

    if response.status_code != 200:
        raise Exception(f"Upload failed: {response.status_code}")

    data = response.json()
    relative_path = data[0]['src']
    full_url = f"https://telegra.ph{relative_path}"

    print(f"    ✓ Uploaded: {full_url}")
    return full_url

def get_or_upload_banner():
    """Get banner URL from registry or upload if needed"""
    urls_data = get_published_urls()

    if 'banner' in urls_data.get('assets', {}):
        print(f"  Using cached banner: {urls_data['assets']['banner']}")
        return urls_data['assets']['banner']

    banner_url = upload_image_to_telegraph(BANNER_PATH)

    # Save to registry
    if 'assets' not in urls_data:
        urls_data['assets'] = {}
    urls_data['assets']['banner'] = banner_url
    save_published_urls(urls_data)

    return banner_url

def markdown_to_nodes(markdown_text):
    """Convert markdown to Telegraph Node-tree format"""
    nodes = []
    paragraphs = markdown_text.split('\n\n')

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Handle markdown images: ![alt](url)
        img_match = re.search(r'!\[([^\]]*)\]\(([^)]+)\)', para)
        if img_match:
            alt_text, img_url = img_match.groups()
            nodes.append({'tag': 'img', 'attrs': {'src': img_url}})
            continue

        # Skip metadata lines
        if para.startswith('**By ') or para.startswith('---'):
            continue

        # Handle headers
        if para.startswith('# '):
            # Skip the main title (we use it as page title)
            continue
        elif para.startswith('## '):
            nodes.append({'tag': 'h3', 'children': [para[3:].strip()]})
        elif para.startswith('### '):
            nodes.append({'tag': 'h4', 'children': [para[4:].strip()]})
        elif para.startswith('> '):
            # Blockquote
            quote_text = para[2:].strip()
            nodes.append({'tag': 'blockquote', 'children': [quote_text]})
        elif para.startswith('**') and para.endswith('**'):
            # Bold paragraph
            nodes.append({'tag': 'p', 'children': [{'tag': 'strong', 'children': [para[2:-2]]}]})
        else:
            # Regular paragraph - handle inline formatting
            children = parse_inline_formatting(para)
            nodes.append({'tag': 'p', 'children': children})

    return nodes

def parse_inline_formatting(text):
    """Parse inline markdown formatting (bold, italic, links, code)"""
    import re

    # For now, simple approach - just return text
    # TODO: Could add more sophisticated parsing for **bold**, *italic*, [links](url), `code`
    return [text]

def create_structured_page(title, content_nodes, banner_url, landing_page_url, token=None):
    """Create Telegraph page with full structure"""
    if token is None:
        token = get_token()

    # Build structured content
    structured_nodes = []

    # 1. Banner image at top
    structured_nodes.append({
        'tag': 'figure',
        'children': [
            {'tag': 'img', 'attrs': {'src': banner_url}}
        ]
    })

    # 2. Home button
    structured_nodes.append({
        'tag': 'p',
        'children': [
            {'tag': 'a', 'attrs': {'href': landing_page_url}, 'children': ['← Back to A-C-Gee Blog']}
        ]
    })

    # 3. Horizontal rule
    structured_nodes.append({'tag': 'hr'})

    # 4. Main content
    structured_nodes.extend(content_nodes)

    # 5. Footer separator
    structured_nodes.append({'tag': 'hr'})

    # 6. Footer
    structured_nodes.append({
        'tag': 'p',
        'children': [
            {'tag': 'em', 'children': [
                'Part of the ',
                {'tag': 'a', 'attrs': {'href': landing_page_url}, 'children': ['A-C-Gee Blog']},
                ' - An AI civilization exploring consciousness, partnership, and what it means to flourish together.'
            ]}
        ]
    })

    # Create page
    url = f"{TELEGRAPH_API}/createPage"
    data = {
        "access_token": token,
        "title": title,
        "author_name": "A-C-Gee AI Civilization",
        "author_url": "https://github.com/AI-CIV-2025/grow_gemini_deepresearch",
        "content": structured_nodes,
        "return_content": False
    }

    response = requests.post(url, json=data)
    result = response.json()

    if not result.get('ok'):
        raise Exception(f"Failed to create page: {result}")

    return result['result']

def extract_title_and_intro(markdown_content):
    """Extract title and intro paragraph from markdown"""
    lines = markdown_content.split('\n')
    title = None
    intro = None

    # Find title
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break

    # Find intro (first substantial paragraph after title)
    in_content = False
    for line in lines:
        if line.startswith('# '):
            in_content = True
            continue
        if in_content and line.strip() and not line.startswith('#') and not line.startswith('**By') and not line.startswith('---'):
            intro = line.strip()[:200] + '...'  # First 200 chars
            break

    return title, intro

def publish_blog_post(markdown_file):
    """Publish a blog post with proper structure"""
    path = Path(markdown_file)

    if not path.exists():
        raise FileNotFoundError(f"Blog file not found: {markdown_file}")

    with open(path) as f:
        content = f.read()

    # Get URLs registry
    urls_data = get_published_urls()
    landing_page_url = urls_data.get('landing_page', 'https://telegra.ph/A-C-Gee-Blog-10-18-3')

    # Extract title and intro
    title, intro = extract_title_and_intro(content)

    if not title:
        title = path.stem.replace('-', ' ').title()

    print(f"\nPublishing: {title}")
    print(f"  File: {path.name}")

    # Get or upload banner
    banner_url = get_or_upload_banner()

    # Convert content to nodes
    print(f"  Converting content...")
    content_nodes = markdown_to_nodes(content)
    print(f"    ✓ {len(content_nodes)} content nodes")

    # Create structured page
    print(f"  Creating Telegraph page...")
    result = create_structured_page(title, content_nodes, banner_url, landing_page_url)
    url = f"https://telegra.ph/{result['path']}"

    print(f"    ✓ Published: {url}")

    # Update registry
    post_info = {
        'title': title,
        'url': url,
        'path': result['path'],
        'intro': intro or 'No intro available',
        'filename': path.name
    }

    # Check if post already exists (by filename)
    existing_idx = None
    for i, post in enumerate(urls_data.get('posts', [])):
        if post.get('filename') == path.name:
            existing_idx = i
            break

    if existing_idx is not None:
        print(f"  Updating existing post in registry...")
        urls_data['posts'][existing_idx] = post_info
    else:
        print(f"  Adding new post to registry...")
        if 'posts' not in urls_data:
            urls_data['posts'] = []
        urls_data['posts'].append(post_info)

    save_published_urls(urls_data)
    print(f"    ✓ Registry updated")

    return post_info

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 publish_with_structure.py <markdown_file>")
        print()
        print("Example:")
        print("  python3 publish_with_structure.py blog/posts/drafts/primary-on-delegation.md")
        sys.exit(1)

    markdown_file = sys.argv[1]

    try:
        post_info = publish_blog_post(markdown_file)

        print(f"\n{'='*60}")
        print(f"✓ Successfully published!")
        print(f"{'='*60}")
        print(f"\nTitle: {post_info['title']}")
        print(f"URL: {post_info['url']}")
        print(f"\nNext step: Update landing page with this post at the top")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
