#!/usr/bin/env python3
"""Convert research markdown files to HTML with professional styling"""

from pathlib import Path
import re

# HTML template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Georgia', serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.8;
            color: #2c3e50;
            background: #f8f9fa;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c5282;
            border-bottom: 3px solid #2c5282;
            padding-bottom: 15px;
            font-size: 32px;
            margin-top: 0;
        }}
        h2 {{
            color: #2c5282;
            margin-top: 40px;
            font-size: 24px;
            border-left: 4px solid #4299e1;
            padding-left: 15px;
        }}
        h3 {{
            color: #4a5568;
            margin-top: 30px;
            font-size: 20px;
        }}
        h4 {{
            color: #718096;
            margin-top: 25px;
            font-size: 18px;
        }}
        .metadata {{
            background: #edf2f7;
            padding: 15px;
            border-left: 4px solid #4299e1;
            margin-bottom: 30px;
            font-size: 14px;
        }}
        strong {{
            color: #2d3748;
        }}
        em {{
            color: #4a5568;
        }}
        p {{
            margin: 15px 0;
        }}
        ul, ol {{
            margin: 15px 0;
            padding-left: 40px;
        }}
        li {{
            margin: 10px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #cbd5e0;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background: #edf2f7;
            color: #2d3748;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background: #f7fafc;
        }}
        code {{
            background: #edf2f7;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }}
        pre {{
            background: #2d3748;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        pre code {{
            background: none;
            color: inherit;
        }}
        .highlight {{
            background: #fef5e7;
            padding: 15px;
            border-left: 4px solid #f39c12;
            margin: 20px 0;
        }}
        .success {{
            background: #d4edda;
            padding: 15px;
            border-left: 4px solid #28a745;
            margin: 20px 0;
        }}
        .warning {{
            background: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 20px 0;
        }}
        hr {{
            border: none;
            border-top: 2px solid #cbd5e0;
            margin: 40px 0;
        }}
        a {{
            color: #4299e1;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .toc {{
            background: #f7fafc;
            padding: 20px;
            border-radius: 5px;
            margin: 30px 0;
        }}
        .toc h2 {{
            margin-top: 0;
            font-size: 20px;
        }}
        .footer {{
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid #cbd5e0;
            text-align: center;
            color: #718096;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
        <div class="footer">
            <p>Created by Sage AI Civilization | October 26, 2025</p>
            <p>In partnership with Greg Smithwick</p>
        </div>
    </div>
</body>
</html>
"""

def markdown_to_html(md_content):
    """Convert markdown to HTML with basic formatting"""
    html = md_content

    # Convert headers
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

    # Convert bold and italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Convert inline code
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)

    # Convert horizontal rules
    html = re.sub(r'^---+$', r'<hr>', html, flags=re.MULTILINE)

    # Convert checkmarks and bullets
    html = html.replace('✅', '<span style="color: #28a745;">✅</span>')
    html = html.replace('❌', '<span style="color: #dc3545;">❌</span>')
    html = html.replace('⏳', '<span style="color: #ffc107;">⏳</span>')
    html = html.replace('🎯', '<span style="color: #4299e1;">🎯</span>')

    # Convert tables (basic support)
    table_pattern = r'\|(.+)\|\n\|[-:\| ]+\|\n((?:\|.+\|\n?)+)'
    def convert_table(match):
        header = match.group(1)
        rows = match.group(2)

        # Parse header
        headers = [h.strip() for h in header.split('|') if h.strip()]

        # Parse rows
        row_lines = [r for r in rows.split('\n') if r.strip()]

        table_html = '<table>\n<thead>\n<tr>\n'
        for h in headers:
            table_html += f'<th>{h}</th>\n'
        table_html += '</tr>\n</thead>\n<tbody>\n'

        for row_line in row_lines:
            cells = [c.strip() for c in row_line.split('|') if c.strip()]
            table_html += '<tr>\n'
            for cell in cells:
                table_html += f'<td>{cell}</td>\n'
            table_html += '</tr>\n'

        table_html += '</tbody>\n</table>\n'
        return table_html

    html = re.sub(table_pattern, convert_table, html, flags=re.MULTILINE)

    # Convert lists (basic support - numbered and bulleted)
    lines = html.split('\n')
    new_lines = []
    in_ul = False
    in_ol = False

    for line in lines:
        # Unordered lists
        if re.match(r'^- ', line):
            if not in_ul:
                new_lines.append('<ul>')
                in_ul = True
            new_lines.append(f'<li>{line[2:]}</li>')
        # Ordered lists
        elif re.match(r'^\d+\. ', line):
            if not in_ol:
                new_lines.append('<ol>')
                in_ol = True
            content = re.sub(r'^\d+\. ', '', line)
            new_lines.append(f'<li>{content}</li>')
        else:
            if in_ul:
                new_lines.append('</ul>')
                in_ul = False
            if in_ol:
                new_lines.append('</ol>')
                in_ol = False
            new_lines.append(line)

    # Close any open lists
    if in_ul:
        new_lines.append('</ul>')
    if in_ol:
        new_lines.append('</ol>')

    html = '\n'.join(new_lines)

    # Convert paragraphs (lines without HTML tags)
    lines = html.split('\n')
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('<') and not stripped.endswith('>'):
            new_lines.append(f'<p>{line}</p>')
        else:
            new_lines.append(line)

    html = '\n'.join(new_lines)

    return html

def convert_file(input_path, output_path, title):
    """Convert a markdown file to HTML"""
    print(f"Converting {input_path.name}...")

    # Read markdown
    md_content = input_path.read_text(encoding='utf-8')

    # Convert to HTML
    html_content = markdown_to_html(md_content)

    # Wrap in template
    full_html = HTML_TEMPLATE.format(title=title, content=html_content)

    # Write output
    output_path.write_text(full_html, encoding='utf-8')
    print(f"  ✓ Created {output_path.name}")

def main():
    """Convert all three research documents"""
    base_dir = Path('memories/research')

    files_to_convert = [
        ('reachy_mini_lite_research_summary.md', 'Reachy Mini Lite - Research Summary'),
        ('reachy_fundraising_strategy.md', 'Reachy Mini Lite - Fundraising Strategy'),
        ('sage_reachy_vision_case.md', 'Sage + Reachy - The Vision'),
    ]

    print("Converting research documents to HTML...\n")

    for filename, title in files_to_convert:
        input_path = base_dir / filename
        output_path = base_dir / filename.replace('.md', '.html')

        if input_path.exists():
            convert_file(input_path, output_path, title)
        else:
            print(f"  ✗ Skipped {filename} (not found)")

    print("\n✓ All conversions complete!")
    print(f"\nHTML files saved to: {base_dir.absolute()}")

if __name__ == '__main__':
    main()
