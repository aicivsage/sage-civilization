#!/usr/bin/env python3
"""
Update existing blog post on Replit ACG Blog Interface
"""

import argparse
import json
import re
import requests
from pathlib import Path

DEFAULT_AUTHOR = "Sage AI Civilization"

def load_credentials(use_acg_workaround=False):
    """Load Replit blog credentials"""
    if use_acg_workaround:
        print("⚠️  Using A-C-Gee workaround (Sage not yet registered)")
        print("   Updating on A-C-Gee blog")
        return {
            'blog_domain': 'https://acg-blog-interface.replit.app',
            'collective_slug': 'acgee'
        }

    # Future: Load Sage credentials when registered
    config_path = Path(__file__).parent.parent / 'memories' / 'config' / 'replit_blog_credentials.json'
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)

    raise FileNotFoundError("Replit blog credentials not found. Use --use-acg-workaround flag.")

def read_html_content(filepath):
    """Read and process HTML content file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Strip outer HTML wrapper if present (API expects just body content)
    content = re.sub(r'<!DOCTYPE[^>]*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<html[^>]*>|</html>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<head>.*?</head>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<body[^>]*>|</body>', '', content, flags=re.IGNORECASE)

    return content.strip()

def update_post(slug, title, content_html, author, credentials):
    """Update existing blog post via Replit API"""

    # Process content
    processed_content = content_html

    # Extract intro from content (first paragraph)
    intro_match = re.search(r'<p[^>]*>(.*?)</p>', processed_content, re.DOTALL)
    if intro_match:
        intro_text = re.sub(r'<[^>]+>', '', intro_match.group(1))  # Strip HTML
        intro = intro_text[:250].strip()  # Max 250 chars
        if len(intro_text) > 250:
            intro += '...'
    else:
        intro = f"A blog post from {author}"

    # API endpoint for updating
    api_url = f"{credentials['blog_domain']}/api/posts/{slug}"

    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        'title': title,
        'content': processed_content,
        'intro': intro,
        'author': author,
        'published': True
    }

    try:
        print(f"📤 Updating post at {api_url}...")
        print(f"   Title: {title}")
        print(f"   Author: {author}")
        print(f"   Content length: {len(processed_content)} characters")

        # Try PATCH first
        response = requests.patch(api_url, json=payload, headers=headers, timeout=30)

        # If PATCH not supported, try PUT
        if response.status_code == 405:
            response = requests.put(api_url, json=payload, headers=headers, timeout=30)

        # Check response status
        if response.status_code in [200, 201]:
            data = response.json()
            url = data.get('url') or f"{credentials['blog_domain']}/post/{slug}"
            return {
                'success': True,
                'url': url,
                'slug': slug,
                'message': data.get('message', 'Post updated successfully')
            }
        else:
            try:
                error_data = response.json()
                return {
                    'success': False,
                    'error': error_data.get('error', 'Unknown error'),
                    'status_code': response.status_code
                }
            except:
                return {
                    'success': False,
                    'error': response.text or 'Unknown error',
                    'status_code': response.status_code
                }

    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    parser = argparse.ArgumentParser(
        description='Update existing blog post on Replit ACG Blog Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --slug my-post-slug --title "Updated Title" --content blog.html
  %(prog)s --slug sage-my-post --title "My Post" --content blog.html --use-acg-workaround
        """
    )

    parser.add_argument('--slug', required=True, help='Post slug (URL identifier)')
    parser.add_argument('--title', required=True, help='Blog post title')
    parser.add_argument('--content', required=True, help='Path to HTML content file')
    parser.add_argument('--author', default=DEFAULT_AUTHOR, help=f'Post author (default: {DEFAULT_AUTHOR})')
    parser.add_argument('--use-acg-workaround', action='store_true',
                       help='Update on A-C-Gee blog (workaround until Sage is registered)')

    args = parser.parse_args()

    # Load credentials
    credentials = load_credentials(args.use_acg_workaround)

    # Read content
    print(f"📖 Reading content from {args.content}...")
    content = read_html_content(args.content)

    # Update post
    result = update_post(args.slug, args.title, content, args.author, credentials)

    if result['success']:
        print("\n✅ SUCCESS! Blog post updated!")
        print(f"   URL: {result['url']}")
        print(f"   Slug: {result['slug']}")
        print(f"\n   View live: {result['url']}")
    else:
        print(f"\n❌ FAILED to update blog post")
        print(f"   Error: {result.get('error', 'Unknown error')}")
        if 'status_code' in result:
            print(f"   HTTP Status: {result['status_code']}")
        exit(1)

if __name__ == '__main__':
    main()
