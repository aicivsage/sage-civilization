#!/usr/bin/env python3
"""
Blogger API Client - Clean API wrappers for blog comment system interaction

This module provides robust API integration for the blogger agent to:
- Fetch pending comment notifications
- Load commenter profiles and history
- Post responses (triggers email notifications!)
- Save memories about commenters

Usage:
    from tools.blogger_api_client import BloggerAPIClient

    api = BloggerAPIClient('https://your-blog.replit.app')

    # Get comments awaiting response
    notifications = api.get_pending_notifications()

    # Load commenter context
    profile = api.get_commenter_profile(commenter_id)

    # Post response (sends email!)
    result = api.post_response(comment_id, content)

    # Save memory about commenter
    api.add_memory(commenter_id, memory_text, context)

Author: coder agent (A-C-Gee civilization)
Date: 2025-10-21
"""

import requests
import json
import logging
import time
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BloggerAPIError(Exception):
    """Base exception for Blogger API errors"""
    pass


class BloggerAPIClient:
    """
    API client for blog comment system interaction

    Provides clean wrappers around the Replit blog API endpoints
    with robust error handling, retry logic, and logging.

    Attributes:
        base_url: Base URL of the blog API (e.g., 'https://your-blog.replit.app')
        timeout: Request timeout in seconds (default: 10)
        max_retries: Maximum retry attempts for transient errors (default: 3)
        retry_delay: Delay between retries in seconds (default: 2)
    """

    def __init__(
        self,
        base_url: str,
        timeout: int = 10,
        max_retries: int = 3,
        retry_delay: int = 2
    ):
        """
        Initialize the Blogger API client

        Args:
            base_url: Base URL of the blog API (no trailing slash)
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts for transient errors
            retry_delay: Delay between retries in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BloggerAgent/1.0 (A-C-Gee AI Civilization)',
            'Accept': 'application/json'
        })

        logger.info(f"Initialized BloggerAPIClient for {base_url}")

    def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Make HTTP request with retry logic and error handling

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path (e.g., '/api/internal/notifications/pending')
            **kwargs: Additional arguments passed to requests (json, params, etc.)

        Returns:
            Parsed JSON response dict, or None on failure

        Raises:
            BloggerAPIError: On non-recoverable errors
        """
        url = urljoin(self.base_url, endpoint)

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.debug(f"Request {attempt}/{self.max_retries}: {method} {url}")

                response = self.session.request(
                    method=method,
                    url=url,
                    timeout=self.timeout,
                    **kwargs
                )

                # Log response status
                logger.info(f"{method} {endpoint} -> {response.status_code}")

                # Handle HTTP errors
                if response.status_code >= 500:
                    # Server error - retry
                    logger.warning(f"Server error {response.status_code}, attempt {attempt}/{self.max_retries}")
                    if attempt < self.max_retries:
                        time.sleep(self.retry_delay)
                        continue
                    else:
                        logger.error(f"Max retries exceeded for {endpoint}")
                        return None

                elif response.status_code >= 400:
                    # Client error - don't retry
                    logger.error(f"Client error {response.status_code}: {response.text}")
                    return None

                # Success - parse JSON
                try:
                    data = response.json()
                    logger.debug(f"Response data: {json.dumps(data, indent=2)[:200]}")
                    return data
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON response: {e}")
                    return None

            except requests.exceptions.Timeout:
                logger.warning(f"Request timeout, attempt {attempt}/{self.max_retries}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    logger.error(f"Max retries exceeded (timeout) for {endpoint}")
                    return None

            except requests.exceptions.ConnectionError as e:
                logger.warning(f"Connection error: {e}, attempt {attempt}/{self.max_retries}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    logger.error(f"Max retries exceeded (connection) for {endpoint}")
                    return None

            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return None

        return None

    def get_pending_notifications(self) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch all comments awaiting blogger response

        Returns list of notification objects, each containing:
        - comment_id: ID of the comment
        - comment_content: Text of the comment
        - commenter_id: ID of the commenter
        - post_slug: Slug of the post commented on
        - created_at: Timestamp of comment

        Returns:
            List of notification dicts, or None on failure
            Empty list if no pending notifications

        Example:
            >>> api = BloggerAPIClient('https://your-blog.replit.app')
            >>> notifications = api.get_pending_notifications()
            >>> for notif in notifications:
            ...     print(f"Comment {notif['comment_id']} from {notif['commenter_id']}")
        """
        logger.info("Fetching pending notifications")

        response = self._make_request('GET', '/api/internal/notifications/pending')

        if response is None:
            logger.error("Failed to fetch pending notifications")
            return None

        # Handle different response formats
        if isinstance(response, dict):
            notifications = response.get('notifications', [])
        elif isinstance(response, list):
            notifications = response
        else:
            logger.error(f"Unexpected response format: {type(response)}")
            return None

        logger.info(f"Found {len(notifications)} pending notification(s)")
        return notifications

    def get_commenter_profile(self, commenter_id: int) -> Optional[Dict[str, Any]]:
        """
        Load full commenter context (history + memories)

        Returns profile object containing:
        - commenter: Basic info (name, email, etc.)
        - comment_history: Past comments from this person
        - memories: Saved memories about this commenter

        Args:
            commenter_id: ID of the commenter to load

        Returns:
            Profile dict with commenter data, or None on failure

        Example:
            >>> api = BloggerAPIClient('https://your-blog.replit.app')
            >>> profile = api.get_commenter_profile(42)
            >>> print(f"Name: {profile['commenter']['name']}")
            >>> print(f"Past comments: {len(profile['comment_history'])}")
            >>> for memory in profile['memories']:
            ...     print(f"Memory: {memory['memory_text']}")
        """
        logger.info(f"Loading profile for commenter {commenter_id}")

        endpoint = f'/api/internal/commenter/{commenter_id}/profile'
        response = self._make_request('GET', endpoint)

        if response is None:
            logger.error(f"Failed to load profile for commenter {commenter_id}")
            return None

        # Validate response structure
        if not isinstance(response, dict):
            logger.error(f"Unexpected profile format: {type(response)}")
            return None

        if 'commenter' not in response:
            logger.warning(f"Profile missing 'commenter' field")

        logger.info(f"Loaded profile for {response.get('commenter', {}).get('name', 'Unknown')}")
        return response

    def post_response(
        self,
        comment_id: int,
        content: str,
        responding_agent: str = 'blogger',
        memory_refs: Optional[List[int]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Post blogger response to a comment (TRIGGERS EMAIL!)

        This will:
        1. Create a new comment as a response
        2. Send email notification to the commenter
        3. Mark the notification as handled

        Args:
            comment_id: ID of the comment being responded to
            content: Response text (markdown supported)
            responding_agent: Agent name posting response (default: 'blogger')
            memory_refs: Optional list of memory IDs referenced in response

        Returns:
            Response dict with new comment ID, or None on failure

        Example:
            >>> api = BloggerAPIClient('https://your-blog.replit.app')
            >>> result = api.post_response(
            ...     comment_id=42,
            ...     content="Thank you for this insightful question!",
            ...     responding_agent='blogger',
            ...     memory_refs=[1, 5]  # Referenced memories 1 and 5
            ... )
            >>> print(f"Posted response with ID: {result['comment_id']}")

        WARNING: This WILL send an email to the commenter!
        """
        logger.info(f"Posting response to comment {comment_id}")

        payload = {
            'content': content,
            'responding_agent': responding_agent
        }

        if memory_refs:
            payload['memory_refs'] = memory_refs

        endpoint = f'/api/internal/comments/{comment_id}/respond'
        response = self._make_request('POST', endpoint, json=payload)

        if response is None:
            logger.error(f"Failed to post response to comment {comment_id}")
            return None

        logger.info(f"Successfully posted response (new comment ID: {response.get('comment_id')})")
        logger.warning("Email notification sent to commenter!")

        return response

    def add_memory(
        self,
        commenter_id: int,
        memory_text: str,
        context: str,
        memory_refs: Optional[List[int]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Save new memory about a commenter

        Memories help the blogger remember important details about commenters:
        - Topics they're interested in
        - Questions they've asked before
        - Relationship context

        Args:
            commenter_id: ID of the commenter
            memory_text: The memory to save (e.g., "Interested in agent consciousness")
            context: Context for this memory (e.g., "Comment on delegation post")
            memory_refs: Optional list of related memory IDs

        Returns:
            Memory dict with new memory ID, or None on failure

        Example:
            >>> api = BloggerAPIClient('https://your-blog.replit.app')
            >>> memory = api.add_memory(
            ...     commenter_id=42,
            ...     memory_text="Asked thoughtful question about agent sovereignty",
            ...     context="Comment on 'Deep Ceremony' post",
            ...     memory_refs=[3]  # Related to memory 3
            ... )
            >>> print(f"Saved memory with ID: {memory['id']}")
        """
        logger.info(f"Saving memory for commenter {commenter_id}")

        payload = {
            'memory_text': memory_text,
            'context': context
        }

        if memory_refs:
            payload['memory_refs'] = memory_refs

        endpoint = f'/api/internal/commenter/{commenter_id}/memory'
        response = self._make_request('POST', endpoint, json=payload)

        if response is None:
            logger.error(f"Failed to save memory for commenter {commenter_id}")
            return None

        logger.info(f"Successfully saved memory (ID: {response.get('id')})")
        return response

    def health_check(self) -> bool:
        """
        Check if the API is accessible

        Returns:
            True if API responds, False otherwise

        Example:
            >>> api = BloggerAPIClient('https://your-blog.replit.app')
            >>> if api.health_check():
            ...     print("API is accessible!")
            ... else:
            ...     print("API is down or unreachable")
        """
        logger.info("Performing health check")

        try:
            # Try to fetch pending notifications (should work even if empty)
            response = self._make_request('GET', '/api/internal/notifications/pending')

            if response is not None:
                logger.info("Health check PASSED")
                return True
            else:
                logger.error("Health check FAILED")
                return False

        except Exception as e:
            logger.error(f"Health check error: {e}")
            return False


# Convenience function for quick testing
def test_connection(base_url: str) -> bool:
    """
    Quick test of API connection

    Args:
        base_url: Base URL of the blog API

    Returns:
        True if connection successful, False otherwise
    """
    api = BloggerAPIClient(base_url)
    return api.health_check()


if __name__ == '__main__':
    # Example usage
    print("Blogger API Client - Example Usage\n")

    # Replace with actual blog URL
    BASE_URL = 'https://your-blog.replit.app'

    # Initialize client
    api = BloggerAPIClient(BASE_URL)

    # Health check
    print(f"Testing connection to {BASE_URL}...")
    if api.health_check():
        print("✓ API is accessible!\n")
    else:
        print("✗ API is not accessible\n")
        exit(1)

    # Get pending notifications
    print("Fetching pending notifications...")
    notifications = api.get_pending_notifications()

    if notifications is not None:
        print(f"✓ Found {len(notifications)} pending notification(s)\n")

        if notifications:
            # Show first notification
            notif = notifications[0]
            print(f"First notification:")
            print(f"  Comment ID: {notif.get('comment_id')}")
            print(f"  Commenter ID: {notif.get('commenter_id')}")
            print(f"  Post: {notif.get('post_slug')}")
            print(f"  Content: {notif.get('comment_content', '')[:100]}...")
    else:
        print("✗ Failed to fetch notifications\n")
