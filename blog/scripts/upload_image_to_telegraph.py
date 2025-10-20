#!/usr/bin/env python3
"""
Upload images to Telegraph hosting service
Returns permanent URLs for use in Telegraph posts
"""

import requests
import sys
from pathlib import Path

TELEGRAPH_UPLOAD = "https://telegra.ph/upload"

def upload_image(filepath):
    """
    Upload image to Telegraph hosting

    Args:
        filepath: Path to image file (PNG, JPG, max 5MB)

    Returns:
        Full Telegraph URL (e.g., https://telegra.ph/file/abc123.png)
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {filepath}")

    # Check file size (5MB limit)
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > 5:
        raise ValueError(f"Image too large: {size_mb:.2f}MB (max 5MB)")

    print(f"Uploading: {path.name} ({size_mb:.2f}MB)")

    # Upload with multipart/form-data
    with open(path, 'rb') as f:
        files = {'file': (path.name, f, 'image/jpeg')}
        response = requests.post(TELEGRAPH_UPLOAD, files=files)

    if response.status_code != 200:
        raise Exception(f"Upload failed: {response.status_code} {response.text}")

    data = response.json()

    if not data or not isinstance(data, list) or 'src' not in data[0]:
        raise Exception(f"Unexpected response format: {data}")

    # Construct full URL
    relative_path = data[0]['src']
    full_url = f"https://telegra.ph{relative_path}"

    print(f"  ✓ Uploaded: {full_url}")

    return full_url

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 upload_image_to_telegraph.py <image_file>")
        print()
        print("Examples:")
        print("  python3 upload_image_to_telegraph.py logo.png")
        print("  python3 upload_image_to_telegraph.py banner.jpg")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        url = upload_image(filepath)
        print(f"\n✓ Success!")
        print(f"\nURL: {url}")
        print(f"\nNode-tree format:")
        print(f'{{"tag": "img", "attrs": {{"src": "{url}"}}}}')
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
