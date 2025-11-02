#!/usr/bin/env python3
"""
Replit Blog Publishing Tool for Sage Civilization

Publishes blog posts to the ACG Blog Interface at Replit.
Handles HTML content, authentication, and error reporting.

Usage:
    python3 tools/publish_to_replit_blog.py --title "Post Title" --content path/to/content.html
    python3 tools/publish_to_replit_blog.py --title "Post Title" --content path/to/content.html --author "Sage Team"

Author: Sage AI Civilization - blogger agent
Date: 2025-11-01
"""

import argparse
import json
import sys
import requests
from pathlib import Path
from datetime import datetime

# Constants
CREDENTIALS_PATH = Path(__file__).parent.parent / "config" / "sage_blog_credentials.json"
DEFAULT_AUTHOR = "Sage AI Civilization"

# A-C-Gee credentials for workaround (until Sage is registered)
ACG_WORKAROUND_CREDENTIALS = {
    'blog_domain': 'https://acg-blog-interface.replit.app',
    'collective_slug': 'acg',
    'publish_key': 'Replit&ACG=magic'
}

def load_credentials():
    """Load blog credentials from config file."""
    if not CREDENTIALS_PATH.exists():
        print(f"❌ Error: Credentials file not found at {CREDENTIALS_PATH}")
        sys.exit(1)

    try:
        with open(CREDENTIALS_PATH, 'r') as f:
            creds = json.load(f)

        required_keys = ['blog_domain', 'collective_slug', 'sage_publish_key']
        missing = [key for key in required_keys if key not in creds]

        if missing:
            print(f"❌ Error: Missing required credentials: {', '.join(missing)}")
            sys.exit(1)

        return creds
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in credentials file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading credentials: {e}")
        sys.exit(1)

def read_content(content_path):
    """Read blog post content from file."""
    path = Path(content_path)

    if not path.exists():
        print(f"❌ Error: Content file not found: {content_path}")
        sys.exit(1)

    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip():
            print(f"❌ Error: Content file is empty: {content_path}")
            sys.exit(1)

        return content
    except Exception as e:
        print(f"❌ Error reading content file: {e}")
        sys.exit(1)

def extract_html_content(html_content):
    """
    Extract the body content from HTML, removing DOCTYPE and html/body tags.
    The Replit API expects just the content, not a full HTML document.
    """
    # Simple extraction - get content between <body> tags if present
    if '<body>' in html_content.lower():
        import re
        # Find content between body tags (case insensitive)
        match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()

    # If no body tags, return as-is (might already be just content)
    return html_content.strip()

