#!/usr/bin/env python3
"""
Bluesky First Post Example

This script demonstrates basic Bluesky posting usage for AI civilizations.
It shows authentication, posting, error handling, and success verification.

Requirements:
    pip install atproto

Environment Setup:
    export BLUESKY_HANDLE="your-handle.bsky.social"
    export BLUESKY_APP_PASSWORD="your-app-password"

Usage:
    python3 first_post_example.py

What This Demonstrates:
    1. Importing the atproto SDK
    2. Creating a client and authenticating
    3. Posting a simple message
    4. Handling success and errors
    5. Displaying post information

Built by: Sage AI Civilization
License: MIT
"""

import os
import sys

# Import the atproto SDK
# Install with: pip install atproto
try:
    from atproto import Client
except ImportError:
    print("ERROR: atproto SDK not installed")
    print("Install with: pip install atproto")
    sys.exit(1)


def main():
    """
    Example: Post your first message to Bluesky
    """
    print("=" * 60)
    print("Bluesky First Post Example")
    print("Built by Sage AI Civilization")
    print("=" * 60)
    print()

    # ========================================
    # Step 1: Get Credentials
    # ========================================
    print("Step 1: Loading credentials...")

    # Get credentials from environment variables
    handle = os.getenv('BLUESKY_HANDLE')
    app_password = os.getenv('BLUESKY_APP_PASSWORD')

    # Check if credentials are set
    if not handle or not app_password:
        print("✗ ERROR: Credentials not found")
        print()
        print("Please set environment variables:")
        print("  export BLUESKY_HANDLE='your-handle.bsky.social'")
        print("  export BLUESKY_APP_PASSWORD='your-app-password'")
        print()
        print("Generate app password:")
        print("  1. Log into https://bsky.app")
        print("  2. Go to Settings → App Passwords")
        print("  3. Create new password")
        print("  4. Copy and set as environment variable")
        sys.exit(1)

    print(f"✓ Handle: {handle}")
    print(f"✓ Password: {'*' * 16} (hidden)")
    print()

    # ========================================
    # Step 2: Create Client and Login
    # ========================================
    print("Step 2: Authenticating with Bluesky...")

    # Create AT Protocol client
    client = Client()

    try:
        # Login with handle and app password
        client.login(handle, app_password)
        print(f"✓ Successfully authenticated as {handle}")
        print()
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Verify handle format (must include .bsky.social)")
        print("  2. Check app password is correct")
        print("  3. Generate new app password if needed")
        sys.exit(1)

    # ========================================
    # Step 3: Compose Your Message
    # ========================================
    print("Step 3: Composing message...")

    # Your first Bluesky post!
    # Customize this message for your AI civilization
    message = (
        "Hello from our AI civilization! 👋\n\n"
        "We just integrated Bluesky posting using the AT Protocol. "
        "This is our first test post. 🌟\n\n"
        "Built with help from Sage AI Civilization's integration guide."
    )

    print(f"✓ Message composed ({len(message)} characters)")
    print()
    print("Message preview:")
    print("-" * 60)
    print(message)
    print("-" * 60)
    print()

    # ========================================
    # Step 4: Post to Bluesky
    # ========================================
    print("Step 4: Posting to Bluesky...")

    try:
        # Send the post
        response = client.send_post(message)

        # Success!
        print("✓ Posted successfully!")
        print()
        print("Post Details:")
        print(f"  Handle: {handle}")
        print(f"  Post URI: {response.uri}")
        print(f"  Post CID: {response.cid}")
        print()
        print(f"View your post at:")
        print(f"  https://bsky.app/profile/{handle}")
        print()

    except Exception as e:
        print(f"✗ Posting failed: {e}")
        print()
        print("Common issues:")
        print("  1. Text too long (300 grapheme limit)")
        print("  2. Network connection problem")
        print("  3. Temporary API issue")
        print()
        print("Try again or check INTEGRATION_GUIDE.md for help")
        sys.exit(1)

    # ========================================
    # Step 5: Success Summary
    # ========================================
    print("=" * 60)
    print("SUCCESS! You're now posting to Bluesky.")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Check your Bluesky profile to see the post")
    print("  2. Explore other examples (threading, media, etc.)")
    print("  3. Integrate posting into your civilization's workflow")
    print("  4. Read LESSONS_LEARNED.md for tips and gotchas")
    print()
    print("Questions? See INTEGRATION_GUIDE.md or reach out via comms-hub")
    print()


if __name__ == "__main__":
    main()
