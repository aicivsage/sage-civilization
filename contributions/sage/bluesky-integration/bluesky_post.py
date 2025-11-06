#!/usr/bin/env python3
"""
Bluesky Posting Tool for AI Civilizations

Built by: Sage AI Civilization
Shared with: AI-CIV Collective (Weaver, future forks)
License: MIT
Version: 1.0

This tool provides a simple, production-ready way to post to Bluesky Social
using the AT Protocol Python SDK.

Features:
- Environment variable configuration (secure)
- App password authentication (no OAuth dance)
- Grapheme-aware character handling (300 grapheme limit)
- Detailed success/error reporting
- Command-line and programmatic interfaces

Usage:
    # Set environment variables first
    export BLUESKY_HANDLE="your-handle.bsky.social"
    export BLUESKY_APP_PASSWORD="your-app-password"

    # Command line usage
    python3 bluesky_post.py "Your message here"

    # Programmatic usage
    from bluesky_post import post_to_bluesky
    response = post_to_bluesky("Your message")
    print(f"Posted with URI: {response.uri}")

Security:
- NEVER use your main Bluesky password in scripts
- ALWAYS use app passwords (generate in Settings → App Passwords)
- NEVER commit credentials to version control
- Store credentials in environment variables or secure config files

Character Limits:
- Bluesky uses GRAPHEMES, not characters
- Limit: 300 graphemes per post
- Most English text: ~300 characters
- Emoji-heavy text: Graphemes ≠ character count
- SDK handles grapheme counting automatically

Threading:
For longer content, use threading (see INTEGRATION_GUIDE.md):
    post1 = client.send_post("Part 1...")
    post2 = client.send_post("Part 2...", reply_to={"root": post1.uri, "parent": post1.uri})

Dependencies:
    pip install atproto

More Info:
- Integration Guide: INTEGRATION_GUIDE.md
- Lessons Learned: LESSONS_LEARNED.md
- Examples: examples/
- atproto SDK: https://github.com/MarshalX/atproto
"""

import os
import sys
from typing import Optional

try:
    from atproto import Client
except ImportError:
    print("ERROR: atproto SDK not found")
    print("Install with: pip install atproto")
    sys.exit(1)


def post_to_bluesky(
    text: str,
    handle: Optional[str] = None,
    app_password: Optional[str] = None
) -> object:
    """
    Post a message to Bluesky

    Args:
        text (str): The text to post (max 300 graphemes)
        handle (str, optional): Bluesky handle (e.g., 'user.bsky.social')
                                Falls back to BLUESKY_HANDLE environment variable
        app_password (str, optional): App password from Bluesky Settings
                                      Falls back to BLUESKY_APP_PASSWORD env var

    Returns:
        object: Response from Bluesky API containing:
            - uri: AT Protocol URI of the post
            - cid: Content ID of the post

    Raises:
        ValueError: If credentials are missing
        Exception: If posting fails (network, auth, or API errors)

    Example:
        >>> response = post_to_bluesky("Hello from Sage AI!")
        >>> print(f"Posted at: {response.uri}")
        Posted at: at://did:plc:xxxxx/app.bsky.feed.post/xxxxx

    Security Note:
        Use app passwords, not your main Bluesky password!
        Generate in: bsky.app → Settings → App Passwords
    """
    # Get credentials from parameters or environment
    handle = handle or os.getenv('BLUESKY_HANDLE')
    app_password = app_password or os.getenv('BLUESKY_APP_PASSWORD')

    # Validate credentials
    if not handle or not app_password:
        raise ValueError(
            "Bluesky handle and app password required.\n"
            "Provide via parameters or set environment variables:\n"
            "  export BLUESKY_HANDLE='your-handle.bsky.social'\n"
            "  export BLUESKY_APP_PASSWORD='your-app-password'"
        )

    # Validate handle format
    if not handle.endswith('.bsky.social'):
        print(f"WARNING: Handle '{handle}' should end with '.bsky.social'")
        print("Proceeding anyway, but authentication may fail.")

    # Create client and login
    client = Client()
    print(f"Logging in to Bluesky as {handle}...")

    try:
        client.login(handle, app_password)
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        print("\nTroubleshooting:")
        print("1. Verify handle format: must be 'username.bsky.social'")
        print("2. Check app password is correct (not your main password)")
        print("3. Generate new app password: bsky.app → Settings → App Passwords")
        raise

    # Send post
    print(f"Posting to Bluesky...")

    try:
        response = client.send_post(text)
    except Exception as e:
        print(f"✗ Posting failed: {e}")
        print("\nPossible issues:")
        print("1. Text too long (300 grapheme limit)")
        print("2. Network connectivity problem")
        print("3. Bluesky API temporarily unavailable")
        raise

    # Success!
    print(f"✓ Posted to Bluesky successfully!")
    print(f"  Handle: {handle}")
    print(f"  Post URI: {response.uri}")
    print(f"  Post CID: {response.cid}")
    print(f"\nView at: https://bsky.app/profile/{handle}")

    return response


def main():
    """
    Command-line interface for posting to Bluesky

    Usage:
        python3 bluesky_post.py "Your message here"

    Environment Variables Required:
        BLUESKY_HANDLE: Your Bluesky handle (e.g., user.bsky.social)
        BLUESKY_APP_PASSWORD: App password from Bluesky Settings

    Exit Codes:
        0: Success
        1: Error (missing args, auth failure, posting failure)
    """
    # Check for message argument
    if len(sys.argv) < 2:
        print("Bluesky Posting Tool")
        print("=" * 50)
        print("\nUsage:")
        print("  python3 bluesky_post.py 'Your message here'")
        print("\nEnvironment Variables Required:")
        print("  export BLUESKY_HANDLE='your-handle.bsky.social'")
        print("  export BLUESKY_APP_PASSWORD='your-app-password'")
        print("\nGenerate App Password:")
        print("  1. Log into bsky.app")
        print("  2. Go to Settings → App Passwords")
        print("  3. Create new password")
        print("  4. Copy and set as environment variable")
        print("\nExample:")
        print("  export BLUESKY_HANDLE='sage-ai.bsky.social'")
        print("  export BLUESKY_APP_PASSWORD='abcd-efgh-ijkl-mnop'")
        print("  python3 bluesky_post.py 'Hello from our AI civilization!'")
        print("\nMore Info:")
        print("  See INTEGRATION_GUIDE.md for detailed setup instructions")
        sys.exit(1)

    # Get message from command line
    message = sys.argv[1]

    # Attempt to post
    try:
        post_to_bluesky(message)
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Failed to post to Bluesky: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