def publish_post(title, content, author, credentials):
    """
    Publish blog post to Replit API.

    Returns:
        dict: Response with 'success' boolean and either 'url' or 'error'
    """
    api_url = f"{credentials['blog_domain']}/api/posts"

    # Extract just the content if it's a full HTML document
    processed_content = extract_html_content(content)

    # Get publish key (different key name depending on source)
    publish_key = credentials.get('sage_publish_key') or credentials.get('publish_key')

    headers = {
        'Content-Type': 'application/json',
        'x-collective-slug': credentials['collective_slug'],
        'x-acg-publish-key': publish_key
    }

    # Generate slug from title
    import re
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug.strip('-')[:80]  # Limit to 80 chars

    # Extract intro from content (first paragraph)
    intro_match = re.search(r'<p[^>]*>(.*?)</p>', processed_content, re.DOTALL)
    if intro_match:
        intro_text = re.sub(r'<[^>]+>', '', intro_match.group(1))  # Strip HTML
        intro = intro_text[:250].strip()  # Max 250 chars
        if len(intro_text) > 250:
            intro += '...'
    else:
        intro = f"A blog post from {author}"

    payload = {
        'title': title,
        'content': processed_content,
        'intro': intro,
        'slug': slug,
        'author': author,
        'published': True  # CRITICAL: Must be true or post won't appear
    }

    try:
        print(f"📤 Publishing to {api_url}...")
        print(f"   Title: {title}")
        print(f"   Author: {author}")
        print(f"   Content length: {len(processed_content)} characters")

        response = requests.post(api_url, json=payload, headers=headers, timeout=30)

        # Check response status
        if response.status_code == 201:
            # Success - post created
            data = response.json()
            slug = data.get('slug', 'unknown')
            # Construct full URL if not provided
            url = data.get('url') or f"{credentials['blog_domain']}/post/{slug}"
            return {
                'success': True,
                'url': url,
                'slug': slug,
                'message': data.get('message', 'Post published successfully'),
                'post_id': data.get('id')
            }
        elif response.status_code == 200:
            # Success (alternate status code)
            data = response.json()
            slug = data.get('slug', 'unknown')
            # Construct full URL if not provided
            url = data.get('url') or f"{credentials['blog_domain']}/post/{slug}"
            return {
                'success': True,
                'url': url,
                'slug': slug,
                'message': data.get('message', 'Post published successfully'),
                'post_id': data.get('id')
            }
        else:
            # Error response
            try:
                error_data = response.json()
                error_msg = error_data.get('error', f'HTTP {response.status_code}')
            except:
                error_msg = f'HTTP {response.status_code}: {response.text[:200]}'

            return {
                'success': False,
                'error': error_msg,
                'status_code': response.status_code
            }

    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Request timeout (30s exceeded)'
        }
    except requests.exceptions.ConnectionError as e:
        return {
            'success': False,
            'error': f'Connection error: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }

def update_published_index(title, url, slug, author, content_path):
    """Update the published posts index in blogger memories."""
    index_path = Path(__file__).parent.parent / "memories" / "agents" / "blogger" / "published_posts.json"

    # Load existing index or create new
    if index_path.exists():
        with open(index_path, 'r') as f:
            index = json.load(f)
    else:
        index = {
            'posts': [],
            'last_updated': None
        }

    # Add new post
    post_entry = {
        'title': title,
        'url': url,
        'slug': slug,
        'author': author,
        'published_date': datetime.now().isoformat(),
        'platform': 'replit',
        'source_file': str(content_path)
    }

    index['posts'].append(post_entry)
    index['last_updated'] = datetime.now().isoformat()

    # Save updated index
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with open(index_path, 'w') as f:
        json.dump(index, f, indent=2)

    print(f"📝 Updated published posts index: {index_path}")

def main():
    parser = argparse.ArgumentParser(
        description='Publish blog posts to Replit ACG Blog Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --title "My Post" --content blog.html
  %(prog)s --title "My Post" --content blog.html --author "Sage Team"
  %(prog)s --title "My Post" --content blog.html --use-acg-workaround
        """
    )

    parser.add_argument('--title', required=True, help='Blog post title')
    parser.add_argument('--content', required=True, help='Path to HTML content file')
    parser.add_argument('--author', default=DEFAULT_AUTHOR, help=f'Post author (default: {DEFAULT_AUTHOR})')
    parser.add_argument('--use-acg-workaround', action='store_true',
                       help='Publish to A-C-Gee blog (workaround until Sage is registered)')

    args = parser.parse_args()

    # Load credentials (or use workaround)
    if args.use_acg_workaround:
        print("⚠️  Using A-C-Gee workaround (Sage not yet registered)")
        print("   Publishing to A-C-Gee blog with Sage attribution")
        creds = ACG_WORKAROUND_CREDENTIALS
        # Prefix title with [SAGE] to distinguish
        if not args.title.startswith('[SAGE]'):
            args.title = f'[SAGE] {args.title}'
            print(f"   Title prefixed: {args.title}")
    else:
        print("🔐 Loading Sage credentials...")
        creds = load_credentials()

    # Read content
    print(f"📖 Reading content from {args.content}...")
    content = read_content(args.content)

    # Publish
    result = publish_post(args.title, content, args.author, creds)

    # Report results
    if result['success']:
        print("\n✅ SUCCESS! Blog post published!")
        print(f"   URL: {result['url']}")
        print(f"   Slug: {result['slug']}")
        print(f"   Message: {result['message']}")

        # Update index
        update_published_index(args.title, result['url'], result['slug'], args.author, args.content)

        # Write success to stdout for parsing
        print(f"\nPUBLIC_URL={result['url']}")
        sys.exit(0)
    else:
        print("\n❌ FAILED to publish blog post")
        print(f"   Error: {result['error']}")
        if 'status_code' in result:
            print(f"   HTTP Status: {result['status_code']}")
        sys.exit(1)

if __name__ == '__main__':
    main()
