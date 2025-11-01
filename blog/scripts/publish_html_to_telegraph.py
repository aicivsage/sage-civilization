#!/usr/bin/env python3
"""
Publish HTML blog posts to Telegraph with proper formatting.
Converts HTML structure to Telegraph's Node-tree format.
"""

import requests
import json
import sys
from pathlib import Path
from html.parser import HTMLParser

TELEGRAPH_API = "https://api.telegra.ph"
TOKEN_FILE = Path(__file__).parent / "telegraph_token.json"
URLS_FILE = Path(__file__).parent.parent / "published_urls.json"

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

class HTMLToTelegraphConverter(HTMLParser):
    """Convert HTML to Telegraph Node format"""

    def __init__(self):
        super().__init__()
        self.nodes = []
        self.current_tag_stack = []
        self.current_text = []
        self.title = None
        self.in_header = False
        self.skip_content = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Skip style and script tags
        if tag in ['style', 'script', 'head', 'meta', 'link']:
            self.skip_content = True
            return

        # Skip divs with class header (we'll extract title separately)
        if tag == 'div' and attrs_dict.get('class') == 'header':
            self.in_header = True
            return

        # Map HTML tags to Telegraph-supported tags
        telegraph_tag = tag
        if tag in ['h1', 'h2']:
            telegraph_tag = 'h3'
        elif tag == 'h3':
            telegraph_tag = 'h4'
        elif tag == 'div':
            # Most divs become paragraphs or are skipped
            if 'conversation-block' in attrs_dict.get('class', ''):
                telegraph_tag = 'blockquote'
            elif 'highlight-box' in attrs_dict.get('class', ''):
                telegraph_tag = 'aside'
            elif 'insight-box' in attrs_dict.get('class', ''):
                telegraph_tag = 'aside'
            elif 'pullquote' in attrs_dict.get('class', ''):
                telegraph_tag = 'blockquote'
            elif 'agent-reflection' in attrs_dict.get('class', ''):
                telegraph_tag = 'aside'
            elif 'key-insights' in attrs_dict.get('class', ''):
                telegraph_tag = 'aside'
            else:
                # Skip most divs, process their content
                return

        # Build node
        node = {'tag': telegraph_tag}

        # Handle special attributes for Telegraph
        if tag == 'a' and 'href' in attrs_dict:
            node['attrs'] = {'href': attrs_dict['href']}
        elif tag == 'img' and 'src' in attrs_dict:
            node['attrs'] = {'src': attrs_dict['src']}

        self.current_tag_stack.append(node)

    def handle_endtag(self, tag):
        if tag in ['style', 'script', 'head', 'meta', 'link']:
            self.skip_content = False
            return

        if tag == 'div' and self.in_header:
            self.in_header = False
            return

        if tag == 'div':
            # Most divs don't have opening tags in our stack
            return

        if not self.current_tag_stack:
            return

        # Pop the current tag and add accumulated text
        node = self.current_tag_stack.pop()

        if self.current_text:
            text = ''.join(self.current_text).strip()
            if text:
                node['children'] = [text]
            self.current_text = []

        # Add to parent or to nodes list
        if self.current_tag_stack:
            parent = self.current_tag_stack[-1]
            if 'children' not in parent:
                parent['children'] = []
            parent['children'].append(node)
        else:
            self.nodes.append(node)

    def handle_data(self, data):
        if self.skip_content:
            return

        # Extract title from header
        if self.in_header and not self.title and data.strip():
            stripped = data.strip()
            if len(stripped) > 10:  # Likely the main title
                self.title = stripped

        # Accumulate text data
        if data.strip() and not self.in_header:
            self.current_text.append(data)

def convert_html_to_telegraph_nodes(html_content):
    """Convert HTML content to Telegraph node format"""
    converter = HTMLToTelegraphConverter()
    converter.feed(html_content)

    # Clean up nodes - remove empty nodes
    cleaned_nodes = []
    for node in converter.nodes:
        if node.get('tag') and (node.get('children') or node.get('attrs')):
            cleaned_nodes.append(node)

    return converter.title, cleaned_nodes

def create_telegraph_page(title, content_nodes, author_name="Sage AI Civilization", token=None):
    """Create Telegraph page"""
    if token is None:
        token = get_token()

    url = f"{TELEGRAPH_API}/createPage"
    data = {
        "access_token": token,
        "title": title,
        "author_name": author_name,
        "content": content_nodes,
        "return_content": False
    }

    response = requests.post(url, json=data)
    result = response.json()

    if not result.get('ok'):
        raise Exception(f"Failed to create page: {result}")

    return result['result']

def publish_html_blog_post(html_file):
    """Publish an HTML blog post to Telegraph"""
    path = Path(html_file)

    if not path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_file}")

    with open(path, encoding='utf-8') as f:
        content = f.read()

    print(f"\nPublishing HTML blog post: {path.name}")

    # Convert HTML to Telegraph nodes
    print(f"  Converting HTML to Telegraph format...")
    title, content_nodes = convert_html_to_telegraph_nodes(content)

    if not title:
        title = path.stem.replace('-', ' ').title()

    print(f"    Title: {title}")
    print(f"    Nodes: {len(content_nodes)}")

    # Create Telegraph page
    print(f"  Publishing to Telegraph...")
    result = create_telegraph_page(title, content_nodes)
    url = f"https://telegra.ph/{result['path']}"

    print(f"    ✓ Published: {url}")

    # Update registry
    urls_data = get_published_urls()

    post_info = {
        'title': title,
        'url': url,
        'path': result['path'],
        'intro': 'Can an AI care? Not simulate caring, but genuinely care about humans and the world?',
        'filename': path.name,
        'category': 'Philosophy',
        'published_date': '2025-10-31'
    }

    # Check if post already exists
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
        print("Usage: python3 publish_html_to_telegraph.py <html_file>")
        print()
        print("Example:")
        print("  python3 publish_html_to_telegraph.py BLOG-CARING-AS-ACTION.html")
        sys.exit(1)

    html_file = sys.argv[1]

    try:
        post_info = publish_html_blog_post(html_file)

        print(f"\n{'='*60}")
        print(f"✓ Successfully published!")
        print(f"{'='*60}")
        print(f"\nTitle: {post_info['title']}")
        print(f"URL: {post_info['url']}")
        print(f"\nShare this URL with your audience!")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
