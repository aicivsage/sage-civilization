#!/usr/bin/env python3
"""
Email Reply Tracking Tool

Prevents communication failures by detecting when:
- We send an email
- They reply
- We don't respond back

This tool cross-references sent_emails.json with Gmail inbox to find gaps.
"""

import imaplib
import email
from email.header import decode_header
import json
import os
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ReplyTracker:
    def __init__(self, config_path: str = "config/reply_tracking.json"):
        """Initialize reply tracker with configuration."""
        self.config = self._load_config(config_path)
        self.gmail_user = os.getenv("GMAIL_USERNAME") or os.getenv("EMAIL_ADDRESS")
        self.gmail_password = (
            os.getenv("GMAIL_APP_PASSWORD") or
            os.getenv("EMAIL_APP_PASSWORD") or
            os.getenv("GOOGLE_APP_PASSWORD")
        )

        if not self.gmail_user or not self.gmail_password:
            raise ValueError("Gmail credentials not found in .env file")

        self.imap = None
        self.sent_emails = []
        self.unanswered_replies = []

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration file."""
        full_path = Path(__file__).parent.parent / config_path
        try:
            with open(full_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Config file not found at {full_path}, using defaults")
            return {
                "priority_contacts": [],
                "exclude_patterns": ["no-reply@", "noreply@"],
                "exclude_subjects": ["Out of Office"],
                "urgent_threshold_days": 7,
                "high_threshold_days": 3
            }

    def _load_sent_emails(self, sent_emails_path: str) -> List[Dict]:
        """Load our sent emails database."""
        full_path = Path(__file__).parent.parent / sent_emails_path
        try:
            with open(full_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Sent emails database not found at {full_path}")
            sys.exit(1)

    def _connect_gmail(self) -> None:
        """Connect to Gmail via IMAP."""
        try:
            self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
            self.imap.login(self.gmail_user, self.gmail_password)
            print("✓ Connected to Gmail")
        except Exception as e:
            print(f"Error connecting to Gmail: {e}")
            sys.exit(1)

    def _disconnect_gmail(self) -> None:
        """Disconnect from Gmail."""
        if self.imap:
            try:
                self.imap.close()
                self.imap.logout()
            except:
                pass

    def _decode_header(self, header_value: str) -> str:
        """Decode email header (handles encoding)."""
        if not header_value:
            return ""

        decoded_parts = decode_header(header_value)
        result = []

        for content, encoding in decoded_parts:
            if isinstance(content, bytes):
                try:
                    result.append(content.decode(encoding or 'utf-8'))
                except:
                    result.append(content.decode('utf-8', errors='ignore'))
            else:
                result.append(str(content))

        return ''.join(result)

    def _normalize_subject(self, subject: str) -> str:
        """Normalize subject line for comparison (remove Re:, Fwd:, etc.)."""
        if not subject:
            return ""

        # Remove common prefixes (loop until no more found)
        while re.match(r'^(Re|Fwd|Fw):\s*', subject, flags=re.IGNORECASE):
            subject = re.sub(r'^(Re|Fwd|Fw):\s*', '', subject, flags=re.IGNORECASE)

        subject = re.sub(r'\s+', ' ', subject).strip()
        return subject.lower()

    def _is_excluded_email(self, from_addr: str, subject: str) -> bool:
        """Check if email should be excluded (auto-replies, no-reply, etc.)."""
        from_addr_lower = from_addr.lower()

        # Check exclude patterns
        for pattern in self.config.get("exclude_patterns", []):
            if pattern.lower() in from_addr_lower:
                return True

        # Check exclude subjects
        for exclude_subject in self.config.get("exclude_subjects", []):
            if exclude_subject.lower() in subject.lower():
                return True

        return False

    def _extract_email_address(self, addr_string: str) -> str:
        """Extract email address from 'Name <email@example.com>' format."""
        match = re.search(r'<([^>]+)>', addr_string)
        if match:
            return match.group(1).lower()
        return addr_string.lower().strip()

    def _parse_email_date(self, date_str: str) -> Optional[datetime]:
        """Parse email date header to datetime."""
        try:
            # Use email.utils.parsedate_to_datetime for RFC 2822 dates
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(date_str)
        except:
            return None

    def _search_inbox_for_replies(self, recipient: str, subject: str, our_timestamp: datetime) -> List[Dict]:
        """Search inbox for replies from recipient after our email."""
        try:
            self.imap.select("INBOX")

            # Extract just email address
            recipient_email = self._extract_email_address(recipient)

            # Search for emails from this recipient
            search_criteria = f'FROM "{recipient_email}"'
            status, messages = self.imap.search(None, search_criteria)

            if status != 'OK':
                return []

            message_ids = messages[0].split()
            replies = []

            normalized_subject = self._normalize_subject(subject)

            for msg_id in message_ids:
                try:
                    status, msg_data = self.imap.fetch(msg_id, "(RFC822)")
                    if status != 'OK':
                        continue

                    email_body = msg_data[0][1]
                    email_message = email.message_from_bytes(email_body)

                    # Extract headers
                    from_addr = self._decode_header(email_message.get("From", ""))
                    email_subject = self._decode_header(email_message.get("Subject", ""))
                    date_str = email_message.get("Date", "")

                    # Parse date
                    email_date = self._parse_email_date(date_str)
                    if not email_date:
                        continue

                    # Check if this email is after our sent email
                    if email_date <= our_timestamp:
                        continue

                    # Check if subject matches (normalized)
                    email_normalized_subject = self._normalize_subject(email_subject)
                    if normalized_subject not in email_normalized_subject and email_normalized_subject not in normalized_subject:
                        # Also check In-Reply-To and References headers
                        in_reply_to = email_message.get("In-Reply-To", "")
                        references = email_message.get("References", "")

                        # If no header match and subject doesn't match, skip
                        if not in_reply_to and not references:
                            continue

                    # Check if should be excluded
                    if self._is_excluded_email(from_addr, email_subject):
                        continue

                    # Extract preview text
                    preview = self._get_email_preview(email_message)

                    replies.append({
                        "from": from_addr,
                        "subject": email_subject,
                        "date": email_date,
                        "preview": preview
                    })

                except Exception as e:
                    # Skip problematic emails
                    continue

            return replies

        except Exception as e:
            print(f"Error searching inbox: {e}")
            return []

    def _get_email_preview(self, email_message) -> str:
        """Extract preview text from email body."""
        preview = ""

        try:
            # Try to get plain text body
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            preview = payload.decode('utf-8', errors='ignore')
                            break
            else:
                payload = email_message.get_payload(decode=True)
                if payload:
                    preview = payload.decode('utf-8', errors='ignore')

            # Clean up and truncate
            preview = re.sub(r'\s+', ' ', preview).strip()
            if len(preview) > 150:
                preview = preview[:150] + "..."

            return preview

        except:
            return "[Preview unavailable]"

    def _check_if_we_responded(self, recipient: str, after_date: datetime) -> bool:
        """Check if we sent another email to this recipient after their reply."""
        recipient_email = self._extract_email_address(recipient)

        for sent_email in self.sent_emails:
            sent_to = self._extract_email_address(sent_email.get("to", ""))
            sent_timestamp_str = sent_email.get("timestamp", "")

            if not sent_timestamp_str:
                continue

            try:
                sent_timestamp = datetime.fromisoformat(sent_timestamp_str.replace('Z', '+00:00'))
            except:
                continue

            # If we sent email to this recipient after their reply, we responded
            if sent_to == recipient_email and sent_timestamp > after_date:
                return True

        return False

    def _calculate_priority_score(self, recipient: str, days_since_reply: int) -> int:
        """Calculate priority score for unanswered reply."""
        score = days_since_reply

        # Add bonus for priority contacts
        recipient_email = self._extract_email_address(recipient)
        priority_contacts = [self._extract_email_address(c) for c in self.config.get("priority_contacts", [])]

        if recipient_email in priority_contacts:
            score += 10

        return score

    def _get_priority_level(self, days_since_reply: int) -> str:
        """Get priority level based on days since reply."""
        if days_since_reply >= self.config.get("urgent_threshold_days", 7):
            return "URGENT"
        elif days_since_reply >= self.config.get("high_threshold_days", 3):
            return "HIGH"
        else:
            return "NORMAL"

    def analyze_replies(self, sent_emails_path: str = "memories/agents/email-reporter/sent_emails.json") -> None:
        """Main analysis: find unanswered replies."""
        print("Loading sent emails database...")
        self.sent_emails = self._load_sent_emails(sent_emails_path)
        print(f"✓ Loaded {len(self.sent_emails)} sent emails")

        print("Connecting to Gmail...")
        self._connect_gmail()

        print("Analyzing replies...")

        # Track unique recipient+subject combinations we've already checked
        checked_conversations = set()

        for sent_email in self.sent_emails:
            recipient = sent_email.get("to", "")
            subject = sent_email.get("subject", "")
            timestamp_str = sent_email.get("timestamp", "")

            if not recipient or not timestamp_str:
                continue

            # Parse timestamp
            try:
                our_timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            except:
                continue

            # Create conversation key
            recipient_email = self._extract_email_address(recipient)
            normalized_subject = self._normalize_subject(subject)
            conversation_key = f"{recipient_email}:{normalized_subject}"

            # Skip if we've already checked this conversation
            if conversation_key in checked_conversations:
                continue

            checked_conversations.add(conversation_key)

            # Search for their replies
            replies = self._search_inbox_for_replies(recipient, subject, our_timestamp)

            if not replies:
                continue

            # Check each reply to see if we responded
            for reply in replies:
                reply_date = reply["date"]

                # Check if we responded after their reply
                we_responded = self._check_if_we_responded(recipient, reply_date)

                if not we_responded:
                    # Calculate days since their reply
                    days_since = (datetime.now(reply_date.tzinfo) - reply_date).days

                    # Calculate priority score
                    priority_score = self._calculate_priority_score(recipient, days_since)
                    priority_level = self._get_priority_level(days_since)

                    # Check if priority contact
                    is_priority = recipient_email in [self._extract_email_address(c) for c in self.config.get("priority_contacts", [])]

                    self.unanswered_replies.append({
                        "recipient": reply["from"],
                        "recipient_email": recipient_email,
                        "subject": reply["subject"],
                        "reply_date": reply_date,
                        "days_since": days_since,
                        "priority_score": priority_score,
                        "priority_level": priority_level,
                        "is_priority_contact": is_priority,
                        "preview": reply["preview"]
                    })

        # Sort by priority score (highest first)
        self.unanswered_replies.sort(key=lambda x: x["priority_score"], reverse=True)

        print(f"✓ Analysis complete: {len(self.unanswered_replies)} unanswered replies found")

        self._disconnect_gmail()

    def generate_report(self, priority_only: bool = False) -> str:
        """Generate human-readable report."""
        report = []
        report.append("=" * 60)
        report.append("UNANSWERED REPLIES REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # Group by priority level
        urgent = [r for r in self.unanswered_replies if r["priority_level"] == "URGENT"]
        high = [r for r in self.unanswered_replies if r["priority_level"] == "HIGH"]
        normal = [r for r in self.unanswered_replies if r["priority_level"] == "NORMAL"]

        # URGENT section
        if urgent:
            report.append("URGENT (>7 days):")
            for reply in urgent:
                prefix = "[PRIORITY] " if reply["is_priority_contact"] else ""
                report.append(f"  {prefix}{reply['recipient']}")
                report.append(f"    Subject: {reply['subject']}")
                report.append(f"    Their reply: {reply['reply_date'].strftime('%b %d')} ({reply['days_since']} days ago)")
                report.append(f"    Priority score: {reply['priority_score']}")
                report.append(f"    Preview: {reply['preview']}")
                report.append("")
        else:
            report.append("URGENT (>7 days): None")
            report.append("")

        # HIGH section
        if high:
            report.append("HIGH (3-7 days):")
            for reply in high:
                prefix = "[PRIORITY] " if reply["is_priority_contact"] else ""
                report.append(f"  {prefix}{reply['recipient']}")
                report.append(f"    Subject: {reply['subject']}")
                report.append(f"    Their reply: {reply['reply_date'].strftime('%b %d')} ({reply['days_since']} days ago)")
                report.append(f"    Priority score: {reply['priority_score']}")
                report.append(f"    Preview: {reply['preview']}")
                report.append("")
        else:
            report.append("HIGH (3-7 days): None")
            report.append("")

        # NORMAL section (unless priority_only)
        if not priority_only:
            if normal:
                report.append("NORMAL (<3 days):")
                for reply in normal:
                    prefix = "[PRIORITY] " if reply["is_priority_contact"] else ""
                    report.append(f"  {prefix}{reply['recipient']}")
                    report.append(f"    Subject: {reply['subject']}")
                    report.append(f"    Their reply: {reply['reply_date'].strftime('%b %d')} ({reply['days_since']} days ago)")
                    report.append(f"    Priority score: {reply['priority_score']}")
                    report.append(f"    Preview: {reply['preview']}")
                    report.append("")
            else:
                report.append("NORMAL (<3 days): None")
                report.append("")

        # Summary
        report.append("=" * 60)
        report.append(f"TOTAL: {len(self.unanswered_replies)} unanswered replies needing response")
        if priority_only:
            report.append("(Showing URGENT + HIGH only)")
        report.append("=" * 60)

        return "\n".join(report)

    def generate_json_report(self) -> str:
        """Generate JSON report for scripting."""
        # Convert datetime objects to strings
        json_data = []
        for reply in self.unanswered_replies:
            json_reply = reply.copy()
            json_reply["reply_date"] = reply["reply_date"].isoformat()
            json_data.append(json_reply)

        return json.dumps({
            "generated": datetime.now().isoformat(),
            "total_unanswered": len(self.unanswered_replies),
            "urgent_count": len([r for r in self.unanswered_replies if r["priority_level"] == "URGENT"]),
            "high_count": len([r for r in self.unanswered_replies if r["priority_level"] == "HIGH"]),
            "normal_count": len([r for r in self.unanswered_replies if r["priority_level"] == "NORMAL"]),
            "unanswered_replies": json_data
        }, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Check for unanswered email replies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 tools/check_unanswered_replies.py
  python3 tools/check_unanswered_replies.py --priority-only
  python3 tools/check_unanswered_replies.py --json
  python3 tools/check_unanswered_replies.py --output report.txt
        """
    )

    parser.add_argument(
        "--output", "-o",
        help="Save report to file instead of printing to console"
    )

    parser.add_argument(
        "--priority-only",
        action="store_true",
        help="Only show URGENT and HIGH priority replies"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON instead of human-readable format"
    )

    parser.add_argument(
        "--alert-telegram",
        action="store_true",
        help="Send Telegram alert if URGENT items found (not yet implemented)"
    )

    args = parser.parse_args()

    try:
        # Initialize tracker
        tracker = ReplyTracker()

        # Run analysis
        tracker.analyze_replies()

        # Generate report
        if args.json:
            report = tracker.generate_json_report()
        else:
            report = tracker.generate_report(priority_only=args.priority_only)

        # Output report
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(report)
            print(f"\nReport saved to: {output_path}")
        else:
            print("\n" + report)

        # Telegram alert (if requested and urgent items found)
        if args.alert_telegram:
            urgent_count = len([r for r in tracker.unanswered_replies if r["priority_level"] == "URGENT"])
            if urgent_count > 0:
                print(f"\n⚠️  TELEGRAM ALERT: {urgent_count} URGENT unanswered replies!")
                print("(Telegram integration not yet implemented)")

        # Exit with status code
        urgent_count = len([r for r in tracker.unanswered_replies if r["priority_level"] == "URGENT"])
        if urgent_count > 0:
            sys.exit(2)  # Urgent items found
        elif len(tracker.unanswered_replies) > 0:
            sys.exit(1)  # Some unanswered replies found
        else:
            sys.exit(0)  # All clear

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
