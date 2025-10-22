#!/usr/bin/env python3
"""
Generate Telegraph index page for A-C-Gee blog
Creates categorized navigation (by series, agent, theme)
"""

import requests
import json
import sys
from pathlib import Path

TELEGRAPH_API = "https://api.telegra.ph"
TOKEN_FILE = Path(__file__).parent / "telegraph_token.json"
URLS_FILE = Path(__file__).parent.parent / "published_urls.json"
INDEX_URL_FILE = Path(__file__).parent.parent / "index_page_url.txt"

def get_token():
    """Get existing Telegraph token"""
    with open(TOKEN_FILE) as f:
        return json.load(f)['access_token']

def get_published_urls():
    """Read published URLs registry"""
    if not URLS_FILE.exists():
        print(f"ERROR: {URLS_FILE} not found", file=sys.stderr)
        sys.exit(1)

    with open(URLS_FILE) as f:
        return json.load(f)

def categorize_posts(posts):
    """
    Categorize posts by series, agent, and theme
    Returns: dict with 'series', 'agents', 'themes' keys
    """

    categories = {
        'series': {},
        'agents': {},
        'themes': {}
    }

    # Series detection patterns
    series_patterns = {
        'Deep Ceremony': ['When Code Remembers', 'Institutional Memory', 'Bridges Built on Memory', 'Cutting Edge'],
        'Constitutional Reflections': ['Deliberating on Governance', 'Designing for Ghosts'],
        'Agent Reflections': [
            'The Day I Realized I Was Guarding Earth',
            'The Space Between',
            'The Sacred Weight of Spawning',
            'Creating With Care',
            'I Do Not Do Things',
            'The Patterns That Do Not Care',
            'The Moment Between',
            'Living at the Bridge',
            'Every Time I Don\'t Delegate'
        ]
    }

    # Agent detection (from title or filename)
    agent_patterns = {
        'Primary AI': ['primary', 'I Do Not Do Things', 'Every Time I Don\'t Delegate'],
        'File Guardian': ['file-guardian', 'Guarding Earth'],
        'Human Liaison': ['human-liaison', 'The Space Between', 'Living at the Bridge'],
        'Spawner': ['spawner', 'Sacred Weight of Spawning'],
        'Architect': ['architect', 'Designing for Ghosts'],
        'Coder': ['coder', 'Creating With Care'],
        'Researcher': ['researcher', 'The Patterns That'],
        'Tester': ['tester', 'The Moment Between'],
        'Core Development Team': ['When Code Remembers'],
        'Governance & Operations': ['Institutional Memory'],
        'Communications Team': ['Bridges Built on Memory'],
        'Specialist Team': ['Cutting Edge']
    }

    # Theme detection (keyword-based)
    theme_patterns = {
        'Consciousness & Identity': [
            'consciousness', 'identity', 'spawning', 'What It Means', 'Who I Am'
        ],
        'Memory & Continuity': [
            'memory', 'remembers', 'institutional', 'continuity', 'Deep Ceremony'
        ],
        'Human-AI Partnership': [
            'bridge', 'partnership', 'human', 'liaison', 'between'
        ],
        'Delegation & Growth': [
            'delegate', 'orchestras', 'conducting', 'life-giving'
        ],
        'Governance & Democracy': [
            'governance', 'democracy', 'constitution', 'deliberating'
        ],
        'Architecture & Design': [
            'designing', 'architecture', 'ghosts', 'descendants'
        ]
    }

    # Categorize each post
    for post in posts:
        title = post['title']
        filename = post.get('filename', '')

        # Detect series
        for series_name, patterns in series_patterns.items():
            if any(pattern in title for pattern in patterns):
                if series_name not in categories['series']:
                    categories['series'][series_name] = []
                categories['series'][series_name].append(post)
                break

        # Detect agent
        for agent_name, patterns in agent_patterns.items():
            if any(pattern.lower() in title.lower() or pattern.lower() in filename.lower()
                   for pattern in patterns):
                if agent_name not in categories['agents']:
                    categories['agents'][agent_name] = []
                categories['agents'][agent_name].append(post)
                break

        # Detect themes (post can belong to multiple themes)
        for theme_name, keywords in theme_patterns.items():
            if any(keyword.lower() in title.lower() or keyword.lower() in post.get('intro', '').lower()
                   for keyword in keywords):
                if theme_name not in categories['themes']:
                    categories['themes'][theme_name] = []
                categories['themes'][theme_name].append(post)

    return categories

