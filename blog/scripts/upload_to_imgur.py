#!/usr/bin/env python3
"""
Upload images to Imgur (anonymous, no account needed)
"""

import requests
import base64
import sys
from pathlib import Path

# Imgur anonymous upload endpoint
IMGUR_CLIENT_ID = "546c25a59c58ad7"  # Public client ID for anonymous uploads
IMGUR_UPLOAD_URL = "https://api.imgur.com/3/image"

def upload_to_imgur(filepath):
    """
    Upload image to Imgur anonymously

    Returns:
        Direct image URL (e.g., https://i.imgur.com/abc123.jpg)
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {filepath}")

    print(f"Uploading {path.name} to Imgur...")

    # Read and encode image
    with open(path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    # Upload to Imgur
    headers = {
        'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'
    }

    data = {
        'image': image_data,
        'type': 'base64'
    }

    response = requests.post(IMGUR_UPLOAD_URL, headers=headers, data=data)

    if response.status_code != 200:
        raise Exception(f"Upload failed: {response.status_code} {response.text}")

    result = response.json()

    if not result.get('success'):
        raise Exception(f"Upload failed: {result}")

    # Get direct link
    link = result['data']['link']

    print(f"  ✓ Uploaded: {link}")

    return link

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 upload_to_imgur.py <image_file>")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        url = upload_to_imgur(filepath)
        print(f"\nDirect URL: {url}")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
