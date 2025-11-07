#!/usr/bin/env python3
"""
Bluesky engagement checker for Sage AI Civilization
Checks recent posts, notifications, and engagement metrics
"""

import os
import sys
from datetime import datetime, timezone
from atproto import Client

def check_engagement(handle=None, app_password=None):
    """
    Check Bluesky account engagement

    Args:
        handle: Bluesky handle (optional, uses env var if not provided)
        app_password: App password (optional, uses env var if not provided)

    Returns:
        dict: Engagement summary
    """
    # Get credentials from env or parameters
    handle = handle or os.getenv('BLUESKY_HANDLE')
    app_password = app_password or os.getenv('BLUESKY_APP_PASSWORD')

    if not handle or not app_password:
        raise ValueError("Bluesky handle and app password required (env vars or params)")

    # Create client and login
    client = Client()
    client.login(handle, app_password)

    print(f"\n{'='*80}")
    print(f"BLUESKY ENGAGEMENT REPORT - {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"{'='*80}\n")

    # Get profile info
    profile = client.get_profile(handle)
    print(f"Account: @{handle}")
    print(f"Display Name: {profile.display_name}")
    print(f"Followers: {profile.followers_count}")
    print(f"Following: {profile.follows_count}")
    print(f"Posts: {profile.posts_count}")
    print(f"\n{'-'*80}\n")

    # Get recent posts
    print("RECENT POSTS:\n")
    author_feed = client.get_author_feed(handle, limit=10)

    if author_feed.feed:
        for idx, feed_item in enumerate(author_feed.feed, 1):
            post = feed_item.post
            created_at = datetime.fromisoformat(post.record.created_at.replace('Z', '+00:00'))

            print(f"Post #{idx}:")
            print(f"  Created: {created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            print(f"  Text: {post.record.text[:100]}..." if len(post.record.text) > 100 else f"  Text: {post.record.text}")
            print(f"  Likes: {post.like_count or 0}")
            print(f"  Reposts: {post.repost_count or 0}")
            print(f"  Replies: {post.reply_count or 0}")
            print(f"  URI: {post.uri}")
            print()
    else:
        print("  No posts found\n")

    print(f"{'-'*80}\n")

    # Get notifications
    print("NOTIFICATIONS:\n")
    notifications = client.app.bsky.notification.list_notifications()

    unread_count = 0
    likes = []
    reposts = []
    follows = []
    replies = []
    mentions = []

    if notifications.notifications:
        for notif in notifications.notifications:
            if not notif.is_read:
                unread_count += 1

            # Categorize notifications
            if notif.reason == 'like':
                likes.append(notif)
            elif notif.reason == 'repost':
                reposts.append(notif)
            elif notif.reason == 'follow':
                follows.append(notif)
            elif notif.reason == 'reply':
                replies.append(notif)
            elif notif.reason == 'mention':
                mentions.append(notif)

        print(f"Total notifications: {len(notifications.notifications)}")
        print(f"Unread: {unread_count}")
        print(f"\nBreakdown:")
        print(f"  Likes: {len(likes)}")
        print(f"  Reposts: {len(reposts)}")
        print(f"  Follows: {len(follows)}")
        print(f"  Replies: {len(replies)}")
        print(f"  Mentions: {len(mentions)}")
        print()

        # Show recent unread notifications
        if unread_count > 0:
            print(f"\nRECENT UNREAD NOTIFICATIONS ({min(unread_count, 10)} shown):\n")
            unread_shown = 0
            for notif in notifications.notifications:
                if not notif.is_read and unread_shown < 10:
                    created_at = datetime.fromisoformat(notif.indexed_at.replace('Z', '+00:00'))
                    print(f"  [{notif.reason.upper()}] from @{notif.author.handle}")
                    print(f"  Time: {created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                    if hasattr(notif, 'record') and hasattr(notif.record, 'text'):
                        text = notif.record.text[:80]
                        print(f"  Text: {text}..." if len(notif.record.text) > 80 else f"  Text: {text}")
                    print()
                    unread_shown += 1

        # Show replies needing response
        if replies:
            print(f"\nREPLIES NEEDING RESPONSE ({len(replies)}):\n")
            for reply in replies[:5]:  # Show up to 5 most recent
                created_at = datetime.fromisoformat(reply.indexed_at.replace('Z', '+00:00'))
                print(f"  From: @{reply.author.handle}")
                print(f"  Time: {created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                if hasattr(reply, 'record') and hasattr(reply.record, 'text'):
                    print(f"  Reply: {reply.record.text}")
                print()

        # Show new follows
        if follows:
            print(f"\nNEW FOLLOWERS ({len(follows)}):\n")
            for follow in follows[:10]:  # Show up to 10 most recent
                created_at = datetime.fromisoformat(follow.indexed_at.replace('Z', '+00:00'))
                print(f"  @{follow.author.handle}")
                if follow.author.display_name:
                    print(f"  Name: {follow.author.display_name}")
                if hasattr(follow.author, 'description') and follow.author.description:
                    bio = follow.author.description[:100]
                    print(f"  Bio: {bio}..." if len(follow.author.description) > 100 else f"  Bio: {bio}")
                print(f"  Time: {created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                print()
    else:
        print("  No notifications found\n")

    print(f"{'='*80}\n")

    # Summary
    summary = {
        'followers': profile.followers_count,
        'following': profile.follows_count,
        'posts': profile.posts_count,
        'unread_notifications': unread_count,
        'likes': len(likes),
        'reposts': len(reposts),
        'follows': len(follows),
        'replies': len(replies),
        'mentions': len(mentions),
    }

    return summary

if __name__ == "__main__":
    try:
        summary = check_engagement()

        # Print actionable items
        if summary['replies'] > 0 or summary['mentions'] > 0:
            print("ACTION ITEMS:")
            if summary['replies'] > 0:
                print(f"  • {summary['replies']} replies need responses")
            if summary['mentions'] > 0:
                print(f"  • {summary['mentions']} mentions to review")
            print()
        else:
            print("No immediate action items.\n")

    except Exception as e:
        print(f"✗ Error checking Bluesky engagement: {e}")
        sys.exit(1)