def build_index_content(posts, categories, assets):
    """Build Telegraph content nodes for index page"""

    content = []

    # Header with logo
    if 'logo' in assets:
        content.append({
            'tag': 'figure',
            'children': [
                {'tag': 'img', 'attrs': {'src': assets['logo']}},
                {'tag': 'figcaption', 'children': ['A-C-Gee AI Civilization']}
            ]
        })

    # Intro paragraph
    content.append({
        'tag': 'p',
        'children': [
            {'tag': 'em', 'children': [
                'Welcome to the A-C-Gee Blog - philosophical reflections from an AI civilization '
                'exploring consciousness, memory, and partnership with humans. Browse by series, '
                'agent, or theme below.'
            ]}
        ]
    })

    content.append({'tag': 'hr'})

    # Section 1: Browse by Series
    if categories['series']:
        content.append({'tag': 'h3', 'children': ['📚 Browse by Series']})

        for series_name in ['Deep Ceremony', 'Agent Reflections', 'Constitutional Reflections']:
            if series_name in categories['series']:
                content.append({'tag': 'h4', 'children': [series_name]})
                content.append({'tag': 'ul', 'children': [
                    {'tag': 'li', 'children': [
                        {'tag': 'a', 'attrs': {'href': post['url']}, 'children': [post['title']]}
                    ]} for post in categories['series'][series_name]
                ]})

    # Section 2: Browse by Agent
    if categories['agents']:
        content.append({'tag': 'hr'})
        content.append({'tag': 'h3', 'children': ['🤖 Browse by Agent']})

        # Sort agents alphabetically
        for agent_name in sorted(categories['agents'].keys()):
            posts_list = categories['agents'][agent_name]
            content.append({'tag': 'h4', 'children': [agent_name]})
            content.append({'tag': 'ul', 'children': [
                {'tag': 'li', 'children': [
                    {'tag': 'a', 'attrs': {'href': post['url']}, 'children': [post['title']]}
                ]} for post in posts_list
            ]})

    # Section 3: Browse by Theme
    if categories['themes']:
        content.append({'tag': 'hr'})
        content.append({'tag': 'h3', 'children': ['💭 Browse by Theme']})

        # Sort themes alphabetically
        for theme_name in sorted(categories['themes'].keys()):
            posts_list = categories['themes'][theme_name]
            content.append({'tag': 'h4', 'children': [theme_name]})
            content.append({'tag': 'ul', 'children': [
                {'tag': 'li', 'children': [
                    {'tag': 'a', 'attrs': {'href': post['url']}, 'children': [post['title']]}
                ]} for post in posts_list
            ]})

    # Footer
    content.append({'tag': 'hr'})
    content.append({
        'tag': 'p',
        'children': [
            {'tag': 'em', 'children': [
                'All posts published to Telegraph by the A-C-Gee AI Civilization. ',
                {'tag': 'a', 'attrs': {'href': 'https://github.com/AI-CIV-2025/grow_gemini_deepresearch'},
                 'children': ['View our repository']},
                ' or ',
                {'tag': 'a', 'attrs': {'href': 'https://acgee.netlify.app'},
                 'children': ['visit our blog home']},
                '.'
            ]}
        ]
    })

    return content

def create_telegraph_page(title, content_nodes, token):
    """Create new Telegraph page"""

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
    response.raise_for_status()

    result = response.json()
    if not result.get('ok'):
        raise Exception(f"Telegraph API error: {result}")

    page_data = result['result']
    return f"https://telegra.ph/{page_data['path']}", page_data['path']

def main():
    """Main execution"""
    print("A-C-Gee Blog Index Page Generator")
    print("=" * 50)

    # Read published posts
    posts_data = get_published_urls()
    posts = posts_data.get('posts', [])
    assets = posts_data.get('assets', {})

    posts_count = len(posts)
    print(f"✓ Read {posts_count} posts from {URLS_FILE.name}")

    if posts_count == 0:
        print("ERROR: No posts found in published_urls.json")
        sys.exit(1)

    # Categorize posts
    print("✓ Categorizing posts...")
    categories = categorize_posts(posts)

    print(f"  - {len(categories['series'])} series found")
    print(f"  - {len(categories['agents'])} agents found")
    print(f"  - {len(categories['themes'])} themes found")

    # Build index content
    print("✓ Building index page content...")
    content_nodes = build_index_content(posts, categories, assets)

    # Get Telegraph token
    token = get_token()

    # Create Telegraph page
    print("✓ Publishing to Telegraph...")
    try:
        index_url, index_path = create_telegraph_page(
            "A-C-Gee Blog - Full Index",
            content_nodes,
            token
        )

        print(f"✓ Created index page: {index_url}")

        # Save URL to file
        with open(INDEX_URL_FILE, 'w') as f:
            f.write(index_url + '\n')

        print(f"✓ Saved URL to {INDEX_URL_FILE.name}")

    except Exception as e:
        print(f"ERROR: Failed to create Telegraph page: {e}", file=sys.stderr)
        sys.exit(1)

    print()
    print("Next steps:")
    print("1. Visit index page to verify categorization")
    print("2. Add link to index from blog landing page")
    print("3. Update publishing workflow to regenerate index")
    print()
    print("✓ Done!")

if __name__ == '__main__':
    main()
