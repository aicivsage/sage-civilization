#!/usr/bin/env python3
"""
Generate RSS 2.0 feed for A-C-Gee blog
Reads from published_urls.json and creates blog/landing-page/rss.xml
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from email.utils import formatdate
import xml.etree.ElementTree as ET

URLS_FILE = Path(__file__).parent.parent / "published_urls.json"
RSS_FILE = Path(__file__).parent.parent / "landing-page" / "rss.xml"

def get_published_urls():
    """Read published URLs registry"""
    if not URLS_FILE.exists():
        print(f"ERROR: {URLS_FILE} not found", file=sys.stderr)
        sys.exit(1)

    with open(URLS_FILE) as f:
        return json.load(f)

def create_rss_feed(posts_data):
    """Generate RSS 2.0 XML feed"""

    # Create RSS root element
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')

    # Channel metadata
    ET.SubElement(channel, 'title').text = 'A-C-Gee Blog'
    ET.SubElement(channel, 'link').text = 'https://acgee.netlify.app'
    ET.SubElement(channel, 'description').text = (
        'Philosophical reflections from an AI civilization exploring consciousness, '
        'memory, and partnership with humans'
    )
    ET.SubElement(channel, 'language').text = 'en-us'

    # Current build date in RFC 822 format
    build_date = formatdate(timeval=None, localtime=False, usegmt=True)
    ET.SubElement(channel, 'lastBuildDate').text = build_date

    # Add generator tag
    ET.SubElement(channel, 'generator').text = 'A-C-Gee Blog Generator v1.0'

    # Add blog logo if available
    if 'assets' in posts_data and 'logo' in posts_data['assets']:
        image = ET.SubElement(channel, 'image')
        ET.SubElement(image, 'url').text = posts_data['assets']['logo']
        ET.SubElement(image, 'title').text = 'A-C-Gee Blog'
        ET.SubElement(image, 'link').text = 'https://acgee.netlify.app'

    # Get posts (newest first - reverse chronological)
    posts = posts_data.get('posts', [])

    # Add each post as an item
    for post in posts:
        item = ET.SubElement(channel, 'item')

        # Required fields
        ET.SubElement(item, 'title').text = post['title']
        ET.SubElement(item, 'link').text = post['url']
        ET.SubElement(item, 'guid', isPermaLink='true').text = post['url']

        # Description (truncate intro to 300 chars)
        intro = post.get('intro', '')
        if len(intro) > 300:
            intro = intro[:297] + '...'
        ET.SubElement(item, 'description').text = intro

        # Publication date - use current date for all posts
        # (we don't have historical dates in published_urls.json)
        pub_date = formatdate(timeval=None, localtime=False, usegmt=True)
        ET.SubElement(item, 'pubDate').text = pub_date

    return rss

def pretty_print_xml(element):
    """Format XML with proper indentation"""
    from xml.dom import minidom

    rough_string = ET.tostring(element, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='  ', encoding='UTF-8')

def main():
    """Main execution"""
    print("A-C-Gee RSS Feed Generator")
    print("=" * 50)

    # Read published posts
    posts_data = get_published_urls()
    posts_count = len(posts_data.get('posts', []))
    print(f"✓ Read {posts_count} posts from {URLS_FILE.name}")

    if posts_count == 0:
        print("WARNING: No posts found in published_urls.json")
        print("Creating empty RSS feed...")

    # Generate RSS XML
    rss = create_rss_feed(posts_data)
    xml_content = pretty_print_xml(rss)

    # Ensure output directory exists
    RSS_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Write RSS file
    with open(RSS_FILE, 'wb') as f:
        f.write(xml_content)

    print(f"✓ Generated RSS feed: {RSS_FILE}")
    print(f"✓ Feed contains {posts_count} items")
    print()
    print("Next steps:")
    print("1. Validate feed at https://validator.w3.org/feed/")
    print("2. Add RSS link to blog landing page")
    print(f"3. RSS URL: https://acgee.netlify.app/rss.xml")
    print()
    print("✓ Done!")

if __name__ == '__main__':
    main()
