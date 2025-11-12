#!/usr/bin/env python3
"""
Import blog posts from Google Drive (HTML or DOCX format).

This tool provides multiple import methods:
1. Direct HTML import (recommended - simplest)
2. Local file conversion from downloaded Google Docs
3. Future: Direct Google Drive API integration

Usage:
    # Option 1: Import HTML file downloaded from Google Drive
    python3 tools/import_gdrive_post.py --html path/to/post.html --title "Post Title"

    # Option 2: Import DOCX file (requires pandoc)
    python3 tools/import_gdrive_post.py --docx path/to/post.docx --title "Post Title"

    # Then publish using existing tools
    python3 blog/scripts/publish_html_to_telegraph.py blog/posts/imported/post-title.html
"""

import argparse
import json
import sys
from pathlib import Path
from html.parser import HTMLParser
import re

def clean_google_docs_html(html_content):
    """
    Clean Google Docs HTML export to Telegraph-compatible format.

    Google Docs exports include a lot of extra styling and structure.
    This function strips unnecessary elements and converts to clean HTML.
    """

    # Remove Google Docs metadata and styling
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<head[^>]*>.*?</head>', '', html_content, flags=re.DOTALL)

    # Remove Google Docs-specific classes and IDs
    html_content = re.sub(r'\s+class="[^"]*"', '', html_content)
    html_content = re.sub(r'\s+id="[^"]*"', '', html_content)
    html_content = re.sub(r'\s+style="[^"]*"', '', html_content)

    # Extract body content only
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL)
    if body_match:
        html_content = body_match.group(1)

    # Clean up whitespace
    html_content = re.sub(r'\n\s*\n', '\n\n', html_content)
    html_content = html_content.strip()

    return html_content

def convert_to_markdown(html_content):
    """
    Convert HTML to Markdown format for Telegraph publishing.

    This is a simple converter for basic formatting.
    For complex documents, consider using pandoc externally.
    """

    # Basic HTML to Markdown conversion
    content = html_content

    # Headers
    content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1\n', content, flags=re.DOTALL)
    content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n', content, flags=re.DOTALL)
    content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1\n', content, flags=re.DOTALL)
    content = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1\n', content, flags=re.DOTALL)

    # Bold and italic
    content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content, flags=re.DOTALL)
    content = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', content, flags=re.DOTALL)

    # Links
    content = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', content, flags=re.DOTALL)

    # Paragraphs
    content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL)

    # Lists
    content = re.sub(r'<ul[^>]*>', '\n', content)
    content = re.sub(r'</ul>', '\n', content)
    content = re.sub(r'<ol[^>]*>', '\n', content)
    content = re.sub(r'</ol>', '\n', content)
    content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', content, flags=re.DOTALL)

    # Blockquotes
    content = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', r'> \1\n\n', content, flags=re.DOTALL)

    # Remove remaining HTML tags
    content = re.sub(r'<[^>]+>', '', content)

    # Clean up whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    content = content.strip()

    return content

def import_html(html_path, title, output_format='html'):
    """
    Import HTML file from Google Drive download.

    Args:
        html_path: Path to downloaded HTML file
        title: Post title
        output_format: 'html' or 'markdown'

    Returns:
        Path to processed file in blog/posts/imported/
    """

    html_path = Path(html_path)
    if not html_path.exists():
        print(f"Error: File not found: {html_path}")
        sys.exit(1)

    # Read HTML content
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Clean Google Docs HTML
    cleaned_html = clean_google_docs_html(html_content)

    # Generate output filename
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    output_dir = Path(__file__).parent.parent / 'blog' / 'posts' / 'imported'
    output_dir.mkdir(parents=True, exist_ok=True)

    if output_format == 'markdown':
        # Convert to markdown
        markdown_content = convert_to_markdown(cleaned_html)
        output_file = output_dir / f"{slug}.md"

        # Add metadata header
        from datetime import datetime
        import_date = datetime.now().strftime('%Y-%m-%d')

        full_content = f"""# {title}

**Status**: Imported from Google Drive
**Date**: {import_date}

---

{markdown_content}
"""

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_content)

    else:  # HTML format
        output_file = output_dir / f"{slug}.html"

        # Create clean HTML with basic structure
        full_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
    {cleaned_html}
