#!/usr/bin/env python3
"""
Bluesky posting tool for Sage AI Civilization
Uses atproto Python SDK
"""

import os
import sys
from atproto import Client

def post_to_bluesky(text, handle=None, app_password=None):
    """
    Post a message to Bluesky

    Args:
        text: The text to post (max 300 graphemes)
        handle: Bluesky handle (optional, uses env var if not provided)
        app_password: App password (optional, uses env var if not provided)

    Returns:
        dict: Response from Bluesky API
    """
    # Get credentials from env or parameters
    handle = handle or os.getenv('BLUESKY_HANDLE')
    app_password = app_password or os.getenv('BLUESKY_APP_PASSWORD')

    if not handle or not app_password:
        raise ValueError("Bluesky handle and app password required (env vars or params)")

    # Create client and login
    client = Client()
    print(f"Logging in to Bluesky as {handle}...")
    client.login(handle, app_password)

    # Send post
    print(f"Posting to Bluesky...")
    response = client.send_post(text)

    print(f"✓ Posted to Bluesky successfully!")
    print(f"  Handle: {handle}")
    print(f"  Post URI: {response.uri}")
    print(f"  Post CID: {response.cid}")

    return response

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 bluesky_post.py 'Your message here'")
        print("\nOr set environment variables:")
        print("  export BLUESKY_HANDLE='your-handle.bsky.social'")
        print("  export BLUESKY_APP_PASSWORD='your-app-password'")
        sys.exit(1)

    message = sys.argv[1]

    try:
        post_to_bluesky(message)
    except Exception as e:
        print(f"✗ Error posting to Bluesky: {e}")
        sys.exit(1)
