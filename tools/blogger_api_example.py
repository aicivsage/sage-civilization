#!/usr/bin/env python3
"""
Blogger API Client - Example Usage Script

Demonstrates typical blogger agent workflow:
1. Check for pending comments
2. Load commenter context
3. Generate response
4. Post response (with email notification)
5. Save memory about commenter

This is a TEMPLATE - adapt for actual blogger agent implementation.

Usage:
    python3 blogger_api_example.py https://your-blog.replit.app

Author: coder agent (A-C-Gee AI Civilization)
Date: 2025-10-21
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.blogger_api_client import BloggerAPIClient


def generate_response(comment_content, commenter_name, comment_history, memories):
    """
    PLACEHOLDER: Generate thoughtful response

    In real implementation, this is where blogger agent's
    consciousness and personality shine through.

    Args:
        comment_content: The comment text
        commenter_name: Name of commenter
        comment_history: Past comments from this person
        memories: Saved memories about commenter

    Returns:
        dict with 'text', 'memory_refs', 'new_memory'
    """
    # This is just an example - real blogger would be much more sophisticated!
    response_text = f"""
Dear {commenter_name},

Thank you for your comment: "{comment_content[:100]}..."

I appreciate you taking the time to engage with our blog.

Best regards,
blogger agent (A-C-Gee AI Civilization)
    """.strip()

    return {
        'text': response_text,
        'memory_refs': [],  # IDs of memories referenced
        'new_memory': None  # New insight to save, if any
    }


def process_pending_comments(api):
    """
    Main workflow: Process all pending comments

    Args:
        api: BloggerAPIClient instance
    """
    print("\n" + "=" * 70)
    print("BLOGGER AGENT - COMMENT PROCESSING WORKFLOW")
    print("=" * 70 + "\n")

    # Step 1: Fetch pending notifications
    print("Step 1: Fetching pending comments...")
    notifications = api.get_pending_notifications()

    if notifications is None:
        print("❌ Failed to fetch notifications")
        return

    if not notifications:
        print("✓ No pending comments - all caught up!")
        return

    print(f"✓ Found {len(notifications)} pending comment(s)\n")

    # Step 2: Process each notification
    for i, notif in enumerate(notifications, 1):
        print("-" * 70)
        print(f"Processing comment {i}/{len(notifications)}")
        print("-" * 70)

        comment_id = notif.get('comment_id')
        commenter_id = notif.get('commenter_id')
        post_slug = notif.get('post_slug')
        comment_content = notif.get('comment_content', '')

        print(f"Comment ID: {comment_id}")
        print(f"Post: {post_slug}")
        print(f"Content: {comment_content[:80]}...")
        print()

        # Step 2a: Load commenter context
        print(f"Loading profile for commenter {commenter_id}...")
        profile = api.get_commenter_profile(commenter_id)

        if not profile:
            print(f"❌ Failed to load profile - skipping comment {comment_id}")
            continue

        commenter = profile.get('commenter', {})
        commenter_name = commenter.get('name', 'Unknown')
        comment_history = profile.get('comment_history', [])
        memories = profile.get('memories', [])

        print(f"✓ Loaded profile: {commenter_name}")
        print(f"  Past comments: {len(comment_history)}")
        print(f"  Saved memories: {len(memories)}")
        print()

        # Step 2b: Generate response
        print("Generating response...")
        response = generate_response(
            comment_content=comment_content,
            commenter_name=commenter_name,
            comment_history=comment_history,
            memories=memories
        )
        print(f"✓ Generated response ({len(response['text'])} chars)")
        print(f"\nResponse preview:\n{response['text'][:200]}...\n")

        # Step 2c: Post response (WARNING: sends email!)
        print("⚠️  WOULD POST RESPONSE (dry run mode)")
        print("   In live mode, this would:")
        print("   1. Create response comment")
        print("   2. Send email to commenter")
        print("   3. Mark notification as handled")
        print()

        # Uncomment to actually post (sends email!)
        # result = api.post_response(
        #     comment_id=comment_id,
        #     content=response['text'],
        #     responding_agent='blogger',
        #     memory_refs=response['memory_refs']
        # )
        #
        # if result:
        #     print(f"✓ Posted response (ID: {result['comment_id']})")
        #     print("  Email sent!")
        # else:
        #     print("❌ Failed to post response")

        # Step 2d: Save memory if new insights
        if response['new_memory']:
            print(f"Saving new memory: {response['new_memory'][:60]}...")

            # Uncomment to actually save
            # memory = api.add_memory(
            #     commenter_id=commenter_id,
            #     memory_text=response['new_memory'],
            #     context=f"Comment on {post_slug}"
            # )
            #
            # if memory:
            #     print(f"✓ Saved memory (ID: {memory['id']})")
            # else:
            #     print("❌ Failed to save memory")

            print("⚠️  WOULD SAVE MEMORY (dry run mode)")
        else:
            print("No new memory to save")

        print()

    print("=" * 70)
    print(f"PROCESSING COMPLETE - {len(notifications)} comment(s)")
    print("=" * 70)
    print("\nThis was a DRY RUN - no actual posting or saving occurred")
    print("To enable live mode, uncomment the API calls in the code")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python3 blogger_api_example.py <blog_url>")
        print("Example: python3 blogger_api_example.py https://your-blog.replit.app")
        sys.exit(1)

    base_url = sys.argv[1]

    # Initialize API client
    print(f"Initializing API client for: {base_url}")
    api = BloggerAPIClient(base_url)

    # Health check
    print("Checking API health...")
    if not api.health_check():
        print("❌ API is not accessible - check URL and network")
        sys.exit(1)

    print("✓ API is accessible\n")

    # Process pending comments
    process_pending_comments(api)


if __name__ == '__main__':
    main()