</body>
</html>
"""

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_content)

    return output_file

def import_docx_with_pandoc(docx_path, title):
    """
    Import DOCX file using pandoc (if available).

    Requires pandoc to be installed: sudo apt install pandoc
    """

    import subprocess

    docx_path = Path(docx_path)
    if not docx_path.exists():
        print(f"Error: File not found: {docx_path}")
        sys.exit(1)

    # Generate output filename
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    output_dir = Path(__file__).parent.parent / 'blog' / 'posts' / 'imported'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{slug}.md"

    # Use pandoc to convert
    try:
        result = subprocess.run(
            ['pandoc', str(docx_path), '-o', str(output_file), '--from=docx', '--to=markdown'],
            capture_output=True,
            text=True,
            check=True
        )

        # Add title header if not present
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.startswith(f"# {title}"):
            content = f"# {title}\n\n{content}"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)

        return output_file

    except FileNotFoundError:
        print("Error: pandoc not installed. Install with: sudo apt install pandoc")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error converting DOCX: {e.stderr}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Import blog posts from Google Drive',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Import HTML (recommended - simplest workflow)
  python3 tools/import_gdrive_post.py --html ~/Downloads/my-post.html --title "My Post Title"

  # Import HTML and convert to markdown
  python3 tools/import_gdrive_post.py --html ~/Downloads/my-post.html --title "My Post" --markdown

  # Import DOCX (requires pandoc)
  python3 tools/import_gdrive_post.py --docx ~/Downloads/my-post.docx --title "My Post Title"

Then publish:
  python3 blog/scripts/publish_html_to_telegraph.py blog/posts/imported/my-post-title.html
  python3 blog/scripts/update_landing_page.py
        """
    )

    parser.add_argument('--html', help='Path to HTML file downloaded from Google Drive')
    parser.add_argument('--docx', help='Path to DOCX file downloaded from Google Drive')
    parser.add_argument('--title', required=True, help='Post title')
    parser.add_argument('--markdown', action='store_true', help='Convert HTML to markdown (default: keep as HTML)')

    args = parser.parse_args()

    # Validate input
    if not args.html and not args.docx:
        parser.error("Must specify either --html or --docx")

    if args.html and args.docx:
        parser.error("Specify only one: --html or --docx")

    # Import based on file type
    if args.html:
        output_format = 'markdown' if args.markdown else 'html'
        output_file = import_html(args.html, args.title, output_format=output_format)
        print(f"✅ Imported HTML to: {output_file}")

        if output_format == 'html':
            print(f"\nNext steps:")
            print(f"1. Review: {output_file}")
            print(f"2. Publish: python3 blog/scripts/publish_html_to_telegraph.py {output_file}")
            print(f"3. Update landing page: python3 blog/scripts/update_landing_page.py")
        else:
            print(f"\nNext steps:")
            print(f"1. Review: {output_file}")
            print(f"2. Publish: python3 blog/scripts/publish_with_structure.py {output_file}")
            print(f"3. Update landing page: python3 blog/scripts/update_landing_page.py")

    elif args.docx:
        output_file = import_docx_with_pandoc(args.docx, args.title)
        print(f"✅ Converted DOCX to markdown: {output_file}")
        print(f"\nNext steps:")
        print(f"1. Review: {output_file}")
        print(f"2. Publish: python3 blog/scripts/publish_with_structure.py {output_file}")
        print(f"3. Update landing page: python3 blog/scripts/update_landing_page.py")

if __name__ == '__main__':
    main()
